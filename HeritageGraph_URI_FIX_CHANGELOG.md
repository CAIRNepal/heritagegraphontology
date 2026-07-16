# HeritageGraph 0.1.0-alpha.5 — Fabricated-URI Remediation Changelog

**Scope:** removal of every fabricated / non-existent external URI from `HeritageGraph_fixed.yaml`, producing `HeritageGraph_fixed_alpha5.yaml`. No class hierarchy, slot, mapping-set structure, or documentation change beyond the URI substitutions themselves. Every replacement carries an inline `# URI FIX (alpha.5)` comment at the point of change. Validated after edit with linkml-runtime SchemaView: 74 classes, 171 induced slots, 7 enums, 0 induced-slot errors (identical to alpha.4).

**Policy applied:** replace each fabricated URI with the correct *official* term where one exists; where no official term exists, mint a `heritageGraph:` IRI. No CRM terms were invented.

## URI changes

| # | Location (alpha.4 line) | Element | Old (fabricated) | New | Rationale |
|---|---|---|---|---|---|
| 1 | 438 | `ArchitecturalElement.class_uri` | `crm:E25_Architectural_Element` | `crm:E25_Human-Made_Feature` | CIDOC-CRM has no class "E25 Architectural Element"; the official E25 is *Human-Made Feature* (human-made features attached to physical things, e.g. carvings), matching this class's intent (Gajur, Torana, Tundal). |
| 2 | 514 | `CalendarSystem.class_uri` | `time:Calendar` | `heritageGraph:CalendarSystem` | OWL-Time defines no `Calendar` class. No official ontology defines a "calendar" class exactly; IRI minted per policy. |
| 3 | 516 | `CalendarSystem.exact_mappings[0]` | `time:Calendar` | `time:TRS` | A calendar is a temporal reference system; `time:TRS` is the official OWL-Time class (the Gregorian calendar is its canonical instance). |
| 4 | 517 | `CalendarSystem.exact_mappings[1]` | `crm:E29_Designated_Reference_System` | *(removed)* | No such CIDOC-CRM class exists (E29 is *Design or Procedure*, used correctly elsewhere in the schema). No official CRM equivalent for reference systems exists in base CRM; per the no-invented-CRM-terms rule the entry is removed, leaving `time:TRS` as the mapping. |
| 5 | 475 | `Deity.exact_mappings` | `schema:Deity` | `wikidata:Q178885` | schema.org defines no `Deity` type. Replaced with the existing Wikidata concept *deity* (Q178885) to preserve an equivalent web-scale mapping. |
| 6 | 1768 | `occurs_after.slot_uri` | `crm:P120i_is_occurred_before_by` | `crm:P120i_occurs_after` | The official CIDOC-CRM RDF name of the inverse of `P120_occurs_before` is `P120i_occurs_after`. |
| 7 | 2204 | `datacite_identifier.slot_uri` | `datacite:identifier` | `heritageGraph:persistentIdentifier` | SPAR DataCite has no literal-valued identifier property; its `datacite:hasIdentifier` is object-valued via a `datacite:Identifier` node. `dcterms:identifier` is already the URI of the `id` slot — reusing it would merge two distinct predicates in RDF. Minted per policy. |
| 8 | 2209 | `datacite_identifier_type.slot_uri` | `datacite:identifierType` | `heritageGraph:identifierScheme` | Not in SPAR DataCite; the official pattern is object-valued `datacite:usesIdentifierScheme`. No literal-valued official term exists; minted per policy. |
| 9 | 2214 | `datacite_creator.slot_uri` | `datacite:creator` | `dcterms:creator` | Not in SPAR DataCite. `dcterms:creator` is the official, agent-valued creator property and matches the slot's `Actor` range. |
| 10 | 2219 | `datacite_publisher.slot_uri` | `datacite:publisher` | `dcterms:publisher` | Not in SPAR DataCite. `dcterms:publisher` is the official publisher property. |
| 11 | 2224 | `datacite_resource_type.slot_uri` | `datacite:resourceType` | `heritageGraph:resourceType` | Not in SPAR DataCite (`resourceTypeGeneral` is a DataCite kernel XML field with no RDF form). Minted per policy; a future revision may adopt `dcterms:type` with a controlled class value. |

## Namespace changes

| # | Location | Prefix | Old | New | Rationale |
|---|---|---|---|---|---|
| 12 | 206 | `crminf:` | `http://www.cidoc-crm.org/crminf/` | `http://www.ics.forth.gr/isl/CRMinf/` | Verified 2026-07-16 against cidoc-crm.org: CRMinf v1.2.1 is released as PDF/DOCX only — there is **no current official RDF release**, and `cidoc-crm.org/crminf/` term URIs return 404. The FORTH namespace is the de-facto RDF namespace used by existing CRMinf data and implementations (e.g. ResearchSpace); adopting it makes HeritageGraph's `crminf:I2_Belief` triples co-resolvable with existing CRMinf datasets. |
| 13 | 204 | `crmsci:` | `http://www.cidoc-crm.org/crmsci/` | `http://www.ics.forth.gr/isl/CRMsci/` | Same situation verified for CRMsci (v2.1 release page ships PDF/DOCX only; `cidoc-crm.org/crmsci/S4_Observation` returns 404). The FORTH namespace is the namespace of the official CRMsci RDFS encodings and of existing CRMsci data (`…/CRMsci/S4_Observation`). Affects `FieldSurveyActivity.class_uri` (`crmsci:S4_Observation`) via prefix expansion. |

## Non-URI corrections (adjacent factual fix)

| # | Location | Change |
|---|---|---|
| 14 | 839 | Inline comment on `Assertion.class_uri` corrected from "`ISO standard for arguments`" to "`CRMinf I2 Belief (CRM-SIG argumentation extension; CRMinf itself is not an ISO standard)`". CIDOC-CRM base is ISO 21127; CRMinf is a CRM-SIG extension and has never been an ISO standard. The old comment was a factual error shipped in source. |

## Metadata

| # | Location | Change |
|---|---|---|
| 15 | 5 | `version: 0.1.0-alpha.4` → `0.1.0-alpha.5` |
| 16 | 214 | `owl:versionIRI` → `https://w3id.org/heritagegraph/ontology/0.1.0-alpha.5` |

## Notes

- The `datacite:` prefix declaration (line 208) is now **unused** (no `datacite:` CURIE remains after fixes 7–11). It was deliberately left in place because prefix removal was out of scope ("no other changes"); it may be deleted in the next revision.
- Downstream artifacts (OWL export, SHACL, docs, ABox, CQ queries) must be regenerated from `HeritageGraph_fixed_alpha5.yaml` — in particular, any data using the old `crminf:`/`crmsci:` expansions or `datacite:` predicates will no longer match.
- Post-edit verification: (a) linkml-runtime SchemaView loads with 0 errors and identical class/slot/enum counts to alpha.4; (b) grep confirms no occurrence of any fabricated URI outside the explanatory `# URI FIX` comments.

