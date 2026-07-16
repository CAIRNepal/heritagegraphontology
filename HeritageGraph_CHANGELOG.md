# HeritageGraph 0.1.0-alpha.4 — inconsistency fixes

> **HISTORICAL DOCUMENT (through 0.1.0-alpha.4).** Superseded by
> `HeritageGraph_URI_FIX_CHANGELOG.md` (rounds 1–11, 0.1.0-alpha.5), which
> corrects several statements below — in particular: deprecated stubs were
> later deleted (item 27 here; IRI-stability applies only after first
> release), `AssertableEntity` became `AssertionSubject` with a minted IRI,
> `results_in_role` (item 40) was later unified into `confers_role`, and the
> validation count on the next line was inaccurate even for alpha.4
> (measured: 74 classes / 171 induced slots). Current verified state
> (alpha.5): 75 classes / 190 slots / 7 enums — all 46 items below re-verified against the final alpha.5 on 2026-07-16 (46/46: held, strengthened, or superseded by a documented later round).

Source: LinkML schema (the .owl is its RDF/XML export). All fixes applied in the YAML.
Validated with linkml-runtime SchemaView: 75 classes, 141 slots, 7 enums, 0 induced-slot errors.
Published IRIs are never deleted — renamed/dissolved classes are retained as `deprecated` with `owl:equivalentClass`/`skos:changeNote`.

## Changes

1. §1b  schema id/name 'HeritageGrap' -> 'HeritageGraph' (typo fix)
2. §4.1 header version 1.0.0 -> 0.1.0-alpha.2 (match owl:versionIRI)
3. §1a  43 minted property IRIs snake_case -> lowerCamelCase (slot names unchanged)
4. §3a  8 classes given unique minted class_uri (were colliding on a shared CIDOC URI); CIDOC tie moved to exact_mappings
5. §3b  BuddhistMonument dissolved -> deprecated (retained IRI); new abstract ReligiousStructure inserted; Stupa/Chaitya repointed; Stupa disjointWith Chaitya; aat:300007576 moved to Stupa
6. §3c  Temple: removed legal 'Ancient Monument' clause from definition (now per-instance); schema:HinduTemple exact->close (was excluding Buddhist/syncretic temples); reparented to ReligiousStructure
7. §2b  supersedes_assertion: prov:invalidated -> prov:wasRevisionOf (invalidated is Activity->Entity; wrong for version chaining)
8. §2c  documented_by: prov:wasGeneratedBy -> heritageGraph:documentedBy (aligned prov:wasInfluencedBy); added inverse 'documents'. was_generated_by keeps prov:wasGeneratedBy (correct: InformationObject IS generated).
9. §2f  documented_in_source: prov:wasDerivedFrom -> heritageGraph:mentionedInSource (kept wasDerivedFrom only for assertion derivation)
10. §5b  removed asserted_property/asserted_value string slots (reified predicate+object as literals). Claim carried by assertion_content + CRMinf proposition pattern instead.
11. §5d/§2d  Assertion: exact_mappings [prov:Entity, schema:Claim] demoted (Belief != prov:Entity != schema:Claim); prov:Entity->related, schema:Claim->close. CRMinf I2 Belief is the identity.
12. §2e  AssertableEntity class_uri crminf:E1_Entity -> crm:E1_CRM_Entity (crminf has no E1; CRMinf classes are I1..I7)
13. §3e  AssertableEntity union: removed ArchitecturalStructure & IconographicObject (already subsumed by HumanMadeObject); kept ArchitecturalElement (standalone)
14. §6  subject_entity range PhysicalHeritageThing -> AssertableEntity (was narrower than asserts_about_entity for the same relation)
15. §6  is_about_entity range ArchitecturalStructure -> AssertableEntity (was excluding Deity/Person/etc.)
16. §4.2  removed 3 dead slots: assertion_author (dup of was_attributed_to), archival_location, source_type (both unreferenced)
17. LG  LivingGoddessRetirement -> LivingGoddessTenureEnd (renamed; old IRI deprecated, equivalentClass). New abstract LivingGoddessLifecycleEvent groups Selection+TenureEnd under RitualEvent with shared axiom bounds_tenure -> LivingGoddessTenure. LivingGoddessTenure (E4 Period) remains the bounded entity.
18. §2a  11 event/activity classes given broad_mappings: prov:Activity as an explicit PROJECT-LEVEL assertion (verified: no normative CRM<->PROV mapping exists; asserted on our classes, not globally on E7)
19. §1c  dropped '...Enum' suffix on 7 enums (ConditionTypeEnum, ExistenceStatusEnum, RitualTypeEnum, DatePrecisionEnum, SyncreticTypeEnum, ArchitecturalStyleEnum, GuthiTypeEnum) and updated all range references (implementation vocabulary leaking into semantics)
20. §4.3  removed 11 dangling enum 'meaning:' IRIs (heritageGraph:NityaPuja etc. were undefined; kept valid aat: exact_mappings)
21. §4.5/§4.4  flagged (design_note): RitualType mixes 3 orthogonal axes; processional values duplicate RitualEvent route_* slots. Left as annotation (splitting changes the data-entry contract).
22. LG->Kumari  Renamed LivingGoddess{Tenure,Selection} -> Kumari{Tenure,SelectionEvent} (+ session-only LifecycleEvent/TenureEnd -> Kumari{LifecycleEvent,RetirementEvent}); published originals kept as deprecated equivalentClass stubs. Emic-term principle.
23. Kumari  Added KumariRole (E55), KumariHouse (ReligiousStructure), KumariEnthronementEvent (3rd lifecycle event).
24. Kumari  Added explicit SelectionCriterion hierarchy (Age/Lineage/ThirtyTwoPerfections/HoroscopeCompatibility/PhysicalIntegrity) + has_criterion/confers_role slots; free-text selection_criteria_met deprecated.
25. Kumari  Fearlessness test modelled as RitualAssessment/FearlessnessAssessment (NOT a mandatory criterion) — contested practice; accounts attach as provenanced Assertions per your refinement.
26. Kumari  KumariTenure gains assumes_role/selected_through/enthroned_through/retired_through links (matches requested embodies/assumesRole/residesIn/selectedThrough/enthronedThrough/retiredThrough property set).

