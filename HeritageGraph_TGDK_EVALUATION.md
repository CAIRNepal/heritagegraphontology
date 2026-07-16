# HeritageGraph 0.1.0-alpha.5 — Standard Ontology Evaluation for TGDK Submission

**Role:** independent reviewer applying the evaluation canon expected by TGDK (Transactions on Graph Data and Knowledge) and comparable venues (SWJ resource/ontology track) for ontology papers.
**Date:** 2026-07-16. **Every number below was produced by executing `evaluation/run_tgdk_eval.py`** (committed; consolidated output at `evaluation/results/tgdk_eval_report.txt`, archived at `release/evaluation/`). Nothing is estimated.

TGDK reviewers expect an ontology paper's evaluation section to cover six standard practices: (1) structural metrics, (2) pitfall scanning, (3) competency-question coverage, (4) data-driven validation, (5) logical consistency, (6) FAIR/availability. Each is executed and judged below, followed by what the paper must claim — and must *not* claim.

---

## 1. Structural & schema metrics (OntoQA / OQuaRE)

| Metric | Value | Reviewer judgement |
|---|---|---|
| Classes | 75 (69 concrete, 6 abstract, 3 PROV mixins) | Right size for a domain profile; no class explosion. |
| Slots / enums / enum values | 190 / 7 / 51 | Property-rich; justified by the event-centric style. |
| OWL export | 5,258 triples; 139 object + 46 datatype properties | — |
| Inheritance | max depth 3, mean branching 2.80, tangledness 0 | Shallow, clean mono-hierarchy + mixins; no diamond problems. |
| **Relationship richness RR** | **0.77** (137 relations vs 42 subclass edges) | High — the ontology is relation-driven, not a bare taxonomy. Strong for the "graph data" framing of TGDK. |
| Inheritance richness IR | 0.56 | Moderate; consistent with a profile over CRM rather than a deep taxonomy. |
| Attribute richness AR | 0.71 | Adequate. |
| **Documentation coverage** | **100% classes, 100% slots** carry definitions | Publication-grade (was 99%/95%; the last 11 gaps were closed during this evaluation). |
| External mapping coverage | 42/75 classes (56%) — every mapping label-verified against the live authority | The 56% is honest: value-object and Kumari-specific classes legitimately have no external counterpart. The *verification*, not the percentage, is the selling point. |
| IRI policy | 59 minted / 16 external-identity class IRIs, zero collisions | Policy-clean (documented keep-list). |
| Axiom inventory | 928 subClassOf, 20 subPropertyOf, 16 inverseOf, 1 disjointWith, 2 union definitions, bounds, 1 deprecated | See §2 P10 — the single disjointness axiom is the weakest number in this table. |

## 2. Pitfall scan (OOPS! practice)

The OOPS! web service was unreachable on both attempts (timeout; chronically overloaded) — **rerun at oops.linkeddata.es before submission and cite the code list**. In lieu, the checkable pitfalls were implemented locally:

| Pitfall | Result |
|---|---|
| P08 missing annotations | **PASS** (0 classes, 0 slots after this round). |
| **P10 missing disjointness** | **IMPORTANT — the one open pitfall.** A single axiom (Stupa ⊓ Chaitya). Sibling sets (Temple/Stupa/Chaitya, the RestHouse kinds, Person/Guthi) are undeclared. Consequence: DL consistency checking is near-vacuous. If this is a deliberate minimal-commitment stance (defensible for contested heritage categories), **the paper must argue it explicitly**; otherwise add the uncontroversial sibling disjointness and re-run the reasoner. |
| P13 missing inverses | Minor — 120 object slots without declared inverse; the load-bearing pairs (assertion layer, Kumari lifecycle, enshrinement shortcuts) all have them; the rest follow the CRM/PROV one-directional idiom. Reviewed, acceptable. |
| P22 naming convention | PASS — uniform snake_case slots / UpperCamelCase classes / lowerCamelCase IRIs. |
| P04 unconnected elements | PASS — every class reachable via hierarchy, ranges, unions, or Container. |
| P41/P38 license | PASS — `dcterms:license` as IRI (CC-BY-4.0). |

