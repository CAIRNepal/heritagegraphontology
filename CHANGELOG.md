# Changelog

## [Unreleased]

### Planned for 1.1.0 (branch `fix/ontology-v1.1.0`; not yet released)

**Breaking changes and migration rules** (data valid under 1.0.x that 1.1.0 rejects or reads differently):
- Place coordinates move from geo:asWKT to crm:P168_place_is_defined_by (same WKT literal).
- Data giving one structure two values of a single-valued enumeration slot is now inconsistent.
- The holder of a Kumari tenure is given with `hg:tenureHolder`, not `hg:hadParticipant`
  (rewrite `?t hg:hadParticipant ?p` on a `hg:KumariTenure` to `?t hg:tenureHolder ?p`).
- An endowment that sustained a tenure now sustains the tenure's office
  (`hg:sustains ?tenure` becomes `hg:sustains ?office`, where `?tenure hg:tenureOffice ?office`).
- The ArchitecturalStyle values Stupa and Chaitya are deprecated, replaced by the classes
  `hg:Stupa` and `hg:Chaitya`.
- A syncretic relationship is cited with `hg:mentionedInSource`, not `prov:wasDerivedFrom`.

**Added**
- The generic tenure pattern: `hg:Tenure`, `hg:Office`, `hg:RitualOffice`, `hg:TenureEvent`, with
  `hg:tenureHolder`, `hg:tenureOffice`, `hg:tenureOpenedBy` and `hg:tenureClosedBy`.
- `hg:StructureType` and `hg:structureType` (generic typing in place of new structure classes);
  `hg:StateHeritageAuthority`.
- Reuse of crm:P13 destroyed (required on a destruction event) and crm:P17 was motivated by;
  ExistenceStatus `Reconstructed`.
- dcterms:accessRights, and its subproperty `hg:accessProtocol` with the AccessProtocol values.
- An optional CRM-PROV bridge module; an SSSOM mapping set; GOVERNANCE.md and a term-request template.

**Changed**
- The core states no axiom about a term of another vocabulary unless that vocabulary states it.
- HeritageGraph classes are stated subclasses of the CIDOC-CRM class every instance belongs to.
  Disjoint kinds are stated with `owl:AllDisjointClasses`.
- Max cardinality 1 is kept on a reused CRM property only where CRM's own quantification allows it.
- Free text accepts language-tagged literals, with at most one value per language.
- JSON Schema: date-times use the xsd:dateTime lexical form (offset optional). Abstract references
  are resolved, and multivalued text accepts a single string.
- Mappings: corrected SKOS strengths (Temple, Deity, IconographicObject, documentedBy).
- LUX module: corrected the mappings, and the minted terms are marked `rdfs:isDefinedBy` the module.
- Enumerations are subclasses of crm:E55_Type and their values are `owl:AllDifferent`, so two
  values of a single-valued status (Destroyed and Extant) are inconsistent rather than merged.
- The official CIDOC-CRM `owl:inverseOf` axioms are copied for reused inverse pairs.
  `hg:invokesDeity` and `hg:isInvokedInRitual` are inverses, and `hg:succeeds` is irreflexive
  and asymmetric.
- Properties without `rdfs:domain` carry `schema:domainIncludes` (an annotation) for the classes
  that use them. Class context stays in restrictions and SHACL, so reusing a property elsewhere
  does not retype its subject.
- `hg:EndowmentEvent` is a subclass of crm:E8_Acquisition. Its donor and recipient are
  subproperties of crm:P23 / crm:P22.
- Place geometry uses crm:P168 place is defined by (a GeoSPARQL WKT literal), not geo:asWKT,
  whose domain is geo:Geometry.
- Related mappings: confidenceScore to crminf:J5, recordedDate to crm:P1, startPlace / endPlace
  to crm:P27 / P26, managedByGuthi to crm:P49 (each with the reason it is not a subproperty).
- The normative source route is stated: `hg:mentionedInSource` for descriptions;
  `prov:wasDerivedFrom` with `prov:wasAttributedTo` for beliefs; `hg:sourceCitation`,
  `hg:sourceCreator` and `hg:sourceUrl` for a source's own data. The demonstrator uses it, links
  to Wikidata with skos:exactMatch / closeMatch (not owl:sameAs), and gives each belief a
  CRMinf proposition (J4).

**Deprecated** (kept, marked `owl:deprecated` with `dcterms:isReplacedBy` where there is a replacement)
- The 1.0.x container terms, and the ArchitecturalStyle values Stupa and Chaitya.

**Evaluation**
- `make reproduce` regenerates every artefact from a clean checkout and compares it with the
  committed copy. It also runs all release gates, the mutation analysis and the metric reports, and
  writes the paper's numbers.
- The reasoning gates pin each downloaded vocabulary by sha256.

### Changed (documentation generated with OntoReview)
- The documentation site (GitHub Pages) is generated with OntoReview 1.0.1 (`ontoreview build`, configured
  by `ontoreview.toml`) instead of WIDOCO: term pages, class graph, a quality report (HermiT consistency,
  ROBOT, OOPS!, OntoCheck, IRI checks, cross-domain interoperability) and a changelog against the
  previous release (from `owl:priorVersion`). The abstract, introduction, description and references are
  kept as Markdown in `docs-src/`.
