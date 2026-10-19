# Contributing to heritagegraph-lux-migration

Thanks for your interest. This document describes how to propose changes — to the alignment, the migration scripts, or the documentation — and how the project keeps quality stable.

## Quick rules

1. **Open an issue first** for non-trivial changes (new HG class proposals, alignment-breaking edits, new Docker services). For typo fixes and small clarifications a direct PR is fine.
2. **Branch from `main`**, name the branch `feat/<short-name>`, `fix/<short-name>`, or `docs/<short-name>`.
3. **One concern per PR.** Don't mix alignment edits with infrastructure changes.
4. **Every PR must pass CI** (TTL parse, Python syntax, SPARQL syntax). Locally: `make ci-local`.

## Setting up

```bash
git clone https://github.com/CAIRNepal/heritagegraph-lux-migration.git
cd heritagegraph-lux-migration
python3 -m venv .venv && source .venv/bin/activate
pip install rdflib pyoxigraph requests tqdm
make ci-local        # ttl-check + py-check
```

You do not need a running Oxigraph for most local checks. For end-to-end testing:

```bash
cp docker/.env.example docker/.env
# edit docker/.env: RING_MODE=crawl, LIMIT_PER_QUERY=100 (fast local smoke)
make up
make logs
```

## Where to put things

| Type of change | Where to edit |
|---|---|
| Alignment fact (a HG class ↔ CIDOC/LinkedArt mapping) | `alignment/heritagegraph-lux-alignment.ttl` |
| Mapping spreadsheet | edit `mapping/build_mapping.py` then run it to regenerate `mapping/HeritageGraph_LUX_Mapping.xlsx` — do not hand-edit the .xlsx |
| Transformation query | `queries/lux_to_hg_migration.sparql` |
| Validation query | `queries/validation_queries.sparql` |
| Migration orchestrator behaviour | `scripts/migrate_lux_to_hg.py` |
| Container behaviour | `docker/migrator/entrypoint.sh` or `Dockerfile` |
| Server deployment | `deploy.sh` (rsync + ssh), `scripts/server-bootstrap.sh` (one-shot host prep) |
| Long-form docs | `docs/` |

## Alignment changes — extra care

The alignment ontology is the source of truth that downstream consumers depend on. If you add or change a triple:

1. **Cite your evidence** in the PR description. For Linked Art mappings, link to the relevant section of `linked.art/model/...` or quote the JSON-LD context at `https://linked.art/ns/v1/linked-art.json`. For CIDOC-CRM, link to `cidoc-crm.org/Property/Pnn-…` or `cidoc-crm.org/Entity/Enn-…/version-7.1.3`.
2. **Re-run the verification** (see `docs/VERIFICATION_FINDINGS.md` §method). Update that doc if your change invalidates any prior finding.
3. **Update the XLSX**: `python mapping/build_mapping.py` regenerates it from the canonical Python data; commit the regenerated file too.
4. **Keep `owl:equivalentClass` strict.** Use `rdfs:subClassOf` for one-way refinements, `skos:closeMatch` for non-strict semantic neighbours, `skos:broadMatch` when HG is broader.

## Coding style

* Python: standard library + `rdflib`/`requests`/`pyoxigraph`. `ruff` clean (line length 100). No new heavy deps without discussion.
* Shell: `set -Eeuo pipefail` at the top; functions with `local`; quote all variables; `bash -n` must pass.
* SPARQL: 4-space indent, prefix block first, queries separated by `# === label ===` headers (so the migrator can iterate them).
* Turtle: 4-space indent, group by section comment, prefer `;` continuation over repeated subject.

## Testing checklist for a migration-affecting PR

- [ ] `make ci-local` passes (TTL parses, Python syntax OK)
- [ ] Pilot run completes locally: `make up && make logs` shows phase P7 = master.done
- [ ] V1 / V2 hard gates pass: `make validate` returns 0
- [ ] If you changed alignment: V3 (count parity) still within ±5%
- [ ] If you changed entrypoint/Dockerfile: image rebuilds cleanly

## Reporting LUX upstream changes

Yale ships LUX schema updates periodically. If you see V1 reporting new unmapped class types after a delta sync, please:

1. Open an issue titled `LUX schema drift: <className>`.
2. Attach the V1 output snippet (class URI + instance count).
3. Suggest the alignment line(s) needed.

## Commit messages

Use imperative present tense, 50-char subject line, blank line, optional body. Conventional-commits-style scopes welcome:

```
fix(alignment): correct la:Encounter to sci:S19_Encounter_Event

la:Encounter is not in the Linked Art JSON-LD context as crm:E87.
It expands to sci:S19_Encounter_Event (CRMsci extension).
Updates TTL, XLSX, SPARQL.

Refs #N
```

## License of contributions

By submitting a PR you agree that your contribution is licensed under the project's Apache License 2.0 (see `LICENSE`). The alignment ontology and mapping spreadsheet stay under Apache 2.0 to match Yale's LUX and project-lux/data-pipeline.

## Contact

* Issues: https://github.com/CAIRNepal/heritagegraph-lux-migration/issues
* Maintainers: Tek Raj Chhetri, Semih Yumuşak, Niraj Karki, Nabin Oli
* For LUX-specific questions, ping the [Linked Art Slack](https://linked-art.slack.com/) or open an issue at https://github.com/project-lux/data-pipeline.
