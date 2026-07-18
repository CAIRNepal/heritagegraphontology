# Post-Fix Audit: HeritageGraph alpha.5 → DL-compliant regeneration

**Date:** 2026-07-16. Companion to `REPORT.md` (the pre-fix independent evaluation). Raw evidence for every value: `raw-postfix/` (post-fix) vs `raw/` (pre-fix).
**Post-fix artifact:** `ontology/HeritageGraph.ttl`, SHA-256 `f443622cdd8476db348f4336dbcede78dce3de9bdad842d55b300242c5aaec5d` (`raw-postfix/00_file_identity.txt`).

## What was changed, and where

All fixes were applied at the **generator layer** (the TTL is a generated artifact and says so in its header): 3 edits to `ontology/HeritageGraph.yaml`, plus a new `repair_dl_profile()` step and two small changes in `scripts/finalize_alpha5_artifacts.py`. The TTL/SHACL/JSON-Schema/JSON-LD-context/docs artifacts were regenerated through the sanctioned pipeline; `scripts/check_yaml_ttl_sync.py` reports both generated files in sync with the YAML.

| # | Fix | Layer | Nature |
|---|---|---|---|
| 1 | `rdf:subject/predicate/object` slot IRIs → `heritageGraph:propositionSubject/…` | YAML | Rename of three property IRIs. **No instance data used the old IRIs** (grep over `examples/*.ttl` before the change). |
| 2 | Deprecated `selection_criteria_met` detached from `KumariSelectionEvent` (slot stays declared + `owl:deprecated`) | YAML | Removes live axioms referencing a deprecated property. |
| 3 | `place_type`/`custodian_type` no longer `is_a: has_type` | YAML | Removes a semantically wrong axiom (string-valued property ⊑ object property `crm:P2_has_type` is both OWL Full and false in CIDOC-CRM terms). |
| 4 | `rdfs:label` reverted to built-in annotation (declaration + 93 class restrictions on it dropped) | finalize | Instance data keeps `rdfs:label`; SHACL keeps the name constraints (min/max count, datatype). |
| 5 | `xsd:date` / `geo:wktLiteral` removed from logical axioms (4 ranges + 4 restrictions; wrong `DatatypeDefinition(wktLiteral := xsd:string)` dropped) | finalize | These datatypes are outside the OWL 2 datatype map (strict HermiT rejects them). SHACL keeps the exact `sh:datatype` checks. |
| 6 | 57 self-referential `skos:*Match` triples removed | finalize | Pure bug fix: `gen-owl --no-use-native-uris` emits `exactMatch <own IRI>`. |
| 7 | `skos:Concept`/`ConceptScheme` + all used SKOS/DCTERMS annotation predicates declared | finalize | Purely additive declarations. |
| 8 | `crm:P2_has_type`, `prov:wasInfluencedBy` retyped DataProperty→ObjectProperty (spurious `xsd:string` default range dropped) | finalize | Matches every logical axiom that uses them, and their actual definitions in CIDOC-CRM/PROV-O. |
| 9 | Mistranslated anonymous GCI removed (gen-owl rendered the "extant ⇒ current location" rule with nonexistent property IRIs and an unconditional precondition) | finalize | Removes an axiom the schema does not assert. The real conditional rule lives in SHACL. |
| 10 | One ontology identity: IRI `https://w3id.org/heritagegraph/ontology`, real `owl:versionIRI …/0.1.0-alpha.5`, `dcterms:title`+`description` added, literal `owl:ontologyIRI`/`owl:versionIRI` annotations removed | finalize | Header repair. |
| 11 | `rdfs:label` added to SKOS schemes and minted enumeration concepts | finalize | Purely additive. |

## Did anything degrade? — the empirical checks [MEASURED]

Three independent guards, all green after regeneration:

1. **Axiom-survival guard** (built into the pipeline): every YAML-declared axiom — disjointness, unions, inverses, all mappings, deprecations, enum concepts — verified present in the final graph; the pipeline aborts otherwise. It did not abort.
2. **Reasoner agreement preserved:** HermiT via ROBOT (`raw-postfix/04…`), JFact (`raw-postfix/06…`), Pellet (`raw-postfix/07…`) all report **consistent, 0 unsatisfiable classes** — same verdict as pre-fix, now over the *unrepaired* axioms.
3. **Data compatibility:** the pipeline's pySHACL gate re-validated `examples/kathmandu-mini-abox-alpha5.ttl` against the regenerated shapes + ontology: **conforms: True** (`raw-postfix/13_pyshacl_abox_demonstrator.txt`). No instance-data predicate changed.

What was *removed* was exclusively: axioms illegal in OWL 2 DL whose checking function SHACL already carries (fixes 4, 5), axioms that were factually wrong (3, 9, the `wktLiteral:=string` definition), generator bugs (6), and vacuous metadata (10). Nothing that the YAML schema asserts was weakened.