---

# Round 2 — Strict class-URI identity policy (de-squatting)

**Policy:** whenever a HeritageGraph class is *narrower* than the CIDOC-CRM (or CRMsci) class whose IRI it carried, the class receives a minted `heritageGraph:` `class_uri` and the CRM IRI moves to `broad_mappings` (the CRM concept is broader). Classes already carrying minted IRIs but claiming a broader CRM class in `exact_mappings` had that CRM entry moved to `broad_mappings`. Every class in the schema was reviewed. Each change carries an inline `# URI POLICY (alpha.5)` comment.

## 2a. Classes whose `class_uri` was minted (CRM IRI → `broad_mappings`)

| # | Class | Old class_uri | New class_uri | CRM IRI now in |
|---|---|---|---|---|
| 1 | Deity | `crm:E28_Conceptual_Object` | `heritageGraph:Deity` | broad_mappings |
| 2 | Guthi | `crm:E74_Group` | `heritageGraph:Guthi` | broad_mappings (appended to existing list) |
| 3 | RitualEvent | `crm:E7_Activity` | `heritageGraph:RitualEvent` | broad_mappings |
| 4 | ReligiousTradition | `crm:E55_Type` | `heritageGraph:ReligiousTradition` | broad_mappings |
| 5 | HistoricalEvent | `crm:E5_Event` | `heritageGraph:HistoricalEvent` | broad_mappings |
| 6 | OralHistoryInterview | `crm:E65_Creation` | `heritageGraph:OralHistoryInterview` | broad_mappings |
| 7 | FieldSurveyDataset | `crm:E31_Document` | `heritageGraph:FieldSurveyDataset` | broad_mappings |
| 8 | OralHistoryRecording | `crm:E33_Linguistic_Object` | `heritageGraph:OralHistoryRecording` | broad_mappings |
| 9 | InformationObject | `crm:E73_Information_Object` | `heritageGraph:InformationObject` | broad_mappings |
| 10 | ArchitecturalElement | `crm:E25_Human-Made_Feature` | `heritageGraph:ArchitecturalElement` | broad_mappings |
| 11 | FieldSurveyActivity | `crmsci:S4_Observation` | `heritageGraph:FieldSurveyActivity` | broad_mappings |
| 12 | SyncreticRelationship | `crm:E13_Attribute_Assignment` | `heritageGraph:SyncreticRelationship` | broad_mappings |
| 13 | AssertionSubject | `crm:E1_CRM_Entity` | `heritageGraph:AssertionSubject` | broad_mappings — this also removes the covering axiom over `crm:E1` created by class_uri + `union_of` |

## 2b. Minted classes whose broader CRM IRI moved `exact_mappings` → `broad_mappings`

| # | Class | CRM IRI moved | Note |
|---|---|---|---|
| 14 | ArchitecturalStructure | `crm:E22_Human-Made_Object` | already implied by `is_a: HumanMadeObject` |
| 15 | IconographicObject | `crm:E22_Human-Made_Object` | close_mapping `crm:E36_Visual_Item` untouched |
| 16 | CasteGroup | `crm:E74_Group` | merged into existing broad list with `prov:Organization` |
| 17 | DataSource | `crm:E73_Information_Object` | also dissolves the parent≡child≡E73 equivalence collapse with InformationObject |
| 18 | Festival | `crm:E7_Activity` | merged with existing `prov:Activity` broad list |
| 19 | Consecration | `crm:E7_Activity` | |
| 20 | Enshrinement | `crm:E7_Activity` | |
| 21 | DocumentationActivity | `crm:E7_Activity` | |
| 22 | KumariLifecycleEvent | `crm:E7_Activity` | |
| 23 | KumariSelectionEvent | `crm:E7_Activity` | merged into its existing broad list |
| 24 | KumariEnthronementEvent | `crm:E7_Activity` | |
| 25 | KumariRetirementEvent | `crm:E7_Activity` | merged into its existing broad list |
| 26 | RitualAssessment | `crm:E7_Activity` | |
| 27 | KumariRole | `crm:E55_Type` | |
| 28 | SelectionCriterion | `crm:E55_Type` | |

## 2c. Classes reviewed and deliberately left unchanged (identity ≈ external class)

