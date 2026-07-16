# HeritageGraph — Ontology Documentation

**Version:** 0.1.0-alpha.5  ·  **License:** CC-BY-4.0  ·  **Base IRI:** `https://w3id.org/heritagegraph/`

> An event-centric LinkML schema for representing cultural heritage information, aligned with CIDOC-CRM and PROV-O through exact/broad mappings and subproperty bridges, enabling provenance tracking and ritual-spatial-temporal reasoning.

HeritageGraph is an **event-centric** LinkML schema for cultural-heritage information in the Kathmandu Valley tradition. The **authoritative source is `ontology/HeritageGraph.yaml`** — the 0.1.0-alpha.5 schema approved per `HeritageGraph_FINAL_REPORT.md` (`HeritageGraph_fixed_alpha5.yaml` is the same file under its working name; the repo-root `HeritageGraph_fixed.yaml` is a symlink to it). `ontology/HeritageGraph.ttl` (OWL) and `ontology/HeritageGraph.shacl.ttl` are generated from it by `scripts/finalize_alpha5_artifacts.py`, which also publishes `docs/ontology.{ttl,owl,nt,jsonld}`. This document is the curated guide; per-class/per-slot reference pages are generated separately under `docs/`.

**At a glance:** 75 classes · 190 slots (incl. container collections) · 7 enumerations. Every insertable class inherits a PROV-O category. This document reflects the 0.1.0-alpha.5 remediation; every URI, mapping, wiring, and constraint change is itemized in `HeritageGraph_URI_FIX_CHANGELOG.md`.

## Generated OWL — construct-to-axiom mapping (completeness guaranteed)

`ontology/HeritageGraph.ttl` (5,474 triples) is produced by `scripts/finalize_alpha5_artifacts.py`, which repairs the known LinkML gen-owl omissions and **aborts the build if any declared axiom is missing** (axiom-survival guard). Every YAML construct and its OWL representation:

| YAML construct | OWL representation in the TTL | Count |
|---|---|---|
| `is_a` / mixins | `rdfs:subClassOf` (incl. restriction axioms) | 928 |
| `slot_usage` required / cardinality | `owl:Restriction` (minCardinality/maxCardinality/allValuesFrom) | 806 restrictions |
| `disjoint_with` | `owl:disjointWith` (**re-injected** — gen-owl drops it) | 1 |
| `union_of` | `owl:equivalentClass [ owl:unionOf (…) ]` (**re-injected**) | 2 (3 + 25 members) |
| slot `is_a` bridges | `rdfs:subPropertyOf` to CRM P2/P4/P7/P14i/P62 etc. | 20 |
| `inverse` | `owl:inverseOf` (**restored where dropped**) | 16 |
| enums + permissible values | **SKOS ConceptSchemes + Concepts** (meaning-URIs used where declared, e.g. Pagoda → aat:300004829; minted `scheme/<Enum>/<value>` IRIs otherwise) | 7 schemes / 51 concepts |
| `aliases` | `skos:altLabel` (e.g. KumariRole → "Living Goddess", "Royal Kumari") | 8 classes |
| `minimum/maximum_value` | datatype restriction (float ∩ ≥0 ∩ ≤1 on confidence_score) | ✓ |
| `deprecated` | `owl:deprecated true` | 1 |
| descriptions | `skos:definition` | 100% of classes and slots |
| header + FAIR annotations | dcterms created/modified/license/citation, bibo:status, vann prefix/URI | ✓ |
| `rules:` (conditional constraints) | **not expressible in OWL** — enforced at LinkML/JSON-Schema/SHACL level | documented |

## Modelling principles

1. **Event-centric, not attribute-centric.** A structure is tied to the *events* that produced, used, documented, and (sometimes) destroyed it — following CIDOC-CRM — rather than carrying flat descriptive attributes.
2. **Emic terminology.** Where an established indigenous term exists it is the class name (`Stupa`, `Chaitya`, `DhungeDhara`, `Kumari`) rather than a generic English gloss.
3. **Living heritage.** Class names avoid authorized-heritage-discourse framing ("monument") that connotes static, past-tense heritage; the ontology treats these systems as ritually active.
4. **Contested knowledge is provenanced, not asserted.** Claims that different sources dispute are modelled as source-attributed assertions (CRMinf + PROV-O), never baked into class definitions.
5. **Direct PROV-O starting points.** The schema declares reusable LinkML mixins `Entity`, `Activity`, and `Agent` with the corresponding PROV-O class URIs. Every insertable class inherits at least one of these categories. `Agent` is not globally subclassed under `Entity`; an individual may carry both types where appropriate.

