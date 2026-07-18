# Independent Reviewer Evaluation of HeritageGraph.ttl

**Reviewer stance:** independent evaluation in the style of a TGDK (Transactions on Graph Data and Knowledge) resource-paper review.
**Evaluated artifact:** `ontology/HeritageGraph.ttl` only (plus its declared imports — of which there are none, see §2.2). The existing `evaluation/` folder was **not** read, referenced, or cross-checked.
**Date of evaluation:** 2026-07-16.

**Evidence policy.** Every number in this report was produced by a command or reasoner actually executed over the file on this date. Each table cites the raw output file (under `evaluation-independent/raw/`) and the command or script (under `evaluation-independent/scripts/`) that produced it. Values that could not be computed are marked **not computed** with the reason. Sections labeled **[MEASURED]** contain tool outputs only; sections labeled **[OPINION]** are reviewer judgment.

---

## 1. Artifact identity and evaluation environment [MEASURED]

| Item | Value | Evidence |
|---|---|---|
| File | `ontology/HeritageGraph.ttl` | — |
| SHA-256 | `ae26535c20f0bffea6b2acadaf39d8f5cdcc7fa5a8f45b4447ec331deab61721` | `raw/00_file_identity.txt` (`shasum -a 256`) |
| Size / lines | 218,909 bytes / 4,910 lines | `raw/00_file_identity.txt`; `wc -l` |
| Last modified | 2026-07-16 19:48:28 | `raw/00_file_identity.txt` (`stat`) |
| Provenance comment | "GENERATED from HeritageGraph.yaml by scripts/finalize_alpha5_artifacts.py on 2026-07-16" | file header, lines 1–3 |

Tooling (all runs local; JRE and ROBOT downloaded to a session scratchpad, no system modification):

| Tool | Version | Used for |
|---|---|---|
| rdflib | 7.5.0 | parsing, SPARQL-level counts, conversions |
| ROBOT | 1.9.8 (OWLAPI 4.5.29) | `measure`, `validate-profile`, `reason`, `report`, `convert` |
| HermiT | 1.4.5.456 (embedded in ROBOT) | consistency / satisfiability |
| HermiT CLI | bundled with owlready2 0.50 (strict CLI build) | independent consistency attempt |
| JFact | 4.0.4 (embedded in ROBOT) | cross-check reasoning |
| Pellet | 2.3.1 (via owlready2 0.50) | cross-check reasoning, unsatisfiable-class enumeration |
| pySHACL | 0.31.0 | SHACL validation |
| Temurin JRE | 21.0.11 (ROBOT), 25.0.3 (Pellet jars require class-file 69) | JVM |

Version evidence: `robot --version` in setup transcript; jar manifests read from `robot.jar` (`unzip -p … pom.properties`); `pellet-2.3.1.jar` filename in owlready2 distribution.

---

## 2. Parsing, ontology header, imports [MEASURED]

Command: `venv/bin/python3 evaluation-independent/scripts/01_parse_and_header.py` → `raw/01_parse_and_header.txt`.

- **Syntax:** parses cleanly as Turtle with rdflib 7.5.0. ROBOT/OWLAPI also loads it (`syntax: Turtle`, `raw/02_robot_measure_extended.tsv` line 189).
- **Triples:** 5,553.
- **`owl:Ontology` declarations:** 1, with subject IRI `https://w3id.org/heritagegraph/schema.owl.ttl`.

### 2.1 Header annotations present

`dcterms:license <https://creativecommons.org/licenses/by/4.0/>`, `dcterms:created "2025-11-23"`, `dcterms:modified "2026-07-16"`, `dcterms:creator`/`dcterms:publisher "CAIR-Nepal"`, `dcterms:source <https://github.com/CAIRNepal/heritagegraphontology>`, `dcterms:bibliographicCitation`, `pav:version "0.1.0-alpha.5"`, `bibo:status "Pre-release specification draft (alpha)"`, `vann:preferredNamespacePrefix "heritageGraph"`, `vann:preferredNamespaceUri "https://w3id.org/heritagegraph/"`, `rdfs:label "HeritageGraph"`, `skos:definition` (scope statement). Full list: `raw/01_parse_and_header.txt`.

