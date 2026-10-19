#!/usr/bin/env bash
# =============================================================================
# Delta-syncer entrypoint — runs `migrate_lux_to_hg.py --mode delta` on a
# weekly schedule. Pure-bash polling loop; no supercronic dependency.
#
# Why pure bash? supercronic v0.2.34 in our base image crashloops with
# "Failed to fork exec: no such file or directory" on startup (likely a
# parser quirk with day-name cron syntax under env-file expansion). The
# delta job runs at most weekly, so a 30-second polling loop is more than
# precise enough and eliminates the dependency.
#
# Schedule controls (all UTC, all optional):
#   DELTA_DAY      day of week (1=Mon … 7=Sun, default 1)
#   DELTA_HOUR     hour 00-23 (default 04)
#   DELTA_MIN      minute 00-59 (default 00)
#   DELTA_CRON     legacy "M H * * DOW" string; parsed if set (overrides above)
#   DELTA_RUN_ON_START  if "1", run one delta cycle immediately on startup
# =============================================================================
set -Eeuo pipefail

mkdir -p /work/logs /work/state
LOG_FILE=/work/logs/delta-syncer.log

# ---- Schedule resolution ----------------------------------------------------

DELTA_DAY="${DELTA_DAY:-1}"
DELTA_HOUR="${DELTA_HOUR:-04}"
DELTA_MIN="${DELTA_MIN:-00}"

if [[ -n "${DELTA_CRON:-}" ]]; then
    # Parse "M H * * DOW" — only fields 1, 2, and 5 are used.
    read -ra C <<< "$DELTA_CRON"
    if [[ ${#C[@]} -ge 5 ]]; then
        if [[ "${C[0]}" =~ ^[0-9]{1,2}$ ]]; then DELTA_MIN="${C[0]}"; fi
        if [[ "${C[1]}" =~ ^[0-9]{1,2}$ ]]; then DELTA_HOUR="${C[1]}"; fi
        case "${C[4]^^}" in
            MON|1) DELTA_DAY=1 ;;
            TUE|2) DELTA_DAY=2 ;;
            WED|3) DELTA_DAY=3 ;;
            THU|4) DELTA_DAY=4 ;;
            FRI|5) DELTA_DAY=5 ;;
            SAT|6) DELTA_DAY=6 ;;
            SUN|0|7) DELTA_DAY=7 ;;
            *) ;;
        esac
    fi
fi

# Normalise to two-digit form for direct comparison with `date +%H/%M`.
printf -v DELTA_HOUR '%02d' "$((10#$DELTA_HOUR))"
printf -v DELTA_MIN  '%02d' "$((10#$DELTA_MIN))"

ENDPOINT="${OXIGRAPH_ENDPOINT:-http://oxigraph:7878}"
DELTA_URL="${DELTA_URL:-https://linked-art.lux.collections.yale.edu/data/diffs/latest.nq.gz}"
QUERIES_DIR="${QUERIES_DIR:-/work/queries}"
GRAPH_IMPORTED="https://w3id.org/heritagegraph/imported/lux"

# Graceful shutdown — log and exit cleanly on TERM/INT.
shutdown() {
    echo "[$(date -u +%FT%TZ)] delta-syncer received signal, exiting" \
        | tee -a "$LOG_FILE"
    exit 0
}
trap shutdown TERM INT

# ---- Startup banner ---------------------------------------------------------

dow_name() {
    case "$1" in
        1) echo "Mon" ;; 2) echo "Tue" ;; 3) echo "Wed" ;;
        4) echo "Thu" ;; 5) echo "Fri" ;; 6) echo "Sat" ;; 7) echo "Sun" ;;
        *) echo "?" ;;
    esac
}

cat <<EOF | tee -a "$LOG_FILE"
[$(date -u +%FT%TZ)] delta-syncer starting (pure-bash scheduler)
  schedule:  $(dow_name "$DELTA_DAY") $DELTA_HOUR:$DELTA_MIN UTC, weekly
  endpoint:  $ENDPOINT
  delta url: $DELTA_URL
  graph:     $GRAPH_IMPORTED
EOF

# ---- Job body ---------------------------------------------------------------

run_delta() {
    local stamp; stamp="$(date -u +%FT%H%MZ)"
    local log="/work/logs/delta-${stamp}.log"
    {
        echo "[$(date -u +%FT%TZ)] running delta sync"
        /work/bin/migrate_lux_to_hg.py \
            --mode delta \
            --endpoint "$ENDPOINT" \
            --diff-url "$DELTA_URL" \
            --queries  "$QUERIES_DIR/lux_to_hg_migration.sparql" \
            --target-graph "$GRAPH_IMPORTED"
        echo "[$(date -u +%FT%TZ)] running V1+V2 hard-gate validation after delta"
        /work/bin/migrate_lux_to_hg.py \
            --mode validate \
            --endpoint "$ENDPOINT" \
            --queries  "$QUERIES_DIR/validation_queries.sparql"
        echo "[$(date -u +%FT%TZ)] delta cycle complete"
    } 2>&1 | tee -a "$log"
}

# ---- Optional one-shot on startup ------------------------------------------

if [[ "${DELTA_RUN_ON_START:-0}" == "1" ]]; then
    echo "[$(date -u +%FT%TZ)] DELTA_RUN_ON_START=1 — running once now" \
        | tee -a "$LOG_FILE"
    run_delta || echo "[$(date -u +%FT%TZ)] one-shot delta failed; continuing to schedule" \
        | tee -a "$LOG_FILE"
fi

# ---- Main polling loop ------------------------------------------------------
# Poll every 30 seconds; at most one missed minute under abnormal scheduler
# delay. After a successful run, sleep ~90s so we don't double-fire in the
# same trigger minute.

LAST_FIRE_KEY=""

while true; do
    now_dow="$(date -u +%u)"     # 1..7
    now_hour="$(date -u +%H)"    # 00..23
    now_min="$(date -u +%M)"     # 00..59
    fire_key="${now_dow}-${now_hour}-${now_min}"

    if [[ "$now_dow" == "$DELTA_DAY" \
       && "$now_hour" == "$DELTA_HOUR" \
       && "$now_min" == "$DELTA_MIN" \
       && "$fire_key" != "$LAST_FIRE_KEY" ]]; then
        LAST_FIRE_KEY="$fire_key"
        run_delta || echo "[$(date -u +%FT%TZ)] delta cycle failed; will retry next week" \
            | tee -a "$LOG_FILE"
        sleep 90
    else
        sleep 30
    fi
done
