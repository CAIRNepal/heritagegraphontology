# Migrator image — orchestrates the LUX → HeritageGraph pipeline.
#
# IMPORTANT: this Dockerfile expects the build context to be the REPO ROOT
# (one level up from docker/). docker-compose.yml configures this with
# `context: ..`. The Dockerfile then COPYs from canonical locations:
#   * scripts/migrate_lux_to_hg.py
#   * docker/migrator/entrypoint.sh
#   * docker/migrator/delta_loop.sh
#
# Bundles:
#   * Python 3.12 + rdflib + pyoxigraph + requests + tqdm
#   * The migrate_lux_to_hg.py script (canonical copy from scripts/)
#   * Phase-runner scripts (entrypoint.sh, delta_loop.sh)
#   * supercronic (for cron-style delta sync without privileged systemd)

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Runtime deps:
#   curl       — fetch LUX dumps
#   ca-certificates — TLS for Yale endpoints
#   pigz       — fast parallel gunzip for big LUX dumps
#   tini       — proper PID 1 / signal handling
#   raptor2-utils — `rapper` for round-trip Turtle/N-Quads validation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl ca-certificates pigz tini raptor2-utils && \
    rm -rf /var/lib/apt/lists/*

# Install supercronic — cron without root, friendly with containers.
ARG SUPERCRONIC_VERSION=v0.2.34
ARG SUPERCRONIC_SHA1=e8631edc1775000d119b70fd40339a7238eece14
RUN ARCH=$(dpkg --print-architecture); \
    case "$ARCH" in \
        amd64) F="supercronic-linux-amd64" ;; \
        arm64) F="supercronic-linux-arm64" ;; \
        *) echo "unsupported arch $ARCH" >&2; exit 1 ;; \
    esac && \
    curl -fsSLo /usr/local/bin/supercronic \
         "https://github.com/aptible/supercronic/releases/download/${SUPERCRONIC_VERSION}/${F}" && \
    chmod +x /usr/local/bin/supercronic

# Python deps.
RUN pip install --no-cache-dir \
      "rdflib>=7.0,<8" \
      "pyoxigraph>=0.4,<0.5" \
      "requests>=2.31,<3" \
      "tqdm>=4.66,<5"

WORKDIR /work

# Copy from the REPO ROOT (build context is `..`):
COPY scripts/migrate_lux_to_hg.py        /work/bin/migrate_lux_to_hg.py
COPY docker/migrator/entrypoint.sh       /work/bin/entrypoint.sh
COPY docker/migrator/delta_loop.sh       /work/bin/delta_loop.sh
RUN chmod +x /work/bin/*.sh /work/bin/migrate_lux_to_hg.py

# Default mount points (declared so docker volumes attach cleanly).
VOLUME ["/work/lux", "/work/logs", "/work/state"]

# tini handles SIGTERM correctly (long-running migration must drain).
ENTRYPOINT ["/usr/bin/tini", "--", "/work/bin/entrypoint.sh"]
