# HeritageGraph ↔ LUX migration

Ontology alignment and migration pipeline that lifts Yale's [LUX](https://lux.collections.yale.edu/) (Linked Art / CIDOC-CRM) cultural-heritage records into the [CAIR Nepal HeritageGraph](https://github.com/CAIRNepal/heritagegraphontology) knowledge graph.

| | |
|---|---|
| Source dataset | LUX — ~16 M Linked Art records across objects, persons, places, concepts, events, sets, works |
| Target dataset | HeritageGraph — Nepal-focused cultural heritage ontology |
| Alignment | 273 OWL triples (33 new HG class declarations, 12 `owl:equivalentClass`, 88 `rdfs:subClassOf`, 18 `owl:equivalentProperty`, 45 `rdfs:subPropertyOf`) |
| Migration tooling | Python (`rdflib`, `pyoxigraph`) + SPARQL CONSTRUCTs + Docker Compose |
| Target triplestore | [Oxigraph](https://github.com/oxigraph/oxigraph) — embedded or HTTP |
| Status | alignment verified · pilot ready · server-deployable |

## Quick start (local pilot — ~30 min)

```bash
git clone https://github.com/CAIRNepal/heritagegraph-lux-migration.git
cd heritagegraph-lux-migration

# 1. fetch HeritageGraph.ttl into alignment/
curl -L -o alignment/HeritageGraph.ttl \
  https://raw.githubusercontent.com/CAIRNepal/heritagegraphontology/HeritageGraph/ontology/HeritageGraph.ttl

# 2. configure
cp docker/.env.example docker/.env
$EDITOR docker/.env        # RING_MODE=crawl, LIMIT_PER_QUERY=10000 by default

# 3. run
make up
make logs                  # follow migration progress
make status                # triple counts per named graph
make validate              # V1/V2 hard-gate validation
```

## Quick start (server deployment)

Targets `server42.dnsbilisim.net` (or override via `.deploy.env`):

```bash
# first time only — provisions Docker, /root/github/heritagegraph-lux-migration/, systemd unit, logrotate
make deploy-bootstrap

# every deploy
make deploy                # rsync repo + docker compose up -d --build

# observe
make ssh-status
make ssh-logs-migrator
```

Full playbook: [`docs/DEPLOY_SERVER.md`](docs/DEPLOY_SERVER.md).

## Repository layout

```
heritagegraph-lux-migration/
├── README.md                        ← you are here
├── LICENSE                          ← Apache 2.0
├── CONTRIBUTING.md
├── CHANGELOG.md
├── Makefile                         ← `make help` for all targets
├── deploy.sh                        ← lokal → server42 rsync deploy
├── .gitignore
├── .github/workflows/               ← CI: TTL parse, Python lint, SPARQL syntax
│
├── alignment/                       ← the OWL alignment ontology
│   ├── heritagegraph-lux-alignment.ttl
│   └── HeritageGraph.ttl            ← (gitignored — fetched from upstream)
│
├── mapping/                         ← human-facing mapping artefact
│   ├── HeritageGraph_LUX_Mapping.xlsx   ← 5 sheets: classes / props / new HG / coverage / notes
│   └── build_mapping.py             ← regenerates the XLSX
│
├── queries/                         ← SPARQL
│   ├── lux_to_hg_migration.sparql   ← 9 CONSTRUCT-as-INSERT transforms
│   └── validation_queries.sparql    ← 8 post-migration checks (V1/V2 hard gates)
│
├── scripts/                         ← runnable Python + shell
│   ├── migrate_lux_to_hg.py         ← 4-mode orchestrator (crawl/transform/validate/delta)
│   ├── discover_lux_endpoints.sh    ← probes which LUX endpoints are live
│   └── server-bootstrap.sh          ← runs ONCE on the server
│
├── docker/                          ← container stack
│   ├── docker-compose.yml           ← oxigraph + migrator + delta-syncer
│   ├── .env.example
│   └── migrator/
│       ├── Dockerfile
│       ├── entrypoint.sh            ← 7-phase orchestrator, idempotent
│       └── delta_loop.sh            ← supercronic-driven weekly sync
│
└── docs/                            ← all the long-form documentation
    ├── MIGRATION_PLAN.md            ← 7-phase migration scenario
    ├── DEPLOY_SERVER.md             ← server42 playbook
    ├── LUX_DATA_DOWNLOAD.md         ← how to get LUX data (REST/dump/AS)
    ├── DOCKER_USAGE.md              ← docker stack reference
    └── VERIFICATION_FINDINGS.md     ← deep verification report + 6 bug fixes
```

## What's inside

### The alignment (`alignment/heritagegraph-lux-alignment.ttl`)

* **65 HG classes** mapped to either `crm:` (CIDOC-CRM) or `la:` (Linked Art-only — only seven of these exist; the rest of the LUX short names expand directly to `crm:` URIs).
* **69 HG properties** aligned via `owl:equivalentProperty` or `rdfs:subPropertyOf`.
* **34 new HG classes proposed** (drop-in TTL scaffolding) for full LUX migration coverage — Birth, Death, Formation, Dissolution, Acquisition, Move, VisualItem, LinguisticObject, DigitalObject, Set, Identifier, Name, MeasurementUnit, Dimension, Right, LegalObject, Modification, Language, Currency, BeginningOfExistence, EndOfExistence, PropositionalObject, Measurement, Inscription, Title, CuratedHolding, CurationActivity, MonetaryAmount, AttributeAssignment, Period, Encounter, ProvenanceActivity, Group, AttributeAssignment.
* Verified against the [official Linked Art JSON-LD context](https://linked.art/ns/v1/linked-art.json) — see [`docs/VERIFICATION_FINDINGS.md`](docs/VERIFICATION_FINDINGS.md) for the six material bugs found and fixed.

### The migration (`scripts/migrate_lux_to_hg.py`)

Four operational modes, each invokable from the CLI:

| Mode | What it does |
|---|---|
| `crawl` | REST-fetch records from LUX's `/api/search/*` endpoints, write JSON-LD to disk |
| `transform` | Batched SPARQL `INSERT WHERE` over the LUX raw graph → HG instances in the imported graph |
| `validate` | Runs the 8 validation queries; V1/V2 are hard gates (exit 1 on failure) |
| `delta` | Pull the latest LUX diff, apply it, re-run validation |

### The Docker stack (`docker/`)

Three services:

* **oxigraph** — Rust-based SPARQL 1.1 triplestore, persistent volume, healthcheck.
* **migrator** — one-shot container that runs the 7-phase pipeline (fetch → bulk-load → load HG → transform → validate → snapshot → master flag). Idempotent via flag files.
* **delta-syncer** — long-running container, supercronic-driven weekly delta sync after the initial migration completes.

## How LUX data gets in

LUX does **not** publish a public bulk dump as of May 2026. Realistic paths (detailed in [`docs/LUX_DATA_DOWNLOAD.md`](docs/LUX_DATA_DOWNLOAD.md)):

1. **Email Yale** ([lux@yale.edu](mailto:lux@yale.edu)) for an academic-use dump — recommended, ~1-2 weeks turnaround.
2. **IIIF Change Discovery / ActivityStreams** — Yale's blessed harvester protocol (~3-4 days for full dataset).
3. **REST per-record crawl** — `scripts/migrate_lux_to_hg.py --mode crawl`, ~2-4 days for full, ~30 min for a 10K-record pilot.
4. **LuxY Python wrapper** — Yale's official client at https://github.com/project-lux/luxy.
5. **Selective subset** — filter to South/East Asian religious heritage (~50-200K records, 6-12 hours) — recommended production scope.

Run `scripts/discover_lux_endpoints.sh` first to see which endpoints are actually responding before configuring `.env`.

## Validation gates

After migration, `make validate` runs eight queries (`queries/validation_queries.sparql`). Two are **hard gates**:

* **V1** — every LUX class type must have a HG target class. Returns 0 rows when alignment is complete.
* **V2** — every imported HG instance must carry exactly one `owl:sameAs` back to its LUX origin URI.

The other six (count parity, unaligned-property usage, round-trip spot-check, HG-native class preservation, unique type per record, orphan check) are informational.

## Citing

If you use this package in a paper:

```bibtex
@software{heritagegraph_lux_migration,
  author  = {Yumuşak, Semih and Chhetri, Tek Raj and Karki, Niraj and Oli, Nabin},
  title   = {{HeritageGraph–LUX migration}: ontology alignment and ingestion pipeline},
  year    = {2026},
  url     = {https://github.com/CAIRNepal/heritagegraph-lux-migration},
  license = {Apache-2.0}
}
```

## Acknowledgements

* Yale University's LUX team and the [Linked Art](https://linked.art/) community for the source data model and exemplars.
* CAIR Nepal for the HeritageGraph ontology.
* The CIDOC-CRM SIG and IIIF community for the underlying standards.

## License

Apache License 2.0 — see [`LICENSE`](LICENSE).

The alignment ontology (`alignment/heritagegraph-lux-alignment.ttl`) and the mapping spreadsheet are released under Apache 2.0 to match Yale LUX and project-lux/data-pipeline. The CAIR Nepal HeritageGraph ontology (`alignment/HeritageGraph.ttl`, fetched at install time) keeps its upstream license — see the [HeritageGraph repo](https://github.com/CAIRNepal/heritagegraphontology).
