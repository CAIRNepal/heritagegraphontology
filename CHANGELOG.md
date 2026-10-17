# Changelog

## [Unreleased] - v1.0.0 consistency fixes

### Changed (schema pass)
- `ArchitecturalStyle` values Pagoda, Dome, Chaitya, Stupa have their own IRIs
  (`…/ArchitecturalStyle#Pagoda`, …). Their AAT concepts (building types / an architectural element)
  had been the values' IRIs, which typed Getty terms as `ArchitecturalStyle` and made
  `aat:300007576` both the `Stupa` class's `skos:exactMatch` target and a style value. They are now
  linked by `skos:closeMatch` (Pagoda, Chaitya, Stupa) and `skos:relatedMatch` (Dome).
- `RitualEvent` declares `took_place_at` (`crm:P7_took_place_at`), which CQ11 and the demonstrator use.
- `ArchitecturalStructure` declares `managed_by_guthi`, which CQ19 and the demonstrator use.
- `RitualEvent` declares `had_participant`, which CQ30 and the demonstrator use for the Kumari in a
  procession (a participant, not the performer: `crm:P14_carried_out_by` stays with the performing group).
- LUX module: `hadParticipant owl:equivalentProperty crm:P11_had_participant` replaced by `skos:closeMatch`.
  P11's domain is `crm:E5_Event`, so the equivalence typed every `KumariTenure` (min-1 participant) as an
  event once merged with CIDOC-CRM, contrary to its deliberate `crm:E4_Period` broad match.
- New gate `reasoning_extras.py tenure-not-event` (make check, CI): core + LUX + CIDOC-CRM + CRMinf + CRMsci
  + the demonstrator must not infer any `KumariTenure` to be `crm:E5_Event`; a negative control re-adding
  the equivalence must be caught.
- SHACL negative tests: 11 (added sh:maxCount, sh:nodeKind, sh:or); each test now passes only if the report
  contains a violation of the component it targets.
- `mapping_audit.py` also audits `owl:equivalentClass` / `owl:equivalentProperty` mappings.
- `Enshrinement` declares `took_place_at` (CQ7); `ReligiousStructure` declares `has_religious_tradition`
  (CQ23: shared or contested sacred sites).
- New gate `evaluation/check_cq_class_properties.py` (make check, CI): every `?x a C ; p ?y` pattern in the
  CQ queries must use a property the SHACL shapes declare for C or a superclass, so no CQ relies on the
  shapes being open; a negative control must be caught.

### Changed (no axioms on external terms; LUX mapping from the companion repository)
- The core no longer asserts logical axioms whose subject is an external term (257 removed):
  global `rdfs:range`/`rdfs:domain` on CIDOC-CRM/PROV-O properties (incl. `crm:P46_is_composed_of`
  / `crm:P46i_forms_part_of` → ArchitecturalElement/ArchitecturalStructure), cardinality and value
  restrictions on reused classes (`crm:E21_Person`, PROV-O classes, `crminf:I2_Belief`, …),
  and `crm:E6_Destruction ⊑ HistoricalEvent`. The constraints remain as restrictions on
  HeritageGraph classes and in SHACL. Kept, with justification: 12 `rdfs:subClassOf` axioms
  between named external classes (`crm:E21_Person ⊑ crm:E39_Actor`, restated from CIDOC-CRM,
  and the CRM→PROV-O alignment of the reused classes) and the `prov:generated` /
  `prov:wasGeneratedBy` `owl:inverseOf` pair, which PROV-O itself asserts.
- `AssertionSubject` is a covering axiom (`⊑ union`) instead of `≡ union`, which made the reused
  CRM/CRMinf classes subclasses of a HeritageGraph class.
- LUX alignment module rebuilt from the updated mapping in CAIRNepal/heritagegraph-lux-migration
  (alignment/heritagegraph-lux-alignment.ttl), migrated to v1.0.0 core terms: no equivalence to
  external classes (`Deity ≡ crm:E28_Conceptual_Object` removed; `HistoricalEvent`, `Activity`,
  `Concept` now `⊑`), no axioms on external terms, no enumeration under `Concept`, CalendarSystem's
  mapping to the non-existent `crm:E29_Designated_Reference_System` removed.
- New gate `reasoning_extras.py no-external-superclass` (make check, CI): core + LUX module +
  CIDOC-CRM 7.1.3 (+ CRMinf, CRMsci) must not entail an HG superclass for any external class or
  an extra HG type for any enumeration individual.
- `mapping_audit.py` also audits the LUX module, checks every CRM/CRMinf/CRMsci IRI used anywhere
  against the official RDFS, verifies CRMdig/Linked Art targets against the Linked Art context,
  retries Getty AAT, accepts manual verdicts (`mapping_manual_verification.csv`), and exits non-zero
  on any failure.
- Every enumeration value has an HTML anchor (`docs/enum/<Enum>.html`, `scripts/gen_enum_pages.py`);
  nginx routes enumeration IRIs there so `…/ConditionType#Damaged` lands on the value. IRIs are
  served over https (http redirects to https).
- `reconcile_store.py` writes enumeration IRIs, `xsd:decimal` scores, `xsd:dateTime` dates, property
  IRIs for `propositionPredicate`, and a declarations graph.
- Deleted `interop_fixes.py`, `postprocess_shacl.py`, `HeritageGraph_fixed.yaml`.

