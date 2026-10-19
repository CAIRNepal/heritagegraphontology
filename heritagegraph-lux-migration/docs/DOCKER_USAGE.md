# Docker Compose stack — LUX → HeritageGraph migration

Self-contained, server-friendly deployment of the full migration described in `../MIGRATION_PLAN.md`. One command provisions Oxigraph, runs the migration end-to-end, and starts a weekly delta-syncer.

## Layout

```
docker/
├── docker-compose.yml         # 3 services + 4 named volumes
├── .env.example               # → copy to .env and tune
├── Makefile                   # up / down / migrate / validate / backup / restore / sparql / …
├── alignment/                 # .ttl files mounted read-only into the migrator
│   ├── heritagegraph-lux-alignment.ttl  (already here)
│   └── HeritageGraph.ttl                ← drop this in before running
├── queries/
│   ├── lux_to_hg_migration.sparql       (already here)
│   └── validation_queries.sparql        (already here)
└── migrator/
    ├── Dockerfile             # python:3.12-slim + supercronic + raptor2 + script
    ├── entrypoint.sh          # 7-phase orchestrator (idempotent, state-flagged)
    ├── delta_loop.sh          # supercronic-driven weekly delta sync
    └── migrate_lux_to_hg.py   # the orchestrator (copied from parent)
```

## Quickstart (pilot, ~30 min)

```bash
cp .env.example .env
# put HeritageGraph.ttl into alignment/  (download from CAIRNepal/heritagegraphontology)
curl -L -o alignment/HeritageGraph.ttl \
  https://raw.githubusercontent.com/CAIRNepal/heritagegraphontology/HeritageGraph/ontology/HeritageGraph.ttl

docker compose up -d
docker compose logs -f migrator
```

When `migrator` exits 0, validate with:

```bash
make status      # triple counts per named graph
make validate    # re-run V1/V2 hard-gate validation
```

## Going to production (full ring)

Edit `.env`:

```diff
-RING_MODE=pilot
-LIMIT_PER_QUERY=10000
+RING_MODE=full
+LIMIT_PER_QUERY=0
+OXIGRAPH_MEM_LIMIT=128g          # match host
```

Wipe pilot state and re-launch:

```bash
make reset                 # clears /work/state but keeps loaded data
docker compose up -d migrator
docker compose logs -f migrator
```

## Services

| Service | Role | Lifecycle |
|---|---|---|
| `oxigraph` | The SPARQL 1.1 triplestore. Persistent on `oxigraph_data` volume. | Always up |
| `migrator` | One-shot orchestrator. Runs phases P1–P7 and exits 0. Idempotent — re-running on a clean stack is a no-op once `master.done` exists. | One-shot |
| `delta-syncer` | Wakes on `DELTA_CRON` (default Monday 04:00 UTC), pulls the LUX diff, runs `--mode delta`, then re-runs V1/V2 validation. | Always up; `depends_on: migrator service_completed_successfully` |

## Phase-by-phase what `migrator` does

```
P1  fetch_dump   → curl LUX dump (or REST crawl in RING_MODE=crawl)
P2  load_lux     → push N-Quads into <https://lux.collections.yale.edu/>
P3  load_hg      → push HeritageGraph.ttl + alignment.ttl
P4  transform    → batched INSERT WHERE → <…/imported/lux>
P5  validate     → V1/V2 hard gates; failures abort unless VALIDATION_MODE=lenient
P6  snapshot     → prints `make backup` reminder
P7  master       → touches /work/state/master.done; future runs are no-ops
```

Each phase is gated by a flag file in the `migration_state` volume. To force a re-run from any phase: `make reset` and `docker compose up -d migrator`.

## Common operations

```bash
make help              # cheatsheet
make status            # triple counts per named graph
make logs              # tail all service logs
make migrate           # re-run the migrator (no-op if already done)
make validate          # run validation queries against the live store
make delta-now         # trigger an immediate delta sync
make backup            # snapshot oxigraph_data → ./backups/
make restore FILE=backups/oxigraph-2026-05-02.tar.gz
make reset             # clear migration state; data preserved
make reset-everything  # DANGER: drops all volumes
make shell             # bash shell inside the migrator image
make sparql Q='SELECT * WHERE {?s ?p ?o} LIMIT 5'
make ttl-check         # validate every .ttl in alignment/
```

## Resource sizing

| Profile | RAM (oxigraph) | Disk | Wall-clock |
|---|---|---|---|
| pilot   | 8 GB     | 5 GB    | ~30 min |
| domain  | 32 GB    | 50 GB   | ~3 hours |
| full    | 64–128 GB | 500 GB | 8–12 hours |

`OXIGRAPH_MEM_LIMIT` and `MIGRATOR_MEM_LIMIT` in `.env` cap container memory.

## Networking

By default, Oxigraph is exposed on the host at port `${OXIGRAPH_PORT:-7878}`. To put it behind nginx/Caddy with TLS, drop the port mapping and add a reverse-proxy service to the same Compose network. The internal hostname for SPARQL clients is `oxigraph:7878`.

## Failure & recovery

* Migration failed mid-transform? Just `docker compose up -d migrator` again — the SPARQL INSERT WHERE batches are idempotent (RDF set semantics) and the state file resumes from the last completed batch.
* Validation V1 reports unmapped LUX classes? Update `alignment/heritagegraph-lux-alignment.ttl`, `make reset`, re-run.
* Bad data ingested? `DROP GRAPH <https://cair-nepal.org/heritagegraph/imported/lux>` (or `make reset-everything` for full wipe). The HG-native graph is never touched.

## Security notes

* Oxigraph 0.4 ships without auth on the HTTP endpoint. Do **not** expose port 7878 to the public internet without a reverse proxy + TLS + basic auth or OAuth.
* `LUX_DUMP_URL` is fetched at the migration window only; ensure outbound HTTPS to Yale is allowed.
* The `delta-syncer` does the same fetch every Monday — same firewall rule.

## What this Compose does NOT do

* It does not provision the host (RAM, NVMe, OS, Docker) — bring your own server.
* It does not handle TLS termination — pair with Caddy/nginx if exposing to the internet.
* It does not back up to remote storage — `make backup` writes locally; pair with restic/rclone if you need offsite copies.
* It does not schedule Niraj/Nabin's *agentic AI ingestion* pipeline — that's a separate concern; LUX migration just enriches the same Oxigraph store they ingest into.
