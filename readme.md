# HeritageGraph Ontology

Event-centric LinkML schema and OWL release for Nepalese living heritage, aligned with CIDOC-CRM, CRMinf, PROV-O, and Europeana EDM.

**Namespace:** `https://w3id.org/heritagegraph/`  
**Version:** 1.0.0

## Repository layout

All ontology files live in `ontology/`; the generated documentation site lives
in `docs/` (never hand-edit — it is rebuilt by `scripts/build.sh`).

| Artefact | Purpose |
|----------|---------|
| `ontology/HeritageGraph.yaml` | LinkML source of truth |
| `ontology/HeritageGraph.ttl` | OWL/Turtle ontology (core) |
| `ontology/heritagegraph-lux-alignment.ttl` | LUX (Yale Linked Art / CIDOC-CRM) bridge module |
| `ontology/HeritageGraph.shacl.ttl` | SHACL validation shapes |
| `ontology/HeritageGraph-lux.shacl.ttl` | SHACL shapes for the LUX bridge classes |
| `ontology/HeritageGraph-alignment.ttl` | CRM/PROV/Wikidata alignment module |
| `ontology/HeritageGraph-edm.ttl` | Europeana Data Model projection |
| `ontology/heritagegraph-metadata.ttl` | VoID dataset description |
| `examples/kathmandu-mini-abox.ttl` | Sample instance data |
| `CHANGELOG.md` | Release notes |

## Build the documentation + visualization

Regenerate the whole documentation site (Widoco docs + WebVOWL of the **merged**
core + LUX ontology) after any ontology change:

```bash
make docs            # = scripts/build.sh  → writes ./docs
make preview         # build into /tmp/hg-preview without touching docs/
make webvowl         # build, then serve http://localhost:8000/webvowl/
```

Requires Docker (Widoco runs owl2vowl inside the container — no local Java needed).

## Regenerate everything

```bash
pip install -r requirements.txt linkml owlrl
python3 scripts/regenerate_ontology_artifacts.py
python3 scripts/run_release_quality.py
```

## Evaluate

```bash
cd evaluation && pip install -r requirements.txt
make -C evaluation all   # or run individual run_*.py scripts
```

Quality summary: `release/QUALITY_REPORT.md`

## Manuscript (NPJ draft)

Publication-quality LaTeX rewrite: `manuscript/HeritageGraph.tex`

```bash
python3 scripts/generate_manuscript_figures.py
cd manuscript && pdflatex HeritageGraph && bibtex HeritageGraph && pdflatex HeritageGraph
```

Editorial assessment: `manuscript/EDITORIAL_ASSESSMENT.md`

## Journal / release readiness

| Step | Action |
|------|--------|
| 1 | `python3 scripts/regenerate_ontology_artifacts.py` |
| 2 | `python3 scripts/run_release_quality.py` |
| 3 | Tag `v1.0.0` and push to GitHub |
| 4 | Open w3id PR using `w3id/heritagegraph/.htaccess` |
| 5 | Submit `registry/lov-metadata.ttl` to LOV after w3id is live |

HermiT DL log: `release/evaluation/hermit_consistency_log.txt` (auto-generated in CI when Java is available).

## Excel export

```bash
python3 scripts/export_heritagegraph_to_excel.py
```

## Documentation

`scripts/build.sh` (also `make docs`) regenerates the Widoco docs + WebVOWL into
`docs/`. CI runs the same script via `.github/workflows/ci.yaml` and deploys
`docs/` to GitHub Pages on every push.
