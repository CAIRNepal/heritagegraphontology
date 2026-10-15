# Independent-data bundle

Third-party data mapped to the released HeritageGraph vocabulary
(`http://cair-nepal.org/heritagegraph/`), used by `evaluation/run_danam_scale_cq.py`.

| File | Origin | How to regenerate |
|---|---|---|
| `raw/danam/`, `raw/danam.json` | DANAM API pages (raw source) | — (source snapshot) |
| `raw/shapes_spec.json` | Snapshot of the initial DANAM pipeline's SHACL shape specification (pre-1.0.0 vocabulary). Not read by any script. It still names the deprecated CIDOC-CRM `P120_occurs_before` and the non-existent `P120i_is_occurred_before_by`; the released ontology and shapes use `crm:P183_ends_before_the_start_of` / `crm:P183i_starts_after_the_end_of`. | — (historical snapshot, kept unmodified) |
| `reconciled/store_export.nq` | N-Quads export of the initial pipeline's Fuseki/TDB2 store (pre-1.0.0 vocabulary, `https://cair-nepal.org/heritagegraph/`). Its header comments note the legacy P120 references, which occur only in the old T-Box graph that reconciliation drops. | — (reconciliation input, kept unmodified) |
| `reconciled/danam-heritagegraph.nq` | `store_export.nq` rewritten to the released vocabulary via `reconcile_crosswalk.json` | `python3 data/reconcile_store.py` |
| `reconciled/wikidata-kv.nq` | Wikidata enrichment, each statement `prov:wasDerivedFrom` its Wikidata IRI | `python3 data/enrich_wikidata.py` (queries Wikidata live) |

`wikidata-kv.nq` was moved to the `cair-nepal.org` namespace by a pure IRI rewrite of the
existing snapshot (no re-query of Wikidata), so its statements are those retrieved on the
date recorded in its source note; re-running `enrich_wikidata.py` refreshes them.
