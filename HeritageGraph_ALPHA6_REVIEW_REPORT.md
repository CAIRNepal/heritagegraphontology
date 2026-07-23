# HeritageGraph 0.1.0-alpha.6 — independent ontology-engineering review and fixes

**Date:** 2026-07-18
**Scope:** `ontology/HeritageGraph.yaml` (authoritative LinkML source) and the
release pipeline `scripts/finalize_alpha5_artifacts.py`. All OWL/SHACL/JSON
Schema artifacts regenerated from source; **no generated file was edited by hand.**

Every issue raised in the earlier review was re-verified independently against
the source, the generated artifacts, live endpoints, and the LinkML/OWL/SKOS
specifications before any change. One issue the earlier review *missed*
(CIDOC-CRM term hijacking via `enum_uri`) was found and fixed; two claimed
issues were rejected as not objectively justified (see §9).

---

## 1. URI dereferencing

| | |
|---|---|
| Verified independently? | Yes — `curl` against `https://w3id.org/heritagegraph/`, `.../ontology`, and a term IRI: all **HTTP 404** (with and without `Accept: text/turtle`). The intended redirect targets `https://cairnepal.github.io/heritagegraphontology/` and `.../ontology.ttl` both return **HTTP 200**. |
| Severity | High (FAIR F1/A1; blocks resource-paper claims of resolvable IRIs) |
| Evidence | `curl -sIL https://w3id.org/heritagegraph/ontology` → 404; GitHub Pages targets → 200 |
| Specification reference | FAIR principles F1/A1 (Wilkinson et al. 2016); W3C *Best Practice Recipes for Publishing RDF Vocabularies* (303-redirect content negotiation) |
| Change applied | None to redirect claims — **no redirects were fabricated.** A complete w3id submission already exists in `w3id/heritagegraph/` (`.htaccess` with 303 content negotiation for Turtle / RDF/XML / N-Triples / JSON-LD / HTML, plus `README.md`). The existing `.htaccess` was reviewed and found correct (it also covers `text/n3` and `application/owl+xml`); it was left as-is. `w3id/heritagegraph/README.md` gained an explicit **“Deployment status: not yet deployed”** section with the exact activation step (PR to `perma-id/w3id.org`). |
| Justification | Everything necessary for deployment is prepared and verified against live targets; activating the namespace requires an upstream PR that only the maintainers can submit. |

**Action required by maintainers:** open the PR adding `w3id/heritagegraph/`
to <https://github.com/perma-id/w3id.org> before submission of the paper.

## 2. Labels (human-readable + language tags)

| | |
|---|---|
| Verified independently? | Yes — 216 of 379 `rdfs:label` values in the released TTL were raw element names (`AgeCriterion`, `assesses_candidate`); **0 of 379** labels and **0 of 379** `skos:definition` values carried a language tag. |
| Severity | Medium (usability/documentation quality; flagged by OOPS! P08/P22-class checks and ROBOT report) |
| Evidence | rdflib audit of `ontology/HeritageGraph.ttl` (pre-fix) |
| Specification reference | RDFS 1.1 §5.4.1 (labels are for human presentation); W3C i18n best practice / OOPS! P08 (missing annotations), widoco/FOOPS label checks |
| Change applied | New deterministic `humanize_and_tag_labels()` step in the release pipeline: labels that exactly equal the machine name are re-worded (`AgeCriterion` → `"Age Criterion"@en`, `assesses_candidate` → `"Assesses candidate"@en`, `PartiallyExtant` → `"Partially Extant"@en`, `id` → `"ID"@en`); **every** English annotation literal (`rdfs:label`, `skos:prefLabel/altLabel/definition/scopeNote/changeNote`, `dcterms:title/description`) now carries `@en`. Ontology-node proper names (`HeritageGraph`) are tagged but never re-worded. Result: 276 labels humanized, 727 literals tagged, 0 untagged labels remain. |
| Justification | The transform is derived mechanically from the single-source-of-truth LinkML element name at generation time, so it can never drift from the YAML — equivalent to hand-adding 245 redundant `title` fields, without the duplication. **No identifier or URI was renamed.** |

## 3. Naming consistency