### 2.2 Header defects found

- **`owl:imports`: 0.** The file is self-contained; external CIDOC-CRM/PROV/CRMinf terms are used by IRI without importing their ontologies. (All reasoning below is therefore over this file's axioms alone.)
- **`owl:versionIRI` and `owl:ontologyIRI` are string literals, not IRIs** (`raw/01b_versioniri_nodetype.txt`: `rdflib.term.Literal(...)` for both). Consequently OWLAPI reports `ontology_version_iri = no.iri` (`raw/02…tsv` line 166). `owl:ontologyIRI` is additionally not a term of the OWL vocabulary at all (in RDF, the ontology IRI is the subject of `rdf:type owl:Ontology`); both usages are flagged as reserved-vocabulary violations (`raw/03_robot_validate_profile_DL.txt`).
- **Ontology IRI mismatch:** the RDF subject is `…/schema.owl.ttl` while the annotation claims `https://w3id.org/heritagegraph/ontology` and the citation text says the same. Three distinct identifiers for one artifact.
- Per ROBOT report: `missing_ontology_title` and `missing_ontology_description` (no `dcterms:title` / `dcterms:description`; the file uses `rdfs:label`/`skos:definition` instead) — `raw/11_robot_report.tsv`.

---

## 3. Structural metrics [MEASURED]

Primary source: `robot measure --metrics extended` → `raw/02_robot_measure_extended.tsv` (console: `raw/02_robot_measure_console.txt`). Secondary source (declaration-based counts): `scripts/08_structure_annotations_ontoqa.py` → `raw/08_structure_annotations_ontoqa.txt`.

### 3.1 Entity counts

| Metric | OWLAPI signature (ROBOT) | Declared via `rdf:type` (rdflib) |
|---|---|---|
| Classes | 136 | 133 (`owl:Class`) |
| Object properties | 152 | 147 |
| Data properties | 46 | 45 |
| Annotation properties | 31 | 17 |
| Individuals | 379 | 58 typed URI individuals (51 `skos:Concept`, 7 `skos:ConceptScheme`); 0 `owl:NamedIndividual` |
| Datatypes | 9 (7 built-in, 2 non-built-in) | — |
| Total signature entities | 753 | — |

The two columns differ because OWLAPI includes referenced-but-undeclared entities (e.g., `skos:Concept`, `skos:ConceptScheme`, `geo:wktLiteral` are used but never declared — `raw/12_local_pitfall_scan.txt`, "untyped classes: 3") and because illegal punning (§4.2) causes OWLAPI to materialize property IRIs additionally as individuals — which is where 379 "individuals" come from despite only 58 typed URI subjects existing in the RDF.

### 3.2 Axiom counts (ROBOT, OWLAPI axiom model)

| Metric | Value |
|---|---|
| Total axioms | 2,836 |
| Logical axioms | 1,504 |
| TBox / RBox / ABox | 1,086 / 35 / 383 |
| Declaration | 343 |
| SubClassOf | 928 |
| EquivalentClasses | 9 |
| DisjointClasses | 1 |
| SubObjectPropertyOf / SubDataPropertyOf | 26 / 1 |
| InverseObjectProperties | 8 |
| ObjectPropertyRange / DataPropertyRange | 110 / 37 |
| ClassAssertion | 58 |
| DataPropertyAssertion | 325 |
| AnnotationAssertion | 989 |
| DatatypeDefinition | 1 |
| Rules (SWRL) | 0 |

Class-expression usage (same file): `ObjectAllValuesFrom` 211, `ObjectMinCardinality` 213, `ObjectMaxCardinality` 90, `DataAllValuesFrom` 99, `DataMinCardinality` 97, `DataMaxCardinality` 94, `ObjectUnionOf` 17, `ObjectIntersectionOf` 5, `ObjectSomeValuesFrom` **1**, `DataSomeValuesFrom` **1**.

Additionally measured (`raw/15_mincardinality_zero.txt`, `grep -c`): of 310 `owl:minCardinality` occurrences, **281 are `owl:minCardinality 0`** (29 are `1`). A `min 0` restriction is satisfied by every individual, i.e., logically vacuous.

### 3.3 Class hierarchy (named classes, asserted `rdfs:subClassOf`)

Source: `scripts/08_structure_annotations_ontoqa.py` → `raw/08_structure_annotations_ontoqa.txt`. Definition used: depth = number of nodes on the longest asserted subclass path between named classes (blank-node restriction superclasses excluded).

| Metric | Value |
|---|---|
| Named-to-named `rdfs:subClassOf` edges | 123 (out of 928 `rdfs:subClassOf` triples; the rest have restriction superclasses) |
| Hierarchy roots | 10 (`prov:Activity`, `prov:Agent`, `prov:Entity`, `crm:E55_Type`, and 6 local type-classes: `ConditionType`, `DatePrecision`, `ExistenceStatus`, `GuthiType`, `RitualType`, `SyncreticType`) |
| Maximum depth | 5 |
| Leaf classes / mean leaf depth | 108 / 2.556 |
| Multiple inheritance (tangledness) | 0 classes with >1 named parent |
| Declared classes outside the named hierarchy | 0 |
| Cycles | none detected |

### 3.4 Annotation completeness

Source: `raw/08_structure_annotations_ontoqa.txt`; cross-checked by `robot report` (`raw/11_robot_report.tsv`).

| Entity type | n | `rdfs:label` | `skos:definition` or `rdfs:comment` |
|---|---|---|---|
| Classes | 133 | 133 (100.0%) | 133 (100.0%) |
| Object properties | 147 | 147 (100.0%) | 147 (100.0%) |
| Data properties | 45 | 45 (100.0%) | 45 (100.0%) |
| Annotation properties | 17 | 0 (0.0%) | 0 (0.0%) |

ROBOT report counterpoint: 54 `missing_label` ERRORs — all on the SKOS individuals under `…/scheme/…` (enumeration values), which carry no `rdfs:label`; plus 4 `duplicate_label` ERRORs (`Stupa` and `Chaitya` labels shared between `heritageGraph:` classes and the `aat:` entities they map to). No language tags were observed on the sampled labels (all plain `xsd:string`; see any label in the file, e.g. lines 750–765 quoted in `raw/` transcripts) — multilingual coverage is effectively monolingual English.

---

## 4. Logical quality [MEASURED]

### 4.1 Consistency and class satisfiability — reasoner-reported

| Run | Tool + version | Result | Evidence |
|---|---|---|---|
| 1 | HermiT 1.4.5.456 via `robot reason --reasoner hermit` | **Consistent; 0 unsatisfiable classes; 0 unsatisfiable object properties** (ROBOT fails the command otherwise; verbose log shows the checks executing). Completed in ~1 s. | `raw/04_robot_reason_hermit_console.txt`, `raw/04b_robot_reason_hermit_verbose.txt` |
| 2 | JFact 4.0.4 via `robot reason --reasoner jfact` | **Consistent; 0 unsatisfiable classes** (exit 0) | `raw/06_robot_reason_jfact_console.txt` |
| 3 | Pellet 2.3.1 via owlready2 `sync_reasoner_pellet` | **Consistent; `UNSATISFIABLE_CLASS_COUNT: 0`** (explicit enumeration of classes equivalent to `owl:Nothing`) | `raw/07_pellet_owlready2.txt`, `scripts/05_hermit_owlready2.py` |
| 4 | HermiT CLI (strict build bundled with owlready2 0.50) | **Refused to process the ontology**: `UnsupportedDatatypeException: The datatype 'http://www.w3.org/2001/XMLSchema#date' is not part of the OWL 2 datatype map` | `raw/05_hermit_owlready2.txt` |

Caveats attached to the passing runs, verbatim from the tool logs (`raw/04b…`):
- ROBOT: `Reference violations found: 63 - reasoning may be incomplete` (dangling references to undeclared `skos:Concept`/`skos:ConceptScheme`, references to the deprecated property `selectionCriteriaMet`, and a dangling `has_current_location` in an orphan axiom).
- OWLAPI parse-time repair: `Annotation property range axiom turned to data property range after parsing`.
- JFact: `A known datatype for geo:wktLiteral cannot be found; literal will be replaced with rdfs:Literal` and `unsupported operation 'OWLDatatypeDefinitionAxiom', axiom ignored`.

**Measured bottom line:** three OWLAPI-embedded reasoners report the ontology consistent with no unsatisfiable classes, but every one of those runs operated on an OWLAPI-repaired/coerced version of the axioms (necessarily, because the file is not in OWL 2 DL — §4.2), and one strict HermiT build rejects the file outright over `xsd:date`.

### 4.2 OWL 2 profile — reasoner/validator-reported, not asserted

Command: `robot validate-profile --profile DL` → `raw/03_robot_validate_profile_DL.txt` (1,902 lines); summary counts from `robot measure` (`raw/02…tsv` lines 167–181):

| Profile | In profile? |
|---|---|
| OWL 2 (Full) | **true** |
| **OWL 2 DL** | **false** |
| OWL 2 EL / QL / RL | false / false / false |

Violation counts (OWLAPI categories):

| Violation | Count |
|---|---|
| UseOfUndeclaredAnnotationProperty | 921 |
| IllegalPunning | 451 |
| UseOfReservedVocabularyForDataPropertyIRI | 425 |
| UseOfUndeclaredClass | 58 |
| UseOfUndeclaredObjectProperty | 23 |
| UseOfReservedVocabularyForObjectPropertyIRI | 10 |
| UseOfUndeclaredDatatype | 6 |
| UseOfReservedVocabularyForIndividualIRI | 4 |
| UseOfReservedVocabularyForAnnotationPropertyIRI | 2 |
| UseOfUndeclaredDataProperty | 1 |

Root causes located in the source (grep + inspection):
- `rdfs:label a owl:DatatypeProperty` at [HeritageGraph.ttl:4898](../ontology/HeritageGraph.ttl#L4898) (the LinkML `name` slot mapped onto `rdfs:label`). Every `rdfs:label` annotation in the file thereby becomes a `DataPropertyAssertion` on a punned individual — the dominant source of the 451 punnings, 425 reserved-vocabulary data-property uses, and the inflated OWLAPI individual count (379 vs 58, §3.1).
- `rdf:object a owl:ObjectProperty`, `rdf:predicate a owl:DatatypeProperty`, `rdf:subject a owl:ObjectProperty` at [HeritageGraph.ttl:1708-1720](../ontology/HeritageGraph.ttl#L1708-L1720) — RDF reserved vocabulary redeclared as OWL properties (reification modeling of `Proposition`).
- `skos:definition`, `skos:inScheme`, `skos:exactMatch` etc. used as annotations without `owl:AnnotationProperty` declarations (921 counts); `skos:Concept`, `skos:ConceptScheme`, `geo:wktLiteral` used but undeclared (`raw/12_local_pitfall_scan.txt`).
- Literal-valued `owl:ontologyIRI`/`owl:versionIRI` (§2.2).
- One orphan blank-node class axiom (subject is a blank node with `owl:intersectionOf` + `rdfs:subClassOf`) at [HeritageGraph.ttl:4905](../ontology/HeritageGraph.ttl#L4905), which surfaces as the dangling `has_current_location` reference violation in the reasoner log.

### 4.3 DL expressivity — computed

OWLAPI-computed (ROBOT `measure`, `raw/02…tsv` lines 84–93, 120): construct set = {CONCEPT_COMPLEX_NEGATION (C), CONCEPT_INTERSECTION, CONCEPT_UNION (U), FULL_EXISTENTIAL (E), N (number restrictions), ROLE_HIERARCHY (H), ROLE_INVERSE (I), ROLE_DOMAIN_RANGE, UNIVERSAL_RESTRICTION, D}; OWLAPI's raw expressivity string: `RRESTRCUCINTUNIVRESTREHIN(D)`.

Derived conventional name (derivation, not an additional measurement): intersection + universal restriction + full existential + complex negation = **ALC**; adding role Hierarchy (H), Inverses (I), Number restrictions (N), and Datatypes (D) as reported above yields **ALCHIN(D)** (equivalently written ALCUEHIN(D) before absorbing U/E into C; naming convention per Baader et al., *The Description Logic Handbook*, 2003, §2.4). Note the complex negation arises from the single `DisjointClasses` axiom; no `owl:complementOf` occurs in the file. This expressivity is computed over the OWLAPI-repaired axiom set, since the raw file is OWL Full (§4.2).

---

## 5. Automated pitfall scan [MEASURED]

### 5.1 OOPS! web service — attempted, failed on this file

Three submissions to `https://oops.linkeddata.es/rest` (RDF/XML converted by rdflib, escaped; RDF/XML converted by ROBOT/OWLAPI, escaped; the latter wrapped in CDATA) all returned HTTP 200 with error payloads `unexpected_error` / `wrong_execution` — `raw/09_oops_response.xml`, `raw/09_oops_console.txt`. A control request with a 2-class minimal ontology **succeeded** and returned pitfall P04, proving the service was operational and the failure is specific to this file (plausibly its OWL Full constructs or size; the service does not say). Scanning by URL is impossible because the ontology's IRIs do not resolve (§6.2). **Official OOPS! results: not computed** for this reason; raw evidence of all attempts preserved.

### 5.2 ROBOT report (SPARQL QC suite)

Command: `robot report` → `raw/11_robot_report.tsv` (71 lines incl. header), console `raw/11_robot_report_console.txt`. Total: **70 violations — 61 ERROR, 2 WARN, 7 INFO**:

| Level | Rule | Count | Note |
|---|---|---|---|
| ERROR | missing_label | 54 | all SKOS enumeration individuals under `…/scheme/…` |
| ERROR | duplicate_label | 4 | `Stupa`, `Chaitya` shared with mapped `aat:` entities |
| ERROR | missing_ontology_title | 1 | no `dcterms:title` |
| ERROR | missing_ontology_description | 1 | no `dcterms:description` |
| ERROR | deprecated_property_reference | 1 | deprecated `selectionCriteriaMet` still used in 2 restrictions + a range axiom |
| WARN | missing_obsolete_label / equivalent_pair | 1 + 1 | |
| INFO | missing_superclass | 7 | |

### 5.3 Local OOPS-catalogue-inspired scan

Script: `scripts/12_local_pitfall_scan.py` → `raw/12_local_pitfall_scan.txt`. These re-implement mechanically computable pitfalls from the OOPS! catalogue (Poveda-Villalón et al., *OOPS! (OntOlogy Pitfall Scanner!)*, IJSWIS 10(2), 2014); they approximate the catalogue definitions, not the OOPS! implementation.

| Pitfall (OOPS! id) | Finding |
|---|---|
| P07 conjunction-in-name | 0 candidates |
| P10 missing disjointness | **1** `owl:disjointWith` in the whole file (`Stupa ⊥ Chaitya`, line 760); 0 `owl:AllDisjointClasses` — for 133 classes |
| P11 missing domain/range | **192/192 properties lack `rdfs:domain`**; 45/192 lack `rdfs:range` (109/147 object and 38/45 data properties have ranges) |
| P13 undeclared inverses | 16/147 object properties participate in `owl:inverseOf` |
| P19 multiple domain/range | 0 |
| P22 mixed naming conventions | properties: 86 camelCase, 30 snake_case, 15 lowercase; classes: 65 PascalCase, 46 other (the `…/scheme/…` IRIs) |
| P24 recursive-definition candidates | 6 (classes with `allValuesFrom` self, e.g. `RitualEvent` sub-events — see §8 opinion; not necessarily errors) |
| P25 self-inverse | 0 |
| P34 untyped classes | 3 (`skos:Concept`, `skos:ConceptScheme`, `geo:wktLiteral`) |
| P38 no ontology declaration | not triggered (declared) |
| P41 no license | not triggered (CC BY 4.0 present) |

Property characteristics (also `raw/08…txt`): 0 functional, 0 inverse-functional, 0 transitive, 0 symmetric properties.

Additional mechanical finding (`raw/13b…`, `raw/14…`): of 90 `skos:exactMatch` triples, **57 are self-referential** (`X skos:exactMatch X`, e.g. `heritageGraph:Sattal → heritageGraph:Sattal`), and 16 further ones map external CRM/PROV classes to internal classes; only 17 point at genuinely external vocabulary (6 wikidata, 5 aat, 2 dcterms, 2 dbo, 1 ric, 1 schema).

---

## 6. SHACL validation and FAIR/metadata [MEASURED]

### 6.1 SHACL

A sibling shapes file exists: `ontology/HeritageGraph.shacl.ttl` (10,486 triples, 75 `sh:NodeShape`, 0 standalone `sh:PropertyShape`). pySHACL 0.31.0 run with the ontology graph as data graph, `inference='none'`:

- **Conforms: True** — `raw/13_pyshacl_ontology_vs_shapes.txt`.
- **However, the conformance is vacuous:** the 75 `sh:targetClass` values have **0 instances** in the ontology graph (total focus nodes = 0, `raw/13b_shacl_vacuity_and_selfmatch.txt`). The shapes target instance data; no instance data ships inside `HeritageGraph.ttl`. SHACL validation of actual heritage data: **not computed** — no instance dataset is part of the evaluated artifact.

### 6.2 FAIR-relevant measurements (from the file + live IRI resolution)

Positive, in-file:
- License (CC BY 4.0), version (`pav:version` + dated `dcterms:created/modified`), attribution (`dcterms:creator/publisher`), citation (`dcterms:bibliographicCitation`), namespace prefix registration hints (`vann:*`), source repository link (`dcterms:source` → GitHub) — `raw/01_parse_and_header.txt`.
- Vocabulary reuse in the signature: CIDOC-CRM (crm:, 29 broadMatch targets + subclassing), PROV-O (12 broadMatch targets + 3 hierarchy roots), CRMinf/CRMsci, SKOS, Getty AAT, Wikidata, GeoSPARQL, OWL-Time, DCTERMS — namespace axiom counts in `raw/02…tsv` lines 126–161; mapping breakdown in `raw/14_mapping_targets.txt`. 27 `rdfs:subPropertyOf` bridges (`raw/08…txt`).

Negative, live-measured on 2026-07-16 (`curl -sIL`, `raw/10_w3id_resolution.txt`):

| IRI | HTTP status |
|---|---|
| `https://w3id.org/heritagegraph/` (declared namespace) | **404** |
| `https://w3id.org/heritagegraph/ontology` (annotated ontology IRI) | **404** |
| `https://w3id.org/heritagegraph/schema.owl.ttl` (actual ontology IRI) | **404** |
| `https://w3id.org/heritagegraph/ontology/0.1.0-alpha.5` (annotated version IRI) | **404** |

None of the artifact's identifiers dereference (content negotiation could not even be tested). FOOPS!/automated FAIR scoring: **not computed** — such services fetch the ontology by IRI, and every declared IRI returns 404.

---

## 7. Ontology-quality metrics with cited definitions [MEASURED]

Script: `scripts/08_structure_annotations_ontoqa.py` → `raw/08_structure_annotations_ontoqa.txt`. Definitions from Tartir, Arpinar, Moore, Sheth & Aleman-Meza, *OntoQA: Metric-Based Ontology Quality Analysis* (IEEE ICDM Workshop KADASH, 2005); tangledness from Gangemi, Catenacci, Ciaramita & Lehmann, *A theoretical framework for ontology evaluation and validation* (SWAP, 2005). Inputs: C = 133 declared classes, P = 147 declared object properties, ATT = 45 declared data properties, H = 123 named-to-named subclass edges.

| Metric | Definition | Value |
|---|---|---|
| Relationship Richness RR | P / (P + H) | 147/270 = **0.5444** |
| Inheritance Richness IR | H / C | 123/133 = **0.9248** |
| Attribute Richness AR | ATT / C | 45/133 = **0.3383** |
| Class Richness CR | classes with ≥1 instance / C | 0/133 = **0.0000** (the only typed individuals are SKOS concepts, not instances of ontology classes) |
| Tangledness | classes with >1 named parent | **0** |
| Annotation coverage | see §3.4 | 100% classes/properties; 0% for the 54 SKOS individuals (labels) |

Interpretation caveat [MEASURED→context]: CR = 0 is expected for a schema-only release; it is reported because the file does embed 58 SKOS individuals as value sets, so "no ABox" would be inaccurate.

---

## 8. Reviewer judgment [OPINION]

Everything in this section is my assessment as a reviewer; the facts it rests on are cited to §§2–7.

**Strengths.**
1. Documentation discipline is excellent for an alpha: 100% label + definition coverage on classes and properties (§3.4) is rare and commendable.
2. The reuse strategy (CIDOC-CRM, PROV-O, CRMinf, AAT, Wikidata anchoring; subproperty bridges instead of hard imports) is a reasonable, defensible design for a LinkML-generated artifact, and the mapping surface is substantial (§6.2).
3. Consistency is corroborated by three independent reasoners, with unsatisfiable-class enumeration explicitly empty (§4.1) — within the limits of the DL-repair caveat below.
4. The hierarchy is clean: no cycles, no accidental multiple inheritance, no orphan classes (§3.3).

**Major concerns (would block acceptance as-is).**
1. **The ontology is OWL Full, not OWL 2 DL** (§4.2, `owl2_dl=false`, ~1,900 violations). Any paper claim of "verified with HermiT/OOPS" is undermined: strict HermiT refuses the file (`xsd:date`, §4.1 run 4), the OOPS! service itself chokes on it (§5.1), and the passing reasoner runs are over OWLAPI's silently repaired axioms. The root causes are few and mechanical — the `rdfs:label`-as-DatatypeProperty and `rdf:subject/predicate/object` redeclarations, undeclared SKOS terms, literal version IRI — and all fixable in the LinkML-to-OWL generation step.
2. **Nothing dereferences.** All four declared identifiers 404 (§6.2). For a resource paper, F1/A1 of FAIR fail outright today, and the three-way identifier mismatch (§2.2) should be resolved to one ontology IRI plus a proper `owl:versionIRI`.
3. **The axiomatization is thinner than the axiom counts suggest.** 281 of 310 min-cardinality restrictions are vacuous `min 0` (§3.2); there is exactly 1 disjointness axiom for 133 classes, 0 property domains, 0 property characteristics, and only 2 existential restrictions against 310 universal ones (§5.3, §3.2). Universal-only modeling constrains but almost never *infers*; combined with CR = 0 this means the "ritual-spatial-temporal reasoning" promised in the scope annotation is not yet demonstrable from this file. The consistency result should accordingly be read as weak evidence: with so few negative axioms, inconsistency was nearly impossible a priori.
4. **The mapping layer contains a generation bug:** 57 of 90 `skos:exactMatch` triples are self-loops (§5.3). Any reported count of "external alignments" based on raw exactMatch numbers would overstate reality by ~3×; the genuinely external exactMatch count is 17.

**Minor concerns.**
5. The 54 SKOS enumeration individuals lack labels; 4 duplicate labels with AAT targets; deprecated `selectionCriteriaMet` still referenced by live axioms (§5.2).
6. Mixed property naming (camelCase vs snake_case, §5.3 P22) — cosmetic but visible to every consumer.
7. SHACL shapes ship alongside but validate nothing in this artifact (§6.1); the paper should either include a validated instance dataset or scope the SHACL claim to future data.
8. The 6 "recursive definition" hits (P24) look like legitimate part-whole modeling (`RitualEvent` sub-events, agent delegation), not errors — I do not count them against the ontology, but OOPS! would flag them, so pre-empting with a comment would help.
9. `geo:wktLiteral owl:equivalentClass xsd:string` (a `DatatypeDefinition` in OWLAPI terms) is semantically wrong (WKT literals are not plain strings) and is already being ignored or coerced by reasoners (§4.1 JFact log).

**Overall (opinion).** As a schema artifact the resource is well-documented, coherently structured, and honestly versioned as alpha. As the subject of a journal evaluation section, the measured evidence supports claims about documentation coverage, hierarchy quality, mapping breadth, and reasoner-checked consistency *with the DL-repair caveat stated*; it does not currently support claims of OWL 2 DL compliance, FAIR-resolvable identifiers, OOPS!-verified pitfall-freeness, or demonstrated reasoning capability. Fixing concerns 1, 2, and 4 is mechanical and would materially change the evaluation; I would recommend major revision rather than rejection.

---

## Appendix A. Raw-evidence index

| File (`evaluation-independent/raw/`) | Producing command |
|---|---|
| `00_file_identity.txt` | `shasum -a 256 ontology/HeritageGraph.ttl; stat -f …` |
| `01_parse_and_header.txt` | `scripts/01_parse_and_header.py` (rdflib parse, header, imports) |
| `01b_versioniri_nodetype.txt` | inline rdflib: node types of `owl:*IRI` values |
| `02_robot_measure_extended.tsv` + `_console.txt` | `robot measure --metrics extended` |
| `03_robot_validate_profile_DL.txt` + `_console.txt` | `robot validate-profile --profile DL` |
| `04_robot_reason_hermit_console.txt`, `04b_…_verbose.txt` | `robot reason --reasoner hermit` (2nd run with `-vv`) |
| `05_hermit_owlready2.txt` | `scripts/05_hermit_owlready2.py` (strict HermiT CLI attempt) |
| `06_robot_reason_jfact_console.txt` | `robot reason --reasoner jfact` |
| `07_pellet_owlready2.txt` | script 05 variant with `sync_reasoner_pellet` (Java 25) |
| `08_structure_annotations_ontoqa.txt` | `scripts/08_structure_annotations_ontoqa.py` |
| `09_oops_response.xml`, `09_oops_console.txt` | POSTs to `https://oops.linkeddata.es/rest` (3 attempts + control) |
| `10_w3id_resolution.txt` | `curl -sIL` on the four declared IRIs |
| `11_robot_report.tsv` + `_console.txt` | `robot report` |
| `12_local_pitfall_scan.txt` | `scripts/12_local_pitfall_scan.py` |
| `13_pyshacl_ontology_vs_shapes.txt` | pySHACL validate (shapes = `HeritageGraph.shacl.ttl`) |
| `13b_shacl_vacuity_and_selfmatch.txt` | inline rdflib: focus-node count, self-exactMatch |
| `14_mapping_targets.txt`, `14b_internal_exactmatch.txt` | inline rdflib: mapping-triple breakdowns |
| `15_mincardinality_zero.txt` | `grep -c "owl:minCardinality …"` |

## Appendix B. Values explicitly *not computed*

| Value | Reason |
|---|---|
| Official OOPS! pitfall list | service returns `unexpected_error`/`wrong_execution` for this file (3 attempts, control succeeded); IRIs 404 so URL mode impossible |
| FOOPS!/automated FAIR score | scorers dereference the ontology IRI; all declared IRIs return 404 |
| SHACL validation of instance data | no instance dataset inside the evaluated artifact; all 75 shape targets have 0 focus nodes in it |
| Metrics over the imports closure | `owl:imports` count is 0 — closure equals the file |