## Ontology alignment

HeritageGraph reuses established vocabularies rather than minting its own terms wherever possible:

| Prefix | Namespace | Used for |
|---|---|---|
| `crm:` | http://www.cidoc-crm.org/cidoc-crm/ | Core event/object/actor backbone (E-classes, P-properties) |
| `crminf:` | http://www.ics.forth.gr/isl/CRMinf/ | Assertion/belief backbone (I2 Belief, I4 Proposition Set). CRMinf has no official RDF release; this is the de-facto implementation namespace (ResearchSpace) — see changelog round 1. |
| `crmsci:` | http://www.cidoc-crm.org/crmsci/ | Scientific observation (field survey) |
| `prov:` | http://www.w3.org/ns/prov# | Provenance: agents, activities, derivation, attribution, revision |
| `aat:` | http://vocab.getty.edu/aat/ | Concept/type mappings |
| `schema:` | https://schema.org/ | Web-facing mappings |
| `wikidata:` | http://www.wikidata.org/entity/ | Entity mappings |
| `skos:` | http://www.w3.org/2004/02/skos/core# | Notes, change notes, scope notes |

**Provenance stance (PROV-O).** There is no normative CIDOC-CRM↔PROV-O mapping. HeritageGraph therefore asserts `prov:Activity` alignment as a *project-level* `broad_mappings` on its own event classes — never as a global axiom on `crm:E7_Activity`. See the changelog's verification note.

## Class hierarchy

![HeritageGraph class hierarchy, coloured by domain](HeritageGraph_hierarchy.png)

Classes are grouped by domain below. Each entry shows its minted or reused CURIE. `*(abstract)*` marks grouping classes that are not directly instantiated.

### Physical heritage (structures & objects)

- **PhysicalHeritageThing** `heritageGraph:PhysicalHeritageThing`
- **HumanMadeObject** `crm:E22_Human-Made_Object` — Physical objects created by human activity
  - **ArchitecturalStructure** `heritageGraph:ArchitecturalStructure` — Physical structures built for religious, social, or civic purposes. Links to events of production, use, custody, and documentation.
    - **ReligiousStructure** `heritageGraph:ReligiousStructure` — Architectural structure whose defining purpose is religious: enshrines a deity and/or is a locus of ritual activation. Abstract grouping for sacred struct…
      - **Chaitya** `heritageGraph:Chaitya` — Buddhist votive shrine (chaitya); votive stupa form found across the Kathmandu Valley.
      - **KumariHouse** `heritageGraph:KumariHouse` — God-house residence of a Kumari during tenure (e.g., Kumari Ghar, Kathmandu). Specialised ReligiousStructure.
      - **Stupa** `heritageGraph:Stupa` — Buddhist dome-shaped reliquary shrine with circumambulation and ritual activation (e.g., Boudhanath, Swayambhunath).
      - **Temple** `heritageGraph:Temple` — Religious structure characterized by deity enshrinement and ritual activation. Legal designation (e.g. 'Ancient Monument' under Nepal law) is recorded per…
    - **RestHouse** `heritageGraph:RestHouse` — Community structures for travelers and pilgrims, maintained by Guthi organizations
      - **Dharmashala** `heritageGraph:Dharmashala` — Pilgrim lodge operated by a Guthi organization
      - **Pati** `heritageGraph:Pati` — Open-air pavilion for resting travelers
      - **Sattal** `heritageGraph:Sattal` — Multi-story rest house (3-5 floors) with ritual and social functions
    - **WaterStructure** `heritageGraph:WaterStructure` — Engineered water supply systems with ritual and civic significance
      - **DhungeDhara** `heritageGraph:DhungeDhara` — Stone spout (hiti) with carved imagery, used for ritual bathing and daily water supply
      - **Pokhari** `heritageGraph:Pokhari` — Pond or tank for water storage, ritual bathing, and ecological management
  - **IconographicObject** `heritageGraph:IconographicObject` — Sacred visual art objects that depict or embody deities through iconographic conventions
    - **Murti** `heritageGraph:Murti` — Consecrated statue of a deity, ritually activated to serve as divine presence (not merely depiction)
    - **Paubha** `heritageGraph:Paubha` — Traditional Newari scroll painting (thangka) with mandala and deity iconography