| | |
|---|---|
| Verified independently? | Yes — computed the set of snake_case property IRIs in the release: it is **exactly** the set of `Container`/`Metadata` attribute IRIs (set difference = ∅). All 89 minted domain property IRIs are already consistently lowerCamelCase (normalized in an earlier round; see `HeritageGraph_CHANGELOG.md` item 3). |
| Severity | Low (cosmetic; confined to the serialization vessel) |
| Evidence | rdflib audit: 30 snake_case property IRIs, all owned by `Container`/`Metadata` attributes auto-minted by LinkML from attribute names |
| Specification reference | (convention, not spec) — camelCase properties / PascalCase classes per common OWL style |
| Change applied | **Labels only** were standardized (§2 humanization covers them: `ritual_events` → `"Ritual events"@en`). Attribute IRIs left untouched. |
| Justification | Per instruction, public URIs are not changed unless absolutely necessary; these IRIs are not user-facing domain vocabulary and renaming them would break existing JSON/YAML data loaders for zero semantic gain. |

## 4. Enum modeling

Three distinct problems were verified here — one of them **not** in the earlier review:

### 4a. CIDOC-CRM term hijacking (newly found, objectively wrong)

| | |
|---|---|
| Verified independently? | Yes — the released TTL asserted `crm:E55_Type a owl:Class ; rdfs:label "ArchitecturalStyle" ; owl:unionOf (aat:300004829 …)`, i.e. it **redefined the external CIDOC-CRM class E55_Type** as a closed local list of five architectural styles. Root cause: `enum_uri: crm:E55_Type` on the `ArchitecturalStyle` enum. |
| Severity | **High** (asserting axioms on an external term constrains it for every consumer; OOPS! P07 “ontology hijacking”-class defect; also produced the bogus PV IRI `crm:E55_Type#Shikhara`) |
| Evidence | `rg "E55_Type" ontology/HeritageGraph.ttl` (pre-fix); reproduced with a fresh `gen-owl` run |
| Specification reference | OOPS! catalogue (hijacking / re-defining external terms); CIDOC-CRM v7.2.1 definition of E55 Type (open class of categories, not a closed style list) |
| Change applied | **YAML:** removed `enum_uri: crm:E55_Type`; the enum now mints `heritageGraph:ArchitecturalStyle` like every other enum, and the CRM relation is retained as `broad_mappings: [crm:E55_Type]` (emitted as `skos:broadMatch`). `crm:E55_Type` now has **zero** subject triples in the release. |
| Justification | A five-value closed style vocabulary is *narrower* than E55 Type; broadMatch is the semantically correct relation. |

### 4b. Permissible values typed `owl:Class`

| | |
|---|---|
| Verified independently? | Yes — the release pipeline called `gen-owl` without `--default-permissible-value-type`, so every enum value was emitted as `owl:Class rdfs:subClassOf <Enum>`. The manuscript (`tgdk-overleaf/main.tex`) states values are “published as named individuals” — artifact contradicted the paper. |
| Severity | Medium-high (enum values are individuals, not classes; artifact/paper mismatch) |
| Evidence | `heritageGraph:ConditionType#Damaged a owl:Class` in pre-fix TTL; the sibling pipeline `scripts/regenerate_ontology_artifacts.py` already passed the flag |
| Specification reference | OWL 2 Structural Spec §8.1.4 (`ObjectOneOf` — enumeration of *individuals*); LinkML gen-owl `--default-permissible-value-type` |
| Change applied | **Pipeline:** `gen-owl` now runs with `--default-permissible-value-type owl:NamedIndividual`. Each enum is now a proper OWL enumeration class: `heritageGraph:ConditionType owl:oneOf (…#Good …#Damaged …#Ruined …#Restored)` with values typed `owl:NamedIndividual`. |
| Justification | Matches OWL 2 enumeration semantics and the documented modeling. |

### 4c. Dual OWL + SKOS publication minted two IRIs (and duplicate labels) per value