- `scripts/build.sh` still publishes the immutable release copies (`docs/releases/<version>/`), the
  enumeration-value pages and the JSON-LD context; OntoReview's self-hosting files (Docker, nginx, Pages
  workflow) are left out. CI installs OntoReview in its own environment.
- Removed the WIDOCO-specific `Dockerfile`, `scripts/refresh_docs_metadata.py` and
  `scripts/declutter_webvowl.py`; `make webvowl` is now `make serve`.

## [1.0.1] - 2026-10-20

### Added
- Release identifiers: the ontology header carries `bibo:doi` with the Zenodo concept DOI
  (10.5281/zenodo.23435676, valid across versions), `dcterms:issued` (2026-10-17, first release) and
  `owl:priorVersion` <https://cair-nepal.org/heritagegraph/ontology/1.0.0>; version IRI
  `…/ontology/1.0.1`, `owl:versionInfo` 1.0.1. README has the concept-DOI badge; CITATION.cff is
  version 1.0.1 with the concept DOI and lists the v1.0.0 version DOI (10.5281/zenodo.23435677).
- The HeritageGraph–LUX migration repository is kept in `heritagegraph-lux-migration/` (imported unchanged
  from CAIRNepal/heritagegraph-lux-migration@6772240, then synced to v1.0.0). Its
  `alignment/heritagegraph-lux-alignment.ttl` is the single LUX mapping: the duplicate in `ontology/lux/` is
  removed and every check and report reads the folder's file. LUX-facing CRMsci targets use the Linked Art
  context namespace (`http://www.ics.forth.gr/isl/CRMsci/`), as do `generate_lux_eval.py` and the mapping
  audit's Linked Art verification.
- New gate `reasoning_extras.py lux-conservativity` (make check, CI): probe instances of every class/property
  pair the LUX module maps, classified with the module and CIDOC-CRM 7.1.3 (+ CRMinf, CRMsci), must not be
  typed against CRM's disjointness (C1: E2 Temporal Entity / E77 Persistent Item, stated in the E2 scope note;
  C2: E18 Physical Thing / E28 Conceptual Object, from the scope notes) or with a core class that core +
  CIDOC-CRM alone do not entail (C3, conservativity). A negative control re-adding
  `documentedBy ⊑ crm:P94i_was_created_by` must be caught.

### Changed
- Repairs in the module: seven property mappings weakened to `skos:closeMatch` (`documentedBy`,
  `managedByGuthi`, `isAboutDeity`, `birthTimespan`, `deathTimespan`, `publicationTimespan`,
  `hasDataCustodian`); `mentionedInSource ≡ crm:P67i_is_referred_to_by` → `rdfs:subPropertyOf` (the
  equivalence made everything that refers to something a DataSource); `hg:Activity ⊑ hg:HistoricalEvent`
  and `Metadata ⊑ hg:InformationObject` removed (new subsumptions between core classes).

### Fixed
- Quality findings from an OntoReview 1.0.0 run (`ontoreview evaluate`): the style values are labelled
  "Pagoda style", "Stupa style", … (they shared "stupa"/"chaitya" with the `Stupa`/`Chaitya` classes, a ROBOT
  duplicate-label error); enum-valued properties carry distinct labels from their slot titles ("has ritual
  type", "has guthi type", …, "has calendar system", "has metadata"); each SKOS concept scheme has one English
  label; the deprecated `selectionCriteriaMet` is labelled "obsolete selection criteria met" and points to
  `hasCriterion` (`dcterms:isReplacedBy`); the schema's editorial annotation properties have labels and
  definitions; the LinkML schema IRI used by `skos:inScheme` is declared.
- CI: the build toolchain is pinned (`requirements-build.txt`: LinkML 1.9.6, rdflib 7.6.0, owlrl 7.1.4,
  pySHACL 0.31.0, …). Unpinned installs pulled LinkML 1.12, whose SHACL generator emits different shapes
  for `uriorcurie` slots, so the regenerate step failed its own SHACL self-check and every later step
  (checks, documentation, Pages deploy) was skipped.
- Documentation and header metadata at release level: `bibo:status` "Published" (was the hard-coded
  "Pre-release specification draft (alpha)"); `dcterms:creator` lists the five authors (CAIR-Nepal stays
  publisher); `dcterms:bibliographicCitation` names the authors and the concept DOI; the WIDOCO page is
  titled with the version instead of "Release: <created date>"; the authored sections cite CIDOC-CRM 7.1.3
  (not 7.2.1), add CRMsci, drop the unsupported EDM alignment claim, give 11 external vocabularies, and
  point to the LUX alignment in `heritagegraph-lux-migration/`.
- `KumariRetirementEvent`'s `carried_out_by` (`crm:P14_carried_out_by`) range relaxed from `crm:E21_Person`
  to `crm:E39_Actor`. `performedByGroup` is a subproperty of `crm:P14_carried_out_by`, so the Person-only
  restriction made any Guthi or caste group performing a retirement a `crm:E21_Person`.

## [1.0.0] - 2026-10-17

Archived on Zenodo: version DOI 10.5281/zenodo.23435677 (tag v1.0.0).

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

## [1.0.0 pre-release draft] - 2026-06-05

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
