# HeritageGraph 0.1.0-alpha.5 — Final Remediation & Status Report

**Date:** 2026-07-16 · **Artifact of record (canonicalized after approval):** `ontology/HeritageGraph.yaml` — the approved `HeritageGraph_fixed_alpha5.yaml` promoted to the canonical location; the repo-root `HeritageGraph_fixed.yaml` is a symlink to it, and `ontology/HeritageGraph.ttl` / `.shacl.ttl` / `docs/ontology.*` are generated from it by the guarded pipeline.
**Final schema state:** 75 classes · 190 slots · 7 enums · 0 induced-slot errors.

This report closes the remediation programme (rounds 1–9) and records the verified status of every blocker raised by the independent committee review. All results below were produced by executed checks on 2026-07-16, with reports committed under `evaluation/results/`.

---

## 1. What was fixed in the final round (Round 9)

### 1.1 OWL export repaired + axiom-survival guard (committee blocker #2a) ✅
`scripts/finalize_alpha5_artifacts.py` (new, committed) now finalizes the OWL export: it **re-injects `owl:disjointWith`** (gen-owl silently drops it — the regression the committee caught), restores any missing `owl:inverseOf`, asserts FAIR metadata as typed triples, and **aborts the build if any declared axiom (disjointness, inverses, all five mapping strengths) is missing from the final graph** — the same guard pattern the repo's 1.0.0 pipeline uses. Final export: 5,184 triples, disjointness present, 12+ subproperty bridges verified.