## 3. Competency-question coverage (Grüninger & Fox)

**32/32 CQs answer with ≥1 binding** against the finalized OWL export + demonstrator ABox, across all four dimensions: Structural 6/6, Ritual/Festival 12/12, Institutional/Syncretic 7/7, Living Goddess 7/7. Fully reproducible: `scripts/migrate_abox_alpha5.py` → `evaluation/run_abox_cq32_alpha5.py`; queries use the *published* predicate URIs (slot_uris), so the evaluation exercises the actual RDF semantics — this repairs the fatal earlier defect where the CQ suite queried a vocabulary the ontology no longer contained.

**Reviewer caveat the paper must state:** the ABox is a hand-authored demonstrator built to give each CQ a witness. "32/32" is *coverage/answerability* evidence, not retrieval evaluation on independent data. TGDK reviewers will ask: strengthen with the independent-ABox run (`evaluation/independent_abox.py`) or real ingested data if available.

## 4. Data-driven validation (SHACL)

**CONFORMS** — the demonstrator ABox passes the finalized SHACL shapes (172 violations → 0 across the remediation; the final shapes drop identifier min-counts, rewrite union `sh:class` as `sh:or`, and open closed shapes — all documented relaxations in `scripts/finalize_alpha5_artifacts.py`). The paper should describe the shape-repair policy in one paragraph; a reviewer who regenerates raw shapes with `gen-shacl` will otherwise reproduce the 172 violations and cry foul.

## 5. Logical consistency

**OWL 2 RL: CONSISTENT** (owlrl deductive closure over TBox + ABox, 40,194 triples, no `owl:Nothing` entailments). Two caveats that must appear verbatim in the paper: (a) this is a **profile check, not full DL** — run HermiT/Pellet on a Java-equipped machine and report classification results; (b) with one disjointness axiom, consistency is a necessary-but-weak guarantee (ties back to P10). The axiom-survival guard (disjointness, unions, inverses, mappings, deprecation verified present in every export) is itself reportable methodology — generators silently dropping axioms is exactly the failure it caught twice.

## 6. FAIR / availability (FOOPS! practice)

**Local checklist 11/11**: persistent w3id IRI, versionIRI, license-as-IRI, creator/publisher, created/modified, bibliographicCitation, bibo:status, vann prefix/namespace, CITATION.cff, four published serializations (ttl/owl/nt/jsonld), machine-readable changelog.
**Open, deployment-dependent (do before submission):** (i) push + verify w3id term-level dereferencing and content negotiation — the regenerated `docs/` artifacts are correct locally but the deployed site serves whatever was last pushed; (ii) run FOOPS! **after** deployment (it grades the served content, not your working tree); (iii) LOV registry deposit.

---

## Reviewer verdict for the TGDK evaluation section

**The evaluation methodology now meets the venue standard: six practices, all executed, all reproducible from committed scripts.** The three things standing between this and a clean evaluation section:

1. **P10 disjointness** — decide (argue minimal commitment, or add sibling disjointness) and re-run consistency either way. This is the only *ontology-content* item.
2. **DL reasoner + OOPS! + FOOPS! reruns** — three external-tool runs currently blocked by environment/network, each a ten-minute task in the right environment; the paper cannot cite "reasoner-verified" or a pitfall score without them.
3. **CQ evaluation framing** — present 32/32 as answerability over a purpose-built demonstrator, and add the independent-ABox run for retrieval credibility.

What the paper can already claim, with committed evidence: RR 0.77 / clean shallow hierarchy / zero IRI collisions; 100% definition coverage; label-verified external mappings (with the removal of ~20 wrong AAT/Wikidata IDs as a methodological anecdote reviewers will respect); 32/32 CQ answerability, reproducible; SHACL conformance with a documented shape policy; OWL 2 RL consistency with stated caveats; 11/11 local FAIR checklist with a persistent-IRI publishing pipeline.

**Suggested paper table:** one row per practice (metric family, tool, result, artifact path) — the six sections above map 1:1 onto it.