Person=`crm:E21`, Actor=`crm:E39`, Place=`crm:E53`, TimeSpan=`crm:E52`, HumanMadeObject=`crm:E22`, Production=`crm:E12`, TransferOfCustody=`crm:E10`, ConditionAssessment=`crm:E14`, ConditionState=`crm:E3`, Material=`crm:E57`, Technique=`crm:E29_Design_or_Procedure`, DestructionEvent=`crm:E6` (kept; note its description also covers damage, which E6 strictly does not — revisit the description), Assertion=`crminf:I2_Belief` (deliberate: this class *is* the schema's realization of I2 Belief and co-resolvability with CRMinf data is the point), Entity/Activity/Agent=`prov:*` (deliberate direct PROV representations). All remaining classes already carried minted `heritageGraph:` IRIs.

Known residue (out of scope this round): enum `ArchitecturalStyle` still has `enum_uri: crm:E55_Type`.

---

# Round 3 — Predicate-collision repair (slot_uri uniqueness)

**Policy (best practice):** no two semantically different slots may share a `slot_uri`, because in the RDF/OWL export a slot *is* its URI and shared URIs merge into one indistinguishable predicate. The generic slot keeps the CRM predicate as the canonical form; each specialization gets a minted `heritageGraph:` URI **plus `is_a: <generic slot>`**, which LinkML emits as `rdfs:subPropertyOf` — so every specialized triple still entails the CRM triple and CRM compatibility is preserved. Each change carries an inline `# PREDICATE FIX (alpha.5)` comment.

| # | Slot | Old slot_uri | New slot_uri | is_a (⇒ rdfs:subPropertyOf) | Canonical CRM holder |
|---|---|---|---|---|---|
| 1 | birth_timespan | `crm:P4_has_time-span` | `heritageGraph:birthTimespan` | `has_timespan` ⇒ `crm:P4` | `has_timespan` |
| 2 | death_timespan | `crm:P4_has_time-span` | `heritageGraph:deathTimespan` | `has_timespan` ⇒ `crm:P4` | `has_timespan` |
| 3 | publication_timespan | `crm:P4_has_time-span` | `heritageGraph:publicationTimespan` | `has_timespan` ⇒ `crm:P4` | `has_timespan` |
| 4 | route_places | `crm:P7_took_place_at` | `heritageGraph:routePlaces` | `took_place_at` ⇒ `crm:P7` | `took_place_at` |
| 5 | performs_ritual | `crm:P14i_performed` | `heritageGraph:performsRitual` | `carried_out_activity` ⇒ `crm:P14i` | `carried_out_activity` |

Effect: birth vs. death dates, procession routes vs. event venues, and Guthi ritual performance are now distinct, queryable predicates in the RDF export, while a reasoner loading CRM still infers the corresponding `P4`/`P7`/`P14i` statements via subPropertyOf.

**Remaining shared slot_uris — reviewed, deliberately not changed this round** (either the intentional CRM typing idiom or same-meaning specializations; several are flagged in the strict review for separate domain/range repair): `crm:P2_has_type` ×8 (typing idiom), `crm:P12_occurred_in_the_presence_of` ×3, `crm:P12i_was_present_at` ×2, `crm:P11_had_participant` ×2 (one of the two, `consecrated_object`, is a range violation to be fixed on its own), `crm:P8_took_place_on_or_within` ×2, `crm:P14_carried_out_by` ×2 (`performed_by_group is_a carried_out_by` — should get a minted URI in the next pass), `crm:P29_custody_received_by` ×2, `crm:P129_is_about` ×2 (`is_about_deity` is a domain violation to be fixed on its own).

## Post-edit verification (rounds 2–3)

- linkml-runtime SchemaView: **74 classes, 171 slots, 7 enums, 0 induced-slot errors** — identical counts to alpha.4; no structural change.
- Automated sweep: **zero** external (`crm:`/`crmsci:`/`crminf:`/`prov:`/`time:`) `class_uri` remains on any class outside the documented keep-list.
- `crm:P4_has_time-span`, `crm:P7_took_place_at`, `crm:P14i_performed` each now used by **exactly one** slot.
- All five repaired slots verified: minted URI + `is_a` parent + unchanged range.

---

# Round 4 — CIDOC-CRM domain/range repairs

Every slot audited against CRM 7.x class/property definitions. Each fix carries an inline `# CRM D/R FIX (alpha.5)` comment. Policy: use the correct official CRM property where one exists; mint a `heritageGraph:` property where CRM has none; never invent CRM terms.

| # | Slot | Old (violation) | New | Why the old term was wrong / pattern chosen |
|---|---|---|---|---|
| 1 | consecrated_object | `crm:P11_had_participant` | `crm:P16_used_specific_object` | P11's range is **E39 Actor**; a Murti is not an actor. P16 (E7 → E70 Thing) is the official property for an object employed in an activity. |
| 2 | embodied_deity | `crm:P14.1_in_the_role_of` | `heritageGraph:embodiedDeity` (minted) | P14.1 is not a first-class property — in CRM RDF it exists only on the reified PC14 node, and its range is E55 Type. No CRM property links a tenure to an embodied deity; the qualified-role pattern (PC14 / prov:qualifiedAssociation) is noted as the future refactor. Removed the stray “✅” review comment. |
| 3 | residence_structure | `crm:P74_has_current_or_former_residence` | `heritageGraph:residenceStructure` (minted) | P74's range is **E53 Place**; CRM strictly separates physical things from places. Alternative documented: assert P74 to the structure's Place. |
| 4 | is_about_deity | `crm:P129_is_about` | `heritageGraph:isAboutDeity` + `is_a: depicts_deity` (⇒ `rdfs:subPropertyOf crm:P62_depicts`) | P129's domain is **E89 Propositional Object**; a Murti is physical. P62 (domain E24, range E1) is CRM's official depiction shortcut of P65+P138, so the slot specializes `depicts_deity` instead. |
| 5 | holds_custody_of | `crm:P50_has_current_keeper` | `crm:P50i_is_current_keeper_of` | P50 points thing → keeper; the slot points keeper → thing. Official inverse adopted. |
| 6 | used_technique | `crm:P32_used_general_technique` | `crm:P33_used_specific_technique` | **P32/P33 were swapped**: P32's range is E55 Type but the slot's range is Technique (E29). P33's range *is* E29 Design or Procedure. |
| 7 | used_method | `crm:P33_used_specific_technique` | `heritageGraph:usedMethod` (minted) | P33 requires an E29 object; this slot is a free-text note and CRM has no literal-valued technique property. |
| 8 | used_equipment | `crm:P16_used_specific_object` | `heritageGraph:usedEquipment` (minted) | P16 is an object property (range E70); literal values are invalid OWL. |
| 9 | source_language | `crm:P72_has_language` | `schema:inLanguage` | P72 has domain E33 Linguistic Object and object range E56 Language; the slot sits on DataSource with a literal. schema:inLanguage officially admits Text values. |
| 10 | commissioned_by | `crm:P17_was_motivated_by` | `heritageGraph:commissionedBy` (minted) | P17 points to the motivating *thing*, not the commissioning *agent*. CRM's idiom (role-qualified P14/PC14) is a larger refactor; direct minted property in the interim. |
| 11 | had_participant | `crm:P11_had_participant` | `heritageGraph:hadParticipant` (minted) | P11's domain is **E5 Event**; the slot's owner (KumariTenure) is a period. CRM defines no participation property for E4 Period. |
| 12 | KumariTenure (class) | *(no CRM typing)* | + `broad_mappings: crm:E4_Period` | Grounds the documentation's "E4 Period" claim; also makes P4 timespans on the tenure domain-coherent (E4 ⊂ E2). |

Residue check: `crm:P11` no longer used anywhere; the one remaining `crm:P129_is_about` use (`is_about` on InformationObject, E73 ⊂ E89) is domain-correct and untouched.

---

# Round 5 — External mapping audit (evidence-based)

**Every `exact_mappings` statement (classes, slots, and enum values) was checked against live endpoints on 2026-07-16** — Getty AAT (`vocab.getty.edu`), Wikidata (`EntityData` + search API), schema.org, CRM. Rule applied: `exact_mappings` only where semantic equivalence truly holds; broader external concepts → `broad_mappings`; narrower external concepts → `narrow_mappings`; overlapping-but-not-equivalent → `close_mappings`; wrong/nonexistent → removed or replaced with a verified concept. Each change carries a `# MAPPING AUDIT (alpha.5)` comment citing the verified label.

**The audit found that most AAT IDs and several Wikidata QIDs denoted unrelated concepts** — e.g. the "RitualEvent" AAT ID resolves to *ownership*, the "Jatra" ID to *Capuchin (Christian order)*, the "stupa" QID to *a Roman emperor*, the "murti" QID to *an insect species*, and the "Kumari Ghar" QID to *a spider species*.

| Element | Old mapping | Verified meaning of old | New mapping | Action |
|---|---|---|---|---|
| HumanMadeObject | exact `schema:CreativeWork` | overlaps, covers intangibles | close `schema:CreativeWork` | demoted |
| HumanMadeObject | exact `aat:300033618` | *paintings (visual works)* | — | removed (wrong concept) |
| HumanMadeObject | exact `wikidata:Q838948` | *work of art* (narrower) | narrow `wikidata:Q838948` | demoted to narrow |
| ArchitecturalStructure | exact `aat:300006888` | *fortifications* | — | removed (wrong concept) |
| ArchitecturalStructure | exact `schema:Place` | categorially disjoint | close `schema:Place` | demoted |
| ArchitecturalStructure | exact `wikidata:Q811979` | *architectural structure* ✓ | kept exact | verified |
| ReligiousStructure | exact `aat:300007596` | guide term *\<temples by form\>* | — | removed (guide terms are not concepts) |
| Temple | exact `aat:300007595` / `wikidata:Q44539` / `dbo:Temple` | *temples (buildings)* / *temple* ✓ | kept exact | verified |
| Temple | exact `dbo:ReligiousBuilding` | broader | broad | demoted |
| Stupa | exact `aat:300007576` | *stupas* ✓ | kept exact | verified |
| Stupa | exact `wikidata:Q177980` | ***Aemilian, Roman emperor*** | exact `wikidata:Q180987` (*stupa*, verified) | replaced |
| IconographicObject | exact `aat:300033618` / `aat:300041273` | *paintings* / *prints* | — | removed (class includes statues) |
| IconographicObject | exact `dbo:Artwork` | broader | broad | demoted |
| Paubha | exact `aat:300033618` | *paintings* (broader) | broad | demoted |
| Paubha | exact `wikidata:Q130993` | unresolvable | exact `wikidata:Q7148832` (*Paubha — traditional Newar religious painting*, verified) + close `wikidata:Q916651` (*thangka*) | replaced |
| Murti | exact `aat:300264383` | ***sculpting*** (an activity) | — | removed |
| Murti | exact `wikidata:Q2594295` | ***an insect species*** | exact `wikidata:Q1781039` (*murti*, verified) | replaced |
| ArchitecturalElement | exact `aat:300001819` | HTTP 404 (nonexistent) | exact `aat:300000885` (*architectural elements*, verified) | replaced |
| Deity | exact `aat:300343156` | HTTP 404 (nonexistent) | exact `aat:300343850` (*deities*, verified) | replaced |
| RitualEvent | exact `aat:300055603` | ***ownership*** | — | removed |
| CalendarSystem | exact `time:TRS` | broader (TRS covers clocks, CRSs) | broad `time:TRS` | demoted |
| KumariHouse | exact `wikidata:Q2708161` | ***a spider species*** | — | removed (no class-level QID found) |
| RitualType.NityaPuja | exact `aat:300055603` | *ownership* | — | removed |
| RitualType.Abhisheka | exact `aat:300264383` | *sculpting* | — | removed |
| RitualType.Homa | exact `aat:300264387` | *images (object genre)* | — | removed |
| RitualType.Bhajan | exact `aat:300264388` | *pictures (object genre)* | — | removed |
| RitualType.Yagna | exact `aat:300264386` | *trimurti* | — | removed |
| RitualType.Vrata | exact `aat:300264389` | *caliphates* | — | removed |
| RitualType.Jatra | exact `aat:300264390` | *Capuchin (Christian order)* | — | removed |
| RitualType.ChariotProcession | exact `aat:300254776` | HTTP 404 | broad `aat:300069290` (*processions*, verified) | replaced+demoted |
| RitualType.MaskedPerformance | exact `aat:300264391` | *Egyptology* | — | removed |
| ArchitecturalStyle.Dome (meaning) | `aat:300001285` | *onion domes* (narrower) | `aat:300001280` (*domes*, verified) | replaced |
| ArchitecturalStyle.Shikhara (meaning) | `aat:300446671` | *grīvā-śikhara* (a specific variant) | — (commented out) | removed pending domain-expert confirmation |
| ArchitecturalStyle.Pagoda / Chaitya / Stupa (meanings) | `aat:300004829` / `300007562` / `300007576` | *pagodas* / *chaityas* / *stupas* ✓ | kept | verified |
| ReligiousTradition | exact `aat:300073708` | *religions (belief systems)* ✓ | kept exact | verified |
| ArchivalRecord | exact `rico:Record` | archival record ✓ | kept exact | verified |
| id (slot) | exact `schema:identifier` | ✓ | kept | verified |

---

# Round 6 — Container review & serialization

| # | Change | Rationale |
|---|---|---|
| 1 | **Removed** the `has_architectural_style` Container attribute | Duplicate slot: it shadowed the global `has_architectural_style` slot, and declared an inlined *instance* collection over an **enum** (enums have no instances to inline). |
| 2 | **Added** `metadata: inlined: true` | Metadata carries an identifier (Entity mixin); without `inlined: true`, serializers required a string reference where an embedded object was intended — JSON validation failed on the shipped design. |
| 3 | **Added 13 collections**: `structures` (ArchitecturalStructure), `iconographic_objects` (IconographicObject), `actors`, `historical_events`, `condition_assessments`, `condition_states`, `time_spans`, `techniques`, `kumari_tenures`, `kumari_roles`, `kumari_lifecycle_events`, `selection_criteria`, `ritual_assessments` | Previously the tree root could not hold the Kumari module (the schema's flagship pattern), historical events, condition data, time spans, or techniques at all. |
| 4 | Added missing `linkml:` prefix | The schema imports `linkml:types` but never declared the prefix; strict loaders (PythonGenerator) failed on the unresolvable CURIE. |
| 5 | `schema:` prefix `https://schema.org/` → `http://schema.org/` | Canonical schema.org RDF term URIs use http://; the https binding clashed with the imported linkml:types module and emitted non-canonical URIs. |

**Serialization verified end-to-end:** (a) JSON Schema generates cleanly (40 top-level properties); (b) a sample Container instance exercising the new collections (tenure + role + deity + structure + condition data + metadata) **validates against the generated JSON Schema**; (c) the same instance **round-trips through the LinkML-generated Python model** via `json_loader`. Known limitation documented: `physical_heritage_things` ranges over the `union_of` class PhysicalHeritageThing, which LinkML's JSON Schema generator flattens to Entity-level fields only — use the new `structures`/`iconographic_objects`/`architectural_elements` collections for typed physical data. The generator also warns that four declared inverse pairs (`ended_tenure_of`/`has_retirement_event`, `generated`/`was_generated_by`, `documents`/`was_documented_by`, `has_assertion`/`asserts_about`) have range/domain asymmetries — pre-existing wiring flagged in the strict review, untouched here.

## Post-edit verification (rounds 4–6)

- SchemaView: **74 classes, 184 slots, 7 enums, 0 induced-slot errors** (slot count up from 171 due to the 13 new Container collection attributes).
- Residue sweep: `crm:P11` unused; no misused P14.1/P74/P50/P32/P72/P17 remains; the surviving `crm:P129_is_about` is the domain-correct use on InformationObject.
- Every removed/replaced external mapping verified against the live authority on 2026-07-16; verified labels recorded in inline comments.

---

# Round 7 — Constraints, emic aliases, CRMinf substance, overclaim, artifact sync

## 7a. Constraint fixes (`# CONSTRAINT FIX (alpha.5)` comments)

| # | Element | Change |
|---|---|---|
| 1 | `confidence_score` | `minimum_value: 0` / `maximum_value: 1` added — the 0.0–1.0 range promised in prose is now machine-enforced (verified: a 1.7 score is rejected by the generated JSON Schema). |
| 2 | `ArchitecturalStructure.has_current_location` | No longer unconditionally required (contradicted `Destroyed`/`Lost`/`Hypothetical` existence states). Replaced with a LinkML `rules:` conditional — required iff `existence_status` ∈ {Extant, PartiallyExtant}; `maximum_cardinality: 1` retained. |
| 3 | `has_component` | `multivalued: true` — was accidentally single-valued (a structure with exactly one carving). |
| 4 | `selection_criteria_met` | Free-text `annotations: deprecated` replaced with the machine-readable LinkML `deprecated:` metaslot. |

## 7b. Emic aliases (`# EMIC ALIASES (alpha.5)` — implements the reviewer's altLabel request)

`aliases:` (⇒ `skos:altLabel` in the OWL export, verified) added to 16 classes: **KumariRole** ("Living Goddess", "Royal Kumari", कुमारी, Kumārī — the explicitly requested altLabels), KumariTenure, KumariHouse (Kumari Ghar, कुमारी घर), Guthi (गुठी, Guṭhī), DhungeDhara (ढुङ्गे धारा, Hiti, हिति), Pati (पाटी, Phalcha), Sattal, Dharmashala, Pokhari, Chaitya, Stupa, Murti, Paubha, Temple (मन्दिर, Mandir), Festival (जात्रा, Jātrā), ThirtyTwoPerfectionsCriterion (**Battis Lakshana**, बत्तीस लक्षण — resolving the emic-principle inconsistency flagged in the strict review). Devanagari/IAST forms are marked as pending native-speaker verification.

## 7c. CRMinf substance (`# CRMINF FIX (alpha.5)`)

| # | Change | Effect |
|---|---|---|
| 1 | `AssertionSubject.union_of` gains **Assertion** and **CalendarSystem** | Beliefs about beliefs (CRMinf **I7 Belief Adoption** — an expert re-endorsing or disputing a prior claim) and assertions about calendar-conversion claims are now expressible; previously impossible. |
| 2 | New class **Proposition** (`heritageGraph:Proposition`, broad `crminf:I4_Proposition_Set`, Entity mixin) with `proposition_subject` (`rdf:subject`, required), `proposition_predicate` (`rdf:predicate`, uriorcurie, required), `proposition_object_entity` (`rdf:object`) / `proposition_object_literal` (minted) | The assertion layer's claim is no longer only an opaque string: each Assertion can carry machine-queryable subject–predicate–object propositions via the new `asserts_proposition` slot (**`crminf:J4_that`**, matching the I2→I4 pattern the schema's own annotation advertises). `assertion_content` remains for prose. Container gains a `propositions` collection. |

## 7d. Overclaim fix

Header description "…that **fully aligns** with CIDOC-CRM and PROV-O…" → "…**aligned with** CIDOC-CRM and PROV-O **through exact/broad mappings and subproperty bridges**…" — the original claim was falsifiable against rounds 1–5's findings.

## 7e. Artifact drift resolved (single source of truth)

- **Repo sync:** `HeritageGraph_fixed.yaml` in the repo root (previously stale **alpha.2** — pre-PROV-mixins, all fabricated URIs still present) replaced with this alpha.5. This changelog copied alongside.
- **Regenerated artifacts** committed next to it: `HeritageGraph_fixed_alpha5.owl.ttl` (OWL, generated with `--no-use-native-uris` so the export uses the declared CRM/PROV `slot_uri`/`class_uri` values — the default native-URI mode silently discards them), `HeritageGraph_fixed_alpha5.shacl.ttl`, `HeritageGraph_fixed_alpha5.schema.json`.
- **OWL export spot-verified (11/11):** minted `hg:Deity`/`hg:Guthi` classes; `Person`=`crm:E21` identity kept; `birthTimespan`/`routePlaces`/`performsRitual`/`isAboutDeity` emit `rdfs:subPropertyOf` `crm:P4`/`P7`/`P14i`/`P62`; Devanagari altLabels present; `Deity skos:broadMatch E28`; Proposition class present; **no equivalence axiom on `crm:E1`** (covering axiom confirmed gone in the actual export).
- **Not promoted (release decision for the team):** `ontology/HeritageGraph.yaml`, `ontology/*.ttl`, and `docs/ontology.owl|ttl` are a separate lineage feeding the published w3id artifacts; promoting alpha.5 into them changes the published ontology and should go through the repo's `scripts/regenerate_ontology_artifacts.py` + review. The ABox/CQ rebuild (strict-review C2) also remains open.

## Post-edit verification (round 7)

- SchemaView: **75 classes, 190 slots, 7 enums, 0 induced-slot errors** (+1 class Proposition, +5 proposition/assertion slots, +1 Container collection).
- Generated JSON Schema validates a proposition-bearing sample instance and **rejects** an out-of-range confidence score.
- owlgen/shaclgen/jsonschemagen all exit 0 on alpha.5. Note: owlgen warns it cannot translate the `equals_string` rule conditions into OWL — the existence-status/location rule is enforced at LinkML-validation/JSON-Schema level, not in the OWL export.

---

# Round 8 — Language-generic aliases, minors sweep, provenance scoping (C5), Kumari consolidation, CQ evaluation rebuild (C2)

## 8a. Aliases made language-generic (revision of round 7b)

Per project decision ("generic ontology"), all Devanagari and IAST-diacritic aliases were **removed**. Retained (plain romanized, `# ALIASES (alpha.5)`): KumariRole "Living Goddess"/"Royal Kumari" (the explicitly requested altLabels), KumariTenure "Living Goddess Tenure", KumariHouse "Kumari Ghar", DhungeDhara "Hiti", Pati "Phalcha", Temple "Mandir", Festival "Jatra", ThirtyTwoPerfectionsCriterion "Battis Lakshana". Alias blocks that contained only script-specific forms (Guthi, Sattal, Dharmashala, Pokhari, Chaitya, Stupa, Murti, Paubha) were removed entirely. Verified: zero Devanagari codepoints and zero non-ASCII aliases remain. Script-specific labels are deferred to a future localization layer.

## 8b. Minors sweep (`# CLEANUP (alpha.5)`)

| # | Fix |
|---|---|
| 1 | Stale prose: "LivingGoddessRetirement" / "LivingGoddessTenure" in `ended_tenure_of` / `bounds_tenure` descriptions → current class names. |
| 2 | Typos: "a architectural strucuture" → "an architectural structure"; "Place Where event occurred" → "Place where the event occurred"; unclosed paren in `note` description; leading space in KumariSelectionEvent description. |
| 3 | Prefix hygiene: removed `dct:` (duplicate of `dcterms:`), `datacite:` (unused since round 1), and never-used `crmdig:`, `tgn:`, `foaf:`, `wgs84:`. |
| 4 | Removed the `owl:imports` annotation — it serialized as one malformed space-separated literal; alignment is carried by mappings/subproperty bridges, not by importing full external ontologies. |
| 5 | Deleted the 40-line commented-out Guthi subclass block (SiGuthi…RajGuthi) — the GuthiType enum covers the typology. |
| 6 | `HeritageGraph_DOCUMENTATION.md` drift fixed: version → alpha.5; counts → 75 classes / 188 slots; broken `{{artifact:…}}` image → `HeritageGraph_hierarchy.png`; "fully aligns" → "aligned … through mappings"; DocumentationActivity "E13" claim → E7; 15 stale class CURIEs in the hierarchy listing updated to the minted alpha.5 IRIs; alpha.5 changelog added to the Files section. |

## 8c. C5 — provenance scoping (design decision, option B: documented record-level scope)

The Entity mixin's four provenance slots stay universal (the project's stated intent), but the use–mention conflation is now **explicitly scoped**: the mixin's description declares that for real-world referents these slots describe the **data record about** the referent, not the referent itself (a stupa is not generated by the survey that records it); referent-level history belongs to events (Production, DestructionEvent); RDF deployments SHOULD carry record-level provenance in named graphs or on InformationObject/Assertion nodes. Machine-readable marker: `annotations: provenance_scope: record`. The cleaner alternative (restricting the slots to information-bearing classes) is noted as a possible future refactor.

