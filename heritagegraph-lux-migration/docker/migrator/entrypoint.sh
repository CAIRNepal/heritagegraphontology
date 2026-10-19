#!/usr/bin/env bash
# =============================================================================
# Migrator entrypoint — runs the 7-phase LUX → HeritageGraph pipeline.
# =============================================================================
# Each phase writes a flag in /work/state/. If a flag exists, the phase is
# skipped — the whole pipeline is therefore safely idempotent. Tear down by
# emptying /work/state (or use `make reset`).
#
# Phases:
#   P1  fetch_dump     — download LUX N-Quads dump (or skip if RING_MODE=crawl)
#   P2  load_lux       — push the dump into Oxigraph <https://lux.collections.yale.edu/>
#   P3  load_hg        — push HeritageGraph.ttl + alignment.ttl into their graphs
#   P4  transform      — run lux_to_hg_migration.sparql (batched INSERT WHERE)
#   P5  validate       — run validation_queries.sparql, V1/V2 are hard gates
#   P6  snapshot       — print snapshot guidance (snapshot is host-side, see Makefile)
#   P7  done           — touch the master flag; subsequent runs are no-ops
# =============================================================================
set -Eeuo pipefail

LOG_DIR=/work/logs
STATE_DIR=/work/state
LUX_DIR=/work/lux
ALIGN_DIR=/work/alignment
QUERIES_DIR=/work/queries

mkdir -p "$LOG_DIR" "$STATE_DIR" "$LUX_DIR"

LOG_FILE="$LOG_DIR/migrator.log"
exec > >(tee -a "$LOG_FILE") 2>&1

ENDPOINT="${OXIGRAPH_ENDPOINT:-http://oxigraph:7878}"
RING_MODE="${RING_MODE:-crawl}"
BATCH_SIZE="${BATCH_SIZE:-50000}"
LIMIT_PER_QUERY="${LIMIT_PER_QUERY:-0}"
# NOTE: There is no canonical public Yale dump URL as of May 2026.
# LUX_DUMP_URL defaults to empty; if set externally we use it, otherwise
# fall through to a path-mounted dump (LUX_DUMP_PATH) or REST crawl.
LUX_DUMP_URL="${LUX_DUMP_URL:-}"
LUX_DUMP_PATH="${LUX_DUMP_PATH:-}"
LUX_FILTER="${LUX_FILTER:-religious heritage}"
CRAWL_RPS="${CRAWL_RPS:-10}"
VALIDATION_MODE="${VALIDATION_MODE:-strict}"

GRAPH_RAW="https://lux.collections.yale.edu/"
GRAPH_HG="https://w3id.org/heritagegraph/"
GRAPH_ALIGN="https://w3id.org/heritagegraph/alignment/lux"
GRAPH_IMPORTED="https://w3id.org/heritagegraph/imported/lux"

# ---------- helpers -----------------------------------------------------------

log()        { echo "[$(date -u +%FT%TZ)] $*"; }
phase_done() { touch "$STATE_DIR/$1.done"; }
phase_check(){ [[ -f "$STATE_DIR/$1.done" ]]; }

sparql_query() {  # $1 = query string, prints raw response
    curl -sS --fail-with-body \
         -H 'Accept: application/sparql-results+json' \
         --data-urlencode "query=$1" \
         "$ENDPOINT/query"
}
sparql_update() { # $1 = update string
    curl -sS --fail-with-body \
         --data-urlencode "update=$1" \
         "$ENDPOINT/update"
}
http_load() {     # $1 = file, $2 = mime, $3 = graph URI
    # N-Quads carry their own graph names — Oxigraph rejects ?graph= when the
    # body already contains named graphs ("Named graphs are not allowed").
    local target="$ENDPOINT/store?graph=$3"
    case "$2" in
        application/n-quads|application/trig) target="$ENDPOINT/store" ;;
    esac
    curl -sS --fail-with-body -X POST \
         -H "Content-Type: $2" \
         --data-binary "@$1" \
         "$target"
}

# Chunked variant for big line-oriented files (N-Triples / N-Quads).
# Oxigraph OOMs on a single multi-hundred-MB POST on a 16 GiB host.
http_load_chunked() {     # $1 = file, $2 = mime, $3 = graph URI, [$4 = lines/chunk]
    local file="$1" mime="$2" graph="$3" chunk_lines="${4:-200000}"
    local total chunks dir part n=0
    total=$(wc -l < "$file")
    dir=$(mktemp -d)
    split -l "$chunk_lines" -d --additional-suffix=.nq "$file" "$dir/chunk."
    chunks=$(ls "$dir"/chunk.*.nq | wc -l)
    log "[load] $file → $chunks chunks of up to $chunk_lines lines (total $total)."
    for part in "$dir"/chunk.*.nq; do
        n=$((n+1))
        log "[load] chunk $n/$chunks ($(wc -l <"$part") lines)…"
        if ! http_load "$part" "$mime" "$graph"; then
            log "[load] chunk $n failed."
            rm -rf "$dir"
            return 1
        fi
    done
    rm -rf "$dir"
}

