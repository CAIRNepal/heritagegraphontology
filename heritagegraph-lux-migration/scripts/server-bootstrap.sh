#!/usr/bin/env bash
# =============================================================================
# server-bootstrap.sh — first-time setup on server42.dnsbilisim.net
# =============================================================================
# Run once as root, on the server:
#   bash /root/server-bootstrap.sh
#
# Idempotent: safe to rerun if you change something or want to repair state.
# =============================================================================
set -Eeuo pipefail

PROJECT_DIR="${PROJECT_DIR:-/root/github/heritagegraph-lux-migration}"
SERVICE_NAME="heritagegraph-lux"
DISCOVER_LOG="/root/lux_endpoint_probe.log"

say()  { printf '\033[1;36m[bootstrap]\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m   ✓\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m   !\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m   ✗\033[0m %s\n' "$*" >&2; exit 1; }

# -----------------------------------------------------------------------------
# 0. Sanity
# -----------------------------------------------------------------------------
[[ "$EUID" -eq 0 ]] || die "must run as root (try: sudo bash $0)"

say "host info"
echo "   hostname:   $(hostname)"
echo "   kernel:     $(uname -r)"
echo "   total RAM:  $(free -h | awk '/^Mem:/{print $2}')"
echo "   free disk:  $(df -h / | awk 'NR==2{print $4 " on /"}')"

# -----------------------------------------------------------------------------
# 1. Docker + Compose plugin
# -----------------------------------------------------------------------------
say "checking Docker"
if ! command -v docker >/dev/null 2>&1; then
    say "Docker not found — installing"
    curl -fsSL https://get.docker.com | sh
    systemctl enable --now docker
    ok "Docker installed"
else
    ok "Docker present: $(docker --version)"
fi

if ! docker compose version >/dev/null 2>&1; then
    say "Compose v2 plugin missing — installing"
    apt-get update -y && apt-get install -y --no-install-recommends docker-compose-plugin
    ok "Compose v2 installed: $(docker compose version)"
else
    ok "Compose present: $(docker compose version)"
fi

# -----------------------------------------------------------------------------
# 2. Project directory
# -----------------------------------------------------------------------------
say "ensuring project directory exists: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR" "$PROJECT_DIR/backups" "$PROJECT_DIR/lux" \
         "$PROJECT_DIR/logs" "$PROJECT_DIR/state" "$PROJECT_DIR/alignment"
ok "directory tree ready"

# -----------------------------------------------------------------------------
# 3. Resource sanity check
# -----------------------------------------------------------------------------
say "resource sanity"
mem_gb=$(awk '/^MemTotal:/ {printf "%d", $2/1024/1024}' /proc/meminfo)
disk_gb=$(df -BG --output=avail "$PROJECT_DIR" | awk 'NR==2{gsub("G",""); print $1}')

if (( mem_gb < 16 )); then
    warn "only ${mem_gb} GB RAM — pilot OK, full ring needs ≥64 GB"
else
    ok "RAM: ${mem_gb} GB"
fi
if (( disk_gb < 100 )); then
    warn "only ${disk_gb} GB free at $PROJECT_DIR — pilot OK, full ring needs ≥500 GB"
else
    ok "disk: ${disk_gb} GB free at $PROJECT_DIR"
fi

# Port conflict check (OXIGRAPH default 7878)
if ss -tln 2>/dev/null | grep -qE ':7878\b'; then
    warn "port 7878 already in use on this host — set OXIGRAPH_PORT in .env after rsync"
else
    ok "port 7878 free"
fi

# -----------------------------------------------------------------------------
# 4. .env scaffold (won't overwrite an existing one)
# -----------------------------------------------------------------------------
if [[ -f "$PROJECT_DIR/.env" ]]; then
    ok ".env exists — not touching"
elif [[ -f "$PROJECT_DIR/.env.example" ]]; then
    cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
    ok ".env created from .env.example — REVIEW before first run"
else
    warn ".env.example missing — rsync the project files first"
fi

