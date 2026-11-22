# Classes

### Activity

**IRI:** `http://www.w3.org/ns/prov#Activity` · `prov:Activity`

Direct LinkML representation of prov:Activity. Applied to events and processes that use, transform, generate, document, assess, or verify entities.

| | |
|---|---|
| Subclasses | [Condition Assessment](classes.md#e14_condition_assessment), [Consecration](classes.md#consecration), [Documentation Activity](classes.md#documentationactivity), [Enshrinement](classes.md#enshrinement), [Historical Event](classes.md#historicalevent), [Production](classes.md#e12_production), [Ritual Event](classes.md#ritualevent), [Syncretic Relationship](classes.md#syncreticrelationship), [Transfer Of Custody](classes.md#e10_transfer_of_custody) |
| Used in | used in axioms of [Information Object](classes.md#informationobject) |

### Actor

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E39_Actor` · `crm:E39_Actor`

General actor (person or group) responsible for events

| | |
|---|---|
| Superclasses | [Agent](classes.md#agent) |
| Subclasses | [Caste Group](classes.md#castegroup), [Data Custodian](classes.md#datacustodian), [Guthi](classes.md#guthi), [Person](classes.md#e21_person) |
| Used in | in range of [actors](object-properties.md#actors); in range of [Commissioned by](object-properties.md#commissionedby); in range of [Datacite creator](object-properties.md#sourcecreator); in range of [Datacite publisher](object-properties.md#sourcepublisher); in range of [Had participant](object-properties.md#hadparticipant); in range of [Performed by group](object-properties.md#performedbygroup); in range of [Used by](object-properties.md#usedby); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Consecration](classes.md#consecration); used in axioms of [Container](classes.md#container); used in axioms of [Data Source](classes.md#datasource); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Iconographic Object](classes.md#iconographicobject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Age Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/AgeCriterion` · `heritageGraph:AgeCriterion`

Candidate must be within the prescribed pre-pubescent age range.

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Agent

**IRI:** `http://www.w3.org/ns/prov#Agent` · `prov:Agent`

Direct LinkML representation of prov:Agent. Agents bear responsibility for activities or entities. PROV-O permits an individual agent also to be typed as an Entity, but does not define every Agent as a subclass of Entity.

| | |
|---|---|
| Subclasses | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |

### Architectural Element

**IRI:** `https://cair-nepal.org/heritagegraph/ArchitecturalElement` · `heritageGraph:ArchitecturalElement`

Carved or constructed component of an architectural structure (e.g., Gajur, Torana, Tundal)

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Is component of](object-properties.md#p46i_forms_part_of) *only* [Architectural Structure](classes.md#architecturalstructure); [Is component of](object-properties.md#p46i_forms_part_of) *max* `1`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Is component of](object-properties.md#p46i_forms_part_of) *min* `1`; [note](datatype-properties.md#p3_has_note) *max* `1`; [note](datatype-properties.md#p3_has_note) *min* `0` |
| Used in | in range of [Architectural elements](object-properties.md#architectural_elements); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Physical Heritage Thing](classes.md#physicalheritagething) |

### Architectural Structure

**IRI:** `https://cair-nepal.org/heritagegraph/ArchitecturalStructure` · `heritageGraph:ArchitecturalStructure`

Physical structures built for religious, social, or civic purposes. Links to events of production, use, custody, and documentation.

| | |
|---|---|
| Superclasses | [Human Made Object](classes.md#e22_human-made_object) |
| Restrictions | [Documented in source](object-properties.md#mentionedinsource) *only* [Data Source](classes.md#datasource); [Last known existence date](datatype-properties.md#lastknownexistencedate) *max* `1`; [Was produced by event](object-properties.md#p108i_was_produced_by) *max* `1`; [Hypothesized location](object-properties.md#hypothesizedlocation) *min* `0`; [Has component](object-properties.md#p46_is_composed_of) *only* [Architectural Element](classes.md#architecturalelement); [Has condition assessment](object-properties.md#p34i_was_assessed_by) *only* [Condition Assessment](classes.md#e14_condition_assessment); [has existence status](object-properties.md#existencestatus) *only* [Existence Status](classes.md#existencestatus-2); [note](datatype-properties.md#p3_has_note) *min* `0`; [Has architectural style](object-properties.md#hasarchitecturalstyle) *only* [Architectural Style](classes.md#architecturalstyle-2); [Has condition assessment](object-properties.md#p34i_was_assessed_by) *min* `0`; [Last known existence date](datatype-properties.md#lastknownexistencedate) *min* `0`; [has destruction event](object-properties.md#destructionevent) *min* `0`; [Managed by guthi](object-properties.md#managedbyguthi) *only* [Guthi](classes.md#guthi); [Was produced by event](object-properties.md#p108i_was_produced_by) *only* [Production](classes.md#e12_production); [Has component](object-properties.md#p46_is_composed_of) *min* `0`; [Has assertion](object-properties.md#hasassertion) *only* [Assertion](classes.md#i2_belief); [Was produced by event](object-properties.md#p108i_was_produced_by) *min* `0`; [Managed by guthi](object-properties.md#managedbyguthi) *min* `0`; [Last known existence date](datatype-properties.md#lastknownexistencedate) *only* [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime); [has destruction event](object-properties.md#destructionevent) *max* `1`; [has existence status](object-properties.md#existencestatus) *min* `0`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Has current location](object-properties.md#p55_has_current_location) *only* [Place](classes.md#e53_place); [Documented in source](object-properties.md#mentionedinsource) *min* `0`; [Has current location](object-properties.md#p55_has_current_location) *min* `0`; [Has architectural style](object-properties.md#hasarchitecturalstyle) *max* `1`; [Has architectural style](object-properties.md#hasarchitecturalstyle) *min* `0`; [Has assertion](object-properties.md#hasassertion) *min* `0`; [Has current location](object-properties.md#p55_has_current_location) *max* `1`; [has destruction event](object-properties.md#destructionevent) *only* [Destruction Event](classes.md#e6_destruction); [Hypothesized location](object-properties.md#hypothesizedlocation) *only* [Place](classes.md#e53_place); [has existence status](object-properties.md#existencestatus) *max* `1`; [note](datatype-properties.md#p3_has_note) *max* `1` |
| Subclasses | [Religious Structure](classes.md#religiousstructure), [Rest House](classes.md#resthouse), [Water Structure](classes.md#waterstructure) |
| Used in | in range of [Architectural structures](object-properties.md#architecturalstructures); in range of [Residence structure](object-properties.md#residencestructure); in range of [structures](object-properties.md#structures); used in axioms of [Architectural Element](classes.md#architecturalelement); used in axioms of [Container](classes.md#container); used in axioms of [Guthi](classes.md#guthi); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Physical Heritage Thing](classes.md#physicalheritagething) |

### Architectural Style

**IRI:** `https://cair-nepal.org/heritagegraph/ArchitecturalStyle` · `heritageGraph:ArchitecturalStyle`

A vocabulary of architectural styles for South Asian heritage, mapped to CIDOC E55 Type.

| | |
|---|---|
| Instances | [Chaitya style](concepts.md#chaitya), [Dome style](concepts.md#dome), [Pagoda style](concepts.md#pagoda), [Shikhara style](concepts.md#shikhara), [Stupa style](concepts.md#stupa) |
| Used in | in range of [Has architectural style](object-properties.md#hasarchitecturalstyle); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Temple](classes.md#temple) |
| permissible_values | Dome style; Chaitya style; Shikhara style; Stupa style; Pagoda style |

### Archival Record

**IRI:** `https://cair-nepal.org/heritagegraph/ArchivalRecord` · `heritageGraph:ArchivalRecord`

Government or institutional administrative record

| | |
|---|---|
| Superclasses | [Data Source](classes.md#datasource) |

### Assertion

**IRI:** `http://www.cidoc-crm.org/extensions/crminf/I2_Belief` · `crminf:I2_Belief`

A provenance-bearing belief or claim about a heritage entity or event. The assertion is represented as CRMinf I2 Belief and as a prov:Entity, allowing source, attribution, generation time, revision, confidence, and reconciliation status to be recorded explicitly.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Used in | in range of [assertions](object-properties.md#assertions); in range of [Has assertion](object-properties.md#hasassertion); in range of [Verified assertion](object-properties.md#verifiedassertion); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Verification](classes.md#verification) |
| crminf pattern | I2_Belief -J4_that-> I4_Proposition_Set; evidence via I5_Inference_Making (J1_used_as_premise / J2_concluded_that); expert re-check via I7_Belief_Adoption |

### Assertion Subject

**IRI:** `https://cair-nepal.org/heritagegraph/AssertionSubject` · `heritageGraph:AssertionSubject`

Any HeritageGraph entity or event that may be the subject of an assertion.

| | |
|---|---|
| Restrictions | [Human Made Object](classes.md#e22_human-made_object) *or* [Architectural Element](classes.md#architecturalelement) *or* [Deity](classes.md#deity) *or* [Religious Tradition](classes.md#religioustradition) *or* [Historical Event](classes.md#historicalevent) *or* [Ritual Event](classes.md#ritualevent) *or* [Production](classes.md#e12_production) *or* [Consecration](classes.md#consecration) *or* [Enshrinement](classes.md#enshrinement) *or* [Transfer Of Custody](classes.md#e10_transfer_of_custody) *or* [Condition Assessment](classes.md#e14_condition_assessment) *or* [Condition State](classes.md#e3_condition_state) *or* [Actor](classes.md#e39_actor) *or* [Place](classes.md#e53_place) *or* [Time Span](classes.md#e52_time-span) *or* [Data Source](classes.md#datasource) *or* [Documentation Activity](classes.md#documentationactivity) *or* [Syncretic Relationship](classes.md#syncreticrelationship) *or* [Kumari Tenure](classes.md#kumaritenure) *or* [Technique](classes.md#e29_design_or_procedure) *or* [Material](classes.md#e57_material) *or* [Kumari Role](classes.md#kumarirole) *or* [Selection Criterion](classes.md#selectioncriterion) *or* [Assertion](classes.md#i2_belief) *or* [Calendar System](classes.md#calendarsystem) |
| Used in | in range of [Asserts about](object-properties.md#assertsabout); in range of [documents](object-properties.md#documents); in range of [Proposition object entity](object-properties.md#propositionobjectentity); in range of [Proposition subject](object-properties.md#propositionsubject); used in axioms of [Documentation Activity](classes.md#documentationactivity); used in axioms of [Information Object](classes.md#informationobject); used in axioms of [Proposition](classes.md#proposition) |

### Calendar System

**IRI:** `https://cair-nepal.org/heritagegraph/CalendarSystem` · `heritageGraph:CalendarSystem`

Calendar reckoning system with conversion rules for multi-calendar temporal reasoning

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Epoch date gregorian](datatype-properties.md#epochdategregorian) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Epoch date gregorian](datatype-properties.md#epochdategregorian) *max* `1`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Year offset from gregorian](datatype-properties.md#yearoffsetfromgregorian) *max* `1`; [note](datatype-properties.md#p3_has_note) *min* `0`; [Is primary for tradition](object-properties.md#isprimaryfortradition) *min* `0`; [Epoch date gregorian](datatype-properties.md#epochdategregorian) *min* `0`; [Is primary for tradition](object-properties.md#isprimaryfortradition) *only* [Religious Tradition](classes.md#religioustradition); [note](datatype-properties.md#p3_has_note) *max* `1`; [Year offset from gregorian](datatype-properties.md#yearoffsetfromgregorian) *min* `0`; [Year offset from gregorian](datatype-properties.md#yearoffsetfromgregorian) *only* [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) |
| Used in | in range of [Calendar systems](object-properties.md#calendar_systems); in range of [has calendar system](object-properties.md#calendarsystem); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container) |

### Caste Group

**IRI:** `https://cair-nepal.org/heritagegraph/CasteGroup` · `heritageGraph:CasteGroup`

Hereditary social group (Jati) with specific ritual roles and occupational duties

| | |
|---|---|
| Superclasses | [Actor](classes.md#e39_actor) |
| Restrictions | [Traditional role](datatype-properties.md#traditionalrole) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Traditional role](datatype-properties.md#traditionalrole) *min* `0`; [note](datatype-properties.md#p3_has_note) *max* `1`; [Traditional role](datatype-properties.md#traditionalrole) *max* `1`; [note](datatype-properties.md#p3_has_note) *min* `0`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | in range of [Caste groups](object-properties.md#caste_groups); in range of [Performed by group](object-properties.md#performedbygroup); used in axioms of [Container](classes.md#container); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Chaitya

**IRI:** `https://cair-nepal.org/heritagegraph/Chaitya` · `heritageGraph:Chaitya`

Buddhist votive shrine (chaitya); votive stupa form found across the Kathmandu Valley.

| | |
|---|---|
| Superclasses | [Religious Structure](classes.md#religiousstructure) |
| Disjoint with | [Stupa](classes.md#stupa-2) |

### Chariot Festival

**IRI:** `https://cair-nepal.org/heritagegraph/ChariotFestival` · `heritageGraph:ChariotFestival`

Festival involving ceremonial chariot procession (e.g., Rato Machhindranath Jatra)

| | |
|---|---|
| Superclasses | [Festival](classes.md#festival) |

### Concept

**IRI:** `http://www.w3.org/2004/02/skos/core#Concept` · `skos:Concept`

| | |
|---|---|
| Instances | [Abhisheka](concepts.md#abhisheka), [Appropriation](concepts.md#appropriation), [Bhajan](concepts.md#bhajan), [Century](concepts.md#century), [Chaitya style](concepts.md#chaitya), [Chariot Procession](concepts.md#chariotprocession), [Circa](concepts.md#circa), [Circumambulation](concepts.md#circumambulation), [Damaged](concepts.md#damaged), [Decade](concepts.md#decade), [Deinstallation Ritual](concepts.md#deinstallationritual), [Destroyed](concepts.md#destroyed), [Dome style](concepts.md#dome), [Equivalence](concepts.md#equivalence), [Exact](concepts.md#exact), [Extant](concepts.md#extant), [Fusion](concepts.md#fusion), [Good](concepts.md#good), [Historical](concepts.md#historical), [Homa](concepts.md#homa), [Hypothetical](concepts.md#hypothetical), [Installation Ritual](concepts.md#installationritual), [Jatra](concepts.md#jatra), [Jatra Guthi](concepts.md#jatraguthi), [Kamya Puja](concepts.md#kamyapuja), [Lost](concepts.md#lost), [Masked Performance](concepts.md#maskedperformance), [Naimittika Puja](concepts.md#naimittikapuja), [Nasha Guthi](concepts.md#nashaguthi), [Nitya Puja](concepts.md#nityapuja), [Pagoda style](concepts.md#pagoda), [Partially Extant](concepts.md#partiallyextant), [Procession Ritual](concepts.md#processionritual), [Processional Movement](concepts.md#processionalmovement), [Puja Guthi](concepts.md#pujaguthi), [Raj Guthi](concepts.md#rajguthi), [Relic Tour](concepts.md#relictour), [Restored](concepts.md#restored), [Returning Ritual](concepts.md#returningritual), [Ritual Consecration](concepts.md#ritualconsecration), [Ruined](concepts.md#ruined), [San Guthi](concepts.md#sanguthi), [Sana Guthi](concepts.md#sanaguthi), [Shikhara style](concepts.md#shikhara), [Si Guthi](concepts.md#siguthi), [Stupa style](concepts.md#stupa), [Temple Guthi](concepts.md#templeguthi), [Unknown](concepts.md#unknown), [Vrata](concepts.md#vrata), [Yagna](concepts.md#yagna), [Year](concepts.md#year) |

### ConceptScheme

**IRI:** `http://www.w3.org/2004/02/skos/core#ConceptScheme` · `skos:ConceptScheme`

| | |
|---|---|
| Instances | [Architectural Style (concept scheme)](concept-schemes.md#architecturalstyle), [Condition Type (concept scheme)](concept-schemes.md#conditiontype), [Date Precision (concept scheme)](concept-schemes.md#dateprecision-2), [Existence Status (concept scheme)](concept-schemes.md#existencestatus), [Guthi Type (concept scheme)](concept-schemes.md#guthitype), [HeritageGraph LinkML schema](concept-schemes.md#schema), [Ritual Type (concept scheme)](concept-schemes.md#ritualtype-2), [Syncretic Type (concept scheme)](concept-schemes.md#syncretictype-2) |

### Condition Assessment

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E14_Condition_Assessment` · `crm:E14_Condition_Assessment`

Event of evaluating the physical state of a heritage object or structure

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity) |
| Used in | in range of [Condition assessments](object-properties.md#condition_assessments); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container) |
| prov_alignment_note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Condition State

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E3_Condition_State` · `crm:E3_Condition_State`

A physical condition state of a heritage object

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Used in | in range of [Condition states](object-properties.md#condition_states); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container) |

### Condition Type

**IRI:** `https://cair-nepal.org/heritagegraph/ConditionType` · `heritageGraph:ConditionType`

Controlled vocabulary for the physical condition of heritage objects and structures.

| | |
|---|---|
| Instances | [Damaged](concepts.md#damaged), [Good](concepts.md#good), [Restored](concepts.md#restored), [Ruined](concepts.md#ruined) |
| Used in | in range of [Has condition type](object-properties.md#hasconditiontype) |
| permissible_values | Ruined; Restored; Good; Damaged |

### Consecration

**IRI:** `https://cair-nepal.org/heritagegraph/Consecration` · `heritageGraph:Consecration`

Ritual event that transforms an object into a sacred vessel (e.g., Prana Pratistha for Murti)

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity) |
| Restrictions | [Took place at](object-properties.md#p7_took_place_at) *min* `0`; [Consecrated object](object-properties.md#p16_used_specific_object) *max* `1`; [Took place at](object-properties.md#p7_took_place_at) *max* `1`; [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [Carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Consecrated object](object-properties.md#p16_used_specific_object) *min* `0`; [Carried out by](object-properties.md#p14_carried_out_by) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *min* `0`; [Makes deity present](object-properties.md#makesdeitypresent) *only* [Deity](classes.md#deity); [Consecrated object](object-properties.md#p16_used_specific_object) *only* [Murti](classes.md#murti); [Makes deity present](object-properties.md#makesdeitypresent) *max* `1`; [Took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [Makes deity present](object-properties.md#makesdeitypresent) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *max* `1` |
| Used in | in range of [Consecrated by event](object-properties.md#consecratedbyevent); in range of [Consecration events](object-properties.md#consecration_events); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Murti](classes.md#murti) |
| prov alignment note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Container

**IRI:** `https://cair-nepal.org/heritagegraph/Container` · `heritageGraph:Container`

Root container for cultural heritage data instances. PLACEMENT RULE: put each instance in the most specific collection available (e.g. a Festival in festivals, not ritual_events; a Person in persons, not actors); broader collections exist for instances of the general classes only.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Ritual events](object-properties.md#ritual_events) *min* `0`; [Human made objects](object-properties.md#human_made_objects) *only* [Human Made Object](classes.md#e22_human-made_object); [Architectural elements](object-properties.md#architectural_elements) *min* `0`; [Religious traditions](object-properties.md#religious_traditions) *only* [Religious Tradition](classes.md#religioustradition); [Kumari roles](object-properties.md#kumari_roles) *min* `0`; [techniques](object-properties.md#techniques) *only* [Technique](classes.md#e29_design_or_procedure); [Selection criteria](object-properties.md#selection_criteria) *only* [Selection Criterion](classes.md#selectioncriterion); [assertions](object-properties.md#assertions) *min* `0`; [festivals](object-properties.md#festivals) *min* `0`; [Documentation activities](object-properties.md#documentation_activities) *min* `0`; [persons](object-properties.md#persons) *only* [Person](classes.md#e21_person); [Caste groups](object-properties.md#caste_groups) *only* [Caste Group](classes.md#castegroup); [Physical heritage things](object-properties.md#physical_heritage_things) *min* `0`; [Condition assessments](object-properties.md#condition_assessments) *only* [Condition Assessment](classes.md#e14_condition_assessment); [propositions](object-properties.md#propositions) *min* `0`; [Syncretic relationships](object-properties.md#syncretic_relationships) *only* [Syncretic Relationship](classes.md#syncreticrelationship); [Human made objects](object-properties.md#human_made_objects) *min* `0`; [Kumari lifecycle events](object-properties.md#kumari_lifecycle_events) *min* `0`; [places](object-properties.md#places) *only* [Place](classes.md#e53_place); [Kumari tenures](object-properties.md#kumari_tenures) *only* [Kumari Tenure](classes.md#kumaritenure); [materials](object-properties.md#materials) *only* [Material](classes.md#e57_material); [Architectural elements](object-properties.md#architectural_elements) *only* [Architectural Element](classes.md#architecturalelement); [assertions](object-properties.md#assertions) *only* [Assertion](classes.md#i2_belief); [Consecration events](object-properties.md#consecration_events) *only* [Consecration](classes.md#consecration); [Caste groups](object-properties.md#caste_groups) *min* `0`; [Kumari roles](object-properties.md#kumari_roles) *only* [Kumari Role](classes.md#kumarirole); [Calendar systems](object-properties.md#calendar_systems) *only* [Calendar System](classes.md#calendarsystem); [guthis](object-properties.md#guthis) *only* [Guthi](classes.md#guthi); [actors](object-properties.md#actors) *min* `0`; [Enshrinement events](object-properties.md#enshrinement_events) *min* `0`; [Data sources](object-properties.md#data_sources) *only* [Data Source](classes.md#datasource); [Data sources](object-properties.md#data_sources) *min* `0`; [Kumari lifecycle events](object-properties.md#kumari_lifecycle_events) *only* [Kumari Lifecycle Event](classes.md#kumarilifecycleevent); [materials](object-properties.md#materials) *min* `0`; [Iconographic objects](object-properties.md#iconographic_objects) *min* `0`; [Iconographic objects](object-properties.md#iconographic_objects) *only* [Iconographic Object](classes.md#iconographicobject); [Condition assessments](object-properties.md#condition_assessments) *min* `0`; [Enshrinement events](object-properties.md#enshrinement_events) *only* [Enshrinement](classes.md#enshrinement); [Calendar systems](object-properties.md#calendar_systems) *min* `0`; [actors](object-properties.md#actors) *only* [Actor](classes.md#e39_actor); [Religious traditions](object-properties.md#religious_traditions) *min* `0`; [Documentation activities](object-properties.md#documentation_activities) *only* [Documentation Activity](classes.md#documentationactivity); [Historical events](object-properties.md#historical_events) *min* `0`; [techniques](object-properties.md#techniques) *min* `0`; [Selection criteria](object-properties.md#selection_criteria) *min* `0`; [Ritual assessments](object-properties.md#ritual_assessments) *only* [Ritual Assessment](classes.md#ritualassessment); [Time spans](object-properties.md#time_spans) *only* [Time Span](classes.md#e52_time-span); [Data custodians](object-properties.md#data_custodians) *only* [Data Custodian](classes.md#datacustodian); [deities](object-properties.md#deities) *min* `0`; [Production events](object-properties.md#production_events) *only* [Production](classes.md#e12_production); [Ritual assessments](object-properties.md#ritual_assessments) *min* `0`; [guthis](object-properties.md#guthis) *min* `0`; [Information objects](object-properties.md#information_objects) *only* [Information Object](classes.md#informationobject); [persons](object-properties.md#persons) *min* `0`; [Custody events](object-properties.md#custody_events) *min* `0`; [Information objects](object-properties.md#information_objects) *min* `0`; [places](object-properties.md#places) *min* `0`; [Kumari tenures](object-properties.md#kumari_tenures) *min* `0`; [has metadata](object-properties.md#metadata-2) *max* `1`; [has metadata](object-properties.md#metadata-2) *min* `0`; [Condition states](object-properties.md#condition_states) *only* [Condition State](classes.md#e3_condition_state); [Consecration events](object-properties.md#consecration_events) *min* `0`; [Production events](object-properties.md#production_events) *min* `0`; [Ritual events](object-properties.md#ritual_events) *only* [Ritual Event](classes.md#ritualevent); [Time spans](object-properties.md#time_spans) *min* `0`; [propositions](object-properties.md#propositions) *only* [Proposition](classes.md#proposition); [Data custodians](object-properties.md#data_custodians) *min* `0`; [structures](object-properties.md#structures) *only* [Architectural Structure](classes.md#architecturalstructure); [has metadata](object-properties.md#metadata-2) *only* [Metadata](classes.md#metadata); [Historical events](object-properties.md#historical_events) *only* [Historical Event](classes.md#historicalevent); [festivals](object-properties.md#festivals) *only* [Festival](classes.md#festival); [structures](object-properties.md#structures) *min* `0`; [Condition states](object-properties.md#condition_states) *min* `0`; [Custody events](object-properties.md#custody_events) *only* [Transfer Of Custody](classes.md#e10_transfer_of_custody); [deities](object-properties.md#deities) *only* [Deity](classes.md#deity); [Syncretic relationships](object-properties.md#syncretic_relationships) *min* `0`; [Physical heritage things](object-properties.md#physical_heritage_things) *only* [Physical Heritage Thing](classes.md#physicalheritagething) |
| design note | Serialization construct, not a domain class: this is the LinkML tree_root that anchors JSON/YAML dataset serializations (its collection properties exist for data exchange only). Reasoners and domain queries should ignore it; RDF instance data does not need a Container node. |

### Data Custodian

**IRI:** `https://cair-nepal.org/heritagegraph/DataCustodian` · `heritageGraph:DataCustodian`

Institution or person currently responsible for stewarding heritage data.

| | |
|---|---|
| Superclasses | [Actor](classes.md#e39_actor) |
| Restrictions | [Custodian type](datatype-properties.md#custodiantype) *max* `1`; [note](datatype-properties.md#p3_has_note) *max* `1`; [Custodian type](datatype-properties.md#custodiantype) *min* `0`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Custodian type](datatype-properties.md#custodiantype) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [note](datatype-properties.md#p3_has_note) *min* `0` |
| Used in | in range of [Data custodians](object-properties.md#data_custodians); used in axioms of [Container](classes.md#container) |

### Data Source

**IRI:** `https://cair-nepal.org/heritagegraph/DataSource` · `heritageGraph:DataSource`

Original source from which heritage information was derived

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Datacite identifier type](datatype-properties.md#identifierscheme) *max* `1`; [Source language](datatype-properties.md#inlanguage) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Datacite publisher](object-properties.md#sourcepublisher) *only* [Actor](classes.md#e39_actor); [Datacite publisher](object-properties.md#sourcepublisher) *min* `0`; [note](datatype-properties.md#p3_has_note) *min* `0`; [Source language](datatype-properties.md#inlanguage) *min* `0`; [Publication timespan](object-properties.md#publicationtimespan) *max* `1`; [Datacite creator](object-properties.md#sourcecreator) *only* [Actor](classes.md#e39_actor); [Source citation](datatype-properties.md#sourcecitation) *min* `0`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Publication timespan](object-properties.md#publicationtimespan) *min* `0`; [Datacite resource type](datatype-properties.md#resourcetype) *min* `0`; [Datacite creator](object-properties.md#sourcecreator) *min* `0`; [Source url](datatype-properties.md#sourceurl) *max* `1`; [Datacite identifier type](datatype-properties.md#identifierscheme) *min* `0`; [note](datatype-properties.md#p3_has_note) *max* `1`; [Datacite resource type](datatype-properties.md#resourcetype) *max* `1`; [Datacite resource type](datatype-properties.md#resourcetype) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Datacite identifier](datatype-properties.md#persistentidentifier) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Datacite identifier type](datatype-properties.md#identifierscheme) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Datacite identifier](datatype-properties.md#persistentidentifier) *max* `1`; [Source citation](datatype-properties.md#sourcecitation) *max* `1`; [Source language](datatype-properties.md#inlanguage) *max* `1`; [Source url](datatype-properties.md#sourceurl) *min* `0`; [Publication timespan](object-properties.md#publicationtimespan) *only* [Time Span](classes.md#e52_time-span); [Datacite publisher](object-properties.md#sourcepublisher) *max* `1`; [Source citation](datatype-properties.md#sourcecitation) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Source url](datatype-properties.md#sourceurl) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Datacite identifier](datatype-properties.md#persistentidentifier) *min* `0` |
| Subclasses | [Archival Record](classes.md#archivalrecord), [Field Survey Dataset](classes.md#fieldsurveydataset), [Information Object](classes.md#informationobject), [Oral History Recording](classes.md#oralhistoryrecording) |
| Used in | in range of [Data sources](object-properties.md#data_sources); in range of [Documented in source](object-properties.md#mentionedinsource); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### Date Precision

**IRI:** `https://cair-nepal.org/heritagegraph/DatePrecision` · `heritageGraph:DatePrecision`

Controlled vocabulary for the temporal precision of recorded heritage dates.

| | |
|---|---|
| Instances | [Century](concepts.md#century), [Circa](concepts.md#circa), [Decade](concepts.md#decade), [Exact](concepts.md#exact), [Year](concepts.md#year) |
| Used in | in range of [has date precision](object-properties.md#dateprecision) |
| permissible_values | Circa; Decade; Year; Century; Exact |

### Deity

**IRI:** `https://cair-nepal.org/heritagegraph/Deity` · `heritageGraph:Deity`

Divine conceptual entity in Hindu, Buddhist, or syncretic traditions. Distinct from physical representations (Murti) and ritual presences.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Is depicted in](object-properties.md#p62i_is_depicted_by) *only* [Iconographic Object](classes.md#iconographicobject); [note](datatype-properties.md#p3_has_note) *max* `1`; [Has religious tradition](object-properties.md#hasreligioustradition) *only* [Religious Tradition](classes.md#religioustradition); [Is invoked in ritual](object-properties.md#isinvokedinritual) *only* [Ritual Event](classes.md#ritualevent); [note](datatype-properties.md#p3_has_note) *min* `0`; [Is depicted in](object-properties.md#p62i_is_depicted_by) *min* `0`; [Has religious tradition](object-properties.md#hasreligioustradition) *min* `0`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Is enshrined through event](object-properties.md#isenshrinedthroughevent) *min* `0`; [Is invoked in ritual](object-properties.md#isinvokedinritual) *min* `0`; [Is enshrined through event](object-properties.md#isenshrinedthroughevent) *only* [Enshrinement](classes.md#enshrinement) |
| Used in | in range of [deities](object-properties.md#deities); in range of [Embodied deity](object-properties.md#embodieddeity); in range of [Enshrined deity](object-properties.md#enshrineddeity); in range of [Invokes deity](object-properties.md#invokesdeity); in range of [Is about deity](object-properties.md#isaboutdeity); in range of [Makes deity present](object-properties.md#makesdeitypresent); in range of [Role deity](object-properties.md#roledeity); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Consecration](classes.md#consecration); used in axioms of [Container](classes.md#container); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Iconographic Object](classes.md#iconographicobject); used in axioms of [Kumari Role](classes.md#kumarirole); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Murti](classes.md#murti); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### Destruction Event

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E6_Destruction` · `crm:E6_Destruction`

Event that destroyed or damaged a structure.

| | |
|---|---|
| Used in | in range of [has destruction event](object-properties.md#destructionevent); used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### Dharmashala

**IRI:** `https://cair-nepal.org/heritagegraph/Dharmashala` · `heritageGraph:Dharmashala`

Pilgrim lodge operated by a Guthi organization

| | |
|---|---|
| Superclasses | [Rest House](classes.md#resthouse) |

### Dhunge Dhara

**IRI:** `https://cair-nepal.org/heritagegraph/DhungeDhara` · `heritageGraph:DhungeDhara`

Stone spout (hiti) with carved imagery, used for ritual bathing and daily water supply

| | |
|---|---|
| Superclasses | [Water Structure](classes.md#waterstructure) |

### Documentation Activity

**IRI:** `https://cair-nepal.org/heritagegraph/DocumentationActivity` · `heritageGraph:DocumentationActivity`

Activity that records information about a heritage entity or event and may generate information objects or assertions. It aligns CIDOC CRM documentation practices with prov:Activity.

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity) |
| Restrictions | [Used method](datatype-properties.md#usedmethod) *max* `1`; [Has timespan](object-properties.md#p4_has_time-span) *min* `0`; [Used equipment](datatype-properties.md#usedequipment) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *max* `1`; [Used method](datatype-properties.md#usedmethod) *min* `0`; [Was associated with](object-properties.md#wasassociatedwith) *min* `0`; [documents](object-properties.md#documents) *min* `0`; [generated](object-properties.md#generated) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [documents](object-properties.md#documents) *only* [Assertion Subject](classes.md#assertionsubject); [Used equipment](datatype-properties.md#usedequipment) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Was associated with](object-properties.md#wasassociatedwith) *only* [Agent](classes.md#agent); [generated](object-properties.md#generated) *only* [Entity](classes.md#entity); [Used method](datatype-properties.md#usedmethod) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Subclasses | [Field Survey Activity](classes.md#fieldsurveyactivity), [Oral History Interview](classes.md#oralhistoryinterview), [Verification](classes.md#verification) |
| Used in | in range of [Documentation activities](object-properties.md#documentation_activities); in range of [Was documented by](object-properties.md#documentedby); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Information Object](classes.md#informationobject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |
| prov_alignment_note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Enshrinement

**IRI:** `https://cair-nepal.org/heritagegraph/Enshrinement` · `heritageGraph:Enshrinement`

Event of installing a deity's murti or symbol within a temple sanctum

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity) |
| Restrictions | [Has timespan](object-properties.md#p4_has_time-span) *min* `0`; [Enshrined in structure](object-properties.md#enshrinedinstructure) *min* `0`; [Enshrined deity](object-properties.md#enshrineddeity) *max* `1`; [Took place at](object-properties.md#p7_took_place_at) *min* `0`; [Enshrined deity](object-properties.md#enshrineddeity) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [Has timespan](object-properties.md#p4_has_time-span) *max* `1`; [Enshrined deity](object-properties.md#enshrineddeity) *only* [Deity](classes.md#deity); [Took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [Took place at](object-properties.md#p7_took_place_at) *max* `1`; [Carried out by](object-properties.md#p14_carried_out_by) *min* `0`; [Enshrined in structure](object-properties.md#enshrinedinstructure) *max* `1`; [Carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Enshrined in structure](object-properties.md#enshrinedinstructure) *only* [Temple](classes.md#temple) |
| Used in | in range of [Enshrinement events](object-properties.md#enshrinement_events); in range of [Enshrines deity through event](object-properties.md#enshrinesdeitythroughevent); in range of [Is enshrined through event](object-properties.md#isenshrinedthroughevent); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Deity](classes.md#deity); used in axioms of [Temple](classes.md#temple) |
| prov alignment note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Entity

**IRI:** `http://www.w3.org/ns/prov#Entity` · `prov:Entity`

Direct LinkML representation of prov:Entity. Applied to physical, digital, conceptual, and assertion-bearing things that participate in provenance relations. PROVENANCE SCOPE (design decision): for classes whose instances are real-world referents (structures, deities, places, actors), the provenance slots (was_derived_from, was_attributed_to, was_generated_by, generated_at_time) describe the DATA RECORD about the referent, not the referent itself -- a stupa is not generated by the survey that records it. Referent-level history is modelled through events (Production, DestructionEvent, etc.). RDF deployments SHOULD carry record-level provenance in named graphs or on InformationObject/Assertion nodes.

| | |
|---|---|
| Subclasses | [Architectural Element](classes.md#architecturalelement), [Assertion](classes.md#i2_belief), [Calendar System](classes.md#calendarsystem), [Condition State](classes.md#e3_condition_state), [Container](classes.md#container), [Data Source](classes.md#datasource), [Deity](classes.md#deity), [Human Made Object](classes.md#e22_human-made_object), [Kumari Role](classes.md#kumarirole), [Kumari Tenure](classes.md#kumaritenure), [Material](classes.md#e57_material), [Metadata](classes.md#metadata), [Physical Heritage Thing](classes.md#physicalheritagething), [Place](classes.md#e53_place), [Proposition](classes.md#proposition), [Religious Tradition](classes.md#religioustradition), [Selection Criterion](classes.md#selectioncriterion), [Technique](classes.md#e29_design_or_procedure), [Time Span](classes.md#e52_time-span) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |
| provenance scope | record |

### Existence Status

**IRI:** `https://cair-nepal.org/heritagegraph/ExistenceStatus` · `heritageGraph:ExistenceStatus`

Controlled vocabulary for whether a heritage structure still exists physically.

| | |
|---|---|
| Instances | [Destroyed](concepts.md#destroyed), [Extant](concepts.md#extant), [Hypothetical](concepts.md#hypothetical), [Lost](concepts.md#lost), [Partially Extant](concepts.md#partiallyextant), [Unknown](concepts.md#unknown) |
| Used in | in range of [has existence status](object-properties.md#existencestatus); used in axioms of [Architectural Structure](classes.md#architecturalstructure) |
| permissible_values | Lost; Hypothetical; PartiallyExtant; Unknown; Destroyed; Extant |

### Fearlessness Assessment

**IRI:** `https://cair-nepal.org/heritagegraph/FearlessnessAssessment` · `heritageGraph:FearlessnessAssessment`

The 'fearlessness test' popularly described (animal heads, masked dancers in darkness). Its historical and contemporary practice is DISPUTED -- some former Kumaris contest how it is described. Represented as an assessment whose accounts are source-attributed via has_assertion, NOT as a mandatory criterion.

| | |
|---|---|
| Superclasses | [Ritual Assessment](classes.md#ritualassessment) |

### Festival

**IRI:** `https://cair-nepal.org/heritagegraph/Festival` · `heritageGraph:Festival`

Large-scale community ritual event (Jatra) involving processions, music, and collective participation

| | |
|---|---|
| Superclasses | [Ritual Event](classes.md#ritualevent) |
| Restrictions | [Includes ritual event](object-properties.md#p9_consists_of) *only* [Ritual Event](classes.md#ritualevent); [Includes ritual event](object-properties.md#p9_consists_of) *min* `0` |
| Subclasses | [Chariot Festival](classes.md#chariotfestival), [Masked Dance](classes.md#maskeddance) |
| Used in | in range of [festivals](object-properties.md#festivals); used in axioms of [Container](classes.md#container); used in axioms of [Ritual Event](classes.md#ritualevent) |
| prov_alignment_note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Field Survey Activity

**IRI:** `https://cair-nepal.org/heritagegraph/FieldSurveyActivity` · `heritageGraph:FieldSurveyActivity`

The activity of measuring, photographing, or assessing a site in person.

| | |
|---|---|
| Superclasses | [Documentation Activity](classes.md#documentationactivity) |

### Field Survey Dataset

**IRI:** `https://cair-nepal.org/heritagegraph/FieldSurveyDataset` · `heritageGraph:FieldSurveyDataset`

The structured data or report resulting from a field survey.

| | |
|---|---|
| Superclasses | [Data Source](classes.md#datasource) |

### Guthi

**IRI:** `https://cair-nepal.org/heritagegraph/Guthi` · `heritageGraph:Guthi`

Endowed trust organization unique to Nepal, managing temples, rituals, and land through hereditary or voluntary membership

| | |
|---|---|
| Superclasses | [Actor](classes.md#e39_actor) |
| Restrictions | [note](datatype-properties.md#p3_has_note) *min* `0`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Holds custody of](object-properties.md#p50i_is_current_keeper_of) *min* `0`; [Performs ritual](object-properties.md#performsritual) *min* `0`; [Has membership](object-properties.md#p107_has_current_or_former_member) *min* `0`; [Holds custody of](object-properties.md#p50i_is_current_keeper_of) *only* [Architectural Structure](classes.md#architecturalstructure); [note](datatype-properties.md#p3_has_note) *max* `1`; [has guthi type](object-properties.md#guthitype) *max* `1`; [Has membership](object-properties.md#p107_has_current_or_former_member) *only* [Person](classes.md#e21_person); [has guthi type](object-properties.md#guthitype) *min* `0`; [Performs ritual](object-properties.md#performsritual) *only* [Ritual Event](classes.md#ritualevent); [has guthi type](object-properties.md#guthitype) *only* [Guthi Type](classes.md#guthitype-2) |
| Used in | in range of [guthis](object-properties.md#guthis); in range of [Managed by guthi](object-properties.md#managedbyguthi); in range of [Performed by group](object-properties.md#performedbygroup); in range of [Supported by institution](object-properties.md#supportedbyinstitution); in range of [Transferred to guthi](object-properties.md#transferredtoguthi); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Container](classes.md#container); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Guthi Type

**IRI:** `https://cair-nepal.org/heritagegraph/GuthiType` · `heritageGraph:GuthiType`

Controlled vocabulary of Guthi functional types (CRM E55_Type)

| | |
|---|---|
| Instances | [Jatra Guthi](concepts.md#jatraguthi), [Nasha Guthi](concepts.md#nashaguthi), [Puja Guthi](concepts.md#pujaguthi), [Raj Guthi](concepts.md#rajguthi), [San Guthi](concepts.md#sanguthi), [Sana Guthi](concepts.md#sanaguthi), [Si Guthi](concepts.md#siguthi), [Temple Guthi](concepts.md#templeguthi) |
| Used in | in range of [has guthi type](object-properties.md#guthitype); used in axioms of [Guthi](classes.md#guthi) |
| permissible_values | SanGuthi; NashaGuthi; Puja Guthi; Raj Guthi; Sana Guthi; Temple Guthi; JatraGuthi; Si Guthi |

### Historical Event

**IRI:** `https://cair-nepal.org/heritagegraph/HistoricalEvent` · `heritageGraph:HistoricalEvent`

Major event affecting heritage structures or ritual life (earthquake, epidemic, political transition, fire, flood).

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity) |
| Restrictions | [note](datatype-properties.md#p3_has_note) *min* `0`; [Includes ritual event](object-properties.md#p9_consists_of) *only* [Ritual Event](classes.md#ritualevent); [Took place at](object-properties.md#p7_took_place_at) *min* `0`; [Took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [Has timespan](object-properties.md#p4_has_time-span) *min* `0`; [Architectural structures](object-properties.md#architecturalstructures) *only* [Architectural Structure](classes.md#architecturalstructure); [note](datatype-properties.md#p3_has_note) *max* `1`; [Architectural structures](object-properties.md#architecturalstructures) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Includes ritual event](object-properties.md#p9_consists_of) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *max* `1`; [Took place at](object-properties.md#p7_took_place_at) *max* `1` |
| Used in | in range of [Historical events](object-properties.md#historical_events); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container) |
| prov_alignment_note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Horoscope Compatibility Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/HoroscopeCompatibilityCriterion` · `heritageGraph:HoroscopeCompatibilityCriterion`

Candidate's horoscope must be compatible with the city and ruling authority.

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Human Made Object

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E22_Human-Made_Object` · `crm:E22_Human-Made_Object`

Physical objects created by human activity

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Subclasses | [Architectural Structure](classes.md#architecturalstructure), [Iconographic Object](classes.md#iconographicobject) |
| Used in | in range of [Human made objects](object-properties.md#human_made_objects); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container) |

### Iconographic Object

**IRI:** `https://cair-nepal.org/heritagegraph/IconographicObject` · `heritageGraph:IconographicObject`

Sacred visual art objects that depict or embody deities through iconographic conventions

| | |
|---|---|
| Superclasses | [Human Made Object](classes.md#e22_human-made_object) |
| Restrictions | [Depicts deity](object-properties.md#p62_depicts) *only* [Deity](classes.md#deity); [Has current location](object-properties.md#p55_has_current_location) *max* `1`; [Used by](object-properties.md#usedby) *min* `0`; [Was produced by event](object-properties.md#p108i_was_produced_by) *max* `1`; [Was produced by event](object-properties.md#p108i_was_produced_by) *only* [Production](classes.md#e12_production); [note](datatype-properties.md#p3_has_note) *max* `1`; [Has current location](object-properties.md#p55_has_current_location) *min* `0`; [Used by](object-properties.md#usedby) *only* [Actor](classes.md#e39_actor); [note](datatype-properties.md#p3_has_note) *min* `0`; [Has current location](object-properties.md#p55_has_current_location) *only* [Place](classes.md#e53_place); [Participates in ritual](object-properties.md#participatesinritual) *min* `0`; [Was produced by event](object-properties.md#p108i_was_produced_by) *min* `0`; [Participates in ritual](object-properties.md#participatesinritual) *only* [Ritual Event](classes.md#ritualevent); [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Depicts deity](object-properties.md#p62_depicts) *min* `0` |
| Subclasses | [Murti](classes.md#murti), [Paubha](classes.md#paubha) |
| Used in | in range of [Iconographic objects](object-properties.md#iconographic_objects); used in axioms of [Container](classes.md#container); used in axioms of [Deity](classes.md#deity); used in axioms of [Physical Heritage Thing](classes.md#physicalheritagething) |

### Information Object

**IRI:** `https://cair-nepal.org/heritagegraph/InformationObject` · `heritageGraph:InformationObject`

A recorded piece of information about heritage

| | |
|---|---|
| Superclasses | [Data Source](classes.md#datasource) |
| Restrictions | [Was generated by](object-properties.md#wasgeneratedby) *min* `0`; [Was documented by](object-properties.md#documentedby) *min* `0`; [Is about](object-properties.md#p129_is_about) *min* `0`; [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [Source language](datatype-properties.md#inlanguage) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Was generated by](object-properties.md#wasgeneratedby) *max* `1`; [Was generated by](object-properties.md#wasgeneratedby) *only* [Activity](classes.md#activity); [Source language](datatype-properties.md#inlanguage) *min* `0`; [Source language](datatype-properties.md#inlanguage) *max* `1`; [Is about](object-properties.md#p129_is_about) *only* [Assertion Subject](classes.md#assertionsubject) |
| Used in | in range of [Information objects](object-properties.md#information_objects); used in axioms of [Container](classes.md#container) |

### Kumari Enthronement Event

**IRI:** `https://cair-nepal.org/heritagegraph/KumariEnthronementEvent` · `heritageGraph:KumariEnthronementEvent`

Ritual installing a selected girl into the Kumari role and residence, activating the tenure (distinct from selection, which chooses her, and retirement, which ends it).

| | |
|---|---|
| Superclasses | [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |
| Restrictions | [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [Confers role](object-properties.md#confersrole) *min* `1`; [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [Took place at](object-properties.md#p7_took_place_at) *min* `0`; [Enthroned person](object-properties.md#enthronedperson) *only* [Person](classes.md#e21_person); [Bounds tenure](object-properties.md#boundstenure) *max* `1`; [Enthroned person](object-properties.md#enthronedperson) *max* `1`; [Bounds tenure](object-properties.md#boundstenure) *min* `1`; [Has timespan](object-properties.md#p4_has_time-span) *max* `1`; [Has timespan](object-properties.md#p4_has_time-span) *min* `0`; [Took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [Enthroned person](object-properties.md#enthronedperson) *min* `1`; [Has assertion](object-properties.md#hasassertion) *only* [Assertion](classes.md#i2_belief); [Has assertion](object-properties.md#hasassertion) *min* `0`; [Carried out by](object-properties.md#p14_carried_out_by) *min* `0`; [Was documented by](object-properties.md#documentedby) *min* `0`; [Confers role](object-properties.md#confersrole) *max* `1`; [Confers role](object-properties.md#confersrole) *only* [Kumari Role](classes.md#kumarirole); [Bounds tenure](object-properties.md#boundstenure) *only* [Kumari Tenure](classes.md#kumaritenure); [Carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Took place at](object-properties.md#p7_took_place_at) *max* `1` |
| Used in | in range of [Enthroned through](object-properties.md#enthronedthrough); used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Kumari House

**IRI:** `https://cair-nepal.org/heritagegraph/KumariHouse` · `heritageGraph:KumariHouse`

God-house residence of a Kumari during tenure (e.g., Kumari Ghar, Kathmandu). Specialised ReligiousStructure.

| | |
|---|---|
| Superclasses | [Religious Structure](classes.md#religiousstructure) |

### Kumari Lifecycle Event

**IRI:** `https://cair-nepal.org/heritagegraph/KumariLifecycleEvent` · `heritageGraph:KumariLifecycleEvent`

Abstract event that bounds a KumariTenure (selection, enthronement, or retirement). Each concrete subclass requires exactly one tenure edge via slot_usage: initiated_tenure (selection), ended_tenure_of (retirement), or bounds_tenure itself (enthronement).

| | |
|---|---|
| Superclasses | [Ritual Event](classes.md#ritualevent) |
| Restrictions | [Bounds tenure](object-properties.md#boundstenure) *max* `1`; [Bounds tenure](object-properties.md#boundstenure) *only* [Kumari Tenure](classes.md#kumaritenure); [Bounds tenure](object-properties.md#boundstenure) *min* `0` |
| Subclasses | [Kumari Enthronement Event](classes.md#kumarienthronementevent), [Kumari Retirement Event](classes.md#kumariretirementevent), [Kumari Selection Event](classes.md#kumariselectionevent) |
| Used in | in range of [Kumari lifecycle events](object-properties.md#kumari_lifecycle_events); used in axioms of [Container](classes.md#container) |

### Kumari Retirement Event

**IRI:** `https://cair-nepal.org/heritagegraph/KumariRetirementEvent` · `heritageGraph:KumariRetirementEvent`

Ritual or administrative event that formally ends a Living Goddess tenure, returning the person to secular status. Common triggers: first menstruation, injury causing blood loss, serious illness.

| | |
|---|---|
| Superclasses | [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |
| Restrictions | [note](datatype-properties.md#p3_has_note) *max* `1`; [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [Carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Has assertion](object-properties.md#hasassertion) *only* [Assertion](classes.md#i2_belief); [Took place at](object-properties.md#p7_took_place_at) *max* `1`; [Ended tenure of](object-properties.md#endedtenureof) *max* `1`; [Took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Ended tenure of](object-properties.md#endedtenureof) *only* [Kumari Tenure](classes.md#kumaritenure); [Took place at](object-properties.md#p7_took_place_at) *min* `0`; [Carried out by](object-properties.md#p14_carried_out_by) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *max* `1`; [Performed by group](object-properties.md#performedbygroup) *min* `0`; [Performed by group](object-properties.md#performedbygroup) *only* (([Guthi](classes.md#guthi) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor)); [note](datatype-properties.md#p3_has_note) *min* `0`; [Was documented by](object-properties.md#documentedby) *min* `0`; [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [Has assertion](object-properties.md#hasassertion) *min* `0`; [Ended tenure of](object-properties.md#endedtenureof) *min* `1`; [Has timespan](object-properties.md#p4_has_time-span) *min* `1` |
| Used in | in range of [Retired through](object-properties.md#retiredthrough); used in axioms of [Kumari Tenure](classes.md#kumaritenure) |
| prov_alignment_note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Kumari Role

**IRI:** `https://cair-nepal.org/heritagegraph/KumariRole` · `heritageGraph:KumariRole`

The role/office of Kumari (living-goddess embodiment) that a person assumes for the duration of a KumariTenure. The role is the type; the tenure is the time-bounded holding of it; the person is the holder.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Role deity](object-properties.md#roledeity) *max* `1`; [Role deity](object-properties.md#roledeity) *only* [Deity](classes.md#deity); [Role deity](object-properties.md#roledeity) *min* `0` |
| Used in | in range of [Assumes role](object-properties.md#assumesrole); in range of [Confers role](object-properties.md#confersrole); in range of [Kumari roles](object-properties.md#kumari_roles); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Kumari Selection Event

**IRI:** `https://cair-nepal.org/heritagegraph/KumariSelectionEvent` · `heritageGraph:KumariSelectionEvent`

Tantric ritual process of selecting a new Living Goddess from eligible candidates. Involves examination of 32 auspicious physical marks (lakshana), horoscope matching with the city and ruling authority, and tests of fearlessness (e.g., remaining calm among buffalo heads and masked dancers in darkness). Performed by committee of Vajracharya priests, royal priest (Raj Jyotish), and astrologer.

| | |
|---|---|
| Superclasses | [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |
| Restrictions | [Has criterion](object-properties.md#hascriterion) *min* `0`; [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [Has assertion](object-properties.md#hasassertion) *only* [Assertion](classes.md#i2_belief); [Took place at](object-properties.md#p7_took_place_at) *min* `0`; [Selected person](object-properties.md#selectedperson) *only* [Person](classes.md#e21_person); [Initiated tenure](object-properties.md#initiatedtenure) *max* `1`; [Confers role](object-properties.md#confersrole) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *min* `0`; [Initiated tenure](object-properties.md#initiatedtenure) *only* [Kumari Tenure](classes.md#kumaritenure); [Is critical for festival](datatype-properties.md#iscriticalforfestival) *max* `1`; [Carried out by](object-properties.md#p14_carried_out_by) *min* `0`; [Was documented by](object-properties.md#documentedby) *min* `0`; [Confers role](object-properties.md#confersrole) *only* [Kumari Role](classes.md#kumarirole); [Performed by group](object-properties.md#performedbygroup) *only* (([Guthi](classes.md#guthi) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor)); [Took place at](object-properties.md#p7_took_place_at) *max* `1`; [Has criterion](object-properties.md#hascriterion) *only* [Selection Criterion](classes.md#selectioncriterion); [Performed by group](object-properties.md#performedbygroup) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *max* `1`; [Selected person](object-properties.md#selectedperson) *max* `1`; [Has assertion](object-properties.md#hasassertion) *min* `0`; [Carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Confers role](object-properties.md#confersrole) *max* `1`; [Is critical for festival](datatype-properties.md#iscriticalforfestival) *only* [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean); [Selected person](object-properties.md#selectedperson) *min* `1`; [Initiated tenure](object-properties.md#initiatedtenure) *min* `1`; [Is critical for festival](datatype-properties.md#iscriticalforfestival) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [Took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place) |
| Used in | in range of [Part of selection](object-properties.md#partofselection); in range of [Selected through](object-properties.md#selectedthrough); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment) |
| prov_alignment_note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Kumari Tenure

**IRI:** `https://cair-nepal.org/heritagegraph/KumariTenure` · `heritageGraph:KumariTenure`

Time-bounded role where a person embodies a deity as Living Goddess (Kumari), residing at a specific god-house and supported by religious institutions. This class captures the unique Nepali tradition of living deity embodiment in young girls selected from Buddhist Shakya/Vajracharya families.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Selected through](object-properties.md#selectedthrough) *min* `0`; [Selected through](object-properties.md#selectedthrough) *only* [Kumari Selection Event](classes.md#kumariselectionevent); [Assumes role](object-properties.md#assumesrole) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [Embodied deity](object-properties.md#embodieddeity) *only* [Deity](classes.md#deity); [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [Retired through](object-properties.md#retiredthrough) *min* `0`; [Enthroned through](object-properties.md#enthronedthrough) *min* `0`; [Assumes role](object-properties.md#assumesrole) *only* [Kumari Role](classes.md#kumarirole); [Has timespan](object-properties.md#p4_has_time-span) *max* `1`; [Has timespan](object-properties.md#p4_has_time-span) *min* `1`; [Embodied deity](object-properties.md#embodieddeity) *min* `1`; [Embodied deity](object-properties.md#embodieddeity) *max* `1`; [Selected through](object-properties.md#selectedthrough) *max* `1`; [Residence structure](object-properties.md#residencestructure) *max* `1`; [Supported by institution](object-properties.md#supportedbyinstitution) *only* [Guthi](classes.md#guthi); [Assumes role](object-properties.md#assumesrole) *max* `1`; [Residence structure](object-properties.md#residencestructure) *min* `1`; [Residence structure](object-properties.md#residencestructure) *only* [Architectural Structure](classes.md#architecturalstructure); [Supported by institution](object-properties.md#supportedbyinstitution) *min* `0`; [Was documented by](object-properties.md#documentedby) *min* `0`; [Enthroned through](object-properties.md#enthronedthrough) *only* [Kumari Enthronement Event](classes.md#kumarienthronementevent); [Retired through](object-properties.md#retiredthrough) *max* `1`; [Had participant](object-properties.md#hadparticipant) *only* [Person](classes.md#e21_person); [Enthroned through](object-properties.md#enthronedthrough) *max* `1`; [Retired through](object-properties.md#retiredthrough) *only* [Kumari Retirement Event](classes.md#kumariretirementevent); [Had participant](object-properties.md#hadparticipant) *min* `1` |
| Used in | in range of [Bounds tenure](object-properties.md#boundstenure); in range of [Ended tenure of](object-properties.md#endedtenureof); in range of [Initiated tenure](object-properties.md#initiatedtenure); in range of [Kumari tenures](object-properties.md#kumari_tenures); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Lifecycle Event](classes.md#kumarilifecycleevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |

### Lineage Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/LineageCriterion` · `heritageGraph:LineageCriterion`

Candidate must belong to an eligible lineage (Shakya / Vajracharya Newar Buddhist family).

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Masked Dance

**IRI:** `https://cair-nepal.org/heritagegraph/MaskedDance` · `heritageGraph:MaskedDance`

Festival featuring masked dancers embodying deities (e.g., Kartik Naach)

| | |
|---|---|
| Superclasses | [Festival](classes.md#festival) |

### Material

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E57_Material` · `crm:E57_Material`

Physical substance used in construction or crafting

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Used in | in range of [materials](object-properties.md#materials); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Metadata

**IRI:** `https://cair-nepal.org/heritagegraph/Metadata` · `heritageGraph:Metadata`

Dataset metadata information

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Schema version](datatype-properties.md#schema_version) *min* `0`; [license](datatype-properties.md#license-2) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Schema version](datatype-properties.md#schema_version) *max* `1`; [Dataset name](datatype-properties.md#dataset_name) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [license](datatype-properties.md#license-2) *max* `1`; [Dataset version](datatype-properties.md#dataset_version) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [curator](datatype-properties.md#curator) *min* `0`; [Dataset name](datatype-properties.md#dataset_name) *max* `1`; [Generated date](datatype-properties.md#generated_date) *max* `1`; [Generated date](datatype-properties.md#generated_date) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [curator](datatype-properties.md#curator) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Schema version](datatype-properties.md#schema_version) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Dataset version](datatype-properties.md#dataset_version) *min* `0`; [Dataset version](datatype-properties.md#dataset_version) *max* `1`; [Dataset name](datatype-properties.md#dataset_name) *min* `0`; [curator](datatype-properties.md#curator) *max* `1`; [Generated date](datatype-properties.md#generated_date) *min* `0`; [license](datatype-properties.md#license-2) *min* `0` |
| Used in | in range of [has metadata](object-properties.md#metadata-2); used in axioms of [Container](classes.md#container) |

### Murti

**IRI:** `https://cair-nepal.org/heritagegraph/Murti` · `heritageGraph:Murti`

Consecrated statue of a deity, ritually activated to serve as divine presence (not merely depiction)

| | |
|---|---|
| Superclasses | [Iconographic Object](classes.md#iconographicobject) |
| Restrictions | [Consecrated by event](object-properties.md#consecratedbyevent) *min* `0`; [Is about deity](object-properties.md#isaboutdeity) *only* [Deity](classes.md#deity); [Consecrated by event](object-properties.md#consecratedbyevent) *only* [Consecration](classes.md#consecration); [Consecrated by event](object-properties.md#consecratedbyevent) *max* `1`; [Is about deity](object-properties.md#isaboutdeity) *max* `1`; [Is about deity](object-properties.md#isaboutdeity) *min* `0` |
| Used in | used in axioms of [Consecration](classes.md#consecration) |

### Oral History Interview

**IRI:** `https://cair-nepal.org/heritagegraph/OralHistoryInterview` · `heritageGraph:OralHistoryInterview`

The interaction event between a researcher and a knowledge holder.

| | |
|---|---|
| Superclasses | [Documentation Activity](classes.md#documentationactivity) |

### Oral History Recording

**IRI:** `https://cair-nepal.org/heritagegraph/OralHistoryRecording` · `heritageGraph:OralHistoryRecording`

The recording or transcript of an oral history interview.

| | |
|---|---|
| Superclasses | [Data Source](classes.md#datasource) |

### Pati

**IRI:** `https://cair-nepal.org/heritagegraph/Pati` · `heritageGraph:Pati`

Open-air pavilion for resting travelers

| | |
|---|---|
| Superclasses | [Rest House](classes.md#resthouse) |

### Paubha

**IRI:** `https://cair-nepal.org/heritagegraph/Paubha` · `heritageGraph:Paubha`

Traditional Newari scroll painting (thangka) with mandala and deity iconography

| | |
|---|---|
| Superclasses | [Iconographic Object](classes.md#iconographicobject) |

### Person

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E21_Person` · `crm:E21_Person`

Individual person who performs, commissions, documents, or verifies heritage activities

| | |
|---|---|
| Superclasses | [Actor](classes.md#e39_actor) |
| Used in | in range of [Assesses candidate](object-properties.md#assessescandidate); in range of [Enthroned person](object-properties.md#enthronedperson); in range of [persons](object-properties.md#persons); in range of [Selected person](object-properties.md#selectedperson); in range of [Verified by expert](object-properties.md#verifiedbyexpert); used in axioms of [Container](classes.md#container); used in axioms of [Guthi](classes.md#guthi); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Verification](classes.md#verification) |

### Physical Heritage Thing

**IRI:** `https://cair-nepal.org/heritagegraph/PhysicalHeritageThing` · `heritageGraph:PhysicalHeritageThing`

Union of the tangible heritage classes: architectural structures, iconographic objects, and standalone architectural elements. Used as the range of slots that apply to any physical heritage thing (production, custody, condition assessment).

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Equivalent to | [Architectural Structure](classes.md#architecturalstructure) *or* [Iconographic Object](classes.md#iconographicobject) *or* [Architectural Element](classes.md#architecturalelement) |
| Used in | in range of [Physical heritage things](object-properties.md#physical_heritage_things); used in axioms of [Container](classes.md#container); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Physical Integrity Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/PhysicalIntegrityCriterion` · `heritageGraph:PhysicalIntegrityCriterion`

Candidate must have an unblemished body with no scars, wounds, or loss of blood/teeth.

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Place

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E53_Place` · `crm:E53_Place`

Defined geographic location where events occur and structures exist

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Used in | in range of [End place](object-properties.md#endplace); in range of [Hypothesized location](object-properties.md#hypothesizedlocation); in range of [places](object-properties.md#places); in range of [Route places](object-properties.md#routeplaces); in range of [Start place](object-properties.md#startplace); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Consecration](classes.md#consecration); used in axioms of [Container](classes.md#container); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Iconographic Object](classes.md#iconographicobject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Pokhari

**IRI:** `https://cair-nepal.org/heritagegraph/Pokhari` · `heritageGraph:Pokhari`

Pond or tank for water storage, ritual bathing, and ecological management

| | |
|---|---|
| Superclasses | [Water Structure](classes.md#waterstructure) |

### Production

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E12_Production` · `crm:E12_Production`

Event of creating an architectural structure, murti, or paubha

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity) |
| Used in | in range of [Production events](object-properties.md#production_events); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Iconographic Object](classes.md#iconographicobject) |
| prov_alignment_note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Proposition

**IRI:** `https://cair-nepal.org/heritagegraph/Proposition` · `heritageGraph:Proposition`

A single machine-readable proposition (subject - predicate - object) held true by an Assertion. Modelled as a singleton proposition set (CRMinf I4); the predicate is a URI/CURIE, the object either a heritage entity or a literal.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Proposition subject](object-properties.md#propositionsubject) *max* `1`; [Proposition object entity](object-properties.md#propositionobjectentity) *max* `1`; [Proposition subject](object-properties.md#propositionsubject) *min* `1`; [Proposition predicate](datatype-properties.md#propositionpredicate) *only* [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI); [Proposition predicate](datatype-properties.md#propositionpredicate) *max* `1`; [Proposition object literal](datatype-properties.md#propositionliteralvalue) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Proposition object literal](datatype-properties.md#propositionliteralvalue) *max* `1`; [Proposition object literal](datatype-properties.md#propositionliteralvalue) *min* `0`; [Proposition object entity](object-properties.md#propositionobjectentity) *only* [Assertion Subject](classes.md#assertionsubject); [Proposition subject](object-properties.md#propositionsubject) *only* [Assertion Subject](classes.md#assertionsubject); [Proposition object entity](object-properties.md#propositionobjectentity) *min* `0`; [Proposition predicate](datatype-properties.md#propositionpredicate) *min* `1` |
| Used in | in range of [propositions](object-properties.md#propositions); used in axioms of [Container](classes.md#container) |

### Religious Structure

**IRI:** `https://cair-nepal.org/heritagegraph/ReligiousStructure` · `heritageGraph:ReligiousStructure`

Architectural structure whose defining purpose is religious: enshrines a deity and/or is a locus of ritual activation. Abstract grouping for sacred structures across traditions (temple, stupa, chaitya).

| | |
|---|---|
| Superclasses | [Architectural Structure](classes.md#architecturalstructure) |
| Restrictions | [Has religious tradition](object-properties.md#hasreligioustradition) *min* `0`; [Has religious tradition](object-properties.md#hasreligioustradition) *only* [Religious Tradition](classes.md#religioustradition) |
| Subclasses | [Chaitya](classes.md#chaitya-2), [Kumari House](classes.md#kumarihouse), [Stupa](classes.md#stupa-2), [Temple](classes.md#temple) |

### Religious Tradition

**IRI:** `https://cair-nepal.org/heritagegraph/ReligiousTradition` · `heritageGraph:ReligiousTradition`

Religious or philosophical tradition (e.g., Hindu, Buddhist, Syncretic)

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [note](datatype-properties.md#p3_has_note) *min* `0`; [note](datatype-properties.md#p3_has_note) *max* `1` |
| Used in | in range of [Has religious tradition](object-properties.md#hasreligioustradition); in range of [Is primary for tradition](object-properties.md#isprimaryfortradition); in range of [Religious traditions](object-properties.md#religious_traditions); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Calendar System](classes.md#calendarsystem); used in axioms of [Container](classes.md#container); used in axioms of [Deity](classes.md#deity); used in axioms of [Religious Structure](classes.md#religiousstructure) |

### Rest House

**IRI:** `https://cair-nepal.org/heritagegraph/RestHouse` · `heritageGraph:RestHouse`

Community structures for travelers and pilgrims, maintained by Guthi organizations

| | |
|---|---|
| Superclasses | [Architectural Structure](classes.md#architecturalstructure) |
| Subclasses | [Dharmashala](classes.md#dharmashala), [Pati](classes.md#pati), [Sattal](classes.md#sattal) |

### Ritual Assessment

**IRI:** `https://cair-nepal.org/heritagegraph/RitualAssessment` · `heritageGraph:RitualAssessment`

A performed assessment carried out during Kumari selection. Modelled as an event (not a hard criterion) so that source-specific, possibly conflicting accounts of whether/how it was conducted attach as provenanced Assertions rather than being asserted as fact.

| | |
|---|---|
| Superclasses | [Ritual Event](classes.md#ritualevent) |
| Restrictions | [Was documented by](object-properties.md#documentedby) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [Assesses candidate](object-properties.md#assessescandidate) *only* [Person](classes.md#e21_person); [Part of selection](object-properties.md#partofselection) *max* `1`; [Carried out by](object-properties.md#p14_carried_out_by) *min* `0`; [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [Part of selection](object-properties.md#partofselection) *min* `0`; [Assesses candidate](object-properties.md#assessescandidate) *min* `0`; [Has assertion](object-properties.md#hasassertion) *only* [Assertion](classes.md#i2_belief); [Has timespan](object-properties.md#p4_has_time-span) *max* `1`; [Has assertion](object-properties.md#hasassertion) *min* `0`; [Carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Part of selection](object-properties.md#partofselection) *only* [Kumari Selection Event](classes.md#kumariselectionevent); [Assesses candidate](object-properties.md#assessescandidate) *max* `1` |
| Subclasses | [Fearlessness Assessment](classes.md#fearlessnessassessment) |
| Used in | in range of [Ritual assessments](object-properties.md#ritual_assessments); used in axioms of [Container](classes.md#container) |

### Ritual Event

**IRI:** `https://cair-nepal.org/heritagegraph/RitualEvent` · `heritageGraph:RitualEvent`

Intentional ritual activity that activates sacred space, invokes deities, and binds social groups

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity) |
| Restrictions | [has ritual type](object-properties.md#ritualtype) *max* `1`; [Has timespan](object-properties.md#p4_has_time-span) *min* `0`; [note](datatype-properties.md#p3_has_note) *max* `1`; [Occurs before](object-properties.md#p183_ends_before_the_start_of) *min* `0`; [note](datatype-properties.md#p3_has_note) *min* `0`; [Lunar date tithi](datatype-properties.md#lunardatetithi) *max* `1`; [Start place](object-properties.md#startplace) *max* `1`; [Ritual on structure](object-properties.md#p8_took_place_on_or_within) *max* `1`; [Route places](object-properties.md#routeplaces) *min* `0`; [Lunar date tithi](datatype-properties.md#lunardatetithi) *min* `0`; [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [Is part of festival](object-properties.md#p9i_forms_part_of) *only* [Festival](classes.md#festival); [Used materials](object-properties.md#p125_used_object_of_type) *min* `0`; [Recurrence pattern](datatype-properties.md#recurrencepattern) *min* `0`; [has ritual type](object-properties.md#ritualtype) *min* `0`; [Has assertion](object-properties.md#hasassertion) *only* [Assertion](classes.md#i2_belief); [End place](object-properties.md#endplace) *max* `1`; [Has assertion](object-properties.md#hasassertion) *min* `0`; [has ritual type](object-properties.md#ritualtype) *only* [Ritual Type](classes.md#ritualtype); [Had participant](object-properties.md#hadparticipant) *only* [Actor](classes.md#e39_actor); [Recurrence pattern](datatype-properties.md#recurrencepattern) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Was documented by](object-properties.md#documentedby) *min* `0`; [Is part of festival](object-properties.md#p9i_forms_part_of) *min* `0`; [Had participant](object-properties.md#hadparticipant) *min* `0`; [Ritual on structure](object-properties.md#p8_took_place_on_or_within) *only* [Physical Heritage Thing](classes.md#physicalheritagething); [Route places](object-properties.md#routeplaces) *only* [Place](classes.md#e53_place); [Invokes deity](object-properties.md#invokesdeity) *min* `0`; [Invokes deity](object-properties.md#invokesdeity) *only* [Deity](classes.md#deity); [Occurs before](object-properties.md#p183_ends_before_the_start_of) *only* [Ritual Event](classes.md#ritualevent); [Occurs after](object-properties.md#p183i_starts_after_the_end_of) *only* [Ritual Event](classes.md#ritualevent); [Occurs after](object-properties.md#p183i_starts_after_the_end_of) *max* `1`; [Took place at](object-properties.md#p7_took_place_at) *min* `0`; [End place](object-properties.md#endplace) *only* [Place](classes.md#e53_place); [Occurs after](object-properties.md#p183i_starts_after_the_end_of) *min* `0`; [Start place](object-properties.md#startplace) *min* `0`; [Lunar date tithi](datatype-properties.md#lunardatetithi) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Has timespan](object-properties.md#p4_has_time-span) *max* `1`; [Performed by group](object-properties.md#performedbygroup) *min* `0`; [Has timespan](object-properties.md#p4_has_time-span) *only* [Time Span](classes.md#e52_time-span); [End place](object-properties.md#endplace) *min* `0`; [Ritual on structure](object-properties.md#p8_took_place_on_or_within) *min* `0`; [Recurrence pattern](datatype-properties.md#recurrencepattern) *max* `1`; [Performed by group](object-properties.md#performedbygroup) *only* (([Guthi](classes.md#guthi) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor)); [Carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Used materials](object-properties.md#p125_used_object_of_type) *only* [Material](classes.md#e57_material); [Route description](datatype-properties.md#routedescription) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Route description](datatype-properties.md#routedescription) *min* `0`; [Managed by guthi](object-properties.md#managedbyguthi) *only* [Guthi](classes.md#guthi); [Carried out by](object-properties.md#p14_carried_out_by) *min* `0`; [Managed by guthi](object-properties.md#managedbyguthi) *min* `0`; [Occurs before](object-properties.md#p183_ends_before_the_start_of) *max* `1`; [Took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [Took place at](object-properties.md#p7_took_place_at) *max* `1`; [Is part of festival](object-properties.md#p9i_forms_part_of) *max* `1`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Start place](object-properties.md#startplace) *only* [Place](classes.md#e53_place); [Route description](datatype-properties.md#routedescription) *max* `1` |
| Subclasses | [Festival](classes.md#festival), [Kumari Lifecycle Event](classes.md#kumarilifecycleevent), [Ritual Assessment](classes.md#ritualassessment) |
| Used in | in range of [Is invoked in ritual](object-properties.md#isinvokedinritual); in range of [Participates in ritual](object-properties.md#participatesinritual); in range of [Performs ritual](object-properties.md#performsritual); in range of [Ritual events](object-properties.md#ritual_events); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Deity](classes.md#deity); used in axioms of [Festival](classes.md#festival); used in axioms of [Guthi](classes.md#guthi); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Iconographic Object](classes.md#iconographicobject) |
| prov alignment note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Ritual Type

**IRI:** `https://cair-nepal.org/heritagegraph/RitualType` · `heritageGraph:RitualType`

Controlled vocabulary of ritual and festival activity types in Kathmandu Valley living heritage.

| | |
|---|---|
| Instances | [Abhisheka](concepts.md#abhisheka), [Bhajan](concepts.md#bhajan), [Chariot Procession](concepts.md#chariotprocession), [Circumambulation](concepts.md#circumambulation), [Deinstallation Ritual](concepts.md#deinstallationritual), [Homa](concepts.md#homa), [Installation Ritual](concepts.md#installationritual), [Jatra](concepts.md#jatra), [Kamya Puja](concepts.md#kamyapuja), [Masked Performance](concepts.md#maskedperformance), [Naimittika Puja](concepts.md#naimittikapuja), [Nitya Puja](concepts.md#nityapuja), [Procession Ritual](concepts.md#processionritual), [Processional Movement](concepts.md#processionalmovement), [Relic Tour](concepts.md#relictour), [Returning Ritual](concepts.md#returningritual), [Ritual Consecration](concepts.md#ritualconsecration), [Vrata](concepts.md#vrata), [Yagna](concepts.md#yagna) |
| Used in | in range of [has ritual type](object-properties.md#ritualtype); used in axioms of [Ritual Event](classes.md#ritualevent) |
| design_note | RitualType currently mixes three orthogonal axes: worship-frequency (NityaPuja/NaimittikaPuja/KamyaPuja), ritual form (Homa/Jatra/MaskedPerformance), and lifecycle (InstallationRitual/ReturningRitual). Consider splitting into RitualFrequency + RitualForm. Also: Circumambulation/ProcessionalMovement/ProcessionRitual/RelicTour overlap with RitualEvent.route_places/start_place/end_place/route_description -- pick one canonical mechanism for moving rituals. |
| permissible_values | Chariot Procession; Circumambulation; Deinstallation Ritual; Vrata; NityaPuja; Bhajan; Jatra; KamyaPuja; MaskedPerformance; Yagna; NaimittikaPuja; Ritual Consecration; ReturningRitual; Abhisheka; InstallationRitual; RelicTour; ProcessionRitual; Homa; ProcessionalMovement |

### Sattal

**IRI:** `https://cair-nepal.org/heritagegraph/Sattal` · `heritageGraph:Sattal`

Multi-story rest house (3-5 floors) with ritual and social functions

| | |
|---|---|
| Superclasses | [Rest House](classes.md#resthouse) |

### Selection Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/SelectionCriterion` · `heritageGraph:SelectionCriterion`

An eligibility criterion a candidate must satisfy to assume the Kumari role. Modelled as explicit subclasses so 'what are the eligibility criteria?' is a subclass query, not free text.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Subclasses | [Age Criterion](classes.md#agecriterion), [Horoscope Compatibility Criterion](classes.md#horoscopecompatibilitycriterion), [Lineage Criterion](classes.md#lineagecriterion), [Physical Integrity Criterion](classes.md#physicalintegritycriterion), [Thirty Two Perfections Criterion](classes.md#thirtytwoperfectionscriterion) |
| Used in | in range of [Has criterion](object-properties.md#hascriterion); in range of [Selection criteria](object-properties.md#selection_criteria); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |

### Stupa

**IRI:** `https://cair-nepal.org/heritagegraph/Stupa` · `heritageGraph:Stupa`

Buddhist dome-shaped reliquary shrine with circumambulation and ritual activation (e.g., Boudhanath, Swayambhunath).

| | |
|---|---|
| Superclasses | [Religious Structure](classes.md#religiousstructure) |
| Disjoint with | [Chaitya](classes.md#chaitya-2) |

### Syncretic Relationship

**IRI:** `https://cair-nepal.org/heritagegraph/SyncreticRelationship` · `heritageGraph:SyncreticRelationship`

Formalizes the syncretic equivalence between divine entities across different theological frameworks. Following CIDOC CRM E13, it treats syncretism as a propositional claim with associated epistemic authority and provenance.

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity) |
| Restrictions | [Assigned to deity](object-properties.md#p140_assigned_attribute_to) *max* `1`; [Assigned to deity](object-properties.md#p140_assigned_attribute_to) *only* [Deity](classes.md#deity); [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [used](object-properties.md#used) *only* [Entity](classes.md#entity); [has syncretic type](object-properties.md#syncretictype) *only* [Syncretic Type](classes.md#syncretictype); [Assigned to deity](object-properties.md#p140_assigned_attribute_to) *min* `1`; [Assigned equivalent](object-properties.md#p141_assigned) *min* `1`; [has syncretic type](object-properties.md#syncretictype) *max* `1`; [Documented in source](object-properties.md#mentionedinsource) *only* [Data Source](classes.md#datasource); [has syncretic type](object-properties.md#syncretictype) *min* `0`; [used](object-properties.md#used) *min* `0`; [note](datatype-properties.md#p3_has_note) *max* `1`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Was documented by](object-properties.md#documentedby) *min* `0`; [note](datatype-properties.md#p3_has_note) *min* `0`; [Assigned equivalent](object-properties.md#p141_assigned) *only* [Deity](classes.md#deity); [Documented in source](object-properties.md#mentionedinsource) *min* `0` |
| Used in | in range of [Syncretic relationships](object-properties.md#syncretic_relationships); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container) |

### Syncretic Type

**IRI:** `https://cair-nepal.org/heritagegraph/SyncreticType` · `heritageGraph:SyncreticType`

Controlled vocabulary for kinds of syncretic theological relationships between deities.

| | |
|---|---|
| Instances | [Appropriation](concepts.md#appropriation), [Equivalence](concepts.md#equivalence), [Fusion](concepts.md#fusion), [Historical](concepts.md#historical) |
| Used in | in range of [has syncretic type](object-properties.md#syncretictype); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |
| permissible_values | Appropriation; Historical; Fusion; Equivalence |

### Technique

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E29_Design_or_Procedure` · `crm:E29_Design_or_Procedure`

Method or craft process used in production or ritual

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Used in | in range of [techniques](object-properties.md#techniques); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container) |

### Temple

**IRI:** `https://cair-nepal.org/heritagegraph/Temple` · `heritageGraph:Temple`

Religious structure characterized by deity enshrinement and ritual activation. Legal designation (e.g. 'Ancient Monument' under Nepal law) is recorded per-instance via a governance assertion, not as a class criterion.

| | |
|---|---|
| Superclasses | [Religious Structure](classes.md#religiousstructure) |
| Restrictions | [Has architectural style](object-properties.md#hasarchitecturalstyle) *min* `1`; [Enshrines deity through event](object-properties.md#enshrinesdeitythroughevent) *only* [Enshrinement](classes.md#enshrinement); [Has architectural style](object-properties.md#hasarchitecturalstyle) *only* [Architectural Style](classes.md#architecturalstyle-2); [Has architectural style](object-properties.md#hasarchitecturalstyle) *max* `1`; [Enshrines deity through event](object-properties.md#enshrinesdeitythroughevent) *min* `0` |
| Used in | in range of [Enshrined in structure](object-properties.md#enshrinedinstructure); used in axioms of [Enshrinement](classes.md#enshrinement) |

### Thirty Two Perfections Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/ThirtyTwoPerfectionsCriterion` · `heritageGraph:ThirtyTwoPerfectionsCriterion`

Candidate must exhibit the battis lakshana (thirty-two perfections/auspicious bodily marks).

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Time Span

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E52_Time-Span` · `crm:E52_Time-Span`

Temporal extent of an event or period

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Used in | in range of [Birth timespan](object-properties.md#birthtimespan); in range of [Death timespan](object-properties.md#deathtimespan); in range of [Publication timespan](object-properties.md#publicationtimespan); in range of [Time spans](object-properties.md#time_spans); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Consecration](classes.md#consecration); used in axioms of [Container](classes.md#container); used in axioms of [Data Source](classes.md#datasource); used in axioms of [Documentation Activity](classes.md#documentationactivity); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Transfer Of Custody

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E10_Transfer_of_Custody` · `crm:E10_Transfer_of_Custody`

Event of transferring responsibility for temple maintenance, ritual performance, or artifact stewardship

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity) |
| Used in | in range of [Custody events](object-properties.md#custody_events); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Container](classes.md#container) |
| prov_alignment_note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Verification

**IRI:** `https://cair-nepal.org/heritagegraph/Verification` · `heritageGraph:Verification`

Process of cross-checking heritage claims against multiple sources

| | |
|---|---|
| Superclasses | [Documentation Activity](classes.md#documentationactivity) |
| Restrictions | [Verified assertion](object-properties.md#verifiedassertion) *min* `0`; [Verified by expert](object-properties.md#verifiedbyexpert) *min* `0`; [Verified by expert](object-properties.md#verifiedbyexpert) *only* [Person](classes.md#e21_person); [Verification method](datatype-properties.md#verificationmethod) *min* `0`; [Verified assertion](object-properties.md#verifiedassertion) *only* [Assertion](classes.md#i2_belief); [Verification method](datatype-properties.md#verificationmethod) *max* `1`; [note](datatype-properties.md#p3_has_note) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [note](datatype-properties.md#p3_has_note) *max* `1`; [note](datatype-properties.md#p3_has_note) *min* `0`; [Verification method](datatype-properties.md#verificationmethod) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| prov_alignment_note | prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally. |

### Water Structure

**IRI:** `https://cair-nepal.org/heritagegraph/WaterStructure` · `heritageGraph:WaterStructure`

Engineered water supply systems with ritual and civic significance

| | |
|---|---|
| Superclasses | [Architectural Structure](classes.md#architecturalstructure) |
| Subclasses | [Dhunge Dhara](classes.md#dhungedhara), [Pokhari](classes.md#pokhari) |