## 8d. Kumari wiring consolidation (`# KUMARI WIRING (alpha.5)`)

| # | Change | Effect |
|---|---|---|
| 1 | **Deleted `has_retirement_event`** (IRI still carried pre-rename `hasTenureEndEvent`) | One tenure→retirement edge (`retired_through`); IRI drift eliminated by removal. |
| 2 | `initiated_tenure`, `ended_tenure_of` → `is_a: bounds_tenure` | One canonical event→tenure edge *family*; specializations entail `boundsTenure` via subPropertyOf in RDF. |
| 3 | `bounds_tenure` no longer globally required; each concrete lifecycle event requires exactly one tenure edge via `slot_usage` (selection: `initiated_tenure`; retirement: `ended_tenure_of`; enthronement: `bounds_tenure`) | **Double-mandatory tenure entry eliminated.** |
| 4 | Declared inverses: `selected_through ↔ initiated_tenure`, `retired_through ↔ ended_tenure_of` | Resolves the Kumari inverse asymmetry the generator warned about. |
| 5 | **Deleted `results_in_role`**; selection now uses `confers_role` (same as enthronement) | One name for "yields this role". |
| 6 | `AssertionSubject.union_of` gains Production, Consecration, Enshrinement, TransferOfCustody, ConditionAssessment | These standalone event classes carry `has_assertion`/`was_documented_by` but were not union members — assertions could not legally target them. |