- **ArchitecturalElement** `heritageGraph:ArchitecturalElement` — Carved or constructed component of a architectural strucuture (e.g., Gajur, Torana, Tundal)

### Events & activities (PROV-aligned)

- **RitualEvent** `heritageGraph:RitualEvent` — Intentional ritual activity that activates sacred space, invokes deities, and binds social groups
  - **Festival** `heritageGraph:Festival` — Large-scale community ritual event (Jatra) involving processions, music, and collective participation
    - **ChariotFestival** `heritageGraph:ChariotFestival` — Festival involving ceremonial chariot procession (e.g., Rato Machhindranath Jatra)
    - **MaskedDance** `heritageGraph:MaskedDance` — Festival featuring masked dancers embodying deities (e.g., Kartik Naach)
  - **RitualAssessment** *(abstract)* `heritageGraph:RitualAssessment` — A performed assessment carried out during Kumari selection. Modelled as an event (not a hard criterion) so that source-specific, possibly conflicting acco…
    - **FearlessnessAssessment** `heritageGraph:FearlessnessAssessment` — The 'fearlessness test' popularly described (animal heads, masked dancers in darkness). Its historical and contemporary practice is DISPUTED -- some forme…
- **Consecration** `heritageGraph:Consecration` — Ritual event that transforms an object into a sacred vessel (e.g., Prana Pratistha for Murti)
- **Enshrinement** `heritageGraph:Enshrinement` — Event of installing a deity's murti or symbol within a temple sanctum
- **Production** `crm:E12_Production` — Event of creating an architectural structure, murti, or paubha
- **TransferOfCustody** `crm:E10_Transfer_of_Custody` — Event of transferring responsibility for temple maintenance, ritual performance, or artifact stewardship
- **ConditionAssessment** `crm:E14_Condition_Assessment` — Event of evaluating the physical state of a heritage object or structure
- **HistoricalEvent** `heritageGraph:HistoricalEvent` — Major event affecting heritage structures or ritual life (earthquake, epidemic, political transition, fire, flood).
  - **DestructionEvent** `crm:E6_Destruction` — Event that destroyed or damaged a structure.

### Kumari (living-goddess) lifecycle