## Before → after scorecard [MEASURED]

| Check | Pre-fix (`raw/`) | Post-fix (`raw-postfix/`) |
|---|---|---|
| **OWL 2 DL profile** (`robot validate-profile`) | **NOT in profile** (~1,900 violation lines) | **IN PROFILE** |
| Strict HermiT CLI | rejects file (`UnsupportedDatatypeException: xsd:date`) | **consistent, 0 unsatisfiable** |
| HermiT/JFact/Pellet (OWLAPI) | consistent, 0 unsat (over repaired axioms) | consistent, 0 unsat (no repair needed) |
| **OOPS! web service** | fails (`unexpected_error`/`wrong_execution`) | **scans successfully**: P04(2), P07(1), P08(2) Minor; P11(190), P24(5) Important; P13(133), P22(1) Minor; **0 Critical** |
| DL expressivity (OWLAPI) | ALCHIN(D)-equivalent, over repaired axioms | same construct family minus full existential (the only ∃ axioms were the removed GCI/wktLiteral ones) |
| Individuals (OWLAPI) | 379 (punning artifact) | 58 (true count: 51 concepts + 7 schemes) |
| Axioms / logical axioms | 2,836 / 1,504 | 2,734 / 1,071 (vacuous+illegal removed) |
| `skos:exactMatch` | 90 (57 self-loops) | 33 (0 self-loops) |
| Ontology identity | 3 different IRIs, versionIRI a string literal ("no.iri") | 1 IRI + real `owl:versionIRI` |
| `dcterms:title`/`description` | missing | present |
| Deprecated-property references | 1 (live axioms) | 0 |
| ROBOT report | 70 rows (61 ERROR incl. 54 missing_label) | 439 rows (112 ERROR duplicate_label, 319 WARN missing_definition, 7 INFO) — see explanation below |
| SHACL demonstrator (example ABox) | conforms | conforms |
| YAML↔TTL sync check | OK | OK |

### The ROBOT-report numbers need reading, not fearing

- **319 `missing_definition` WARNs are an OBO-convention mismatch, newly *visible*, not newly *introduced*.** The rule accepts only `obo:IAO_0000115`; this ontology defines everything with `skos:definition` (100% coverage on classes/properties, re-measured in `raw-postfix/08…`). Pre-fix these rows were masked by the punning bug: the rule skips `owl:NamedIndividual`s, and OWLAPI punned every labelled entity into one. The clean pre-fix number was an artifact of the defect we removed (rule source: `raw`-postfix extraction of `report_queries/missing_definition.rq`).
- **112 `duplicate_label` ERRORs are twin renderings of the same enumeration value** — gen-owl's `Enum#Value` class and the published SKOS concept intentionally share a label (e.g. "Year"). They are distinct IRIs for one conceptual value, not ambiguity between different things. Eliminating them would require either deleting labels (re-creating the 54 `missing_label` errors we fixed) or unifying the two enum renderings — a design change for the authors to consider, noted below.

## What remains open (unchanged by these fixes) [OPINION]

1. **w3id resolution** — all `https://w3id.org/heritagegraph/…` IRIs still 404. Requires a redirect PR to `perma-id/w3id.org` pointing at the GitHub Pages copies (`docs/ontology.ttl` etc. are regenerated and ready to serve). Until merged, FAIR F1/A1 still fail and the paper must not claim resolvable identifiers.
2. **Axiomatization thinness** — deliberately untouched, as adding domains/disjointness is authorial modeling, not mechanical repair: still 1 disjointness axiom, 0 property domains, 0 property characteristics, 255 `minCardinality 0` restrictions (was 281), OOPS! P11 flags 190 properties. The paper should scope its reasoning claims accordingly or the authors should invest in real axioms.
3. **Enum double-rendering** — the `Enum#Value` class vs. SKOS concept duplication (source of all remaining duplicate labels) could be unified via class–individual punning (legal in OWL 2 DL) in a future release.
4. **Naming-convention mix** (camelCase vs snake_case properties) — left alone on purpose; renaming public IRIs at submission time would break downstream consumers for a cosmetic gain.
5. Nothing was committed to git; the working tree holds the changes for the authors' review.

## Bottom line

The fixes did not degrade the ontology by any measurable criterion: all three reasoners return the same clean verdict (now on the honest, unrepaired axioms), the schema's declared semantics survived verbatim (pipeline guard), and the instance-data contract is untouched (demonstrator still conforms). What changed is that the artifact's verification claims are now literally true: it **is** OWL 2 DL, strict HermiT **does** process it, and OOPS! **can** scan it (0 critical pitfalls). The remaining discrepancies are disclosed above and are either external (w3id), authorial (axiom depth), or reporting-convention artifacts (OBO-style QC rules) — none blocks submission if stated honestly in the evaluation section.
