# LUX → HeritageGraph Migration Plan

**Author:** Semih Yumuşak
**Date:** May 2026
**Target deployment:** Oxigraph triplestore (per user choice)
**Scope:** Full LUX dataset (one-shot bulk migration)
**Companion artifacts:** `heritagegraph-lux-alignment.ttl`, `HeritageGraph_LUX_Mapping.xlsx`, `lux_to_hg_migration.sparql`, `migrate_lux_to_hg.py`, `validation_queries.sparql`.

## TL;DR

Seven phases — Discovery → Infrastructure → Extraction → Bulk-load → Transformation → Validation → Maintenance. The recommended path uses Oxigraph's native CLI for bulk loading and Python (`pyoxigraph` + `rdflib`) for orchestration and transformation. Full LUX is ~16 M records, ~300–600 M triples after JSON-LD expansion; expect 4-12 hours wall-clock on a 16-core / 64 GB machine. Phase 6 (validation) is the gate — only after the sanity-check returns zero unmapped LUX classes do we declare migration complete.

> **Strong recommendation: do a 10K-record pilot first**, validate end-to-end, *then* scale to full LUX. The plan below supports both modes. Pilot gates production; expect 1-2 days for pilot, 1 week for full.

---

## Phase 1 — Discovery & scope

### 1.1 Inventory LUX

| Aspect | Detail |
|---|---|
| Top-level entity types | HumanMadeObject, DigitalObject, Person, Group, Place, Event, Activity, Period, Type, Set, LinguisticObject, VisualItem, PropositionalObject — 13 endpoints |
| Approximate counts (May 2026) | ~5.5 M objects · ~1.2 M persons · ~700 K places · ~3 M concepts · ~150 K sets · ~5 M activities/events |
| Total records | ~16 M |
| Avg triples per record | ~25 (after JSON-LD expansion + provenance graphs) |
| Estimated total triples | 300–600 M |
| Compressed dump size | 15–35 GB (N-Quads gzipped) |
| Format | JSON-LD (record-level) + N-Quads bulk dump |
| Update cadence | Yale publishes diffs roughly weekly |

### 1.2 Decide source acquisition mode

| Mode | Fit for full LUX | Notes |
|---|---|---|
| **A. Bulk N-Quads dump** | ✅ Recommended | Fetch the official static dump (or git-LFS mirror). Single download, fastest to load. |
| B. REST crawl of `/data/{type}/{uuid}` | ⚠️ Slow at scale | ~16 M HTTP roundtrips even at 100 req/s ≈ 1.8 days. Use only if no dump is available. |
| C. SPARQL federation | ❌ Out for bulk | Acceptable for ad-hoc queries, not for migration. |

### 1.3 Subset gating

We migrate full LUX as the eventual target, but **stage in three rings**:

1. **Pilot (10 K records, ~30 min):** filter LUX to `classified_as` Hindu/Buddhist religious objects via the search API. Validate transform end-to-end and the sanity-check query.
2. **Domain ring (~50–100 K records, ~3 hours):** South Asian + East Asian religious heritage (Nepal, India, Tibet, Bhutan, China, Japan).
3. **Full ring (16 M records, ~12 hours):** the rest of LUX.

Each ring writes to the same target named graph; the pilot's HG instances are not deleted before scaling up — additivity is the rollback strategy.

---

## Phase 2 — Infrastructure

### 2.1 Hardware / sizing

| Component | Sizing target |
|---|---|
| CPU | 8–16 cores (Oxigraph parallelizes inference & query) |
| RAM | 64 GB minimum; 128 GB ideal for full ring |
| Disk | 500 GB NVMe (the .db file plus working space) |
| OS | Linux, glibc ≥ 2.31 (Oxigraph supports x86_64 and arm64) |

### 2.2 Oxigraph layout

Oxigraph is the chosen target. Single binary, RocksDB-backed, supports SPARQL 1.1 Update + Query. Spin up once, point at one persistent directory.

```bash
# Server mode (recommended for the migration window):
oxigraph serve --location /var/lib/oxigraph --bind 127.0.0.1:7878

# Embedded mode (faster bulk operations from Python):
python -c "import pyoxigraph as ox; store = ox.Store('/var/lib/oxigraph')"
```

### 2.3 Named-graph plan

Keep LUX raw, alignment, HG-native, and HG-imported in separate graphs so we can `DROP GRAPH` cleanly on rollback.

