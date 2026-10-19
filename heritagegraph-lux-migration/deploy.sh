#!/usr/bin/env bash
# =============================================================================
# deploy.sh — push the repo to server42 and bring the docker stack up.
# =============================================================================
# Run from the REPO ROOT.
#
# Usage:
#   ./deploy.sh                      # rsync + build + up (default)
#   ./deploy.sh --service migrator   # only rebuild/recreate one service
#   ./deploy.sh --no-build           # rsync + recreate, skip docker build
#   ./deploy.sh --dry-run            # show what would happen
#   ./deploy.sh --follow-logs        # tail migrator logs after deploy
#
# Reads optional overrides from ./.deploy.env (gitignored):
#   SERVER=root@server42.dnsbilisim.net
#   REMOTE_DIR=/root/github/heritagegraph-lux-migration
# =============================================================================
set -Eeuo pipefail

# -----------------------------------------------------------------------------
# Defaults — override via ./.deploy.env or environment.
# -----------------------------------------------------------------------------
SERVER="${SERVER:-root@server42.dnsbilisim.net}"
REMOTE_DIR="${REMOTE_DIR:-/root/github/heritagegraph-lux-migration}"

[[ -f .deploy.env ]] && . .deploy.env

# -----------------------------------------------------------------------------
# Args
# -----------------------------------------------------------------------------
SERVICE=""
BUILD=1
DRY_RUN=0
FOLLOW=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --service)      SERVICE="$2"; shift 2 ;;
        --no-build)     BUILD=0; shift ;;
        --dry-run)      DRY_RUN=1; shift ;;
        --follow-logs)  FOLLOW=1; shift ;;
        --server)       SERVER="$2"; shift 2 ;;
        --remote-dir)   REMOTE_DIR="$2"; shift 2 ;;
        -h|--help)      sed -n '2,18p' "$0"; exit 0 ;;
        *) echo "Unknown argument: $1" >&2; exit 2 ;;
    esac
done

say()  { printf '\033[1;36m[deploy]\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m   ✓\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m   !\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m   ✗\033[0m %s\n' "$*" >&2; exit 1; }
maybe(){ if [[ $DRY_RUN -eq 1 ]]; then printf '\033[1;90m   (dry-run)\033[0m %s\n' "$*"; else eval "$*"; fi }

# -----------------------------------------------------------------------------
# 0. Pre-flight checks
# -----------------------------------------------------------------------------
say "pre-flight (running from $(pwd))"

[[ -f docker/docker-compose.yml ]] || die "docker/docker-compose.yml not found — are you at the repo root?"
[[ -f docker/.env ]] || die "docker/.env missing — run: cp docker/.env.example docker/.env && \$EDITOR docker/.env"

if [[ ! -f alignment/HeritageGraph.ttl ]]; then
    warn "alignment/HeritageGraph.ttl not present — migrator will skip the HG ontology load."
    warn "Download with:"
    warn "  curl -L -o alignment/HeritageGraph.ttl https://raw.githubusercontent.com/CAIRNepal/heritagegraphontology/HeritageGraph/HeritageGraph.ttl"
fi
ok "local files look sane"

# SSH reachability
say "checking SSH to $SERVER"
ssh -o BatchMode=yes -o ConnectTimeout=10 "$SERVER" 'echo OK' >/dev/null \
    || die "cannot SSH to $SERVER (key auth required)"
ok "ssh OK"

# Remote dir
say "ensuring remote dir $REMOTE_DIR exists"
maybe "ssh '$SERVER' 'mkdir -p $REMOTE_DIR'"
ok "remote dir ready"

# Disk space sanity
if [[ $DRY_RUN -eq 0 ]]; then
    avail=$(ssh "$SERVER" "df -BG --output=avail '$REMOTE_DIR' | tail -1 | tr -d ' G'" 2>/dev/null || echo 0)
    if [[ "$avail" =~ ^[0-9]+$ ]] && (( avail < 20 )); then
        warn "only ${avail}G free at $REMOTE_DIR — pilot needs ≥20G, full needs ≥500G"
    else
        ok "remote disk: ${avail}G free"
    fi
fi

# -----------------------------------------------------------------------------
# 1. rsync the WHOLE REPO (excludes secrets + runtime data)
# -----------------------------------------------------------------------------
say "rsyncing repo to $SERVER:$REMOTE_DIR"

EXCLUDES=(
    --exclude='.env'
    --exclude='docker/.env'
    --exclude='.deploy.env'
    --exclude='backups/'
    --exclude='lux/'
    --exclude='logs/'
    --exclude='state/'
    --exclude='__pycache__/'
    --exclude='.git/'
    --exclude='.github/workflows/_cache/'
    --exclude='*.swp'
    --exclude='*.tmp'
    --exclude='.DS_Store'
)

RSYNC_OPTS=(-avz --delete --progress)
[[ $DRY_RUN -eq 1 ]] && RSYNC_OPTS+=(--dry-run)

rsync "${RSYNC_OPTS[@]}" "${EXCLUDES[@]}" ./ "$SERVER:$REMOTE_DIR/"
ok "rsync complete"

# Bootstrap .env on first deploy
maybe "ssh '$SERVER' 'cd $REMOTE_DIR/docker && test -f .env || (cp .env.example .env && echo \"  docker/.env created from example — REVIEW IT before next deploy\")'"

# -----------------------------------------------------------------------------
# 2. docker compose up
# -----------------------------------------------------------------------------
say "running docker compose on $SERVER"

build_flag=""
[[ $BUILD -eq 1 ]] && build_flag="--build"

if [[ -n "$SERVICE" ]]; then
    cmd="cd $REMOTE_DIR/docker && docker compose up -d $build_flag --no-deps $SERVICE"
else
    cmd="cd $REMOTE_DIR/docker && docker compose up -d $build_flag"
fi

maybe "ssh '$SERVER' '$cmd'"
ok "compose up issued"

# -----------------------------------------------------------------------------
# 3. Status
# -----------------------------------------------------------------------------
if [[ $DRY_RUN -eq 0 ]]; then
    say "status"
    ssh "$SERVER" "cd $REMOTE_DIR/docker && docker compose ps" || warn "docker compose ps failed"
fi

# -----------------------------------------------------------------------------
# 4. Follow logs
# -----------------------------------------------------------------------------
if [[ $FOLLOW -eq 1 && $DRY_RUN -eq 0 ]]; then
    say "following migrator logs (Ctrl-C to detach — container keeps running)"
    ssh -t "$SERVER" "cd $REMOTE_DIR/docker && docker compose logs -f --tail=200 migrator"
fi

ok "deploy complete"
