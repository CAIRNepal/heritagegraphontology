# Changelog: 1.0.1 → 1.1.0

## Added (73)

- **Access Protocol** (`heritageGraph:AccessProtocol`, class)
- **Access Protocol (concept scheme)** (`https://cair-nepal.org/heritagegraph/scheme/AccessProtocol`, concept scheme)
- **Access Rights** (`dcterms:accessRights`, object property)
- **Acquisition** (`crm:E8_Acquisition`, class)
- **Activity** (`crm:E7_Activity`, class)
- **Alienation of an endowment** (`https://cair-nepal.org/heritagegraph/EndowmentEventType#Alienation`, concept)
- **Attribute Assignment** (`crm:E13_Attribute_Assignment`, class)
- **Augmentation of an endowment** (`https://cair-nepal.org/heritagegraph/EndowmentEventType#Augmentation`, concept)
- **Community Use Only** (`https://cair-nepal.org/heritagegraph/AccessProtocol#CommunityUseOnly`, concept)
- **Concerns endowment** (`heritageGraph:concernsEndowment`, object property)
- **Confidence method** (`heritageGraph:confidenceMethod`, object property)
- **Custody closed by** (`heritageGraph:custodyClosedBy`, object property)
- **Custody holder** (`heritageGraph:custodyHolder`, object property)
- **Custody object** (`heritageGraph:custodyObject`, object property)
- **Custody opened by** (`heritageGraph:custodyOpenedBy`, object property)
- **Custody Period** (`heritageGraph:CustodyPeriod`, class)
- **Death** (`crm:E69_Death`, class)
- **destroyed** (`crm:P13_destroyed`, object property)
- **died in** (`crm:P100i_died_in`, object property)
- **domainIncludes** (`schema1:domainIncludes`, annotation property)
- **Duty for** (`heritageGraph:dutyFor`, object property)
- **editorialNote** (`skos:editorialNote`, annotation property)
- **Endowed land** (`heritageGraph:endowedLand`, object property)
- **Endowment** (`heritageGraph:Endowment`, class)
- **Endowment donor** (`heritageGraph:endowmentDonor`, object property)
- **Endowment Event** (`heritageGraph:EndowmentEvent`, class)
- **Endowment Event Type** (`heritageGraph:EndowmentEventType`, class)
- **Endowment Event Type (concept scheme)** (`https://cair-nepal.org/heritagegraph/scheme/EndowmentEventType`, concept scheme)
- **Endowment recipient** (`heritageGraph:endowmentRecipient`, object property)
- **Event** (`crm:E5_Event`, class)
- **falls within** (`crm:P86_falls_within`, object property)
- **Founding of an endowment** (`https://cair-nepal.org/heritagegraph/EndowmentEventType#Founding`, concept)
- **Group** (`crm:E74_Group`, class)
- **has access protocol** (`heritageGraph:accessProtocol`, object property)
- **has endowment event type** (`heritageGraph:endowmentEventType`, object property)
- **has structure type** (`heritageGraph:structureType`, object property)
- **Hereditary Role Tenure** (`heritageGraph:HereditaryRoleTenure`, class)
- **Information Object** (`crm:E73_Information_Object`, class)
- **Initiates Only** (`https://cair-nepal.org/heritagegraph/AccessProtocol#InitiatesOnly`, concept)
- **Legal Object** (`crm:E72_Legal_Object`, class)
- **Mandated by** (`heritageGraph:mandatedBy`, object property)
- **Month** (`https://cair-nepal.org/heritagegraph/DatePrecision#Month`, concept)
- **Nationalisation of an endowment** (`https://cair-nepal.org/heritagegraph/EndowmentEventType#Nationalisation`, concept)
- **Office** (`heritageGraph:Office`, class)
- **Open** (`https://cair-nepal.org/heritagegraph/AccessProtocol#Open`, concept)
- **Period** (`crm:E4_Period`, class)
- **Physical Human-Made Thing** (`crm:E24_Physical_Human-Made_Thing`, class)
- **place is defined by** (`crm:P168_place_is_defined_by`, datatype property)
- **Proposition Set** (`crminf:I4_Proposition_Set`, class)
- **Reconstructed** (`https://cair-nepal.org/heritagegraph/ExistenceStatus#Reconstructed`, concept)
- **Recorded date** (`heritageGraph:recordedDate`, datatype property)
- **right held by** (`crm:P105_right_held_by`, object property)
- **Ritual Office** (`heritageGraph:RitualOffice`, class)
- **Role duty** (`heritageGraph:roleDuty`, datatype property)
- **Role holder** (`heritageGraph:roleHolder`, object property)
- **Seasonal** (`https://cair-nepal.org/heritagegraph/AccessProtocol#Seasonal`, concept)
- **Secret Sacred** (`https://cair-nepal.org/heritagegraph/AccessProtocol#SecretSacred`, concept)
- **State Heritage Authority** (`heritageGraph:StateHeritageAuthority`, class)
- **Structure Type** (`heritageGraph:StructureType`, class)
- **succeeds** (`heritageGraph:succeeds`, object property)
- **Succession rule** (`heritageGraph:successionRule`, datatype property)
- **sustains** (`heritageGraph:sustains`, object property)
- **Tenure** (`heritageGraph:Tenure`, class)
- **Tenure closed by** (`heritageGraph:tenureClosedBy`, object property)
- **Tenure Event** (`heritageGraph:TenureEvent`, class)
- **Tenure holder** (`heritageGraph:tenureHolder`, object property)
- **Tenure office** (`heritageGraph:tenureOffice`, object property)
- **Tenure opened by** (`heritageGraph:tenureOpenedBy`, object property)
- **transferred title from** (`crm:P23_transferred_title_from`, object property)
- **transferred title to** (`crm:P22_transferred_title_to`, object property)
- **Type** (`crm:E55_Type`, class)
- **was born** (`crm:P98i_was_born`, object property)
- **was motivated by** (`crm:P17_was_motivated_by`, object property)

## Removed (2)

- **permissible_values** (`linkml:permissible_values`, annotation property)
- **Place coordinates** (`geo:asWKT`, datatype property)

## Modified (330)

- **Ontology metadata** (`https://cair-nepal.org/heritagegraph/ontology`, ontology)
  - ➕ dcterms:bibliographicCitation: "Karki, N., Oli, N., Sapkota, A., Chhetri, T. R., & Yumusak, S. (2026). HeritageGraph Ontology (Version 1.1.0). CAIR-Nepal. https://doi.org/10.5281/zenodo.23435676"
  - ➕ dcterms:creator: https://orcid.org/0000-0002-3905-7878
  - ➕ dcterms:creator: https://orcid.org/0000-0002-8878-4991
  - ➕ dcterms:creator: https://orcid.org/0009-0000-7679-0107
  - ➕ dcterms:creator: https://orcid.org/0009-0004-5297-5990
  - ➕ dcterms:creator: https://orcid.org/0009-0007-3770-4668
  - ➕ dcterms:modified: "2026-11-26"^^xsd:date
  - ➕ owl:priorVersion: https://cair-nepal.org/heritagegraph/ontology/1.0.1
  - ➕ owl:versionIRI: https://cair-nepal.org/heritagegraph/ontology/1.1.0
  - ➕ owl:versionInfo: "1.1.0"
  - ➕ pav:version: "1.1.0"
  - ➕ vann:preferredNamespacePrefix: "hg"
  - ➖ dcterms:bibliographicCitation: "Karki, N., Oli, N., Sapkota, A., Yumusak, S., & Chhetri, T. R. (2026). HeritageGraph Ontology (Version 1.0.1). CAIR-Nepal. https://doi.org/10.5281/zenodo.23435676"
  - ➖ dcterms:creator: "Anu Sapkota"
  - ➖ dcterms:creator: "Nabin Oli"
  - ➖ dcterms:creator: "Niraj Karki"
  - ➖ dcterms:creator: "Semih Yumusak"
  - ➖ dcterms:creator: "Tek Raj Chhetri"
  - ➖ dcterms:modified: "2026-11-22"^^xsd:date
  - ➖ owl:priorVersion: https://cair-nepal.org/heritagegraph/ontology/1.0.0
  - ➖ owl:versionIRI: https://cair-nepal.org/heritagegraph/ontology/1.0.1
  - ➖ owl:versionInfo: "1.0.1"
  - ➖ pav:version: "1.0.1"
  - ➖ vann:preferredNamespacePrefix: "heritageGraph"