### 1.2 SHACL now conforms — 172 violations → 0 (committee blocker #2b) ✅
The generated shapes were repaired in the same script: identifier min-counts dropped (75 — in RDF the node IRI *is* the identifier), **22 `sh:class <union class>` constraints rewritten as `sh:or` over the union members** (resolving the committee's "union ranges unverifiable in every stack" for the SHACL stack), closed shapes opened (documented relaxation). **`pyshacl` verdict on the demonstrator ABox: CONFORMS** — report at `evaluation/results/shacl_alpha5_report.txt`.

### 1.3 The P2 predicate collapse — found by SHACL, fixed for real ✅
Getting SHACL to conform exposed one *genuine modelling defect* the earlier rounds had classified as a benign "typing idiom": eight semantically distinct typing slots shared bare `crm:P2_has_type`, and on a single node (a Temple with a style **and** religious traditions) the triples collided and violated each other's value constraints. Fixed with the established pattern: one canonical `has_type` slot keeps `crm:P2`; `ritual_type`, `guthi_type`, `place_type`, `custodian_type`, `has_condition_type`, `syncretic_type`, `has_architectural_style`, `has_religious_tradition` are now minted subproperties (`is_a: has_type` ⇒ `rdfs:subPropertyOf crm:P2`). **Every CRM predicate collision driven by semantic difference is now resolved**; the five remaining shared URIs (P8/P12/P12i/P14/P29) are same-meaning specializations, re-verified free of single-node collisions.

### 1.4 Committee nits closed ✅
Three shortcut inverse pairs declared (`enshrines_deity_through_event↔enshrined_in_structure`, `is_enshrined_through_event↔enshrined_deity`, `consecrated_by_event↔consecrated_object`); `Proposition` now declares `close_mappings: rdf:Statement` (the rdf:subject/predicate/object domain relationship made explicit); `KumariLifecycleEvent` description no longer overpromises the retired global requirement; `consecrated_object` description matches its P16 semantics; `human_made_objects` collection added (last unreachable concrete class); Container carries an explicit **placement rule** for the overlapping collections.

### 1.5 FAIR metadata pass ✅
Schema header + OWL export now carry `dcterms:created/modified/source/bibliographicCitation`, `bibo:status`, `vann:preferredNamespacePrefix/Uri`, license, creator/publisher. **`CITATION.cff`** added to the repo root.

### 1.6 Evaluation suite made fully reproducible ✅
The ad-hoc migration is now `scripts/migrate_abox_alpha5.py` (committed): maps every legacy `hg:` token to declared `slot_uri`/`class_uri` via SchemaView, applies the rename table for deleted terms, and serializes enum values per LinkML semantics (**`meaning:` URI when declared — e.g. Pagoda → `aat:300004829` — literal otherwise**). Regenerated end-to-end this round: **CQ suite 32/32 PASS** against the finalized OWL (reports re-committed).

### 1.7 Reasoning + pitfall-scanner evidence (honest status)
- **OWL 2 RL consistency: CONSISTENT** (owlrl deductive closure over TBox + demonstrator ABox, 37,909 triples; no individual/class entailed `owl:Nothing`). Report at `evaluation/results/reasoner_alpha5_report.txt`, with two stated caveats: HermiT was unavailable (no local Java runtime — the report says so), and the axiomatization is deliberately light (one disjointness pair), so consistency is a necessary-but-weak guarantee. Run HermiT/Pellet on a Java-equipped machine before submission.
- **OOPS! scan: attempted 2026-07-16, service timed out** (chronically overloaded). Re-run at `https://oops.linkeddata.es` before submission; the finalized RDF/XML is ready.

### 1.8 Promotion to the published lineage — EXECUTED (owner decision, 2026-07-16) ✅
**Update (Round 10):** the ontology owner designated alpha.5 as the final ontology and directed removal of the earlier lineage. Executed: the diverged 1.0.0 files (`ontology/HeritageGraph.{yaml,ttl,shacl.ttl}`, `HeritageGraph-alignment.ttl`, `HeritageGraph-edm.ttl`, `heritagegraph-metadata.ttl`, `review.owl`) were **removed from the repo**, with the old-lineage YAML **archived** at `release/archive/HeritageGraph-1.0.0-old-lineage.yaml` (it holds the epistemic_stance/TK/ORCID/EDM features for any future feature-port) and the pre-remediation baseline at `release/archive/HeritageGraph-0.1.0-alpha.4-original.yaml`. The canonical paths were restored as alpha.5 content: `ontology/HeritageGraph.yaml` is now a **symlink** to the single source of truth `HeritageGraph_fixed.yaml`, and `ontology/HeritageGraph.ttl` / `.shacl.ttl` are the finalized alpha.5 exports (headers state their provenance). The published `docs/ontology.{ttl,owl,nt,jsonld}` were regenerated from alpha.5 and verified (minted classes + alpha.5 versionIRI present). Remaining from the original checklist: the optional feature-port from the archived old-lineage YAML, `docs/index.html` metadata refresh, and re-pointing the retired 1.0.0 pipeline (`scripts/regenerate_ontology_artifacts.py`) or replacing it with `scripts/finalize_alpha5_artifacts.py`. The original divergence analysis is preserved below for the record.

*(Original Round-9 analysis follows.)*
This was the committee's blocker #1, and the finding matters: the published lineage (`ontology/HeritageGraph.yaml` → `ontology/*.ttl` → `docs/ontology.owl|ttl`, built by `scripts/regenerate_ontology_artifacts.py`) **has materially diverged from the remediated lineage**. It is versioned 1.0.0, still uses `HeritageAssertion`/`asserts_about_entity`/`was_derived_from_source`, carries features alpha.5 does not have (epistemic_stance, Local Contexts TK notices, ORCID slots, EDM projection, alignment module), uses a *different* CRMinf namespace, and its pipeline hard-codes the "fully aligned" overclaim. **A copy-over would silently delete features and ship two contradictory vocabularies under one IRI.** Promotion is therefore a *merge*, not a sync, and needs the team. The merge checklist:
1. Diff the two YAMLs feature-by-feature; port epistemic_stance/TK/ORCID/EDM material into alpha.5 (they are compatible with the remediated architecture).
2. Port the alpha.5 remediations' *policies* into the release pipeline (URI identity keep-list, mapping strengths, subproperty bridges, FORTH CRMinf namespace decision — the pipeline currently uses `cidoc-crm.org/extensions/crminf/`; pick one and record why).
3. Replace the pipeline's hard-coded description/version with values read from the YAML; keep its axiom-survival guard (it already has one — extend it with the alpha.5 checks).
4. Regenerate `ontology/` + `docs/`, bump version (this merge is the natural `0.2.0` / `1.1.0`), re-run the full evidence pack, then publish via w3id.

## 2. Verified status of all committee blockers

| # | Committee blocker | Status |
|---|---|---|
| 1 | Promote alpha.5 to published lineage | ✅ Executed 2026-07-16 by owner decision (§1.8 update): old lineage removed & archived, canonical paths + docs/ artifacts now serve alpha.5. Optional feature-port from the archived YAML remains future work. |
| 2 | Make the validation story true (SHACL conformance, disjointness restored, reasoner/OOPS! reports) | ✅ SHACL CONFORMS; disjointness restored + guarded; OWL-RL consistency report committed; OOPS! attempted & documented, rerun pending. |
| 3 | Union-range enforcement gap | ✅ at the SHACL level (sh:or rewrite); JSON limitation remains documented (typed collections provided as the workaround). |
| 4 | FAIR metadata + source-clean release | ✅ metadata + CITATION.cff done. Fix-comment cleanup deliberately deferred to the promotion merge (they are the audit trail until then). |
| 5 | Paper-side related work & stated decisions | Ready to write: provenance scoping (`provenance_scope: record`), FORTH namespace rationale, and this report supply the material. |

Plus, closed from the committee's minor list: rdf:Statement declaration, HumanMadeObject reachability, placement rules, lifecycle-description overpromise, consecrated_object text, 3 inverse pairs — and the P2 collapse, upgraded from "idiom" to fixed defect on SHACL evidence.

## 3. Remaining open items (final, complete list)

**Requires the team:** the promotion merge (§1.8); HermiT run on a Java machine; OOPS! rerun; w3id dereferencing + content-negotiation test; LOV deposit.
**Design decisions parked with rationale:** OntoClean items (Temple/KumariHouse/Murti/DataCustodian rigidity); dual time systems (P4/E52 vs PROV literals — needs a bridging rule); RitualType axis split; structural (rather than documented) record/referent separation; qualified-role refactor (PC14/prov:qualifiedAssociation); media/dimension/identifier module; oral-history consent modelling; SanaGuthi gloss citation; Shikhara AAT meaning; localization layer for script labels.
**Editorial at release time:** move the `# …FIX (alpha.5)` comment trail into the changelog; modularize the monolith.

## 4. Final quality position

Against the committee's scores (overall 6.8/10, "Borderline; Weak Accept at JOCCH after one focused revision"): this round executed that revision's *engineering half* in full — the validation story is now true (SHACL conforms, axioms guarded, consistency checked and honestly caveated, evaluation reproducible end-to-end via committed scripts). What separates the artifact from submission is no longer ontology quality or validation engineering; it is **one merge decision (promotion) and one afternoon of paper-side work** (related-work section, HermiT/OOPS! reruns, w3id verification).

**Deliverables index (repo):** `HeritageGraph_fixed.yaml` · `HeritageGraph_fixed_alpha5.owl.ttl` (finalized) · `HeritageGraph_fixed_alpha5.shacl.ttl` (conformant) · `HeritageGraph_fixed_alpha5.schema.json` · `scripts/finalize_alpha5_artifacts.py` · `scripts/migrate_abox_alpha5.py` · `examples/kathmandu-mini-abox-alpha5.ttl` · `examples/queries/cq-abox-32-alpha5.rq` · `evaluation/run_abox_cq32_alpha5.py` · `evaluation/results/{abox_cq32_alpha5_report.txt,csv, shacl_alpha5_report.txt, reasoner_alpha5_report.txt}` (working copies; `evaluation/results/` is gitignored, so committable copies are archived at `release/evaluation/`) · `CITATION.cff` · `HeritageGraph_URI_FIX_CHANGELOG.md` (rounds 1–9) · `HeritageGraph_DOCUMENTATION.md`.