### Changed (namespace and alignment)
- Namespace moved from the former w3id.org namespace to `https://cair-nepal.org/heritagegraph/`
  (ontology IRI `…/ontology`, version IRI `…/ontology/1.0.0`), set once in the LinkML source;
  `finalize_alpha5_artifacts.py` now derives the namespace and ontology IRI from the YAML.
  Example data uses `https://cair-nepal.org/heritagegraph/example/`.
- `w3id/` replaced by `deploy/nginx/`: content negotiation for the ontology, version, term, and
  concept-scheme IRIs, plus `deploy/nginx/check_conneg.py` (`make conneg`). Version IRIs serve
  the immutable copy written by `scripts/publish_release.py` to `docs/releases/<version>/`.
- CRMinf and CRMsci use the official namespaces of their RDFS releases
  (`http://www.cidoc-crm.org/extensions/crminf/`, `…/extensions/crmsci/`); the merged
  classification (`reasoning_extras.py merged-import`) now checks that it loads every
  CRMinf/CRMsci/CRM/PROV-O term the ontology uses, and includes CRMsci v2.0.
- LUX alignment module migrated to v1.0.0 core terms (camelCase minted properties; no axioms on
  external CIDOC-CRM/CRMinf terms; external terms declared for OWL 2 DL) and re-included in
  `check_combined_dl.py` and `check_declared_terms.py`. `generate_lux_eval.py` decides coverage
  locally against core + module and has an `--offline` mode.
- Removed the 16 `skos:exactMatch` mappings from CRM/PROV/CRMinf classes to undeclared
  HeritageGraph "native" IRIs (`heritageGraph:Person`, …) that gen-owl emitted.
- `reasoning_extras.py entailments` prints the asserted `rdfs:subClassOf` count and the inferred
  named-class subsumptions (excluding `owl:Thing`).
- Deleted the stale `scripts/regenerate_ontology_artifacts.py`.

### Fixed
- `confidenceScore` range: LinkML's `float ∩ integer[>=0] ∩ integer[<=1]` was an empty
  datatype, making every ABox with a score inconsistent under HermiT. The slot is now
  `decimal`, and the release pipeline collapses faceted intersections into one datatype
  restriction (`xsd:decimal[>= 0.0, <= 1.0]`). Example scores are `xsd:decimal`.
- Enumeration slots (`hasConditionType`, `guthiType`, `ritualType`, `syncreticType`,
  `existenceStatus`, `datePrecision`, `hasArchitecturalStyle`): SHACL `sh:in` now lists
  the enumeration individuals' IRIs instead of string literals, and all instance data
  uses those IRIs, so ontology + data no longer puns the object properties (OWL 2 DL).
- Ritual precedence uses `crm:P183_ends_before_the_start_of` /
  `crm:P183i_starts_after_the_end_of` (CIDOC-CRM v7.1.3), replacing the deprecated
  "occurs before" pair.
- `date_earliest`, `date_latest`, `last_known_existence_date` are `xsd:dateTime`
  (`xsd:date` is outside the OWL 2 datatype map); example dates follow.
- Examples type agents as `crm:E21_Person`; `propositionPredicate` values are
  `xsd:anyURI` literals as declared; `dcterms:date` is declared as an annotation property.
- CRMinf/CRMsci prefix declarations (JSON-LD context, README, evaluation namespace tables)
  match the FORTH IRIs the ontology uses; evaluation fixtures use v1.0.0 camelCase terms.
- `cq_sparql.md` is generated from the v1.0.0 CQ queries (`scripts/gen_cq_tbox_doc.py`).

### Added
- `evaluation/check_combined_dl.py`: ontology + each example ABox, parsed into one graph,
  must pass `robot validate-profile --profile DL` and HermiT (`make check`, CI).
- `evaluation/check_declared_terms.py`: every `hg:` term used in examples, queries, and
  evaluation code must be declared in the ontology (`make check`, CI).

### Changed
- `make artefacts` and CI regenerate through `scripts/finalize_alpha5_artifacts.py` (the
  pipeline that produces the released artefacts), which now also syncs `ontology/review.owl`.

## [1.0.0] - 2026-06-05

### Added
- Full OWL `rdfs:subClassOf` axioms for all external `class_uri` mappings (CRM, CRMinf, CRMsci, PROV, OWL-Time).
- Named `owl:unionOf` for `PhysicalHeritageThing`, `HeritageEvent`, and `AssertableEntity`.
- SKOS `ConceptScheme` publication for all controlled enumerations.
- `HeritageGraph-alignment.ttl` alignment module (CRM/PROV/FOAF/Wikidata bridges).
- `HeritageGraph-edm.ttl` Europeana Data Model projection profile.
- `heritagegraph-metadata.ttl` VoID dataset description.
- `examples/abox-conflicting-assertions.ttl` demonstrating multi-vocal assertions.
- `owl:versionIRI` and Dublin Core ontology metadata.
- Local Contexts label slot, ORCID identifier slot, and enum/class definitions completed.
- Expanded `owl:imports` (CRM, CRMinf, PROV, OWL-Time, GeoSPARQL, EDM).

### Changed
- `documented_in_source` aligned to `prov:wasInfluencedBy` (distinct from assertion `wasDerivedFrom`).
- Manuscript metrics reconciled with released TTL counts.
- Regeneration pipeline centralises all release post-processing.

### Fixed
- Manuscript–artefact metric mismatch (class/property counts).
- Missing `skos:definition` on six classes.
- Stale `docs/ontology.ttl` synchronised from release artefact.