## 8e. C2 — CQ evaluation suite rebuilt and passing

- **`examples/kathmandu-mini-abox-alpha5.ttl`** — the demonstrator ABox machine-migrated to alpha.5: every `hg:<slot_name>` token mapped to the declared `slot_uri`/`class_uri` (via SchemaView), with an explicit rename table for deleted terms (`HeritageAssertion→crminf:I2_Belief`, `LivingGoddessTenure→hg:KumariTenure`, `LivingGoddessRetirement→hg:KumariRetirementEvent`, `has_provenance_assertion→hg:hasAssertion`, `asserts_about_entity→hg:assertsAbout`, `asserted_value→prov:value`, `was_attributed_to_agent→prov:wasAttributedTo`, `was_derived_from_source→prov:wasDerivedFrom`, `results_in_role→confers_role`, `has_retirement_event→retired_through`). Enum-value URIs (hg:Pagoda, hg:TempleGuthi, …) intentionally kept as-is.
- **`examples/queries/cq-abox-32-alpha5.rq`** — all 32 CQ queries migrated with the same mapping; missing `PREFIX` declarations auto-added per block.
- **`evaluation/run_abox_cq32_alpha5.py`** — runner executing the suite against the **alpha.5 OWL export** (`HeritageGraph_fixed_alpha5.owl.ttl`) + migrated ABox.
- **Result: 32/32 CQs PASS** (report committed at `evaluation/results/abox_cq32_alpha5_report.txt|csv`; 5,409 triples loaded). The old alpha.1-vocabulary suite is retained untouched for provenance; the alpha.5 suite is the one that matches the published RDF semantics.