## Verification note (§2a)
There is NO normative CIDOC-CRM ↔ PROV-O mapping. The CRM SIG maintains CRMarchaeo/CRMgeo/CRMinf and the FRBR harmonization, not a 'CRMprov'.
An E7 Activity ≈ PROV Activity bridge is defensible only through a shared upper ontology (both are occurrents; a peer-reviewed PROV→BFO mapping equates prov:Activity with the BFO process class).
Therefore prov:Activity alignment is asserted as a HeritageGraph PROJECT-LEVEL mapping on our own event classes (broad_mappings), NOT as a global axiom on crm:E7_Activity.

## Post-review revisions (v2 → v3)

27. **Deprecated classes deleted.** BuddhistMonument, LivingGoddessTenure, LivingGoddessSelection, and LivingGoddessRetirement — previously retained as deprecated equivalentClass stubs — were removed outright. Rationale: the ontology is pre-release (0.1.0-alpha), so no published IRIs are in circulation and the IRI-stability guarantee does not yet apply. Verified no class referenced them via is_a, mixins, slot ranges, or slot_usage before deletion.

28. **Universal provenance (PROV-O).** Provenance was previously uneven — only ~13 of 71 classes carried any provenance slot, and coverage was split between the minted `heritageGraph:hasProvenanceAssertion` and `heritageGraph:documentedBy`. Introduced an abstract mixin **ProvenancedEntity** (`prov:Entity`) that bundles four pure PROV-O properties — `prov:wasDerivedFrom` (source), `prov:wasAttributedTo` (agent), `prov:generatedAtTime`, `prov:wasGeneratedBy` (documentation activity) — and mixed it into **every** class. Every instance of every class can now record provenance in native PROV-O terms. Validated: all 69 concrete classes induce the four provenance slots; 0 induced-slot errors.

29. **Agent range broadened.** `was_attributed_to` (prov:wasAttributedTo) range widened from `Person` to `Actor` (crm:E39), so responsibility can be attributed to individuals *or* Guthi/collective groups.

30. **Assertion layer grounded.** `has_assertion` is the inverse of `asserts_about`, linking an `AssertionSubject` to source-attributed, revisable `Assertion` instances (`crminf:I2_Belief`).

## PROV-first naming and modelling revision

31. Removed the local `ProvenancedEntity` mixin. Domain classes now align semantically with `prov:Entity`, `prov:Activity`, or `prov:Agent`, preventing activities and agents from being classified as entities.
32. Renamed the earlier heritage-specific assertion class to `Assertion` and `has_provenance_assertion` to `has_assertion`; provenance belongs to the assertion, not its subject.
33. Reused PROV names directly in LinkML: `was_derived_from`, `was_attributed_to`, `was_generated_by`, `generated_information_objects`, `generated_assertions`, and `was_associated_with`.
34. Normalized documentation and lifecycle vocabulary: `documented_by`, `initiates_tenure`, `ends_tenure`, and `bounds_tenure`.
35. Renamed quality properties to `confidence`, `quality_note`, and `reconciliation_state`.
36. Renamed `ThirtyTwoPerfectionsCriterion` to the emic `BattisLakshanaCriterion`; selection and enthronement now both use `confers_role`.

## Supplied alpha.3 replacement

The workspace schema was subsequently replaced verbatim with the supplied `heritagegraph_schema_fixed.yaml` (`0.1.0-alpha.3`). This replacement supersedes changes 31–36 where they conflict with the supplied file.

37. Added direct LinkML starting-point mixins `Entity`, `Activity`, and `Agent`, mapped to the corresponding PROV-O class URIs.
38. Added generic PROV activity and delegation slots: `used`, `generated`, `started_at_time`, `ended_at_time`, and `acted_on_behalf_of`.
39. Introduced the unified `AssertionSubject`, `asserts_about`, and `is_about` pattern for entities and events.
40. Restored the supplied property names `was_documented_by`, `confidence_score`, `data_quality_note`, `reconciliation_status`, `initiated_tenure`, `ended_tenure_of`, and `results_in_role`, plus `ThirtyTwoPerfectionsCriterion`.
41. Renamed the supplied `Heritage` + `Assertion` class name to `Assertion` throughout the schema and artifacts, while retaining its `crminf:I2_Belief` identity and `Entity` mixin.

## PROV-O conformance audit

42. Removed the global `Agent is_a Entity` axiom. PROV-O permits the same individual to be both, but does not declare every Agent a subclass of Entity.
43. Added the missing starting-point relation `was_informed_by` (`prov:wasInformedBy`) to `Activity`.
44. Added `was_influenced_by` (`prov:wasInfluencedBy`) to all three PROV mixins and made `was_documented_by` its specialization.
45. Added `prov:Person` and `prov:Organization` mappings to `Person`, `Guthi`, and `CasteGroup`.
46. Added `Entity` provenance coverage to `Container` and `Metadata`; all insertable classes now inherit `Entity`, `Activity`, or `Agent`.