| | |
|---|---|
| Verified independently? | Yes — 51 duplicate `rdfs:label` pairs, each from one hash-IRI OWL entity (`…/ConditionType#Damaged`) plus one slash-IRI SKOS concept (`…/scheme/ConditionType/Damaged`), unlinked. |
| Severity | Medium (two unconnected IRIs for one conceptual value; ROBOT `duplicate_label`) |
| Evidence | rdflib duplicate-label audit (pre-fix) |
| Specification reference | SKOS Reference §3 (concepts are resources — nothing forbids an individual also being a `skos:Concept`); OWL 2 DL punning rules (class/individual distinctness preserved: `skos:Concept` is a class, the value is its instance) |
| Change applied | **Pipeline:** the SKOS concept now **is** the OWL individual — the same IRI is typed `owl:NamedIndividual`, `skos:Concept`, and its enum class, and placed `skos:inScheme` the enum’s concept scheme. The `scheme/<Enum>/<Value>` minting survives only as a fallback for values gen-owl omits (none currently). Concept schemes get a distinct label (`"Condition Type (concept scheme)"@en`) to clear the last duplicate-label pairs. Duplicate labels after fix: **0**. |
| Rationale for keeping both representations (documented in the script) | The OWL enumeration class supports DL reasoning over enum-ranged properties; the SKOS scheme supports vocabulary tooling, mapping (`meaning:` AAT IRIs join the scheme), and future multilingual labels. With a single IRI per value the dual view costs nothing. |

## 5. Container

| | |
|---|---|
| Verified independently? | Yes — `Container` is the LinkML `tree_root: true` class; the demonstrator ABox, the 32 CQ queries, and the SSSOM mappings never instantiate or reference it; the JSON Schema and data-loading path depend on it. |
| Severity | Low-medium (reviewer-facing clarity, not a logical defect) |
| Evidence | `rg "Container" examples/ evaluation/ examples/queries/` → only generated SHACL shape |
| Specification reference | LinkML `tree_root` semantics (serialization anchor) |
| Change applied | **Retained** (technical justification: removing it breaks JSON/YAML loadability and the JSON Schema artifact). **YAML:** added a machine-readable `design_note` annotation, which now travels into the OWL release: *“Serialization construct, not a domain class … Reasoners and domain queries should ignore it; RDF instance data does not need a Container node.”* |
| Justification | Matches the instruction: annotate clearly rather than delete without cause. |

## 6. OWL modeling (domain / range / inverse / subproperty)

| | |
|---|---|
| Verified independently? | Yes, per property. Findings: (a) the 38 object + 7 datatype properties without `rdfs:range` were **exactly** the `Container`/`Metadata` attribute properties (LinkML emits only per-class restrictions for attributes, no global range) plus `lastKnownExistenceDate`; (b) absent `rdfs:domain` on all properties is a **documented, deliberate** decision (the manuscript §Table metrics: “Domain declarations are deliberately sparse … explicit domains would produce unintended entailments”), and domain information is already carried per-class by `owl:Restriction` axioms; (c) all 16 declared inverses and every `is_a` subproperty bridge survive generation — enforced by the pipeline’s axiom-survival guard, which aborts the build on any loss. |
| Severity | Low (ranges); n/a (domains, inverses — no defect) |
| Evidence | rdflib audit; pipeline guard output |
| Specification reference | RDFS 1.1 §3.6–3.7 (domain/range are entailment axioms, not constraints — adding domains to polymorphic properties over-entails) |
| Change applied | **Pipeline:** new `apply_attribute_ranges()` asserts `rdfs:range` for attribute properties from their declared LinkML range (44 ranges added — each attribute property is used by exactly one class, so the global range is semantically exact). After the fix: object properties missing range **0/102**; datatype properties missing range **1/32** (`lastKnownExistenceDate`, whose `xsd:date` range is intentionally excluded from OWL because `xsd:date` is outside the OWL 2 datatype map — the check lives in SHACL; documented in the DL-repair step). No domains were added and no property characteristics (functional/transitive/symmetric) were invented. |
| Justification | Only semantically certain axioms added; everything else would be inventing OWL semantics. |

## 7. Unused terms

| | |
|---|---|
| Verified independently? | Yes — one property (`heritageGraph:selectionCriteriaMet` / slot `selection_criteria_met`) is declared but attached to no class. |
| Severity | Low |
| Evidence | rdflib audit: only HG property never referenced by a class restriction |
| Specification reference | OWL 2 `owl:deprecated` annotation vocabulary |
| Change applied | **None (kept, documented):** the slot carries the LinkML `deprecated:` metaslot, is emitted with `owl:deprecated true`, and was deliberately detached from `KumariSelectionEvent` in alpha.6-round DL fixes so no live axiom references a deprecated property (ROBOT `deprecated_property_reference`). It is retained for backward compatibility with pre-alpha.5 data; its replacement (`has_criterion` → `SelectionCriterion` subclasses) is documented in its description. |
| Justification | Not obsolete — it is a correctly deprecated migration shim. Deleting it would violate the deprecation contract already published. |