| Graph URI | Contents |
|---|---|
| `<https://lux.collections.yale.edu/>` | Raw LUX dump (read-only after load) |
| `<https://w3id.org/heritagegraph/alignment/lux>` | The 273-triple alignment ontology |
| `<https://w3id.org/heritagegraph/>` | HeritageGraph.ttl + native (Niraj/Nabin's) data |
| `<https://w3id.org/heritagegraph/imported/lux>` | LUX records transformed into HG instances (this graph is the migration output) |

---

## Phase 3 — Extraction

### 3.1 Bulk dump path (recommended)

```bash
# Yale publishes a static dump for downstream consumers (URL fixed each release):
DUMP_URL="https://linked-art.lux.collections.yale.edu/data/dump/latest.nq.gz"

mkdir -p /data/lux && cd /data/lux
curl -L -o lux.nq.gz "$DUMP_URL"
gunzip -k lux.nq.gz                       # keep both compressed and unpacked
sha256sum lux.nq lux.nq.gz > checksums.txt
```

If Yale's dump endpoint is offline, use the git-LFS mirror at `https://github.com/project-lux/lux-data-static` (per-record JSON-LD; `git lfs pull --include="*Record*"`).

### 3.2 REST crawl fallback

`migrate_lux_to_hg.py` (companion script) supports `--mode crawl` with concurrency, retry/backoff, and resume. Use only when the dump is unavailable. Typical command:

```bash
python migrate_lux_to_hg.py \
  --mode crawl \
  --filter "religious heritage" \
  --concurrency 32 \
  --resume-state /data/lux/crawl_state.json \
  --out /data/lux/lux_crawled.nq
```

### 3.3 Verify extraction

```bash
# Should be ~16 M lines for a full dump (one quad per line):
wc -l /data/lux/lux.nq

# Spot-check 5 random quads parse cleanly:
shuf -n 5 /data/lux/lux.nq | rapper -i nquads -c -
```

---

## Phase 4 — Bulk load + alignment

### 4.1 Load LUX raw dump into Oxigraph

```bash
oxigraph load \
  --location /var/lib/oxigraph \
  --file    /data/lux/lux.nq \
  --format  application/n-quads
# 4–10 hours for full LUX on a 16-core box. Oxigraph reports progress.
```

### 4.2 Load HG ontology + alignment

```bash
oxigraph load --location /var/lib/oxigraph \
  --file HeritageGraph.ttl              --graph "https://w3id.org/heritagegraph/"
oxigraph load --location /var/lib/oxigraph \
  --file heritagegraph-lux-alignment.ttl --graph "https://w3id.org/heritagegraph/alignment/lux"
```

### 4.3 Materialize subClassOf inferences (optional but recommended)

Oxigraph does NOT do automatic OWL inference. We materialize the alignment closure once so transformation queries are simpler:

```sparql
INSERT { GRAPH <https://w3id.org/heritagegraph/alignment/lux> {
  ?inst a ?super .
} }
WHERE { GRAPH ?g {
  ?inst a ?sub .
  ?sub  rdfs:subClassOf+ ?super .
  FILTER (STRSTARTS(STR(?sub), "https://w3id.org/heritagegraph/"))
} }
```

(This is the only inferred-data step. Strictly speaking, Oxigraph + the alignment let our transform queries match `crm:E22_Human-Made_Object` directly without any inference, so this step is *optional*.)

---

## Phase 5 — Transformation

### 5.1 The 9 CONSTRUCT queries

These are in `lux_to_hg_migration.sparql`. The migration converts each `INSERT { … } WHERE { … }` into an `INSERT { GRAPH <hg_imported> { … } } WHERE { … }` and runs them against the Oxigraph endpoint:

```bash
python migrate_lux_to_hg.py \
  --mode transform \
  --endpoint http://127.0.0.1:7878 \
  --queries lux_to_hg_migration.sparql \
  --target-graph "https://w3id.org/heritagegraph/imported/lux" \
  --batch-size 50000 \
  --log-file migration.log
```

What each query writes:

| # | Query | Writes (HG class) | Approx records |
|---|---|---|---|
| 1 | Object branch | `hg:HumanMadeObject` | ~5.5 M |
| 2 | Person branch | `hg:Person` + `hg:Birth`/`hg:Death` | ~1.2 M |
| 3 | Group branch | `hg:Group` + `hg:Formation`/`hg:Dissolution` | ~150 K |
| 4 | Place branch | `hg:Place` | ~700 K |
| 5 | Concept branch | `hg:Type`/`hg:Material`/`hg:Language`/… | ~3 M |
| 6 | Activity branch | 14 HG event subclasses | ~5 M |
| 7 | Work branch | `hg:LinguisticObject`/`hg:VisualItem`/`hg:PropositionalObject`/`hg:DigitalObject` | ~600 K |
| 8 | Set / CuratedHolding | `hg:Set` / `hg:CuratedHolding` | ~150 K |
| 9 | Identifier / Name | embedded; ~1 per record × 16 M | ~25 M |

### 5.2 Batching strategy

Pure `INSERT { } WHERE { }` over 16 M records will OOM Oxigraph (or any triplestore). The script slices each query by chunk:

```sparql
INSERT { GRAPH <…/imported/lux> { ?hgObj a heritageGraph:HumanMadeObject . … } }
WHERE  {
  ?obj a crm:E22_Human-Made_Object .
  …
}
ORDER BY ?obj
LIMIT  50000
OFFSET ?BATCH_OFFSET
```

`migrate_lux_to_hg.py` increments OFFSET in 50 K-record steps, commits between batches, and logs `(query, batch, triples_inserted, elapsed)` to `migration.log`. Resume reads the log.

### 5.3 URI rewriting

LUX URIs look like `https://lux.collections.yale.edu/data/object/abcd-efgh-…`. The transformation rewrites them to HG-namespaced URIs (preserving the UUID for round-trip auditability):

```
https://lux.collections.yale.edu/data/object/UUID
              ↓
https://w3id.org/heritagegraph/imported/lux/object/UUID
```

The original LUX URI is preserved as `owl:sameAs`, so federated discovery still works:

```turtle
hgi:object/UUID  a heritageGraph:HumanMadeObject ;
                 owl:sameAs <https://lux.collections.yale.edu/data/object/UUID> ;
                 …
```

---

## Phase 6 — Validation (the gate)

`validation_queries.sparql` (companion file) bundles the seven checks below. **Migration is not "done" until V1, V2, V3, V5 all pass.**

| # | Check | Pass criterion |
|---|---|---|
| **V1** Sanity coverage | `?lux a ?cls` where `?cls` has no HG target | **0 rows** |
| **V2** URI rewrite consistency | every imported HG instance has exactly one `owl:sameAs` to a LUX URI | **0 violations** |
| V3 Count parity | per-class counts in LUX vs HG-imported | within ±5 % per class |
| V4 Property coverage | LUX properties referenced but unaligned | manual review |
| V5 Spot-check round-trip | random 100 records: full LUX record vs reconstructed HG record | manual diff, no semantic loss |
| V6 HG-only preserved | HG-only classes (LivingGoddessTenure, SyncreticRelationship, Guthi, …) untouched | counts before == after |
| V7 SHACL constraints | run any SHACL shapes Niraj/Nabin defined | 0 violations |

### 6.1 Sanity check (V1) — the critical query

```sparql
SELECT DISTINCT ?luxClass (COUNT(?x) AS ?instances)
WHERE {
  GRAPH <https://lux.collections.yale.edu/> { ?x a ?luxClass . }
  FILTER(STRSTARTS(STR(?luxClass),"http://www.cidoc-crm.org/cidoc-crm/")
      || STRSTARTS(STR(?luxClass),"http://www.ics.forth.gr/isl/CRMdig/")
      || STRSTARTS(STR(?luxClass),"http://www.ics.forth.gr/isl/CRMsci/")
      || STRSTARTS(STR(?luxClass),"https://linked.art/ns/terms/"))
  FILTER NOT EXISTS {
    GRAPH <https://w3id.org/heritagegraph/alignment/lux> {
      ?hg rdfs:subClassOf+ ?luxClass .   FILTER (STRSTARTS(STR(?hg), "https://w3id.org/heritagegraph/"))
    }
    UNION
    GRAPH <https://w3id.org/heritagegraph/alignment/lux> {
      ?hg owl:equivalentClass ?luxClass . FILTER (STRSTARTS(STR(?hg), "https://w3id.org/heritagegraph/"))
    }
  }
}
GROUP BY ?luxClass
ORDER BY DESC(?instances)
```

Zero rows = every LUX class is covered. Any rows = add HG class for that LUX type and re-run transform query #6 (Activity) or #7 (Work) accordingly.

---

## Phase 7 — Maintenance

After the bulk migration completes:

1. **Snapshot.** `oxigraph backup --location /var/lib/oxigraph --to /backup/oxigraph-post-migration-2026-05-DD.tar.zst`. This is your rollback point.
2. **Schedule weekly delta sync.** Yale publishes diffs at `…/data/diffs/<date>/`. Cron job:
   ```bash
   0 4 * * MON  /opt/hg/bin/sync_lux_delta.sh   # sketched in migrate_lux_to_hg.py --mode delta
   ```
3. **Re-run V1 sanity-check after every delta.** New LUX class types may appear and need new HG mappings.
4. **Track LUX schema version.** Keep `LUX_SCHEMA_VERSION = "2026-05"` in alignment ontology metadata; bump on Linked Art profile updates.

---

## Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LUX dump unavailable / behind auth | medium | high | REST crawl fallback (Phase 3.2) |
| Oxigraph OOMs on 600 M triples | low-medium | high | Batching (5.2); tune Oxigraph mmap; or shard by named graph |
| New LUX class type added (post-2026-05) | medium | medium | V1 sanity check catches it; alignment update is one-line |
| URI rewrite drops LUX provenance | low | high | `owl:sameAs` preservation (5.3); checked by V2 |
| Heritage-graph existing data accidentally overwritten | low | catastrophic | Imported graph isolated; HG-native graph never touched (V6) |
| Confidence score (HG-only) gets stripped | low | low | HG-only properties not referenced by any CONSTRUCT — preserved by construction |
| Yale's data licensing | medium | high | Verify CC BY 4.0 / public-domain status of LUX before bulk hosting; some Yale records are restricted |

---

## Timeline (full ring)

| Day | Task | Outcome |
|---|---|---|
| 1 | Provision Oxigraph, download dump | Server up, dump on disk |
| 1 | Pilot (10 K religious-object subset) | All 7 validations pass on subset |
| 2 | Bulk load LUX | `<lux>` named graph populated |
| 2 | Load alignment + HG ontology | Alignment in place |
| 3 | Transform (Phase 5) | `<imported/lux>` populated |
| 4 | Validation (Phase 6) | V1 → 0 rows; V3 → ±5 %; V5 spot-check signed off |
| 4 | Snapshot + handover | Backup taken; runbook to Niraj/Nabin |

Two-engineer-week realistic estimate including pilot iteration.

---

## Rollback plan

Migration writes to one isolated named graph. Rollback is one SPARQL Update:

```sparql
DROP GRAPH <https://w3id.org/heritagegraph/imported/lux> ;
```

The raw LUX graph and HG-native graph are untouched, so nothing else is affected. The snapshot from Phase 7 is the disaster-recovery fallback.

---

## Operational runbook (TL;DR for Niraj/Nabin)

```bash
# 1. provision
oxigraph serve --location /var/lib/oxigraph --bind 127.0.0.1:7878 &

# 2. extract
curl -L -o /data/lux/lux.nq.gz https://linked-art.lux.collections.yale.edu/data/dump/latest.nq.gz
gunzip -k /data/lux/lux.nq.gz

# 3. bulk-load LUX raw
oxigraph load --location /var/lib/oxigraph --file /data/lux/lux.nq --format application/n-quads

# 4. load HG ontology + alignment
oxigraph load --location /var/lib/oxigraph --file HeritageGraph.ttl              --graph "https://w3id.org/heritagegraph/"
oxigraph load --location /var/lib/oxigraph --file heritagegraph-lux-alignment.ttl --graph "https://w3id.org/heritagegraph/alignment/lux"

# 5. pilot transform (religious subset, dry-run first)
python migrate_lux_to_hg.py --mode transform --endpoint http://127.0.0.1:7878 \
       --filter "religious" --limit 10000 --dry-run

# 6. full transform
python migrate_lux_to_hg.py --mode transform --endpoint http://127.0.0.1:7878 \
       --queries lux_to_hg_migration.sparql --target-graph https://w3id.org/heritagegraph/imported/lux

# 7. validate
python migrate_lux_to_hg.py --mode validate --endpoint http://127.0.0.1:7878 \
       --queries validation_queries.sparql

# 8. snapshot
oxigraph backup --location /var/lib/oxigraph --to /backup/oxigraph-post-migration-$(date -I).tar.zst
```