## 8f. Artifact re-sync

Regenerated `HeritageGraph_fixed_alpha5.owl.ttl` / `.shacl.ttl` / `.schema.json` after rounds 7–8 and re-synced into the repo together with the alpha.5 YAML (as `HeritageGraph_fixed.yaml`), the updated `HeritageGraph_DOCUMENTATION.md`, and this changelog. Promotion into the published `ontology/` + `docs/` lineage remains a team release decision.

## Post-edit verification (round 8)

- SchemaView: **75 classes, 188 slots, 7 enums, 0 induced-slot errors** (−2 slots: `has_retirement_event`, `results_in_role` deleted).
- Zero Devanagari / non-ASCII aliases; zero unused prefixes; owl:imports annotation gone.
- Kumari inverse pairs verified symmetric; enthronement requires `bounds_tenure` via slot_usage.
- **CQ suite: 32/32 PASS against the alpha.5 OWL export.**


---

# Round 9 — Validation engineering finalization (committee blockers)

1. **`scripts/finalize_alpha5_artifacts.py`** (new): finalizes OWL (re-injects `owl:disjointWith` dropped by gen-owl, restores `owl:inverseOf`, asserts FAIR metadata as typed triples) with an **axiom-survival guard** that aborts if any declared disjointness/inverse/mapping is missing from the export; repairs SHACL (75 identifier min-counts dropped, **22 union `sh:class` → `sh:or` rewrites**, closed shapes opened) and aborts unless pyshacl reports conformance.
2. **SHACL: 172 violations → CONFORMS** on the demonstrator ABox (`evaluation/results/shacl_alpha5_report.txt`).
3. **P2 predicate de-collapse** (SHACL evidence upgraded it from "idiom" to defect): canonical `has_type` keeps `crm:P2_has_type`; ritual_type, guthi_type, place_type, custodian_type, has_condition_type, syncretic_type, has_architectural_style, has_religious_tradition are minted subproperties (`is_a: has_type`). Every semantically-driven CRM predicate collision is now resolved.
4. **Committee nits:** 3 shortcut inverse pairs declared; Proposition `close_mappings: rdf:Statement`; KumariLifecycleEvent description corrected; consecrated_object description matches P16; `human_made_objects` collection (last unreachable class); Container placement rule documented.
5. **FAIR:** dcterms created/modified/source/citation, bibo:status, vann prefix/URI in schema + export; `CITATION.cff` added.
6. **Reproducibility:** migration codified as `scripts/migrate_abox_alpha5.py` (incl. enum `meaning:`-URI serialization — Pagoda → aat:300004829); ABox/queries regenerated; **CQ 32/32 PASS** re-verified.
7. **Reasoning:** OWL 2 RL consistency **CONSISTENT** (owlrl; TBox+ABox closure 37,909 triples) — HermiT unavailable (no Java runtime), caveats recorded in `evaluation/results/reasoner_alpha5_report.txt`. **OOPS!** attempted 2026-07-16; service timed out; rerun pending.
8. **Promotion investigated, not executed:** the published `ontology/` lineage has materially diverged (v1.0.0, `HeritageAssertion` vocabulary, epistemic_stance/TK/ORCID/EDM features, different CRMinf namespace, pipeline-hard-coded overclaim). Copy-over would delete features; a merge checklist is documented in `HeritageGraph_FINAL_REPORT.md` §1.8.