wait_for_oxigraph() {
    local n=0
    until curl -sf "$ENDPOINT/" >/dev/null 2>&1; do
        n=$((n+1))
        if (( n > 60 )); then
            log "FATAL: Oxigraph at $ENDPOINT did not respond within 5 minutes."
            exit 2
        fi
        log "waiting for Oxigraph at $ENDPOINT… (${n}/60)"
        sleep 5
    done
    log "Oxigraph is up."
}

# ---------- master pre-flight -------------------------------------------------

if phase_check master; then
    log "Master flag found — migration already complete. Exiting 0."
    log "To force a re-run: docker compose run --rm migrator rm /work/state/master.done"
    exit 0
fi

log "================================================================="
log "LUX → HeritageGraph migrator starting"
log "  RING_MODE        = $RING_MODE"
log "  BATCH_SIZE       = $BATCH_SIZE"
log "  LIMIT_PER_QUERY  = $LIMIT_PER_QUERY  (0 = unlimited)"
log "  ENDPOINT         = $ENDPOINT"
log "  VALIDATION_MODE  = $VALIDATION_MODE"
log "================================================================="

wait_for_oxigraph

# ---------- P1  fetch_dump ----------------------------------------------------
# Three sub-modes — automatically picked based on configuration:
#   1. LUX_DUMP_PATH set + file exists  → use the locally-mounted file (e.g. one
#                                          sent to you by Yale ITS or downloaded
#                                          out-of-band).
#   2. LUX_DUMP_URL set                 → curl the URL into /work/lux/lux.nq.gz
#   3. otherwise                        → REST crawl via /api/search/* paginated.

DUMP_FILE="$LUX_DIR/lux.nq"
DUMP_GZ="$LUX_DIR/lux.nq.gz"

if phase_check fetch_dump; then
    log "[P1] fetch_dump — already done."
elif [[ -n "$LUX_DUMP_PATH" && -f "$LUX_DUMP_PATH" ]]; then
    log "[P1] fetch_dump — using locally-mounted dump at $LUX_DUMP_PATH"
    # Symlink into the canonical place so P2 sees it as $DUMP_FILE.
    case "$LUX_DUMP_PATH" in
        *.gz) cp "$LUX_DUMP_PATH" "$DUMP_GZ"; pigz -dk "$DUMP_GZ" ;;
        *)    ln -sf "$LUX_DUMP_PATH" "$DUMP_FILE" ;;
    esac
    phase_done fetch_dump
elif [[ -n "$LUX_DUMP_URL" ]]; then
    log "[P1] fetch_dump — downloading $LUX_DUMP_URL"
    if ! curl -fL --retry 5 --retry-delay 30 -o "$DUMP_GZ" "$LUX_DUMP_URL"; then
        log "[P1] FATAL: dump URL unreachable. See LUX_DATA_DOWNLOAD.md for what to do."
        log "       (Hint: there is no public Yale dump URL as of May 2026."
        log "        Either omit LUX_DUMP_URL — we'll crawl REST — or request one from lux@yale.edu.)"
        exit 2
    fi
    log "[P1] decompressing $DUMP_GZ → $DUMP_FILE"
    pigz -dk "$DUMP_GZ"
    log "[P1] $(wc -l < "$DUMP_FILE") quads on disk."
    phase_done fetch_dump
else
    log "[P1] fetch_dump — no dump configured. Falling back to REST crawl."
    log "       filter='$LUX_FILTER'  rate=${CRAWL_RPS} req/s"
    log "       To use a dump instead: set LUX_DUMP_PATH (mounted) or LUX_DUMP_URL."
    /work/bin/migrate_lux_to_hg.py \
        --mode crawl \
        --filter "$LUX_FILTER" \
        --out "$LUX_DIR/lux_crawled.jsonl" \
        --resume-state "$STATE_DIR/crawl_state.json" \
        --concurrency 4 \
        --max-pages 10000
    phase_done fetch_dump
fi

# ---------- P2  load_lux ------------------------------------------------------

if phase_check load_lux; then
    log "[P2] load_lux — already done."
else
    log "[P2] loading raw LUX into <$GRAPH_RAW>"
    if [[ -f "$DUMP_FILE" ]]; then
        # Stream the file via the SPARQL Graph Store HTTP Protocol. For very
        # large dumps the migrator should be replaced by `pyoxigraph` Store
        # in embedded mode (faster); see MIGRATION_PLAN §4.1.
        http_load_chunked "$DUMP_FILE" "application/n-quads" "$GRAPH_RAW"
    elif [[ -f "$LUX_DIR/lux_crawled.jsonl" ]]; then
        if [[ -s "$LUX_DIR/lux.nq" ]]; then
            log "[P2] lux.nq already present ($(du -h "$LUX_DIR/lux.nq" | cut -f1)) — skipping JSON-LD→N-Quads conversion."
        else
            log "[P2] crawled JSON-LD path — converting to N-Quads first."
            python3 - <<'PY'
