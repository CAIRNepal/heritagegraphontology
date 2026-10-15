# Changelog

## [Unreleased] - v1.0.0 consistency fixes

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