- **Abhisheka** (`https://cair-nepal.org/heritagegraph/RitualType#Abhisheka`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Ritual bathing/anointing of deity."@en
  - ➖ skos:definition: "Ritual bathing/anointing of deity"@en
- **actedOnBehalfOf** (`prov:actedOnBehalfOf`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "actedOnBehalfOf"
  - ➕ skos:definition: "An object property to express the accountability of an agent towards another agent. The subordinate agent acted on behalf of the responsible agent in an actual activity."@en
  - ➖ rdfs:label: "Acted on behalf of"@en
  - ➖ skos:definition: "Agent on whose behalf this agent acted."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Activity** (`prov:Activity`, class)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "Activity"
  - ➕ skos:definition: "An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities."
  - ➖ rdfs:label: "Activity"@en
  - ➖ skos:definition: "Direct LinkML representation of prov:Activity. Applied to events and processes that use, transform, generate, document, assess, or verify entities."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Actor** (`crm:E39_Actor`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ skos:definition: "Scope note:
This class comprises people, either individually or in groups, who have the potential to perform intentional actions of kinds for which they can be held responsible.

Examples:
- London and Continental Railways (E74)
- the Governor of the Bank of England in 1975 (E21)
- Sir Ian McKellen (E21) (Gibson, 1986)

In First Order Logic:
- E39(x) ⇒ E77(x)"@en
  - ➖ rdfs:subClassOf: prov:Agent
  - ➖ skos:definition: "General actor (person or group) responsible for events"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Age Criterion** (`heritageGraph:AgeCriterion`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **Agent** (`prov:Agent`, class)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "Agent"
  - ➕ skos:definition: "An agent is something that bears some form of responsibility for an activity taking place, for the existence of an entity, or for another agent's activity."@en
  - ➖ rdfs:label: "Agent"@en
  - ➖ skos:definition: "Direct LinkML representation of prov:Agent. Agents bear responsibility for activities or entities. PROV-O permits an individual agent also to be typed as an Entity, but does not define every Agent as a subclass of Entity."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Appropriation** (`https://cair-nepal.org/heritagegraph/SyncreticType#Appropriation`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Claimed adoption: one tradition is held to have taken the deity over from the other."@en
  - ➖ skos:definition: "Deity borrowed from one tradition into another"@en
- **Architectural Element** (`heritageGraph:ArchitecturalElement`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E24_Physical_Human-Made_Thing
  - ➕ skos:definition: "Carved or constructed component of an architectural structure (e.g., Gajur, Torana, Tundal)."@en
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: crm:P46i_forms_part_of max 1
  - ➖ rdfs:subClassOf: crm:P46i_forms_part_of only heritageGraph:ArchitecturalStructure
  - ➖ skos:definition: "Carved or constructed component of an architectural structure (e.g., Gajur, Torana, Tundal)"@en
- **Architectural Structure** (`heritageGraph:ArchitecturalStructure`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: heritageGraph:hasReligiousTradition only heritageGraph:ReligiousTradition
  - ➕ rdfs:subClassOf: heritageGraph:structureType only heritageGraph:StructureType
  - ➖ rdfs:subClassOf: crm:P108i_was_produced_by min 0
  - ➖ rdfs:subClassOf: crm:P108i_was_produced_by only crm:E12_Production
  - ➖ rdfs:subClassOf: crm:P34i_was_assessed_by min 0
  - ➖ rdfs:subClassOf: crm:P34i_was_assessed_by only crm:E14_Condition_Assessment
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: crm:P46_is_composed_of min 0
  - ➖ rdfs:subClassOf: crm:P46_is_composed_of only heritageGraph:ArchitecturalElement
  - ➖ rdfs:subClassOf: crm:P55_has_current_location max 1
  - ➖ rdfs:subClassOf: crm:P55_has_current_location min 0
  - ➖ rdfs:subClassOf: crm:P55_has_current_location only crm:E53_Place
  - ➖ rdfs:subClassOf: heritageGraph:destructionEvent min 0
  - ➖ rdfs:subClassOf: heritageGraph:existenceStatus min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasArchitecturalStyle min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasAssertion min 0
  - ➖ rdfs:subClassOf: heritageGraph:hypothesizedLocation min 0
  - ➖ rdfs:subClassOf: heritageGraph:lastKnownExistenceDate min 0
  - ➖ rdfs:subClassOf: heritageGraph:managedByGuthi min 0
  - ➖ rdfs:subClassOf: heritageGraph:mentionedInSource min 0
  - ➖ skos:broadMatch: crm:E22_Human-Made_Object
- **Architectural structures** (`heritageGraph:architecturalStructures`, object property)
  - ➕ rdfs:domain: crm:E6_Destruction or heritageGraph:HistoricalEvent
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Heritage structures affected by or present during this historical event."@en
  - ➖ skos:definition: "Heritage structures affected by or present during this historical event"@en
- **Architectural Style** (`heritageGraph:ArchitecturalStyle`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E55_Type
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Chaitya
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Dome
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Pagoda
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Shikhara
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Stupa
  - ➖ skos:broadMatch: crm:E55_Type
- **Archival Record** (`heritageGraph:ArchivalRecord`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Government or institutional administrative record."@en
  - ➖ skos:definition: "Government or institutional administrative record"@en
- **Assertion Subject** (`heritageGraph:AssertionSubject`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➖ rdfs:subClassOf: crm:E22_Human-Made_Object or heritageGraph:ArchitecturalElement or heritageGraph:Deity or heritageGraph:ReligiousTradition or heritageGraph:HistoricalEvent or heritageGraph:RitualEvent or crm:E12_Production or heritageGraph:Consecration or heritageGraph:Enshrinement or crm:E10_Transfer_of_Custody or crm:E14_Condition_Assessment or crm:E3_Condition_State or crm:E39_Actor or crm:E53_Place or crm:E52_Time-Span or heritageGraph:DataSource or heritageGraph:DocumentationActivity or heritageGraph:SyncreticRelationship or heritageGraph:KumariTenure or crm:E29_Design_or_Procedure or crm:E57_Material or heritageGraph:KumariRole or heritageGraph:SelectionCriterion or crminf:I2_Belief or heritageGraph:CalendarSystem
- **Asserts about** (`heritageGraph:assertsAbout`, object property)
  - ➕ rdfs:domain: crminf:I2_Belief
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **Assesses candidate** (`heritageGraph:assessesCandidate`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:RitualAssessment
- **assigned** (`crm:P141_assigned`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "assigned"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property associates an instance of E13 Attribute Assignment with the instance of E1 CRM Entity used in the attribution. The instance of E1 CRM Entity here plays the role of the range of the attribution.
The kind of attribution made should be documented using P177 assigned property of type (is type of property assigned).

Examples:
- The Current Ownership Assessment of Martin Doerr’s silver cup February 1997 (E13) assigned Martin Doerr (E21). (fictitious)
- The Identifier Assignment on 1(st) June 1997 of the silver cup donated by Martin Doerr (E15) assigned 232 (E42). (fictitious)
- The examination of MS Sinai Greek 418 (E13) assigned unsupported (E55.) (Honey &amp; Pickwoad, 2010)

In First Order Logic:
- P141(x,y) ⇒ E13(x)
- P141(x,y) ⇒ E1(y)"@en
  - ➖ rdfs:label: "Assigned equivalent"@en
  - ➖ skos:definition: "The deity or sacred figure being identified as equivalent to the primary deity."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **assigned attribute to** (`crm:P140_assigned_attribute_to`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "assigned attribute to"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property associates an instance of E13 Attribute Assignment with the instance of E1 CRM Entity about which it made an attribution. The instance of E1 CRM Entity plays the role of the domain of the attribution. 
The kind of attribution made should be documented using P177 assigned property of type (is type of property assigned).

Examples:
- The Current Ownership Assessment of Martin Doerr’s silver cup February 1997 (E13) assigned attribute to Martin Doerr’s silver cup (E22). (fictitious)
- The Identifier Assignment on 1(st) June 1997 of the silver cup donated by Martin Doerr (E15) assigned attribute to silver cup 232 (E22). (fictitious)
- The examination of MS Sinai Greek 418 (E13) assigned attribute to MS Sinai Greek 418 (E22). (Honey and Pickwoad, 2010)

In First Order Logic:
- P140(x,y) ⇒ E13(x)
- P140(x,y) ⇒ E1(y)"@en
  - ➖ rdfs:label: "Assigned to deity"@en
  - ➖ skos:definition: "The deity instance that is the subject of the syncretic claim."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Assumes role** (`heritageGraph:assumesRole`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subPropertyOf: heritageGraph:tenureOffice
  - ➕ schema1:domainIncludes: heritageGraph:KumariTenure
- **begin of the begin** (`crm:P82a_begin_of_the_begin`, datatype property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "begin of the begin"@en
  - ➖ rdfs:label: "Date earliest"@en
  - ➖ skos:definition: "Earliest possible date (for uncertain dates)"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Belief** (`crminf:I2_Belief`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/extensions/crminf/
  - ➕ rdfs:label: "Belief"@en
  - ➕ skos:definition: "This class comprises the notion that the associated I4 Proposition Set is held to have a particular I6 Belief Value by a particular E39 Actor. This can be understood as the period of time that an individual group holds a particular set of propositions to be true, false, or somewhere in between."@en
  - ➖ heritageGraph:crminf_pattern: "I2_Belief -J4_that-> I4_Proposition_Set; evidence via I5_Inference_Making (J1_used_as_premise / J2_concluded_that); expert re-check via I7_Belief_Adoption"
  - ➖ rdfs:label: "Assertion"@en
  - ➖ rdfs:subClassOf: prov:Entity
  - ➖ skos:definition: "A provenance-bearing belief or claim about a heritage entity or event. The assertion is represented as CRMinf I2 Belief and as a prov:Entity, allowing source, attribution, generation time, revision, confidence, and reconciliation status to be recorded explicitly."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Bhajan** (`https://cair-nepal.org/heritagegraph/RitualType#Bhajan`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Devotional singing ritual."@en
  - ➖ skos:definition: "Devotional singing ritual"@en
- **Birth timespan** (`heritageGraph:birthTimespan`, object property)
  - ➕ owl:propertyChainAxiom: [anonymous]
  - ➕ rdfs:domain: crm:E21_Person
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Person's birth timespan (shortcut for crm:P98i_was_born / crm:P4_has_time-span)."@en
  - ➖ rdfs:subPropertyOf: crm:P4_has_time-span
  - ➖ skos:definition: "Person's birth timespan"@en
- **Bounds tenure** (`heritageGraph:boundsTenure`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariLifecycleEvent
  - ➕ skos:definition: "The KumariTenure period that this lifecycle event bounds (initiates or terminates). Specialized by hg:initiatedTenure (selection) and hg:endedTenureOf (retirement)."@en
  - ➖ skos:definition: "The KumariTenure period that this lifecycle event bounds (initiates or terminates). Specialized by initiated_tenure (selection) and ended_tenure_of (retirement)."@en
- **Calendar System** (`heritageGraph:CalendarSystem`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Calendar reckoning system with conversion rules for multi-calendar temporal reasoning."@en
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:epochDateGregorian min 0
  - ➖ rdfs:subClassOf: heritageGraph:isPrimaryForTradition min 0
  - ➖ rdfs:subClassOf: heritageGraph:yearOffsetFromGregorian min 0
  - ➖ skos:definition: "Calendar reckoning system with conversion rules for multi-calendar temporal reasoning"@en
- **carried out by** (`crm:P14_carried_out_by`, object property)
  - ➕ owl:inverseOf: crm:P14i_performed
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "carried out by"@en
  - ➕ skos:definition: "Quantification: many to many, necessary (1,n:0,n)

Scope note:
This property describes the active participation of an instance of E39 Actor in an instance of E7 Activity. 
It implies causal or legal responsibility. The P14.1 in the role of property of the property specifies the nature of an Actor’s participation.

Examples:
- The painting of the Sistine Chapel (E7) carried out by Michelangelo Buonaroti (E21) in the role of master craftsman (E55). (Goldscheider, 1953)

Properties:
- P14.1 in the role of: E55 Type

In First Order Logic:
- P14(x,y) ⇒ E7(x)
- P14(x,y)⇒ E39(y)
- P14(x,y) ⇒ P11(x,y)
- P14(x,y,z) ⇒ [P14(x,y) ∧ E55(z)]"@en
  - ➖ rdfs:label: "Carried out by"@en
  - ➖ skos:definition: "Actor(s) who performed this event"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Caste Group** (`heritageGraph:CasteGroup`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E74_Group
  - ➕ rdfs:subClassOf: heritageGraph:traditionalRole only rdf:PlainLiteral
  - ➕ skos:definition: "Hereditary social group (Jati) with specific ritual roles and occupational duties."@en
  - ➖ rdfs:subClassOf: crm:E39_Actor
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:traditionalRole max 1
  - ➖ rdfs:subClassOf: heritageGraph:traditionalRole min 0
  - ➖ rdfs:subClassOf: heritageGraph:traditionalRole only xsd:string
  - ➖ skos:broadMatch: crm:E74_Group
  - ➖ skos:definition: "Hereditary social group (Jati) with specific ritual roles and occupational duties"@en
- **Century** (`https://cair-nepal.org/heritagegraph/DatePrecision#Century`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Within century range."@en
  - ➖ skos:definition: "Within century range"@en
- **Chaitya** (`heritageGraph:Chaitya`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Buddhist votive shrine (chaitya); votive stupa form found across the Kathmandu Valley. In Newar usage chaitya (Newar chibhah) also names great stupas (Swayambhu Mahachaitya), so a monument may be both a Stupa and a Chaitya."@en
  - ➖ skos:definition: "Buddhist votive shrine (chaitya); votive stupa form found across the Kathmandu Valley."@en
- **Chariot Festival** (`heritageGraph:ChariotFestival`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Festival involving ceremonial chariot procession (e.g., Rato Machhindranath Jatra)."@en
  - ➖ skos:definition: "Festival involving ceremonial chariot procession (e.g., Rato Machhindranath Jatra)"@en
- **Chariot Procession** (`https://cair-nepal.org/heritagegraph/RitualType#ChariotProcession`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Ritual chariot pulling."@en
  - ➖ skos:definition: "Ritual chariot pulling"@en
- **Circa** (`https://cair-nepal.org/heritagegraph/DatePrecision#Circa`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Approximate date."@en
  - ➖ skos:definition: "Approximate date"@en
- **Circumambulation** (`https://cair-nepal.org/heritagegraph/RitualType#Circumambulation`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Ritual circular movement around sacred site."@en
  - ➖ skos:definition: "Ritual circular movement around sacred site"@en
- **Commissioned by** (`heritageGraph:commissionedBy`, object property)
  - ➕ rdfs:domain: crm:E12_Production
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Person or group who commissioned production."@en
  - ➖ skos:definition: "Person or group who commissioned production"@en
- **concerned** (`crm:P34_concerned`, object property)
  - ➕ owl:inverseOf: crm:P34i_was_assessed_by
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "concerned"@en
  - ➕ skos:definition: "Quantification: many to many, necessary (1,n:0,n)

Scope note:
This property identifies the instance of E18 Physical Thing that was assessed during an instance of E14 Condition Assessment. 
Conditions may be assessed either by direct observation or using recorded evidence. In the latter case the instance of E18 Physical Thing does not need to be present or extant at the time of assessment.

Examples:
- The condition assessment of the silver collection in 1997 (E14) concerned silver cup 232 (E22). (fictitious)
- The condition assessment of the cover of MS Sinai Greek 418 (E14) concerned the cover of MS Sinai Greek 418 (E22). (Honey and Pickwoad, 2010)
- The condition assessment of the endband cores of MS Sinai Greek 418 (E14) concerned the endband cores of MS Sinai Greek 418 (E22). (Honey and Pickwoad, 2010)

In First Order Logic:
- P34(x,y) ⇒ E14(x)
- P34(x,y) ⇒ E18(y) 
- P34(x,y) ⇒ P140(x,y)"@en
  - ➖ rdfs:label: "Assessed object"@en
  - ➖ skos:definition: "Object assessed for condition"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Condition Assessment** (`crm:E14_Condition_Assessment`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ skos:definition: "Scope note:
This class describes the act of assessing the state of preservation of an object during a particular period. 
The condition assessment may be carried out by inspection, measurement, or through historical research. This class is used to document circumstances of the respective assessment that is relevant to interpret its quality at a later stage, or to continue research on related documents.

Examples:
- last year’s inspection of humidity damage to the frescos in the St. George chapel in our village (fictitious)
- the condition assessment of the endband cores of MS Sinai Greek 418 by Nicholas Pickwoad in November 2003 (Honey &amp; Pickwoad, 2010)
- the condition assessment of the cover of MS Sinai Greek 418 by Nicholas Pickwoad in November 2003 (Honey &amp; Pickwoad, 2010)

In First Order Logic:
- E14(x) ⇒ E13(x)"@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: prov:Activity
  - ➖ skos:definition: "Event of evaluating the physical state of a heritage object or structure"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Condition State** (`crm:E3_Condition_State`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ skos:definition: "Scope note:
This class comprises the states of objects characterised by a certain condition over a time-span. 
An instance of this class describes the prevailing physical condition of any material object or feature during a specific instance of E52 Time-Span. In general, the time-span for which a certain condition can be asserted may be shorter than the real time-span, for which this condition held.
The nature of that condition can be described using P2 has type. For example, the instance of E3 Condition State “condition of the SS Great Britain between 22(nd) September 1846 and 27(th) August 1847” can be characterized as an instance “wrecked” of E55 Type.

Examples:
- the "reconstructed" state of the “Amber Room” in Tsarskoje Selo from summer 2003 until now (Owen, 2009)
- the "ruined" state of Peterhof Palace near Saint Petersburg from 1944 to 1946 (Maddox, 2015)
- the state of my turkey in the oven at 14:30 on 25(th) December 2002 [P2 has type: E55 Type “still not cooked”] (fictitious)
- the topography of the leaves of Sinai Printed Book 3234.2361 on the 10(th) July 2007 [described as: of type "cockled"] (fictitious)

In First Order Logic:
- E3(x) ⇒ E2(x)"@en
  - ➖ rdfs:subClassOf: prov:Entity
  - ➖ skos:definition: "A physical condition state of a heritage object"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Condition Type** (`heritageGraph:ConditionType`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E55_Type
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ConditionType#Damaged
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ConditionType#Good
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ConditionType#Restored
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ConditionType#Ruined
- **Confers role** (`heritageGraph:confersRole`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariEnthronementEvent
  - ➕ schema1:domainIncludes: heritageGraph:KumariSelectionEvent
- **Confidence score** (`heritageGraph:confidenceScore`, datatype property)
  - ➕ rdfs:domain: crminf:I2_Belief
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Degree of belief, between 0 and 1, that the asserted value is correct: 1 = certain, 0.5 = undecided, 0 = believed false. The assessor is either the agent the assertion is attributed to (prov:wasAttributedTo) or the activity that generated the assertion (prov:wasGeneratedBy), e.g. an extraction that codes how firmly the source states the claim; hg:confidenceMethod says which, and by what rubric. Scores are comparable only when they share an assessor or a method."@en
  - ➕ skos:relatedMatch: crminf:J5_holds_to_be
  - ➖ skos:definition: "Reliability score for assertion (0.0-1.0)"@en
- **Consecrated by event** (`heritageGraph:consecratedByEvent`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Murti
  - ➕ skos:definition: "Consecration event that activated this murti."@en
  - ➖ owl:inverseOf: crm:P16_used_specific_object
  - ➖ skos:definition: "Consecration event that activated this murti"@en
- **Consecration** (`heritageGraph:Consecration`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E7_Activity
  - ➕ rdfs:subClassOf: heritageGraph:RitualEvent
  - ➕ skos:definition: "Ritual event that transforms an object into a sacred vessel (e.g., Prana Pratistha for Murti)."@en
  - ➕ skos:editorialNote: "PROV-O alignment note: prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by min 0
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by only crm:E39_Actor
  - ➖ rdfs:subClassOf: crm:P16_used_specific_object max 1
  - ➖ rdfs:subClassOf: crm:P16_used_specific_object min 0
  - ➖ rdfs:subClassOf: crm:P16_used_specific_object only heritageGraph:Murti
  - ➖ rdfs:subClassOf: crm:P4_has_time-span min 0
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: crm:P7_took_place_at max 1
  - ➖ rdfs:subClassOf: crm:P7_took_place_at min 0
  - ➖ rdfs:subClassOf: crm:P7_took_place_at only crm:E53_Place
  - ➖ rdfs:subClassOf: heritageGraph:makesDeityPresent min 0
  - ➖ skos:broadMatch: crm:E7_Activity
  - ➖ skos:definition: "Ritual event that transforms an object into a sacred vessel (e.g., Prana Pratistha for Murti)"@en
- **consists of** (`crm:P9_consists_of`, object property)
  - ➕ owl:inverseOf: crm:P9i_forms_part_of
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "consists of"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property associates an instance of E4 Period with another instance of E4 Period that is defined by a subset of the phenomena that define the former. Therefore, the spacetime volume of the latter must fall within the spacetime volume of the former.
This property is transitive and asymmetric.

Examples:
- Cretan Bronze Age (E4) consists of Middle Minoan (E4). (Hood, 1971)

In First Order Logic:
- P9(x,y) ⇒ E4(x)
- P9(x,y) ⇒ E4(y)
- P9(x,y) ⇒ P10(y,x)
- [P9(x,y) ∧ P9(y,z)] ⇒ P9(x,z)
- P9(x,y) ⇒ ¬P9(y,x)"@en
  - ➖ rdfs:label: "Includes ritual event"@en
  - ➖ skos:definition: "Component rituals of festival"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Custodian type** (`heritageGraph:custodianType`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ schema1:domainIncludes: heritageGraph:DataCustodian
  - ➕ skos:definition: "Type of custodian (government, academic, community), free text."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Type of custodian (government, academic, community), free text"@en
- **custody received by** (`crm:P29_custody_received_by`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "custody received by"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property identifies the instance(s) of E39 Actor who receive custody of an instance of E18 Physical Thing in an instance of E10 Transfer of Custody. 
The property will typically describe Actors receiving custody of an object when it is handed over from another Actor’s care. On occasion, physical custody may be received involuntarily or illegally, e.g. through accident, unsolicited donation, or theft.
In reality, custody is either transferred to someone or from someone, or both.

Examples:
- Representatives of The National Gallery (E74) received custody through the delivery of the paintings by Secure Deliveries Inc. to the National Gallery (E10).

In First Order Logic:
- P29(x,y) ⇒ E10(x)
- P29(x,y) ⇒ E39(y) 
- P29(x,y) ⇒ P14(x,y)"@en
  - ➖ rdfs:label: "Transferred to actor"@en
  - ➖ skos:definition: "New custodian (person or group)"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **custody surrendered by** (`crm:P28_custody_surrendered_by`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "custody surrendered by"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property identifies the instance(s) of E39 Actor who surrender custody of an instance of E18 Physical Thing in an instance of E10 Transfer of Custody. 
The property will typically describe an Actor surrendering custody of an object when it is handed over to someone else’s care. On occasion, physical custody may be surrendered involuntarily, e.g. through accident, loss, or theft.
In reality, custody is either transferred to someone or from someone, or both.

Examples:
- The Secure Deliveries Inc. crew (E74) surrendered custody through the delivery of the paintings by Secure Deliveries Inc. to the National Gallery (E10).

In First Order Logic:
- P28(x,y) ⇒ E10(x)
- P28(x,y) ⇒ E39(y) 
- P28(x,y) ⇒ P14(x,y)"@en
  - ➖ rdfs:label: "Transferred from actor"@en
  - ➖ skos:definition: "Previous custodian"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **custody transferred through** (`crm:P30i_custody_transferred_through`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "custody transferred through"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many, necessary (1,n:0,n)

Scope note of the inverse property:
This property identifies the instance(s) of E18 Physical Thing concerned in an instance of E10 Transfer of Custody. 
The property will typically describe the object that is handed over by an instance of E39 Actor to the custody of another instance of E39 Actor. On occasion, physical custody may be transferred involuntarily or illegally, e.g. through accident, unsolicited donation, or theft.

Examples of the inverse property:
- The delivery of the paintings by Secure Deliveries Inc. to the National Gallery (E10) transferred custody of paintings from The Iveagh Bequest (E19).

In First Order Logic of the inverse property:
- P30(x,y) ⇒ E10(x)
- P30(x,y) ⇒ E18(y)"@en
  - ➖ rdfs:label: "Has custody event"@en
  - ➖ skos:definition: "Custody transfer events for this structure"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Damaged** (`https://cair-nepal.org/heritagegraph/ConditionType#Damaged`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Partially damaged."@en
  - ➖ skos:definition: "Partially damaged"@en
- **Data Custodian** (`heritageGraph:DataCustodian`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: heritageGraph:custodianType only rdf:PlainLiteral
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:custodianType max 1
  - ➖ rdfs:subClassOf: heritageGraph:custodianType min 0
  - ➖ rdfs:subClassOf: heritageGraph:custodianType only xsd:string
- **Data quality note** (`heritageGraph:dataQualityNote`, datatype property)
  - ➕ rdfs:domain: crminf:I2_Belief
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ skos:definition: "Notes on data quality, completeness, or uncertainty."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Notes on data quality, completeness, or uncertainty"@en
- **Data Source** (`heritageGraph:DataSource`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E73_Information_Object
  - ➕ rdfs:subClassOf: heritageGraph:sourceCitation only rdf:PlainLiteral
  - ➕ skos:definition: "Original source from which heritage information was derived."@en
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:identifierScheme min 0
  - ➖ rdfs:subClassOf: heritageGraph:persistentIdentifier min 0
  - ➖ rdfs:subClassOf: heritageGraph:publicationTimespan min 0
  - ➖ rdfs:subClassOf: heritageGraph:resourceType min 0
  - ➖ rdfs:subClassOf: heritageGraph:sourceCitation max 1
  - ➖ rdfs:subClassOf: heritageGraph:sourceCitation min 0
  - ➖ rdfs:subClassOf: heritageGraph:sourceCitation only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:sourceCreator min 0
  - ➖ rdfs:subClassOf: heritageGraph:sourcePublisher min 0
  - ➖ rdfs:subClassOf: heritageGraph:sourceUrl min 0
  - ➖ rdfs:subClassOf: schema1:inLanguage max 1
  - ➖ rdfs:subClassOf: schema1:inLanguage min 0
  - ➖ rdfs:subClassOf: schema1:inLanguage only xsd:string
  - ➖ skos:broadMatch: crm:E73_Information_Object
  - ➖ skos:definition: "Original source from which heritage information was derived"@en
- **Datacite identifier** (`heritageGraph:persistentIdentifier`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:DataSource
  - ➕ skos:definition: "Persistent identifier for the source (DOI, archive ID, catalog number)."@en
  - ➖ skos:definition: "Persistent identifier for the source (DOI, archive ID, catalog number)"@en
- **Datacite identifier type** (`heritageGraph:identifierScheme`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:DataSource
  - ➕ skos:definition: "Type of identifier (DOI, ISBN, Handle, LocalArchiveID)."@en
  - ➖ skos:definition: "Type of identifier (DOI, ISBN, Handle, LocalArchiveID)"@en
- **Datacite publisher** (`heritageGraph:sourcePublisher`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:DataSource
  - ➕ skos:definition: "Entity responsible for making the source available."@en
  - ➖ skos:definition: "Entity responsible for making the source available"@en
- **Datacite resource type** (`heritageGraph:resourceType`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:DataSource
  - ➕ skos:definition: "High-level DataCite resource type (Dataset, Text, Image, Audio, Interview)."@en
  - ➖ skos:definition: "High-level DataCite resource type (Dataset, Text, Image, Audio, Interview)"@en
- **Date Precision** (`heritageGraph:DatePrecision`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E55_Type
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/DatePrecision#Century
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/DatePrecision#Circa
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/DatePrecision#Decade
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/DatePrecision#Exact
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/DatePrecision#Year
- **Death timespan** (`heritageGraph:deathTimespan`, object property)
  - ➕ owl:propertyChainAxiom: [anonymous]
  - ➕ rdfs:domain: crm:E21_Person
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Person's death timespan (shortcut for crm:P100i_died_in / crm:P4_has_time-span)."@en
  - ➖ rdfs:subPropertyOf: crm:P4_has_time-span
  - ➖ skos:definition: "Person's death timespan"@en
- **Decade** (`https://cair-nepal.org/heritagegraph/DatePrecision#Decade`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Within 10-year range."@en
  - ➖ skos:definition: "Within 10-year range"@en
- **Deinstallation Ritual** (`https://cair-nepal.org/heritagegraph/RitualType#DeinstallationRitual`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "De-installation/conclusion ritual."@en
  - ➖ skos:definition: "De-installation/conclusion ritual"@en
- **Deity** (`heritageGraph:Deity`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:closeMatch: aat:300343850
  - ➕ skos:closeMatch: dbo:Deity
  - ➕ skos:closeMatch: wikidata:Q178885
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: crm:P62i_is_depicted_by min 0
  - ➖ rdfs:subClassOf: crm:P62i_is_depicted_by only heritageGraph:IconographicObject
  - ➖ rdfs:subClassOf: heritageGraph:hasReligiousTradition min 0
  - ➖ rdfs:subClassOf: heritageGraph:isEnshrinedThroughEvent min 0
  - ➖ rdfs:subClassOf: heritageGraph:isInvokedInRitual min 0
  - ➖ skos:exactMatch: aat:300343850
  - ➖ skos:exactMatch: dbo:Deity
  - ➖ skos:exactMatch: wikidata:Q178885
- **Deity guthi** (`https://cair-nepal.org/heritagegraph/GuthiType#TempleGuthi`, concept)
  - ➕ dcterms:title: "Deity guthi"@en
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "Deity guthi"@en
  - ➕ skos:definition: "Deity guthi (dyah guthi): an association, usually endowed with land, that keeps up the worship and the festival of a deity at its temple or shrine."@en
  - ➕ skos:prefLabel: "Deity guthi"@en
  - ➖ rdfs:label: "Temple Guthi"@en
  - ➖ skos:definition: "Temple maintenance trust"@en
  - ➖ skos:prefLabel: "Temple Guthi"@en
- **depicts** (`crm:P62_depicts`, object property)
  - ➕ owl:inverseOf: crm:P62i_is_depicted_by
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "depicts"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property identifies something that is depicted by an instance of E24 Physical Human-Made Thing. Depicting is meant in the sense that an instance of E24 Physical Human-Made Thing intentionally shows, through its optical qualities or form, a representation of the entity depicted. Photographs are by default regarded as being intentional in this sense. Anything that is designed to change the properties of the depiction, such as an e-book reader, is specifically excluded. The property does not pertain to inscriptions or any other information encoding.
This property is a shortcut of the more fully developed path from E24 Physical Human-Made Thing through P65 shows visual item, E36 Visual Item, P138 represents to E1 CRM Entity. P62.1 mode of depiction allows the nature of the depiction to be refined.

Examples:
- The painting “La Liberté guidant le peuple” by Eugène Delacroix (E22) depicts the French “July Revolution” of 1830 (E7). (Delacroix, 1982)
- The 20 pence coin held by the Department of Coins and Medals of the British Museum under registration number 2006,1101.126 (E22) depicts Queen Elizabeth II (E21) mode of depiction Profile (E55).

Properties:
- P62.1 mode of depiction: E55 Type

In First Order Logic:
- P62(x,y) ⇒ E24(x)
- P62(x,y) ⇒ E1(y) 
- P62(x,y,z) ⇒ [P62(x,y) ∧ E55(z)]
- P62(x,y) ⇐ (∃z) [E36(z) ˄ P65(x,z) ˄ P138(z,y)]"@en
  - ➖ rdfs:label: "Depicts deity"@en
  - ➖ skos:definition: "Deity depicted iconographically (not cultic presence)"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Design or Procedure** (`crm:E29_Design_or_Procedure`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "Design or Procedure"@en
  - ➕ skos:definition: "Scope note:
This class comprises documented plans for the execution of actions in order to achieve a result of a specific quality, form, or contents. In particular, it comprises plans for deliberate human activities that may result in new instances of E71 Human-Made Thing or for shaping or guiding the execution of an instance of E7 Activity.
Instances of E29 Design or Procedure can be structured in parts and sequences or depend on others.
This is modelled using P69 has association with (is associated with): E29 Design or Procedure.
Designs or procedures can be seen as one of the following:
1. A schema for the activities it describes
2. A schema of the products that result from their application
3. An independent intellectual product that may have never been applied, such as Leonardo da Vinci’s famous plans for flying machines
Because designs or procedures may never be applied or only partially executed, the CIDOC CRM models a loose relationship between the plan and the respective product.

Examples:
- the ISO standardisation procedure
- the musical notation for Beethoven’s “Ode to Joy” (Kershaw, 1999)
- the architectural drawings for the Kölner Dom (Cologne Cathedral) in Cologne, Germany (Wolff, 1999)
- the drawing found on Folio 860 of the Codex Atlanticus from Leonardo da Vinci, 1486 to 1490, kept in the Biblioteca Ambrosiana in Milan

In First Order Logic:
- E29(x) ⇒ E73(x)"@en
  - ➖ rdfs:label: "Technique"@en
  - ➖ rdfs:subClassOf: prov:Entity
  - ➖ skos:definition: "Method or craft process used in production or ritual"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Destroyed** (`https://cair-nepal.org/heritagegraph/ExistenceStatus#Destroyed`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Known to have been destroyed; no physical remains."@en
  - ➖ skos:definition: "Known to have been destroyed; no physical remains"@en
- **Destruction** (`crm:E6_Destruction`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "Destruction"@en
  - ➕ skos:definition: "Scope note:
This class comprises events that destroy one or more instances of E18 Physical Thing, such that they lose their identity as the subjects of documentation.
Some destruction events are intentional, while others are independent of human activity. Intentional destruction can be documented by classifying the event as both an instance of E6 Destruction and of E7 Activity. 
The decision to document an object as destroyed, transformed, or modified is context-sensitive: 
1. If the matter remaining from the destruction is not documented, the event is modelled solely as an instance of E6 Destruction. 
2. An event should also be documented using E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the original. In this case, the new items have separate identities. Matter is preserved, but identity is not.
3. When the initial identity of the changed instance of E18 Physical Thing is preserved, the event should be documented as an instance of E11 Modification.

Examples:
- the destruction of Herculaneum by volcanic eruption in 79 AD (Camardo, 2013)
- the destruction of Nineveh (E6, E7) (River, 2016) 
- the breaking of a champagne glass yesterday by my dog (fictitious)

In First Order Logic:
- E6(x) ⇒ E64(x)"@en
  - ➖ rdfs:label: "Destruction Event"@en
  - ➖ skos:definition: "Event that destroyed or damaged a structure."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Dharmashala** (`heritageGraph:Dharmashala`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Pilgrim lodge operated by a Guthi organization."@en
  - ➖ skos:definition: "Pilgrim lodge operated by a Guthi organization"@en
- **Dhunge Dhara** (`heritageGraph:DhungeDhara`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Stone spout (hiti) with carved imagery, used for ritual bathing and daily water supply."@en
  - ➖ skos:definition: "Stone spout (hiti) with carved imagery, used for ritual bathing and daily water supply"@en
- **Documentation Activity** (`heritageGraph:DocumentationActivity`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E7_Activity
  - ➕ rdfs:subClassOf: heritageGraph:usedEquipment only rdf:PlainLiteral
  - ➕ rdfs:subClassOf: heritageGraph:usedMethod only rdf:PlainLiteral
  - ➕ skos:editorialNote: "PROV-O alignment note: prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: crm:P4_has_time-span min 0
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: heritageGraph:documents min 0
  - ➖ rdfs:subClassOf: heritageGraph:usedEquipment min 0
  - ➖ rdfs:subClassOf: heritageGraph:usedEquipment only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:usedMethod max 1
  - ➖ rdfs:subClassOf: heritageGraph:usedMethod min 0
  - ➖ rdfs:subClassOf: heritageGraph:usedMethod only xsd:string
  - ➖ rdfs:subClassOf: prov:generated min 0
  - ➖ rdfs:subClassOf: prov:generated only prov:Entity
  - ➖ rdfs:subClassOf: prov:wasAssociatedWith min 0
  - ➖ rdfs:subClassOf: prov:wasAssociatedWith only prov:Agent
  - ➖ skos:broadMatch: crm:E7_Activity
- **Documented in source** (`heritageGraph:mentionedInSource`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:ArchitecturalStructure
  - ➕ schema1:domainIncludes: heritageGraph:SyncreticRelationship
  - ➕ skos:definition: "Source(s) that mention/document this entity: the normative way to cite a source for a description of a heritage thing, event, actor or relationship. Distinct from prov:wasDerivedFrom, which is used only on assertions (I2 Belief) with prov:wasAttributedTo for the claimant. A source's own bibliographic data uses hg:sourceCitation, hg:sourceCreator, hg:sourceUrl and hg:persistentIdentifier. Entity-mention is not logical derivation."@en
  - ➕ skos:editorialNote: "PROV-O alignment: prov:wasInfluencedBy"@en
  - ➖ heritageGraph:prov_alignment: "prov:wasInfluencedBy"
  - ➖ skos:definition: "Source(s) that mention/document this entity. Distinct from was_derived_from (which is prov:wasDerivedFrom for assertions). Entity-mention is not logical derivation."@en
- **Dome style** (`https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Dome`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Dome-based style (Mughal/Neo-classical influence)."@en
  - ➖ skos:definition: "Dome-based style (Mughal/Neo-classical influence)"@en
- **Embodied deity** (`heritageGraph:embodiedDeity`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariTenure
  - ➕ skos:definition: "Deity role embodied by participant."@en
  - ➖ skos:definition: "Deity role embodied by participant"@en
- **end of the end** (`crm:P82b_end_of_the_end`, datatype property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "end of the end"@en
  - ➖ rdfs:label: "Date latest"@en
  - ➖ skos:definition: "Latest possible date (for uncertain dates)"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **End place** (`heritageGraph:endPlace`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "Ending location of movement ritual."@en
  - ➕ skos:relatedMatch: crm:P26_moved_to
  - ➖ skos:definition: "Ending location of movement ritual"@en
- **Ended tenure of** (`heritageGraph:endedTenureOf`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariRetirementEvent
- **endedAtTime** (`prov:endedAtTime`, datatype property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "endedAtTime"
  - ➕ skos:definition: "The time at which an activity ended. See also prov:startedAtTime."@en
  - ➖ rdfs:label: "Ended at time"@en
  - ➖ skos:definition: "Time at which this activity ended."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **ends before the start of** (`crm:P183_ends_before_the_start_of`, object property)
  - ➕ owl:inverseOf: crm:P183i_starts_after_the_end_of
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "ends before the start of"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity ends definitely before the start of the temporal extent of the range instance B of E2 Temporal Entity. 
In other words, if A = [A(start), A(end)] and B = [B(start), B(end)], it means A(end) &lt; B(start) is true. 
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to the following Allen temporal relation (Allen, 1983) : {before}.
This property is transitive. This property is asymmetric. 


https://cidoc-crm.org/html/version_images/images_7.1.3/image_11.png


Figure 18: Temporal entity A ends before the start of temporal entity B. Here A is longer than B


https://cidoc-crm.org/html/version_images/images_7.1.3/image_12.png


Figure 19: Temporal entity A ends before the start of temporal entity B. Here A is shorter than B

Examples:
- Gisle taking office as Bishop of Linköping 1139 AD (E7) ends before the start of The Guta saga composition (E65). (Peel, 1999)
- Troy VII (E4) ends before the start of Troy VIII (E4). [uninhabited for some 200 years]
- The use of the Tomb Four from Nikitopoulou group in Nihoria in the MHIII-LHI period (E4) ends before the start of the period of reuse of the Tomb Four from Nikitopoulou group in LHIIIA (E4). [“Of the six tombs excavated in the Nikitopoulou group […] the finds in Tomb Four are of MH II or MH III-LH I date, with the exception of the finds with the Northern group of material, which is uniformly dated to LHIIA2, end the ewer in the middle of the floor, dated LHIIIA1. […] The preserved evidence seems clearly to indicate use in the MHIII-LHI use in the MHIII-LHI period followed by a period of reuse in LHIIIA, a pattern matched at architecturally similar sites such as 13:Kaminia and 10:Gouvalári.”] (Boyd, 2002)

In First Order Logic:
- P183(x,y) ⇒ E2(x)
- P183(x,y) ⇒ E2(y)
- P183(x,y) ⇒ P182(x,y)
- [P183(x,y) ∧ P183(y,z)] ⇒ P183(x,z)
- P183(x,y) ⇒ ¬P183(y,x)"@en
  - ➖ rdfs:label: "Occurs before"@en
  - ➖ skos:definition: "Points to the next ritual in the canonical sequence."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Enshrined deity** (`heritageGraph:enshrinedDeity`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Enshrinement
  - ➕ skos:definition: "Deity installed through enshrinement."@en
  - ➖ skos:definition: "Deity installed through enshrinement"@en
- **Enshrined in structure** (`heritageGraph:enshrinedInStructure`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Enshrinement
  - ➕ skos:definition: "Temple where deity was enshrined."@en
  - ➖ skos:definition: "Temple where deity was enshrined"@en
- **Enshrinement** (`heritageGraph:Enshrinement`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E7_Activity
  - ➕ rdfs:subClassOf: heritageGraph:RitualEvent
  - ➕ skos:definition: "Event of installing a deity's murti or symbol within a temple sanctum."@en
  - ➕ skos:editorialNote: "PROV-O alignment note: prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by min 0
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by only crm:E39_Actor
  - ➖ rdfs:subClassOf: crm:P4_has_time-span min 0
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: crm:P7_took_place_at max 1
  - ➖ rdfs:subClassOf: crm:P7_took_place_at min 0
  - ➖ rdfs:subClassOf: crm:P7_took_place_at only crm:E53_Place
  - ➖ rdfs:subClassOf: heritageGraph:enshrinedDeity min 0
  - ➖ rdfs:subClassOf: heritageGraph:enshrinedInStructure min 0
  - ➖ skos:broadMatch: crm:E7_Activity
  - ➖ skos:definition: "Event of installing a deity's murti or symbol within a temple sanctum"@en
- **Enshrines deity through event** (`heritageGraph:enshrinesDeityThroughEvent`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Temple
  - ➕ skos:definition: "Enshrinement event that installed deity in temple."@en
  - ➖ skos:definition: "Enshrinement event that installed deity in temple"@en
- **Enthroned person** (`heritageGraph:enthronedPerson`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariEnthronementEvent
- **Enthroned through** (`heritageGraph:enthronedThrough`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subPropertyOf: heritageGraph:tenureOpenedBy
  - ➕ schema1:domainIncludes: heritageGraph:KumariTenure
- **Entity** (`prov:Entity`, class)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "Entity"
  - ➕ skos:definition: "An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary."@en
  - ➖ heritageGraph:provenance_scope: "record"
  - ➖ rdfs:label: "Entity"@en
  - ➖ skos:definition: "Direct LinkML representation of prov:Entity. Applied to physical, digital, conceptual, and assertion-bearing things that participate in provenance relations. PROVENANCE SCOPE (design decision): for classes whose instances are real-world referents (structures, deities, places, actors), the provenance slots (was_derived_from, was_attributed_to, was_generated_by, generated_at_time) describe the DATA RECORD about the referent, not the referent itself -- a stupa is not generated by the survey that records it. Referent-level history is modelled through events (Production, DestructionEvent, etc.). RDF deployments SHOULD carry record-level provenance in named graphs or on InformationObject/Assertion nodes."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Epoch date gregorian** (`heritageGraph:epochDateGregorian`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:CalendarSystem
  - ➕ skos:definition: "Proleptic Gregorian (ISO 8601, astronomical year numbering) date on which the era began, in the era's own reckoning (Bikram Sambat counts from year 1, e.g. -0056-04-14, a nominal back-projection of the modern solar reckoning rather than an attested date; Nepal Sambat counts elapsed years from year 0, 0879-10-24 = 20 October 879 Julian). Its month and day only indicate the approximate new-year season: the actual new year varies (Bikram Sambat 13-15 April, solar; Nepal Sambat late October to November, lunisolar), so it must not be used for day-level conversion. A value ending in -01-01 marks a calendar whose new year is 1 January, for which year conversion is exact."@en
  - ➖ skos:definition: "The start date of this calendar era in Gregorian ISO format."@en
- **Equivalence** (`https://cair-nepal.org/heritagegraph/SyncreticType#Equivalence`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Claimed identity: the two are held to be one deity in different traditions (e.g. Avalokiteshvara and Matsyendranath for Newar Buddhists)."@en
  - ➖ skos:definition: "Same deity in different traditions (e.g., Avalokiteshvara = Matsyendranath)"@en
- **Exact** (`https://cair-nepal.org/heritagegraph/DatePrecision#Exact`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Precise date known."@en
  - ➖ skos:definition: "Precise date known"@en
- **Existence Status** (`heritageGraph:ExistenceStatus`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E55_Type
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ExistenceStatus#Destroyed
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ExistenceStatus#Extant
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ExistenceStatus#Hypothetical
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ExistenceStatus#Lost
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ExistenceStatus#PartiallyExtant
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/ExistenceStatus#Unknown
- **Expertise area** (`heritageGraph:expertiseArea`, datatype property)
  - ➕ rdfs:domain: crm:E21_Person
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ skos:definition: "Areas of expertise (e.g., Licchavi inscriptions, Sanskrit epigraphy, Newari archaeology)."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Areas of expertise (e.g., Lichhavi inscriptions, Sanskrit epigraphy, Newari archaeology)"@en
- **Extant** (`https://cair-nepal.org/heritagegraph/ExistenceStatus#Extant`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Currently exists in physical form."@en
  - ➖ skos:definition: "Currently exists in physical form"@en
- **Fearlessness Assessment** (`heritageGraph:FearlessnessAssessment`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "The 'fearlessness test' popularly described (animal heads, masked dancers in darkness). Its historical and contemporary practice is DISPUTED -- some former Kumaris contest how it is described. Represented as an assessment whose accounts are source-attributed via hg:hasAssertion, NOT as a mandatory criterion."@en
  - ➖ skos:definition: "The 'fearlessness test' popularly described (animal heads, masked dancers in darkness). Its historical and contemporary practice is DISPUTED -- some former Kumaris contest how it is described. Represented as an assessment whose accounts are source-attributed via has_assertion, NOT as a mandatory criterion."@en
- **Festival** (`heritageGraph:Festival`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Large-scale community ritual event (Jatra) involving processions, music, and collective participation."@en
  - ➕ skos:editorialNote: "PROV-O alignment note: prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: crm:P9_consists_of min 0
  - ➖ rdfs:subClassOf: crm:P9_consists_of only heritageGraph:RitualEvent
  - ➖ skos:definition: "Large-scale community ritual event (Jatra) involving processions, music, and collective participation"@en
- **Field Survey Activity** (`heritageGraph:FieldSurveyActivity`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **Field Survey Dataset** (`heritageGraph:FieldSurveyDataset`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **forms part of** (`crm:P46i_forms_part_of`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "forms part of"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many (0,n:0,n)

Scope note of the inverse property:
This property associates an instance of E18 Physical Thing with another instance of Physical Thing that forms part of it. The spatial extent of the composing part is included in the spatial extent of the whole.
Component elements, since they are themselves instances of E18 Physical Thing, may be further analysed into sub-components, thereby creating a hierarchy of part decomposition. An instance of E18 Physical Thing may be shared between multiple wholes, for example two buildings may share a common wall. This property does not specify when and for how long a component element resided in the respective whole. If a component is not part of a whole from the beginning of existence or until the end of existence of the whole, the classes E79 Part Addition and E90 Part Removal can be used to document when a component became part of a particular whole and/or when it stopped being a part of it. For the time-span of being part of the respective whole, the component is completely contained in the place the whole occupies.
This property is intended to describe specific components that are individually documented, rather than general aspects. Overall descriptions of the structure of an instance of E18 Physical Thing are captured by the P3 has note property.
The instances of E57 Material of which an instance of E18 Physical Thing is composed should be documented using P45 consists of (is incorporated in).
This property is transitive and asymmetric.

Examples of the inverse property:
- The Royal carriage (E22) forms part of the Royal train (E22).
- The “Hog’s Back” (E24) forms part of the “Fosseway” (E24).

In First Order Logic of the inverse property:
- P46(x,y) ⇒ E18(x)
- P46(x,y) ⇒ E18(y)
- P46(x,y) ⇒ P132(x,y)
- [P46(x,y) ∧ P46(y,z)] ⇒ P46(x,z)
- P46(x,y) ⇒ (∃uzw)[E93(u) ∧ P195i (x,u) ∧ E52(z) ∧ P164(u,z) ∧ E93(w) ∧ P195i (w,y) ∧ P164(w,z) ∧ P10(w,u)] 
- P46(x,y) ⇒ ¬P46(y,x)"@en
  - ➖ rdfs:label: "Is component of"@en
  - ➖ skos:definition: "Larger structure that this element is part of"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **forms part of** (`crm:P9i_forms_part_of`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "forms part of"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many (0,n:0,n)

Scope note of the inverse property:
This property associates an instance of E4 Period with another instance of E4 Period that is defined by a subset of the phenomena that define the former. Therefore, the spacetime volume of the latter must fall within the spacetime volume of the former.
This property is transitive and asymmetric.

Examples of the inverse property:
- Cretan Bronze Age (E4) consists of Middle Minoan (E4). (Hood, 1971)

In First Order Logic of the inverse property:
- P9(x,y) ⇒ E4(x)
- P9(x,y) ⇒ E4(y)
- P9(x,y) ⇒ P10(y,x)
- [P9(x,y) ∧ P9(y,z)] ⇒ P9(x,z)
- P9(x,y) ⇒ ¬P9(y,x)"@en
  - ➖ rdfs:label: "Is part of festival"@en
  - ➖ skos:definition: "Larger festival this ritual is part of"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Fusion** (`https://cair-nepal.org/heritagegraph/SyncreticType#Fusion`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Claimed combination: the deity is held to combine features of deities of several traditions."@en
  - ➖ skos:definition: "Intrinsically syncretic deity merging multiple traditions"@en
- **generated** (`prov:generated`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "generated"
  - ➖ rdfs:label: "generated"@en
  - ➖ skos:definition: "Entity generated by this activity."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **generatedAtTime** (`prov:generatedAtTime`, datatype property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "generatedAtTime"
  - ➕ skos:definition: "The time at which an entity was completely created and is available for use."@en
  - ➖ rdfs:label: "Generated at time"@en
  - ➖ skos:definition: "Time at which this entity was generated (ISO 8601)."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Good** (`https://cair-nepal.org/heritagegraph/ConditionType#Good`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "No significant damage."@en
  - ➖ skos:definition: "No significant damage"@en
- **Guthi** (`heritageGraph:Guthi`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E74_Group
  - ➕ skos:definition: "Endowed trust organization unique to Nepal, managing temples, rituals, and land through hereditary or voluntary membership."@en
  - ➖ rdfs:subClassOf: crm:E39_Actor
  - ➖ rdfs:subClassOf: crm:P107_has_current_or_former_member min 0
  - ➖ rdfs:subClassOf: crm:P107_has_current_or_former_member only crm:E21_Person
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: crm:P50i_is_current_keeper_of min 0
  - ➖ rdfs:subClassOf: crm:P50i_is_current_keeper_of only heritageGraph:ArchitecturalStructure
  - ➖ rdfs:subClassOf: heritageGraph:guthiType min 0
  - ➖ rdfs:subClassOf: heritageGraph:performsRitual min 0
  - ➖ skos:broadMatch: crm:E74_Group
  - ➖ skos:definition: "Endowed trust organization unique to Nepal, managing temples, rituals, and land through hereditary or voluntary membership"@en
- **Guthi Type** (`heritageGraph:GuthiType`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E55_Type
  - ➕ skos:definition: "Controlled vocabulary of Guthi functional types (CRM E55_Type)."@en
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/GuthiType#JatraGuthi
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/GuthiType#NashaGuthi
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/GuthiType#PujaGuthi
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/GuthiType#RajGuthi
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/GuthiType#SanGuthi
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/GuthiType#SanaGuthi
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/GuthiType#SiGuthi
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/GuthiType#TempleGuthi
  - ➖ skos:definition: "Controlled vocabulary of Guthi functional types (CRM E55_Type)"@en
- **Guthi Type (concept scheme)** (`https://cair-nepal.org/heritagegraph/scheme/GuthiType`, concept scheme)
  - ➕ skos:definition: "Controlled vocabulary of Guthi functional types (CRM E55_Type)."@en
  - ➖ skos:definition: "Controlled vocabulary of Guthi functional types (CRM E55_Type)"@en
- **Had participant** (`heritageGraph:hadParticipant`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariTenure
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:closeMatch: crm:P11_had_participant
  - ➕ skos:definition: "Actor(s) participating in this period, situation or ritual without carrying it out (e.g. the Kumari in a chariot procession). The holder of a tenure is given with hg:tenureHolder."@en
  - ➖ skos:definition: "Actor(s) participating in this period, situation or ritual without carrying it out (e.g. the girl holding a Kumari tenure, or the Kumari in a chariot procession)."@en
- **Has architectural style** (`heritageGraph:hasArchitecturalStyle`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:ArchitecturalStructure
  - ➕ skos:definition: "Architectural style classification."@en
  - ➖ skos:definition: "Architectural style classification"@en
- **Has assertion** (`heritageGraph:hasAssertion`, object property)
  - ➕ rdfs:domain: heritageGraph:AssertionSubject
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **has calendar system** (`heritageGraph:calendarSystem`, object property)
  - ➕ rdfs:domain: crm:E52_Time-Span
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Calendar system used for date representation."@en
  - ➖ skos:definition: "Calendar system used for date representation"@en
- **Has condition type** (`heritageGraph:hasConditionType`, object property)
  - ➕ rdfs:domain: crm:E3_Condition_State
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Categorization of the condition state."@en
  - ➖ skos:definition: "Categorization of the condition state"@en
- **Has criterion** (`heritageGraph:hasCriterion`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariSelectionEvent
- **has current location** (`crm:P55_has_current_location`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "has current location"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property records the location of an instance of E19 Physical Object at the time of validity of the record or database containing the statement that uses this property.
This property is a specialisation of P53 has former or current location (is former or current location of). It indicates that the instance of E53 Place associated with the instance of E19 Physical Object is the current location of the object. The property does not allow any indication of how long the object has been at the current location. 
This property is a shortcut. A more detailed representation can make use of the fully developed (i.e., indirect) path from E19 Physical Object, through, P25i moved by, E9 Move, P26 moved to to E53 Place if and only if this Move is the most recent.

Examples:
- Silver cup 232 (E22) has current location Display Cabinet 23, Room 4, British Museum (E53). (fictitious)

In First Order Logic:
- P55(x,y) ⇒ E19(x)
- P55(x,y) ⇒ E53(y) 
- P55(x,y) ⇒ P53(x,y)
- P55(x,y) ⇐ (∃z) [ [E9(z) ˄ P25i(x,z) ˄ P26(z,y)]
- ˄ ¬​ (∃w) [E9(w) ˄ P25i(x,w) ˄ P27(w,y)˄ P182(z,w)]]​"@en
  - ➖ rdfs:label: "Has current location"@en
  - ➖ skos:definition: "Current location of object or structure"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **has current or former member** (`crm:P107_has_current_or_former_member`, object property)
  - ➕ owl:inverseOf: crm:P107i_is_current_or_former_member_of
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "has current or former member"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property associates an instance of E74 Group with an instance of E39 Actor that is or has been a member thereof.
Instances of E74 Group and E21 Person may all be members of instances of E74 Group. An instance of E74 Group may be founded initially without any member. 
This property is a shortcut of the more fully developed path from E74 Group, P144i gained member by, E85 Joining, P143 joined to E39 Actor.
The property P107.1 kind of member can be used to specify the type of membership or the role the member has in the group.

Examples:
- László Moholy-Nagy (E21) is current or former member of Bauhaus (E74). (Moholy-Nagy, 2012)
- National Museum of Science and Industry (E74) has current or former member The National Railway Museum (E74). (Rolt, 1971)
- The married couple Queen Elisabeth and Prince Phillip (E74) has current or former member Prince Phillip (E21) kind of member husband (E55). (Brandreth, 2004)

Properties:
- P107.1 kind of member: E55 Type

In First Order Logic:
- P107(x,y) ⇒ E74(x)
- P107(x,y) ⇒ E39(y)
- P107(x,y,z) ⇒ [P107(x,y) ∧ E55(z)]
- P107(x,y) ⇐ (∃z) [E85(z) ˄ P144i(x,z) ˄ P143(z,y)]"@en
  - ➖ rdfs:label: "Has membership"@en
  - ➖ skos:definition: "Members of Guthi organization"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **has date precision** (`heritageGraph:datePrecision`, object property)
  - ➕ rdfs:domain: crm:E52_Time-Span
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **has destruction event** (`heritageGraph:destructionEvent`, object property)
  - ➕ owl:inverseOf: crm:P13_destroyed
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:ArchitecturalStructure
  - ➕ skos:definition: "Event that destroyed this structure (if known)."@en
  - ➖ skos:definition: "Event that destroyed this structure (if known)"@en
- **has existence status** (`heritageGraph:existenceStatus`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:ArchitecturalStructure
  - ➕ skos:definition: "Current physical status of the structure."@en
  - ➖ skos:definition: "Current physical status of the structure"@en
- **has guthi type** (`heritageGraph:guthiType`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Guthi
  - ➕ skos:definition: "Type of Guthi (Si, Jatra, Temple)."@en
  - ➖ skos:definition: "Type of Guthi (Si, Jatra, Temple)"@en
- **has identified** (`crm:P35_has_identified`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "has identified"@en
  - ➕ skos:definition: "Quantification: many to many, necessary (1,n:0,n)

Scope note:
This property identifies the instance of E3 Condition State that was observed in an instance of E14 Condition Assessment activity.

Examples:
- The condition assessment of silver cup 232 in 1997 (E14) has identified oxidation traces were present in 1997 (E3). [which has type (P2) with oxidation traces (E55)] (fictitious)
- The condition assessment of the cover of MS Sinai Greek 418 (E13) has identified the condition state in November 2003 (E3). [which has type fine (E55)] (Honey and Pickwoad, 2010)
- The condition assessment of the endband cores of MS Sinai Greek 418 (E14) has identified the condition state in November 2003 (E3). [which has type broken (E55)] (Honey and Pickwoad, 2010)

In First Order Logic:
- P35(x,y) ⇒E14(x)
- P35(x,y) ⇒ E3(y)
- P35(x,y) ⇒ P141(x,y)"@en
  - ➖ rdfs:label: "Assessed condition state"@en
  - ➖ skos:definition: "Condition state identified by the assessment"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **has note** (`crm:P3_has_note`, datatype property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "has note"@en
  - ➕ skos:definition: "Quantification: one to many (0,n:0,1)

Scope note:
This property is a container for all informal descriptions about an object that have not been expressed in terms of CIDOC CRM constructs. 
In particular, it captures the characterisation of the item itself, its internal structures, appearance, etc.
Like property P2 has type (is type of), this property is a consequence of the restricted focus of the CIDOC CRM. The aim is not to capture, in a structured form, everything that can be said about an item; indeed, the CIDOC CRM formalism is not regarded as sufficient to express everything that can be said. Good practice requires use of distinct note fields for different aspects of a characterisation. The P3.1 has type property of P3 has note allows differentiation of specific notes, e.g. “construction”, “decoration”, etc. 
An item may have many notes, but a note is attached to a specific item.

Examples:
- Coffee mug – OXCMS:1983.1.1 (E19) has note “chipped at edge of handle” (E62) has type Condition (E55). (fictitious)

Properties:
- P3.1 has type: E55 Type

In First Order Logic:
- P3(x,y) ⇒ E1(x)
- P3(x,y) ⇒ E62(y) 
- P3(x,y,z) ⇒ [P3(x,y) ∧ E55(z)]"@en
  - ➖ rdfs:label: "note"@en
  - ➖ skos:definition: "Free-text note (description, reason, verification notes)"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **has produced** (`crm:P108_has_produced`, object property)
  - ➕ owl:inverseOf: crm:P108i_was_produced_by
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "has produced"@en
  - ➕ skos:definition: "Quantification: one to many, necessary, dependent (1,n:1,1)

Scope note:
This property identifies the instance of E24 Physical Human-Made Thing that came into existence as a result of the instance of E12 Production.
The identity of an instance of E24 Physical Human-Made Thing is not defined by its matter, but by its existence as a subject of documentation. An E12 Production can result in the creation of multiple instances of E24 Physical Human-Made Thing.

Examples:
- The building of Rome (E12) has produced the Colosseum (E24). (Hopkins &amp; Beard, 2011)

In First Order Logic:
- P108(x,y) ⇒ E12(x)
- P108(x,y) ⇒ E24(y)
- P108(x,y) ⇒ P31(x,y)
- P108(x,y) ⇒ P92(x,y)"@en
  - ➖ rdfs:label: "Produced object"@en
  - ➖ skos:definition: "Object produced by this production event"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Has religious tradition** (`heritageGraph:hasReligiousTradition`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:ArchitecturalStructure
  - ➕ schema1:domainIncludes: heritageGraph:Deity
  - ➕ skos:definition: "Religious tradition(s) within which this deity is venerated, or which use this structure (a temple, or a pavilion, rest house or water spout with a shrine)."@en
  - ➖ skos:definition: "Religious tradition(s) within which this deity is venerated, or which use this religious structure"@en
- **has ritual type** (`heritageGraph:ritualType`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "Classification of ritual (puja, jatra, consecration)."@en
  - ➖ skos:definition: "Classification of ritual (puja, jatra, consecration)"@en
- **has syncretic type** (`heritageGraph:syncreticType`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:SyncreticRelationship
- **has time-span** (`crm:P4_has_time-span`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "has time-span"@en
  - ➕ skos:definition: "Quantification: many to one, necessary (1,1:0,n)

Scope note:
This property associates an instance of E2 Temporal Entity with the instance of E52 Time-Span during which it was on-going. The associated instance of E52 Time-Span is understood as the real time-span during which the phenomena making up the temporal entity instance were active. More than one instance of E2 Temporal Entity may share a common instance of E52 Time-Span only if they come into being and end being due to identical declarations or events.

Examples:
- The Yalta Conference (E7) has time-span Yalta Conference time-span (E52). (Harbutt, 2010)

In First Order Logic:
- P4(x,y) ⇒ E2(x)
- P4(x,y) ⇒ E52(y)"@en
  - ➖ rdfs:label: "Has timespan"@en
  - ➖ skos:definition: "Links event to its temporal extent"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **has type** (`crm:P2_has_type`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "has type"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property allows sub-typing of CIDOC CRM entities –a form of specialisation – through the use of a terminological hierarchy, or thesaurus. 
The CIDOC CRM is intended to focus on the high-level entities and relationships needed to describe data structures. Consequently, it does not specialise entities any further than is required for this immediate purpose. However, entities in the isA hierarchy of the CIDOC CRM may by specialised into any number of sub-entities, which can be defined in the E55 Type hierarchy. E41 Appellation, for example, may be specialised into “e-mail address”, “telephone number”, “post office box”, “URL”, etc., none of which figures explicitly in the CIDOC CRM class hierarchy. A comprehensive explanation about refining CIDOC CRM concepts by E55 Type is given in the section “About Types” in the section on “Specific Modelling Constructs” of this document.
This property is a shortcut for the path from E1 CRM Entity through P41i was classified by, E17 Type Assignment, P42 assigned to E55 Type.

Examples:
- “enquiries@cidoc-crm.org” (E41) has type e-mail address (E55). (fictitious)

In First Order Logic:
- P2(x,y) ⇒ E1(x)
- P2(x,y) ⇒ E55(y)
- P2(x,y) ⇐ (∃z) [E17(z)] ˄ P41i(x,z) ˄ P42(z,y)]"@en
  - ➖ rdfs:label: "Has type"@en
  - ➖ skos:definition: "Generic CRM typing property (P2 has type). Canonical holder of the CRM predicate; use the specific typing slots below in data."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Heritage information object** (`heritageGraph:InformationObject`, class)
  - ➕ dcterms:title: "Heritage information object"@en
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "Heritage information object"@en
  - ➕ skos:definition: "A recorded piece of information about heritage."@en
  - ➖ rdfs:label: "Information Object"@en
  - ➖ rdfs:subClassOf: crm:P129_is_about min 0
  - ➖ rdfs:subClassOf: crm:P129_is_about only heritageGraph:AssertionSubject
  - ➖ rdfs:subClassOf: heritageGraph:documentedBy min 0
  - ➖ rdfs:subClassOf: prov:wasGeneratedBy max 1
  - ➖ rdfs:subClassOf: prov:wasGeneratedBy min 0
  - ➖ rdfs:subClassOf: prov:wasGeneratedBy only prov:Activity
  - ➖ rdfs:subClassOf: schema1:inLanguage max 1
  - ➖ rdfs:subClassOf: schema1:inLanguage min 0
  - ➖ rdfs:subClassOf: schema1:inLanguage only xsd:string
  - ➖ skos:definition: "A recorded piece of information about heritage"@en
- **Historical** (`https://cair-nepal.org/heritagegraph/SyncreticType#Historical`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Claimed historical derivation: the deity is held to have developed from the other over time."@en
  - ➖ skos:definition: "Gradual syncretism over time"@en
- **Historical Event** (`heritageGraph:HistoricalEvent`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E5_Event
  - ➕ skos:editorialNote: "PROV-O alignment note: prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: crm:P4_has_time-span min 0
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: crm:P7_took_place_at max 1
  - ➖ rdfs:subClassOf: crm:P7_took_place_at min 0
  - ➖ rdfs:subClassOf: crm:P7_took_place_at only crm:E53_Place
  - ➖ rdfs:subClassOf: crm:P9_consists_of min 0
  - ➖ rdfs:subClassOf: crm:P9_consists_of only heritageGraph:RitualEvent
  - ➖ rdfs:subClassOf: heritageGraph:architecturalStructures min 0
  - ➖ skos:broadMatch: crm:E5_Event
- **Homa** (`https://cair-nepal.org/heritagegraph/RitualType#Homa`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Fire offering ritual."@en
  - ➖ skos:definition: "Fire offering ritual"@en
- **Horoscope Compatibility Criterion** (`heritageGraph:HoroscopeCompatibilityCriterion`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **Human-Made Object** (`crm:E22_Human-Made_Object`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "Human-Made Object"@en
  - ➕ skos:definition: "Scope note:
This class comprises all persistent physical objects of any size that are purposely created by human activity and have physical boundaries that separate them completely in an objective way from other objects. 
The class also includes all aggregates of objects made for functional purposes of whatever kind, independent of physical coherence, such as a set of chessmen.

Examples:
- the Rosetta Stone (E22)
- LNER Class A4 4468 Mallard [the World’s fastest steam locomotive, preserved at the National Railway Museum of York, UK] (Solomon, 2003)
- the Portland Vase (Walker, 2004)

In First Order Logic:
- E22(x) ⇒ E19(x)
- E22(x) ⇒ E24(x)"@en
  - ➖ rdfs:label: "Human Made Object"@en
  - ➖ rdfs:subClassOf: prov:Entity
  - ➖ skos:definition: "Physical objects created by human activity"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Hypothesized location** (`heritageGraph:hypothesizedLocation`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:ArchitecturalStructure
  - ➕ skos:definition: "Possible locations if the structure is lost."@en
  - ➖ skos:definition: "Possible locations if the structure is lost"@en
- **Hypothetical** (`https://cair-nepal.org/heritagegraph/ExistenceStatus#Hypothetical`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Theorized (e.g. a reconstruction on paper only); never physically realized."@en
  - ➖ skos:definition: "Reconstructed or theorized; never physically realized"@en
- **Iconographic Object** (`heritageGraph:IconographicObject`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Sacred visual art objects that depict or embody deities through iconographic conventions."@en
  - ➕ skos:relatedMatch: crm:E36_Visual_Item
  - ➖ rdfs:subClassOf: crm:P108i_was_produced_by min 0
  - ➖ rdfs:subClassOf: crm:P108i_was_produced_by only crm:E12_Production
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: crm:P55_has_current_location max 1
  - ➖ rdfs:subClassOf: crm:P55_has_current_location min 0
  - ➖ rdfs:subClassOf: crm:P55_has_current_location only crm:E53_Place
  - ➖ rdfs:subClassOf: crm:P62_depicts min 0
  - ➖ rdfs:subClassOf: crm:P62_depicts only heritageGraph:Deity
  - ➖ rdfs:subClassOf: heritageGraph:participatesInRitual min 0
  - ➖ rdfs:subClassOf: heritageGraph:usedBy min 0
  - ➖ skos:broadMatch: crm:E22_Human-Made_Object
  - ➖ skos:closeMatch: crm:E36_Visual_Item
  - ➖ skos:definition: "Sacred visual art objects that depict or embody deities through iconographic conventions"@en
- **Identifier** (`dcterms:identifier`, datatype property)
  - ➕ rdfs:isDefinedBy: http://purl.org/dc/terms/
  - ➕ rdfs:label: "Identifier"@en
  - ➕ skos:definition: "An unambiguous reference to the resource within a given context."@en
  - ➖ rdfs:label: "ID"@en
  - ➖ skos:definition: "Globally unique URI identifier"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Initiated tenure** (`heritageGraph:initiatedTenure`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariSelectionEvent
  - ➕ skos:definition: "Kumari tenure that was initiated by this selection event."@en
  - ➖ skos:definition: "Kumari tenure that was initiated by this selection event"@en
- **inLanguage** (`schema1:inLanguage`, datatype property)
  - ➕ rdfs:isDefinedBy: http://schema.org/
  - ➕ rdfs:label: "inLanguage"
  - ➕ skos:definition: "The language of the content or performance or used in an action. Please use one of the language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also [[availableLanguage]]."
  - ➖ rdfs:label: "Source language"@en
  - ➖ skos:definition: "Language of the source material"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Installation Ritual** (`https://cair-nepal.org/heritagegraph/RitualType#InstallationRitual`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Installation/enshrinement ritual."@en
  - ➖ skos:definition: "Installation/enshrinement ritual"@en
- **Institutional affiliation** (`heritageGraph:institutionalAffiliation`, datatype property)
  - ➕ rdfs:domain: crm:E21_Person
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ skos:definition: "Institutional affiliation (e.g., Tribhuvan University, Nepal Heritage Society)."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Institutional affiliation (e.g., Tribhuvan University, Nepal Heritage Society)"@en
- **Invokes deity** (`heritageGraph:invokesDeity`, object property)
  - ➕ owl:inverseOf: heritageGraph:isInvokedInRitual
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "Deity invoked or made present through ritual."@en
  - ➖ skos:definition: "Deity invoked or made present through ritual"@en
- **is about** (`crm:P129_is_about`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "is about"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property documents that an instance of E89 Propositional Object has as subject an instance of E1 CRM Entity. 
This differs from P67 refers to (is referred to by), which refers to an instance of E1 CRM Entity, in that it describes the primary subject or subjects of an instance of E89 Propositional Object.

Examples:
- The text entitled ‘Reach for the sky’ (E33) is about Douglas Bader (E21). (Brickhill, 2001)

In First Order Logic:
- P129(x,y) ⇒ E89(x)
- P129(x,y) ⇒ E1(y) 
- P129(x,y) ⇒ P67(x,y)"@en
  - ➖ rdfs:label: "Is about"@en
  - ➖ skos:definition: "Heritage entity or event described by this information object."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Is about deity** (`heritageGraph:isAboutDeity`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Murti
  - ➕ skos:definition: "Deity represented and ritually associated with the Murti."@en
  - ➖ skos:definition: "Deity represented and ritually associated with the Murti"@en
- **is composed of** (`crm:P46_is_composed_of`, object property)
  - ➕ owl:inverseOf: crm:P46i_forms_part_of
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "is composed of"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property associates an instance of E18 Physical Thing with another instance of Physical Thing that forms part of it. The spatial extent of the composing part is included in the spatial extent of the whole.
Component elements, since they are themselves instances of E18 Physical Thing, may be further analysed into sub-components, thereby creating a hierarchy of part decomposition. An instance of E18 Physical Thing may be shared between multiple wholes, for example two buildings may share a common wall. This property does not specify when and for how long a component element resided in the respective whole. If a component is not part of a whole from the beginning of existence or until the end of existence of the whole, the classes E79 Part Addition and E90 Part Removal can be used to document when a component became part of a particular whole and/or when it stopped being a part of it. For the time-span of being part of the respective whole, the component is completely contained in the place the whole occupies.
This property is intended to describe specific components that are individually documented, rather than general aspects. Overall descriptions of the structure of an instance of E18 Physical Thing are captured by the P3 has note property.
The instances of E57 Material of which an instance of E18 Physical Thing is composed should be documented using P45 consists of (is incorporated in).
This property is transitive and asymmetric.

Examples:
- The Royal carriage (E22) forms part of the Royal train (E22).
- The “Hog’s Back” (E24) forms part of the “Fosseway” (E24).

In First Order Logic:
- P46(x,y) ⇒ E18(x)
- P46(x,y) ⇒ E18(y)
- P46(x,y) ⇒ P132(x,y)
- [P46(x,y) ∧ P46(y,z)] ⇒ P46(x,z)
- P46(x,y) ⇒ (∃uzw)[E93(u) ∧ P195i (x,u) ∧ E52(z) ∧ P164(u,z) ∧ E93(w) ∧ P195i (w,y) ∧ P164(w,z) ∧ P10(w,u)] 
- P46(x,y) ⇒ ¬P46(y,x)"@en
  - ➖ rdfs:label: "Has component"@en
  - ➖ skos:definition: "Architectural elements composing structure"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Is critical for festival** (`heritageGraph:isCriticalForFestival`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariSelectionEvent
  - ➕ skos:definition: "Whether this ritual is essential for the festival's completion."@en
  - ➖ skos:definition: "Whether this ritual is essential for the festival's completion"@en
- **is current keeper of** (`crm:P50i_is_current_keeper_of`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "is current keeper of"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many (0,n:0,n)

Scope note of the inverse property:
This property identifies the instance of E39 Actor that had custody of an instance of E18 Physical Thing at the time of validity of the record or database containing the statement that uses this property.
This property is a shortcut for the more detailed path from E18 Physical Thing through, P30i custody transferred through, E10 Transfer of Custody, P29 custody received by to E39 Actor, if and only if the custody has not been surrendered by the receiving actor at any later time

Examples of the inverse property:
- The paintings from The Iveagh Bequest (E78) has current keeper The National Gallery (E74) (Iveagh Bequest, 1975)

In First Order Logic of the inverse property:
- P50(x,y) ⇒ E18(x)
- P50(x,y) ⇒ E39(y) 
- P50(x,y) ⇒ P49(x,y)
- P50(x,y) ⇐ (∃z) [[E10(z) ˄ P30i(x,z) ˄ P29(z,y) ]
- ˄ ¬ (∃w) [E10(w) ˄ P30i(x,w) ˄ P28(w,y)˄ P182(z,w)]]"@en
  - ➖ rdfs:label: "Holds custody of"@en
  - ➖ skos:definition: "Structures under Guthi custodianship"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **is current or former member of** (`crm:P107i_is_current_or_former_member_of`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "is current or former member of"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many (0,n:0,n)

Scope note of the inverse property:
This property associates an instance of E74 Group with an instance of E39 Actor that is or has been a member thereof.
Instances of E74 Group and E21 Person may all be members of instances of E74 Group. An instance of E74 Group may be founded initially without any member. 
This property is a shortcut of the more fully developed path from E74 Group, P144i gained member by, E85 Joining, P143 joined to E39 Actor.
The property P107.1 kind of member can be used to specify the type of membership or the role the member has in the group.

Examples of the inverse property:
- László Moholy-Nagy (E21) is current or former member of Bauhaus (E74). (Moholy-Nagy, 2012)
- National Museum of Science and Industry (E74) has current or former member The National Railway Museum (E74). (Rolt, 1971)
- The married couple Queen Elisabeth and Prince Phillip (E74) has current or former member Prince Phillip (E21) kind of member husband (E55). (Brandreth, 2004)

In First Order Logic of the inverse property:
- P107(x,y) ⇒ E74(x)
- P107(x,y) ⇒ E39(y)
- P107(x,y,z) ⇒ [P107(x,y) ∧ E55(z)]
- P107(x,y) ⇐ (∃z) [E85(z) ˄ P144i(x,z) ˄ P143(z,y)]"@en
  - ➖ rdfs:label: "Member of group"@en
  - ➖ skos:definition: "Groups this person belongs to"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **is depicted by** (`crm:P62i_is_depicted_by`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "is depicted by"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many (0,n:0,n)

Scope note of the inverse property:
This property identifies something that is depicted by an instance of E24 Physical Human-Made Thing. Depicting is meant in the sense that an instance of E24 Physical Human-Made Thing intentionally shows, through its optical qualities or form, a representation of the entity depicted. Photographs are by default regarded as being intentional in this sense. Anything that is designed to change the properties of the depiction, such as an e-book reader, is specifically excluded. The property does not pertain to inscriptions or any other information encoding.
This property is a shortcut of the more fully developed path from E24 Physical Human-Made Thing through P65 shows visual item, E36 Visual Item, P138 represents to E1 CRM Entity. P62.1 mode of depiction allows the nature of the depiction to be refined.

Examples of the inverse property:
- The painting “La Liberté guidant le peuple” by Eugène Delacroix (E22) depicts the French “July Revolution” of 1830 (E7). (Delacroix, 1982)
- The 20 pence coin held by the Department of Coins and Medals of the British Museum under registration number 2006,1101.126 (E22) depicts Queen Elizabeth II (E21) mode of depiction Profile (E55).

In First Order Logic of the inverse property:
- P62(x,y) ⇒ E24(x)
- P62(x,y) ⇒ E1(y) 
- P62(x,y,z) ⇒ [P62(x,y) ∧ E55(z)]
- P62(x,y) ⇐ (∃z) [E36(z) ˄ P65(x,z) ˄ P138(z,y)]"@en
  - ➖ rdfs:label: "Is depicted in"@en
  - ➖ skos:definition: "Iconographic objects (murti, paubha) in which this deity is depicted."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Is enshrined through event** (`heritageGraph:isEnshrinedThroughEvent`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Deity
  - ➕ skos:definition: "Events where this deity was enshrined."@en
  - ➖ skos:definition: "Events where this deity was enshrined"@en
- **is former or current location of** (`crm:P53i_is_former_or_current_location_of`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "is former or current location of"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many, necessary (1,n:0,n)

Scope note of the inverse property:
This property identifies an instance of E53 Place as the former or current location of an instance of E18 Physical Thing.
In the case of instances of E19 Physical Object, the property does not allow any indication of the Time-Span during which the instance of E19 Physical Object was located at this instance of E53 Place, nor if this is the current location.
In the case of immobile objects, the Place would normally correspond to the Place of creation.
This property is a shortcut. A more detailed representation can make use of the fully developed (i.e. indirect) path from E19 Physical Object, though, P25i moved by, E9 Move, P26 moved to or P27 moved from to E53 Place.

Examples of the inverse property:
- Silver cup 232 (E22) has former or current location Display Case 4, Room 23, Museum of Oxford (E53). (fictitious)

In First Order Logic of the inverse property:
- P53(x,y) ⇒ E18(x)
- P53(x,y) ⇒ E53(y)
- P53(x,y) ⇐ (∃z) [E9(z) ˄ P25i(x,z) ˄ [P26(z,y) ˅ P27(z,y)]]"@en
  - ➖ rdfs:label: "Contains structure"@en
  - ➖ skos:definition: "Structures located in this place"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Is invoked in ritual** (`heritageGraph:isInvokedInRitual`, object property)
  - ➕ owl:inverseOf: heritageGraph:invokesDeity
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Deity
  - ➕ skos:definition: "Rituals where this deity is invoked."@en
  - ➖ skos:definition: "Rituals where this deity is invoked"@en
- **Is primary for tradition** (`heritageGraph:isPrimaryForTradition`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:CalendarSystem
  - ➕ skos:definition: "Religious tradition(s) that use this calendar system for their rites. Calendars are not divided by religion in Nepal: Nepal Sambat is the era of the Newar ritual calendar, used by Newar Hindus and Buddhists alike, and Bikram Sambat is the official civil era."@en
  - ➖ skos:definition: "Religious tradition(s) that primarily use this calendar system (e.g., Bikram Sambat for Hindu, Nepal Sambat for Newar Buddhist)"@en
- **Jatra** (`https://cair-nepal.org/heritagegraph/RitualType#Jatra`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Festival procession ritual."@en
  - ➖ skos:definition: "Festival procession ritual"@en
- **Jatra Guthi** (`https://cair-nepal.org/heritagegraph/GuthiType#JatraGuthi`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Festival organization trust."@en
  - ➖ skos:definition: "Festival organization trust"@en
- **Kamya Puja** (`https://cair-nepal.org/heritagegraph/RitualType#KamyaPuja`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Desire-based optional worship."@en
  - ➖ skos:definition: "Desire-based optional worship"@en
- **Kumari Enthronement Event** (`heritageGraph:KumariEnthronementEvent`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by min 0
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by only crm:E39_Actor
  - ➖ rdfs:subClassOf: crm:P4_has_time-span min 0
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: crm:P7_took_place_at max 1
  - ➖ rdfs:subClassOf: crm:P7_took_place_at min 0
  - ➖ rdfs:subClassOf: crm:P7_took_place_at only crm:E53_Place
  - ➖ rdfs:subClassOf: heritageGraph:documentedBy min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasAssertion min 0
- **Kumari House** (`heritageGraph:KumariHouse`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **Kumari Lifecycle Event** (`heritageGraph:KumariLifecycleEvent`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Abstract event that bounds a KumariTenure (selection, enthronement, or retirement). Each concrete subclass requires exactly one tenure edge via slot_usage: hg:initiatedTenure (selection), hg:endedTenureOf (retirement), or hg:boundsTenure itself (enthronement)."@en
  - ➖ rdfs:subClassOf: heritageGraph:boundsTenure min 0
  - ➖ skos:definition: "Abstract event that bounds a KumariTenure (selection, enthronement, or retirement). Each concrete subclass requires exactly one tenure edge via slot_usage: initiated_tenure (selection), ended_tenure_of (retirement), or bounds_tenure itself (enthronement)."@en
- **Kumari Retirement Event** (`heritageGraph:KumariRetirementEvent`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Ritual or administrative event that formally ends a Living Goddess tenure according to tradition, returning the person to secular life. Record the event and its date, not the reason: the traditional grounds concern the bodily state of a child, and HeritageGraph does not record health or bodily data about persons."@en
  - ➕ skos:editorialNote: "PROV-O alignment note: prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by min 0
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by only crm:E39_Actor
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: crm:P7_took_place_at max 1
  - ➖ rdfs:subClassOf: crm:P7_took_place_at min 0
  - ➖ rdfs:subClassOf: crm:P7_took_place_at only crm:E53_Place
  - ➖ rdfs:subClassOf: heritageGraph:documentedBy min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasAssertion min 0
  - ➖ rdfs:subClassOf: heritageGraph:performedByGroup min 0
  - ➖ skos:definition: "Ritual or administrative event that formally ends a Living Goddess tenure, returning the person to secular status. Common triggers: first menstruation, injury causing blood loss, serious illness."@en
- **Kumari Role** (`heritageGraph:KumariRole`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: heritageGraph:RitualOffice
  - ➖ rdfs:subClassOf: heritageGraph:roleDeity min 0
  - ➖ rdfs:subClassOf: prov:Entity
- **Kumari Selection Event** (`heritageGraph:KumariSelectionEvent`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Tantric ritual process of selecting a new Living Goddess from eligible candidates. Involves examination of 32 auspicious physical marks (lakshana) and horoscope matching with the city and ruling authority, carried out, in published accounts, by the priests of Taleju and the Buddhist Vajracharya priests with an astrologer. Accounts of a fearlessness test are disputed and are recorded as such with FearlessnessAssessment, not stated here."@en
  - ➕ skos:editorialNote: "PROV-O alignment note: prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by min 0
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by only crm:E39_Actor
  - ➖ rdfs:subClassOf: crm:P4_has_time-span min 0
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: crm:P7_took_place_at max 1
  - ➖ rdfs:subClassOf: crm:P7_took_place_at min 0
  - ➖ rdfs:subClassOf: crm:P7_took_place_at only crm:E53_Place
  - ➖ rdfs:subClassOf: heritageGraph:confersRole min 0
  - ➖ rdfs:subClassOf: heritageGraph:documentedBy min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasAssertion min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasCriterion min 0
  - ➖ rdfs:subClassOf: heritageGraph:isCriticalForFestival min 0
  - ➖ rdfs:subClassOf: heritageGraph:performedByGroup min 0
  - ➖ skos:definition: "Tantric ritual process of selecting a new Living Goddess from eligible candidates. Involves examination of 32 auspicious physical marks (lakshana), horoscope matching with the city and ruling authority, and tests of fearlessness (e.g., remaining calm among buffalo heads and masked dancers in darkness). Performed by committee of Vajracharya priests, royal priest (Raj Jyotish), and astrologer."@en
- **Kumari Tenure** (`heritageGraph:KumariTenure`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: heritageGraph:Tenure
  - ➕ rdfs:subClassOf: heritageGraph:hadParticipant only crm:E39_Actor
  - ➕ rdfs:subClassOf: heritageGraph:supportedByInstitution only crm:E74_Group
  - ➕ rdfs:subClassOf: heritageGraph:tenureHolder max 1
  - ➕ rdfs:subClassOf: heritageGraph:tenureHolder min 1
  - ➕ rdfs:subClassOf: heritageGraph:tenureHolder only crm:E21_Person
  - ➕ skos:editorialNote: "Design note: PROV placement: a prov:Entity, i.e. a thing whose provenance is tracked (sources, attributions, assertions about it), and a crm:E4_Period (stated, 1.1.0). A period is not a crm:E7_Activity, so the class stays outside any E7 ⊑ prov:Activity alignment and the PROV-O Entity/Activity disjointness is not engaged; reasoning with CIDOC-CRM, CRMinf, CRMsci and PROV-O loaded is consistent with the example data."@en
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: heritageGraph:assumesRole min 0
  - ➖ rdfs:subClassOf: heritageGraph:documentedBy min 0
  - ➖ rdfs:subClassOf: heritageGraph:enthronedThrough min 0
  - ➖ rdfs:subClassOf: heritageGraph:hadParticipant min 1
  - ➖ rdfs:subClassOf: heritageGraph:hadParticipant only crm:E21_Person
  - ➖ rdfs:subClassOf: heritageGraph:retiredThrough min 0
  - ➖ rdfs:subClassOf: heritageGraph:selectedThrough min 0
  - ➖ rdfs:subClassOf: heritageGraph:supportedByInstitution min 0
  - ➖ rdfs:subClassOf: heritageGraph:supportedByInstitution only heritageGraph:Guthi
  - ➖ rdfs:subClassOf: prov:Entity
- **Last known existence date** (`heritageGraph:lastKnownExistenceDate`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:ArchitecturalStructure
  - ➕ skos:definition: "Latest date when this structure is documented as existing (ISO 8601)."@en
  - ➖ skos:definition: "Latest date when this structure is documented as existing (ISO 8601)"@en
- **Lineage Criterion** (`heritageGraph:LineageCriterion`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **Lost** (`https://cair-nepal.org/heritagegraph/ExistenceStatus#Lost`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Existence documented but location/remains unknown."@en
  - ➖ skos:definition: "Existence documented but location/remains unknown"@en
- **Lunar date tithi** (`heritageGraph:lunarDateTithi`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "Lunar day (tithi) by which the practice is timed, in free text (e.g. 'Bhadra Shukla Chaturdashi')."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Lunar day (Tithi) for ritual timing"@en
- **Makes deity present** (`heritageGraph:makesDeityPresent`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Consecration
  - ➕ skos:definition: "Deity made present through consecration."@en
  - ➖ skos:definition: "Deity made present through consecration"@en
- **Managed by guthi** (`heritageGraph:managedByGuthi`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:ArchitecturalStructure
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "Guthi organization managing this structure or ritual."@en
  - ➕ skos:relatedMatch: crm:P49_has_former_or_current_keeper
  - ➖ skos:definition: "Guthi organization managing this structure or ritual"@en
- **Masked Dance** (`heritageGraph:MaskedDance`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: heritageGraph:RitualEvent
  - ➕ skos:definition: "Performance in which masked dancers embody deities (e.g. Kartik Naach); usually part of a festival (crm:P9 forms part of), not itself a festival."@en
  - ➖ rdfs:subClassOf: heritageGraph:Festival
  - ➖ skos:definition: "Festival featuring masked dancers embodying deities (e.g., Kartik Naach)"@en
- **Masked Performance** (`https://cair-nepal.org/heritagegraph/RitualType#MaskedPerformance`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Ritual masked dance."@en
  - ➖ skos:definition: "Ritual masked dance"@en
- **Material** (`crm:E57_Material`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ skos:definition: "Scope note:
This class is a specialization of E55 Type and comprises the concepts of materials. 
Instances of E57 Material may denote properties of matter before its use, during its use, and as incorporated in an object, such as ultramarine powder, tempera paste, reinforced concrete. Discrete pieces of raw-materials kept in museums, such as bricks, sheets of fabric, pieces of metal, should be modelled individually in the same way as other objects. Discrete used or processed pieces, such as the stones from Nefer Titi's temple, should be modelled as parts (cf. P46 is composed of (forms part of): E18 Physical Thing).
This type is used categorically in the model without reference to instances of it, i.e. the Model does not foresee the description of instances of instances of E57 Material, e.g. “instances of gold”.
It is recommended that internationally or nationally agreed codes and terminology should be used.

Examples:
- brick (Gurcke, 1987)
- gold (Watson, 1990)
- aluminium (Norman, 1986)
- polycarbonate (Mhaske, 2011)
- resin (Barton, 1992)

In First Order Logic:
- E57(x) ⇒ E55(x)"@en
  - ➖ rdfs:subClassOf: prov:Entity
  - ➖ skos:definition: "Physical substance used in construction or crafting"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Murti** (`heritageGraph:Murti`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Consecrated image or seat of a deity, figural or aniconic (e.g. a stone, a linga, a pitha), ritually activated to serve as divine presence (not merely depiction)."@en
  - ➖ rdfs:subClassOf: heritageGraph:consecratedByEvent min 0
  - ➖ rdfs:subClassOf: heritageGraph:isAboutDeity min 0
  - ➖ skos:definition: "Consecrated statue of a deity, ritually activated to serve as divine presence (not merely depiction)"@en
- **Naimittika Puja** (`https://cair-nepal.org/heritagegraph/RitualType#NaimittikaPuja`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Occasional/Festival worship."@en
  - ➖ skos:definition: "Occasional/Festival worship"@en
- **Nasha Guthi** (`https://cair-nepal.org/heritagegraph/GuthiType#NashaGuthi`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Music and dance trust."@en
  - ➖ skos:definition: "Music and dance trust"@en
- **Nitya Puja** (`https://cair-nepal.org/heritagegraph/RitualType#NityaPuja`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Daily mandatory worship."@en
  - ➖ skos:definition: "Daily mandatory worship"@en
- **obsolete actors** (`heritageGraph:actors`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete actors"@en
  - ➕ skos:definition: "Collection of generic Actor instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "actors"@en
  - ➖ rdfs:range: crm:E39_Actor
  - ➖ skos:definition: "Collection of generic Actor instances"@en
- **obsolete architectural elements** (`heritageGraph:architectural_elements`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete architectural elements"@en
  - ➕ skos:definition: "Collection of ArchitecturalElement instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Architectural elements"@en
  - ➖ rdfs:range: heritageGraph:ArchitecturalElement
  - ➖ skos:definition: "Collection of ArchitecturalElement instances"@en
- **obsolete assertions** (`heritageGraph:assertions`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete assertions"@en
  - ➕ skos:definition: "Collection of Assertion instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "assertions"@en
  - ➖ rdfs:range: crminf:I2_Belief
  - ➖ skos:definition: "Collection of Assertion instances"@en
- **obsolete calendar systems** (`heritageGraph:calendar_systems`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete calendar systems"@en
  - ➕ skos:definition: "Collection of CalendarSystem instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Calendar systems"@en
  - ➖ rdfs:range: heritageGraph:CalendarSystem
  - ➖ skos:definition: "Collection of CalendarSystem instances"@en
- **obsolete caste groups** (`heritageGraph:caste_groups`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete caste groups"@en
  - ➕ skos:definition: "Collection of CasteGroup instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Caste groups"@en
  - ➖ rdfs:range: heritageGraph:CasteGroup
  - ➖ skos:definition: "Collection of CasteGroup instances"@en
- **obsolete Chaitya style** (`https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Chaitya`, concept)
  - ➕ dcterms:isReplacedBy: heritageGraph:Chaitya
  - ➕ dcterms:title: "obsolete Chaitya style"@en
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete Chaitya style"@en
  - ➕ skos:definition: "Buddhist votive shrine style."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: A building type, not an architectural style: type the structure as a Chaitya instead."@en
  - ➕ skos:prefLabel: "obsolete Chaitya style"@en
  - ➖ dcterms:title: "Chaitya style"@en
  - ➖ rdfs:label: "Chaitya style"@en
  - ➖ skos:definition: "Buddhist votive shrine style"@en
  - ➖ skos:prefLabel: "Chaitya style"@en
- **obsolete condition assessments** (`heritageGraph:condition_assessments`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete condition assessments"@en
  - ➕ skos:definition: "Collection of ConditionAssessment instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Condition assessments"@en
  - ➖ rdfs:range: crm:E14_Condition_Assessment
  - ➖ skos:definition: "Collection of ConditionAssessment instances"@en
- **obsolete condition states** (`heritageGraph:condition_states`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete condition states"@en
  - ➕ skos:definition: "Collection of ConditionState instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Condition states"@en
  - ➖ rdfs:range: crm:E3_Condition_State
  - ➖ skos:definition: "Collection of ConditionState instances"@en
- **obsolete consecration events** (`heritageGraph:consecration_events`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete consecration events"@en
  - ➕ skos:definition: "Collection of Consecration event instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Consecration events"@en
  - ➖ rdfs:range: heritageGraph:Consecration
  - ➖ skos:definition: "Collection of Consecration event instances"@en
- **obsolete Container** (`heritageGraph:Container`, class)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete Container"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ heritageGraph:design_note: "Serialization construct, not a domain class: this is the LinkML tree_root that anchors JSON/YAML dataset serializations (its collection properties exist for data exchange only). Reasoners and domain queries should ignore it; RDF instance data does not need a Container node."
  - ➖ rdfs:label: "Container"@en
  - ➖ rdfs:subClassOf: heritageGraph:actors min 0
  - ➖ rdfs:subClassOf: heritageGraph:actors only crm:E39_Actor
  - ➖ rdfs:subClassOf: heritageGraph:architectural_elements min 0
  - ➖ rdfs:subClassOf: heritageGraph:architectural_elements only heritageGraph:ArchitecturalElement
  - ➖ rdfs:subClassOf: heritageGraph:assertions min 0
  - ➖ rdfs:subClassOf: heritageGraph:assertions only crminf:I2_Belief
  - ➖ rdfs:subClassOf: heritageGraph:calendar_systems min 0
  - ➖ rdfs:subClassOf: heritageGraph:calendar_systems only heritageGraph:CalendarSystem
  - ➖ rdfs:subClassOf: heritageGraph:caste_groups min 0
  - ➖ rdfs:subClassOf: heritageGraph:caste_groups only heritageGraph:CasteGroup
  - ➖ rdfs:subClassOf: heritageGraph:condition_assessments min 0
  - ➖ rdfs:subClassOf: heritageGraph:condition_assessments only crm:E14_Condition_Assessment
  - ➖ rdfs:subClassOf: heritageGraph:condition_states min 0
  - ➖ rdfs:subClassOf: heritageGraph:condition_states only crm:E3_Condition_State
  - ➖ rdfs:subClassOf: heritageGraph:consecration_events min 0
  - ➖ rdfs:subClassOf: heritageGraph:consecration_events only heritageGraph:Consecration
  - ➖ rdfs:subClassOf: heritageGraph:custody_events min 0
  - ➖ rdfs:subClassOf: heritageGraph:custody_events only crm:E10_Transfer_of_Custody
  - ➖ rdfs:subClassOf: heritageGraph:data_custodians min 0
  - ➖ rdfs:subClassOf: heritageGraph:data_custodians only heritageGraph:DataCustodian
  - ➖ rdfs:subClassOf: heritageGraph:data_sources min 0
  - ➖ rdfs:subClassOf: heritageGraph:data_sources only heritageGraph:DataSource
  - ➖ rdfs:subClassOf: heritageGraph:deities min 0
  - ➖ rdfs:subClassOf: heritageGraph:deities only heritageGraph:Deity
  - ➖ rdfs:subClassOf: heritageGraph:documentation_activities min 0
  - ➖ rdfs:subClassOf: heritageGraph:documentation_activities only heritageGraph:DocumentationActivity
  - ➖ rdfs:subClassOf: heritageGraph:enshrinement_events min 0
  - ➖ rdfs:subClassOf: heritageGraph:enshrinement_events only heritageGraph:Enshrinement
  - ➖ rdfs:subClassOf: heritageGraph:festivals min 0
  - ➖ rdfs:subClassOf: heritageGraph:festivals only heritageGraph:Festival
  - ➖ rdfs:subClassOf: heritageGraph:guthis min 0
  - ➖ rdfs:subClassOf: heritageGraph:guthis only heritageGraph:Guthi
  - ➖ rdfs:subClassOf: heritageGraph:historical_events min 0
  - ➖ rdfs:subClassOf: heritageGraph:historical_events only heritageGraph:HistoricalEvent
  - ➖ rdfs:subClassOf: heritageGraph:human_made_objects min 0
  - ➖ rdfs:subClassOf: heritageGraph:human_made_objects only crm:E22_Human-Made_Object
  - ➖ rdfs:subClassOf: heritageGraph:iconographic_objects min 0
  - ➖ rdfs:subClassOf: heritageGraph:iconographic_objects only heritageGraph:IconographicObject
  - ➖ rdfs:subClassOf: heritageGraph:information_objects min 0
  - ➖ rdfs:subClassOf: heritageGraph:information_objects only heritageGraph:InformationObject
  - ➖ rdfs:subClassOf: heritageGraph:kumari_lifecycle_events min 0
  - ➖ rdfs:subClassOf: heritageGraph:kumari_lifecycle_events only heritageGraph:KumariLifecycleEvent
  - ➖ rdfs:subClassOf: heritageGraph:kumari_roles min 0
  - ➖ rdfs:subClassOf: heritageGraph:kumari_roles only heritageGraph:KumariRole
  - ➖ rdfs:subClassOf: heritageGraph:kumari_tenures min 0
  - ➖ rdfs:subClassOf: heritageGraph:kumari_tenures only heritageGraph:KumariTenure
  - ➖ rdfs:subClassOf: heritageGraph:materials min 0
  - ➖ rdfs:subClassOf: heritageGraph:materials only crm:E57_Material
  - ➖ rdfs:subClassOf: heritageGraph:metadata max 1
  - ➖ rdfs:subClassOf: heritageGraph:metadata min 0
  - ➖ rdfs:subClassOf: heritageGraph:metadata only heritageGraph:Metadata
  - ➖ rdfs:subClassOf: heritageGraph:persons min 0
  - ➖ rdfs:subClassOf: heritageGraph:persons only crm:E21_Person
  - ➖ rdfs:subClassOf: heritageGraph:physical_heritage_things min 0
  - ➖ rdfs:subClassOf: heritageGraph:physical_heritage_things only heritageGraph:PhysicalHeritageThing
  - ➖ rdfs:subClassOf: heritageGraph:places min 0
  - ➖ rdfs:subClassOf: heritageGraph:places only crm:E53_Place
  - ➖ rdfs:subClassOf: heritageGraph:production_events min 0
  - ➖ rdfs:subClassOf: heritageGraph:production_events only crm:E12_Production
  - ➖ rdfs:subClassOf: heritageGraph:propositions min 0
  - ➖ rdfs:subClassOf: heritageGraph:propositions only heritageGraph:Proposition
  - ➖ rdfs:subClassOf: heritageGraph:religious_traditions min 0
  - ➖ rdfs:subClassOf: heritageGraph:religious_traditions only heritageGraph:ReligiousTradition
  - ➖ rdfs:subClassOf: heritageGraph:ritual_assessments min 0
  - ➖ rdfs:subClassOf: heritageGraph:ritual_assessments only heritageGraph:RitualAssessment
  - ➖ rdfs:subClassOf: heritageGraph:ritual_events min 0
  - ➖ rdfs:subClassOf: heritageGraph:ritual_events only heritageGraph:RitualEvent
  - ➖ rdfs:subClassOf: heritageGraph:selection_criteria min 0
  - ➖ rdfs:subClassOf: heritageGraph:selection_criteria only heritageGraph:SelectionCriterion
  - ➖ rdfs:subClassOf: heritageGraph:structures min 0
  - ➖ rdfs:subClassOf: heritageGraph:structures only heritageGraph:ArchitecturalStructure
  - ➖ rdfs:subClassOf: heritageGraph:syncretic_relationships min 0
  - ➖ rdfs:subClassOf: heritageGraph:syncretic_relationships only heritageGraph:SyncreticRelationship
  - ➖ rdfs:subClassOf: heritageGraph:techniques min 0
  - ➖ rdfs:subClassOf: heritageGraph:techniques only crm:E29_Design_or_Procedure
  - ➖ rdfs:subClassOf: heritageGraph:time_spans min 0
  - ➖ rdfs:subClassOf: heritageGraph:time_spans only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: prov:Entity
  - ➖ skos:broadMatch: prov:Collection
- **obsolete crminf pattern** (`heritageGraph:crminf_pattern`, annotation property)
  - ➕ dcterms:isReplacedBy: skos:editorialNote
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete crminf pattern"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: the note is published as skos:editorialNote with the prefix 'CRMinf pattern: '."@en
  - ➕ skos:inScheme: heritageGraph:schema
  - ➖ rdfs:label: "crminf pattern"@en
- **obsolete curator** (`heritageGraph:curator`, datatype property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete curator"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "curator"@en
  - ➖ rdfs:range: xsd:string
- **obsolete custody events** (`heritageGraph:custody_events`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete custody events"@en
  - ➕ skos:definition: "Collection of TransferOfCustody event instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Custody events"@en
  - ➖ rdfs:range: crm:E10_Transfer_of_Custody
  - ➖ skos:definition: "Collection of TransferOfCustody event instances"@en
- **obsolete data custodians** (`heritageGraph:data_custodians`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete data custodians"@en
  - ➕ skos:definition: "Collection of DataCustodian instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Data custodians"@en
  - ➖ rdfs:range: heritageGraph:DataCustodian
  - ➖ skos:definition: "Collection of DataCustodian instances"@en
- **obsolete data sources** (`heritageGraph:data_sources`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete data sources"@en
  - ➕ skos:definition: "Collection of DataSource instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Data sources"@en
  - ➖ rdfs:range: heritageGraph:DataSource
  - ➖ skos:definition: "Collection of DataSource instances"@en
- **obsolete dataset name** (`heritageGraph:dataset_name`, datatype property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete dataset name"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Dataset name"@en
  - ➖ rdfs:range: xsd:string
- **obsolete dataset version** (`heritageGraph:dataset_version`, datatype property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete dataset version"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Dataset version"@en
  - ➖ rdfs:range: xsd:string
- **obsolete deities** (`heritageGraph:deities`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete deities"@en
  - ➕ skos:definition: "Collection of Deity instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "deities"@en
  - ➖ rdfs:range: heritageGraph:Deity
  - ➖ skos:definition: "Collection of Deity instances"@en
- **obsolete design note** (`heritageGraph:design_note`, annotation property)
  - ➕ dcterms:isReplacedBy: skos:editorialNote
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete design note"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: the note is published as skos:editorialNote with the prefix 'Design note: '."@en
  - ➕ skos:inScheme: heritageGraph:schema
  - ➖ rdfs:label: "design note"@en
- **obsolete documentation activities** (`heritageGraph:documentation_activities`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete documentation activities"@en
  - ➕ skos:definition: "Collection of DocumentationActivity instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Documentation activities"@en
  - ➖ rdfs:range: heritageGraph:DocumentationActivity
  - ➖ skos:definition: "Collection of DocumentationActivity instances"@en
- **obsolete enshrinement events** (`heritageGraph:enshrinement_events`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete enshrinement events"@en
  - ➕ skos:definition: "Collection of Enshrinement event instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Enshrinement events"@en
  - ➖ rdfs:range: heritageGraph:Enshrinement
  - ➖ skos:definition: "Collection of Enshrinement event instances"@en
- **obsolete festivals** (`heritageGraph:festivals`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete festivals"@en
  - ➕ skos:definition: "Collection of Festival instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "festivals"@en
  - ➖ rdfs:range: heritageGraph:Festival
  - ➖ skos:definition: "Collection of Festival instances"@en
- **obsolete generated date** (`heritageGraph:generated_date`, datatype property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete generated date"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Generated date"@en
  - ➖ rdfs:range: xsd:string
- **obsolete guthis** (`heritageGraph:guthis`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete guthis"@en
  - ➕ skos:definition: "Collection of Guthi instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "guthis"@en
  - ➖ rdfs:range: heritageGraph:Guthi
  - ➖ skos:definition: "Collection of Guthi instances"@en
- **obsolete has metadata** (`heritageGraph:metadata`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete has metadata"@en
  - ➕ skos:definition: "Dataset metadata."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ dcterms:title: "has metadata"@en
  - ➖ rdfs:label: "has metadata"@en
  - ➖ rdfs:range: heritageGraph:Metadata
  - ➖ skos:definition: "Dataset metadata"@en
- **obsolete historical events** (`heritageGraph:historical_events`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete historical events"@en
  - ➕ skos:definition: "Collection of HistoricalEvent (incl. DestructionEvent) instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Historical events"@en
  - ➖ rdfs:range: heritageGraph:HistoricalEvent
  - ➖ skos:definition: "Collection of HistoricalEvent (incl. DestructionEvent) instances"@en
- **obsolete human made objects** (`heritageGraph:human_made_objects`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete human made objects"@en
  - ➕ skos:definition: "Collection of generic HumanMadeObject instances (use structures / iconographic_objects for subclasses)."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Human made objects"@en
  - ➖ rdfs:range: crm:E22_Human-Made_Object
  - ➖ skos:definition: "Collection of generic HumanMadeObject instances (use structures / iconographic_objects for subclasses)"@en
- **obsolete iconographic objects** (`heritageGraph:iconographic_objects`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete iconographic objects"@en
  - ➕ skos:definition: "Collection of IconographicObject instances (incl. Murti, Paubha)."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Iconographic objects"@en
  - ➖ rdfs:range: heritageGraph:IconographicObject
  - ➖ skos:definition: "Collection of IconographicObject instances (incl. Murti, Paubha)"@en
- **obsolete information objects** (`heritageGraph:information_objects`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete information objects"@en
  - ➕ skos:definition: "Collection of InformationObject instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Information objects"@en
  - ➖ rdfs:range: heritageGraph:InformationObject
  - ➖ skos:definition: "Collection of InformationObject instances"@en
- **obsolete kumari lifecycle events** (`heritageGraph:kumari_lifecycle_events`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete kumari lifecycle events"@en
  - ➕ skos:definition: "Collection of Kumari lifecycle events (selection, enthronement, retirement)."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Kumari lifecycle events"@en
  - ➖ rdfs:range: heritageGraph:KumariLifecycleEvent
  - ➖ skos:definition: "Collection of Kumari lifecycle events (selection, enthronement, retirement)"@en
- **obsolete kumari roles** (`heritageGraph:kumari_roles`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete kumari roles"@en
  - ➕ skos:definition: "Collection of KumariRole instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Kumari roles"@en
  - ➖ rdfs:range: heritageGraph:KumariRole
  - ➖ skos:definition: "Collection of KumariRole instances"@en
- **obsolete kumari tenures** (`heritageGraph:kumari_tenures`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete kumari tenures"@en
  - ➕ skos:definition: "Collection of KumariTenure instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Kumari tenures"@en
  - ➖ rdfs:range: heritageGraph:KumariTenure
  - ➖ skos:definition: "Collection of KumariTenure instances"@en
- **obsolete license** (`heritageGraph:license`, datatype property)
  - ➕ dcterms:isReplacedBy: dcterms:license
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete license"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "license"@en
  - ➖ rdfs:range: xsd:string
- **obsolete materials** (`heritageGraph:materials`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete materials"@en
  - ➕ skos:definition: "Collection of Material instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "materials"@en
  - ➖ rdfs:range: crm:E57_Material
  - ➖ skos:definition: "Collection of Material instances"@en
- **obsolete Metadata** (`heritageGraph:Metadata`, class)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete Metadata"@en
  - ➕ skos:definition: "Dataset metadata information."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Metadata"@en
  - ➖ rdfs:subClassOf: heritageGraph:curator max 1
  - ➖ rdfs:subClassOf: heritageGraph:curator min 0
  - ➖ rdfs:subClassOf: heritageGraph:curator only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:dataset_name max 1
  - ➖ rdfs:subClassOf: heritageGraph:dataset_name min 0
  - ➖ rdfs:subClassOf: heritageGraph:dataset_name only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:dataset_version max 1
  - ➖ rdfs:subClassOf: heritageGraph:dataset_version min 0
  - ➖ rdfs:subClassOf: heritageGraph:dataset_version only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:generated_date max 1
  - ➖ rdfs:subClassOf: heritageGraph:generated_date min 0
  - ➖ rdfs:subClassOf: heritageGraph:generated_date only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:license max 1
  - ➖ rdfs:subClassOf: heritageGraph:license min 0
  - ➖ rdfs:subClassOf: heritageGraph:license only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:schema_version max 1
  - ➖ rdfs:subClassOf: heritageGraph:schema_version min 0
  - ➖ rdfs:subClassOf: heritageGraph:schema_version only xsd:string
  - ➖ rdfs:subClassOf: prov:Entity
  - ➖ skos:definition: "Dataset metadata information"@en
- **obsolete persons** (`heritageGraph:persons`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete persons"@en
  - ➕ skos:definition: "Collection of Person instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "persons"@en
  - ➖ rdfs:range: crm:E21_Person
  - ➖ skos:definition: "Collection of Person instances"@en
- **obsolete physical heritage things** (`heritageGraph:physical_heritage_things`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete physical heritage things"@en
  - ➕ skos:definition: "Collection of all physical heritage objects."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Physical heritage things"@en
  - ➖ rdfs:range: heritageGraph:PhysicalHeritageThing
  - ➖ skos:definition: "Collection of all physical heritage objects"@en
- **obsolete places** (`heritageGraph:places`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete places"@en
  - ➕ skos:definition: "Collection of Place instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "places"@en
  - ➖ rdfs:range: crm:E53_Place
  - ➖ skos:definition: "Collection of Place instances"@en
- **obsolete production events** (`heritageGraph:production_events`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete production events"@en
  - ➕ skos:definition: "Collection of Production event instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Production events"@en
  - ➖ rdfs:range: crm:E12_Production
  - ➖ skos:definition: "Collection of Production event instances"@en
- **obsolete propositions** (`heritageGraph:propositions`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete propositions"@en
  - ➕ skos:definition: "Collection of Proposition instances referenced by assertions."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "propositions"@en
  - ➖ rdfs:range: heritageGraph:Proposition
  - ➖ skos:definition: "Collection of Proposition instances referenced by assertions"@en
- **obsolete prov alignment** (`heritageGraph:prov_alignment`, annotation property)
  - ➕ dcterms:isReplacedBy: skos:editorialNote
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete prov alignment"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: the note is published as skos:editorialNote with the prefix 'PROV-O alignment: '."@en
  - ➕ skos:inScheme: heritageGraph:schema
  - ➖ rdfs:label: "prov alignment"@en
- **obsolete prov alignment note** (`heritageGraph:prov_alignment_note`, annotation property)
  - ➕ dcterms:isReplacedBy: skos:editorialNote
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete prov alignment note"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: the note is published as skos:editorialNote with the prefix 'PROV-O alignment note: '."@en
  - ➕ skos:inScheme: heritageGraph:schema
  - ➖ rdfs:label: "prov alignment note"@en
- **obsolete provenance scope** (`heritageGraph:provenance_scope`, annotation property)
  - ➕ dcterms:isReplacedBy: skos:editorialNote
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete provenance scope"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: the note is published as skos:editorialNote with the prefix 'Provenance scope: '."@en
  - ➕ skos:inScheme: heritageGraph:schema
  - ➖ rdfs:label: "provenance scope"@en
- **obsolete religious traditions** (`heritageGraph:religious_traditions`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete religious traditions"@en
  - ➕ skos:definition: "Collection of ReligiousTradition instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Religious traditions"@en
  - ➖ rdfs:range: heritageGraph:ReligiousTradition
  - ➖ skos:definition: "Collection of ReligiousTradition instances"@en
- **obsolete ritual assessments** (`heritageGraph:ritual_assessments`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete ritual assessments"@en
  - ➕ skos:definition: "Collection of RitualAssessment (e.g. FearlessnessAssessment) instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Ritual assessments"@en
  - ➖ rdfs:range: heritageGraph:RitualAssessment
  - ➖ skos:definition: "Collection of RitualAssessment (e.g. FearlessnessAssessment) instances"@en
- **obsolete ritual events** (`heritageGraph:ritual_events`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete ritual events"@en
  - ➕ skos:definition: "Collection of RitualEvent instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Ritual events"@en
  - ➖ rdfs:range: heritageGraph:RitualEvent
  - ➖ skos:definition: "Collection of RitualEvent instances"@en
- **obsolete San Guthi** (`https://cair-nepal.org/heritagegraph/GuthiType#SanGuthi`, concept)
  - ➕ dcterms:isReplacedBy: https://cair-nepal.org/heritagegraph/GuthiType#SanaGuthi
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete San Guthi"@en
  - ➕ skos:definition: "Variant spelling of sanah guthi."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: A duplicate of SanaGuthi (variant spelling of sanah guthi), previously glossed wrongly as a life-cycle ritual trust."@en
  - ➕ skos:prefLabel: "obsolete San Guthi"@en
  - ➖ rdfs:label: "San Guthi"@en
  - ➖ skos:definition: "Life-cycle ritual trust"@en
  - ➖ skos:prefLabel: "San Guthi"@en
- **obsolete schema version** (`heritageGraph:schema_version`, datatype property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete schema version"@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Schema version"@en
  - ➖ rdfs:range: xsd:string
- **obsolete selection criteria** (`heritageGraph:selection_criteria`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete selection criteria"@en
  - ➕ skos:definition: "Collection of SelectionCriterion instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Selection criteria"@en
  - ➖ rdfs:range: heritageGraph:SelectionCriterion
  - ➖ skos:definition: "Collection of SelectionCriterion instances"@en
- **obsolete selection criteria met** (`heritageGraph:selectionCriteriaMet`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ skos:definition: "DEPRECATED free-text list; use hg:hasCriterion -> SelectionCriterion subclasses instead. Retained for backward compatibility."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "DEPRECATED free-text list; use has_criterion -> SelectionCriterion subclasses instead. Retained for backward compatibility."@en
- **obsolete structures** (`heritageGraph:structures`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete structures"@en
  - ➕ skos:definition: "Collection of ArchitecturalStructure instances (incl. subclasses)."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "structures"@en
  - ➖ rdfs:range: heritageGraph:ArchitecturalStructure
  - ➖ skos:definition: "Collection of ArchitecturalStructure instances (incl. subclasses)"@en
- **obsolete Stupa style** (`https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Stupa`, concept)
  - ➕ dcterms:isReplacedBy: heritageGraph:Stupa
  - ➕ dcterms:title: "obsolete Stupa style"@en
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete Stupa style"@en
  - ➕ skos:definition: "Buddhist dome-shaped reliquary."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: A building type, not an architectural style: type the structure as a Stupa instead."@en
  - ➕ skos:prefLabel: "obsolete Stupa style"@en
  - ➖ dcterms:title: "Stupa style"@en
  - ➖ rdfs:label: "Stupa style"@en
  - ➖ skos:definition: "Buddhist dome-shaped reliquary"@en
  - ➖ skos:prefLabel: "Stupa style"@en
- **obsolete syncretic relationships** (`heritageGraph:syncretic_relationships`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete syncretic relationships"@en
  - ➕ skos:definition: "Collection of SyncreticRelationship instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Syncretic relationships"@en
  - ➖ rdfs:range: heritageGraph:SyncreticRelationship
  - ➖ skos:definition: "Collection of SyncreticRelationship instances"@en
- **obsolete techniques** (`heritageGraph:techniques`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete techniques"@en
  - ➕ skos:definition: "Collection of Technique instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "techniques"@en
  - ➖ rdfs:range: crm:E29_Design_or_Procedure
  - ➖ skos:definition: "Collection of Technique instances"@en
- **obsolete time spans** (`heritageGraph:time_spans`, object property)
  - ➕ owl:deprecated: true
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "obsolete time spans"@en
  - ➕ skos:definition: "Collection of TimeSpan instances."@en
  - ➕ skos:editorialNote: "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for JSON/YAML data files, not a domain term. It is defined in HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance data should not use it."@en
  - ➖ rdfs:label: "Time spans"@en
  - ➖ rdfs:range: crm:E52_Time-Span
  - ➖ skos:definition: "Collection of TimeSpan instances"@en
- **occurred in the presence of** (`crm:P12_occurred_in_the_presence_of`, object property)
  - ➕ owl:inverseOf: crm:P12i_was_present_at
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "occurred in the presence of"@en
  - ➕ skos:definition: "Quantification: many to many, necessary (1,n:0,n)

Scope note:
This property describes the active or passive presence of an E77 Persistent Item in an instance of E5 Event without implying any specific role. 
It documents known events in which an instance of E77 Persistent Item was present during the course of its life or history. For example, an object may be the desk, now in a museum, on which a treaty was signed. The instance of E53 Place and the instance of E52 Time-Span where and when these events happened provide constraints about the presence of the related instance E77 Persistent Item in the past. Instances of E90 Symbolic Object, in particular information objects, are physically present in events via at least one of the instances of E18 Physical Thing carrying them. Note, that the human mind can be such a carrier. A precondition for a transfer of information to a person or another new physical carrier is the presence of the respective information object and this person or physical thing in one event.

Examples:
- Deckchair 42 (E19) was present at the sinking of the Titanic (E5). (Aldridge, 2008)

In First Order Logic:
- P12(x,y) ⇒ E5(x)
- P12(x,y) ⇒ E77(y)"@en
  - ➖ rdfs:label: "Occurred in presence of"@en
  - ➖ skos:definition: "Generic CRM presence relation (P12): entity present at an event. Canonical holder of the CRM predicate; use the specific presence slots in data."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Oral History Interview** (`heritageGraph:OralHistoryInterview`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **Oral History Recording** (`heritageGraph:OralHistoryRecording`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **Pagoda style** (`https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Pagoda`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Multi-tiered roof form of the Kathmandu Valley, as in the Newar tiered temple: roofs that diminish upward and rest on carved struts (also used on other building types)."@en
  - ➖ skos:definition: "Multi-tiered roof style indigenous to Nepal"@en
- **Part of selection** (`heritageGraph:partOfSelection`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:RitualAssessment
- **Partially Extant** (`https://cair-nepal.org/heritagegraph/ExistenceStatus#PartiallyExtant`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Fragments or ruins remain."@en
  - ➖ skos:definition: "Fragments or ruins remain"@en
- **Participates in ritual** (`heritageGraph:participatesInRitual`, object property)
  - ➕ rdfs:domain: crm:E22_Human-Made_Object
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Rituals in which this structure participates."@en
  - ➖ skos:definition: "Rituals in which this structure participates"@en
- **Pati** (`heritageGraph:Pati`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Open-air pavilion for resting travelers."@en
  - ➖ skos:definition: "Open-air pavilion for resting travelers"@en
- **Paubha** (`heritageGraph:Paubha`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Traditional Newar religious scroll painting, Hindu or Buddhist, with mandala and deity iconography; related to, but not the same as, the Tibetan thangka."@en
  - ➖ skos:definition: "Traditional Newari scroll painting (thangka) with mandala and deity iconography"@en
- **performed** (`crm:P14i_performed`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "performed"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many, necessary (1,n:0,n)

Scope note of the inverse property:
This property describes the active participation of an instance of E39 Actor in an instance of E7 Activity. 
It implies causal or legal responsibility. The P14.1 in the role of property of the property specifies the nature of an Actor’s participation.

Examples of the inverse property:
- The painting of the Sistine Chapel (E7) carried out by Michelangelo Buonaroti (E21) in the role of master craftsman (E55). (Goldscheider, 1953)

In First Order Logic of the inverse property:
- P14(x,y) ⇒ E7(x)
- P14(x,y)⇒ E39(y)
- P14(x,y) ⇒ P11(x,y)
- P14(x,y,z) ⇒ [P14(x,y) ∧ E55(z)]"@en
  - ➖ rdfs:label: "Carried out activity"@en
  - ➖ skos:definition: "Activities performed by this actor"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Performed by group** (`heritageGraph:performedByGroup`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "Group (Guthi, caste) responsible for ritual."@en
  - ➖ skos:definition: "Group (Guthi, caste) responsible for ritual"@en
- **Performs ritual** (`heritageGraph:performsRitual`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Guthi
  - ➕ skos:definition: "Rituals performed by this Guthi."@en
  - ➖ skos:definition: "Rituals performed by this Guthi"@en
- **Person** (`crm:E21_Person`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ skos:definition: "Scope note:
This class comprises real persons who live or are assumed to have lived. 
Legendary figures that may have existed, such as Ulysses and King Arthur, fall into this class if the documentation refers to them as historical figures. In cases where doubt exists as to whether several persons are in fact identical, multiple instances can be created and linked to indicate their relationship. The CIDOC CRM does not propose a specific form to support reasoning about possible identity.
In a bibliographic context, a name presented following the conventions usually employed for personal names will be assumed to correspond to an actual real person (an instance of E21 Person), unless evidence is available to indicate that this is not the case. The fact that a persona may erroneously be classified as an instance of E21 Person does not imply that the concept comprises personae.

Examples:
- Tut-Ankh-Amun (Edwards and Boltin, 1979)
- Nelson Mandela (Brown and Hort, 2006)

In First Order Logic:
- E21(x) ⇒ E20(x)
- E21(x) ⇒ E39(x)"@en
  - ➖ skos:definition: "Individual person who performs, commissions, documents, or verifies heritage activities"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Physical Heritage Thing** (`heritageGraph:PhysicalHeritageThing`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
- **Physical Integrity Criterion** (`heritageGraph:PhysicalIntegrityCriterion`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "The traditional requirement of physical integrity in a candidate. HeritageGraph records that the criterion belongs to the selection, not any assessment of a candidate's body or health."@en
  - ➖ skos:definition: "Candidate must have an unblemished body with no scars, wounds, or loss of blood/teeth."@en
- **Place** (`crm:E53_Place`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ skos:definition: "Scope note:
This class comprises extents in the natural space where people live, in particular on the surface of the Earth, in the pure sense of physics: independent from temporal phenomena and matter. They may serve describing the physical location of things or phenomena or other areas of interest. Geometrically, instances of E53 Place constitute single contiguous areas or a finite aggregation of disjoint areas in space which are each individually contiguous. They may have fuzzy boundaries.
The instances of E53 Place are usually determined by reference to the position of “immobile” objects such as buildings, cities, mountains, rivers, or dedicated geodetic marks, but may also be determined by reference to mobile objects. A Place can be determined by combining a frame of reference and a location with respect to this frame.
It is sometimes argued that instances of E53 Place are best identified by global coordinates or absolute reference systems. However, relative references are often more relevant in the context of cultural documentation and tend to be more precise. In particular, people are often interested in position in relation to large, mobile objects, such as ships. For example, the Place at which Nelson died is known with reference to a large mobile object, i.e. H.M.S Victory. A resolution of this Place in terms of absolute coordinates would require knowledge of the movements of the vessel and the precise time of death, either of which may be revised, and the result would lack historical and cultural relevance.
Any instance of E18 Physical Thing can serve as a frame of reference for an instance of E53 Place. This may be documented using the property P157 is at rest relative to (provides reference space for).

Examples:
- the extent of the UK in the year 2003
- the position of the hallmark on the inside of my wedding ring (fictitious)
- the place referred to in the phrase: “Fish collected at three miles north of the confluence of the Arve and the Rhone”
- here -&gt; &lt;- [the place between these two arrows in one of the reader's paper copy of this document. Each copy constitutes a different place of this spot.]

In First Order Logic:
- E53(x) ⇒ E1(x)"@en
  - ➖ rdfs:subClassOf: prov:Entity
  - ➖ skos:definition: "Defined geographic location where events occur and structures exist"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Place type** (`heritageGraph:placeType`, datatype property)
  - ➕ rdfs:domain: crm:E53_Place
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ skos:definition: "Type of place (city, village, region), free text."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Type of place (city, village, region), free text"@en
- **Pokhari** (`heritageGraph:Pokhari`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Pond or tank for water storage, ritual bathing, and ecological management."@en
  - ➖ skos:definition: "Pond or tank for water storage, ritual bathing, and ecological management"@en
- **Procession Ritual** (`https://cair-nepal.org/heritagegraph/RitualType#ProcessionRitual`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Ritual procession/movement."@en
  - ➖ skos:definition: "Ritual procession/movement"@en
- **Processional Movement** (`https://cair-nepal.org/heritagegraph/RitualType#ProcessionalMovement`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "General ritual movement between locations."@en
  - ➖ skos:definition: "General ritual movement between locations"@en
- **Production** (`crm:E12_Production`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ skos:definition: "Scope note:
This class comprises activities that are designed to, and succeed in, creating one or more new items. 
It specializes the notion of modification into production. The decision as to whether or not an object is regarded as new is context sensitive. Normally, items are considered “new” if there is no obvious overall similarity between them and the consumed items and material used in their production. In other cases, an item is considered “new” because it becomes relevant to documentation by a modification. For example, the scribbling of a name on a potsherd may make it a voting token. The original potsherd may not be worth documenting, in contrast to the inscribed one. 
This entity can be collective: the printing of a thousand books, for example, would normally be considered a single event. 
An event should also be documented using an instance of E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the originals. In this case, the new items have separate identities and matter is preserved, but identity is not.

Examples:
- the construction of the SS Great Britain (Gregor, 1971)
- the first casting of the Little Mermaid from the harbour of Copenhagen (Dewey, 2003)
- Rembrandt’s creating of the seventh state of his etching “Woman sitting half dressed beside a stove”, 1658, identified by Bartsch Number 197 (E12, E65, E81) (Hind, 1923)

In First Order Logic:
- E12(x) ⇒ E11(x)
- E12(x) ⇒ E63(x)"@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: prov:Activity
  - ➖ skos:definition: "Event of creating an architectural structure, murti, or paubha"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Proposition** (`heritageGraph:Proposition`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crminf:I4_Proposition_Set
  - ➕ rdfs:subClassOf: heritageGraph:propositionLiteralValue only rdfs:Literal
  - ➖ rdfs:subClassOf: heritageGraph:propositionLiteralValue min 0
  - ➖ rdfs:subClassOf: heritageGraph:propositionLiteralValue only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:propositionObjectEntity min 0
  - ➖ skos:broadMatch: crminf:I4_Proposition_Set
- **Proposition object entity** (`heritageGraph:propositionObjectEntity`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Proposition
- **Proposition object literal** (`heritageGraph:propositionLiteralValue`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdfs:Literal
  - ➕ schema1:domainIncludes: heritageGraph:Proposition
  - ➖ rdfs:range: xsd:string
- **Proposition predicate** (`heritageGraph:propositionPredicate`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Proposition
- **Proposition subject** (`heritageGraph:propositionSubject`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Proposition
- **Publication timespan** (`heritageGraph:publicationTimespan`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:DataSource
  - ➕ skos:definition: "When source was published."@en
  - ➖ rdfs:subPropertyOf: crm:P4_has_time-span
  - ➖ skos:definition: "When source was published"@en
- **Puja Guthi** (`https://cair-nepal.org/heritagegraph/GuthiType#PujaGuthi`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Daily worship trust."@en
  - ➖ skos:definition: "Daily worship trust"@en
- **Raj Guthi** (`https://cair-nepal.org/heritagegraph/GuthiType#RajGuthi`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Raj guthi (state trust): a guthi in which the Guthi Sansthan holds rights and which it manages and operates, under the Guthi Corporation Act 2033 BS (1976); a legal-administrative status, not a functional type."@en
  - ➖ skos:definition: "Royal endowment trust"@en
- **Reconciliation status** (`heritageGraph:reconciliationStatus`, datatype property)
  - ➕ rdfs:domain: crminf:I2_Belief
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Status of multi-source reconciliation of the asserted value: confirmed (independent sources agree), conflicting (sources disagree; see the competing assertions), or unverified (single source, not yet checked)."@en
  - ➖ skos:definition: "Status of multi-source reconciliation (confirmed, conflicting, unverified)"@en
- **records** (`heritageGraph:documents`, object property)
  - ➕ dcterms:title: "records"@en
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "records"@en
  - ➕ schema1:domainIncludes: heritageGraph:DocumentationActivity
  - ➕ skos:definition: "Pre-existing heritage entity or event recorded by this documentation activity (inverse of hg:documentedBy)."@en
  - ➕ skos:relatedMatch: crm:P70_documents
  - ➖ rdfs:label: "documents"@en
  - ➖ skos:definition: "Pre-existing heritage entity or event recorded by this documentation activity (inverse of was_documented_by)."@en
- **Recurrence pattern** (`heritageGraph:recurrencePattern`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "How the practice this occurrence belongs to recurs (e.g. annual, monthly), in free text. It describes the practice, not the occurrence: each occurrence is its own RitualEvent with its own time-span."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Frequency of recurring ritual (e.g., annual, monthly)"@en
- **Relic Tour** (`https://cair-nepal.org/heritagegraph/RitualType#RelicTour`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Procession with sacred relics between sites."@en
  - ➖ skos:definition: "Procession with sacred relics between sites"@en
- **Religious Structure** (`heritageGraph:ReligiousStructure`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➖ rdfs:subClassOf: heritageGraph:hasReligiousTradition min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasReligiousTradition only heritageGraph:ReligiousTradition
- **Religious Tradition** (`heritageGraph:ReligiousTradition`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E55_Type
  - ➕ skos:definition: "Religious or philosophical tradition (e.g., Hindu, Buddhist, Syncretic)."@en
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ skos:broadMatch: crm:E55_Type
  - ➖ skos:definition: "Religious or philosophical tradition (e.g., Hindu, Buddhist, Syncretic)"@en
- **Residence structure** (`heritageGraph:residenceStructure`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariTenure
- **Rest House** (`heritageGraph:RestHouse`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Community structures for travelers and pilgrims, maintained by Guthi organizations."@en
  - ➖ skos:definition: "Community structures for travelers and pilgrims, maintained by Guthi organizations"@en
- **Restored** (`https://cair-nepal.org/heritagegraph/ConditionType#Restored`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Repaired and stabilized."@en
  - ➖ skos:definition: "Repaired and stabilized"@en
- **Retired through** (`heritageGraph:retiredThrough`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subPropertyOf: heritageGraph:tenureClosedBy
  - ➕ schema1:domainIncludes: heritageGraph:KumariTenure
- **Returning Ritual** (`https://cair-nepal.org/heritagegraph/RitualType#ReturningRitual`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Return to normal state ritual."@en
  - ➖ skos:definition: "Return to normal state ritual"@en
- **Ritual Assessment** (`heritageGraph:RitualAssessment`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by min 0
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by only crm:E39_Actor
  - ➖ rdfs:subClassOf: crm:P4_has_time-span min 0
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: heritageGraph:assessesCandidate min 0
  - ➖ rdfs:subClassOf: heritageGraph:documentedBy min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasAssertion min 0
  - ➖ rdfs:subClassOf: heritageGraph:partOfSelection min 0
- **Ritual Consecration** (`https://cair-nepal.org/heritagegraph/RitualType#RitualConsecration`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Consecration/activation ritual."@en
  - ➖ skos:definition: "Consecration/activation ritual"@en
- **Ritual Event** (`heritageGraph:RitualEvent`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E7_Activity
  - ➕ rdfs:subClassOf: heritageGraph:lunarDateTithi only rdf:PlainLiteral
  - ➕ rdfs:subClassOf: heritageGraph:recurrencePattern only rdf:PlainLiteral
  - ➕ rdfs:subClassOf: heritageGraph:routeDescription only rdf:PlainLiteral
  - ➕ skos:definition: "Intentional ritual activity that activates sacred space, invokes deities, and binds social groups. An instance is one dated occurrence (one CIDOC-CRM E7 with at most one time-span), e.g. the Indra Jatra of 2025; the recurring practice it belongs to (annual, by lunar date) is described by hg:recurrencePattern and hg:lunarDateTithi, not by the instance's time-span."@en
  - ➕ skos:editorialNote: "PROV-O alignment note: prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: crm:P125_used_object_of_type min 0
  - ➖ rdfs:subClassOf: crm:P125_used_object_of_type only crm:E57_Material
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by min 0
  - ➖ rdfs:subClassOf: crm:P14_carried_out_by only crm:E39_Actor
  - ➖ rdfs:subClassOf: crm:P183_ends_before_the_start_of max 1
  - ➖ rdfs:subClassOf: crm:P183_ends_before_the_start_of min 0
  - ➖ rdfs:subClassOf: crm:P183_ends_before_the_start_of only heritageGraph:RitualEvent
  - ➖ rdfs:subClassOf: crm:P183i_starts_after_the_end_of max 1
  - ➖ rdfs:subClassOf: crm:P183i_starts_after_the_end_of min 0
  - ➖ rdfs:subClassOf: crm:P183i_starts_after_the_end_of only heritageGraph:RitualEvent
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: crm:P4_has_time-span min 0
  - ➖ rdfs:subClassOf: crm:P4_has_time-span only crm:E52_Time-Span
  - ➖ rdfs:subClassOf: crm:P7_took_place_at max 1
  - ➖ rdfs:subClassOf: crm:P7_took_place_at min 0
  - ➖ rdfs:subClassOf: crm:P7_took_place_at only crm:E53_Place
  - ➖ rdfs:subClassOf: crm:P8_took_place_on_or_within max 1
  - ➖ rdfs:subClassOf: crm:P8_took_place_on_or_within min 0
  - ➖ rdfs:subClassOf: crm:P8_took_place_on_or_within only heritageGraph:PhysicalHeritageThing
  - ➖ rdfs:subClassOf: crm:P9i_forms_part_of max 1
  - ➖ rdfs:subClassOf: crm:P9i_forms_part_of min 0
  - ➖ rdfs:subClassOf: crm:P9i_forms_part_of only heritageGraph:Festival
  - ➖ rdfs:subClassOf: heritageGraph:documentedBy min 0
  - ➖ rdfs:subClassOf: heritageGraph:endPlace min 0
  - ➖ rdfs:subClassOf: heritageGraph:hadParticipant min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasAssertion min 0
  - ➖ rdfs:subClassOf: heritageGraph:invokesDeity min 0
  - ➖ rdfs:subClassOf: heritageGraph:lunarDateTithi max 1
  - ➖ rdfs:subClassOf: heritageGraph:lunarDateTithi min 0
  - ➖ rdfs:subClassOf: heritageGraph:lunarDateTithi only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:managedByGuthi min 0
  - ➖ rdfs:subClassOf: heritageGraph:performedByGroup min 0
  - ➖ rdfs:subClassOf: heritageGraph:recurrencePattern max 1
  - ➖ rdfs:subClassOf: heritageGraph:recurrencePattern min 0
  - ➖ rdfs:subClassOf: heritageGraph:recurrencePattern only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:ritualType min 0
  - ➖ rdfs:subClassOf: heritageGraph:routeDescription max 1
  - ➖ rdfs:subClassOf: heritageGraph:routeDescription min 0
  - ➖ rdfs:subClassOf: heritageGraph:routeDescription only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:routePlaces min 0
  - ➖ rdfs:subClassOf: heritageGraph:startPlace min 0
  - ➖ skos:broadMatch: crm:E7_Activity
  - ➖ skos:definition: "Intentional ritual activity that activates sacred space, invokes deities, and binds social groups"@en
- **Ritual Type** (`heritageGraph:RitualType`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E55_Type
  - ➕ skos:editorialNote: "Design note: RitualType currently mixes three orthogonal axes: worship-frequency (NityaPuja/NaimittikaPuja/KamyaPuja), ritual form (Homa/Jatra/MaskedPerformance), and lifecycle (InstallationRitual/ReturningRitual). Consider splitting into RitualFrequency + RitualForm. Also: Circumambulation/ProcessionalMovement/ProcessionRitual/RelicTour overlap with RitualEvent.hg:routePlaces/hg:startPlace/hg:endPlace/hg:routeDescription -- pick one canonical mechanism for moving rituals."@en
  - ➖ heritageGraph:design_note: "RitualType currently mixes three orthogonal axes: worship-frequency (NityaPuja/NaimittikaPuja/KamyaPuja), ritual form (Homa/Jatra/MaskedPerformance), and lifecycle (InstallationRitual/ReturningRitual). Consider splitting into RitualFrequency + RitualForm. Also: Circumambulation/ProcessionalMovement/ProcessionRitual/RelicTour overlap with RitualEvent.route_places/start_place/end_place/route_description -- pick one canonical mechanism for moving rituals."
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#Abhisheka
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#Bhajan
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#ChariotProcession
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#Circumambulation
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#DeinstallationRitual
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#Homa
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#InstallationRitual
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#Jatra
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#KamyaPuja
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#MaskedPerformance
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#NaimittikaPuja
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#NityaPuja
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#ProcessionRitual
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#ProcessionalMovement
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#RelicTour
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#ReturningRitual
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#RitualConsecration
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#Vrata
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/RitualType#Yagna
- **Role deity** (`heritageGraph:roleDeity`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariRole
- **Route description** (`heritageGraph:routeDescription`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "Text description of the procession route."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Text description of the procession route"@en
- **Route places** (`heritageGraph:routePlaces`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "Ordered list of places visited during movement ritual."@en
  - ➕ skos:relatedMatch: crm:P7_took_place_at
  - ➖ rdfs:subPropertyOf: crm:P7_took_place_at
  - ➖ skos:definition: "Ordered list of places visited during movement ritual"@en
- **Ruined** (`https://cair-nepal.org/heritagegraph/ConditionType#Ruined`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Severely damaged or collapsed."@en
  - ➖ skos:definition: "Severely damaged or collapsed"@en
- **Sana Guthi** (`https://cair-nepal.org/heritagegraph/GuthiType#SanaGuthi`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Funeral association (sanah guthi): the association that organises the funeral procession and cremation of member households; in some localities it and the si guthi are one body."@en
  - ➖ skos:definition: "Agricultural cooperative trust"@en
- **Sattal** (`heritageGraph:Sattal`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Multi-storey public rest house (e.g. the three-storey Kasthamandap) with ritual and social functions."@en
  - ➖ skos:definition: "Multi-story rest house (3-5 floors) with ritual and social functions"@en
- **Selected person** (`heritageGraph:selectedPerson`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariSelectionEvent
  - ➕ skos:definition: "Person selected through a ritual selection process to assume a sacred role or office."@en
  - ➖ skos:definition: "Person selected through a ritual selection process to assume a sacred role or office"@en
- **Selected through** (`heritageGraph:selectedThrough`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:KumariTenure
  - ➕ skos:definition: "Selection event that preceded this tenure. Not a tenure-opening event: the tenure opens with the enthronement (hg:enthronedThrough, a subproperty of hg:tenureOpenedBy)."@en
  - ➖ skos:definition: "Selection event that initiated this tenure."@en
- **Selection Criterion** (`heritageGraph:SelectionCriterion`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E55_Type
  - ➕ skos:definition: "An eligibility criterion a candidate must satisfy to assume the Kumari role. Modelled as explicit subclasses so 'what are the eligibility criteria?' is a subclass query, not free text. Ethics: candidates are children. Criteria describe the tradition; data about how a named or identifiable child met them (bodily marks, health, horoscope) must not be recorded."@en
  - ➖ skos:broadMatch: crm:E55_Type
  - ➖ skos:definition: "An eligibility criterion a candidate must satisfy to assume the Kumari role. Modelled as explicit subclasses so 'what are the eligibility criteria?' is a subclass query, not free text."@en
- **Shikhara style** (`https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Shikhara`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "North Indian spire-shaped style."@en
  - ➖ skos:definition: "North Indian spire-shaped style"@en
- **Si Guthi** (`https://cair-nepal.org/heritagegraph/GuthiType#SiGuthi`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Death guthi (si guthi): the association whose members carry out the cremation and death rites of member households."@en
  - ➖ skos:definition: "Funeral trust"@en
- **Source citation** (`heritageGraph:sourceCitation`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ schema1:domainIncludes: heritageGraph:DataSource
  - ➕ skos:definition: "Formal citation of source."@en
  - ➕ skos:relatedMatch: crm:P3_has_note
  - ➖ rdfs:range: xsd:string
  - ➖ rdfs:subPropertyOf: crm:P3_has_note
  - ➖ skos:definition: "Formal citation of source"@en
- **source creator** (`heritageGraph:sourceCreator`, object property)
  - ➕ dcterms:title: "source creator"@en
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:label: "source creator"@en
  - ➕ schema1:domainIncludes: heritageGraph:DataSource
  - ➕ skos:definition: "Person or organization primarily responsible for creating the source."@en
  - ➖ rdfs:label: "Datacite creator"@en
  - ➖ skos:definition: "Person or organization primarily responsible for creating the source"@en
- **Source url** (`heritageGraph:sourceUrl`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:DataSource
  - ➕ skos:definition: "URL or digital identifier for source."@en
  - ➖ skos:definition: "URL or digital identifier for source"@en
- **Start place** (`heritageGraph:startPlace`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:RitualEvent
  - ➕ skos:definition: "Starting location of movement ritual."@en
  - ➕ skos:relatedMatch: crm:P27_moved_from
  - ➖ skos:definition: "Starting location of movement ritual"@en
- **startedAtTime** (`prov:startedAtTime`, datatype property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "startedAtTime"
  - ➕ skos:definition: "The time at which an activity started. See also prov:endedAtTime."@en
  - ➖ rdfs:label: "Started at time"@en
  - ➖ skos:definition: "Time at which this activity started."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **starts after the end of** (`crm:P183i_starts_after_the_end_of`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "starts after the end of"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many (0,n:0,n)

Scope note of the inverse property:
This property specifies that the temporal extent of the domain instance A of E2 Temporal Entity ends definitely before the start of the temporal extent of the range instance B of E2 Temporal Entity. 
In other words, if A = [A(start), A(end)] and B = [B(start), B(end)], it means A(end) &lt; B(start) is true. 
This property is part of the set of temporal primitives P173 – P176, P182 – P185.
This property corresponds to the following Allen temporal relation (Allen, 1983) : {before}.
This property is transitive. This property is asymmetric. 


https://cidoc-crm.org/html/version_images/images_7.1.3/image_11.png


Figure 18: Temporal entity A ends before the start of temporal entity B. Here A is longer than B


https://cidoc-crm.org/html/version_images/images_7.1.3/image_12.png


Figure 19: Temporal entity A ends before the start of temporal entity B. Here A is shorter than B

Examples of the inverse property:
- Gisle taking office as Bishop of Linköping 1139 AD (E7) ends before the start of The Guta saga composition (E65). (Peel, 1999)
- Troy VII (E4) ends before the start of Troy VIII (E4). [uninhabited for some 200 years]
- The use of the Tomb Four from Nikitopoulou group in Nihoria in the MHIII-LHI period (E4) ends before the start of the period of reuse of the Tomb Four from Nikitopoulou group in LHIIIA (E4). [“Of the six tombs excavated in the Nikitopoulou group […] the finds in Tomb Four are of MH II or MH III-LH I date, with the exception of the finds with the Northern group of material, which is uniformly dated to LHIIA2, end the ewer in the middle of the floor, dated LHIIIA1. […] The preserved evidence seems clearly to indicate use in the MHIII-LHI use in the MHIII-LHI period followed by a period of reuse in LHIIIA, a pattern matched at architecturally similar sites such as 13:Kaminia and 10:Gouvalári.”] (Boyd, 2002)

In First Order Logic of the inverse property:
- P183(x,y) ⇒ E2(x)
- P183(x,y) ⇒ E2(y)
- P183(x,y) ⇒ P182(x,y)
- [P183(x,y) ∧ P183(y,z)] ⇒ P183(x,z)
- P183(x,y) ⇒ ¬P183(y,x)"@en
  - ➖ rdfs:label: "Occurs after"@en
  - ➖ skos:definition: "Points to the prerequisite ritual."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Stupa** (`heritageGraph:Stupa`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➖ owl:disjointWith: heritageGraph:Chaitya
- **Supported by institution** (`heritageGraph:supportedByInstitution`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: crm:E74_Group
  - ➕ schema1:domainIncludes: heritageGraph:KumariTenure
  - ➖ rdfs:range: heritageGraph:Guthi
- **Syncretic Relationship** (`heritageGraph:SyncreticRelationship`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E13_Attribute_Assignment
  - ➕ skos:definition: "The act of identifying one deity with another across theological frameworks (a CIDOC-CRM E13 Attribute Assignment: P140 the deity identified, P141 the deity it is identified with), recorded with the source that reports it (hg:mentionedInSource)."@en
  - ➖ rdfs:subClassOf: crm:P140_assigned_attribute_to max 1
  - ➖ rdfs:subClassOf: crm:P140_assigned_attribute_to only heritageGraph:Deity
  - ➖ rdfs:subClassOf: crm:P141_assigned only heritageGraph:Deity
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:documentedBy min 0
  - ➖ rdfs:subClassOf: heritageGraph:mentionedInSource min 0
  - ➖ rdfs:subClassOf: heritageGraph:syncreticType min 0
  - ➖ rdfs:subClassOf: prov:used min 0
  - ➖ rdfs:subClassOf: prov:used only prov:Entity
  - ➖ skos:broadMatch: crm:E13_Attribute_Assignment
  - ➖ skos:definition: "Formalizes the syncretic equivalence between divine entities across different theological frameworks. Following CIDOC CRM E13, it treats syncretism as a propositional claim with associated epistemic authority and provenance."@en
- **Syncretic Type** (`heritageGraph:SyncreticType`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: crm:E55_Type
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/SyncreticType#Appropriation
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/SyncreticType#Equivalence
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/SyncreticType#Fusion
  - ➖ linkml:permissible_values: https://cair-nepal.org/heritagegraph/SyncreticType#Historical
- **Temple** (`heritageGraph:Temple`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:broadMatch: schema1:PlaceOfWorship
  - ➕ skos:narrowMatch: schema1:HinduTemple
  - ➖ rdfs:subClassOf: heritageGraph:enshrinesDeityThroughEvent min 0
  - ➖ rdfs:subClassOf: heritageGraph:hasArchitecturalStyle min 1
  - ➖ skos:closeMatch: schema1:HinduTemple
  - ➖ skos:closeMatch: schema1:PlaceOfWorship
- **that** (`crminf:J4_that`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/extensions/crminf/
  - ➕ rdfs:label: "that"@en
  - ➕ skos:definition: "This property associates an instance of I4 Proposition Set with the instance of I2 Belief that holds an opinion about it."@en
  - ➖ rdfs:label: "Asserts proposition"@en
  - ➖ skos:definition: "Machine-readable proposition(s) this assertion holds to be true (CRMinf J4 that). Complements the free-text assertion_content."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Thirty Two Perfections Criterion** (`heritageGraph:ThirtyTwoPerfectionsCriterion`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "The battis lakshana, the traditional list of thirty-two auspicious marks a candidate is held to bear. HeritageGraph records that the criterion belongs to the selection, not any assessment of a candidate."@en
  - ➖ skos:definition: "Candidate must exhibit the battis lakshana (thirty-two perfections/auspicious bodily marks)."@en
- **Time-Span** (`crm:E52_Time-Span`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "Time-Span"@en
  - ➕ skos:definition: "Scope note:
This class comprises abstract temporal extents, in the sense of Galilean physics, having a beginning, an end, and a duration. 
Instances of E52 Time-Span have no semantic connotations about phenomena happening within the temporal extent they represent. They do not convey any meaning other than a positioning on the “time-line” of chronology. The actual extent of an instance of E52 Time-Span can be approximated by properties of E52 Time-Span giving inner and outer bounds in the form of dates (instances of E61 Time Primitive). Comparing knowledge about time-spans is fundamental for chronological reasoning.
Some instances of E52 Time-Span may be defined as the actual, in principle observable, temporal extent of instances of E2 Temporal Entity via the property P4 has time-span (is time-span of): E52 Time-Span. They constitute phenomenal time-spans as defined in CRMgeo (Doerr &amp; Hiebel 2013). Since our knowledge of history is imperfect and physical phenomena are fuzzy in nature, the extent of phenomenal time-spans can only be described in approximation. An extreme case of approximation, might, for example, define an instance of E52 Time-Span having unknown beginning, end and duration. It may, nevertheless, be associated with other descriptions by which people can infer knowledge about it, such as in relative chronologies.
Some instances of E52 may be defined precisely as representing a declaration of a temporal extent, as, for instance, done in a business contract. They constitute declarative time-spans as defined in CRMgeo (Doerr &amp; Hiebel 2013) and can be described via the property E61 Time Primitive P170 defines time (time is defined by): E52 Time-Span. 
When used as a common E52 Time-Span for two events, it will nevertheless describe them as being simultaneous, even if nothing else is known.

Examples:
- 1961
- From 12-17-1993 to 12-8-1996
- 14h30 to 16h22 4(th) July 1945
- 9.30 am 1.1.1999 to 2.00 pm 1.1.1999
- the time-span of the Ming Dynasty (Chan, 2011)

In First Order Logic:
- E52(x) ⇒ E1(x)"@en
  - ➖ rdfs:label: "Time Span"@en
  - ➖ rdfs:subClassOf: prov:Entity
  - ➖ skos:definition: "Temporal extent of an event or period"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **took place at** (`crm:P7_took_place_at`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "took place at"@en
  - ➕ skos:definition: "Quantification: many to many, necessary (1,n:0,n)

Scope note:
This property describes the spatial location of an instance of E4 Period. 
The related instance of E53 Place should be seen as a wider approximation of the geometric area within which the phenomena that characterise the period in question occurred, see below. P7 took place at (witnessed) does not convey any meaning other than spatial positioning (frequently on the surface of the earth). For example, the period “Révolution française” can be said to have taken place in “France in 1789”; the “Victorian” period may be said to have taken place in “Britain from 1837-1901” and its colonies, as well as other parts of Europe and North America. An instance of E4 Period can take place at multiple non-contiguous, non-overlapping locations.
Any place where something happened includes the spatial projection of the happening given in the same geometric reference system. For instance, HMS Victory, as place of Lord Nelson's dying, includes the location of his body relative to the hull of HMS Victory at his time of death as the most precise location of his death. By the definition of P161 has spatial projection, an instance of E4 Period takes place on all its spatial projections to respective reference systems, that is, instances of E53 Place. Therefore, this property implies the more fully developed path from E4 Period through P161 has spatial projection, E53 Place, P89 falls within to E53 Place, where both places are defined in the same geometric reference system. The relation between an instance of E53 Place and its reference system can conveniently be documented via the property P157 is at rest relative to (provides reference space for).
Something that has happened at a given place can also be considered to have happened at a smaller place within it: for example, it is reasonable to say Caesar’s murder took place in Rome, but also on the Forum Romanum, and more precisely in the Curia. It is characteristic for different historical sources to use varying precision in such statements, without being in contradiction with each other. This may be due to lack of knowledge or to the relevance of the precision for the purpose of the statement. In information integration, the more precise statement improves the overall knowledge.

Examples:
- The period “Révolution française” (E4) took place at the area covered by France in 1789 (E53). (Bertaud, 2004)

In First Order Logic:
- P7(x,y) ⇒ E4(x)
- P7(x,y) ⇒ E53(y)
- P7(x,y) ⇒ (∃z,u) [P157(y,u) ˄ P157(z,u) ˄ P161(x,z) ˄ P89(z,y)]
- [E4(x) ˄ P157(y,u) ˄ P157(v,u) ˄ P7(x,y) ˄ P161(x,z) ˄ P89(z,v) ˄ P89(v,y)] ⇒ P7(x,v)"@en
  - ➖ rdfs:label: "Took place at"@en
  - ➖ skos:definition: "Place where the event occurred"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **took place on or within** (`crm:P8_took_place_on_or_within`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "took place on or within"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property describes the location of an instance of E4 Period with respect to an instance of E18 Physical Thing. 
This property is a shortcut of the more fully developed path from E4 Period through P7 took place at, E53 Place, P156i is occupied by to E18 Physical Thing.
It describes a period that can be located with respect to the space defined by an E19 Physical Object such as a ship or a building. The precise geographical location of the object during the period in question may be unknown or unimportant. 
For example, the French and German armistice of 22(nd) June 1940 was signed in the same railway carriage as the armistice of 11(th) November 1918.

Examples:
- The coronation of Queen Elizabeth II (E7) took place on or within Westminster Abbey (E18). (Strong, 2005)

In First Order Logic:
- P8(x,y) ⇒ E4(x)
- P8(x,y) ⇒ E18(y)
- P8(x,y) ⇐ (∃z) [E53(z) ˄ P7(x,z) ˄ P156i(z,y)]"@en
  - ➖ rdfs:label: "Ritual on structure"@en
  - ➖ skos:definition: "Ritual occurs at specific temple or monument"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Traditional role** (`heritageGraph:traditionalRole`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ schema1:domainIncludes: heritageGraph:CasteGroup
  - ➕ skos:definition: "Hereditary occupation or ritual duty."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Hereditary occupation or ritual duty"@en
- **Transfer of Custody** (`crm:E10_Transfer_of_Custody`, class)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "Transfer of Custody"@en
  - ➕ skos:definition: "Scope note:
This class comprises transfers of the physical custody or the legal responsibility for the physical custody of objects. The recording of the donor or recipient is optional. It is possible that in an instance of E10 Transfer of Custody there is either no donor or no recipient. 
Depending on the circumstances, it may describe: 
1. the beginning of custody (there is no previous custodian)
2. the end of custody (there is no subsequent custodian)
3. the transfer of custody (transfer from one custodian to the next)
4. the receipt of custody from an unknown source (the previous custodian is unknown)
5. the declared loss of an object (the current or subsequent custodian is unknown)
In the event that only a single kind of transfer of custody occurs, either the legal responsibility for the custody or the actual physical possession of the object but not both, this difference should be expressed using the property 
P2 has type (is type of).
The sense of physical possession requires that the object of custody be in the hands of the keeper at least with a part representative for the whole. The way, in which a representative part is defined, should ensure that it is unambiguous who keeps a part and who the whole and should be consistent with the identity criteria of the kept instance of E18 Physical Thing.
The interpretation of the museum notion of "accession" differs between institutions. The CIDOC CRM therefore models legal ownership and physical custody separately. Institutions will then model their specific notions of accession and deaccession as combinations of these. 
Theft is a specific case of illegal transfer of custody.

Examples:
- the delivery of the paintings by Secure Deliveries Inc. to the National Gallery
- the return of Picasso’s “Guernica” to Madrid’s Prado in 1981 (Chipp, 1988)
- the transfer of custody of the work described as “Von der Velden ein Ufer an der See” from Johann Matthäus von Merian to the Auction House Heldevier (Jacob) for the purpose of sale, ca. 1716
- the transfer of custody of the painting ‘Mrs. Fitzherbert’ to the art dealer Knoedler from Parke-Bernet Galleries (New York, NY, USA) ca. March 1941

In First Order Logic:
- E10(x) ⇒ E7(x)"@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:label: "Transfer Of Custody"@en
  - ➖ rdfs:subClassOf: prov:Activity
  - ➖ skos:definition: "Event of transferring responsibility for temple maintenance, ritual performance, or artifact stewardship"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **transferred custody of** (`crm:P30_transferred_custody_of`, object property)
  - ➕ owl:inverseOf: crm:P30i_custody_transferred_through
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "transferred custody of"@en
  - ➕ skos:definition: "Quantification: many to many, necessary (1,n:0,n)

Scope note:
This property identifies the instance(s) of E18 Physical Thing concerned in an instance of E10 Transfer of Custody. 
The property will typically describe the object that is handed over by an instance of E39 Actor to the custody of another instance of E39 Actor. On occasion, physical custody may be transferred involuntarily or illegally, e.g. through accident, unsolicited donation, or theft.

Examples:
- The delivery of the paintings by Secure Deliveries Inc. to the National Gallery (E10) transferred custody of paintings from The Iveagh Bequest (E19).

In First Order Logic:
- P30(x,y) ⇒ E10(x)
- P30(x,y) ⇒ E18(y)"@en
  - ➖ rdfs:label: "Transferred object"@en
  - ➖ skos:definition: "Object transferred in custody event"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Transferred to guthi** (`heritageGraph:transferredToGuthi`, object property)
  - ➕ rdfs:domain: crm:E10_Transfer_of_Custody
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "New custodian (Guthi)."@en
  - ➖ skos:definition: "New custodian (Guthi)"@en
- **Unknown** (`https://cair-nepal.org/heritagegraph/ExistenceStatus#Unknown`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Existence status uncertain."@en
  - ➖ skos:definition: "Existence status uncertain"@en
- **used** (`prov:used`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "used"
  - ➕ skos:definition: "A prov:Entity that was used by this prov:Activity. For example, :baking prov:used :spoon, :egg, :oven ."@en
  - ➖ rdfs:label: "used"@en
  - ➖ skos:definition: "Entity used by this activity."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Used by** (`heritageGraph:usedBy`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:IconographicObject
  - ➕ skos:definition: "Actor(s) who use, handle, or are responsible for this object in ritual contexts."@en
  - ➖ skos:definition: "Actor(s) who use, handle, or are responsible for this object in ritual contexts"@en
- **Used equipment** (`heritageGraph:usedEquipment`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ schema1:domainIncludes: heritageGraph:DocumentationActivity
  - ➕ skos:definition: "Equipment used in documentation."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Equipment used in documentation"@en
- **Used method** (`heritageGraph:usedMethod`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ schema1:domainIncludes: heritageGraph:DocumentationActivity
  - ➕ skos:definition: "Documentation method used."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Documentation method used"@en
- **used object of type** (`crm:P125_used_object_of_type`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "used object of type"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property associates an instance of E7 Activity to an instance of E55 Type, which classifies an instance of E70 Thing used in an instance of E7 Activity, when the specific instance is either unknown or not of interest, such as use of “a hammer”.
This property is a shortcut of the more fully developed path from E7 Activity through P16 used specific object, E70 Thing, P2 has type, to E55 Type.

Examples:
- The English archers’ activity in the Battle of Agincourt (E7) used object of type long bow (E55). (Curry, 2015)

In First Order Logic:
- P125(x,y) ⇒ E7(x)
- P125(x,y) ⇒ E55(y)
- P125(x,y) ⇔ (∃z) [E70(z) ∧ P16(x,z) ∧ P2(z,y)]"@en
  - ➖ rdfs:label: "Used materials"@en
  - ➖ skos:definition: "Ephemeral materials consumed during the ritual (e.g., oil, rice)."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **used specific object** (`crm:P16_used_specific_object`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "used specific object"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property describes the use of material or immaterial things in a way essential to the performance or the outcome of an instance of E7 Activity. 
This property typically applies to tools, instruments, moulds, raw materials and items embedded in a product. It implies that the presence of the object in question was a necessary condition for the action. For example, the activity of writing this text required the use of a computer. An immaterial thing can be used if at least one of its carriers is present. For example, the software tools on a computer.
Another example is the use of a particular name by a particular group of people over some span to identify a thing, such as a settlement. In this case, the physical carriers of this name are at least the people understanding its use.

Examples:
- The writing of the scope note of the CIDOC CRM property “P16 used specific object” contained in the CIDOC CRM version 4.1 (E7) used specific object Nicholas Crofts’ computer (E22) mode of use Typing Tool; Storage Medium (E55). [the original scope note was later extended in the CIDOC CRM version 4.3] 
- The people of Iraq calling the place identified by TGN ‘7017998’ (E7) used specific object “Quyunjig” (E41) mode of use current; vernacular (E55).

Properties:
- P16.1 mode of use: E55 Type

In First Order Logic:
- P16(x,y) ⇒ E7(x)
- P16(x,y) ⇒ E70(y)
- P16(x,y) ⇒ P12(x,y)
- P16(x,y) ⇒ P15(x,y)
- P16(x,y,z) ⇒ [P16(x,y) ∧ E55(z)]"@en
  - ➖ rdfs:label: "Consecrated object"@en
  - ➖ skos:definition: "Murti employed in (and transformed by) the consecration ritual"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **used specific technique** (`crm:P33_used_specific_technique`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "used specific technique"@en
  - ➕ skos:definition: "Quantification: many to many (0,n:0,n)

Scope note:
This property identifies a specific instance of E29 Design or Procedure in order to carry out an instance of E7 Activity or parts of it. 
The property differs from P32 used general technique (was technique of) in that P33 refers to an instance of E29 Design or Procedure, which is a concrete information object in its own right rather than simply being a term or a method known by tradition. 
Typical examples would include intervention plans for conservation or the construction plans of a building.

Examples:
- The ornamentation of silver cup 232 (E11) used specific technique ‘Instructions for golden chase work by A N Other’ (E29). (fictitious)
- The rebuilding of the German Reichstag in Berlin (E11) used specific technique Architectural plans by Foster and Partners (E29). (Foster, 2000)

In First Order Logic:
- P33(x,y) ⇒ E7(x)
- P33(x,y) ⇒ E29(y)
- P33(x,y) ⇒ P16(x,y)"@en
  - ➖ rdfs:label: "Used technique"@en
  - ➖ skos:definition: "Craft technique used in production"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **value** (`prov:value`, datatype property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "value"
  - ➕ skos:definition: "Provides a value that is a direct representation of an entity."@en
  - ➖ rdfs:label: "Assertion content"@en
  - ➖ skos:definition: "The factual claim being asserted"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Verification** (`heritageGraph:Verification`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:subClassOf: heritageGraph:verificationMethod only rdf:PlainLiteral
  - ➕ skos:definition: "Process of cross-checking heritage claims against multiple sources."@en
  - ➕ skos:editorialNote: "PROV-O alignment note: prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."@en
  - ➖ heritageGraph:prov_alignment_note: "prov:Activity alignment is a HeritageGraph project-level assertion (not a normative CIDOC axiom; no official CRM<->PROV mapping exists). Asserted on this class, not on crm:E7_Activity globally."
  - ➖ rdfs:subClassOf: crm:P3_has_note max 1
  - ➖ rdfs:subClassOf: crm:P3_has_note min 0
  - ➖ rdfs:subClassOf: crm:P3_has_note only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:verificationMethod max 1
  - ➖ rdfs:subClassOf: heritageGraph:verificationMethod min 0
  - ➖ rdfs:subClassOf: heritageGraph:verificationMethod only xsd:string
  - ➖ rdfs:subClassOf: heritageGraph:verifiedAssertion min 0
  - ➖ rdfs:subClassOf: heritageGraph:verifiedByExpert min 0
  - ➖ skos:definition: "Process of cross-checking heritage claims against multiple sources"@en
- **Verification method** (`heritageGraph:verificationMethod`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ rdfs:range: rdf:PlainLiteral
  - ➕ schema1:domainIncludes: heritageGraph:Verification
  - ➕ skos:definition: "Method used for verification (cross-check, expert review, field visit)."@en
  - ➖ rdfs:range: xsd:string
  - ➖ skos:definition: "Method used for verification (cross-check, expert review, field visit)"@en
- **Verified assertion** (`heritageGraph:verifiedAssertion`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Verification
  - ➕ skos:definition: "Assertions verified by this activity."@en
  - ➖ skos:definition: "Assertions verified by this activity"@en
- **Verified by expert** (`heritageGraph:verifiedByExpert`, object property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:Verification
  - ➕ skos:definition: "Expert who performed verification."@en
  - ➖ skos:definition: "Expert who performed verification"@en
- **Vrata** (`https://cair-nepal.org/heritagegraph/RitualType#Vrata`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Vow observance ritual."@en
  - ➖ skos:definition: "Vow observance ritual"@en
- **was assessed by** (`crm:P34i_was_assessed_by`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "was assessed by"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many, necessary (1,n:0,n)

Scope note of the inverse property:
This property identifies the instance of E18 Physical Thing that was assessed during an instance of E14 Condition Assessment. 
Conditions may be assessed either by direct observation or using recorded evidence. In the latter case the instance of E18 Physical Thing does not need to be present or extant at the time of assessment.

Examples of the inverse property:
- The condition assessment of the silver collection in 1997 (E14) concerned silver cup 232 (E22). (fictitious)
- The condition assessment of the cover of MS Sinai Greek 418 (E14) concerned the cover of MS Sinai Greek 418 (E22). (Honey and Pickwoad, 2010)
- The condition assessment of the endband cores of MS Sinai Greek 418 (E14) concerned the endband cores of MS Sinai Greek 418 (E22). (Honey and Pickwoad, 2010)

In First Order Logic of the inverse property:
- P34(x,y) ⇒ E14(x)
- P34(x,y) ⇒ E18(y) 
- P34(x,y) ⇒ P140(x,y)"@en
  - ➖ rdfs:label: "Has condition assessment"@en
  - ➖ skos:definition: "Condition assessment events for this structure"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Was documented by** (`heritageGraph:documentedBy`, object property)
  - ➕ rdfs:domain: heritageGraph:AssertionSubject
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:closeMatch: crmsci:O8i_was_observed_by
  - ➕ skos:definition: "Documentation event that recorded this (pre-existing) entity or event. Uses hg:documentedBy (aligned to prov:wasInfluencedBy). NOTE: prov:wasGeneratedBy was incorrect: a stupa is not *generated by* the survey that records it."@en
  - ➕ skos:editorialNote: "PROV-O alignment: prov:wasInfluencedBy"@en
  - ➖ heritageGraph:prov_alignment: "prov:wasInfluencedBy"
  - ➖ skos:definition: "Documentation event that recorded this (pre-existing) entity or event. Uses heritageGraph:documentedBy (aligned to prov:wasInfluencedBy). NOTE: prov:wasGeneratedBy was incorrect: a stupa is not *generated by* the survey that records it."@en
- **was present at** (`crm:P12i_was_present_at`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "was present at"@en
  - ➕ skos:definition: "Quantification of the inverse property: many to many, necessary (1,n:0,n)

Scope note of the inverse property:
This property describes the active or passive presence of an E77 Persistent Item in an instance of E5 Event without implying any specific role. 
It documents known events in which an instance of E77 Persistent Item was present during the course of its life or history. For example, an object may be the desk, now in a museum, on which a treaty was signed. The instance of E53 Place and the instance of E52 Time-Span where and when these events happened provide constraints about the presence of the related instance E77 Persistent Item in the past. Instances of E90 Symbolic Object, in particular information objects, are physically present in events via at least one of the instances of E18 Physical Thing carrying them. Note, that the human mind can be such a carrier. A precondition for a transfer of information to a person or another new physical carrier is the presence of the respective information object and this person or physical thing in one event.

Examples of the inverse property:
- Deckchair 42 (E19) was present at the sinking of the Titanic (E5). (Aldridge, 2008)

In First Order Logic of the inverse property:
- P12(x,y) ⇒ E5(x)
- P12(x,y) ⇒ E77(y)"@en
  - ➖ rdfs:label: "Was present at"@en
  - ➖ skos:definition: "Generic CRM presence relation (P12i): event this entity was present at. Canonical holder of the CRM predicate; use the specific slots in data."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **was produced by** (`crm:P108i_was_produced_by`, object property)
  - ➕ rdfs:isDefinedBy: http://www.cidoc-crm.org/cidoc-crm/
  - ➕ rdfs:label: "was produced by"@en
  - ➕ skos:definition: "Quantification of the inverse property: one to many, necessary, dependent (1,n:1,1)

Scope note of the inverse property:
This property identifies the instance of E24 Physical Human-Made Thing that came into existence as a result of the instance of E12 Production.
The identity of an instance of E24 Physical Human-Made Thing is not defined by its matter, but by its existence as a subject of documentation. An E12 Production can result in the creation of multiple instances of E24 Physical Human-Made Thing.

Examples of the inverse property:
- The building of Rome (E12) has produced the Colosseum (E24). (Hopkins &amp; Beard, 2011)

In First Order Logic of the inverse property:
- P108(x,y) ⇒ E12(x)
- P108(x,y) ⇒ E24(y)
- P108(x,y) ⇒ P31(x,y)
- P108(x,y) ⇒ P92(x,y)"@en
  - ➖ rdfs:label: "Was produced by event"@en
  - ➖ skos:definition: "Event that created this object or structure"@en
  - ➖ skos:inScheme: heritageGraph:schema
- **wasAssociatedWith** (`prov:wasAssociatedWith`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "wasAssociatedWith"
  - ➕ skos:definition: "An prov:Agent that had some (unspecified) responsibility for the occurrence of this prov:Activity."@en
  - ➖ rdfs:label: "Was associated with"@en
  - ➖ skos:definition: "Agent associated with responsibility for this activity."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **wasAttributedTo** (`prov:wasAttributedTo`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "wasAttributedTo"
  - ➕ skos:definition: "Attribution is the ascribing of an entity to an agent."@en
  - ➖ rdfs:label: "Was attributed to"@en
  - ➖ skos:definition: "Agent to whom responsibility for this entity is attributed."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **wasDerivedFrom** (`prov:wasDerivedFrom`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "wasDerivedFrom"
  - ➕ skos:definition: "A derivation is a transformation of an entity into another, an update of an entity resulting in a new one, or the construction of a new entity based on a pre-existing entity."@en
  - ➖ rdfs:label: "Was derived from"@en
  - ➖ skos:definition: "Entity from which this entity was derived."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **wasGeneratedBy** (`prov:wasGeneratedBy`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "wasGeneratedBy"
  - ➖ rdfs:label: "Was generated by"@en
  - ➖ skos:definition: "Activity that generated this entity."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **wasInfluencedBy** (`prov:wasInfluencedBy`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "wasInfluencedBy"
  - ➕ skos:definition: "Because prov:wasInfluencedBy is a broad relation, its more specific subproperties (e.g. prov:wasInformedBy, prov:actedOnBehalfOf, prov:wasEndedBy, etc.) should be used when applicable."@en
  - ➖ rdfs:label: "Was influenced by"@en
  - ➖ skos:definition: "General PROV-O influence relation. Prefer a more specific PROV relation whenever one applies."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **wasInformedBy** (`prov:wasInformedBy`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "wasInformedBy"
  - ➕ skos:definition: "An activity a2 is dependent on or informed by another activity a1, by way of some unspecified entity that is generated by a1 and used by a2."@en
  - ➖ rdfs:label: "Was informed by"@en
  - ➖ skos:definition: "Activity that informed this activity; PROV-O uses this when the intervening generated and used entity is unknown or omitted."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **wasRevisionOf** (`prov:wasRevisionOf`, object property)
  - ➕ rdfs:isDefinedBy: http://www.w3.org/ns/prov-o#
  - ➕ rdfs:label: "wasRevisionOf"
  - ➕ skos:definition: "A revision is a derivation that revises an entity into a revised version."@en
  - ➖ rdfs:label: "Supersedes assertion"@en
  - ➖ skos:definition: "Previous assertion that this one revises (version chain A1->A2->A3). Uses prov:wasRevisionOf (a derivation between entities); the latest assertion is the one with no incoming wasRevisionOf. NOTE: prov:invalidated was incorrect here (it is an Activity->Entity relation, not Entity->Entity)."@en
  - ➖ skos:inScheme: heritageGraph:schema
- **Water Structure** (`heritageGraph:WaterStructure`, class)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Engineered water supply systems with ritual and civic significance."@en
  - ➖ skos:definition: "Engineered water supply systems with ritual and civic significance"@en
- **Yagna** (`https://cair-nepal.org/heritagegraph/RitualType#Yagna`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Vedic sacrifice ritual."@en
  - ➖ skos:definition: "Vedic sacrifice ritual"@en
- **Year** (`https://cair-nepal.org/heritagegraph/DatePrecision#Year`, concept)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ skos:definition: "Year-level precision only."@en
  - ➖ skos:definition: "Year-level precision only"@en
- **Year offset from gregorian** (`heritageGraph:yearOffsetFromGregorian`, datatype property)
  - ➕ rdfs:isDefinedBy: heritageGraph:ontology
  - ➕ schema1:domainIncludes: heritageGraph:CalendarSystem
  - ➕ skos:definition: "Number of years this calendar runs ahead of the Gregorian (Common Era) year at the start of its year (e.g. 57 for Bikram Sambat, -879 for Nepal Sambat). Because the calendar's new year does not fall on 1 January (see hg:epochDateGregorian), a year-precision date Y converts to the two-year interval [Y - offset, Y - offset + 1] CE; the single year Y - offset is correct only for dates between the calendar's new year and 31 December. A calendar whose new year is 1 January converts to Y - offset exactly."@en
  - ➖ skos:definition: "Mathematical offset to convert to Common Era (e.g., +57 for BS)."@en
