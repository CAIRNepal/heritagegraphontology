# Object properties

### Acted on behalf of

**IRI:** `http://www.w3.org/ns/prov#actedOnBehalfOf` · `prov:actedOnBehalfOf`

Agent on whose behalf this agent acted.

### actors

**IRI:** `https://cair-nepal.org/heritagegraph/actors` · `heritageGraph:actors`

Collection of generic Actor instances

| | |
|---|---|
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Container](classes.md#container) |

### Architectural elements

**IRI:** `https://cair-nepal.org/heritagegraph/architectural_elements` · `heritageGraph:architectural_elements`

Collection of ArchitecturalElement instances

| | |
|---|---|
| Range | [Architectural Element](classes.md#architecturalelement) |
| Used in | used in axioms of [Container](classes.md#container) |

### Architectural structures

**IRI:** `https://cair-nepal.org/heritagegraph/architecturalStructures` · `heritageGraph:architecturalStructures`

Heritage structures affected by or present during this historical event

| | |
|---|---|
| Super-properties | [Occurred in presence of](object-properties.md#p12_occurred_in_the_presence_of) |
| Range | [Architectural Structure](classes.md#architecturalstructure) |
| Used in | used in axioms of [Historical Event](classes.md#historicalevent) |

### assertions

**IRI:** `https://cair-nepal.org/heritagegraph/assertions` · `heritageGraph:assertions`

Collection of Assertion instances

| | |
|---|---|
| Range | [Assertion](classes.md#i2_belief) |
| Used in | used in axioms of [Container](classes.md#container) |

### Asserts about

**IRI:** `https://cair-nepal.org/heritagegraph/assertsAbout` · `heritageGraph:assertsAbout`

Heritage entity or event that is the subject of this assertion.

| | |
|---|---|
| Range | [Assertion Subject](classes.md#assertionsubject) |
| Inverse of | [Has assertion](object-properties.md#hasassertion) |

### Asserts proposition

**IRI:** `http://www.cidoc-crm.org/extensions/crminf/J4_that` · `crminf:J4_that`

Machine-readable proposition(s) this assertion holds to be true (CRMinf J4 that). Complements the free-text assertion_content.

### Assessed condition state

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P35_has_identified` · `crm:P35_has_identified`

Condition state identified by the assessment

### Assessed object

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P34_concerned` · `crm:P34_concerned`

Object assessed for condition

### Assesses candidate

**IRI:** `https://cair-nepal.org/heritagegraph/assessesCandidate` · `heritageGraph:assessesCandidate`

Candidate being assessed.

| | |
|---|---|
| Range | [Person](classes.md#e21_person) |
| Used in | used in axioms of [Ritual Assessment](classes.md#ritualassessment) |

### Assigned equivalent

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P141_assigned` · `crm:P141_assigned`

The deity or sacred figure being identified as equivalent to the primary deity.

| | |
|---|---|
| Used in | used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### Assigned to deity

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P140_assigned_attribute_to` · `crm:P140_assigned_attribute_to`

The deity instance that is the subject of the syncretic claim.

| | |
|---|---|
| Used in | used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### Assumes role

**IRI:** `https://cair-nepal.org/heritagegraph/assumesRole` · `heritageGraph:assumesRole`

KumariRole held during this tenure.

| | |
|---|---|
| Range | [Kumari Role](classes.md#kumarirole) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Birth timespan

**IRI:** `https://cair-nepal.org/heritagegraph/birthTimespan` · `heritageGraph:birthTimespan`

Person's birth timespan

| | |
|---|---|
| Super-properties | [Has timespan](object-properties.md#p4_has_time-span) |
| Range | [Time Span](classes.md#e52_time-span) |

### Bounds tenure

**IRI:** `https://cair-nepal.org/heritagegraph/boundsTenure` · `heritageGraph:boundsTenure`

The KumariTenure period that this lifecycle event bounds (initiates or terminates). Specialized by initiated_tenure (selection) and ended_tenure_of (retirement).

| | |
|---|---|
| Sub-properties | [Ended tenure of](object-properties.md#endedtenureof), [Initiated tenure](object-properties.md#initiatedtenure) |
| Range | [Kumari Tenure](classes.md#kumaritenure) |
| Used in | used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |

### Calendar systems

**IRI:** `https://cair-nepal.org/heritagegraph/calendar_systems` · `heritageGraph:calendar_systems`

Collection of CalendarSystem instances

| | |
|---|---|
| Range | [Calendar System](classes.md#calendarsystem) |
| Used in | used in axioms of [Container](classes.md#container) |

### Carried out activity

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P14i_performed` · `crm:P14i_performed`

Activities performed by this actor

| | |
|---|---|
| Sub-properties | [Performs ritual](object-properties.md#performsritual) |

### Carried out by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by` · `crm:P14_carried_out_by`

Actor(s) who performed this event

| | |
|---|---|
| Sub-properties | [Performed by group](object-properties.md#performedbygroup), [Verified by expert](object-properties.md#verifiedbyexpert) |
| Used in | used in axioms of [Consecration](classes.md#consecration); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Caste groups

**IRI:** `https://cair-nepal.org/heritagegraph/caste_groups` · `heritageGraph:caste_groups`

Collection of CasteGroup instances

| | |
|---|---|
| Range | [Caste Group](classes.md#castegroup) |
| Used in | used in axioms of [Container](classes.md#container) |

### Commissioned by

**IRI:** `https://cair-nepal.org/heritagegraph/commissionedBy` · `heritageGraph:commissionedBy`

Person or group who commissioned production

| | |
|---|---|
| Range | [Actor](classes.md#e39_actor) |

### Condition assessments

**IRI:** `https://cair-nepal.org/heritagegraph/condition_assessments` · `heritageGraph:condition_assessments`

Collection of ConditionAssessment instances

| | |
|---|---|
| Range | [Condition Assessment](classes.md#e14_condition_assessment) |
| Used in | used in axioms of [Container](classes.md#container) |

### Condition states

**IRI:** `https://cair-nepal.org/heritagegraph/condition_states` · `heritageGraph:condition_states`

Collection of ConditionState instances

| | |
|---|---|
| Range | [Condition State](classes.md#e3_condition_state) |
| Used in | used in axioms of [Container](classes.md#container) |

### Confers role

**IRI:** `https://cair-nepal.org/heritagegraph/confersRole` · `heritageGraph:confersRole`

KumariRole conferred by this selection or enthronement event.

| | |
|---|---|
| Range | [Kumari Role](classes.md#kumarirole) |
| Used in | used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |

### Consecrated by event

**IRI:** `https://cair-nepal.org/heritagegraph/consecratedByEvent` · `heritageGraph:consecratedByEvent`

Consecration event that activated this murti

| | |
|---|---|
| Range | [Consecration](classes.md#consecration) |
| Inverse of | [Consecrated object](object-properties.md#p16_used_specific_object) |
| Used in | used in axioms of [Murti](classes.md#murti) |

### Consecrated object

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P16_used_specific_object` · `crm:P16_used_specific_object`

Murti employed in (and transformed by) the consecration ritual

| | |
|---|---|
| Inverse of | [Consecrated by event](object-properties.md#consecratedbyevent) |
| Used in | used in axioms of [Consecration](classes.md#consecration) |

### Consecration events

**IRI:** `https://cair-nepal.org/heritagegraph/consecration_events` · `heritageGraph:consecration_events`

Collection of Consecration event instances

| | |
|---|---|
| Range | [Consecration](classes.md#consecration) |
| Used in | used in axioms of [Container](classes.md#container) |

### Contains structure

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P53i_is_former_or_current_location_of` · `crm:P53i_is_former_or_current_location_of`

Structures located in this place

### Custody events

**IRI:** `https://cair-nepal.org/heritagegraph/custody_events` · `heritageGraph:custody_events`

Collection of TransferOfCustody event instances

| | |
|---|---|
| Range | [Transfer Of Custody](classes.md#e10_transfer_of_custody) |
| Used in | used in axioms of [Container](classes.md#container) |

### Data custodians

**IRI:** `https://cair-nepal.org/heritagegraph/data_custodians` · `heritageGraph:data_custodians`

Collection of DataCustodian instances

| | |
|---|---|
| Range | [Data Custodian](classes.md#datacustodian) |
| Used in | used in axioms of [Container](classes.md#container) |

### Data sources

**IRI:** `https://cair-nepal.org/heritagegraph/data_sources` · `heritageGraph:data_sources`

Collection of DataSource instances

| | |
|---|---|
| Range | [Data Source](classes.md#datasource) |
| Used in | used in axioms of [Container](classes.md#container) |

### Datacite creator

**IRI:** `https://cair-nepal.org/heritagegraph/sourceCreator` · `heritageGraph:sourceCreator`

Person or organization primarily responsible for creating the source

| | |
|---|---|
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |

### Datacite publisher

**IRI:** `https://cair-nepal.org/heritagegraph/sourcePublisher` · `heritageGraph:sourcePublisher`

Entity responsible for making the source available

| | |
|---|---|
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |

### Death timespan

**IRI:** `https://cair-nepal.org/heritagegraph/deathTimespan` · `heritageGraph:deathTimespan`

Person's death timespan

| | |
|---|---|
| Super-properties | [Has timespan](object-properties.md#p4_has_time-span) |
| Range | [Time Span](classes.md#e52_time-span) |

### deities

**IRI:** `https://cair-nepal.org/heritagegraph/deities` · `heritageGraph:deities`

Collection of Deity instances

| | |
|---|---|
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Container](classes.md#container) |

### Depicts deity

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P62_depicts` · `crm:P62_depicts`

Deity depicted iconographically (not cultic presence)

| | |
|---|---|
| Sub-properties | [Is about deity](object-properties.md#isaboutdeity) |
| Used in | used in axioms of [Iconographic Object](classes.md#iconographicobject) |

### Documentation activities

**IRI:** `https://cair-nepal.org/heritagegraph/documentation_activities` · `heritageGraph:documentation_activities`

Collection of DocumentationActivity instances

| | |
|---|---|
| Range | [Documentation Activity](classes.md#documentationactivity) |
| Used in | used in axioms of [Container](classes.md#container) |

### Documented in source

**IRI:** `https://cair-nepal.org/heritagegraph/mentionedInSource` · `heritageGraph:mentionedInSource`

Source(s) that mention/document this entity. Distinct from was_derived_from (which is prov:wasDerivedFrom for assertions). Entity-mention is not logical derivation.

| | |
|---|---|
| Range | [Data Source](classes.md#datasource) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |
| prov alignment | prov:wasInfluencedBy |

### documents

**IRI:** `https://cair-nepal.org/heritagegraph/documents` · `heritageGraph:documents`

Pre-existing heritage entity or event recorded by this documentation activity (inverse of was_documented_by).

| | |
|---|---|
| Range | [Assertion Subject](classes.md#assertionsubject) |
| Inverse of | [Was documented by](object-properties.md#documentedby) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |

### Embodied deity

**IRI:** `https://cair-nepal.org/heritagegraph/embodiedDeity` · `heritageGraph:embodiedDeity`

Deity role embodied by participant

| | |
|---|---|
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### End place

**IRI:** `https://cair-nepal.org/heritagegraph/endPlace` · `heritageGraph:endPlace`

Ending location of movement ritual

| | |
|---|---|
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Ended tenure of

**IRI:** `https://cair-nepal.org/heritagegraph/endedTenureOf` · `heritageGraph:endedTenureOf`

Points from a KumariRetirementEvent to the tenure that it terminated. Enables reconstruction of the complete Kumari lifecycle.

| | |
|---|---|
| Super-properties | [Bounds tenure](object-properties.md#boundstenure) |
| Range | [Kumari Tenure](classes.md#kumaritenure) |
| Inverse of | [Retired through](object-properties.md#retiredthrough) |
| Used in | used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent) |

### Enshrined deity

**IRI:** `https://cair-nepal.org/heritagegraph/enshrinedDeity` · `heritageGraph:enshrinedDeity`

Deity installed through enshrinement

| | |
|---|---|
| Super-properties | [Occurred in presence of](object-properties.md#p12_occurred_in_the_presence_of) |
| Range | [Deity](classes.md#deity) |
| Inverse of | [Is enshrined through event](object-properties.md#isenshrinedthroughevent) |
| Used in | used in axioms of [Enshrinement](classes.md#enshrinement) |

### Enshrined in structure

**IRI:** `https://cair-nepal.org/heritagegraph/enshrinedInStructure` · `heritageGraph:enshrinedInStructure`

Temple where deity was enshrined

| | |
|---|---|
| Super-properties | [Ritual on structure](object-properties.md#p8_took_place_on_or_within) |
| Range | [Temple](classes.md#temple) |
| Inverse of | [Enshrines deity through event](object-properties.md#enshrinesdeitythroughevent) |
| Used in | used in axioms of [Enshrinement](classes.md#enshrinement) |

### Enshrinement events

**IRI:** `https://cair-nepal.org/heritagegraph/enshrinement_events` · `heritageGraph:enshrinement_events`

Collection of Enshrinement event instances

| | |
|---|---|
| Range | [Enshrinement](classes.md#enshrinement) |
| Used in | used in axioms of [Container](classes.md#container) |

### Enshrines deity through event

**IRI:** `https://cair-nepal.org/heritagegraph/enshrinesDeityThroughEvent` · `heritageGraph:enshrinesDeityThroughEvent`

Enshrinement event that installed deity in temple

| | |
|---|---|
| Range | [Enshrinement](classes.md#enshrinement) |
| Inverse of | [Enshrined in structure](object-properties.md#enshrinedinstructure) |
| Used in | used in axioms of [Temple](classes.md#temple) |

### Enthroned person

**IRI:** `https://cair-nepal.org/heritagegraph/enthronedPerson` · `heritageGraph:enthronedPerson`

Girl enthroned as Kumari by this enthronement event.

| | |
|---|---|
| Range | [Person](classes.md#e21_person) |
| Used in | used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent) |

### Enthroned through

**IRI:** `https://cair-nepal.org/heritagegraph/enthronedThrough` · `heritageGraph:enthronedThrough`

Enthronement event that activated this tenure.

| | |
|---|---|
| Range | [Kumari Enthronement Event](classes.md#kumarienthronementevent) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### festivals

**IRI:** `https://cair-nepal.org/heritagegraph/festivals` · `heritageGraph:festivals`

Collection of Festival instances

| | |
|---|---|
| Range | [Festival](classes.md#festival) |
| Used in | used in axioms of [Container](classes.md#container) |

### generated

**IRI:** `http://www.w3.org/ns/prov#generated` · `prov:generated`

Entity generated by this activity.

| | |
|---|---|
| Inverse of | [Was generated by](object-properties.md#wasgeneratedby) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |

### guthis

**IRI:** `https://cair-nepal.org/heritagegraph/guthis` · `heritageGraph:guthis`

Collection of Guthi instances

| | |
|---|---|
| Range | [Guthi](classes.md#guthi) |
| Used in | used in axioms of [Container](classes.md#container) |

### Had participant

**IRI:** `https://cair-nepal.org/heritagegraph/hadParticipant` · `heritageGraph:hadParticipant`

Actor(s) participating in this period, situation or ritual without carrying it out (e.g. the girl holding a Kumari tenure, or the Kumari in a chariot procession).

| | |
|---|---|
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Has architectural style

**IRI:** `https://cair-nepal.org/heritagegraph/hasArchitecturalStyle` · `heritageGraph:hasArchitecturalStyle`

Architectural style classification

| | |
|---|---|
| Super-properties | [Has type](object-properties.md#p2_has_type) |
| Range | [Architectural Style](classes.md#architecturalstyle) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Temple](classes.md#temple) |

### Has assertion

**IRI:** `https://cair-nepal.org/heritagegraph/hasAssertion` · `heritageGraph:hasAssertion`

Provenance-bearing assertion made about this entity or event.

| | |
|---|---|
| Range | [Assertion](classes.md#i2_belief) |
| Inverse of | [Asserts about](object-properties.md#assertsabout) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent) |

### has calendar system

**IRI:** `https://cair-nepal.org/heritagegraph/calendarSystem` · `heritageGraph:calendarSystem`

Calendar system used for date representation

| | |
|---|---|
| Range | [Calendar System](classes.md#calendarsystem) |

### Has component

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P46_is_composed_of` · `crm:P46_is_composed_of`

Architectural elements composing structure

| | |
|---|---|
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### Has condition assessment

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P34i_was_assessed_by` · `crm:P34i_was_assessed_by`

Condition assessment events for this structure

| | |
|---|---|
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### Has condition type

**IRI:** `https://cair-nepal.org/heritagegraph/hasConditionType` · `heritageGraph:hasConditionType`

Categorization of the condition state

| | |
|---|---|
| Super-properties | [Has type](object-properties.md#p2_has_type) |
| Range | [Condition Type](classes.md#conditiontype) |

### Has criterion

**IRI:** `https://cair-nepal.org/heritagegraph/hasCriterion` · `heritageGraph:hasCriterion`

Eligibility criterion applied in this selection.

| | |
|---|---|
| Range | [Selection Criterion](classes.md#selectioncriterion) |
| Used in | used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |

### Has current location

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P55_has_current_location` · `crm:P55_has_current_location`

Current location of object or structure

| | |
|---|---|
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Iconographic Object](classes.md#iconographicobject) |

### Has custody event

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P30i_custody_transferred_through` · `crm:P30i_custody_transferred_through`

Custody transfer events for this structure

### has date precision

**IRI:** `https://cair-nepal.org/heritagegraph/datePrecision` · `heritageGraph:datePrecision`

The level of precision for a recorded date.

| | |
|---|---|
| Range | [Date Precision](classes.md#dateprecision) |

### has destruction event

**IRI:** `https://cair-nepal.org/heritagegraph/destructionEvent` · `heritageGraph:destructionEvent`

Event that destroyed this structure (if known)

| | |
|---|---|
| Range | [Destruction Event](classes.md#e6_destruction) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### has existence status

**IRI:** `https://cair-nepal.org/heritagegraph/existenceStatus` · `heritageGraph:existenceStatus`

Current physical status of the structure

| | |
|---|---|
| Range | [Existence Status](classes.md#existencestatus) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### has guthi type

**IRI:** `https://cair-nepal.org/heritagegraph/guthiType` · `heritageGraph:guthiType`

Type of Guthi (Si, Jatra, Temple)

| | |
|---|---|
| Super-properties | [Has type](object-properties.md#p2_has_type) |
| Range | [Guthi Type](classes.md#guthitype-2) |
| Used in | used in axioms of [Guthi](classes.md#guthi) |

### Has membership

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P107_has_current_or_former_member` · `crm:P107_has_current_or_former_member`

Members of Guthi organization

| | |
|---|---|
| Used in | used in axioms of [Guthi](classes.md#guthi) |

### has metadata

**IRI:** `https://cair-nepal.org/heritagegraph/metadata` · `heritageGraph:metadata`

Dataset metadata

| | |
|---|---|
| Range | [Metadata](classes.md#metadata) |
| Used in | used in axioms of [Container](classes.md#container) |

### Has religious tradition

**IRI:** `https://cair-nepal.org/heritagegraph/hasReligiousTradition` · `heritageGraph:hasReligiousTradition`

Religious tradition(s) within which this deity is venerated, or which use this religious structure

| | |
|---|---|
| Super-properties | [Has type](object-properties.md#p2_has_type) |
| Range | [Religious Tradition](classes.md#religioustradition) |
| Used in | used in axioms of [Deity](classes.md#deity); used in axioms of [Religious Structure](classes.md#religiousstructure) |

### has ritual type

**IRI:** `https://cair-nepal.org/heritagegraph/ritualType` · `heritageGraph:ritualType`

Classification of ritual (puja, jatra, consecration)

| | |
|---|---|
| Super-properties | [Has type](object-properties.md#p2_has_type) |
| Range | [Ritual Type](classes.md#ritualtype-2) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### has syncretic type

**IRI:** `https://cair-nepal.org/heritagegraph/syncreticType` · `heritageGraph:syncreticType`

The typological nature of the syncretism (e.g., Ontological Identity, Functional Overlap, Iconographic Similarity).

| | |
|---|---|
| Super-properties | [Has type](object-properties.md#p2_has_type) |
| Range | [Syncretic Type](classes.md#syncretictype) |
| Used in | used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### Has timespan

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P4_has_time-span` · `crm:P4_has_time-span`

Links event to its temporal extent

| | |
|---|---|
| Sub-properties | [Birth timespan](object-properties.md#birthtimespan), [Death timespan](object-properties.md#deathtimespan), [Publication timespan](object-properties.md#publicationtimespan) |
| Used in | used in axioms of [Consecration](classes.md#consecration); used in axioms of [Documentation Activity](classes.md#documentationactivity); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Has type

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P2_has_type` · `crm:P2_has_type`

Generic CRM typing property (P2 has type). Canonical holder of the CRM predicate; use the specific typing slots below in data.

| | |
|---|---|
| Sub-properties | [Has architectural style](object-properties.md#hasarchitecturalstyle), [Has condition type](object-properties.md#hasconditiontype), [has guthi type](object-properties.md#guthitype), [Has religious tradition](object-properties.md#hasreligioustradition), [has ritual type](object-properties.md#ritualtype), [has syncretic type](object-properties.md#syncretictype) |

### Historical events

**IRI:** `https://cair-nepal.org/heritagegraph/historical_events` · `heritageGraph:historical_events`

Collection of HistoricalEvent (incl. DestructionEvent) instances

| | |
|---|---|
| Range | [Historical Event](classes.md#historicalevent) |
| Used in | used in axioms of [Container](classes.md#container) |

### Holds custody of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P50i_is_current_keeper_of` · `crm:P50i_is_current_keeper_of`

Structures under Guthi custodianship

| | |
|---|---|
| Used in | used in axioms of [Guthi](classes.md#guthi) |

### Human made objects

**IRI:** `https://cair-nepal.org/heritagegraph/human_made_objects` · `heritageGraph:human_made_objects`

Collection of generic HumanMadeObject instances (use structures / iconographic_objects for subclasses)

| | |
|---|---|
| Range | [Human Made Object](classes.md#e22_human-made_object) |
| Used in | used in axioms of [Container](classes.md#container) |

### Hypothesized location

**IRI:** `https://cair-nepal.org/heritagegraph/hypothesizedLocation` · `heritageGraph:hypothesizedLocation`

Possible locations if the structure is lost

| | |
|---|---|
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### Iconographic objects

**IRI:** `https://cair-nepal.org/heritagegraph/iconographic_objects` · `heritageGraph:iconographic_objects`

Collection of IconographicObject instances (incl. Murti, Paubha)

| | |
|---|---|
| Range | [Iconographic Object](classes.md#iconographicobject) |
| Used in | used in axioms of [Container](classes.md#container) |

### Includes ritual event

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P9_consists_of` · `crm:P9_consists_of`

Component rituals of festival

| | |
|---|---|
| Used in | used in axioms of [Festival](classes.md#festival); used in axioms of [Historical Event](classes.md#historicalevent) |

### Information objects

**IRI:** `https://cair-nepal.org/heritagegraph/information_objects` · `heritageGraph:information_objects`

Collection of InformationObject instances

| | |
|---|---|
| Range | [Information Object](classes.md#informationobject) |
| Used in | used in axioms of [Container](classes.md#container) |

### Initiated tenure

**IRI:** `https://cair-nepal.org/heritagegraph/initiatedTenure` · `heritageGraph:initiatedTenure`

Kumari tenure that was initiated by this selection event

| | |
|---|---|
| Super-properties | [Bounds tenure](object-properties.md#boundstenure) |
| Range | [Kumari Tenure](classes.md#kumaritenure) |
| Inverse of | [Selected through](object-properties.md#selectedthrough) |
| Used in | used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |

### Invokes deity

**IRI:** `https://cair-nepal.org/heritagegraph/invokesDeity` · `heritageGraph:invokesDeity`

Deity invoked or made present through ritual

| | |
|---|---|
| Super-properties | [Occurred in presence of](object-properties.md#p12_occurred_in_the_presence_of) |
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Is about

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P129_is_about` · `crm:P129_is_about`

Heritage entity or event described by this information object.

| | |
|---|---|
| Used in | used in axioms of [Information Object](classes.md#informationobject) |

### Is about deity

**IRI:** `https://cair-nepal.org/heritagegraph/isAboutDeity` · `heritageGraph:isAboutDeity`

Deity represented and ritually associated with the Murti

| | |
|---|---|
| Super-properties | [Depicts deity](object-properties.md#p62_depicts) |
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Murti](classes.md#murti) |

### Is component of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P46i_forms_part_of` · `crm:P46i_forms_part_of`

Larger structure that this element is part of

| | |
|---|---|
| Used in | used in axioms of [Architectural Element](classes.md#architecturalelement) |

### Is depicted in

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P62i_is_depicted_by` · `crm:P62i_is_depicted_by`

Iconographic objects (murti, paubha) in which this deity is depicted.

| | |
|---|---|
| Used in | used in axioms of [Deity](classes.md#deity) |

### Is enshrined through event

**IRI:** `https://cair-nepal.org/heritagegraph/isEnshrinedThroughEvent` · `heritageGraph:isEnshrinedThroughEvent`

Events where this deity was enshrined

| | |
|---|---|
| Range | [Enshrinement](classes.md#enshrinement) |
| Inverse of | [Enshrined deity](object-properties.md#enshrineddeity) |
| Used in | used in axioms of [Deity](classes.md#deity) |

### Is invoked in ritual

**IRI:** `https://cair-nepal.org/heritagegraph/isInvokedInRitual` · `heritageGraph:isInvokedInRitual`

Rituals where this deity is invoked

| | |
|---|---|
| Super-properties | [Was present at](object-properties.md#p12i_was_present_at) |
| Range | [Ritual Event](classes.md#ritualevent) |
| Used in | used in axioms of [Deity](classes.md#deity) |

### Is part of festival

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P9i_forms_part_of` · `crm:P9i_forms_part_of`

Larger festival this ritual is part of

| | |
|---|---|
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Is primary for tradition

**IRI:** `https://cair-nepal.org/heritagegraph/isPrimaryForTradition` · `heritageGraph:isPrimaryForTradition`

Religious tradition(s) that primarily use this calendar system (e.g., Bikram Sambat for Hindu, Nepal Sambat for Newar Buddhist)

| | |
|---|---|
| Range | [Religious Tradition](classes.md#religioustradition) |
| Used in | used in axioms of [Calendar System](classes.md#calendarsystem) |

### Kumari lifecycle events

**IRI:** `https://cair-nepal.org/heritagegraph/kumari_lifecycle_events` · `heritageGraph:kumari_lifecycle_events`

Collection of Kumari lifecycle events (selection, enthronement, retirement)

| | |
|---|---|
| Range | [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |
| Used in | used in axioms of [Container](classes.md#container) |

### Kumari roles

**IRI:** `https://cair-nepal.org/heritagegraph/kumari_roles` · `heritageGraph:kumari_roles`

Collection of KumariRole instances

| | |
|---|---|
| Range | [Kumari Role](classes.md#kumarirole) |
| Used in | used in axioms of [Container](classes.md#container) |

### Kumari tenures

**IRI:** `https://cair-nepal.org/heritagegraph/kumari_tenures` · `heritageGraph:kumari_tenures`

Collection of KumariTenure instances

| | |
|---|---|
| Range | [Kumari Tenure](classes.md#kumaritenure) |
| Used in | used in axioms of [Container](classes.md#container) |

### Makes deity present

**IRI:** `https://cair-nepal.org/heritagegraph/makesDeityPresent` · `heritageGraph:makesDeityPresent`

Deity made present through consecration

| | |
|---|---|
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Consecration](classes.md#consecration) |

### Managed by guthi

**IRI:** `https://cair-nepal.org/heritagegraph/managedByGuthi` · `heritageGraph:managedByGuthi`

Guthi organization managing this structure or ritual

| | |
|---|---|
| Range | [Guthi](classes.md#guthi) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Ritual Event](classes.md#ritualevent) |

### materials

**IRI:** `https://cair-nepal.org/heritagegraph/materials` · `heritageGraph:materials`

Collection of Material instances

| | |
|---|---|
| Range | [Material](classes.md#e57_material) |
| Used in | used in axioms of [Container](classes.md#container) |

### Member of group

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P107i_is_current_or_former_member_of` · `crm:P107i_is_current_or_former_member_of`

Groups this person belongs to

### Occurred in presence of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P12_occurred_in_the_presence_of` · `crm:P12_occurred_in_the_presence_of`

Generic CRM presence relation (P12): entity present at an event. Canonical holder of the CRM predicate; use the specific presence slots in data.

| | |
|---|---|
| Sub-properties | [Architectural structures](object-properties.md#architecturalstructures), [Enshrined deity](object-properties.md#enshrineddeity), [Invokes deity](object-properties.md#invokesdeity) |

### Occurs after

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P183i_starts_after_the_end_of` · `crm:P183i_starts_after_the_end_of`

Points to the prerequisite ritual.

| | |
|---|---|
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Occurs before

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P183_ends_before_the_start_of` · `crm:P183_ends_before_the_start_of`

Points to the next ritual in the canonical sequence.

| | |
|---|---|
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Part of selection

**IRI:** `https://cair-nepal.org/heritagegraph/partOfSelection` · `heritageGraph:partOfSelection`

Selection event this assessment is part of.

| | |
|---|---|
| Range | [Kumari Selection Event](classes.md#kumariselectionevent) |
| Used in | used in axioms of [Ritual Assessment](classes.md#ritualassessment) |

### Participates in ritual

**IRI:** `https://cair-nepal.org/heritagegraph/participatesInRitual` · `heritageGraph:participatesInRitual`

Rituals in which this structure participates

| | |
|---|---|
| Super-properties | [Was present at](object-properties.md#p12i_was_present_at) |
| Range | [Ritual Event](classes.md#ritualevent) |
| Used in | used in axioms of [Iconographic Object](classes.md#iconographicobject) |

### Performed by group

**IRI:** `https://cair-nepal.org/heritagegraph/performedByGroup` · `heritageGraph:performedByGroup`

Group (Guthi, caste) responsible for ritual

| | |
|---|---|
| Super-properties | [Carried out by](object-properties.md#p14_carried_out_by) |
| Range | ([Guthi](classes.md#guthi) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Performs ritual

**IRI:** `https://cair-nepal.org/heritagegraph/performsRitual` · `heritageGraph:performsRitual`

Rituals performed by this Guthi

| | |
|---|---|
| Super-properties | [Carried out activity](object-properties.md#p14i_performed) |
| Range | [Ritual Event](classes.md#ritualevent) |
| Used in | used in axioms of [Guthi](classes.md#guthi) |

### persons

**IRI:** `https://cair-nepal.org/heritagegraph/persons` · `heritageGraph:persons`

Collection of Person instances

| | |
|---|---|
| Range | [Person](classes.md#e21_person) |
| Used in | used in axioms of [Container](classes.md#container) |

### Physical heritage things

**IRI:** `https://cair-nepal.org/heritagegraph/physical_heritage_things` · `heritageGraph:physical_heritage_things`

Collection of all physical heritage objects

| | |
|---|---|
| Range | [Physical Heritage Thing](classes.md#physicalheritagething) |
| Used in | used in axioms of [Container](classes.md#container) |

### places

**IRI:** `https://cair-nepal.org/heritagegraph/places` · `heritageGraph:places`

Collection of Place instances

| | |
|---|---|
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Container](classes.md#container) |

### Produced object

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P108_has_produced` · `crm:P108_has_produced`

Object produced by this production event

### Production events

**IRI:** `https://cair-nepal.org/heritagegraph/production_events` · `heritageGraph:production_events`

Collection of Production event instances

| | |
|---|---|
| Range | [Production](classes.md#e12_production) |
| Used in | used in axioms of [Container](classes.md#container) |

### Proposition object entity

**IRI:** `https://cair-nepal.org/heritagegraph/propositionObjectEntity` · `heritageGraph:propositionObjectEntity`

Object of the proposition when it is a heritage entity (plays the role of rdf:object).

| | |
|---|---|
| Range | [Assertion Subject](classes.md#assertionsubject) |
| Used in | used in axioms of [Proposition](classes.md#proposition) |

### Proposition subject

**IRI:** `https://cair-nepal.org/heritagegraph/propositionSubject` · `heritageGraph:propositionSubject`

Entity the proposition is about (plays the role of rdf:subject).

| | |
|---|---|
| Range | [Assertion Subject](classes.md#assertionsubject) |
| Used in | used in axioms of [Proposition](classes.md#proposition) |

### propositions

**IRI:** `https://cair-nepal.org/heritagegraph/propositions` · `heritageGraph:propositions`

Collection of Proposition instances referenced by assertions

| | |
|---|---|
| Range | [Proposition](classes.md#proposition) |
| Used in | used in axioms of [Container](classes.md#container) |

### Publication timespan

**IRI:** `https://cair-nepal.org/heritagegraph/publicationTimespan` · `heritageGraph:publicationTimespan`

When source was published

| | |
|---|---|
| Super-properties | [Has timespan](object-properties.md#p4_has_time-span) |
| Range | [Time Span](classes.md#e52_time-span) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |

### Religious traditions

**IRI:** `https://cair-nepal.org/heritagegraph/religious_traditions` · `heritageGraph:religious_traditions`

Collection of ReligiousTradition instances

| | |
|---|---|
| Range | [Religious Tradition](classes.md#religioustradition) |
| Used in | used in axioms of [Container](classes.md#container) |

### Residence structure

**IRI:** `https://cair-nepal.org/heritagegraph/residenceStructure` · `heritageGraph:residenceStructure`

Structure where a person resides during a specific period. For Living Goddess, this is typically a Kumari Ghar (god-house).

| | |
|---|---|
| Range | [Architectural Structure](classes.md#architecturalstructure) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Retired through

**IRI:** `https://cair-nepal.org/heritagegraph/retiredThrough` · `heritageGraph:retiredThrough`

Retirement/desanctification event that ended this tenure.

| | |
|---|---|
| Range | [Kumari Retirement Event](classes.md#kumariretirementevent) |
| Inverse of | [Ended tenure of](object-properties.md#endedtenureof) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Ritual assessments

**IRI:** `https://cair-nepal.org/heritagegraph/ritual_assessments` · `heritageGraph:ritual_assessments`

Collection of RitualAssessment (e.g. FearlessnessAssessment) instances

| | |
|---|---|
| Range | [Ritual Assessment](classes.md#ritualassessment) |
| Used in | used in axioms of [Container](classes.md#container) |

### Ritual events

**IRI:** `https://cair-nepal.org/heritagegraph/ritual_events` · `heritageGraph:ritual_events`

Collection of RitualEvent instances

| | |
|---|---|
| Range | [Ritual Event](classes.md#ritualevent) |
| Used in | used in axioms of [Container](classes.md#container) |

### Ritual on structure

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P8_took_place_on_or_within` · `crm:P8_took_place_on_or_within`

Ritual occurs at specific temple or monument

| | |
|---|---|
| Sub-properties | [Enshrined in structure](object-properties.md#enshrinedinstructure) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Role deity

**IRI:** `https://cair-nepal.org/heritagegraph/roleDeity` · `heritageGraph:roleDeity`

Deity embodied by whoever holds this role (e.g., Taleju).

| | |
|---|---|
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Kumari Role](classes.md#kumarirole) |

### Route places

**IRI:** `https://cair-nepal.org/heritagegraph/routePlaces` · `heritageGraph:routePlaces`

Ordered list of places visited during movement ritual

| | |
|---|---|
| Super-properties | [Took place at](object-properties.md#p7_took_place_at) |
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Selected person

**IRI:** `https://cair-nepal.org/heritagegraph/selectedPerson` · `heritageGraph:selectedPerson`

Person selected through a ritual selection process to assume a sacred role or office

| | |
|---|---|
| Range | [Person](classes.md#e21_person) |
| Used in | used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |

### Selected through

**IRI:** `https://cair-nepal.org/heritagegraph/selectedThrough` · `heritageGraph:selectedThrough`

Selection event that initiated this tenure.

| | |
|---|---|
| Range | [Kumari Selection Event](classes.md#kumariselectionevent) |
| Inverse of | [Initiated tenure](object-properties.md#initiatedtenure) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Selection criteria

**IRI:** `https://cair-nepal.org/heritagegraph/selection_criteria` · `heritageGraph:selection_criteria`

Collection of SelectionCriterion instances

| | |
|---|---|
| Range | [Selection Criterion](classes.md#selectioncriterion) |
| Used in | used in axioms of [Container](classes.md#container) |

### Start place

**IRI:** `https://cair-nepal.org/heritagegraph/startPlace` · `heritageGraph:startPlace`

Starting location of movement ritual

| | |
|---|---|
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### structures

**IRI:** `https://cair-nepal.org/heritagegraph/structures` · `heritageGraph:structures`

Collection of ArchitecturalStructure instances (incl. subclasses)

| | |
|---|---|
| Range | [Architectural Structure](classes.md#architecturalstructure) |
| Used in | used in axioms of [Container](classes.md#container) |

### Supersedes assertion

**IRI:** `http://www.w3.org/ns/prov#wasRevisionOf` · `prov:wasRevisionOf`

Previous assertion that this one revises (version chain A1->A2->A3). Uses prov:wasRevisionOf (a derivation between entities); the latest assertion is the one with no incoming wasRevisionOf. NOTE: prov:invalidated was incorrect here (it is an Activity->Entity relation, not Entity->Entity).

### Supported by institution

**IRI:** `https://cair-nepal.org/heritagegraph/supportedByInstitution` · `heritageGraph:supportedByInstitution`

Institution(s) providing economic support (stipend, land endowment) or ritual support (priest salaries) for a Living Goddess during tenure. Extends Guthi role beyond structure management to person support.

| | |
|---|---|
| Range | [Guthi](classes.md#guthi) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Syncretic relationships

**IRI:** `https://cair-nepal.org/heritagegraph/syncretic_relationships` · `heritageGraph:syncretic_relationships`

Collection of SyncreticRelationship instances

| | |
|---|---|
| Range | [Syncretic Relationship](classes.md#syncreticrelationship) |
| Used in | used in axioms of [Container](classes.md#container) |

### techniques

**IRI:** `https://cair-nepal.org/heritagegraph/techniques` · `heritageGraph:techniques`

Collection of Technique instances

| | |
|---|---|
| Range | [Technique](classes.md#e29_design_or_procedure) |
| Used in | used in axioms of [Container](classes.md#container) |

### Time spans

**IRI:** `https://cair-nepal.org/heritagegraph/time_spans` · `heritageGraph:time_spans`

Collection of TimeSpan instances

| | |
|---|---|
| Range | [Time Span](classes.md#e52_time-span) |
| Used in | used in axioms of [Container](classes.md#container) |

### Took place at

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P7_took_place_at` · `crm:P7_took_place_at`

Place where the event occurred

| | |
|---|---|
| Sub-properties | [Route places](object-properties.md#routeplaces) |
| Used in | used in axioms of [Consecration](classes.md#consecration); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Transferred from actor

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P28_custody_surrendered_by` · `crm:P28_custody_surrendered_by`

Previous custodian

### Transferred object

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P30_transferred_custody_of` · `crm:P30_transferred_custody_of`

Object transferred in custody event

### Transferred to actor

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P29_custody_received_by` · `crm:P29_custody_received_by`

New custodian (person or group)

| | |
|---|---|
| Sub-properties | [Transferred to guthi](object-properties.md#transferredtoguthi) |

### Transferred to guthi

**IRI:** `https://cair-nepal.org/heritagegraph/transferredToGuthi` · `heritageGraph:transferredToGuthi`

New custodian (Guthi)

| | |
|---|---|
| Super-properties | [Transferred to actor](object-properties.md#p29_custody_received_by) |
| Range | [Guthi](classes.md#guthi) |

### used

**IRI:** `http://www.w3.org/ns/prov#used` · `prov:used`

Entity used by this activity.

| | |
|---|---|
| Used in | used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### Used by

**IRI:** `https://cair-nepal.org/heritagegraph/usedBy` · `heritageGraph:usedBy`

Actor(s) who use, handle, or are responsible for this object in ritual contexts

| | |
|---|---|
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Iconographic Object](classes.md#iconographicobject) |

### Used materials

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P125_used_object_of_type` · `crm:P125_used_object_of_type`

Ephemeral materials consumed during the ritual (e.g., oil, rice).

| | |
|---|---|
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Used technique

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P33_used_specific_technique` · `crm:P33_used_specific_technique`

Craft technique used in production

### Verified assertion

**IRI:** `https://cair-nepal.org/heritagegraph/verifiedAssertion` · `heritageGraph:verifiedAssertion`

Assertions verified by this activity

| | |
|---|---|
| Range | [Assertion](classes.md#i2_belief) |
| Used in | used in axioms of [Verification](classes.md#verification) |

### Verified by expert

**IRI:** `https://cair-nepal.org/heritagegraph/verifiedByExpert` · `heritageGraph:verifiedByExpert`

Expert who performed verification

| | |
|---|---|
| Super-properties | [Carried out by](object-properties.md#p14_carried_out_by) |
| Range | [Person](classes.md#e21_person) |
| Used in | used in axioms of [Verification](classes.md#verification) |

### Was associated with

**IRI:** `http://www.w3.org/ns/prov#wasAssociatedWith` · `prov:wasAssociatedWith`

Agent associated with responsibility for this activity.

| | |
|---|---|
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |

### Was attributed to

**IRI:** `http://www.w3.org/ns/prov#wasAttributedTo` · `prov:wasAttributedTo`

Agent to whom responsibility for this entity is attributed.

### Was derived from

**IRI:** `http://www.w3.org/ns/prov#wasDerivedFrom` · `prov:wasDerivedFrom`

Entity from which this entity was derived.

### Was documented by

**IRI:** `https://cair-nepal.org/heritagegraph/documentedBy` · `heritageGraph:documentedBy`

Documentation event that recorded this (pre-existing) entity or event. Uses heritageGraph:documentedBy (aligned to prov:wasInfluencedBy). NOTE: prov:wasGeneratedBy was incorrect: a stupa is not *generated by* the survey that records it.

| | |
|---|---|
| Super-properties | [Was influenced by](object-properties.md#wasinfluencedby) |
| Range | [Documentation Activity](classes.md#documentationactivity) |
| Inverse of | [documents](object-properties.md#documents) |
| Used in | used in axioms of [Information Object](classes.md#informationobject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |
| prov alignment | prov:wasInfluencedBy |

### Was generated by

**IRI:** `http://www.w3.org/ns/prov#wasGeneratedBy` · `prov:wasGeneratedBy`

Activity that generated this entity.

| | |
|---|---|
| Inverse of | [generated](object-properties.md#generated) |
| Used in | used in axioms of [Information Object](classes.md#informationobject) |

### Was influenced by

**IRI:** `http://www.w3.org/ns/prov#wasInfluencedBy` · `prov:wasInfluencedBy`

General PROV-O influence relation. Prefer a more specific PROV relation whenever one applies.

| | |
|---|---|
| Sub-properties | [Was documented by](object-properties.md#documentedby) |

### Was informed by

**IRI:** `http://www.w3.org/ns/prov#wasInformedBy` · `prov:wasInformedBy`

Activity that informed this activity; PROV-O uses this when the intervening generated and used entity is unknown or omitted.

### Was present at

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P12i_was_present_at` · `crm:P12i_was_present_at`

Generic CRM presence relation (P12i): event this entity was present at. Canonical holder of the CRM predicate; use the specific slots in data.

| | |
|---|---|
| Sub-properties | [Is invoked in ritual](object-properties.md#isinvokedinritual), [Participates in ritual](object-properties.md#participatesinritual) |

### Was produced by event

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P108i_was_produced_by` · `crm:P108i_was_produced_by`

Event that created this object or structure

| | |
|---|---|
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Iconographic Object](classes.md#iconographicobject) |