- **KumariTenure** `heritageGraph:KumariTenure` — Time-bounded role where a person embodies a deity as Living Goddess (Kumari), residing at a specific god-house and supported by religious institutions. Th…
- **KumariRole** `heritageGraph:KumariRole` — The role/office of Kumari (living-goddess embodiment) that a person assumes for the duration of a KumariTenure. The role is the type; the tenure is the ti…
- **KumariLifecycleEvent** *(abstract)* `heritageGraph:KumariLifecycleEvent` — Abstract event that bounds a KumariTenure (selection, enthronement, or retirement). Shared axiom: every instance references some KumariTenure via bounds_t…
  - **KumariEnthronementEvent** `heritageGraph:KumariEnthronementEvent` — Ritual installing a selected girl into the Kumari role and residence, activating the tenure (distinct from selection, which chooses her, and retirement, w…
  - **KumariRetirementEvent** `heritageGraph:KumariRetirementEvent` — Ritual or administrative event that formally ends a Living Goddess tenure, returning the person to secular status. Common triggers: first menstruation, in…
  - **KumariSelectionEvent** `heritageGraph:KumariSelectionEvent` — Tantric ritual process of selecting a new Living Goddess from eligible candidates. Involves examination of 32 auspicious physical marks (lakshana), horosc…
- **SelectionCriterion** `heritageGraph:SelectionCriterion` — An eligibility criterion a candidate must satisfy to assume the Kumari role. Modelled as explicit subclasses so 'what are the eligibility criteria?' is a …
  - **AgeCriterion** `heritageGraph:AgeCriterion` — Candidate must be within the prescribed pre-pubescent age range.
  - **HoroscopeCompatibilityCriterion** `heritageGraph:HoroscopeCompatibilityCriterion` — Candidate's horoscope must be compatible with the city and ruling authority.
  - **LineageCriterion** `heritageGraph:LineageCriterion` — Candidate must belong to an eligible lineage (Shakya / Vajracharya Newar Buddhist family).
  - **PhysicalIntegrityCriterion** `heritageGraph:PhysicalIntegrityCriterion` — Candidate must have an unblemished body with no scars, wounds, or loss of blood/teeth.
  - **ThirtyTwoPerfectionsCriterion** `heritageGraph:ThirtyTwoPerfectionsCriterion` — Candidate must exhibit the battis lakshana (thirty-two perfections/auspicious bodily marks).

### Actors & social groups

- **Actor** `crm:E39_Actor` — General actor (person or group) responsible for events
- **Person** `crm:E21_Person` — Individual person who performs, commissions, documents, or verifies heritage activities
- **Deity** `heritageGraph:Deity` — Divine conceptual entity in Hindu, Buddhist, or syncretic traditions. Distinct from physical representations (Murti) and ritual presences.
- **Guthi** `heritageGraph:Guthi` — Endowed trust organization unique to Nepal, managing temples, rituals, and land through hereditary or voluntary membership
- **CasteGroup** `heritageGraph:CasteGroup` — Hereditary social group (Jati) with specific ritual roles and occupational duties
- **DataCustodian** `heritageGraph:DataCustodian` — Institution or person currently stewarding heritage data

### Assertion / evidence / provenance (CRMinf + PROV-O)

- **Assertion** `crminf:I2_Belief` — A belief/claim about a heritage entity (CRMinf I2 Belief) that holds an I4 Proposition Set to be true, with explicit source, agent, time, and confidence_score. …
- **AssertionSubject** `heritageGraph:AssertionSubject` — Any entity that can be the subject of a heritage assertion
- **SyncreticRelationship** `heritageGraph:SyncreticRelationship` — Formalizes the syncretic equivalence between divine entities across different theological frameworks. Following CIDOC CRM E13, it treats syncretism as a p…
- **DocumentationActivity** `heritageGraph:DocumentationActivity` — The intellectual or technical process of recording information about a heritage entity, aligned with CIDOC E7 (Activity) and PROV-O Activity.
  - **FieldSurveyActivity** `heritageGraph:FieldSurveyActivity` — The activity of measuring, photographing, or assessing a site in person.
  - **OralHistoryInterview** `heritageGraph:OralHistoryInterview` — The interaction event between a researcher and a knowledge holder.
  - **Verification** `heritageGraph:Verification` — Process of cross-checking heritage claims against multiple sources
- **DataSource** `heritageGraph:DataSource` — Original source from which heritage information was derived
  - **ArchivalRecord** `heritageGraph:ArchivalRecord` — Government or institutional administrative record
  - **InformationObject** `heritageGraph:InformationObject` — A recorded piece of information about heritage

### Supporting / value objects

- **Place** `crm:E53_Place` — Defined geographic location where events occur and structures exist
- **TimeSpan** `crm:E52_Time-Span` — Temporal extent of an event or period
- **Material** `crm:E57_Material` — Physical substance used in construction or crafting
- **Technique** `crm:E29_Design_or_Procedure` — Method or craft process used in production or ritual
- **ReligiousTradition** `heritageGraph:ReligiousTradition` — Religious or philosophical tradition (e.g., Hindu, Buddhist, Syncretic)
- **CalendarSystem** `heritageGraph:CalendarSystem` — Calendar reckoning system with conversion rules for multi-calendar temporal reasoning
- **ConditionState** `crm:E3_Condition_State` — A physical condition state of a heritage object
- **Container** `` — Root container for cultural heritage data instances
- **Metadata** `` — Dataset metadata information
- **FieldSurveyDataset** `heritageGraph:FieldSurveyDataset` — The structured data or report resulting from a field survey.
- **OralHistoryRecording** `heritageGraph:OralHistoryRecording` — The recording or transcript of an oral history interview.

## Enumerations

### ConditionType
| Value | Meaning |
|---|---|
| `Good` | No significant damage |
| `Damaged` | Partially damaged |
| `Ruined` | Severely damaged or collapsed |
| `Restored` | Repaired and stabilized |

### ExistenceStatus
| Value | Meaning |
|---|---|
| `Extant` | Currently exists in physical form |
| `PartiallyExtant` | Fragments or ruins remain |
| `Destroyed` | Known to have been destroyed; no physical remains |
| `Lost` | Existence documented but location/remains unknown |
| `Hypothetical` | Reconstructed or theorized; never physically realized |
| `Unknown` | Existence status uncertain |

### RitualType
| Value | Meaning |
|---|---|
| `NityaPuja` | Daily mandatory worship |
| `NaimittikaPuja` | Occasional/Festival worship |
| `KamyaPuja` | Desire-based optional worship |
| `Abhisheka` | Ritual bathing/anointing of deity |
| `Homa` | Fire offering ritual |
| `Bhajan` | Devotional singing ritual |
| `Yagna` | Vedic sacrifice ritual |
| `Vrata` | Vow observance ritual |
| `Jatra` | Festival procession ritual |
| `ChariotProcession` | Ritual chariot pulling |
| `MaskedPerformance` | Ritual masked dance |
| `RitualConsecration` | Consecration/activation ritual |
| `ProcessionRitual` | Ritual procession/movement |
| `InstallationRitual` | Installation/enshrinement ritual |
| `DeinstallationRitual` | De-installation/conclusion ritual |
| `ReturningRitual` | Return to normal state ritual |
| `Circumambulation` | Ritual circular movement around sacred site |
| `RelicTour` | Procession with sacred relics between sites |
| `ProcessionalMovement` | General ritual movement between locations |

> **Design note:** RitualType currently mixes three orthogonal axes: worship-frequency (NityaPuja/NaimittikaPuja/KamyaPuja), ritual form (Homa/Jatra/MaskedPerformance), and lifecycle (InstallationRitual/ReturningRitual). Consider splitting into RitualFrequency + RitualForm. Also: Circumambulation/ProcessionalMovement/ProcessionRitual/RelicTour overlap with RitualEvent.route_places/start_place/end_place/route_description -- pick one canonical mechanism for moving rituals.

### DatePrecision
| Value | Meaning |
|---|---|
| `Exact` | Precise date known |
| `Year` | Year-level precision only |
| `Decade` | Within 10-year range |
| `Century` | Within century range |
| `Circa` | Approximate date |

### SyncreticType
| Value | Meaning |
|---|---|
| `Equivalence` | Same deity in different traditions (e.g., Avalokiteshvara = Matsyendranath) |
| `Appropriation` | Deity borrowed from one tradition into another |
| `Fusion` | Intrinsically syncretic deity merging multiple traditions |
| `Historical` | Gradual syncretism over time |

### ArchitecturalStyle
A vocabulary of architectural styles for South Asian heritage, mapped to CIDOC E55 Type.

| Value | Meaning |
|---|---|
| `Pagoda` | Multi-tiered roof style indigenous to Nepal |
| `Shikhara` | North Indian spire-shaped style |
| `Dome` | Dome-based style (Mughal/Neo-classical influence) |
| `Chaitya` | Buddhist votive shrine style |
| `Stupa` | Buddhist dome-shaped reliquary |

### GuthiType
Controlled vocabulary of Guthi functional types (CRM E55_Type)

| Value | Meaning |
|---|---|
| `SiGuthi` | Funeral trust |
| `JatraGuthi` | Festival organization trust |
| `PujaGuthi` | Daily worship trust |
| `TempleGuthi` | Temple maintenance trust |
| `NashaGuthi` | Music and dance trust |
| `SanaGuthi` | Agricultural cooperative trust |
| `SanGuthi` | Life-cycle ritual trust |
| `RajGuthi` | Royal endowment trust |

## Design pattern — provenance & assertions

Provenance in HeritageGraph separates PROV categories from the assertion layer.

![HeritageGraph provenance pattern — PROV-O categories plus the CRMinf assertion layer](HeritageGraph_provenance.png)

**Layer 1 — direct PROV-O mixins.** `Entity`, `Activity`, and `Agent` provide LinkML validation and generated-model fields while reusing PROV-O class and property URIs directly:

| Slot | PROV-O property | Points to |
|---|---|---|
| `was_derived_from` | `prov:wasDerivedFrom` | `Entity` |
| `was_attributed_to` | `prov:wasAttributedTo` | `Agent` |
| `generated_at_time` | `prov:generatedAtTime` | `datetime` |
| `was_generated_by` | `prov:wasGeneratedBy` | `Activity` |
| `used` | `prov:used` | `Entity` |
| `generated` | `prov:generated` | `Entity` |
| `was_associated_with` | `prov:wasAssociatedWith` | `Agent` |
| `was_informed_by` | `prov:wasInformedBy` | `Activity` |
| `was_influenced_by` | `prov:wasInfluencedBy` | `Entity`, `Activity`, or `Agent` |
| `started_at_time` / `ended_at_time` | PROV activity timestamps | `datetime` |
| `acted_on_behalf_of` | `prov:actedOnBehalfOf` | `Agent` |

`was_influenced_by` is the general fallback relation. More specific PROV properties should be used whenever their semantics are known. `was_documented_by` specializes this general influence pattern for a pre-existing entity or event recorded by a `DocumentationActivity`.

The schema makes provenance fields available on every inserted domain object, including `Container` and `Metadata`. Cardinality and automatic population remain ingestion-policy concerns: the application inserting a record must supply or generate the relevant activity, agent, and timestamp values.

**Layer 2 — contested claims (opt-in).** Where sources *disagree* about a fact, the claim itself becomes a first-class, revisable object rather than ground truth. Rather than stating "this stupa was built in 598 CE" as fact, the schema records *who claimed it, from what source, when, and with what confidence_score* — so conflicting accounts coexist. The backbone is **CRMinf (belief) composed with PROV-O (agent/time/derivation)**:

```
  AssertionSubject  ──asserts_about (heritageGraph:assertsAbout)──  Assertion
   (the subject)      ◄─has_assertion (inverse)  (crminf:I2_Belief)
                                                             │
     was_attributed_to (prov:wasAttributedTo) ────────┤
     was_derived_from (prov:wasDerivedFrom)  ────────┤
     generated_at_time       (prov:generatedAtTime) ────────┤
     confidence_score        (0.0–1.0)              ────────┤
     supersedes_assertion    (prov:wasRevisionOf)   ────────┘  ← version chain
                                                             │
     generated (prov:generated)                    │
  DocumentationActivity ─────────────────────────────────────┘
   (prov:Activity)
```

Key points:
- `has_assertion` means that assertions exist about the subject; it does **not** say that provenance belongs to the subject. Provenance is carried by each `Assertion`.
- **Machine-readable claims:** besides the free-text `assertion_content`, an Assertion can carry **Proposition** objects (`heritageGraph:Proposition`, broad `crminf:I4_Proposition_Set`, close `rdf:Statement`) via `asserts_proposition` (`crminf:J4_that`) — each a subject–predicate–object statement whose predicate is a URI/CURIE, so *what is claimed* is queryable, not just readable.
- **AltLabels:** emic English/romanized alternate labels (`skos:altLabel`) are declared via `aliases:` — e.g. KumariRole carries "Living Goddess" and "Royal Kumari"; script-specific (Devanagari) labels are deferred to a localization layer.
- **`Assertion`** is a `crminf:I2_Belief` — a *belief*, not a bare fact.
- **Version chains** use `supersedes_assertion` → `prov:wasRevisionOf`. The current assertion is the one with no incoming revision. (This replaced a misuse of `prov:invalidated`, which is an Activity→Entity relation.)
- **Entity-mention vs. derivation** are distinct: `mentioned_in_source` (`heritageGraph:mentionedInSource`) for "a source talks about this entity" vs. `was_derived_from` (`prov:wasDerivedFrom`) for "this claim was logically derived from a source".

## Design pattern — the Kumari (living-goddess) lifecycle

The Kumari tradition is modelled as a **time-bounded role holding** (CIDOC E4 Period) bounded by lifecycle events, with eligibility criteria as explicit classes and contested tests as provenanced assessments.

```
  Person ──had_participant──►  KumariTenure  ◄── the E4 Period (the 'living goddess')
                                 │  embodies ► Deity (Taleju)
                                 │  assumes_role ► KumariRole
                                 │  residence_structure ► KumariHouse
                                 │
       KumariLifecycleEvent (abstract, bounds_tenure ► KumariTenure)
            ├── KumariSelectionEvent    selected_through   (chooses the girl)
            ├── KumariEnthronementEvent enthroned_through  (activates the tenure)
            └── KumariRetirementEvent   retired_through    (desanctification / return to secular status)
```

**Eligibility criteria are explicit subclasses**, so "what are the criteria to become a Kumari?" is a subclass query rather than free-text parsing:

- **AgeCriterion** — Candidate must be within the prescribed pre-pubescent age range.
- **HoroscopeCompatibilityCriterion** — Candidate's horoscope must be compatible with the city and ruling authority.
- **LineageCriterion** — Candidate must belong to an eligible lineage (Shakya / Vajracharya Newar Buddhist family).
- **PhysicalIntegrityCriterion** — Candidate must have an unblemished body with no scars, wounds, or loss of blood/teeth.
- **ThirtyTwoPerfectionsCriterion** — Candidate must exhibit the battis lakshana (thirty-two perfections/auspicious bodily marks).

**The fearlessness test is *not* a criterion.** Its practice (animal heads, masked dancers) is disputed — some former Kumaris contest how it is described. It is therefore modelled as an assessment event whose accounts attach as provenanced assertions:

```
  RitualAssessment (abstract, prov:Activity)
       └── FearlessnessAssessment  ──has_assertion──►  Assertion (per source)
```
> The 'fearlessness test' popularly described (animal heads, masked dancers in darkness). Its historical and contemporary practice is DISPUTED -- some former Kumaris contest how it is described. Represented as an assessment whose accounts are source-attributed via has_assertion, NOT as a mandatory criterion.

*Scope note:* Deliberately not a SelectionCriterion subclass: popular accounts and lived testimony disagree. Attach each account as a Assertion (CRMinf I2 Belief) with its own source and confidence_score.

## Query patterns

Illustrative SPARQL over the OWL export. Prefixes assumed:

```sparql
PREFIX heritageGraph: <https://w3id.org/heritagegraph/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX crminf: <http://www.ics.forth.gr/isl/CRMinf/>
```

**1. Eligibility criteria to become a Kumari** (subclass query, no string parsing):
```sparql
SELECT ?criterion WHERE { ?criterion rdfs:subClassOf heritageGraph:SelectionCriterion . }
```

**2. Latest (non-superseded) assertion about an entity:**
```sparql
SELECT ?a WHERE {
  ?a a crminf:I2_Belief ;
     heritageGraph:assertsAbout ?entity .
  FILTER NOT EXISTS { ?newer prov:wasRevisionOf ?a . }
}
```

**3. All source-attributed accounts of a fearlessness assessment** (contested claims, side by side):
```sparql
SELECT ?assessment ?claim ?source ?confidence_score WHERE {
  ?assessment a heritageGraph:FearlessnessAssessment ;
              heritageGraph:hasAssertion ?claim .
  ?claim prov:value ?text ;
         prov:wasDerivedFrom ?source ;
         heritageGraph:confidenceScore ?confidence_score .
}
```

**4. Reconstruct a full Kumari lifecycle** (selection → enthronement → retirement):
```sparql
SELECT ?tenure ?selection ?enthronement ?retirement WHERE {
  ?tenure a heritageGraph:KumariTenure .
  OPTIONAL { ?tenure heritageGraph:selectedThrough  ?selection . }
  OPTIONAL { ?tenure heritageGraph:enthronedThrough ?enthronement . }
  OPTIONAL { ?tenure heritageGraph:retiredThrough   ?retirement . }
}
```


## Files

- `ontology/HeritageGraph.yaml` — authoritative LinkML source (approved 0.1.0-alpha.5; `HeritageGraph_fixed.yaml` symlinks to it)
- `ontology/HeritageGraph.ttl` / `ontology/HeritageGraph.shacl.ttl` — generated OWL + SHACL (finalized: disjointness/unions/inverses guarded, shapes conformance-gated)
- `HeritageGraph_CHANGELOG.md` — every fix through the 0.1.0-alpha.4 PROV-O audit, with rationale
- `HeritageGraph_URI_FIX_CHANGELOG.md` — the 0.1.0-alpha.5 remediation (URI policy, mapping audit, CRM domain/range repairs, wiring, constraints)
- `docs/` — auto-generated per-class and per-slot reference pages (LinkML `gen-doc`)
- This file — curated overview