import json, pathlib, rdflib
g = rdflib.ConjunctiveGraph()
RAW = "https://lux.collections.yale.edu/"
for line in pathlib.Path("/work/lux/lux_crawled.jsonl").read_text().splitlines():
    if not line.strip(): continue
    try:
        rec = json.loads(line)
        sub = rdflib.Graph(identifier=rdflib.URIRef(RAW))
        sub.parse(data=line, format="json-ld")
        for s,p,o in sub:
            g.add((s,p,o, rdflib.URIRef(RAW)))
    except Exception as e:
        print("skip:", e)
g.serialize(destination="/work/lux/lux.nq", format="nquads")
PY
        fi
        http_load_chunked "$LUX_DIR/lux.nq" "application/n-quads" "$GRAPH_RAW"
    else
        log "FATAL: neither dump nor crawl output found."
        exit 3
    fi
    log "[P2] confirming load…"
    n=$(sparql_query "SELECT (COUNT(*) AS ?c) WHERE { GRAPH <$GRAPH_RAW> { ?s ?p ?o } }" \
        | python3 -c 'import json,sys; r=json.load(sys.stdin)["results"]["bindings"]; print(r[0]["c"]["value"] if r else 0)')
    log "[P2] LUX raw graph has $n triples."
    [[ "$n" -gt 0 ]] || { log "FATAL: load failed (0 triples)."; exit 4; }
    phase_done load_lux
fi

# ---------- P3  load_hg -------------------------------------------------------

if phase_check load_hg; then
    log "[P3] load_hg — already done."
else
    log "[P3] loading HeritageGraph.ttl into <$GRAPH_HG>"
    if [[ -f "$ALIGN_DIR/HeritageGraph.ttl" ]]; then
        http_load "$ALIGN_DIR/HeritageGraph.ttl" "text/turtle" "$GRAPH_HG"
    else
        log "[P3] WARN: $ALIGN_DIR/HeritageGraph.ttl missing — skipping."
    fi
    log "[P3] loading heritagegraph-lux-alignment.ttl into <$GRAPH_ALIGN>"
    http_load "$ALIGN_DIR/heritagegraph-lux-alignment.ttl" "text/turtle" "$GRAPH_ALIGN"
    phase_done load_hg
fi

# ---------- P4  transform -----------------------------------------------------

if phase_check transform; then
    log "[P4] transform — already done."
else
    log "[P4] running batched INSERT WHERE (batch=$BATCH_SIZE, limit_per_query=$LIMIT_PER_QUERY)"
    LIMIT_FLAG=""
    [[ "$LIMIT_PER_QUERY" -gt 0 ]] && LIMIT_FLAG="--limit $LIMIT_PER_QUERY"

    # Use the script's builtin TRANSFORM_TEMPLATES (INSERT-WHERE with
    # {TARGET}/{LIMIT}/{OFFSET} placeholders). The .sparql file in queries/
    # is documentation — its CONSTRUCT bodies are not directly executable
    # by transform mode and its '# ===' separators lack the label form
    # the parser expects.
    /work/bin/migrate_lux_to_hg.py \
        --mode transform \
        --endpoint "$ENDPOINT" \
        --queries  builtin \
        --target-graph "$GRAPH_IMPORTED" \
        --batch-size "$BATCH_SIZE" \
        --log-file "$LOG_DIR/transform.state.json" \
        $LIMIT_FLAG
    phase_done transform
fi

# ---------- P5  validate ------------------------------------------------------

if phase_check validate; then
    log "[P5] validate — already done."
else
    log "[P5] running validation_queries.sparql (mode=$VALIDATION_MODE)"
    if /work/bin/migrate_lux_to_hg.py \
            --mode validate \
            --endpoint "$ENDPOINT" \
            --queries "$QUERIES_DIR/validation_queries.sparql"; then
        phase_done validate
    else
        rc=$?
        if [[ "$VALIDATION_MODE" == "lenient" ]]; then
            log "[P5] WARN: validation failed (rc=$rc) but VALIDATION_MODE=lenient — continuing."
            phase_done validate
        else
            log "[P5] FATAL: validation failed (rc=$rc). See $LOG_DIR/migrator.log."
            log "       Set VALIDATION_MODE=lenient to override (NOT recommended for prod)."
            exit "$rc"
        fi
    fi
fi

# ---------- P6  snapshot guidance --------------------------------------------

if ! phase_check snapshot; then
    log "[P6] snapshot guidance: snapshot Oxigraph from the host with:"
    log "       make backup   # or:"
    log "       docker run --rm -v hg-oxigraph_oxigraph_data:/data -v \$PWD:/backup busybox \\"
    log "           tar czf /backup/oxigraph-\$(date +%F).tar.gz -C /data ."
    phase_done snapshot
fi

# ---------- P7  master --------------------------------------------------------

phase_done master
log "================================================================="
log "Migration COMPLETE."
log "  imported graph: <$GRAPH_IMPORTED>"
log "  log:            $LOG_FILE"
log "  state:          $STATE_DIR"
log "================================================================="
exit 0