# -----------------------------------------------------------------------------
# 5. HeritageGraph.ttl fetch (best-effort)
# -----------------------------------------------------------------------------
HG_TTL="$PROJECT_DIR/alignment/HeritageGraph.ttl"
if [[ -f "$HG_TTL" ]]; then
    ok "HeritageGraph.ttl already present"
else
    say "fetching HeritageGraph.ttl from CAIR Nepal GitHub"
    # NB July 2026 (alpha5 sync, see docs/SERVER_AND_MIGRATION_STATE.md §6):
    # 'main' has been stale since Feb 2026 — active development is on the
    # 'HeritageGraph' branch, and as of the alpha5 regeneration (2026-07-22)
    # the ontology lives at ontology/HeritageGraph.ttl on THAT branch (moved
    # out of the repo root). Try that first; fall back to the old root path
    # on 'HeritageGraph' (pre-alpha5 layout), then to 'main' (known stale,
    # last resort so bootstrap doesn't hard-fail).
    if curl -fL --retry 3 \
        -o "$HG_TTL" \
        "https://raw.githubusercontent.com/CAIRNepal/heritagegraphontology/HeritageGraph/ontology/HeritageGraph.ttl" \
       || curl -fL --retry 3 \
        -o "$HG_TTL" \
        "https://raw.githubusercontent.com/CAIRNepal/heritagegraphontology/HeritageGraph/HeritageGraph.ttl" \
       || curl -fL --retry 3 \
        -o "$HG_TTL" \
        "https://raw.githubusercontent.com/CAIRNepal/heritagegraphontology/main/HeritageGraph.ttl"; then
        ok "HeritageGraph.ttl downloaded ($(wc -l < "$HG_TTL") lines)"
    else
        warn "couldn't fetch HeritageGraph.ttl — migrator will skip the HG ontology load until you put it in alignment/"
    fi
fi

# -----------------------------------------------------------------------------
# 6. systemd unit
# -----------------------------------------------------------------------------
say "installing systemd unit $SERVICE_NAME"

cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=HeritageGraph LUX migration stack (oxigraph + migrator + delta-syncer)
Requires=docker.service
After=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$PROJECT_DIR
ExecStartPre=/usr/bin/test -f $PROJECT_DIR/.env
ExecStart=/usr/bin/docker compose --project-directory $PROJECT_DIR up -d
ExecStop=/usr/bin/docker compose --project-directory $PROJECT_DIR down
TimeoutStartSec=600

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "$SERVICE_NAME.service" >/dev/null
ok "systemd unit installed and enabled (will run on next boot)"

# -----------------------------------------------------------------------------
# 7. logrotate
# -----------------------------------------------------------------------------
say "installing logrotate config"
cat > "/etc/logrotate.d/${SERVICE_NAME}" <<EOF
$PROJECT_DIR/logs/*.log {
    weekly
    rotate 14
    missingok
    notifempty
    compress
    delaycompress
    copytruncate
    su root root
}
EOF
ok "logrotate config installed (weekly, 14 weeks retention)"

# -----------------------------------------------------------------------------
# 8. LUX endpoint probe
# -----------------------------------------------------------------------------
if [[ -f "$PROJECT_DIR/discover_lux_endpoints.sh" ]]; then
    say "probing LUX endpoints (writing to $DISCOVER_LOG)"
    bash "$PROJECT_DIR/discover_lux_endpoints.sh" 2>&1 | tee "$DISCOVER_LOG" || warn "probe partial"
else
    warn "$PROJECT_DIR/discover_lux_endpoints.sh missing — rsync from local first"
fi

# -----------------------------------------------------------------------------
# 9. Next steps
# -----------------------------------------------------------------------------
cat <<EOF

==============================================================
 bootstrap complete.

 Next steps:

   1. From your LOCAL machine, run:
        cd <package>/docker
        ./deploy.sh

   2. Then on this server, tail the migrator:
        cd $PROJECT_DIR && docker compose logs -f migrator

   3. Once pilot finishes (~30-45 min), validate:
        cd $PROJECT_DIR && make validate

   4. To start on boot:
        systemctl status $SERVICE_NAME    # already enabled by this script

 LUX endpoint probe log: $DISCOVER_LOG
==============================================================
EOF