## 8. Release metadata

| | |
|---|---|
| Verified independently? | Yes — YAML said `0.1.0-alpha.5` while the source already contained applied “alpha.6” fixes; the pipeline hardcoded the alpha.5 citation string. |
| Severity | Low-medium (stale/self-inconsistent versioning) |
| Evidence | `version:` vs. `# DL FIX (alpha.6)` comments in the YAML; hardcoded literal in `finalize_alpha5_artifacts.py` |
| Specification reference | `owl:versionIRI` (OWL 2 §3.1), PAV/DCTerms versioning practice |
| Change applied | **YAML:** `version: 0.1.0-alpha.6`; `owl:versionIRI …/0.1.0-alpha.6`; `dcterms:modified 2026-07-18`; citation updated. **Pipeline:** `dcterms:bibliographicCitation` is now derived from `SchemaView.schema.version` instead of a hardcoded string, so it can never go stale again. `bibo:status` stays “Pre-release specification draft (alpha)” — still accurate. |

## 9. Review claims rejected (verified, no change)

1. **“Add rdfs:domain to properties.”** Rejected — the sparse-domain policy is
   an explicit, published design decision with a sound rationale (polymorphic
   properties across disjoint branches; RDFS domains entail, they don’t
   constrain). Domain information is carried per-class via restrictions and
   SHACL. Adding domains would *create* incorrect entailments.
2. **“Weak axiomatization (no functional/transitive/symmetric properties).”**
   Rejected as an objective defect — no property in the schema is demonstrably
   functional/transitive/symmetric on the evidence available, and the
   instruction forbids inventing OWL semantics. The ontology is explicitly
   positioned as SHACL-validated with OWL alignment, which is a legitimate,
   documented profile.

## 10. Known remaining gaps (documented, out of scope for objective fixes)

- **w3id activation** requires the upstream `perma-id/w3id.org` PR (§1).
- **WIDOCO HTML re-build** (`scripts/build.sh`) requires the Docker daemon,
  which was not running; `scripts/refresh_docs_metadata.py` was run instead and
  patched version/date metadata into `docs/index.html`, and the WebVOWL JSON
  was fully regenerated offline. Run `scripts/build.sh` once Docker is up for
  the complete HTML refresh.
- **`sssom.tsv` is stale** (predates alpha.5: still references
  `ArchitecturalStyleEnum#…` IRIs and maps `ReligiousTradition` from
  `crm:E55_Type`). Not touched here — regenerating it faithfully from the YAML
  mappings is a separate task; flagging to avoid shipping it as-is.
- **pyshacl workaround:** pyshacl ≤ 0.31 degrades pathologically when the
  mixed-in ontology graph contains `owl:NamedIndividual` declarations. The
  release artifact keeps the (correct) declarations; the validation gate strips
  them from its in-memory copy only (semantics unchanged — values keep their
  enum-class typing). Documented in `run_pyshacl()`.

---

## Validation results (after regeneration)

| Check | Result |
|---|---|
| LinkML SchemaView loads | ✅ 75 classes / 192 slots / 7 enums |
| Induced-slot errors | ✅ 0 |
| OWL parses (Turtle + RDF/XML) | ✅ 5,096 triples |
| SHACL parses | ✅ 10,476 triples |
| JSON Schema generates / valid JSON | ✅ |
| Axiom-survival guard (disjoints, unions, inverses, all YAML mappings incl. new enum mapping) | ✅ build passes (aborts on any loss) |
| pyshacl gate over demonstrator ABox | ✅ conforms |
| Competency questions | ✅ 32/32 return bindings |
| YAML ↔ TTL sha256 sync check | ✅ in sync (`4a6702552082…`) |
| `crm:E55_Type` subject triples | ✅ 0 (hijack removed) |
| Duplicate labels among HG terms | ✅ 0 (was 51 pairs) |
| Labels/definitions without `@en` | ✅ 0 (was 379/379) |
| HG object properties without `rdfs:range` | ✅ 0/102 (was 38/102) |

