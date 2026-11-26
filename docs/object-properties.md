# Object properties

### Access Rights

**IRI:** `http://purl.org/dc/terms/accessRights` · `dcterms:accessRights`

Information about who access the resource or an indication of its security status.

| | |
|---|---|
| Sub-properties | [has access protocol](object-properties.md#accessprotocol) |

### actedOnBehalfOf

**IRI:** `http://www.w3.org/ns/prov#actedOnBehalfOf` · `prov:actedOnBehalfOf`

An object property to express the accountability of an agent towards another agent. The subordinate agent acted on behalf of the responsible agent in an actual activity.

### Architectural structures

**IRI:** `https://cair-nepal.org/heritagegraph/architecturalStructures` · `hg:architecturalStructures`

Heritage structures affected by or present during this historical event.

| | |
|---|---|
| Super-properties | [occurred in the presence of](object-properties.md#p12_occurred_in_the_presence_of) |
| Domain | [Destruction](classes.md#e6_destruction) *or* [Historical Event](classes.md#historicalevent) |
| Range | [Architectural Structure](classes.md#architecturalstructure) |
| Used in | used in axioms of [Historical Event](classes.md#historicalevent) |

### Asserts about

**IRI:** `https://cair-nepal.org/heritagegraph/assertsAbout` · `hg:assertsAbout`

Heritage entity or event that is the subject of this assertion.

| | |
|---|---|
| Domain | [Belief](classes.md#i2_belief) |
| Range | [Assertion Subject](classes.md#assertionsubject) |
| Inverse of | [Has assertion](object-properties.md#hasassertion) |

### Assesses candidate

**IRI:** `https://cair-nepal.org/heritagegraph/assessesCandidate` · `hg:assessesCandidate`

Candidate being assessed.

| | |
|---|---|
| Domain | [Ritual Assessment](classes.md#ritualassessment) |
| Range | [Person](classes.md#e21_person) |
| Used in | used in axioms of [Ritual Assessment](classes.md#ritualassessment) |
| domainIncludes | hg:RitualAssessment |

### assigned

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P141_assigned` · `crm:P141_assigned`

Quantification: many to many (0,n:0,n)

Scope note:
This property associates an instance of E13 Attribute Assignment with the instance of E1 CRM Entity used in the attribution. The instance of E1 CRM Entity here plays the role of the range of the attribution.
The kind of attribution made should be documented using P177 assigned property of type (is type of property assigned).

Examples:
- The Current Ownership Assessment of Martin Doerr’s silver cup February 1997 (E13) assigned Martin Doerr (E21). (fictitious)
- The Identifier Assignment on 1(st) June 1997 of the silver cup donated by Martin Doerr (E15) assigned 232 (E42). (fictitious)
- The examination of MS Sinai Greek 418 (E13) assigned unsupported (E55.) (Honey &amp; Pickwoad, 2010)

In First Order Logic:
- P141(x,y) ⇒ E13(x)
- P141(x,y) ⇒ E1(y)

| | |
|---|---|
| Used in | used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### assigned attribute to

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P140_assigned_attribute_to` · `crm:P140_assigned_attribute_to`

Quantification: many to many (0,n:0,n)

Scope note:
This property associates an instance of E13 Attribute Assignment with the instance of E1 CRM Entity about which it made an attribution. The instance of E1 CRM Entity plays the role of the domain of the attribution. 
The kind of attribution made should be documented using P177 assigned property of type (is type of property assigned).

Examples:
- The Current Ownership Assessment of Martin Doerr’s silver cup February 1997 (E13) assigned attribute to Martin Doerr’s silver cup (E22). (fictitious)
- The Identifier Assignment on 1(st) June 1997 of the silver cup donated by Martin Doerr (E15) assigned attribute to silver cup 232 (E22). (fictitious)
- The examination of MS Sinai Greek 418 (E13) assigned attribute to MS Sinai Greek 418 (E22). (Honey and Pickwoad, 2010)

In First Order Logic:
- P140(x,y) ⇒ E13(x)
- P140(x,y) ⇒ E1(y)

| | |
|---|---|
| Used in | used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### Assumes role

**IRI:** `https://cair-nepal.org/heritagegraph/assumesRole` · `hg:assumesRole`

KumariRole held during this tenure.

| | |
|---|---|
| Super-properties | [Tenure office](object-properties.md#tenureoffice) |
| Domain | [Kumari Tenure](classes.md#kumaritenure) |
| Range | [Kumari Role](classes.md#kumarirole) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |
| domainIncludes | hg:KumariTenure |

### Birth timespan

**IRI:** `https://cair-nepal.org/heritagegraph/birthTimespan` · `hg:birthTimespan`

Person's birth timespan (shortcut for crm:P98i_was_born / crm:P4_has_time-span).

| | |
|---|---|
| Domain | [Person](classes.md#e21_person) |
| Range | [Time-Span](classes.md#e52_time-span) |
| Property chain | [was born](object-properties.md#p98i_was_born) *o* [has time-span](object-properties.md#p4_has_time-span) |

### Bounds tenure

**IRI:** `https://cair-nepal.org/heritagegraph/boundsTenure` · `hg:boundsTenure`

The KumariTenure period that this lifecycle event bounds (initiates or terminates). Specialized by hg:initiatedTenure (selection) and hg:endedTenureOf (retirement).

| | |
|---|---|
| Sub-properties | [Ended tenure of](object-properties.md#endedtenureof), [Initiated tenure](object-properties.md#initiatedtenure) |
| Domain | [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |
| Range | [Kumari Tenure](classes.md#kumaritenure) |
| Used in | used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |
| domainIncludes | hg:KumariLifecycleEvent |

### carried out by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P14_carried_out_by` · `crm:P14_carried_out_by`

Quantification: many to many, necessary (1,n:0,n)

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
- P14(x,y,z) ⇒ [P14(x,y) ∧ E55(z)]

| | |
|---|---|
| Sub-properties | [Performed by group](object-properties.md#performedbygroup), [Verified by expert](object-properties.md#verifiedbyexpert) |
| Inverse of | [performed](object-properties.md#p14i_performed) |

### Commissioned by

**IRI:** `https://cair-nepal.org/heritagegraph/commissionedBy` · `hg:commissionedBy`

Person or group who commissioned production.

| | |
|---|---|
| Domain | [Production](classes.md#e12_production) |
| Range | [Actor](classes.md#e39_actor) |

### concerned

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P34_concerned` · `crm:P34_concerned`

Quantification: many to many, necessary (1,n:0,n)

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
- P34(x,y) ⇒ P140(x,y)

| | |
|---|---|
| Inverse of | [was assessed by](object-properties.md#p34i_was_assessed_by) |

### Concerns endowment

**IRI:** `https://cair-nepal.org/heritagegraph/concernsEndowment` · `hg:concernsEndowment`

Endowment founded, augmented, nationalised or alienated by this event.

| | |
|---|---|
| Domain | [Endowment Event](classes.md#endowmentevent) |
| Range | [Endowment](classes.md#endowment) |
| Used in | used in axioms of [Endowment Event](classes.md#endowmentevent) |
| domainIncludes | hg:EndowmentEvent |

### Confers role

**IRI:** `https://cair-nepal.org/heritagegraph/confersRole` · `hg:confersRole`

KumariRole conferred by this selection or enthronement event.

| | |
|---|---|
| Domain | [Kumari Enthronement Event](classes.md#kumarienthronementevent); [Kumari Selection Event](classes.md#kumariselectionevent) |
| Range | [Kumari Role](classes.md#kumarirole) |
| Used in | used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |
| domainIncludes | hg:KumariEnthronementEvent; hg:KumariSelectionEvent |

### Confidence method

**IRI:** `https://cair-nepal.org/heritagegraph/confidenceMethod` · `hg:confidenceMethod`

The documented procedure (crm:E29 Design or Procedure) by which the confidence score was assigned, described once (e.g. an expert 5-point scale mapped to 0-1, agreement between independent sources, or coding of the source's hedging: 0.9 stated plainly, 0.7 mild hedging, 0.5 explicitly uncertain, 0.3 disputed by the author).

| | |
|---|---|
| Domain | [Belief](classes.md#i2_belief) |
| Range | [Design or Procedure](classes.md#e29_design_or_procedure) |

### Consecrated by event

**IRI:** `https://cair-nepal.org/heritagegraph/consecratedByEvent` · `hg:consecratedByEvent`

Consecration event that activated this murti.

| | |
|---|---|
| Domain | [Murti](classes.md#murti) |
| Range | [Consecration](classes.md#consecration) |
| Used in | used in axioms of [Murti](classes.md#murti) |
| domainIncludes | hg:Murti |

### consists of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P9_consists_of` · `crm:P9_consists_of`

Quantification: many to many (0,n:0,n)

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
- P9(x,y) ⇒ ¬P9(y,x)

| | |
|---|---|
| Inverse of | [forms part of](object-properties.md#p9i_forms_part_of) |

### Custody closed by

**IRI:** `https://cair-nepal.org/heritagegraph/custodyClosedBy` · `hg:custodyClosedBy`

Transfer of custody that ended the period.

| | |
|---|---|
| Super-properties | [Tenure closed by](object-properties.md#tenureclosedby) |
| Domain | [Custody Period](classes.md#custodyperiod) |
| Range | [Transfer of Custody](classes.md#e10_transfer_of_custody) |
| Used in | used in axioms of [Custody Period](classes.md#custodyperiod) |
| domainIncludes | hg:CustodyPeriod |

### Custody holder

**IRI:** `https://cair-nepal.org/heritagegraph/custodyHolder` · `hg:custodyHolder`

Actor (typically a Guthi) holding custody during the period.

| | |
|---|---|
| Super-properties | [Tenure holder](object-properties.md#tenureholder) |
| Domain | [Custody Period](classes.md#custodyperiod) |
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Custody Period](classes.md#custodyperiod) |
| domainIncludes | hg:CustodyPeriod |

### Custody object

**IRI:** `https://cair-nepal.org/heritagegraph/custodyObject` · `hg:custodyObject`

Structure or object in custody during the period (any heritage structure, element or human-made object, e.g. a museum object).

| | |
|---|---|
| Domain | [Custody Period](classes.md#custodyperiod) |
| Range | ([Physical Heritage Thing](classes.md#physicalheritagething) *or* [Human-Made Object](classes.md#e22_human-made_object)) *and* [Assertion Subject](classes.md#assertionsubject) |
| Used in | used in axioms of [Custody Period](classes.md#custodyperiod) |
| domainIncludes | hg:CustodyPeriod |

### Custody opened by

**IRI:** `https://cair-nepal.org/heritagegraph/custodyOpenedBy` · `hg:custodyOpenedBy`

Transfer of custody that began the period.

| | |
|---|---|
| Super-properties | [Tenure opened by](object-properties.md#tenureopenedby) |
| Domain | [Custody Period](classes.md#custodyperiod) |
| Range | [Transfer of Custody](classes.md#e10_transfer_of_custody) |
| Used in | used in axioms of [Custody Period](classes.md#custodyperiod) |
| domainIncludes | hg:CustodyPeriod |

### custody received by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P29_custody_received_by` · `crm:P29_custody_received_by`

Quantification: many to many (0,n:0,n)

Scope note:
This property identifies the instance(s) of E39 Actor who receive custody of an instance of E18 Physical Thing in an instance of E10 Transfer of Custody. 
The property will typically describe Actors receiving custody of an object when it is handed over from another Actor’s care. On occasion, physical custody may be received involuntarily or illegally, e.g. through accident, unsolicited donation, or theft.
In reality, custody is either transferred to someone or from someone, or both.

Examples:
- Representatives of The National Gallery (E74) received custody through the delivery of the paintings by Secure Deliveries Inc. to the National Gallery (E10).

In First Order Logic:
- P29(x,y) ⇒ E10(x)
- P29(x,y) ⇒ E39(y) 
- P29(x,y) ⇒ P14(x,y)

| | |
|---|---|
| Sub-properties | [Transferred to guthi](object-properties.md#transferredtoguthi) |

### custody surrendered by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P28_custody_surrendered_by` · `crm:P28_custody_surrendered_by`

Quantification: many to many (0,n:0,n)

Scope note:
This property identifies the instance(s) of E39 Actor who surrender custody of an instance of E18 Physical Thing in an instance of E10 Transfer of Custody. 
The property will typically describe an Actor surrendering custody of an object when it is handed over to someone else’s care. On occasion, physical custody may be surrendered involuntarily, e.g. through accident, loss, or theft.
In reality, custody is either transferred to someone or from someone, or both.

Examples:
- The Secure Deliveries Inc. crew (E74) surrendered custody through the delivery of the paintings by Secure Deliveries Inc. to the National Gallery (E10).

In First Order Logic:
- P28(x,y) ⇒ E10(x)
- P28(x,y) ⇒ E39(y) 
- P28(x,y) ⇒ P14(x,y)

### custody transferred through

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P30i_custody_transferred_through` · `crm:P30i_custody_transferred_through`

Quantification of the inverse property: many to many, necessary (1,n:0,n)

Scope note of the inverse property:
This property identifies the instance(s) of E18 Physical Thing concerned in an instance of E10 Transfer of Custody. 
The property will typically describe the object that is handed over by an instance of E39 Actor to the custody of another instance of E39 Actor. On occasion, physical custody may be transferred involuntarily or illegally, e.g. through accident, unsolicited donation, or theft.

Examples of the inverse property:
- The delivery of the paintings by Secure Deliveries Inc. to the National Gallery (E10) transferred custody of paintings from The Iveagh Bequest (E19).

In First Order Logic of the inverse property:
- P30(x,y) ⇒ E10(x)
- P30(x,y) ⇒ E18(y)

| | |
|---|---|
| Inverse of | [transferred custody of](object-properties.md#p30_transferred_custody_of) |

### Datacite publisher

**IRI:** `https://cair-nepal.org/heritagegraph/sourcePublisher` · `hg:sourcePublisher`

Entity responsible for making the source available.

| | |
|---|---|
| Domain | [Data Source](classes.md#datasource) |
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |
| domainIncludes | hg:DataSource |

### Death timespan

**IRI:** `https://cair-nepal.org/heritagegraph/deathTimespan` · `hg:deathTimespan`

Person's death timespan (shortcut for crm:P100i_died_in / crm:P4_has_time-span).

| | |
|---|---|
| Domain | [Person](classes.md#e21_person) |
| Range | [Time-Span](classes.md#e52_time-span) |
| Property chain | [died in](object-properties.md#p100i_died_in) *o* [has time-span](object-properties.md#p4_has_time-span) |

### depicts

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P62_depicts` · `crm:P62_depicts`

Quantification: many to many (0,n:0,n)

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
- P62(x,y) ⇐ (∃z) [E36(z) ˄ P65(x,z) ˄ P138(z,y)]

| | |
|---|---|
| Sub-properties | [Is about deity](object-properties.md#isaboutdeity) |
| Inverse of | [is depicted by](object-properties.md#p62i_is_depicted_by) |

### destroyed

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P13_destroyed` · `crm:P13_destroyed`

Quantification: one to many, necessary (1,n:0,1)

Scope note:
This property links an instance of E6 Destruction to an instance of E18 Physical Thing that has been destroyed by it. 
Destruction implies the end of an item’s life as a subject of cultural documentation – the physical matter of which the item was composed may in fact continue to exist. An instance of E6 Destruction may be contiguous with an instance of E12 Production that brings into existence a derived object composed partly of matter from the destroyed object.

Examples:
- The Tay Bridge Disaster (E6) destroyed the Tay Bridge (E22). (Thomas, 1972)

In First Order Logic:
- P13(x,y) ⇒ E6 (x)
- P13(x,y) ⇒ E18(y) 
- P13(x,y) ⇒ P93(x,y)

| | |
|---|---|
| Inverse of | [has destruction event](object-properties.md#destructionevent) |

### died in

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P100i_died_in` · `crm:P100i_died_in`

Quantification of the inverse property: one to many, necessary (1,n:0,1)

Scope note of the inverse property:
This property links an instance of E69 Death to the instance of E21 Person that died.
An instance of E69 Death may involve multiple people, for example in the case of a battle or disaster.
This is not intended for use with general natural history material, only people.

Examples of the inverse property:
- Mozart’s death (E69) was death of Mozart (E21). (Sitwell, 2017)

In First Order Logic of the inverse property:
- P100(x,y) ⇒ E69(x)
- P100(x,y) ⇒ E21(y)
- P100(x,y) ⇒ P93(x,y)

### Documented in source

**IRI:** `https://cair-nepal.org/heritagegraph/mentionedInSource` · `hg:mentionedInSource`

Source(s) that mention/document this entity: the normative way to cite a source for a description of a heritage thing, event, actor or relationship. Distinct from prov:wasDerivedFrom, which is used only on assertions (I2 Belief) with prov:wasAttributedTo for the claimant. A source's own bibliographic data uses hg:sourceCitation, hg:sourceCreator, hg:sourceUrl and hg:persistentIdentifier. Entity-mention is not logical derivation.

| | |
|---|---|
| Domain | [Syncretic Relationship](classes.md#syncreticrelationship); [Architectural Structure](classes.md#architecturalstructure) |
| Range | [Data Source](classes.md#datasource) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |
| domainIncludes | hg:SyncreticRelationship; hg:ArchitecturalStructure |

### Duty for

**IRI:** `https://cair-nepal.org/heritagegraph/dutyFor` · `hg:dutyFor`

Ritual or festival the hereditary duty serves.

| | |
|---|---|
| Domain | [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| Range | [Ritual Event](classes.md#ritualevent) |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| domainIncludes | hg:HereditaryRoleTenure |

### Embodied deity

**IRI:** `https://cair-nepal.org/heritagegraph/embodiedDeity` · `hg:embodiedDeity`

Deity role embodied by participant.

| | |
|---|---|
| Domain | [Kumari Tenure](classes.md#kumaritenure) |
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |
| domainIncludes | hg:KumariTenure |

### End place

**IRI:** `https://cair-nepal.org/heritagegraph/endPlace` · `hg:endPlace`

Ending location of movement ritual.

| | |
|---|---|
| Domain | [Ritual Event](classes.md#ritualevent) |
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent |

### Ended tenure of

**IRI:** `https://cair-nepal.org/heritagegraph/endedTenureOf` · `hg:endedTenureOf`

Points from a KumariRetirementEvent to the tenure that it terminated. Enables reconstruction of the complete Kumari lifecycle.

| | |
|---|---|
| Super-properties | [Bounds tenure](object-properties.md#boundstenure) |
| Domain | [Kumari Retirement Event](classes.md#kumariretirementevent) |
| Range | [Kumari Tenure](classes.md#kumaritenure) |
| Inverse of | [Retired through](object-properties.md#retiredthrough) |
| Used in | used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent) |
| domainIncludes | hg:KumariRetirementEvent |

### Endowed land

**IRI:** `https://cair-nepal.org/heritagegraph/endowedLand` · `hg:endowedLand`

Land (plots, fields) dedicated to the endowment.

| | |
|---|---|
| Domain | [Endowment](classes.md#endowment) |
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Endowment](classes.md#endowment) |
| domainIncludes | hg:Endowment |

### Endowment donor

**IRI:** `https://cair-nepal.org/heritagegraph/endowmentDonor` · `hg:endowmentDonor`

Person or group who gave the property (the donor in a founding or augmentation).

| | |
|---|---|
| Super-properties | [transferred title from](object-properties.md#p23_transferred_title_from) |
| Domain | [Endowment Event](classes.md#endowmentevent) |
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Endowment Event](classes.md#endowmentevent) |
| domainIncludes | hg:EndowmentEvent |

### Endowment recipient

**IRI:** `https://cair-nepal.org/heritagegraph/endowmentRecipient` · `hg:endowmentRecipient`

Guthi or state body that received the property (e.g. the Guthi Sansthan in a nationalisation).

| | |
|---|---|
| Super-properties | [transferred title to](object-properties.md#p22_transferred_title_to) |
| Domain | [Endowment Event](classes.md#endowmentevent) |
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Endowment Event](classes.md#endowmentevent) |
| domainIncludes | hg:EndowmentEvent |

### ends before the start of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P183_ends_before_the_start_of` · `crm:P183_ends_before_the_start_of`

Quantification: many to many (0,n:0,n)

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
- P183(x,y) ⇒ ¬P183(y,x)

| | |
|---|---|
| Inverse of | [starts after the end of](object-properties.md#p183i_starts_after_the_end_of) |

### Enshrined deity

**IRI:** `https://cair-nepal.org/heritagegraph/enshrinedDeity` · `hg:enshrinedDeity`

Deity installed through enshrinement.

| | |
|---|---|
| Super-properties | [occurred in the presence of](object-properties.md#p12_occurred_in_the_presence_of) |
| Domain | [Enshrinement](classes.md#enshrinement) |
| Range | [Deity](classes.md#deity) |
| Inverse of | [Is enshrined through event](object-properties.md#isenshrinedthroughevent) |
| Used in | used in axioms of [Enshrinement](classes.md#enshrinement) |
| domainIncludes | hg:Enshrinement |

### Enshrined in structure

**IRI:** `https://cair-nepal.org/heritagegraph/enshrinedInStructure` · `hg:enshrinedInStructure`

Temple where deity was enshrined.

| | |
|---|---|
| Super-properties | [took place on or within](object-properties.md#p8_took_place_on_or_within) |
| Domain | [Enshrinement](classes.md#enshrinement) |
| Range | [Temple](classes.md#temple) |
| Inverse of | [Enshrines deity through event](object-properties.md#enshrinesdeitythroughevent) |
| Used in | used in axioms of [Enshrinement](classes.md#enshrinement) |
| domainIncludes | hg:Enshrinement |

### Enshrines deity through event

**IRI:** `https://cair-nepal.org/heritagegraph/enshrinesDeityThroughEvent` · `hg:enshrinesDeityThroughEvent`

Enshrinement event that installed deity in temple.

| | |
|---|---|
| Domain | [Temple](classes.md#temple) |
| Range | [Enshrinement](classes.md#enshrinement) |
| Inverse of | [Enshrined in structure](object-properties.md#enshrinedinstructure) |
| Used in | used in axioms of [Temple](classes.md#temple) |
| domainIncludes | hg:Temple |

### Enthroned person

**IRI:** `https://cair-nepal.org/heritagegraph/enthronedPerson` · `hg:enthronedPerson`

Girl enthroned as Kumari by this enthronement event.

| | |
|---|---|
| Domain | [Kumari Enthronement Event](classes.md#kumarienthronementevent) |
| Range | [Person](classes.md#e21_person) |
| Used in | used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent) |
| domainIncludes | hg:KumariEnthronementEvent |

### Enthroned through

**IRI:** `https://cair-nepal.org/heritagegraph/enthronedThrough` · `hg:enthronedThrough`

Enthronement event that activated this tenure.

| | |
|---|---|
| Super-properties | [Tenure opened by](object-properties.md#tenureopenedby) |
| Domain | [Kumari Tenure](classes.md#kumaritenure) |
| Range | [Kumari Enthronement Event](classes.md#kumarienthronementevent) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |
| domainIncludes | hg:KumariTenure |

### falls within

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P86_falls_within` · `crm:P86_falls_within`

Quantification: many to many (0,n:0,n)

Scope note:
This property describes the inclusion relationship between two instances of E52 Time-Span.
This property supports the notion that the temporal extent of an instance of E52 Time-Span falls within the temporal extent of another instance of E52 Time-Span. It addresses temporal containment only, and no contextual link between the two instances of E52 Time-Span is implied. This property is transitive and reflexive.

Examples:
- The time-span of the Apollo 11 moon mission (E52) falls within the time-span of the reign of Queen Elizabeth II (E52). (Riley, 2009; Robinson, 2000)

In First Order Logic:
- P86(x,y) ⇒ E52(x) 
- P86(x,y) ⇒ E52(y)
- [P86(x,y) ∧ P86(y,z)] ⇒ P86(x,z)
- P86(x,x)

### forms part of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P46i_forms_part_of` · `crm:P46i_forms_part_of`

Quantification of the inverse property: many to many (0,n:0,n)

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
- P46(x,y) ⇒ ¬P46(y,x)

| | |
|---|---|
| Inverse of | [is composed of](object-properties.md#p46_is_composed_of) |
| Used in | used in axioms of [Architectural Element](classes.md#architecturalelement) |

### forms part of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P9i_forms_part_of` · `crm:P9i_forms_part_of`

Quantification of the inverse property: many to many (0,n:0,n)

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
- P9(x,y) ⇒ ¬P9(y,x)

| | |
|---|---|
| Inverse of | [consists of](object-properties.md#p9_consists_of) |

### generated

**IRI:** `http://www.w3.org/ns/prov#generated` · `prov:generated`

| | |
|---|---|
| Inverse of | [wasGeneratedBy](object-properties.md#wasgeneratedby) |

### Had participant

**IRI:** `https://cair-nepal.org/heritagegraph/hadParticipant` · `hg:hadParticipant`

Actor(s) participating in this period, situation or ritual without carrying it out (e.g. the Kumari in a chariot procession). The holder of a tenure is given with hg:tenureHolder.

| | |
|---|---|
| Domain | [Ritual Event](classes.md#ritualevent); [Kumari Tenure](classes.md#kumaritenure) |
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent; hg:KumariTenure |

### has access protocol

**IRI:** `https://cair-nepal.org/heritagegraph/accessProtocol` · `hg:accessProtocol`

Cultural access protocol for the thing or its record (e.g. restricted to initiates, secret or sacred, seasonal), set with the community concerned; a subproperty of dcterms:accessRights. Data under a restriction should not be published.

| | |
|---|---|
| Super-properties | [Access Rights](object-properties.md#accessrights) |
| Domain | [Transfer of Custody](classes.md#e10_transfer_of_custody) *or* [Production](classes.md#e12_production) *or* [Condition Assessment](classes.md#e14_condition_assessment) *or* [Human-Made Object](classes.md#e22_human-made_object) *or* [Design or Procedure](classes.md#e29_design_or_procedure) *or* [Condition State](classes.md#e3_condition_state) *or* [Time-Span](classes.md#e52_time-span) *or* [Place](classes.md#e53_place) *or* [Material](classes.md#e57_material) *or* [Destruction](classes.md#e6_destruction) *or* [Belief](classes.md#i2_belief) *or* [Architectural Element](classes.md#architecturalelement) *or* [Calendar System](classes.md#calendarsystem) *or* [Data Source](classes.md#datasource) *or* [Deity](classes.md#deity) *or* [Documentation Activity](classes.md#documentationactivity) *or* [Endowment](classes.md#endowment) *or* [Endowment Event](classes.md#endowmentevent) *or* [Historical Event](classes.md#historicalevent) *or* [Office](classes.md#office) *or* [Physical Heritage Thing](classes.md#physicalheritagething) *or* [Proposition](classes.md#proposition) *or* [Religious Tradition](classes.md#religioustradition) *or* [Ritual Event](classes.md#ritualevent) *or* [Selection Criterion](classes.md#selectioncriterion) *or* [Structure Type](classes.md#structuretype) *or* [Syncretic Relationship](classes.md#syncreticrelationship) *or* [Tenure](classes.md#tenure) |
| Range | [Access Protocol](classes.md#accessprotocol-2) |

### Has architectural style

**IRI:** `https://cair-nepal.org/heritagegraph/hasArchitecturalStyle` · `hg:hasArchitecturalStyle`

Architectural style classification.

| | |
|---|---|
| Super-properties | [has type](object-properties.md#p2_has_type) |
| Domain | [Architectural Structure](classes.md#architecturalstructure) |
| Range | [Architectural Style](classes.md#architecturalstyle-2) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Temple](classes.md#temple) |
| domainIncludes | hg:ArchitecturalStructure |

### Has assertion

**IRI:** `https://cair-nepal.org/heritagegraph/hasAssertion` · `hg:hasAssertion`

Provenance-bearing assertion made about this entity or event.

| | |
|---|---|
| Domain | [Assertion Subject](classes.md#assertionsubject) |
| Range | [Belief](classes.md#i2_belief) |
| Inverse of | [Asserts about](object-properties.md#assertsabout) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Custody Period](classes.md#custodyperiod); used in axioms of [Endowment](classes.md#endowment); used in axioms of [Endowment Event](classes.md#endowmentevent); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Tenure](classes.md#tenure) |

### has calendar system

**IRI:** `https://cair-nepal.org/heritagegraph/calendarSystem` · `hg:calendarSystem`

Calendar system used for date representation.

| | |
|---|---|
| Domain | [Time-Span](classes.md#e52_time-span) |
| Range | [Calendar System](classes.md#calendarsystem) |

### Has condition type

**IRI:** `https://cair-nepal.org/heritagegraph/hasConditionType` · `hg:hasConditionType`

Categorization of the condition state.

| | |
|---|---|
| Super-properties | [has type](object-properties.md#p2_has_type) |
| Domain | [Condition State](classes.md#e3_condition_state) |
| Range | [Condition Type](classes.md#conditiontype-2) |

### Has criterion

**IRI:** `https://cair-nepal.org/heritagegraph/hasCriterion` · `hg:hasCriterion`

Eligibility criterion applied in this selection.

| | |
|---|---|
| Domain | [Kumari Selection Event](classes.md#kumariselectionevent) |
| Range | [Selection Criterion](classes.md#selectioncriterion) |
| Used in | used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |
| domainIncludes | hg:KumariSelectionEvent |

### has current location

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P55_has_current_location` · `crm:P55_has_current_location`

Quantification: many to many (0,n:0,n)

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
- ˄ ¬​ (∃w) [E9(w) ˄ P25i(x,w) ˄ P27(w,y)˄ P182(z,w)]]​

### has current or former member

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P107_has_current_or_former_member` · `crm:P107_has_current_or_former_member`

Quantification: many to many (0,n:0,n)

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
- P107(x,y) ⇐ (∃z) [E85(z) ˄ P144i(x,z) ˄ P143(z,y)]

| | |
|---|---|
| Inverse of | [is current or former member of](object-properties.md#p107i_is_current_or_former_member_of) |

### has date precision

**IRI:** `https://cair-nepal.org/heritagegraph/datePrecision` · `hg:datePrecision`

The level of precision for a recorded date.

| | |
|---|---|
| Domain | [Time-Span](classes.md#e52_time-span) |
| Range | [Date Precision](classes.md#dateprecision-2) |

### has destruction event

**IRI:** `https://cair-nepal.org/heritagegraph/destructionEvent` · `hg:destructionEvent`

Event that destroyed this structure (if known).

| | |
|---|---|
| Domain | [Architectural Structure](classes.md#architecturalstructure) |
| Range | [Destruction](classes.md#e6_destruction) |
| Inverse of | [destroyed](object-properties.md#p13_destroyed) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |
| domainIncludes | hg:ArchitecturalStructure |

### has endowment event type

**IRI:** `https://cair-nepal.org/heritagegraph/endowmentEventType` · `hg:endowmentEventType`

Kind of endowment event (founding, augmentation, nationalisation, alienation).

| | |
|---|---|
| Domain | [Endowment Event](classes.md#endowmentevent) |
| Range | [Endowment Event Type](classes.md#endowmenteventtype) |
| Used in | used in axioms of [Endowment Event](classes.md#endowmentevent) |
| domainIncludes | hg:EndowmentEvent |

### has existence status

**IRI:** `https://cair-nepal.org/heritagegraph/existenceStatus` · `hg:existenceStatus`

Current physical status of the structure.

| | |
|---|---|
| Domain | [Architectural Structure](classes.md#architecturalstructure) |
| Range | [Existence Status](classes.md#existencestatus-2) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |
| domainIncludes | hg:ArchitecturalStructure |

### has guthi type

**IRI:** `https://cair-nepal.org/heritagegraph/guthiType` · `hg:guthiType`

Type of Guthi (Si, Jatra, Temple).

| | |
|---|---|
| Super-properties | [has type](object-properties.md#p2_has_type) |
| Domain | [Guthi](classes.md#guthi) |
| Range | [Guthi Type](classes.md#guthitype-2) |
| Used in | used in axioms of [Guthi](classes.md#guthi) |
| domainIncludes | hg:Guthi |

### has identified

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P35_has_identified` · `crm:P35_has_identified`

Quantification: many to many, necessary (1,n:0,n)

Scope note:
This property identifies the instance of E3 Condition State that was observed in an instance of E14 Condition Assessment activity.

Examples:
- The condition assessment of silver cup 232 in 1997 (E14) has identified oxidation traces were present in 1997 (E3). [which has type (P2) with oxidation traces (E55)] (fictitious)
- The condition assessment of the cover of MS Sinai Greek 418 (E13) has identified the condition state in November 2003 (E3). [which has type fine (E55)] (Honey and Pickwoad, 2010)
- The condition assessment of the endband cores of MS Sinai Greek 418 (E14) has identified the condition state in November 2003 (E3). [which has type broken (E55)] (Honey and Pickwoad, 2010)

In First Order Logic:
- P35(x,y) ⇒E14(x)
- P35(x,y) ⇒ E3(y)
- P35(x,y) ⇒ P141(x,y)

### has produced

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P108_has_produced` · `crm:P108_has_produced`

Quantification: one to many, necessary, dependent (1,n:1,1)

Scope note:
This property identifies the instance of E24 Physical Human-Made Thing that came into existence as a result of the instance of E12 Production.
The identity of an instance of E24 Physical Human-Made Thing is not defined by its matter, but by its existence as a subject of documentation. An E12 Production can result in the creation of multiple instances of E24 Physical Human-Made Thing.

Examples:
- The building of Rome (E12) has produced the Colosseum (E24). (Hopkins &amp; Beard, 2011)

In First Order Logic:
- P108(x,y) ⇒ E12(x)
- P108(x,y) ⇒ E24(y)
- P108(x,y) ⇒ P31(x,y)
- P108(x,y) ⇒ P92(x,y)

| | |
|---|---|
| Inverse of | [was produced by](object-properties.md#p108i_was_produced_by) |

### Has religious tradition

**IRI:** `https://cair-nepal.org/heritagegraph/hasReligiousTradition` · `hg:hasReligiousTradition`

Religious tradition(s) within which this deity is venerated, or which use this structure (a temple, or a pavilion, rest house or water spout with a shrine).

| | |
|---|---|
| Super-properties | [has type](object-properties.md#p2_has_type) |
| Domain | [Architectural Structure](classes.md#architecturalstructure); [Deity](classes.md#deity) |
| Range | [Religious Tradition](classes.md#religioustradition) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Deity](classes.md#deity) |
| domainIncludes | hg:ArchitecturalStructure; hg:Deity |

### has ritual type

**IRI:** `https://cair-nepal.org/heritagegraph/ritualType` · `hg:ritualType`

Classification of ritual (puja, jatra, consecration).

| | |
|---|---|
| Super-properties | [has type](object-properties.md#p2_has_type) |
| Domain | [Ritual Event](classes.md#ritualevent) |
| Range | [Ritual Type](classes.md#ritualtype) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent |

### has structure type

**IRI:** `https://cair-nepal.org/heritagegraph/structureType` · `hg:structureType`

Type of the structure from a controlled vocabulary or a local term list (e.g. bahah, dyochhen), finer than its class; a subproperty of crm:P2_has_type.

| | |
|---|---|
| Super-properties | [has type](object-properties.md#p2_has_type) |
| Domain | [Architectural Structure](classes.md#architecturalstructure) |
| Range | [Structure Type](classes.md#structuretype) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |
| domainIncludes | hg:ArchitecturalStructure |

### has syncretic type

**IRI:** `https://cair-nepal.org/heritagegraph/syncreticType` · `hg:syncreticType`

The typological nature of the syncretism (e.g., Ontological Identity, Functional Overlap, Iconographic Similarity).

| | |
|---|---|
| Super-properties | [has type](object-properties.md#p2_has_type) |
| Domain | [Syncretic Relationship](classes.md#syncreticrelationship) |
| Range | [Syncretic Type](classes.md#syncretictype-2) |
| Used in | used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |
| domainIncludes | hg:SyncreticRelationship |

### has time-span

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P4_has_time-span` · `crm:P4_has_time-span`

Quantification: many to one, necessary (1,1:0,n)

Scope note:
This property associates an instance of E2 Temporal Entity with the instance of E52 Time-Span during which it was on-going. The associated instance of E52 Time-Span is understood as the real time-span during which the phenomena making up the temporal entity instance were active. More than one instance of E2 Temporal Entity may share a common instance of E52 Time-Span only if they come into being and end being due to identical declarations or events.

Examples:
- The Yalta Conference (E7) has time-span Yalta Conference time-span (E52). (Harbutt, 2010)

In First Order Logic:
- P4(x,y) ⇒ E2(x)
- P4(x,y) ⇒ E52(y)

| | |
|---|---|
| Used in | used in axioms of [Consecration](classes.md#consecration); used in axioms of [Custody Period](classes.md#custodyperiod); used in axioms of [Documentation Activity](classes.md#documentationactivity); used in axioms of [Endowment Event](classes.md#endowmentevent); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Tenure](classes.md#tenure) |

### has type

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P2_has_type` · `crm:P2_has_type`

Quantification: many to many (0,n:0,n)

Scope note:
This property allows sub-typing of CIDOC CRM entities –a form of specialisation – through the use of a terminological hierarchy, or thesaurus. 
The CIDOC CRM is intended to focus on the high-level entities and relationships needed to describe data structures. Consequently, it does not specialise entities any further than is required for this immediate purpose. However, entities in the isA hierarchy of the CIDOC CRM may by specialised into any number of sub-entities, which can be defined in the E55 Type hierarchy. E41 Appellation, for example, may be specialised into “e-mail address”, “telephone number”, “post office box”, “URL”, etc., none of which figures explicitly in the CIDOC CRM class hierarchy. A comprehensive explanation about refining CIDOC CRM concepts by E55 Type is given in the section “About Types” in the section on “Specific Modelling Constructs” of this document.
This property is a shortcut for the path from E1 CRM Entity through P41i was classified by, E17 Type Assignment, P42 assigned to E55 Type.

Examples:
- “enquiries@cidoc-crm.org” (E41) has type e-mail address (E55). (fictitious)

In First Order Logic:
- P2(x,y) ⇒ E1(x)
- P2(x,y) ⇒ E55(y)
- P2(x,y) ⇐ (∃z) [E17(z)] ˄ P41i(x,z) ˄ P42(z,y)]

| | |
|---|---|
| Sub-properties | [Has architectural style](object-properties.md#hasarchitecturalstyle), [Has condition type](object-properties.md#hasconditiontype), [has guthi type](object-properties.md#guthitype), [Has religious tradition](object-properties.md#hasreligioustradition), [has ritual type](object-properties.md#ritualtype), [has structure type](object-properties.md#structuretype), [has syncretic type](object-properties.md#syncretictype) |

### Hypothesized location

**IRI:** `https://cair-nepal.org/heritagegraph/hypothesizedLocation` · `hg:hypothesizedLocation`

Possible locations if the structure is lost.

| | |
|---|---|
| Domain | [Architectural Structure](classes.md#architecturalstructure) |
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |
| domainIncludes | hg:ArchitecturalStructure |

### Initiated tenure

**IRI:** `https://cair-nepal.org/heritagegraph/initiatedTenure` · `hg:initiatedTenure`

Kumari tenure that was initiated by this selection event.

| | |
|---|---|
| Super-properties | [Bounds tenure](object-properties.md#boundstenure) |
| Domain | [Kumari Selection Event](classes.md#kumariselectionevent) |
| Range | [Kumari Tenure](classes.md#kumaritenure) |
| Inverse of | [Selected through](object-properties.md#selectedthrough) |
| Used in | used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |
| domainIncludes | hg:KumariSelectionEvent |

### Invokes deity

**IRI:** `https://cair-nepal.org/heritagegraph/invokesDeity` · `hg:invokesDeity`

Deity invoked or made present through ritual.

| | |
|---|---|
| Super-properties | [occurred in the presence of](object-properties.md#p12_occurred_in_the_presence_of) |
| Domain | [Ritual Event](classes.md#ritualevent) |
| Range | [Deity](classes.md#deity) |
| Inverse of | [Is invoked in ritual](object-properties.md#isinvokedinritual) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent |

### is about

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P129_is_about` · `crm:P129_is_about`

Quantification: many to many (0,n:0,n)

Scope note:
This property documents that an instance of E89 Propositional Object has as subject an instance of E1 CRM Entity. 
This differs from P67 refers to (is referred to by), which refers to an instance of E1 CRM Entity, in that it describes the primary subject or subjects of an instance of E89 Propositional Object.

Examples:
- The text entitled ‘Reach for the sky’ (E33) is about Douglas Bader (E21). (Brickhill, 2001)

In First Order Logic:
- P129(x,y) ⇒ E89(x)
- P129(x,y) ⇒ E1(y) 
- P129(x,y) ⇒ P67(x,y)

### Is about deity

**IRI:** `https://cair-nepal.org/heritagegraph/isAboutDeity` · `hg:isAboutDeity`

Deity represented and ritually associated with the Murti.

| | |
|---|---|
| Super-properties | [depicts](object-properties.md#p62_depicts) |
| Domain | [Murti](classes.md#murti) |
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Murti](classes.md#murti) |
| domainIncludes | hg:Murti |

### is composed of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P46_is_composed_of` · `crm:P46_is_composed_of`

Quantification: many to many (0,n:0,n)

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
- P46(x,y) ⇒ ¬P46(y,x)

| | |
|---|---|
| Inverse of | [forms part of](object-properties.md#p46i_forms_part_of) |

### is current keeper of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P50i_is_current_keeper_of` · `crm:P50i_is_current_keeper_of`

Quantification of the inverse property: many to many (0,n:0,n)

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
- ˄ ¬ (∃w) [E10(w) ˄ P30i(x,w) ˄ P28(w,y)˄ P182(z,w)]]

### is current or former member of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P107i_is_current_or_former_member_of` · `crm:P107i_is_current_or_former_member_of`

Quantification of the inverse property: many to many (0,n:0,n)

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
- P107(x,y) ⇐ (∃z) [E85(z) ˄ P144i(x,z) ˄ P143(z,y)]

| | |
|---|---|
| Inverse of | [has current or former member](object-properties.md#p107_has_current_or_former_member) |

### is depicted by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P62i_is_depicted_by` · `crm:P62i_is_depicted_by`

Quantification of the inverse property: many to many (0,n:0,n)

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
- P62(x,y) ⇐ (∃z) [E36(z) ˄ P65(x,z) ˄ P138(z,y)]

| | |
|---|---|
| Inverse of | [depicts](object-properties.md#p62_depicts) |

### Is enshrined through event

**IRI:** `https://cair-nepal.org/heritagegraph/isEnshrinedThroughEvent` · `hg:isEnshrinedThroughEvent`

Events where this deity was enshrined.

| | |
|---|---|
| Domain | [Deity](classes.md#deity) |
| Range | [Enshrinement](classes.md#enshrinement) |
| Inverse of | [Enshrined deity](object-properties.md#enshrineddeity) |
| Used in | used in axioms of [Deity](classes.md#deity) |
| domainIncludes | hg:Deity |

### is former or current location of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P53i_is_former_or_current_location_of` · `crm:P53i_is_former_or_current_location_of`

Quantification of the inverse property: many to many, necessary (1,n:0,n)

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
- P53(x,y) ⇐ (∃z) [E9(z) ˄ P25i(x,z) ˄ [P26(z,y) ˅ P27(z,y)]]

### Is invoked in ritual

**IRI:** `https://cair-nepal.org/heritagegraph/isInvokedInRitual` · `hg:isInvokedInRitual`

Rituals where this deity is invoked.

| | |
|---|---|
| Super-properties | [was present at](object-properties.md#p12i_was_present_at) |
| Domain | [Deity](classes.md#deity) |
| Range | [Ritual Event](classes.md#ritualevent) |
| Inverse of | [Invokes deity](object-properties.md#invokesdeity) |
| Used in | used in axioms of [Deity](classes.md#deity) |
| domainIncludes | hg:Deity |

### Is primary for tradition

**IRI:** `https://cair-nepal.org/heritagegraph/isPrimaryForTradition` · `hg:isPrimaryForTradition`

Religious tradition(s) that use this calendar system for their rites. Calendars are not divided by religion in Nepal: Nepal Sambat is the era of the Newar ritual calendar, used by Newar Hindus and Buddhists alike, and Bikram Sambat is the official civil era.

| | |
|---|---|
| Domain | [Calendar System](classes.md#calendarsystem) |
| Range | [Religious Tradition](classes.md#religioustradition) |
| Used in | used in axioms of [Calendar System](classes.md#calendarsystem) |
| domainIncludes | hg:CalendarSystem |

### Makes deity present

**IRI:** `https://cair-nepal.org/heritagegraph/makesDeityPresent` · `hg:makesDeityPresent`

Deity made present through consecration.

| | |
|---|---|
| Domain | [Consecration](classes.md#consecration) |
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Consecration](classes.md#consecration) |
| domainIncludes | hg:Consecration |

### Managed by guthi

**IRI:** `https://cair-nepal.org/heritagegraph/managedByGuthi` · `hg:managedByGuthi`

Guthi organization managing this structure or ritual.

| | |
|---|---|
| Domain | [Ritual Event](classes.md#ritualevent); [Architectural Structure](classes.md#architecturalstructure) |
| Range | [Guthi](classes.md#guthi) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent; hg:ArchitecturalStructure |

### Mandated by

**IRI:** `https://cair-nepal.org/heritagegraph/mandatedBy` · `hg:mandatedBy`

Guthi or state body that mandates (and usually funds) the hereditary duty.

| | |
|---|---|
| Domain | [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| Range | [Group](classes.md#e74_group) |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| domainIncludes | hg:HereditaryRoleTenure |

### obsolete actors ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/actors` · `hg:actors`

Collection of generic Actor instances.

### obsolete architectural elements ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/architectural_elements` · `hg:architectural_elements`

Collection of ArchitecturalElement instances.

### obsolete assertions ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/assertions` · `hg:assertions`

Collection of Assertion instances.

### obsolete calendar systems ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/calendar_systems` · `hg:calendar_systems`

Collection of CalendarSystem instances.

### obsolete caste groups ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/caste_groups` · `hg:caste_groups`

Collection of CasteGroup instances.

### obsolete condition assessments ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/condition_assessments` · `hg:condition_assessments`

Collection of ConditionAssessment instances.

### obsolete condition states ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/condition_states` · `hg:condition_states`

Collection of ConditionState instances.

### obsolete consecration events ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/consecration_events` · `hg:consecration_events`

Collection of Consecration event instances.

### obsolete custody events ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/custody_events` · `hg:custody_events`

Collection of TransferOfCustody event instances.

### obsolete data custodians ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/data_custodians` · `hg:data_custodians`

Collection of DataCustodian instances.

### obsolete data sources ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/data_sources` · `hg:data_sources`

Collection of DataSource instances.

### obsolete deities ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/deities` · `hg:deities`

Collection of Deity instances.

### obsolete documentation activities ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/documentation_activities` · `hg:documentation_activities`

Collection of DocumentationActivity instances.

### obsolete enshrinement events ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/enshrinement_events` · `hg:enshrinement_events`

Collection of Enshrinement event instances.

### obsolete festivals ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/festivals` · `hg:festivals`

Collection of Festival instances.

### obsolete guthis ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/guthis` · `hg:guthis`

Collection of Guthi instances.

### obsolete has metadata ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/metadata` · `hg:metadata`

Dataset metadata.

### obsolete historical events ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/historical_events` · `hg:historical_events`

Collection of HistoricalEvent (incl. DestructionEvent) instances.

### obsolete human made objects ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/human_made_objects` · `hg:human_made_objects`

Collection of generic HumanMadeObject instances (use structures / iconographic_objects for subclasses).

### obsolete iconographic objects ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/iconographic_objects` · `hg:iconographic_objects`

Collection of IconographicObject instances (incl. Murti, Paubha).

### obsolete information objects ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/information_objects` · `hg:information_objects`

Collection of InformationObject instances.

### obsolete kumari lifecycle events ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/kumari_lifecycle_events` · `hg:kumari_lifecycle_events`

Collection of Kumari lifecycle events (selection, enthronement, retirement).

### obsolete kumari roles ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/kumari_roles` · `hg:kumari_roles`

Collection of KumariRole instances.

### obsolete kumari tenures ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/kumari_tenures` · `hg:kumari_tenures`

Collection of KumariTenure instances.

### obsolete materials ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/materials` · `hg:materials`

Collection of Material instances.

### obsolete persons ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/persons` · `hg:persons`

Collection of Person instances.

### obsolete physical heritage things ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/physical_heritage_things` · `hg:physical_heritage_things`

Collection of all physical heritage objects.

### obsolete places ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/places` · `hg:places`

Collection of Place instances.

### obsolete production events ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/production_events` · `hg:production_events`

Collection of Production event instances.

### obsolete propositions ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/propositions` · `hg:propositions`

Collection of Proposition instances referenced by assertions.

### obsolete religious traditions ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/religious_traditions` · `hg:religious_traditions`

Collection of ReligiousTradition instances.

### obsolete ritual assessments ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/ritual_assessments` · `hg:ritual_assessments`

Collection of RitualAssessment (e.g. FearlessnessAssessment) instances.

### obsolete ritual events ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/ritual_events` · `hg:ritual_events`

Collection of RitualEvent instances.

### obsolete selection criteria ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/selection_criteria` · `hg:selection_criteria`

Collection of SelectionCriterion instances.

### obsolete structures ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/structures` · `hg:structures`

Collection of ArchitecturalStructure instances (incl. subclasses).

### obsolete syncretic relationships ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/syncretic_relationships` · `hg:syncretic_relationships`

Collection of SyncreticRelationship instances.

### obsolete techniques ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/techniques` · `hg:techniques`

Collection of Technique instances.

### obsolete time spans ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/time_spans` · `hg:time_spans`

Collection of TimeSpan instances.

### occurred in the presence of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P12_occurred_in_the_presence_of` · `crm:P12_occurred_in_the_presence_of`

Quantification: many to many, necessary (1,n:0,n)

Scope note:
This property describes the active or passive presence of an E77 Persistent Item in an instance of E5 Event without implying any specific role. 
It documents known events in which an instance of E77 Persistent Item was present during the course of its life or history. For example, an object may be the desk, now in a museum, on which a treaty was signed. The instance of E53 Place and the instance of E52 Time-Span where and when these events happened provide constraints about the presence of the related instance E77 Persistent Item in the past. Instances of E90 Symbolic Object, in particular information objects, are physically present in events via at least one of the instances of E18 Physical Thing carrying them. Note, that the human mind can be such a carrier. A precondition for a transfer of information to a person or another new physical carrier is the presence of the respective information object and this person or physical thing in one event.

Examples:
- Deckchair 42 (E19) was present at the sinking of the Titanic (E5). (Aldridge, 2008)

In First Order Logic:
- P12(x,y) ⇒ E5(x)
- P12(x,y) ⇒ E77(y)

| | |
|---|---|
| Sub-properties | [Architectural structures](object-properties.md#architecturalstructures), [Enshrined deity](object-properties.md#enshrineddeity), [Invokes deity](object-properties.md#invokesdeity) |
| Inverse of | [was present at](object-properties.md#p12i_was_present_at) |

### Part of selection

**IRI:** `https://cair-nepal.org/heritagegraph/partOfSelection` · `hg:partOfSelection`

Selection event this assessment is part of.

| | |
|---|---|
| Domain | [Ritual Assessment](classes.md#ritualassessment) |
| Range | [Kumari Selection Event](classes.md#kumariselectionevent) |
| Used in | used in axioms of [Ritual Assessment](classes.md#ritualassessment) |
| domainIncludes | hg:RitualAssessment |

### Participates in ritual

**IRI:** `https://cair-nepal.org/heritagegraph/participatesInRitual` · `hg:participatesInRitual`

Rituals in which this structure participates.

| | |
|---|---|
| Super-properties | [was present at](object-properties.md#p12i_was_present_at) |
| Domain | [Human-Made Object](classes.md#e22_human-made_object) |
| Range | [Ritual Event](classes.md#ritualevent) |
| Used in | used in axioms of [Iconographic Object](classes.md#iconographicobject) |

### performed

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P14i_performed` · `crm:P14i_performed`

Quantification of the inverse property: many to many, necessary (1,n:0,n)

Scope note of the inverse property:
This property describes the active participation of an instance of E39 Actor in an instance of E7 Activity. 
It implies causal or legal responsibility. The P14.1 in the role of property of the property specifies the nature of an Actor’s participation.

Examples of the inverse property:
- The painting of the Sistine Chapel (E7) carried out by Michelangelo Buonaroti (E21) in the role of master craftsman (E55). (Goldscheider, 1953)

In First Order Logic of the inverse property:
- P14(x,y) ⇒ E7(x)
- P14(x,y)⇒ E39(y)
- P14(x,y) ⇒ P11(x,y)
- P14(x,y,z) ⇒ [P14(x,y) ∧ E55(z)]

| | |
|---|---|
| Sub-properties | [Performs ritual](object-properties.md#performsritual) |
| Inverse of | [carried out by](object-properties.md#p14_carried_out_by) |

### Performed by group

**IRI:** `https://cair-nepal.org/heritagegraph/performedByGroup` · `hg:performedByGroup`

Group (Guthi, caste) responsible for ritual.

| | |
|---|---|
| Super-properties | [carried out by](object-properties.md#p14_carried_out_by) |
| Domain | [Ritual Event](classes.md#ritualevent) |
| Range | ([Guthi](classes.md#guthi) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent |

### Performs ritual

**IRI:** `https://cair-nepal.org/heritagegraph/performsRitual` · `hg:performsRitual`

Rituals performed by this Guthi.

| | |
|---|---|
| Super-properties | [performed](object-properties.md#p14i_performed) |
| Domain | [Guthi](classes.md#guthi) |
| Range | [Ritual Event](classes.md#ritualevent) |
| Used in | used in axioms of [Guthi](classes.md#guthi) |
| domainIncludes | hg:Guthi |

### Proposition object entity

**IRI:** `https://cair-nepal.org/heritagegraph/propositionObjectEntity` · `hg:propositionObjectEntity`

Object of the proposition when it is a heritage entity (plays the role of rdf:object).

| | |
|---|---|
| Domain | [Proposition](classes.md#proposition) |
| Range | [Assertion Subject](classes.md#assertionsubject) |
| Used in | used in axioms of [Proposition](classes.md#proposition) |
| domainIncludes | hg:Proposition |

### Proposition subject

**IRI:** `https://cair-nepal.org/heritagegraph/propositionSubject` · `hg:propositionSubject`

Entity the proposition is about (plays the role of rdf:subject).

| | |
|---|---|
| Domain | [Proposition](classes.md#proposition) |
| Range | [Assertion Subject](classes.md#assertionsubject) |
| Used in | used in axioms of [Proposition](classes.md#proposition) |
| domainIncludes | hg:Proposition |

### Publication timespan

**IRI:** `https://cair-nepal.org/heritagegraph/publicationTimespan` · `hg:publicationTimespan`

When source was published.

| | |
|---|---|
| Domain | [Data Source](classes.md#datasource) |
| Range | [Time-Span](classes.md#e52_time-span) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |
| domainIncludes | hg:DataSource |

### records

**IRI:** `https://cair-nepal.org/heritagegraph/documents` · `hg:documents`

Pre-existing heritage entity or event recorded by this documentation activity (inverse of hg:documentedBy).

| | |
|---|---|
| Domain | [Documentation Activity](classes.md#documentationactivity) |
| Range | [Assertion Subject](classes.md#assertionsubject) |
| Inverse of | [Was documented by](object-properties.md#documentedby) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |
| domainIncludes | hg:DocumentationActivity |

### Residence structure

**IRI:** `https://cair-nepal.org/heritagegraph/residenceStructure` · `hg:residenceStructure`

Structure where a person resides during a specific period. For Living Goddess, this is typically a Kumari Ghar (god-house).

| | |
|---|---|
| Domain | [Kumari Tenure](classes.md#kumaritenure) |
| Range | [Architectural Structure](classes.md#architecturalstructure) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |
| domainIncludes | hg:KumariTenure |

### Retired through

**IRI:** `https://cair-nepal.org/heritagegraph/retiredThrough` · `hg:retiredThrough`

Retirement/desanctification event that ended this tenure.

| | |
|---|---|
| Super-properties | [Tenure closed by](object-properties.md#tenureclosedby) |
| Domain | [Kumari Tenure](classes.md#kumaritenure) |
| Range | [Kumari Retirement Event](classes.md#kumariretirementevent) |
| Inverse of | [Ended tenure of](object-properties.md#endedtenureof) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |
| domainIncludes | hg:KumariTenure |

### right held by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P105_right_held_by` · `crm:P105_right_held_by`

Quantification: many to many (0,n:0,n)

Scope note:
This property identifies the instance of E39 Actor who holds the instances of E30 Right to an instance of E72 Legal Object.
It is a superproperty of P52 has current owner (is current owner of) because ownership is a right that is held on the owned object.
This property is a shortcut of the fully developed path from E72 Legal Object, P104 is subject to, E30 Right, P75i is possessed by to E39 Actor.

Examples:
- The Beatles back catalogue (E73) right held by Michael Jackson (E21). (Raga, 2016)

In First Order Logic:
- P105(x,y) ⇒ E72(x)
- P105(x,y) ⇒ E39(y)
- P105(x,y) ⇐ (∃z) [E30(z) ˄ P104(x,z) ˄ P75i(z,y)]

| | |
|---|---|
| Used in | used in axioms of [Endowment](classes.md#endowment) |

### Role deity

**IRI:** `https://cair-nepal.org/heritagegraph/roleDeity` · `hg:roleDeity`

Deity embodied by whoever holds this role (e.g., Taleju).

| | |
|---|---|
| Domain | [Kumari Role](classes.md#kumarirole) |
| Range | [Deity](classes.md#deity) |
| Used in | used in axioms of [Kumari Role](classes.md#kumarirole) |
| domainIncludes | hg:KumariRole |

### Role holder

**IRI:** `https://cair-nepal.org/heritagegraph/roleHolder` · `hg:roleHolder`

Person or caste group holding the hereditary duty during this tenure.

| | |
|---|---|
| Super-properties | [Tenure holder](object-properties.md#tenureholder) |
| Domain | [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| Range | ([Person](classes.md#e21_person) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| domainIncludes | hg:HereditaryRoleTenure |

### Route places

**IRI:** `https://cair-nepal.org/heritagegraph/routePlaces` · `hg:routePlaces`

Ordered list of places visited during movement ritual.

| | |
|---|---|
| Domain | [Ritual Event](classes.md#ritualevent) |
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent |

### Selected person

**IRI:** `https://cair-nepal.org/heritagegraph/selectedPerson` · `hg:selectedPerson`

Person selected through a ritual selection process to assume a sacred role or office.

| | |
|---|---|
| Domain | [Kumari Selection Event](classes.md#kumariselectionevent) |
| Range | [Person](classes.md#e21_person) |
| Used in | used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |
| domainIncludes | hg:KumariSelectionEvent |

### Selected through

**IRI:** `https://cair-nepal.org/heritagegraph/selectedThrough` · `hg:selectedThrough`

Selection event that preceded this tenure. Not a tenure-opening event: the tenure opens with the enthronement (hg:enthronedThrough, a subproperty of hg:tenureOpenedBy).

| | |
|---|---|
| Domain | [Kumari Tenure](classes.md#kumaritenure) |
| Range | [Kumari Selection Event](classes.md#kumariselectionevent) |
| Inverse of | [Initiated tenure](object-properties.md#initiatedtenure) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |
| domainIncludes | hg:KumariTenure |

### source creator

**IRI:** `https://cair-nepal.org/heritagegraph/sourceCreator` · `hg:sourceCreator`

Person or organization primarily responsible for creating the source.

| | |
|---|---|
| Domain | [Data Source](classes.md#datasource) |
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |
| domainIncludes | hg:DataSource |

### Start place

**IRI:** `https://cair-nepal.org/heritagegraph/startPlace` · `hg:startPlace`

Starting location of movement ritual.

| | |
|---|---|
| Domain | [Ritual Event](classes.md#ritualevent) |
| Range | [Place](classes.md#e53_place) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent |

### starts after the end of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P183i_starts_after_the_end_of` · `crm:P183i_starts_after_the_end_of`

Quantification of the inverse property: many to many (0,n:0,n)

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
- P183(x,y) ⇒ ¬P183(y,x)

| | |
|---|---|
| Inverse of | [ends before the start of](object-properties.md#p183_ends_before_the_start_of) |

### succeeds

**IRI:** `https://cair-nepal.org/heritagegraph/succeeds` · `hg:succeeds`

Earlier tenure of the same hereditary office that this tenure succeeds.

| | |
|---|---|
| Domain | [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| Range | [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| Characteristics | Asymmetric, Irreflexive |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| domainIncludes | hg:HereditaryRoleTenure |

### Supported by institution

**IRI:** `https://cair-nepal.org/heritagegraph/supportedByInstitution` · `hg:supportedByInstitution`

Institution(s) providing economic support (stipend, land endowment) or ritual support (priest salaries) for a Living Goddess during tenure. Extends Guthi role beyond structure management to person support.

| | |
|---|---|
| Domain | [Kumari Tenure](classes.md#kumaritenure) |
| Range | [Group](classes.md#e74_group) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure) |
| domainIncludes | hg:KumariTenure |

### sustains

**IRI:** `https://cair-nepal.org/heritagegraph/sustains` · `hg:sustains`

Structure, ritual or festival, or sacred office whose upkeep or performance the endowment funds.

| | |
|---|---|
| Domain | [Endowment](classes.md#endowment) |
| Range | ([Architectural Structure](classes.md#architecturalstructure) *or* [Ritual Event](classes.md#ritualevent) *or* [Office](classes.md#office)) *and* [Assertion Subject](classes.md#assertionsubject) |
| Used in | used in axioms of [Endowment](classes.md#endowment) |
| domainIncludes | hg:Endowment |

### Tenure closed by

**IRI:** `https://cair-nepal.org/heritagegraph/tenureClosedBy` · `hg:tenureClosedBy`

Event that closed the tenure (e.g. a retirement, a death, a transfer of custody).

| | |
|---|---|
| Sub-properties | [Custody closed by](object-properties.md#custodyclosedby), [Retired through](object-properties.md#retiredthrough) |
| Domain | [Tenure](classes.md#tenure) |
| Range | [Tenure Event](classes.md#tenureevent) |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Tenure](classes.md#tenure) |
| domainIncludes | hg:Tenure |

### Tenure holder

**IRI:** `https://cair-nepal.org/heritagegraph/tenureHolder` · `hg:tenureHolder`

Actor holding the office, duty or custody during the tenure.

| | |
|---|---|
| Sub-properties | [Custody holder](object-properties.md#custodyholder), [Role holder](object-properties.md#roleholder) |
| Domain | [Tenure](classes.md#tenure) |
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Tenure](classes.md#tenure) |
| domainIncludes | hg:Tenure |

### Tenure office

**IRI:** `https://cair-nepal.org/heritagegraph/tenureOffice` · `hg:tenureOffice`

Office, role or duty held during the tenure.

| | |
|---|---|
| Sub-properties | [Assumes role](object-properties.md#assumesrole) |
| Domain | [Tenure](classes.md#tenure) |
| Range | [Office](classes.md#office) |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Tenure](classes.md#tenure) |
| domainIncludes | hg:Tenure |

### Tenure opened by

**IRI:** `https://cair-nepal.org/heritagegraph/tenureOpenedBy` · `hg:tenureOpenedBy`

Event that opened the tenure (e.g. an enthronement, an appointment, a transfer of custody).

| | |
|---|---|
| Sub-properties | [Custody opened by](object-properties.md#custodyopenedby), [Enthroned through](object-properties.md#enthronedthrough) |
| Domain | [Tenure](classes.md#tenure) |
| Range | [Tenure Event](classes.md#tenureevent) |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Tenure](classes.md#tenure) |
| domainIncludes | hg:Tenure |

### that

**IRI:** `http://www.cidoc-crm.org/extensions/crminf/J4_that` · `crminf:J4_that`

This property associates an instance of I4 Proposition Set with the instance of I2 Belief that holds an opinion about it.

### took place at

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P7_took_place_at` · `crm:P7_took_place_at`

Quantification: many to many, necessary (1,n:0,n)

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
- [E4(x) ˄ P157(y,u) ˄ P157(v,u) ˄ P7(x,y) ˄ P161(x,z) ˄ P89(z,v) ˄ P89(v,y)] ⇒ P7(x,v)

### took place on or within

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P8_took_place_on_or_within` · `crm:P8_took_place_on_or_within`

Quantification: many to many (0,n:0,n)

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
- P8(x,y) ⇐ (∃z) [E53(z) ˄ P7(x,z) ˄ P156i(z,y)]

| | |
|---|---|
| Sub-properties | [Enshrined in structure](object-properties.md#enshrinedinstructure) |

### transferred custody of

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P30_transferred_custody_of` · `crm:P30_transferred_custody_of`

Quantification: many to many, necessary (1,n:0,n)

Scope note:
This property identifies the instance(s) of E18 Physical Thing concerned in an instance of E10 Transfer of Custody. 
The property will typically describe the object that is handed over by an instance of E39 Actor to the custody of another instance of E39 Actor. On occasion, physical custody may be transferred involuntarily or illegally, e.g. through accident, unsolicited donation, or theft.

Examples:
- The delivery of the paintings by Secure Deliveries Inc. to the National Gallery (E10) transferred custody of paintings from The Iveagh Bequest (E19).

In First Order Logic:
- P30(x,y) ⇒ E10(x)
- P30(x,y) ⇒ E18(y)

| | |
|---|---|
| Inverse of | [custody transferred through](object-properties.md#p30i_custody_transferred_through) |

### transferred title from

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P23_transferred_title_from` · `crm:P23_transferred_title_from`

Quantification: many to many (0,n:0,n)

Scope note:
This property identifies the instance(s) of E39 Actor who relinquish legal ownership as the result of an instance of E8 Acquisition.
The property will typically be used to describe a person donating or selling an object to a museum. In reality, the title is either transferred to or from someone, or both.

Examples:
- The acquisition of the Amoudruz collection by the Geneva Ethnography Museum (E8) transferred title from the Heirs of Amoudruz (E74).

In First Order Logic:
- P23(x,y) ⇒ E8(x)
- P23(x,y) ⇒ E39(y) 
- P23(x,y) ⇒ P14(x,y)

| | |
|---|---|
| Sub-properties | [Endowment donor](object-properties.md#endowmentdonor) |

### transferred title to

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P22_transferred_title_to` · `crm:P22_transferred_title_to`

Quantification: many to many (0,n:0,n)

Scope note:
This property identifies the instance of E39 Actor that acquires the legal ownership of an object as a result of an instance of E8 Acquisition. 
The property will typically describe an Actor purchasing or otherwise acquiring an object from another Actor. However, title may also be acquired without any corresponding loss of title by another Actor, through legal fieldwork such as hunting, shooting, or fishing.
In reality, the title is either transferred to or from someone, or both.

Examples:
- The acquisition of the Amoudruz collection by the Geneva Ethnography Museum (E8) transferred title to the Geneva Ethnography Museum (E74).

In First Order Logic:
- P22(x,y) ⇒ E8(x)
- P22(x,y) ⇒ E39(y) 
- P22(x,y) ⇒ P14(x,y)

| | |
|---|---|
| Sub-properties | [Endowment recipient](object-properties.md#endowmentrecipient) |

### Transferred to guthi

**IRI:** `https://cair-nepal.org/heritagegraph/transferredToGuthi` · `hg:transferredToGuthi`

New custodian (Guthi).

| | |
|---|---|
| Super-properties | [custody received by](object-properties.md#p29_custody_received_by) |
| Domain | [Transfer of Custody](classes.md#e10_transfer_of_custody) |
| Range | [Guthi](classes.md#guthi) |

### used

**IRI:** `http://www.w3.org/ns/prov#used` · `prov:used`

A prov:Entity that was used by this prov:Activity. For example, :baking prov:used :spoon, :egg, :oven .

### Used by

**IRI:** `https://cair-nepal.org/heritagegraph/usedBy` · `hg:usedBy`

Actor(s) who use, handle, or are responsible for this object in ritual contexts.

| | |
|---|---|
| Domain | [Iconographic Object](classes.md#iconographicobject) |
| Range | [Actor](classes.md#e39_actor) |
| Used in | used in axioms of [Iconographic Object](classes.md#iconographicobject) |
| domainIncludes | hg:IconographicObject |

### used object of type

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P125_used_object_of_type` · `crm:P125_used_object_of_type`

Quantification: many to many (0,n:0,n)

Scope note:
This property associates an instance of E7 Activity to an instance of E55 Type, which classifies an instance of E70 Thing used in an instance of E7 Activity, when the specific instance is either unknown or not of interest, such as use of “a hammer”.
This property is a shortcut of the more fully developed path from E7 Activity through P16 used specific object, E70 Thing, P2 has type, to E55 Type.

Examples:
- The English archers’ activity in the Battle of Agincourt (E7) used object of type long bow (E55). (Curry, 2015)

In First Order Logic:
- P125(x,y) ⇒ E7(x)
- P125(x,y) ⇒ E55(y)
- P125(x,y) ⇔ (∃z) [E70(z) ∧ P16(x,z) ∧ P2(z,y)]

### used specific object

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P16_used_specific_object` · `crm:P16_used_specific_object`

Quantification: many to many (0,n:0,n)

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
- P16(x,y,z) ⇒ [P16(x,y) ∧ E55(z)]

### used specific technique

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P33_used_specific_technique` · `crm:P33_used_specific_technique`

Quantification: many to many (0,n:0,n)

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
- P33(x,y) ⇒ P16(x,y)

### Verified assertion

**IRI:** `https://cair-nepal.org/heritagegraph/verifiedAssertion` · `hg:verifiedAssertion`

Assertions verified by this activity.

| | |
|---|---|
| Domain | [Verification](classes.md#verification) |
| Range | [Belief](classes.md#i2_belief) |
| Used in | used in axioms of [Verification](classes.md#verification) |
| domainIncludes | hg:Verification |

### Verified by expert

**IRI:** `https://cair-nepal.org/heritagegraph/verifiedByExpert` · `hg:verifiedByExpert`

Expert who performed verification.

| | |
|---|---|
| Super-properties | [carried out by](object-properties.md#p14_carried_out_by) |
| Domain | [Verification](classes.md#verification) |
| Range | [Person](classes.md#e21_person) |
| Used in | used in axioms of [Verification](classes.md#verification) |
| domainIncludes | hg:Verification |

### was assessed by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P34i_was_assessed_by` · `crm:P34i_was_assessed_by`

Quantification of the inverse property: many to many, necessary (1,n:0,n)

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
- P34(x,y) ⇒ P140(x,y)

| | |
|---|---|
| Inverse of | [concerned](object-properties.md#p34_concerned) |

### was born

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P98i_was_born` · `crm:P98i_was_born`

Quantification of the inverse property: one to many, dependent (0,n:1,1)

Scope note of the inverse property:
This property links an instance of E67 Birth event to an instance of E21 Person in the role of offspring.
Twins, triplets etc. are brought into life by the same instance of E67 Birth. This is not intended for use with general Natural History material, only people. There is no explicit method for modelling conception and gestation except by using extensions.

Examples of the inverse property:
- The Birth of Queen Elizabeth II (E67) brought into life Queen Elizabeth II (E21). (Parker, 2002)

In First Order Logic of the inverse property:
- P98(x,y) ⇒ E67(x)
- P98(x,y) ⇒ E21(y)
- P98(x,y) ⇒ P92(x,y)

### Was documented by

**IRI:** `https://cair-nepal.org/heritagegraph/documentedBy` · `hg:documentedBy`

Documentation event that recorded this (pre-existing) entity or event. Uses hg:documentedBy (aligned to prov:wasInfluencedBy). NOTE: prov:wasGeneratedBy was incorrect: a stupa is not *generated by* the survey that records it.

| | |
|---|---|
| Super-properties | [wasInfluencedBy](object-properties.md#wasinfluencedby) |
| Domain | [Assertion Subject](classes.md#assertionsubject) |
| Range | [Documentation Activity](classes.md#documentationactivity) |
| Inverse of | [records](object-properties.md#documents) |
| Used in | used in axioms of [Heritage information object](classes.md#informationobject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### was motivated by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P17_was_motivated_by` · `crm:P17_was_motivated_by`

Quantification: many to many (0,n:0,n)

Scope note:
This property describes an item or items that are regarded as a reason for carrying out the instance of E7 Activity. 
For example, the discovery of a large hoard of treasure may call for a celebration, an order from headquarters can start a military manoeuvre.

Examples:
- The resignation of the chief executive (E7) was motivated by the collapse of SwissAir (E68).
- The coronation of Elizabeth II (E7) was motivated by the death of George VI (E69). (Strong, 2005)

In First Order Logic:
- P17(x,y) ⇒ E7(x)
- P17(x,y) ⇒ E1(y)
- P17(x,y) ⇒ P15(x,y)

### was present at

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P12i_was_present_at` · `crm:P12i_was_present_at`

Quantification of the inverse property: many to many, necessary (1,n:0,n)

Scope note of the inverse property:
This property describes the active or passive presence of an E77 Persistent Item in an instance of E5 Event without implying any specific role. 
It documents known events in which an instance of E77 Persistent Item was present during the course of its life or history. For example, an object may be the desk, now in a museum, on which a treaty was signed. The instance of E53 Place and the instance of E52 Time-Span where and when these events happened provide constraints about the presence of the related instance E77 Persistent Item in the past. Instances of E90 Symbolic Object, in particular information objects, are physically present in events via at least one of the instances of E18 Physical Thing carrying them. Note, that the human mind can be such a carrier. A precondition for a transfer of information to a person or another new physical carrier is the presence of the respective information object and this person or physical thing in one event.

Examples of the inverse property:
- Deckchair 42 (E19) was present at the sinking of the Titanic (E5). (Aldridge, 2008)

In First Order Logic of the inverse property:
- P12(x,y) ⇒ E5(x)
- P12(x,y) ⇒ E77(y)

| | |
|---|---|
| Sub-properties | [Is invoked in ritual](object-properties.md#isinvokedinritual), [Participates in ritual](object-properties.md#participatesinritual) |
| Inverse of | [occurred in the presence of](object-properties.md#p12_occurred_in_the_presence_of) |

### was produced by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P108i_was_produced_by` · `crm:P108i_was_produced_by`

Quantification of the inverse property: one to many, necessary, dependent (1,n:1,1)

Scope note of the inverse property:
This property identifies the instance of E24 Physical Human-Made Thing that came into existence as a result of the instance of E12 Production.
The identity of an instance of E24 Physical Human-Made Thing is not defined by its matter, but by its existence as a subject of documentation. An E12 Production can result in the creation of multiple instances of E24 Physical Human-Made Thing.

Examples of the inverse property:
- The building of Rome (E12) has produced the Colosseum (E24). (Hopkins &amp; Beard, 2011)

In First Order Logic of the inverse property:
- P108(x,y) ⇒ E12(x)
- P108(x,y) ⇒ E24(y)
- P108(x,y) ⇒ P31(x,y)
- P108(x,y) ⇒ P92(x,y)

| | |
|---|---|
| Inverse of | [has produced](object-properties.md#p108_has_produced) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Iconographic Object](classes.md#iconographicobject) |

### wasAssociatedWith

**IRI:** `http://www.w3.org/ns/prov#wasAssociatedWith` · `prov:wasAssociatedWith`

An prov:Agent that had some (unspecified) responsibility for the occurrence of this prov:Activity.

### wasAttributedTo

**IRI:** `http://www.w3.org/ns/prov#wasAttributedTo` · `prov:wasAttributedTo`

Attribution is the ascribing of an entity to an agent.

### wasDerivedFrom

**IRI:** `http://www.w3.org/ns/prov#wasDerivedFrom` · `prov:wasDerivedFrom`

A derivation is a transformation of an entity into another, an update of an entity resulting in a new one, or the construction of a new entity based on a pre-existing entity.

### wasGeneratedBy

**IRI:** `http://www.w3.org/ns/prov#wasGeneratedBy` · `prov:wasGeneratedBy`

| | |
|---|---|
| Inverse of | [generated](object-properties.md#generated) |

### wasInfluencedBy

**IRI:** `http://www.w3.org/ns/prov#wasInfluencedBy` · `prov:wasInfluencedBy`

Because prov:wasInfluencedBy is a broad relation, its more specific subproperties (e.g. prov:wasInformedBy, prov:actedOnBehalfOf, prov:wasEndedBy, etc.) should be used when applicable.

| | |
|---|---|
| Sub-properties | [Was documented by](object-properties.md#documentedby) |

### wasInformedBy

**IRI:** `http://www.w3.org/ns/prov#wasInformedBy` · `prov:wasInformedBy`

An activity a2 is dependent on or informed by another activity a1, by way of some unspecified entity that is generated by a1 and used by a2.

### wasRevisionOf

**IRI:** `http://www.w3.org/ns/prov#wasRevisionOf` · `prov:wasRevisionOf`

A revision is a derivation that revises an entity into a revised version.