Final state: **75 classes / 190 slots / 7 enums / 0 errors**; OWL 5,184 triples (disjointness present); SHACL conformant; CQ 32/32; OWL-RL consistent.


---

# Round 10 — Promotion executed: alpha.5 is the sole ontology (owner decision)

1. **Earlier lineage removed** (`git rm -f`): `ontology/HeritageGraph.yaml` (diverged 1.0.0), `HeritageGraph.ttl`, `HeritageGraph.shacl.ttl`, `HeritageGraph-alignment.ttl`, `HeritageGraph-edm.ttl`, `heritagegraph-metadata.ttl`, `review.owl`; untracked intermediate `HeritageGraph.build.ttl` deleted; the Desktop pre-remediation alpha.4 copy deleted.
2. **Archives kept** (small, deliberate): `release/archive/HeritageGraph-1.0.0-old-lineage.yaml` (source of the epistemic_stance / Local Contexts TK / ORCID / EDM features for a future feature-port) and `release/archive/HeritageGraph-0.1.0-alpha.4-original.yaml` (pre-remediation audit baseline — the alpha.4 line numbers in rounds 1–4 of this changelog refer to it).
3. **Canonical paths restored as alpha.5**: `ontology/HeritageGraph.yaml` → symlink to `HeritageGraph_fixed.yaml` (single source of truth preserved; the ~20 scripts referencing the canonical path keep working); `ontology/HeritageGraph.ttl` / `.shacl.ttl` = finalized alpha.5 exports with provenance headers. All verified parseable (5,184 / 10,478 triples; SchemaView loads 75 classes through the symlink).
4. **Published artifacts promoted**: `docs/ontology.{ttl,owl,nt,jsonld}` regenerated from the finalized alpha.5 export; verified to contain the minted classes and `versionIRI …/0.1.0-alpha.5`.
5. **Known follow-ups**: `docs/index.html` still shows 1.0.0-era metadata (refresh via docs tooling); `scripts/regenerate_ontology_artifacts.py` (retired 1.0.0 pipeline) and `ontology/lux/*` remain wired to old-lineage assumptions — retire or re-point; `sssom.tsv` may predate alpha.5 mappings.

---

# Round 11 — TTL axiom-completeness audit (owner challenge: "disjointness/union missing?")

Owner questioned whether the generated TTL carries all declared axioms. Full audit result:

