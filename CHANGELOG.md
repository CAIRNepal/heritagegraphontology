# Changelog

## [1.1.0] - 2026-06-18

### Added
- `heritagegraph-lux-alignment.ttl` — modular LUX (Yale Linked Art / CIDOC-CRM)
  alignment ontology. `owl:imports` the HeritageGraph core and adds formal
  `owl:equivalentClass` (12) and `owl:equivalentProperty` (18) axioms to
  CIDOC-CRM, 33 interoperability classes (Group, Set, VisualItem, Inscription,
  Title, Identifier, Name, Dimension, Acquisition, MonetaryAmount, …) rooted in
  the URIs LUX actually emits, plus the HG-internal hierarchy and object
  properties wiring those classes into the core graph. Versioned `owl:Ontology`
  metadata (1.0.0), Apache-2.0 license, authorship (Semih Yumuşak; Niraj Karki / CAIR Nepal).
- `HeritageGraph-lux.shacl.ttl` — companion SHACL module: open NodeShapes for the
  33 interoperability classes (open by design, so migrated LUX records carrying
  unenumerated CRM properties are not rejected).
- `examples/lux-murti-merged.ttl` — a LUX sculpture record expressed in the merged
  ontology, exercising Name/Identifier/VisualItem/DigitalObject/Inscription/
  Dimension/Acquisition/MonetaryAmount/Set. Validates `Conforms: True` against the
  LUX shapes.

### Fixed
- OWL 2 DL validity of the merge: 6 HeritageGraph **datatype** properties
  (`name`, `id`, `place_type`, `custodian_type`, `performed_by_group`,
  `source_citation`) were `rdfs:subPropertyOf` a CIDOC-CRM **object** property
  (P1/P2/P14/P67i) — illegal in OWL 2 DL. Downgraded to `rdfs:seeAlso`; the
  object-property equivalents (`identified_by_name`, `identified_by_identifier`,
  `carried_out_by`, `documented_in_source`) already carry the real CRM linkage.

### Validation
- Structural DL lint (rdflib): 0 datatype→object-property conflicts, 0
  unsatisfiable classes on the merged core+bridge (5,522 triples).
- HermiT/owlready2 reasoning prepared (`/tmp/hg-merged.owl`) but not run in this
  environment — no JDK present; rerun `sync_reasoner_hermit` where Java is available.

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