## Modified files

Source and pipeline (hand-edited):

- `ontology/HeritageGraph.yaml` — version/metadata bump; `ArchitecturalStyle`
  `enum_uri` removal + `broad_mappings`; `Container` design_note annotation
- `scripts/finalize_alpha5_artifacts.py` — NamedIndividual PV generation;
  unified OWL/SKOS enum IRIs + enum-level mapping emission + scheme label
  disambiguation; label humanization/`@en` tagging; attribute `rdfs:range`
  assertion; dynamic citation; JSON Schema generation step; pyshacl
  NamedIndividual workaround; survival-guard extensions (enum concept IRIs,
  enum mappings)
- `w3id/heritagegraph/README.md` — explicit deployment-status section

Regenerated (by the pipeline — do not edit):

- `ontology/HeritageGraph.ttl`
- `ontology/HeritageGraph.shacl.ttl`
- `ontology/HeritageGraph.schema.json`
- `ontology/review.owl`
- `docs/ontology.ttl`, `docs/ontology.owl`, `docs/ontology.nt`, `docs/ontology.jsonld`
- `docs/index.html` (metadata patch via `refresh_docs_metadata.py`)
- `docs/webvowl/data/ontology.json` (offline WebVOWL regeneration + declutter)

## Exact YAML changes

```diff
-version: 0.1.0-alpha.5
+version: 0.1.0-alpha.6
```

```diff
   ArchitecturalStyle:
     description: "A vocabulary of architectural styles for South Asian heritage, mapped to CIDOC E55 Type."
-    enum_uri: crm:E55_Type
+    # ENUM URI FIX (alpha.6): `enum_uri: crm:E55_Type` made gen-owl emit the
+    # enumeration class ON the external CIDOC-CRM IRI, redefining crm:E55_Type
+    # as a local class labelled 'ArchitecturalStyle' with a closed member list
+    # (ontology hijacking; asserting axioms on an external term constrains it
+    # for every ontology that imports CRM). The enum now mints its own IRI
+    # like every other HeritageGraph enum; the CRM relation is carried as a
+    # broad mapping (an architectural style IS a kind of E55 Type, but this
+    # closed five-value list is narrower than E55_Type itself).
+    broad_mappings:
+      - crm:E55_Type
     permissible_values:
```

```diff
 annotations:
   owl:ontologyIRI: "https://w3id.org/heritagegraph/ontology"
-  owl:versionIRI: "https://w3id.org/heritagegraph/ontology/0.1.0-alpha.5"
+  owl:versionIRI: "https://w3id.org/heritagegraph/ontology/0.1.0-alpha.6"
   ...
-  dcterms:modified: "2026-07-16"
+  dcterms:modified: "2026-07-18"
-  dcterms:bibliographicCitation: "CAIR-Nepal (2026). HeritageGraph Ontology (0.1.0-alpha.5). https://w3id.org/heritagegraph/ontology"
+  dcterms:bibliographicCitation: "CAIR-Nepal (2026). HeritageGraph Ontology (0.1.0-alpha.6). https://w3id.org/heritagegraph/ontology"
```

```diff
   Container:
     tree_root: true
     description: "Root container for cultural heritage data instances. ..."
+    # CONTAINER STATUS (alpha.6): retained in the published ontology because
+    # the LinkML tree_root is what makes JSON/YAML data files loadable and the
+    # JSON Schema/Python artifacts depend on it; it carries no domain
+    # semantics. The design_note below travels into the OWL release as an
+    # explicit machine-readable marker so consumers know to ignore it for
+    # reasoning/domain modelling.
+    annotations:
+      design_note: 'Serialization construct, not a domain class: this is the LinkML tree_root
+        that anchors JSON/YAML dataset serializations (its collection properties exist for
+        data exchange only). Reasoners and domain queries should ignore it; RDF instance
+        data does not need a Container node.'
     broad_mappings:
       - prov:Collection
```

No ontology terms, mappings, URIs, or semantic relationships were fabricated;
every added triple is either derived mechanically from the YAML source or is a
verified correction documented above.