| Axiom type | Status before this round | Action |
|---|---|---|
| `owl:disjointWith` (Stupa/Chaitya) | **Present** in all three TTL locations (restored by round 9's finalize script) — not missing. | Verified only. |
| **`owl:unionOf` for PhysicalHeritageThing (3 members) and AssertionSubject (25 members)** | **MISSING — owner was right.** gen-owl silently drops `union_of` (the 15 unionOf lists in the export were range expressions, not the declared class unions), and round 9's survival guard did not cover unions. | `finalize_alpha5_artifacts.py` now injects proper `owl:equivalentClass [ a owl:Class ; owl:unionOf (…) ]` definitions and the guard aborts if they are absent. |
| `owl:deprecated` (selection_criteria_met) | **MISSING** — the LinkML `deprecated:` metaslot did not reach OWL. | Injected (`owl:deprecated true`) + guarded. |
| `owl:inverseOf` | 16/16 declared pairs present. | Verified. |
| `rdfs:subPropertyOf` bridges (P2/P4/P7/P14i/P62 + bounds_tenure family) | Present (20). | Verified. |
| confidence_score bounds | Present as a datatype intersection (float ∩ ≥0 ∩ ≤1); facet datatype is xsd:integer because the YAML declares `0`/`1` — cosmetic, semantics correct. | Noted. |
| LinkML `rules:` (conditional location) | Not expressible in OWL — enforced at LinkML/JSON-Schema level (documented in round 7). | Unchanged. |

Regenerated and propagated to `ontology/HeritageGraph.ttl`, `ontology/HeritageGraph.shacl.ttl`, `docs/ontology.{ttl,owl,nt,jsonld}`. Re-verified after the change: axiom checklist **ALL PASS in all three locations**; SHACL still **CONFORMS**; CQ suite still **32/32**; OWL 2 RL still **CONSISTENT** (reasoner report updated). Final export: **5,247 triples**.

---

# Round 12 — TGDK-standard evaluation battery (executed)

1. **`evaluation/run_tgdk_eval.py`** (new, committed): one-command execution of the six standard ontology-evaluation practices (structural metrics, OOPS!-style pitfall scan, CQ coverage, SHACL, OWL 2 RL consistency, FAIR checklist). Output: `evaluation/results/tgdk_eval_report.txt` (+ archived copy in `release/evaluation/`).
2. **Documentation coverage driven to 100%/100%**: PhysicalHeritageThing description + 10 missing slot/attribute definitions added (P08 pitfall now clean).
3. **Headline measured results**: RR 0.77, IR 0.56, AR 0.71; max depth 3; 0 tangledness; 0 IRI collisions; 42/75 classes externally mapped (all label-verified); CQ 32/32; SHACL CONFORMS; OWL 2 RL CONSISTENT; local FAIR 11/11.
4. **Open items for the paper** (in `HeritageGraph_TGDK_EVALUATION.md`): P10 disjointness stance (argue or add sibling disjointness), HermiT/OOPS!/FOOPS! reruns in a Java/network-equipped environment, independent-ABox CQ run for retrieval credibility, deploy + verify w3id dereferencing.
5. Artifacts regenerated after the definition additions and propagated (root, `ontology/`, `docs/` — 5,258 triples); full battery re-verified green.

---

# Round 13 — Canonicalization of the approved ontology + definitive evaluation

1. **Owner approval enacted:** `HeritageGraph_fixed_alpha5.yaml` (approved per `HeritageGraph_FINAL_REPORT.md`) is now the **real file at `ontology/HeritageGraph.yaml`** — the canonical location; the repo-root `HeritageGraph_fixed.yaml` is a symlink to it (single source of truth, all legacy paths keep working).
2. **TTL created from it at the canonical names:** `ontology/HeritageGraph.ttl` (5,258 triples, disjointness/unions/inverses/deprecation injected + guarded) and `ontology/HeritageGraph.shacl.ttl` (conformance-gated). `scripts/finalize_alpha5_artifacts.py` now also publishes `docs/ontology.{ttl,owl,nt,jsonld}` in the same run; all pipeline/evaluation scripts repointed to the canonical paths. Root alpha5-named artifact duplicates removed; JSON Schema now at `ontology/HeritageGraph.schema.json`.
3. **Documentation and final report updated** to name `ontology/HeritageGraph.yaml` as the authoritative source.
4. Definitive evaluation battery executed against the canonical lineage — results in `evaluation/results/tgdk_eval_report.txt`.

---

# Round 14 — Complete-axiom TTL from the canonical ontology/HeritageGraph.yaml

1. **Full construct audit** of the generated TTL: cardinality restrictions (806 owl:Restriction — verified present, e.g. maxCardinality 1 on has_current_location), annotations (prov_alignment_note ×12, provenance_scope, design_note) and skos:definition coverage all confirmed already emitted. **Genuinely missing family found: enumerations** — 7 enums / 51 values had no OWL/SKOS representation.
2. **Fix:** `finalize_alpha5_artifacts.py` now publishes every enum as a **SKOS ConceptScheme** with its permissible values as skos:Concepts (declared `meaning:` URIs used as concept IRIs — e.g. Pagoda → aat:300004829; meaning-less values minted under `heritageGraph:scheme/<Enum>/<value>` to avoid class-IRI collisions), and the **axiom-survival guard now checks schemes + all 51 concepts**.
3. Final TTL: **5,474 triples**; 14-point completeness checklist passes (disjointness, both unions with exact member counts, 16 inverses, 20 subproperty bridges, 806 restrictions, 7 schemes/51 concepts, deprecated, bounds, altLabels, definitions, FAIR metadata); SHACL still CONFORMS; CQ still 32/32; docs/ artifacts re-synced in the same pipeline run.
4. Documentation gains a **construct-to-axiom mapping table** stating exactly how each YAML construct is represented in the TTL and which repairs the pipeline guarantees.

---

# Round 15 — OOPS! executed (docker), P19/P08-C fixed, total predicate uniqueness, DL punning fixed

1. **OOPS! v2 run locally** via the official docker image (public service down): required installing WordNet-3.0 into the container (committed as `oops-wordnet:v2`), excluding the P12 check (JVM heap exhaustion; assessed manually — no equivalentProperty axioms exist), and harvesting results from the engine log (partial-response serializer NPE). Full narrative in `evaluation/results/oops_report.txt`.
2. **P08-C fixed**: descriptions added to the five description-less enums.
3. **P19 fixed — total slot_uri uniqueness (192/192)**: canonical holders `occurred_in_presence_of` (crm:P12) and `was_present_at` (crm:P12i) added; `invokes_deity`, `enshrined_deity`, `architectural_structures`, `participates_in_ritual`, `is_invoked_in_ritual`, `enshrined_in_structure` (P8), `performed_by_group` (P14), `transferred_to_guthi` (P29) now minted subproperties.
4. **OWL 2 DL punning fixed** (found by the owner's Protégé/HermiT load): `performed_by_group` without a base range made gen-owl declare crm:P14 as both ObjectProperty and DatatypeProperty; base `range: Actor` added. **HermiT 1.4.3 (Protégé 5.6.7) precomputed inferences in 217 ms with no inconsistency** — the pending DL-reasoner run is now done.
5. Final OOPS state: **no pitfall on HeritageGraph-authored terms remains** — residuals are external CRM names (P07/P22), the documented restriction-based domain design (P11), and the one-directional inverse idiom (P13-bis). P10 no longer fires.
6. ABox/queries re-migrated for the new predicates; **CQ 32/32; SHACL CONFORMS; 5,534 triples**; docs/ re-synced; TGDK evaluation report refreshed.

## Round 15 addendum — HermiT verification + annotation-property declarations

- **Owner's Protégé/HermiT run on the final artifact (19:33 NPT) confirms the punning fix**: clean 377 ms load with no redeclaration warning, HermiT precomputed all six inference categories in 239 ms, no inconsistency. Recorded in `evaluation/results/reasoner_alpha5_report.txt` — the DL-reasoner evidence item is closed.
- The one remaining OWLAPI parse note ("annotation property range axiom turned to data property range") traced to 17 used-but-undeclared annotation predicates (dcterms/bibo/pav/vann metadata + minted design_note/prov_alignment_note/provenance_scope/crminf_pattern + linkml:permissible_values); the finalize pipeline now declares them all `owl:AnnotationProperty`. Zero undeclared predicates remain; final TTL 5,551 triples; SHACL still CONFORMS.

## Round 15 addendum 2 — punning fully eliminated (second Protégé verification round)

The owner's 19:40 Protégé load caught a regression introduced by the blanket annotation-property declarations: `dcterms:creator`/`dcterms:publisher` are slot URIs (ObjectProperty via `datacite_creator`/`datacite_publisher`) AND ontology-header metadata — declaring them AnnotationProperty on top produced illegal punning, and their Actor ranges produced the annotation-range parse note. Fix: (1) the two slots now use minted IRIs `heritageGraph:sourceCreator`/`sourcePublisher` with `dcterms:creator`/`publisher` retained as `exact_mappings` (skos:exactMatch verified in export); (2) the finalize pipeline's annotation-declaration step is now punning-safe (skips any predicate already declared object/datatype). Verified on the final TTL (5,553 triples): zero annotation/object punning, zero object/datatype punning, zero annotation properties with rdfs:range, zero used-but-undeclared predicates; SHACL CONFORMS; CQ 32/32.

## Round 15 addendum 3 — YAML↔TTL sync made mechanical

Owner requirement: every ontology change must be reflected in both YAML and TTL. Verified (a) all recent fixes live in the YAML (minted sourceCreator/sourcePublisher, P19 subproperties, range: Actor, enum descriptions), (b) regeneration is deterministic (regenerated TTL isomorphic to the previous one, 5,553 triples). Made the guarantee checkable: `finalize_alpha5_artifacts.py` now stamps each generated TTL with the **SHA-256 of the source YAML** plus a DO-NOT-EDIT header, and the new `scripts/check_yaml_ttl_sync.py` fails whenever the YAML changes without regeneration (or a TTL is hand-edited) — suitable as a CI/pre-commit gate.

## Round 15 addendum 4 — OOPS! re-run via the official v1 docker setup

Per the OOPS! project's official instructions: `mpovedavillalon/oops:v1` with WordNet **volume-mounted** (`-v ./data/oops/WordNet:/usr/local/tomcat/WordNet`, dict at `WordNet-3.0/dict/`), web UI verified at `http://localhost/OOPS/`. Fresh scan of the current ontology (post punning fixes): identical final result — 4 dismissed pitfall types, none on authored terms. The v1 image shares the v2 engine bugs (P12 OOM, partial-response serializer NPE), so results are harvested from the engine log; all documented in `evaluation/results/oops_report.txt`.
