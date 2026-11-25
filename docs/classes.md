# Classes

### Access Protocol

**IRI:** `https://cair-nepal.org/heritagegraph/AccessProtocol` · `hg:AccessProtocol`

Cultural access protocol for heritage knowledge or a record of it, to be set with the community concerned.

| | |
|---|---|
| Superclasses | [Type](classes.md#e55_type) |
| Instances | [Community Use Only](concepts.md#communityuseonly), [Initiates Only](concepts.md#initiatesonly), [Open](concepts.md#open), [Seasonal](concepts.md#seasonal), [Secret Sacred](concepts.md#secretsacred) |
| Used in | in range of [has access protocol](object-properties.md#accessprotocol) |

### Acquisition

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E8_Acquisition` · `crm:E8_Acquisition`

Scope note:
This class comprises transfers of legal ownership from one or more instances of E39 Actor to one or more other instances of E39 Actor. 
The class also applies to the establishment or loss of ownership of instances of E18 Physical Thing. It does not, however, imply changes of any other kinds of rights. The recording of the donor and/or recipient is optional. It is possible that in an instance of E8 Acquisition there is either no donor or no recipient. Depending on the circumstances, it may describe:
1. the beginning of ownership
2. the end of ownership
3. the transfer of ownership
4. the acquisition from an unknown source
5. the loss of title due to destruction of the item
It may also describe events where a collector appropriates legal title, for example, by annexation or field collection. The interpretation of the museum notion of “accession” differs between institutions. The CIDOC CRM therefore models legal ownership (E8 Acquisition) and physical custody (E10 Transfer of Custody) separately. Institutions will then model their specific notions of accession and deaccession as combinations of these.

Examples:
- the collection of a hammerhead shark, genus Sphyrna (Carchariniformes), by John Steinbeck and Edward Ricketts at Puerto Escondido in the Gulf of Mexico on 25(th) March 1940. (Steinbeck, 2000)
- the acquisition of El Greco’s “The Apostles Peter and Paul” by the State Hermitage in Saint Petersburg. (https://hermitagemuseum.org/wps/portal/hermitage/digital-collection/01.+Paintings/32730)
- the loss of my stuffed Fringilla coelebs due to insect damage last year (fictitious)

In First Order Logic:
- E8(x) ⇒ E7(x)

| | |
|---|---|
| Subclasses | [Endowment Event](classes.md#endowmentevent) |

### Activity

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E7_Activity` · `crm:E7_Activity`

Scope note:
This class comprises actions intentionally carried out by instances of E39 Actor that result in changes of state in the cultural, social, or physical systems documented. 
This notion includes complex, composite, and long-lasting actions such as the building of a settlement or a war, as well as simple, short-lived actions such as the opening of a door.

Examples:
- the Battle of Stalingrad (Hoyt, 1993)
- the Yalta Conference (Harbutt, 2010)
- my birthday celebration 28-6-1995
- the writing of “Faust” by Goethe (E65) (Williams, 2020)
- the formation of the Bauhaus 1919 (E66) (Droste, 2006)
- the people of Iraq giving the name ‘Quyunjig’ to the place identified by the TGN as ‘7017998’
- Kira Weber working in glass art from 1984 to 1993
- Kira Weber working in oil and pastel painting from 1993

In First Order Logic:
- E7(x) ⇒ E5(x)

| | |
|---|---|
| Subclasses | [Consecration](classes.md#consecration), [Documentation Activity](classes.md#documentationactivity), [Enshrinement](classes.md#enshrinement), [Ritual Event](classes.md#ritualevent) |
| Used in | used in axioms of [Tenure Event](classes.md#tenureevent) |

### Activity

**IRI:** `http://www.w3.org/ns/prov#Activity` · `prov:Activity`

An activity is something that occurs over a period of time and acts upon or with entities; it may include consuming, processing, transforming, modifying, relocating, using, or generating entities.

| | |
|---|---|
| Subclasses | [Consecration](classes.md#consecration), [Documentation Activity](classes.md#documentationactivity), [Endowment Event](classes.md#endowmentevent), [Enshrinement](classes.md#enshrinement), [Historical Event](classes.md#historicalevent), [Ritual Event](classes.md#ritualevent), [Syncretic Relationship](classes.md#syncreticrelationship) |
| Used in | used in axioms of [Heritage information object](classes.md#informationobject) |

### Actor

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E39_Actor` · `crm:E39_Actor`

Scope note:
This class comprises people, either individually or in groups, who have the potential to perform intentional actions of kinds for which they can be held responsible.

Examples:
- London and Continental Railways (E74)
- the Governor of the Bank of England in 1975 (E21)
- Sir Ian McKellen (E21) (Gibson, 1986)

In First Order Logic:
- E39(x) ⇒ E77(x)

| | |
|---|---|
| Subclasses | [Data Custodian](classes.md#datacustodian), [Group](classes.md#e74_group), [Person](classes.md#e21_person) |
| Used in | in range of [Commissioned by](object-properties.md#commissionedby); in range of [Custody holder](object-properties.md#custodyholder); in range of [Datacite publisher](object-properties.md#sourcepublisher); in range of [Endowment donor](object-properties.md#endowmentdonor); in range of [Endowment recipient](object-properties.md#endowmentrecipient); in range of [Had participant](object-properties.md#hadparticipant); in range of [Performed by group](object-properties.md#performedbygroup); in range of [Role holder](object-properties.md#roleholder); in range of [source creator](object-properties.md#sourcecreator); in range of [Tenure holder](object-properties.md#tenureholder); in range of [Used by](object-properties.md#usedby); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Consecration](classes.md#consecration); used in axioms of [Custody Period](classes.md#custodyperiod); used in axioms of [Data Source](classes.md#datasource); used in axioms of [Endowment Event](classes.md#endowmentevent); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Iconographic Object](classes.md#iconographicobject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Tenure](classes.md#tenure) |

### Age Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/AgeCriterion` · `hg:AgeCriterion`

Candidate must be within the prescribed pre-pubescent age range.

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Agent

**IRI:** `http://www.w3.org/ns/prov#Agent` · `prov:Agent`

An agent is something that bears some form of responsibility for an activity taking place, for the existence of an entity, or for another agent's activity.

| | |
|---|---|
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |

### Architectural Element

**IRI:** `https://cair-nepal.org/heritagegraph/ArchitecturalElement` · `hg:ArchitecturalElement`

Carved or constructed component of an architectural structure (e.g., Gajur, Torana, Tundal).

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity), [Physical Human-Made Thing](classes.md#e24_physical_human-made_thing) |
| Restrictions | [forms part of](object-properties.md#p46i_forms_part_of) *min* `1`; [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Physical Heritage Thing](classes.md#physicalheritagething) |

### Architectural Structure

**IRI:** `https://cair-nepal.org/heritagegraph/ArchitecturalStructure` · `hg:ArchitecturalStructure`

Physical structures built for religious, social, or civic purposes. Links to events of production, use, custody, and documentation.

| | |
|---|---|
| Superclasses | [Human-Made Object](classes.md#e22_human-made_object) |
| Restrictions | [was produced by](object-properties.md#p108i_was_produced_by) *max* `1`; [has existence status](object-properties.md#existencestatus) *only* [Existence Status](classes.md#existencestatus-2); [Has religious tradition](object-properties.md#hasreligioustradition) *only* [Religious Tradition](classes.md#religioustradition); [Hypothesized location](object-properties.md#hypothesizedlocation) *only* [Place](classes.md#e53_place); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Managed by guthi](object-properties.md#managedbyguthi) *only* [Guthi](classes.md#guthi); [has destruction event](object-properties.md#destructionevent) *max* `1`; [Last known existence date](datatype-properties.md#lastknownexistencedate) *only* [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime); [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [Has architectural style](object-properties.md#hasarchitecturalstyle) *only* [Architectural Style](classes.md#architecturalstyle-2); [has destruction event](object-properties.md#destructionevent) *only* [Destruction](classes.md#e6_destruction); [has structure type](object-properties.md#structuretype) *only* [Structure Type](classes.md#structuretype); [has current location](object-properties.md#p55_has_current_location) *only* [Place](classes.md#e53_place); [Documented in source](object-properties.md#mentionedinsource) *only* [Data Source](classes.md#datasource); [Has architectural style](object-properties.md#hasarchitecturalstyle) *max* `1`; [was assessed by](object-properties.md#p34i_was_assessed_by) *only* [Condition Assessment](classes.md#e14_condition_assessment); [was produced by](object-properties.md#p108i_was_produced_by) *only* [Production](classes.md#e12_production); [Last known existence date](datatype-properties.md#lastknownexistencedate) *max* `1`; [has existence status](object-properties.md#existencestatus) *max* `1` |
| Subclasses | [Religious Structure](classes.md#religiousstructure), [Rest House](classes.md#resthouse), [Water Structure](classes.md#waterstructure) |
| Used in | in domain of [Documented in source](object-properties.md#mentionedinsource); in domain of [Has architectural style](object-properties.md#hasarchitecturalstyle); in domain of [has destruction event](object-properties.md#destructionevent); in domain of [has existence status](object-properties.md#existencestatus); in domain of [Has religious tradition](object-properties.md#hasreligioustradition); in domain of [has structure type](object-properties.md#structuretype); in domain of [Hypothesized location](object-properties.md#hypothesizedlocation); in domain of [Last known existence date](datatype-properties.md#lastknownexistencedate); in domain of [Managed by guthi](object-properties.md#managedbyguthi); in range of [Architectural structures](object-properties.md#architecturalstructures); in range of [Residence structure](object-properties.md#residencestructure); in range of [sustains](object-properties.md#sustains); used in axioms of [Endowment](classes.md#endowment); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Physical Heritage Thing](classes.md#physicalheritagething) |

### Architectural Style

**IRI:** `https://cair-nepal.org/heritagegraph/ArchitecturalStyle` · `hg:ArchitecturalStyle`

A vocabulary of architectural styles for South Asian heritage, mapped to CIDOC E55 Type.

| | |
|---|---|
| Superclasses | [Type](classes.md#e55_type) |
| Instances | [Dome style](concepts.md#dome), [obsolete Chaitya style](concepts.md#chaitya-2), [obsolete Stupa style](concepts.md#stupa-2), [Pagoda style](concepts.md#pagoda), [Shikhara style](concepts.md#shikhara) |
| Used in | in range of [Has architectural style](object-properties.md#hasarchitecturalstyle); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Temple](classes.md#temple) |

### Archival Record

**IRI:** `https://cair-nepal.org/heritagegraph/ArchivalRecord` · `hg:ArchivalRecord`

Government or institutional administrative record.

| | |
|---|---|
| Superclasses | [Data Source](classes.md#datasource) |

### Assertion Subject

**IRI:** `https://cair-nepal.org/heritagegraph/AssertionSubject` · `hg:AssertionSubject`

Any HeritageGraph entity or event that may be the subject of an assertion.

| | |
|---|---|
| Restrictions | [Human-Made Object](classes.md#e22_human-made_object) *or* [Architectural Element](classes.md#architecturalelement) *or* [Deity](classes.md#deity) *or* [Religious Tradition](classes.md#religioustradition) *or* [Historical Event](classes.md#historicalevent) *or* [Ritual Event](classes.md#ritualevent) *or* [Production](classes.md#e12_production) *or* [Consecration](classes.md#consecration) *or* [Enshrinement](classes.md#enshrinement) *or* [Transfer of Custody](classes.md#e10_transfer_of_custody) *or* [Condition Assessment](classes.md#e14_condition_assessment) *or* [Condition State](classes.md#e3_condition_state) *or* [Actor](classes.md#e39_actor) *or* [Place](classes.md#e53_place) *or* [Time-Span](classes.md#e52_time-span) *or* [Data Source](classes.md#datasource) *or* [Documentation Activity](classes.md#documentationactivity) *or* [Syncretic Relationship](classes.md#syncreticrelationship) *or* [Kumari Tenure](classes.md#kumaritenure) *or* [Design or Procedure](classes.md#e29_design_or_procedure) *or* [Material](classes.md#e57_material) *or* [Kumari Role](classes.md#kumarirole) *or* [Selection Criterion](classes.md#selectioncriterion) *or* [Belief](classes.md#i2_belief) *or* [Calendar System](classes.md#calendarsystem) *or* [Endowment](classes.md#endowment) *or* [Endowment Event](classes.md#endowmentevent) *or* [Hereditary Role Tenure](classes.md#hereditaryroletenure) *or* [Custody Period](classes.md#custodyperiod) |
| Used in | in domain of [Has assertion](object-properties.md#hasassertion); in domain of [Was documented by](object-properties.md#documentedby); in range of [Asserts about](object-properties.md#assertsabout); in range of [Custody object](object-properties.md#custodyobject); in range of [Proposition object entity](object-properties.md#propositionobjectentity); in range of [Proposition subject](object-properties.md#propositionsubject); in range of [records](object-properties.md#documents); in range of [sustains](object-properties.md#sustains); used in axioms of [Custody Period](classes.md#custodyperiod); used in axioms of [Documentation Activity](classes.md#documentationactivity); used in axioms of [Endowment](classes.md#endowment); used in axioms of [Proposition](classes.md#proposition) |

### Attribute Assignment

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E13_Attribute_Assignment` · `crm:E13_Attribute_Assignment`

Scope note:
This class comprises the actions of making assertions about one property of an object or any single relation between two items or concepts. The type of the property asserted to hold between two items or concepts can be described by the property P177 assigned property of type (is type of property assigned): E55 Type. 
For example, the class describes the actions of people making propositions and statements during certain scientific/scholarly procedures, e.g. the person and date when a condition statement was made, an identifier was assigned, the museum object was measured, etc. Which kinds of such assignments and statements need to be documented explicitly in structures of a schema rather than free text, depends on whether this information should be accessible by structured queries.
This class allows for the documentation of how the respective assignment came about, and whose opinion it was. Note that all instances of properties described in a knowledge base are the opinion of someone. Per default, they are the opinion of the team maintaining the knowledge base. This fact must not individually be registered for all instances of properties provided by the maintaining team, because it would result in an endless recursion of whose opinion was the description of an opinion. Therefore, the use of instances of E13 Attribute Assignment marks the fact that the maintaining team is in general neutral to the validity of the respective assertion, but registers someone else’s opinion and how it came about.
All properties assigned in such an action can also be seen as directly relating the respective pair of items or concepts. Multiple use of instances of E13 Attribute Assignment may possibly lead to a collection of contradictory values.

Examples:
- the examination of MS Sinai Greek 418 by Nicholas Pickwoad in November 2003 (Honey &amp; Pickwoad, 2010)
- the assessment of the current ownership of Martin Doerr’s silver cup in February 1997 (fictitious)

In First Order Logic:
- E13(x) ⇒ E7(x)

| | |
|---|---|
| Subclasses | [Syncretic Relationship](classes.md#syncreticrelationship) |

### Belief

**IRI:** `http://www.cidoc-crm.org/extensions/crminf/I2_Belief` · `crminf:I2_Belief`

This class comprises the notion that the associated I4 Proposition Set is held to have a particular I6 Belief Value by a particular E39 Actor. This can be understood as the period of time that an individual group holds a particular set of propositions to be true, false, or somewhere in between.

| | |
|---|---|
| Used in | in domain of [Asserts about](object-properties.md#assertsabout); in domain of [Confidence method](object-properties.md#confidencemethod); in domain of [Confidence score](datatype-properties.md#confidencescore); in domain of [Data quality note](datatype-properties.md#dataqualitynote); in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Reconciliation status](datatype-properties.md#reconciliationstatus); in range of [Has assertion](object-properties.md#hasassertion); in range of [Verified assertion](object-properties.md#verifiedassertion); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Custody Period](classes.md#custodyperiod); used in axioms of [Endowment](classes.md#endowment); used in axioms of [Endowment Event](classes.md#endowmentevent); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Tenure](classes.md#tenure); used in axioms of [Verification](classes.md#verification) |

### Calendar System

**IRI:** `https://cair-nepal.org/heritagegraph/CalendarSystem` · `hg:CalendarSystem`

Calendar reckoning system with conversion rules for multi-calendar temporal reasoning.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [Year offset from gregorian](datatype-properties.md#yearoffsetfromgregorian) *only* [xsd:integer](http://www.w3.org/2001/XMLSchema#integer); [Is primary for tradition](object-properties.md#isprimaryfortradition) *only* [Religious Tradition](classes.md#religioustradition); [Epoch date gregorian](datatype-properties.md#epochdategregorian) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Epoch date gregorian](datatype-properties.md#epochdategregorian) *max* `1`; [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Year offset from gregorian](datatype-properties.md#yearoffsetfromgregorian) *max* `1` |
| Disjoint with | [Deity](classes.md#deity), [Office](classes.md#office), [Proposition](classes.md#proposition), [Religious Tradition](classes.md#religioustradition), [Selection Criterion](classes.md#selectioncriterion), [Structure Type](classes.md#structuretype) |
| Used in | in domain of [Epoch date gregorian](datatype-properties.md#epochdategregorian); in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Is primary for tradition](object-properties.md#isprimaryfortradition); in domain of [Year offset from gregorian](datatype-properties.md#yearoffsetfromgregorian); in range of [has calendar system](object-properties.md#calendarsystem); used in axioms of [Assertion Subject](classes.md#assertionsubject) |

### Caste Group

**IRI:** `https://cair-nepal.org/heritagegraph/CasteGroup` · `hg:CasteGroup`

Hereditary social group (Jati) with specific ritual roles and occupational duties.

| | |
|---|---|
| Superclasses | [Group](classes.md#e74_group) |
| Restrictions | [Traditional role](datatype-properties.md#traditionalrole) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | in domain of [Traditional role](datatype-properties.md#traditionalrole); in range of [Performed by group](object-properties.md#performedbygroup); in range of [Role holder](object-properties.md#roleholder); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Chaitya

**IRI:** `https://cair-nepal.org/heritagegraph/Chaitya` · `hg:Chaitya`

Buddhist votive shrine (chaitya); votive stupa form found across the Kathmandu Valley. In Newar usage chaitya (Newar chibhah) also names great stupas (Swayambhu Mahachaitya), so a monument may be both a Stupa and a Chaitya.

| | |
|---|---|
| Superclasses | [Religious Structure](classes.md#religiousstructure) |

### Chariot Festival

**IRI:** `https://cair-nepal.org/heritagegraph/ChariotFestival` · `hg:ChariotFestival`

Festival involving ceremonial chariot procession (e.g., Rato Machhindranath Jatra).

| | |
|---|---|
| Superclasses | [Festival](classes.md#festival) |

### Concept

**IRI:** `http://www.w3.org/2004/02/skos/core#Concept` · `skos:Concept`

| | |
|---|---|
| Instances | [Abhisheka](concepts.md#abhisheka), [Alienation of an endowment](concepts.md#alienation), [Appropriation](concepts.md#appropriation), [Augmentation of an endowment](concepts.md#augmentation), [Bhajan](concepts.md#bhajan), [Century](concepts.md#century), [Chariot Procession](concepts.md#chariotprocession), [Circa](concepts.md#circa), [Circumambulation](concepts.md#circumambulation), [Community Use Only](concepts.md#communityuseonly), [Damaged](concepts.md#damaged), [Decade](concepts.md#decade), [Deinstallation Ritual](concepts.md#deinstallationritual), [Deity guthi](concepts.md#templeguthi), [Destroyed](concepts.md#destroyed), [Dome style](concepts.md#dome), [Equivalence](concepts.md#equivalence), [Exact](concepts.md#exact), [Extant](concepts.md#extant), [Founding of an endowment](concepts.md#founding), [Fusion](concepts.md#fusion), [Good](concepts.md#good), [Historical](concepts.md#historical), [Homa](concepts.md#homa), [Hypothetical](concepts.md#hypothetical), [Initiates Only](concepts.md#initiatesonly), [Installation Ritual](concepts.md#installationritual), [Jatra](concepts.md#jatra), [Jatra Guthi](concepts.md#jatraguthi), [Kamya Puja](concepts.md#kamyapuja), [Lost](concepts.md#lost), [Masked Performance](concepts.md#maskedperformance), [Month](concepts.md#month), [Naimittika Puja](concepts.md#naimittikapuja), [Nasha Guthi](concepts.md#nashaguthi), [Nationalisation of an endowment](concepts.md#nationalisation), [Nitya Puja](concepts.md#nityapuja), [obsolete Chaitya style](concepts.md#chaitya-2), [obsolete SanGuthi](concepts.md#sanguthi), [obsolete Stupa style](concepts.md#stupa-2), [Open](concepts.md#open), [Pagoda style](concepts.md#pagoda), [Partially Extant](concepts.md#partiallyextant), [Procession Ritual](concepts.md#processionritual), [Processional Movement](concepts.md#processionalmovement), [Puja Guthi](concepts.md#pujaguthi), [Raj Guthi](concepts.md#rajguthi), [Reconstructed](concepts.md#reconstructed), [Relic Tour](concepts.md#relictour), [Restored](concepts.md#restored), [Returning Ritual](concepts.md#returningritual), [Ritual Consecration](concepts.md#ritualconsecration), [Ruined](concepts.md#ruined), [Sana Guthi](concepts.md#sanaguthi), [Seasonal](concepts.md#seasonal), [Secret Sacred](concepts.md#secretsacred), [Shikhara style](concepts.md#shikhara), [Si Guthi](concepts.md#siguthi), [Unknown](concepts.md#unknown), [Vrata](concepts.md#vrata), [Yagna](concepts.md#yagna), [Year](concepts.md#year) |

### ConceptScheme

**IRI:** `http://www.w3.org/2004/02/skos/core#ConceptScheme` · `skos:ConceptScheme`

| | |
|---|---|
| Instances | [Access Protocol (concept scheme)](concept-schemes.md#accessprotocol-2), [Architectural Style (concept scheme)](concept-schemes.md#architecturalstyle), [Condition Type (concept scheme)](concept-schemes.md#conditiontype-2), [Date Precision (concept scheme)](concept-schemes.md#dateprecision), [Endowment Event Type (concept scheme)](concept-schemes.md#endowmenteventtype), [Existence Status (concept scheme)](concept-schemes.md#existencestatus), [Guthi Type (concept scheme)](concept-schemes.md#guthitype-2), [HeritageGraph LinkML schema](concept-schemes.md#schema), [Ritual Type (concept scheme)](concept-schemes.md#ritualtype), [Syncretic Type (concept scheme)](concept-schemes.md#syncretictype-2) |

### Condition Assessment

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E14_Condition_Assessment` · `crm:E14_Condition_Assessment`

Scope note:
This class describes the act of assessing the state of preservation of an object during a particular period. 
The condition assessment may be carried out by inspection, measurement, or through historical research. This class is used to document circumstances of the respective assessment that is relevant to interpret its quality at a later stage, or to continue research on related documents.

Examples:
- last year’s inspection of humidity damage to the frescos in the St. George chapel in our village (fictitious)
- the condition assessment of the endband cores of MS Sinai Greek 418 by Nicholas Pickwoad in November 2003 (Honey &amp; Pickwoad, 2010)
- the condition assessment of the cover of MS Sinai Greek 418 by Nicholas Pickwoad in November 2003 (Honey &amp; Pickwoad, 2010)

In First Order Logic:
- E14(x) ⇒ E13(x)

| | |
|---|---|
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject) |

### Condition State

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E3_Condition_State` · `crm:E3_Condition_State`

Scope note:
This class comprises the states of objects characterised by a certain condition over a time-span. 
An instance of this class describes the prevailing physical condition of any material object or feature during a specific instance of E52 Time-Span. In general, the time-span for which a certain condition can be asserted may be shorter than the real time-span, for which this condition held.
The nature of that condition can be described using P2 has type. For example, the instance of E3 Condition State “condition of the SS Great Britain between 22(nd) September 1846 and 27(th) August 1847” can be characterized as an instance “wrecked” of E55 Type.

Examples:
- the "reconstructed" state of the “Amber Room” in Tsarskoje Selo from summer 2003 until now (Owen, 2009)
- the "ruined" state of Peterhof Palace near Saint Petersburg from 1944 to 1946 (Maddox, 2015)
- the state of my turkey in the oven at 14:30 on 25(th) December 2002 [P2 has type: E55 Type “still not cooked”] (fictitious)
- the topography of the leaves of Sinai Printed Book 3234.2361 on the 10(th) July 2007 [described as: of type "cockled"] (fictitious)

In First Order Logic:
- E3(x) ⇒ E2(x)

| | |
|---|---|
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Has condition type](object-properties.md#hasconditiontype); used in axioms of [Assertion Subject](classes.md#assertionsubject) |

### Condition Type

**IRI:** `https://cair-nepal.org/heritagegraph/ConditionType` · `hg:ConditionType`

Controlled vocabulary for the physical condition of heritage objects and structures.

| | |
|---|---|
| Superclasses | [Type](classes.md#e55_type) |
| Instances | [Damaged](concepts.md#damaged), [Good](concepts.md#good), [Restored](concepts.md#restored), [Ruined](concepts.md#ruined) |
| Used in | in range of [Has condition type](object-properties.md#hasconditiontype) |

### Consecration

**IRI:** `https://cair-nepal.org/heritagegraph/Consecration` · `hg:Consecration`

Ritual event that transforms an object into a sacred vessel (e.g., Prana Pratistha for Murti).

| | |
|---|---|
| Superclasses | [Activity](classes.md#e7_activity), [Activity](classes.md#activity), [Ritual Event](classes.md#ritualevent) |
| Restrictions | [Makes deity present](object-properties.md#makesdeitypresent) *max* `1`; [took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Makes deity present](object-properties.md#makesdeitypresent) *only* [Deity](classes.md#deity); [carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span) |
| Used in | in domain of [Makes deity present](object-properties.md#makesdeitypresent); in range of [Consecrated by event](object-properties.md#consecratedbyevent); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Murti](classes.md#murti) |

### Custody Period

**IRI:** `https://cair-nepal.org/heritagegraph/CustodyPeriod` · `hg:CustodyPeriod`

Dated period during which an actor (typically a Guthi) holds custody of a heritage structure or object, opened and closed by transfer-of-custody events. Unlike the untimed crm:P50i_is_current_keeper_of, it answers who held custody at a given date.

| | |
|---|---|
| Superclasses | [Tenure](classes.md#tenure) |
| Restrictions | [Custody holder](object-properties.md#custodyholder) *min* `1`; [Custody object](object-properties.md#custodyobject) *only* (([Physical Heritage Thing](classes.md#physicalheritagething) *or* [Human-Made Object](classes.md#e22_human-made_object)) *and* [Assertion Subject](classes.md#assertionsubject)); [Custody closed by](object-properties.md#custodyclosedby) *max* `1`; [Custody opened by](object-properties.md#custodyopenedby) *only* [Transfer of Custody](classes.md#e10_transfer_of_custody); [Custody holder](object-properties.md#custodyholder) *only* [Actor](classes.md#e39_actor); [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [Custody object](object-properties.md#custodyobject) *min* `1`; [has time-span](object-properties.md#p4_has_time-span) *min* `1`; [Custody closed by](object-properties.md#custodyclosedby) *only* [Transfer of Custody](classes.md#e10_transfer_of_custody); [Custody holder](object-properties.md#custodyholder) *max* `1`; [Custody opened by](object-properties.md#custodyopenedby) *max* `1`; [Custody object](object-properties.md#custodyobject) *max* `1` |
| Used in | in domain of [Custody closed by](object-properties.md#custodyclosedby); in domain of [Custody holder](object-properties.md#custodyholder); in domain of [Custody object](object-properties.md#custodyobject); in domain of [Custody opened by](object-properties.md#custodyopenedby); used in axioms of [Assertion Subject](classes.md#assertionsubject) |

### Data Custodian

**IRI:** `https://cair-nepal.org/heritagegraph/DataCustodian` · `hg:DataCustodian`

Institution or person currently responsible for stewarding heritage data.

| | |
|---|---|
| Superclasses | [Actor](classes.md#e39_actor) |
| Restrictions | [Custodian type](datatype-properties.md#custodiantype) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | in domain of [Custodian type](datatype-properties.md#custodiantype) |

### Data Source

**IRI:** `https://cair-nepal.org/heritagegraph/DataSource` · `hg:DataSource`

Original source from which heritage information was derived.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity), [Information Object](classes.md#e73_information_object) |
| Restrictions | [Datacite publisher](object-properties.md#sourcepublisher) *max* `1`; [Datacite identifier](datatype-properties.md#persistentidentifier) *max* `1`; [Datacite resource type](datatype-properties.md#resourcetype) *max* `1`; [Datacite publisher](object-properties.md#sourcepublisher) *only* [Actor](classes.md#e39_actor); [Source url](datatype-properties.md#sourceurl) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [inLanguage](datatype-properties.md#inlanguage) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Datacite identifier type](datatype-properties.md#identifierscheme) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Datacite identifier type](datatype-properties.md#identifierscheme) *max* `1`; [source creator](object-properties.md#sourcecreator) *only* [Actor](classes.md#e39_actor); [Source citation](datatype-properties.md#sourcecitation) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Source url](datatype-properties.md#sourceurl) *max* `1`; [Datacite resource type](datatype-properties.md#resourcetype) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Publication timespan](object-properties.md#publicationtimespan) *only* [Time-Span](classes.md#e52_time-span); [Datacite identifier](datatype-properties.md#persistentidentifier) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Publication timespan](object-properties.md#publicationtimespan) *max* `1` |
| Subclasses | [Archival Record](classes.md#archivalrecord), [Field Survey Dataset](classes.md#fieldsurveydataset), [Heritage information object](classes.md#informationobject), [Oral History Recording](classes.md#oralhistoryrecording) |
| Disjoint with | [Tenure](classes.md#tenure) |
| Used in | in domain of [Datacite identifier](datatype-properties.md#persistentidentifier); in domain of [Datacite identifier type](datatype-properties.md#identifierscheme); in domain of [Datacite publisher](object-properties.md#sourcepublisher); in domain of [Datacite resource type](datatype-properties.md#resourcetype); in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Publication timespan](object-properties.md#publicationtimespan); in domain of [Source citation](datatype-properties.md#sourcecitation); in domain of [source creator](object-properties.md#sourcecreator); in domain of [Source url](datatype-properties.md#sourceurl); in range of [Documented in source](object-properties.md#mentionedinsource); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### Date Precision

**IRI:** `https://cair-nepal.org/heritagegraph/DatePrecision` · `hg:DatePrecision`

Controlled vocabulary for the temporal precision of recorded heritage dates.

| | |
|---|---|
| Superclasses | [Type](classes.md#e55_type) |
| Instances | [Century](concepts.md#century), [Circa](concepts.md#circa), [Decade](concepts.md#decade), [Exact](concepts.md#exact), [Month](concepts.md#month), [Year](concepts.md#year) |
| Used in | in range of [has date precision](object-properties.md#dateprecision) |

### Death

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E69_Death` · `crm:E69_Death`

Scope note:
This class comprises the deaths of human beings. 
If a person is killed, their death should be instantiated as E69 Death and as E7 Activity. The death or perishing of other living beings should be documented as instances of E64 End of Existence.

Examples:
- the murder of Julius Caesar (E69, E7) (Irwin, 1935)
- the death of Senator Paul Wellstone (Monast and Tao, 2002)

In First Order Logic:
- E69(x) ⇒ E64(x)

| | |
|---|---|
| Used in | used in axioms of [Tenure Event](classes.md#tenureevent) |

### Deity

**IRI:** `https://cair-nepal.org/heritagegraph/Deity` · `hg:Deity`

Divine conceptual entity in Hindu, Buddhist, or syncretic traditions. Distinct from physical representations (Murti) and ritual presences.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Restrictions | [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Has religious tradition](object-properties.md#hasreligioustradition) *only* [Religious Tradition](classes.md#religioustradition); [Is invoked in ritual](object-properties.md#isinvokedinritual) *only* [Ritual Event](classes.md#ritualevent); [Is enshrined through event](object-properties.md#isenshrinedthroughevent) *only* [Enshrinement](classes.md#enshrinement) |
| Disjoint with | [Calendar System](classes.md#calendarsystem), [Office](classes.md#office), [Proposition](classes.md#proposition), [Religious Tradition](classes.md#religioustradition), [Selection Criterion](classes.md#selectioncriterion), [Structure Type](classes.md#structuretype) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Has religious tradition](object-properties.md#hasreligioustradition); in domain of [Is enshrined through event](object-properties.md#isenshrinedthroughevent); in domain of [Is invoked in ritual](object-properties.md#isinvokedinritual); in range of [Embodied deity](object-properties.md#embodieddeity); in range of [Enshrined deity](object-properties.md#enshrineddeity); in range of [Invokes deity](object-properties.md#invokesdeity); in range of [Is about deity](object-properties.md#isaboutdeity); in range of [Makes deity present](object-properties.md#makesdeitypresent); in range of [Role deity](object-properties.md#roledeity); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Consecration](classes.md#consecration); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Kumari Role](classes.md#kumarirole); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Murti](classes.md#murti); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Design or Procedure

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E29_Design_or_Procedure` · `crm:E29_Design_or_Procedure`

Scope note:
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
- E29(x) ⇒ E73(x)

| | |
|---|---|
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in range of [Confidence method](object-properties.md#confidencemethod); used in axioms of [Assertion Subject](classes.md#assertionsubject) |

### Destruction

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E6_Destruction` · `crm:E6_Destruction`

Scope note:
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
- E6(x) ⇒ E64(x)

| | |
|---|---|
| Used in | in domain of [Architectural structures](object-properties.md#architecturalstructures); in domain of [has access protocol](object-properties.md#accessprotocol); in range of [has destruction event](object-properties.md#destructionevent); used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### Dharmashala

**IRI:** `https://cair-nepal.org/heritagegraph/Dharmashala` · `hg:Dharmashala`

Pilgrim lodge operated by a Guthi organization.

| | |
|---|---|
| Superclasses | [Rest House](classes.md#resthouse) |

### Dhunge Dhara

**IRI:** `https://cair-nepal.org/heritagegraph/DhungeDhara` · `hg:DhungeDhara`

Stone spout (hiti) with carved imagery, used for ritual bathing and daily water supply.

| | |
|---|---|
| Superclasses | [Water Structure](classes.md#waterstructure) |

### Documentation Activity

**IRI:** `https://cair-nepal.org/heritagegraph/DocumentationActivity` · `hg:DocumentationActivity`

Activity that records information about a heritage entity or event and may generate information objects or assertions. It aligns CIDOC CRM documentation practices with prov:Activity.

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity), [Activity](classes.md#e7_activity) |
| Restrictions | [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Used equipment](datatype-properties.md#usedequipment) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [generated](object-properties.md#generated) *only* [Entity](classes.md#entity); [Used method](datatype-properties.md#usedmethod) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [wasAssociatedWith](object-properties.md#wasassociatedwith) *only* [Agent](classes.md#agent); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [records](object-properties.md#documents) *only* [Assertion Subject](classes.md#assertionsubject) |
| Subclasses | [Field Survey Activity](classes.md#fieldsurveyactivity), [Oral History Interview](classes.md#oralhistoryinterview), [Verification](classes.md#verification) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [records](object-properties.md#documents); in domain of [Used equipment](datatype-properties.md#usedequipment); in domain of [Used method](datatype-properties.md#usedmethod); in range of [Was documented by](object-properties.md#documentedby); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Heritage information object](classes.md#informationobject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship); used in axioms of [Tenure Event](classes.md#tenureevent) |

### Endowment

**IRI:** `https://cair-nepal.org/heritagegraph/Endowment` · `hg:Endowment`

Land, income or other property permanently dedicated to sustain a structure, a ritual or festival, or a sacred office, and held by a Guthi. The endowment, not the membership, is what makes a Guthi a trust.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity), [Legal Object](classes.md#e72_legal_object) |
| Restrictions | [sustains](object-properties.md#sustains) *only* (([Architectural Structure](classes.md#architecturalstructure) *or* [Ritual Event](classes.md#ritualevent) *or* [Office](classes.md#office)) *and* [Assertion Subject](classes.md#assertionsubject)); [Endowed land](object-properties.md#endowedland) *only* [Place](classes.md#e53_place); [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [right held by](object-properties.md#p105_right_held_by) *min* `1`; [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [sustains](object-properties.md#sustains) *min* `1`; [right held by](object-properties.md#p105_right_held_by) *only* [Group](classes.md#e74_group) |
| Used in | in domain of [Endowed land](object-properties.md#endowedland); in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [sustains](object-properties.md#sustains); in range of [Concerns endowment](object-properties.md#concernsendowment); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Endowment Event](classes.md#endowmentevent) |

### Endowment Event

**IRI:** `https://cair-nepal.org/heritagegraph/EndowmentEvent` · `hg:EndowmentEvent`

Event that founds, augments, nationalises or alienates a Guthi endowment, with its donor or recipient and its date.

| | |
|---|---|
| Superclasses | [Acquisition](classes.md#e8_acquisition), [Activity](classes.md#activity) |
| Restrictions | [has endowment event type](object-properties.md#endowmenteventtype) *max* `1`; [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [Concerns endowment](object-properties.md#concernsendowment) *min* `1`; [Endowment recipient](object-properties.md#endowmentrecipient) *max* `1`; [Endowment donor](object-properties.md#endowmentdonor) *only* [Actor](classes.md#e39_actor); [Concerns endowment](object-properties.md#concernsendowment) *max* `1`; [has time-span](object-properties.md#p4_has_time-span) *min* `1`; [took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [has endowment event type](object-properties.md#endowmenteventtype) *min* `1`; [has endowment event type](object-properties.md#endowmenteventtype) *only* [Endowment Event Type](classes.md#endowmenteventtype-2); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Concerns endowment](object-properties.md#concernsendowment) *only* [Endowment](classes.md#endowment); [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Endowment recipient](object-properties.md#endowmentrecipient) *only* [Actor](classes.md#e39_actor) |
| Used in | in domain of [Concerns endowment](object-properties.md#concernsendowment); in domain of [Endowment donor](object-properties.md#endowmentdonor); in domain of [Endowment recipient](object-properties.md#endowmentrecipient); in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [has endowment event type](object-properties.md#endowmenteventtype); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Tenure Event](classes.md#tenureevent) |

### Endowment Event Type

**IRI:** `https://cair-nepal.org/heritagegraph/EndowmentEventType` · `hg:EndowmentEventType`

Controlled vocabulary for events in the life of a Guthi endowment.

| | |
|---|---|
| Superclasses | [Type](classes.md#e55_type) |
| Instances | [Alienation of an endowment](concepts.md#alienation), [Augmentation of an endowment](concepts.md#augmentation), [Founding of an endowment](concepts.md#founding), [Nationalisation of an endowment](concepts.md#nationalisation) |
| Used in | in range of [has endowment event type](object-properties.md#endowmenteventtype); used in axioms of [Endowment Event](classes.md#endowmentevent) |

### Enshrinement

**IRI:** `https://cair-nepal.org/heritagegraph/Enshrinement` · `hg:Enshrinement`

Event of installing a deity's murti or symbol within a temple sanctum.

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity), [Activity](classes.md#e7_activity), [Ritual Event](classes.md#ritualevent) |
| Restrictions | [carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [Enshrined in structure](object-properties.md#enshrinedinstructure) *only* [Temple](classes.md#temple); [Enshrined in structure](object-properties.md#enshrinedinstructure) *max* `1`; [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [Enshrined deity](object-properties.md#enshrineddeity) *max* `1`; [Enshrined deity](object-properties.md#enshrineddeity) *only* [Deity](classes.md#deity) |
| Used in | in domain of [Enshrined deity](object-properties.md#enshrineddeity); in domain of [Enshrined in structure](object-properties.md#enshrinedinstructure); in range of [Enshrines deity through event](object-properties.md#enshrinesdeitythroughevent); in range of [Is enshrined through event](object-properties.md#isenshrinedthroughevent); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Deity](classes.md#deity); used in axioms of [Temple](classes.md#temple) |

### Entity

**IRI:** `http://www.w3.org/ns/prov#Entity` · `prov:Entity`

An entity is a physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary.

| | |
|---|---|
| Subclasses | [Architectural Element](classes.md#architecturalelement), [Calendar System](classes.md#calendarsystem), [Data Source](classes.md#datasource), [Deity](classes.md#deity), [Endowment](classes.md#endowment), [Office](classes.md#office), [Physical Heritage Thing](classes.md#physicalheritagething), [Proposition](classes.md#proposition), [Religious Tradition](classes.md#religioustradition), [Selection Criterion](classes.md#selectioncriterion), [Structure Type](classes.md#structuretype), [Tenure](classes.md#tenure) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |

### Event

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E5_Event` · `crm:E5_Event`

Scope note:
This class comprises distinct, delimited and coherent processes and interactions of a material nature, in cultural, social or physical systems, involving and affecting instances of E77 Persistent Item in a way characteristic of the kind of process. Typical examples are meetings, births, deaths, actions of decision taking, making or inventing things, but also more complex and extended ones such as conferences, elections, building of a castle, or battles.
While the continuous growth of a tree lacks the limits characteristic of an event, its germination from a seed does qualify as an event. Similarly, the blowing of the wind lacks the distinctness and limits of an event, but a hurricane, flood or earthquake would qualify as an event. Mental processes are considered as events, in cases where they are connected with the material externalization of their results; for example, the creation of a poem, a performance or a change of intention that becomes obvious from subsequent actions or declarations.
The effects of an instance of E5 Event may not lead to relevant permanent changes of properties or relations of the items involved in it, for example an unrecorded performance. Of course, in order to be documented, some kind of evidence for an event must exist, be it witnesses, traces or products of the event.
While instances of E4 Period always require some form of coherence between its constituent phenomena, in addition, the essential constituents of instances of E5 Event should contribute to an overall effect; for example, the statements made during a meeting and the listening of the audience.
Viewed at a coarse level of detail, an instance of E5 Event may appear as if it had an ‘instantaneous’ overall effect, but any process or interaction of material nature in reality have an extent in time and space. At a fine level, instances of E5 Event may be analysed into component phenomena and phases within a space and timeframe, and as such can be seen as a period, regardless of the size of the phenomena. The reverse is not necessarily the case: not all instances of E4 Period give rise to a noteworthy overall effect and are thus not instances of E5 Event.

Examples:
- the birth of Cleopatra (E67) (Pomeroy, 1984)
- the destruction of Herculaneum by volcanic eruption in 79 AD (E6) (Camardo, 2013)
- World War II (E7) (Barber, 1994)
- the Battle of Stalingrad (E7) (Hoyt, 1993)
- the Yalta Conference (E7) (Harbutt, 2010)
- my birthday celebration 28-6-1995 (E7)
- the falling of a tile from my roof last Sunday (fictitious)
- the CIDOC conference 2003 (E7)

In First Order Logic:
- E5(x) ⇒ E4(x)

| | |
|---|---|
| Subclasses | [Historical Event](classes.md#historicalevent) |

### Existence Status

**IRI:** `https://cair-nepal.org/heritagegraph/ExistenceStatus` · `hg:ExistenceStatus`

Controlled vocabulary for whether a heritage structure still exists physically.

| | |
|---|---|
| Superclasses | [Type](classes.md#e55_type) |
| Instances | [Destroyed](concepts.md#destroyed), [Extant](concepts.md#extant), [Hypothetical](concepts.md#hypothetical), [Lost](concepts.md#lost), [Partially Extant](concepts.md#partiallyextant), [Reconstructed](concepts.md#reconstructed), [Unknown](concepts.md#unknown) |
| Used in | in range of [has existence status](object-properties.md#existencestatus); used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### Fearlessness Assessment

**IRI:** `https://cair-nepal.org/heritagegraph/FearlessnessAssessment` · `hg:FearlessnessAssessment`

The 'fearlessness test' popularly described (animal heads, masked dancers in darkness). Its historical and contemporary practice is DISPUTED -- some former Kumaris contest how it is described. Represented as an assessment whose accounts are source-attributed via hg:hasAssertion, NOT as a mandatory criterion.

| | |
|---|---|
| Superclasses | [Ritual Assessment](classes.md#ritualassessment) |

### Festival

**IRI:** `https://cair-nepal.org/heritagegraph/Festival` · `hg:Festival`

Large-scale community ritual event (Jatra) involving processions, music, and collective participation.

| | |
|---|---|
| Superclasses | [Ritual Event](classes.md#ritualevent) |
| Subclasses | [Chariot Festival](classes.md#chariotfestival) |

### Field Survey Activity

**IRI:** `https://cair-nepal.org/heritagegraph/FieldSurveyActivity` · `hg:FieldSurveyActivity`

The activity of measuring, photographing, or assessing a site in person.

| | |
|---|---|
| Superclasses | [Documentation Activity](classes.md#documentationactivity) |

### Field Survey Dataset

**IRI:** `https://cair-nepal.org/heritagegraph/FieldSurveyDataset` · `hg:FieldSurveyDataset`

The structured data or report resulting from a field survey.

| | |
|---|---|
| Superclasses | [Data Source](classes.md#datasource) |

### Group

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E74_Group` · `crm:E74_Group`

Scope note:
This class comprises any gatherings or organizations of human individuals or groups that act collectively or in a similar way due to any form of unifying relationship. In the wider sense this class also comprises official positions which used to be regarded in certain contexts as one actor, independent of the current holder of the office, such as the president of a country. In such cases, it may happen that the group never had more than one member. A joint pseudonym (i.e. a name that seems indicative of an individual but that is actually used as a persona by two or more people) is a particular case of E74 Group.
A gathering of people becomes an instance of E74 Group when it exhibits organizational characteristics usually typified by a set of ideas or beliefs held in common, or actions performed together. These might be communication, creating some common artifact, a common purpose such as study, worship, business, sports, etc. Nationality can be modelled as membership in an instance of E74 Group. Married couples and other concepts of family are regarded as particular examples of E74 Group.

Examples:
- the Impressionists (Wilson, 1994)
- the Navajo (Correll, 1972)
- the Greeks (Williams, 1993)
- the peace protestors in New York City on 15(th) February 2003
- Exxon-Mobil (Raymond, 2006)
- King Solomon and his wives (Thieberger, 1947)
- the President of the Swiss Confederation
- Nicolas Bourbaki [the collective pseudonym of a group of mathematicians, predominantly French alumni of the École normale supérieure] (Aczel, 2007)
- Betty Crocker (Crocker, 2012)
- Ellery Queen [Ellery Queen is a pseudonym created in 1929 by American crime fiction writers Frederic Dannay and Manfred Bennington Lee.] (Wheat, 2005)
- Greenpeace
- Paveprime Ltd
- the National Museum of Denmark

In First Order Logic:
- E74(x) ⇒ E39(x)

| | |
|---|---|
| Superclasses | [Actor](classes.md#e39_actor) |
| Subclasses | [Caste Group](classes.md#castegroup), [Guthi](classes.md#guthi), [State Heritage Authority](classes.md#stateheritageauthority) |
| Used in | in range of [Mandated by](object-properties.md#mandatedby); in range of [Supported by institution](object-properties.md#supportedbyinstitution); used in axioms of [Endowment](classes.md#endowment); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Guthi

**IRI:** `https://cair-nepal.org/heritagegraph/Guthi` · `hg:Guthi`

Endowed trust organization unique to Nepal, managing temples, rituals, and land through hereditary or voluntary membership.

| | |
|---|---|
| Superclasses | [Group](classes.md#e74_group) |
| Restrictions | [has current or former member](object-properties.md#p107_has_current_or_former_member) *only* [Person](classes.md#e21_person); [has guthi type](object-properties.md#guthitype) *only* [Guthi Type](classes.md#guthitype); [has guthi type](object-properties.md#guthitype) *max* `1`; [Performs ritual](object-properties.md#performsritual) *only* [Ritual Event](classes.md#ritualevent); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | in domain of [has guthi type](object-properties.md#guthitype); in domain of [Performs ritual](object-properties.md#performsritual); in range of [Managed by guthi](object-properties.md#managedbyguthi); in range of [Performed by group](object-properties.md#performedbygroup); in range of [Transferred to guthi](object-properties.md#transferredtoguthi); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Guthi Type

**IRI:** `https://cair-nepal.org/heritagegraph/GuthiType` · `hg:GuthiType`

Controlled vocabulary of Guthi functional types (CRM E55_Type).

| | |
|---|---|
| Superclasses | [Type](classes.md#e55_type) |
| Instances | [Deity guthi](concepts.md#templeguthi), [Jatra Guthi](concepts.md#jatraguthi), [Nasha Guthi](concepts.md#nashaguthi), [obsolete SanGuthi](concepts.md#sanguthi), [Puja Guthi](concepts.md#pujaguthi), [Raj Guthi](concepts.md#rajguthi), [Sana Guthi](concepts.md#sanaguthi), [Si Guthi](concepts.md#siguthi) |
| Used in | in range of [has guthi type](object-properties.md#guthitype); used in axioms of [Guthi](classes.md#guthi) |

### Hereditary Role Tenure

**IRI:** `https://cair-nepal.org/heritagegraph/HereditaryRoleTenure` · `hg:HereditaryRoleTenure`

Time-bounded holding of a hereditary ritual duty by a person or caste group, under the mandate of a Guthi, with the rule by which the duty passes on. The same period pattern as KumariTenure, applied to hereditary offices (priests, chariot builders, musicians).

| | |
|---|---|
| Superclasses | [Tenure](classes.md#tenure) |
| Restrictions | [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Role duty](datatype-properties.md#roleduty) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Role holder](object-properties.md#roleholder) *max* `1`; [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [succeeds](object-properties.md#succeeds) *max* `1`; [Succession rule](datatype-properties.md#successionrule) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Role holder](object-properties.md#roleholder) *min* `1`; [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [Role holder](object-properties.md#roleholder) *only* (([Person](classes.md#e21_person) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor)); [Mandated by](object-properties.md#mandatedby) *only* [Group](classes.md#e74_group); [Tenure opened by](object-properties.md#tenureopenedby) *only* [Tenure Event](classes.md#tenureevent); [Mandated by](object-properties.md#mandatedby) *max* `1`; [Duty for](object-properties.md#dutyfor) *only* [Ritual Event](classes.md#ritualevent); [succeeds](object-properties.md#succeeds) *only* [Hereditary Role Tenure](classes.md#hereditaryroletenure); [Role duty](datatype-properties.md#roleduty) *min* `1`; [Tenure closed by](object-properties.md#tenureclosedby) *only* [Tenure Event](classes.md#tenureevent); [Tenure office](object-properties.md#tenureoffice) *max* `1`; [Tenure office](object-properties.md#tenureoffice) *only* [Ritual Office](classes.md#ritualoffice) |
| Used in | in domain of [Duty for](object-properties.md#dutyfor); in domain of [Mandated by](object-properties.md#mandatedby); in domain of [Role duty](datatype-properties.md#roleduty); in domain of [Role holder](object-properties.md#roleholder); in domain of [succeeds](object-properties.md#succeeds); in domain of [Succession rule](datatype-properties.md#successionrule); in range of [succeeds](object-properties.md#succeeds); used in axioms of [Assertion Subject](classes.md#assertionsubject) |

### Heritage information object

**IRI:** `https://cair-nepal.org/heritagegraph/InformationObject` · `hg:InformationObject`

A recorded piece of information about heritage.

| | |
|---|---|
| Superclasses | [Data Source](classes.md#datasource) |
| Restrictions | [wasGeneratedBy](object-properties.md#wasgeneratedby) *only* [Activity](classes.md#activity); [inLanguage](datatype-properties.md#inlanguage) *only* [xsd:string](http://www.w3.org/2001/XMLSchema#string); [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity) |

### Historical Event

**IRI:** `https://cair-nepal.org/heritagegraph/HistoricalEvent` · `hg:HistoricalEvent`

Major event affecting heritage structures or ritual life (earthquake, epidemic, political transition, fire, flood).

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity), [Event](classes.md#e5_event) |
| Restrictions | [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Architectural structures](object-properties.md#architecturalstructures) *only* [Architectural Structure](classes.md#architecturalstructure); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | in domain of [Architectural structures](object-properties.md#architecturalstructures); in domain of [has access protocol](object-properties.md#accessprotocol); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Tenure Event](classes.md#tenureevent) |

### Horoscope Compatibility Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/HoroscopeCompatibilityCriterion` · `hg:HoroscopeCompatibilityCriterion`

Candidate's horoscope must be compatible with the city and ruling authority.

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Human-Made Object

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E22_Human-Made_Object` · `crm:E22_Human-Made_Object`

Scope note:
This class comprises all persistent physical objects of any size that are purposely created by human activity and have physical boundaries that separate them completely in an objective way from other objects. 
The class also includes all aggregates of objects made for functional purposes of whatever kind, independent of physical coherence, such as a set of chessmen.

Examples:
- the Rosetta Stone (E22)
- LNER Class A4 4468 Mallard [the World’s fastest steam locomotive, preserved at the National Railway Museum of York, UK] (Solomon, 2003)
- the Portland Vase (Walker, 2004)

In First Order Logic:
- E22(x) ⇒ E19(x)
- E22(x) ⇒ E24(x)

| | |
|---|---|
| Subclasses | [Architectural Structure](classes.md#architecturalstructure), [Iconographic Object](classes.md#iconographicobject) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Participates in ritual](object-properties.md#participatesinritual); in range of [Custody object](object-properties.md#custodyobject); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Custody Period](classes.md#custodyperiod) |

### Iconographic Object

**IRI:** `https://cair-nepal.org/heritagegraph/IconographicObject` · `hg:IconographicObject`

Sacred visual art objects that depict or embody deities through iconographic conventions.

| | |
|---|---|
| Superclasses | [Human-Made Object](classes.md#e22_human-made_object) |
| Restrictions | [Used by](object-properties.md#usedby) *only* [Actor](classes.md#e39_actor); [was produced by](object-properties.md#p108i_was_produced_by) *max* `1`; [Participates in ritual](object-properties.md#participatesinritual) *only* [Ritual Event](classes.md#ritualevent); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [has current location](object-properties.md#p55_has_current_location) *only* [Place](classes.md#e53_place); [was produced by](object-properties.md#p108i_was_produced_by) *only* [Production](classes.md#e12_production) |
| Subclasses | [Murti](classes.md#murti), [Paubha](classes.md#paubha) |
| Used in | in domain of [Used by](object-properties.md#usedby); used in axioms of [Physical Heritage Thing](classes.md#physicalheritagething) |

### Information Object

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E73_Information_Object` · `crm:E73_Information_Object`

Scope note:
This class comprises identifiable immaterial items, such as poems, jokes, data sets, images, texts, multimedia objects, procedural prescriptions, computer program code, algorithm or mathematical formulae, that have an objectively recognizable structure and are documented as single units. The encoding structure known as a “named graph” also falls under this class, so that each “named graph” is an instance of E73 Information Object.
An instance of E73 Information Object does not depend on a specific physical carrier, which can include human memory, and it can exist on one or more carriers simultaneously.
Instances of E73 Information Object of a linguistic nature should be declared as instances of the E33 Linguistic Object subclass. Instances of E73 Information Object of a documentary nature should be declared as instances of the E31 Document subclass. Conceptual items such as types and classes are not instances of E73 Information Object, nor are ideas without a reproducible expression.

Examples:
- image BM000038850.JPG from the Clayton Herbarium in London (E31) (Natural History Museum, 2021)
- E. A. Poe's “The Raven” (Poe, 1869)
- the movie “The Seven Samurai” by Akira Kurosawa (Mellen, 2002)
- the text of Huray describing the Maxwell Equations (Huray, 2010)
- the Getty AAT as published as Linked Open Data, accessed 1/10/2014

In First Order Logic:
- E73(x) ⇒ E89(x)
- E73(x) ⇒ E90(x)

| | |
|---|---|
| Subclasses | [Data Source](classes.md#datasource) |

### Kumari Enthronement Event

**IRI:** `https://cair-nepal.org/heritagegraph/KumariEnthronementEvent` · `hg:KumariEnthronementEvent`

Ritual installing a selected girl into the Kumari role and residence, activating the tenure (distinct from selection, which chooses her, and retirement, which ends it).

| | |
|---|---|
| Superclasses | [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |
| Restrictions | [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [Bounds tenure](object-properties.md#boundstenure) *min* `1`; [Confers role](object-properties.md#confersrole) *min* `1`; [Confers role](object-properties.md#confersrole) *max* `1`; [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [Enthroned person](object-properties.md#enthronedperson) *max* `1`; [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [Enthroned person](object-properties.md#enthronedperson) *min* `1`; [took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [Bounds tenure](object-properties.md#boundstenure) *max* `1`; [Bounds tenure](object-properties.md#boundstenure) *only* [Kumari Tenure](classes.md#kumaritenure); [carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Enthroned person](object-properties.md#enthronedperson) *only* [Person](classes.md#e21_person); [Confers role](object-properties.md#confersrole) *only* [Kumari Role](classes.md#kumarirole) |
| Used in | in domain of [Confers role](object-properties.md#confersrole); in domain of [Enthroned person](object-properties.md#enthronedperson); in range of [Enthroned through](object-properties.md#enthronedthrough); used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Kumari House

**IRI:** `https://cair-nepal.org/heritagegraph/KumariHouse` · `hg:KumariHouse`

God-house residence of a Kumari during tenure (e.g., Kumari Ghar, Kathmandu). Specialised ReligiousStructure.

| | |
|---|---|
| Superclasses | [Religious Structure](classes.md#religiousstructure) |

### Kumari Lifecycle Event

**IRI:** `https://cair-nepal.org/heritagegraph/KumariLifecycleEvent` · `hg:KumariLifecycleEvent`

Abstract event that bounds a KumariTenure (selection, enthronement, or retirement). Each concrete subclass requires exactly one tenure edge via slot_usage: hg:initiatedTenure (selection), hg:endedTenureOf (retirement), or hg:boundsTenure itself (enthronement).

| | |
|---|---|
| Superclasses | [Ritual Event](classes.md#ritualevent) |
| Restrictions | [Bounds tenure](object-properties.md#boundstenure) *max* `1`; [Bounds tenure](object-properties.md#boundstenure) *only* [Kumari Tenure](classes.md#kumaritenure) |
| Subclasses | [Kumari Enthronement Event](classes.md#kumarienthronementevent), [Kumari Retirement Event](classes.md#kumariretirementevent), [Kumari Selection Event](classes.md#kumariselectionevent) |
| Used in | in domain of [Bounds tenure](object-properties.md#boundstenure) |

### Kumari Retirement Event

**IRI:** `https://cair-nepal.org/heritagegraph/KumariRetirementEvent` · `hg:KumariRetirementEvent`

Ritual or administrative event that formally ends a Living Goddess tenure according to tradition, returning the person to secular life. Record the event and its date, not the reason: the traditional grounds concern the bodily state of a child, and HeritageGraph does not record health or bodily data about persons.

| | |
|---|---|
| Superclasses | [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |
| Restrictions | [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Performed by group](object-properties.md#performedbygroup) *only* (([Guthi](classes.md#guthi) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor)); [Ended tenure of](object-properties.md#endedtenureof) *min* `1`; [carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Ended tenure of](object-properties.md#endedtenureof) *max* `1`; [took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [has time-span](object-properties.md#p4_has_time-span) *min* `1`; [Ended tenure of](object-properties.md#endedtenureof) *only* [Kumari Tenure](classes.md#kumaritenure); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span) |
| Used in | in domain of [Ended tenure of](object-properties.md#endedtenureof); in range of [Retired through](object-properties.md#retiredthrough); used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Kumari Role

**IRI:** `https://cair-nepal.org/heritagegraph/KumariRole` · `hg:KumariRole`

The role/office of Kumari (living-goddess embodiment) that a person assumes for the duration of a KumariTenure. The role is the type; the tenure is the time-bounded holding of it; the person is the holder.

| | |
|---|---|
| Superclasses | [Ritual Office](classes.md#ritualoffice) |
| Restrictions | [Role deity](object-properties.md#roledeity) *max* `1`; [Role deity](object-properties.md#roledeity) *only* [Deity](classes.md#deity) |
| Used in | in domain of [Role deity](object-properties.md#roledeity); in range of [Assumes role](object-properties.md#assumesrole); in range of [Confers role](object-properties.md#confersrole); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure) |

### Kumari Selection Event

**IRI:** `https://cair-nepal.org/heritagegraph/KumariSelectionEvent` · `hg:KumariSelectionEvent`

Tantric ritual process of selecting a new Living Goddess from eligible candidates. Involves examination of 32 auspicious physical marks (lakshana) and horoscope matching with the city and ruling authority, carried out, in published accounts, by the priests of Taleju and the Buddhist Vajracharya priests with an astrologer. Accounts of a fearlessness test are disputed and are recorded as such with FearlessnessAssessment, not stated here.

| | |
|---|---|
| Superclasses | [Kumari Lifecycle Event](classes.md#kumarilifecycleevent) |
| Restrictions | [Selected person](object-properties.md#selectedperson) *min* `1`; [Is critical for festival](datatype-properties.md#iscriticalforfestival) *max* `1`; [Confers role](object-properties.md#confersrole) *max* `1`; [Confers role](object-properties.md#confersrole) *only* [Kumari Role](classes.md#kumarirole); [Selected person](object-properties.md#selectedperson) *max* `1`; [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Selected person](object-properties.md#selectedperson) *only* [Person](classes.md#e21_person); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [Initiated tenure](object-properties.md#initiatedtenure) *min* `1`; [carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [Initiated tenure](object-properties.md#initiatedtenure) *max* `1`; [took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [Performed by group](object-properties.md#performedbygroup) *only* (([Guthi](classes.md#guthi) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor)); [Initiated tenure](object-properties.md#initiatedtenure) *only* [Kumari Tenure](classes.md#kumaritenure); [Is critical for festival](datatype-properties.md#iscriticalforfestival) *only* [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean); [Has criterion](object-properties.md#hascriterion) *only* [Selection Criterion](classes.md#selectioncriterion); [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity) |
| Used in | in domain of [Confers role](object-properties.md#confersrole); in domain of [Has criterion](object-properties.md#hascriterion); in domain of [Initiated tenure](object-properties.md#initiatedtenure); in domain of [Is critical for festival](datatype-properties.md#iscriticalforfestival); in domain of [Selected person](object-properties.md#selectedperson); in range of [Part of selection](object-properties.md#partofselection); in range of [Selected through](object-properties.md#selectedthrough); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment) |

### Kumari Tenure

**IRI:** `https://cair-nepal.org/heritagegraph/KumariTenure` · `hg:KumariTenure`

Time-bounded role where a person embodies a deity as Living Goddess (Kumari), residing at a specific god-house and supported by religious institutions. This class captures the unique Nepali tradition of living deity embodiment in young girls selected from Buddhist Shakya/Vajracharya families.

| | |
|---|---|
| Superclasses | [Tenure](classes.md#tenure) |
| Restrictions | [Selected through](object-properties.md#selectedthrough) *max* `1`; [Embodied deity](object-properties.md#embodieddeity) *min* `1`; [has time-span](object-properties.md#p4_has_time-span) *min* `1`; [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Selected through](object-properties.md#selectedthrough) *only* [Kumari Selection Event](classes.md#kumariselectionevent); [Had participant](object-properties.md#hadparticipant) *only* [Actor](classes.md#e39_actor); [Tenure holder](object-properties.md#tenureholder) *max* `1`; [Enthroned through](object-properties.md#enthronedthrough) *max* `1`; [Retired through](object-properties.md#retiredthrough) *only* [Kumari Retirement Event](classes.md#kumariretirementevent); [Enthroned through](object-properties.md#enthronedthrough) *only* [Kumari Enthronement Event](classes.md#kumarienthronementevent); [Residence structure](object-properties.md#residencestructure) *min* `1`; [Embodied deity](object-properties.md#embodieddeity) *only* [Deity](classes.md#deity); [Residence structure](object-properties.md#residencestructure) *max* `1`; [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [Tenure holder](object-properties.md#tenureholder) *only* [Person](classes.md#e21_person); [Retired through](object-properties.md#retiredthrough) *max* `1`; [Tenure holder](object-properties.md#tenureholder) *min* `1`; [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [Supported by institution](object-properties.md#supportedbyinstitution) *only* [Group](classes.md#e74_group); [Assumes role](object-properties.md#assumesrole) *only* [Kumari Role](classes.md#kumarirole); [Residence structure](object-properties.md#residencestructure) *only* [Architectural Structure](classes.md#architecturalstructure); [Assumes role](object-properties.md#assumesrole) *max* `1`; [Embodied deity](object-properties.md#embodieddeity) *max* `1` |
| Used in | in domain of [Assumes role](object-properties.md#assumesrole); in domain of [Embodied deity](object-properties.md#embodieddeity); in domain of [Enthroned through](object-properties.md#enthronedthrough); in domain of [Had participant](object-properties.md#hadparticipant); in domain of [Residence structure](object-properties.md#residencestructure); in domain of [Retired through](object-properties.md#retiredthrough); in domain of [Selected through](object-properties.md#selectedthrough); in domain of [Supported by institution](object-properties.md#supportedbyinstitution); in range of [Bounds tenure](object-properties.md#boundstenure); in range of [Ended tenure of](object-properties.md#endedtenureof); in range of [Initiated tenure](object-properties.md#initiatedtenure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Lifecycle Event](classes.md#kumarilifecycleevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |

### Legal Object

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E72_Legal_Object` · `crm:E72_Legal_Object`

Scope note:
This class comprises those material or immaterial items to which instances of E30 Right, such as the right of ownership or use, can be applied. 
This is generally true for all instances of E18 Physical Thing. In the case of instances of E28 Conceptual Object, however, the identity of an instance of E28 Conceptual Object or the method of its use may be too ambiguous to reliably establish instances of E30 Right, as in the case of taxa and inspirations. Ownership of corporations is currently regarded as out of scope of the CIDOC CRM.

Examples:
- the Cullinan diamond (E19) (Scarratt and Shor, 2006)
- definition of the CIDOC Conceptual Reference Model Version 5.0.4 (E73) (ISO 21127: 2014)

In First Order Logic:
- E72(x) ⇒ E70(x)

| | |
|---|---|
| Subclasses | [Endowment](classes.md#endowment) |

### Lineage Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/LineageCriterion` · `hg:LineageCriterion`

Candidate must belong to an eligible lineage (Shakya / Vajracharya Newar Buddhist family).

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Masked Dance

**IRI:** `https://cair-nepal.org/heritagegraph/MaskedDance` · `hg:MaskedDance`

Performance in which masked dancers embody deities (e.g. Kartik Naach); usually part of a festival (crm:P9 forms part of), not itself a festival.

| | |
|---|---|
| Superclasses | [Ritual Event](classes.md#ritualevent) |

### Material

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E57_Material` · `crm:E57_Material`

Scope note:
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
- E57(x) ⇒ E55(x)

| | |
|---|---|
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Murti

**IRI:** `https://cair-nepal.org/heritagegraph/Murti` · `hg:Murti`

Consecrated image or seat of a deity, figural or aniconic (e.g. a stone, a linga, a pitha), ritually activated to serve as divine presence (not merely depiction).

| | |
|---|---|
| Superclasses | [Iconographic Object](classes.md#iconographicobject) |
| Restrictions | [Is about deity](object-properties.md#isaboutdeity) *max* `1`; [Is about deity](object-properties.md#isaboutdeity) *only* [Deity](classes.md#deity); [Consecrated by event](object-properties.md#consecratedbyevent) *max* `1`; [Consecrated by event](object-properties.md#consecratedbyevent) *only* [Consecration](classes.md#consecration) |
| Used in | in domain of [Consecrated by event](object-properties.md#consecratedbyevent); in domain of [Is about deity](object-properties.md#isaboutdeity) |

### obsolete Container ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/Container` · `hg:Container`

Root container for cultural heritage data instances. PLACEMENT RULE: put each instance in the most specific collection available (e.g. a Festival in festivals, not ritual_events; a Person in persons, not actors); broader collections exist for instances of the general classes only.

### obsolete Metadata ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/Metadata` · `hg:Metadata`

Dataset metadata information.

### Office

**IRI:** `https://cair-nepal.org/heritagegraph/Office` · `hg:Office`

An office, role or duty that persons or groups hold for a period (a CIDOC-CRM E55 Type): the office is the type, a Tenure is the dated holding of it, the holder is the actor.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity), [Type](classes.md#e55_type) |
| Restrictions | [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Subclasses | [Ritual Office](classes.md#ritualoffice) |
| Disjoint with | [Calendar System](classes.md#calendarsystem), [Deity](classes.md#deity), [Proposition](classes.md#proposition), [Religious Tradition](classes.md#religioustradition), [Selection Criterion](classes.md#selectioncriterion), [Structure Type](classes.md#structuretype) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in range of [sustains](object-properties.md#sustains); in range of [Tenure office](object-properties.md#tenureoffice); used in axioms of [Endowment](classes.md#endowment); used in axioms of [Tenure](classes.md#tenure) |

### Oral History Interview

**IRI:** `https://cair-nepal.org/heritagegraph/OralHistoryInterview` · `hg:OralHistoryInterview`

The interaction event between a researcher and a knowledge holder.

| | |
|---|---|
| Superclasses | [Documentation Activity](classes.md#documentationactivity) |

### Oral History Recording

**IRI:** `https://cair-nepal.org/heritagegraph/OralHistoryRecording` · `hg:OralHistoryRecording`

The recording or transcript of an oral history interview.

| | |
|---|---|
| Superclasses | [Data Source](classes.md#datasource) |

### Pati

**IRI:** `https://cair-nepal.org/heritagegraph/Pati` · `hg:Pati`

Open-air pavilion for resting travelers.

| | |
|---|---|
| Superclasses | [Rest House](classes.md#resthouse) |

### Paubha

**IRI:** `https://cair-nepal.org/heritagegraph/Paubha` · `hg:Paubha`

Traditional Newari scroll painting (thangka) with mandala and deity iconography.

| | |
|---|---|
| Superclasses | [Iconographic Object](classes.md#iconographicobject) |

### Period

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E4_Period` · `crm:E4_Period`

Scope note:
This class comprises sets of coherent phenomena or cultural manifestations occurring in time and space.
It is the social or physical coherence of these phenomena that identify an instance of E4 Period and not the associated spatiotemporal extent. This extent is only the “ground” or space in an abstract physical sense that the actual process of growth, spread and retreat has covered. Consequently, different periods can overlap and coexist in time and space, such as when a nomadic culture exists in the same area and time as a sedentary culture. This also means that overlapping land use rights, common among first nations, amounts to overlapping periods.
Often, this class is used to describe prehistoric or historic periods such as the “Neolithic Period”, the “Ming Dynasty” or the “McCarthy Era”, but also geopolitical units and activities of settlements are regarded as special cases of E4 Period. However, there are no assumptions about the scale of the associated phenomena. In particular all events are seen as synthetic processes consisting of coherent phenomena. Therefore, E4 Period is a superclass of E5 Event. For example, a modern clinical birth, an instance of E67 Birth, can be seen as both a single event, i.e. an instance of E5 Event, and as an extended period, i.e. an instance of E4 Period, that consists of multiple physical processes and complementary activities performed by multiple instances of E39 Actor.
E4 Period is a subclass of E2 Temporal Entity and of E92 Spacetime Volume. The latter is intended as a phenomenal spacetime volume as defined in CIDOC CRMgeo (Doerr &amp; Hiebel, 2013). By virtue of this multiple inheritance, it is possible to discuss the physical extent of an instance of E4 Period without representing each instance of it together with an instance of its associated spacetime volume. This model combines two quite different kinds of substance: an instance of E4 Period is a phenomenon while an instance of E92 Spacetime Volume is an aggregation of points in spacetime. However, the real spatiotemporal extent of an instance of E4 Period is regarded to be unique to it due to all its details and fuzziness; its identity and existence depends uniquely on the identity of the instance of E4 Period. Therefore, this multiple inheritance is unambiguous and effective and furthermore corresponds to the intuitions of natural language.
Typical use of this class in cultural heritage documentation is for documenting cultural and artistic periods. There are two different conceptualisations of ‘artistic style’, defined either by physical features or by historical context. For example, “Impressionism” can be viewed as a period in the European sphere of influence lasting from approximately 1870 to 1905 during which paintings with particular characteristics were produced by a group of artists that included (among others) Monet, Renoir, Pissarro, Sisley and Degas. Alternatively, it can be regarded as a style applicable to all paintings sharing the characteristics of the works produced by the Impressionist painters, regardless of historical context. The first interpretation is an instance of E4 Period, and the second defines morphological object types that fall under E55 Type.
A geopolitical unit as a specific case of an instance of E4 Period is the set of activities and phenomena related to the claim of power, the consequences of belonging to a jurisdictional area and an administrative system that establishes a geopolitical unit. Examples from the modern period are countries or administrative areas of countries such as districts whose actions and structures define activities and phenomena in the area that they intend to govern. The borders of geopolitical units are often defined in contracts or treaties although they may deviate from the actual practice. The spatiotemporal properties of Geopolitical units can be modelled through the properties inherited from E92 Spacetime Volume.
Another specific case of an instance of E4 Period is the actual extent of the set of activities and phenomena as evidenced by their physical traces that define a settlement, such as the populated period of Nineveh.

Examples:
- Jurassic (Hallam, 1975)
- Populated Period of Nineveh
- Imperial Rome under Marcus Aurelius
- European Bronze Age (Harrison, 2004) 
- Italian Renaissance (Macdonald, 1992)
- Thirty Years War (Lee, 1991)
- Sturm und Drang (Berkoff, 2013)
- Cubism (Cox, 2000)
- The Capital of Russia (E4) [the capital of Russia in the sense of an administrative unit moved in historical times from Moscow to St Petersburg and then back to Moscow. This exemplifies an administrative unit changing place over time without temporal discontinuity]
- The settling activity of the community of Helsinki (a.k.a. Helsingfors) (E7) [the original settlement called Helsinki was located in the area of the modern airport. The community moved later to settle on the coast. This exemplifies a continued activity changing place over time without temporal discontinuity]
- Bronze Age (E4) [Bronze Age, in the sense of technological adoption, spread over disjoint areas including islands such as the British Isles without temporal discontinuity]
- Japan, the state (E4) [In 2021, the Japanese state as a political unit comprised in 6852 islands extending along the Pacific coast of Asia]

In First Order Logic:
- E4(x) ⇒ E2(x)
- E4(x) ⇒ E92(x)

| | |
|---|---|
| Subclasses | [Tenure](classes.md#tenure) |

### Person

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E21_Person` · `crm:E21_Person`

Scope note:
This class comprises real persons who live or are assumed to have lived. 
Legendary figures that may have existed, such as Ulysses and King Arthur, fall into this class if the documentation refers to them as historical figures. In cases where doubt exists as to whether several persons are in fact identical, multiple instances can be created and linked to indicate their relationship. The CIDOC CRM does not propose a specific form to support reasoning about possible identity.
In a bibliographic context, a name presented following the conventions usually employed for personal names will be assumed to correspond to an actual real person (an instance of E21 Person), unless evidence is available to indicate that this is not the case. The fact that a persona may erroneously be classified as an instance of E21 Person does not imply that the concept comprises personae.

Examples:
- Tut-Ankh-Amun (Edwards and Boltin, 1979)
- Nelson Mandela (Brown and Hort, 2006)

In First Order Logic:
- E21(x) ⇒ E20(x)
- E21(x) ⇒ E39(x)

| | |
|---|---|
| Superclasses | [Actor](classes.md#e39_actor) |
| Used in | in domain of [Birth timespan](object-properties.md#birthtimespan); in domain of [Death timespan](object-properties.md#deathtimespan); in domain of [Expertise area](datatype-properties.md#expertisearea); in domain of [Institutional affiliation](datatype-properties.md#institutionalaffiliation); in range of [Assesses candidate](object-properties.md#assessescandidate); in range of [Enthroned person](object-properties.md#enthronedperson); in range of [Role holder](object-properties.md#roleholder); in range of [Selected person](object-properties.md#selectedperson); in range of [Verified by expert](object-properties.md#verifiedbyexpert); used in axioms of [Guthi](classes.md#guthi); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Verification](classes.md#verification) |

### Physical Heritage Thing

**IRI:** `https://cair-nepal.org/heritagegraph/PhysicalHeritageThing` · `hg:PhysicalHeritageThing`

Union of the tangible heritage classes: architectural structures, iconographic objects, and standalone architectural elements. Used as the range of slots that apply to any physical heritage thing (production, custody, condition assessment).

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity) |
| Equivalent to | [Architectural Structure](classes.md#architecturalstructure) *or* [Iconographic Object](classes.md#iconographicobject) *or* [Architectural Element](classes.md#architecturalelement) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in range of [Custody object](object-properties.md#custodyobject); used in axioms of [Custody Period](classes.md#custodyperiod) |

### Physical Human-Made Thing

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E24_Physical_Human-Made_Thing` · `crm:E24_Physical_Human-Made_Thing`

Scope note:
This class comprises all persistent physical items of any size that are purposely created by human activity. This class comprises, besides others, human-made objects, such as a sword, and human-made features, such as rock art. For example, a “cup and ring” carving on bedrock is regarded as instance of E24 Physical Human-Made Thing.
Instances of E24 Physical Human-Made Thing may be the result of modifying pre-existing physical things, preserving larger parts or most of the original matter and structure, which poses the question if they are new or even human-made, the respective interventions of production made on such original material should be obvious and sufficient to regard that the product has a new, distinct identity and intended function and is human-made. Substantial continuity of the previous matter and structure in the new product can be documented by describing the production process also as an instance of E81 Transformation.
Whereas interventions of conservation and repair are not regarded to produce a new instance of E24 Physical Human-Made Thing, the results of preparation of natural history specimens that substantially change their natural or original state should be regarded as instances of E24 Physical Human-Made Things, including the uncovering of petrified biological features from a solid piece of stone. On the other side, scribbling a museum number on a natural object should not be regarded to make it human-made. This notwithstanding, parts, sections, segments, or features of an instance of E24 Physical Human-Made Thing may continue to be non-human-made and preserved during the production process, for example natural pearls used as a part of an eardrop.

Examples:
- the Forth Railway Bridge (Shipway, Bouch, Baker and Fowler, 1990).
- the Channel Tunnel (E25) (Holliday, Marcou and Vickerman, 1991)
- the Palace of Knossos (Evans, 1921)
- the Colosseum in Rome, Italy (Hopkins and Beard, 2011)
- the Historical Collection of the Museum Benaki in Athens (E78) (Georgoula, 2005)
- the Rosetta Stone (E22)
- my paperback copy of Crime &amp; Punishment (E22) (fictitious)
- the computer disk at ICS-FORTH that stores the canonical Definition of the CIDOC CRM v.3.2 (E22)
- my empty DVD disk (E22) (fictitious)

In First Order Logic:
- E24(x) ⇒ E18(x)
- E24(x) ⇒ E71(x)

| | |
|---|---|
| Subclasses | [Architectural Element](classes.md#architecturalelement) |

### Physical Integrity Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/PhysicalIntegrityCriterion` · `hg:PhysicalIntegrityCriterion`

The traditional requirement of physical integrity in a candidate. HeritageGraph records that the criterion belongs to the selection, not any assessment of a candidate's body or health.

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Place

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E53_Place` · `crm:E53_Place`

Scope note:
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
- E53(x) ⇒ E1(x)

| | |
|---|---|
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Place type](datatype-properties.md#placetype); in range of [End place](object-properties.md#endplace); in range of [Endowed land](object-properties.md#endowedland); in range of [Hypothesized location](object-properties.md#hypothesizedlocation); in range of [Route places](object-properties.md#routeplaces); in range of [Start place](object-properties.md#startplace); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Consecration](classes.md#consecration); used in axioms of [Endowment](classes.md#endowment); used in axioms of [Endowment Event](classes.md#endowmentevent); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Iconographic Object](classes.md#iconographicobject); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Pokhari

**IRI:** `https://cair-nepal.org/heritagegraph/Pokhari` · `hg:Pokhari`

Pond or tank for water storage, ritual bathing, and ecological management.

| | |
|---|---|
| Superclasses | [Water Structure](classes.md#waterstructure) |

### Production

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E12_Production` · `crm:E12_Production`

Scope note:
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
- E12(x) ⇒ E63(x)

| | |
|---|---|
| Used in | in domain of [Commissioned by](object-properties.md#commissionedby); in domain of [has access protocol](object-properties.md#accessprotocol); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Iconographic Object](classes.md#iconographicobject) |

### Proposition

**IRI:** `https://cair-nepal.org/heritagegraph/Proposition` · `hg:Proposition`

A single machine-readable proposition (subject - predicate - object) held true by an Assertion. Modelled as a singleton proposition set (CRMinf I4); the predicate is a URI/CURIE, the object either a heritage entity or a literal.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity), [Proposition Set](classes.md#i4_proposition_set) |
| Restrictions | [Proposition predicate](datatype-properties.md#propositionpredicate) *max* `1`; [Proposition predicate](datatype-properties.md#propositionpredicate) *min* `1`; [Proposition predicate](datatype-properties.md#propositionpredicate) *only* [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI); [Proposition object literal](datatype-properties.md#propositionliteralvalue) *only* [rdfs:Literal](http://www.w3.org/2000/01/rdf-schema#Literal); [Proposition object literal](datatype-properties.md#propositionliteralvalue) *max* `1`; [Proposition object entity](object-properties.md#propositionobjectentity) *max* `1`; [Proposition subject](object-properties.md#propositionsubject) *max* `1`; [Proposition object entity](object-properties.md#propositionobjectentity) *only* [Assertion Subject](classes.md#assertionsubject); [Proposition subject](object-properties.md#propositionsubject) *min* `1`; [Proposition subject](object-properties.md#propositionsubject) *only* [Assertion Subject](classes.md#assertionsubject) |
| Disjoint with | [Calendar System](classes.md#calendarsystem), [Deity](classes.md#deity), [Office](classes.md#office), [Religious Tradition](classes.md#religioustradition), [Selection Criterion](classes.md#selectioncriterion), [Structure Type](classes.md#structuretype) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Proposition object entity](object-properties.md#propositionobjectentity); in domain of [Proposition object literal](datatype-properties.md#propositionliteralvalue); in domain of [Proposition predicate](datatype-properties.md#propositionpredicate); in domain of [Proposition subject](object-properties.md#propositionsubject) |

### Proposition Set

**IRI:** `http://www.cidoc-crm.org/extensions/crminf/I4_Proposition_Set` · `crminf:I4_Proposition_Set`

This class comprises the sets of formal, binary propositions that an I2 Belief is held about. It could be implemented as a named graph, a spreadsheet, or any other structured dataset. Regardless of the specific syntax employed, the effective propositions it contains should be made up of unambiguous identifiers, concepts of a formal ontology, and constructs of logic.

| | |
|---|---|
| Subclasses | [Proposition](classes.md#proposition) |

### Religious Structure

**IRI:** `https://cair-nepal.org/heritagegraph/ReligiousStructure` · `hg:ReligiousStructure`

Architectural structure whose defining purpose is religious: enshrines a deity and/or is a locus of ritual activation. Abstract grouping for sacred structures across traditions (temple, stupa, chaitya).

| | |
|---|---|
| Superclasses | [Architectural Structure](classes.md#architecturalstructure) |
| Subclasses | [Chaitya](classes.md#chaitya), [Kumari House](classes.md#kumarihouse), [Stupa](classes.md#stupa), [Temple](classes.md#temple) |

### Religious Tradition

**IRI:** `https://cair-nepal.org/heritagegraph/ReligiousTradition` · `hg:ReligiousTradition`

Religious or philosophical tradition (e.g., Hindu, Buddhist, Syncretic).

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity), [Type](classes.md#e55_type) |
| Restrictions | [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Disjoint with | [Calendar System](classes.md#calendarsystem), [Deity](classes.md#deity), [Office](classes.md#office), [Proposition](classes.md#proposition), [Selection Criterion](classes.md#selectioncriterion), [Structure Type](classes.md#structuretype) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in range of [Has religious tradition](object-properties.md#hasreligioustradition); in range of [Is primary for tradition](object-properties.md#isprimaryfortradition); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Calendar System](classes.md#calendarsystem); used in axioms of [Deity](classes.md#deity) |

### Rest House

**IRI:** `https://cair-nepal.org/heritagegraph/RestHouse` · `hg:RestHouse`

Community structures for travelers and pilgrims, maintained by Guthi organizations.

| | |
|---|---|
| Superclasses | [Architectural Structure](classes.md#architecturalstructure) |
| Subclasses | [Dharmashala](classes.md#dharmashala), [Pati](classes.md#pati), [Sattal](classes.md#sattal) |

### Ritual Assessment

**IRI:** `https://cair-nepal.org/heritagegraph/RitualAssessment` · `hg:RitualAssessment`

A performed assessment carried out during Kumari selection. Modelled as an event (not a hard criterion) so that source-specific, possibly conflicting accounts of whether/how it was conducted attach as provenanced Assertions rather than being asserted as fact.

| | |
|---|---|
| Superclasses | [Ritual Event](classes.md#ritualevent) |
| Restrictions | [carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Part of selection](object-properties.md#partofselection) *max* `1`; [Assesses candidate](object-properties.md#assessescandidate) *only* [Person](classes.md#e21_person); [Part of selection](object-properties.md#partofselection) *only* [Kumari Selection Event](classes.md#kumariselectionevent); [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [Assesses candidate](object-properties.md#assessescandidate) *max* `1`; [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief) |
| Subclasses | [Fearlessness Assessment](classes.md#fearlessnessassessment) |
| Used in | in domain of [Assesses candidate](object-properties.md#assessescandidate); in domain of [Part of selection](object-properties.md#partofselection) |

### Ritual Event

**IRI:** `https://cair-nepal.org/heritagegraph/RitualEvent` · `hg:RitualEvent`

Intentional ritual activity that activates sacred space, invokes deities, and binds social groups. An instance is one dated occurrence (one CIDOC-CRM E7 with at most one time-span), e.g. the Indra Jatra of 2025; the recurring practice it belongs to (annual, by lunar date) is described by hg:recurrencePattern and hg:lunarDateTithi, not by the instance's time-span.

| | |
|---|---|
| Superclasses | [Activity](classes.md#e7_activity), [Activity](classes.md#activity) |
| Restrictions | [Lunar date tithi](datatype-properties.md#lunardatetithi) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [Recurrence pattern](datatype-properties.md#recurrencepattern) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Had participant](object-properties.md#hadparticipant) *only* [Actor](classes.md#e39_actor); [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [End place](object-properties.md#endplace) *only* [Place](classes.md#e53_place); [Performed by group](object-properties.md#performedbygroup) *only* (([Guthi](classes.md#guthi) *or* [Caste Group](classes.md#castegroup)) *and* [Actor](classes.md#e39_actor)); [used object of type](object-properties.md#p125_used_object_of_type) *only* [Material](classes.md#e57_material); [took place at](object-properties.md#p7_took_place_at) *only* [Place](classes.md#e53_place); [End place](object-properties.md#endplace) *max* `1`; [Invokes deity](object-properties.md#invokesdeity) *only* [Deity](classes.md#deity); [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [Start place](object-properties.md#startplace) *max* `1`; [has ritual type](object-properties.md#ritualtype) *max* `1`; [Start place](object-properties.md#startplace) *only* [Place](classes.md#e53_place); [Route description](datatype-properties.md#routedescription) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Managed by guthi](object-properties.md#managedbyguthi) *only* [Guthi](classes.md#guthi); [carried out by](object-properties.md#p14_carried_out_by) *only* [Actor](classes.md#e39_actor); [has ritual type](object-properties.md#ritualtype) *only* [Ritual Type](classes.md#ritualtype-2); [Route places](object-properties.md#routeplaces) *only* [Place](classes.md#e53_place); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Subclasses | [Consecration](classes.md#consecration), [Enshrinement](classes.md#enshrinement), [Festival](classes.md#festival), [Kumari Lifecycle Event](classes.md#kumarilifecycleevent), [Masked Dance](classes.md#maskeddance), [Ritual Assessment](classes.md#ritualassessment) |
| Used in | in domain of [End place](object-properties.md#endplace); in domain of [Had participant](object-properties.md#hadparticipant); in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [has ritual type](object-properties.md#ritualtype); in domain of [Invokes deity](object-properties.md#invokesdeity); in domain of [Lunar date tithi](datatype-properties.md#lunardatetithi); in domain of [Managed by guthi](object-properties.md#managedbyguthi); in domain of [Performed by group](object-properties.md#performedbygroup); in domain of [Recurrence pattern](datatype-properties.md#recurrencepattern); in domain of [Route description](datatype-properties.md#routedescription); in domain of [Route places](object-properties.md#routeplaces); in domain of [Start place](object-properties.md#startplace); in range of [Duty for](object-properties.md#dutyfor); in range of [Is invoked in ritual](object-properties.md#isinvokedinritual); in range of [Participates in ritual](object-properties.md#participatesinritual); in range of [Performs ritual](object-properties.md#performsritual); in range of [sustains](object-properties.md#sustains); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Deity](classes.md#deity); used in axioms of [Endowment](classes.md#endowment); used in axioms of [Guthi](classes.md#guthi); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Iconographic Object](classes.md#iconographicobject); used in axioms of [Tenure Event](classes.md#tenureevent) |

### Ritual Office

**IRI:** `https://cair-nepal.org/heritagegraph/RitualOffice` · `hg:RitualOffice`

A ritual office or specialist role (e.g. Vajracharya or Rajopadhyaya priest, Karmacharya, chariot builder, festival musician, the Kumari), held by a person or a caste group, often hereditarily.

| | |
|---|---|
| Superclasses | [Office](classes.md#office) |
| Subclasses | [Kumari Role](classes.md#kumarirole) |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure) |

### Ritual Type

**IRI:** `https://cair-nepal.org/heritagegraph/RitualType` · `hg:RitualType`

Controlled vocabulary of ritual and festival activity types in Kathmandu Valley living heritage.

| | |
|---|---|
| Superclasses | [Type](classes.md#e55_type) |
| Instances | [Abhisheka](concepts.md#abhisheka), [Bhajan](concepts.md#bhajan), [Chariot Procession](concepts.md#chariotprocession), [Circumambulation](concepts.md#circumambulation), [Deinstallation Ritual](concepts.md#deinstallationritual), [Homa](concepts.md#homa), [Installation Ritual](concepts.md#installationritual), [Jatra](concepts.md#jatra), [Kamya Puja](concepts.md#kamyapuja), [Masked Performance](concepts.md#maskedperformance), [Naimittika Puja](concepts.md#naimittikapuja), [Nitya Puja](concepts.md#nityapuja), [Procession Ritual](concepts.md#processionritual), [Processional Movement](concepts.md#processionalmovement), [Relic Tour](concepts.md#relictour), [Returning Ritual](concepts.md#returningritual), [Ritual Consecration](concepts.md#ritualconsecration), [Vrata](concepts.md#vrata), [Yagna](concepts.md#yagna) |
| Used in | in range of [has ritual type](object-properties.md#ritualtype); used in axioms of [Ritual Event](classes.md#ritualevent) |

### Sattal

**IRI:** `https://cair-nepal.org/heritagegraph/Sattal` · `hg:Sattal`

Multi-story rest house (3-5 floors) with ritual and social functions.

| | |
|---|---|
| Superclasses | [Rest House](classes.md#resthouse) |

### Selection Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/SelectionCriterion` · `hg:SelectionCriterion`

An eligibility criterion a candidate must satisfy to assume the Kumari role. Modelled as explicit subclasses so 'what are the eligibility criteria?' is a subclass query, not free text. Ethics: candidates are children. Criteria describe the tradition; data about how a named or identifiable child met them (bodily marks, health, horoscope) must not be recorded.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity), [Type](classes.md#e55_type) |
| Subclasses | [Age Criterion](classes.md#agecriterion), [Horoscope Compatibility Criterion](classes.md#horoscopecompatibilitycriterion), [Lineage Criterion](classes.md#lineagecriterion), [Physical Integrity Criterion](classes.md#physicalintegritycriterion), [Thirty Two Perfections Criterion](classes.md#thirtytwoperfectionscriterion) |
| Disjoint with | [Calendar System](classes.md#calendarsystem), [Deity](classes.md#deity), [Office](classes.md#office), [Proposition](classes.md#proposition), [Religious Tradition](classes.md#religioustradition), [Structure Type](classes.md#structuretype) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in range of [Has criterion](object-properties.md#hascriterion); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |

### State Heritage Authority

**IRI:** `https://cair-nepal.org/heritagegraph/StateHeritageAuthority` · `hg:StateHeritageAuthority`

A state body with responsibility for heritage (a CIDOC-CRM E74 Group), e.g. the Guthi Sansthan (Guthi Corporation, a public corporation that administers nationalised guthi land) or the Department of Archaeology.

| | |
|---|---|
| Superclasses | [Group](classes.md#e74_group) |

### Structure Type

**IRI:** `https://cair-nepal.org/heritagegraph/StructureType` · `hg:StructureType`

A type of heritage structure from a controlled vocabulary or a community's own term list (a CIDOC-CRM E55 Type), e.g. the Newar bahah or bahi (Buddhist monastic courtyard), dyochhen (god-house), agam chhen (esoteric shrine house) or pitha (seat of a goddess). Link each term to AAT or Wikidata with SKOS mappings where an equivalent exists; local types need no new ontology class.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity), [Type](classes.md#e55_type) |
| Restrictions | [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Disjoint with | [Calendar System](classes.md#calendarsystem), [Deity](classes.md#deity), [Office](classes.md#office), [Proposition](classes.md#proposition), [Religious Tradition](classes.md#religioustradition), [Selection Criterion](classes.md#selectioncriterion) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in range of [has structure type](object-properties.md#structuretype); used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### Stupa

**IRI:** `https://cair-nepal.org/heritagegraph/Stupa` · `hg:Stupa`

Buddhist dome-shaped reliquary shrine with circumambulation and ritual activation (e.g., Boudhanath, Swayambhunath).

| | |
|---|---|
| Superclasses | [Religious Structure](classes.md#religiousstructure) |

### Syncretic Relationship

**IRI:** `https://cair-nepal.org/heritagegraph/SyncreticRelationship` · `hg:SyncreticRelationship`

The act of identifying one deity with another across theological frameworks (a CIDOC-CRM E13 Attribute Assignment: P140 the deity identified, P141 the deity it is identified with), recorded with the source that reports it (hg:mentionedInSource).

| | |
|---|---|
| Superclasses | [Activity](classes.md#activity), [Attribute Assignment](classes.md#e13_attribute_assignment) |
| Restrictions | [has syncretic type](object-properties.md#syncretictype) *max* `1`; [assigned attribute to](object-properties.md#p140_assigned_attribute_to) *min* `1`; [has syncretic type](object-properties.md#syncretictype) *only* [Syncretic Type](classes.md#syncretictype); [Was documented by](object-properties.md#documentedby) *only* [Documentation Activity](classes.md#documentationactivity); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [assigned](object-properties.md#p141_assigned) *min* `1`; [Documented in source](object-properties.md#mentionedinsource) *only* [Data Source](classes.md#datasource) |
| Used in | in domain of [Documented in source](object-properties.md#mentionedinsource); in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [has syncretic type](object-properties.md#syncretictype); used in axioms of [Assertion Subject](classes.md#assertionsubject) |

### Syncretic Type

**IRI:** `https://cair-nepal.org/heritagegraph/SyncreticType` · `hg:SyncreticType`

Controlled vocabulary for kinds of syncretic theological relationships between deities.

| | |
|---|---|
| Superclasses | [Type](classes.md#e55_type) |
| Instances | [Appropriation](concepts.md#appropriation), [Equivalence](concepts.md#equivalence), [Fusion](concepts.md#fusion), [Historical](concepts.md#historical) |
| Used in | in range of [has syncretic type](object-properties.md#syncretictype); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship) |

### Temple

**IRI:** `https://cair-nepal.org/heritagegraph/Temple` · `hg:Temple`

Religious structure characterized by deity enshrinement and ritual activation. Legal designation (e.g. 'Ancient Monument' under Nepal law) is recorded per-instance via a governance assertion, not as a class criterion.

| | |
|---|---|
| Superclasses | [Religious Structure](classes.md#religiousstructure) |
| Restrictions | [Enshrines deity through event](object-properties.md#enshrinesdeitythroughevent) *only* [Enshrinement](classes.md#enshrinement); [Has architectural style](object-properties.md#hasarchitecturalstyle) *only* [Architectural Style](classes.md#architecturalstyle-2); [Has architectural style](object-properties.md#hasarchitecturalstyle) *max* `1` |
| Used in | in domain of [Enshrines deity through event](object-properties.md#enshrinesdeitythroughevent); in range of [Enshrined in structure](object-properties.md#enshrinedinstructure); used in axioms of [Enshrinement](classes.md#enshrinement) |

### Tenure

**IRI:** `https://cair-nepal.org/heritagegraph/Tenure` · `hg:Tenure`

A dated period during which an actor holds an office, a duty or custody of something (a CIDOC-CRM E4 Period), with the events that open and close it. KumariTenure, HereditaryRoleTenure and CustodyPeriod are specialisations; the pattern applies to offices and custody beyond Nepal.

| | |
|---|---|
| Superclasses | [Entity](classes.md#entity), [Period](classes.md#e4_period) |
| Restrictions | [Tenure office](object-properties.md#tenureoffice) *max* `1`; [Tenure office](object-properties.md#tenureoffice) *only* [Office](classes.md#office); [has time-span](object-properties.md#p4_has_time-span) *only* [Time-Span](classes.md#e52_time-span); [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Tenure opened by](object-properties.md#tenureopenedby) *only* [Tenure Event](classes.md#tenureevent); [has time-span](object-properties.md#p4_has_time-span) *max* `1`; [Tenure holder](object-properties.md#tenureholder) *only* [Actor](classes.md#e39_actor); [Has assertion](object-properties.md#hasassertion) *only* [Belief](classes.md#i2_belief); [Tenure closed by](object-properties.md#tenureclosedby) *only* [Tenure Event](classes.md#tenureevent); [Tenure holder](object-properties.md#tenureholder) *max* `1` |
| Subclasses | [Custody Period](classes.md#custodyperiod), [Hereditary Role Tenure](classes.md#hereditaryroletenure), [Kumari Tenure](classes.md#kumaritenure) |
| Disjoint with | [Data Source](classes.md#datasource) |
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Tenure closed by](object-properties.md#tenureclosedby); in domain of [Tenure holder](object-properties.md#tenureholder); in domain of [Tenure office](object-properties.md#tenureoffice); in domain of [Tenure opened by](object-properties.md#tenureopenedby) |

### Tenure Event

**IRI:** `https://cair-nepal.org/heritagegraph/TenureEvent` · `hg:TenureEvent`

An event that opens or closes a Tenure: a ritual (an enthronement, a retirement), a transfer of custody, an endowment event, a documentation or historical event, any other activity, or a death.

| | |
|---|---|
| Restrictions | [Ritual Event](classes.md#ritualevent) *or* [Historical Event](classes.md#historicalevent) *or* [Transfer of Custody](classes.md#e10_transfer_of_custody) *or* [Endowment Event](classes.md#endowmentevent) *or* [Documentation Activity](classes.md#documentationactivity) *or* [Activity](classes.md#e7_activity) *or* [Death](classes.md#e69_death) |
| Used in | in range of [Tenure closed by](object-properties.md#tenureclosedby); in range of [Tenure opened by](object-properties.md#tenureopenedby); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Tenure](classes.md#tenure) |

### Thirty Two Perfections Criterion

**IRI:** `https://cair-nepal.org/heritagegraph/ThirtyTwoPerfectionsCriterion` · `hg:ThirtyTwoPerfectionsCriterion`

The battis lakshana, the traditional list of thirty-two auspicious marks a candidate is held to bear. HeritageGraph records that the criterion belongs to the selection, not any assessment of a candidate.

| | |
|---|---|
| Superclasses | [Selection Criterion](classes.md#selectioncriterion) |

### Time-Span

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E52_Time-Span` · `crm:E52_Time-Span`

Scope note:
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
- E52(x) ⇒ E1(x)

| | |
|---|---|
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [has calendar system](object-properties.md#calendarsystem); in domain of [has date precision](object-properties.md#dateprecision); in domain of [Recorded date](datatype-properties.md#recordeddate); in range of [Birth timespan](object-properties.md#birthtimespan); in range of [Death timespan](object-properties.md#deathtimespan); in range of [Publication timespan](object-properties.md#publicationtimespan); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Consecration](classes.md#consecration); used in axioms of [Custody Period](classes.md#custodyperiod); used in axioms of [Data Source](classes.md#datasource); used in axioms of [Documentation Activity](classes.md#documentationactivity); used in axioms of [Endowment Event](classes.md#endowmentevent); used in axioms of [Enshrinement](classes.md#enshrinement); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Kumari Enthronement Event](classes.md#kumarienthronementevent); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent); used in axioms of [Kumari Tenure](classes.md#kumaritenure); used in axioms of [Ritual Assessment](classes.md#ritualassessment); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Tenure](classes.md#tenure) |

### Transfer of Custody

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E10_Transfer_of_Custody` · `crm:E10_Transfer_of_Custody`

Scope note:
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
- E10(x) ⇒ E7(x)

| | |
|---|---|
| Used in | in domain of [has access protocol](object-properties.md#accessprotocol); in domain of [Transferred to guthi](object-properties.md#transferredtoguthi); in range of [Custody closed by](object-properties.md#custodyclosedby); in range of [Custody opened by](object-properties.md#custodyopenedby); used in axioms of [Assertion Subject](classes.md#assertionsubject); used in axioms of [Custody Period](classes.md#custodyperiod); used in axioms of [Tenure Event](classes.md#tenureevent) |

### Type

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/E55_Type` · `crm:E55_Type`

Scope note:
This class comprises concepts denoted by terms from thesauri and controlled vocabularies used to characterize and classify instances of CIDOC CRM classes. Instances of E55 Type represent concepts, in contrast to instances of E41 Appellation which are used to name instances of CIDOC CRM classes. 
E55 Type provides an interface to domain specific ontologies and thesauri. These can be represented in the CIDOC CRM as subclasses of E55 Type, forming hierarchies of terms, i.e. instances of E55 Type linked via P127 has broader term (has narrower term): E55 Type. Such hierarchies may be extended with additional properties.

Examples:
- weight, length, depth [types for instances of E54 Dimension]
- portrait, sketch, animation [types for instances of E36 Visual Item]
- French, English, German [types for instances of E56 Language]
- excellent, good, poor [types for instances of E3 Condition State]
- Ford Model T, chop stick [types for instances of E22 Human-Made Object]
- cave, doline, scratch [types for instances of E26 Physical Feature]
- poem, short story [types for instances of E33 Linguistic Object]
- wedding, earthquake, skirmish [types for instances of E5 Event]

In First Order Logic:
- E55(x) ⇒ E28(x)

| | |
|---|---|
| Subclasses | [Access Protocol](classes.md#accessprotocol), [Architectural Style](classes.md#architecturalstyle-2), [Condition Type](classes.md#conditiontype), [Date Precision](classes.md#dateprecision-2), [Endowment Event Type](classes.md#endowmenteventtype-2), [Existence Status](classes.md#existencestatus-2), [Guthi Type](classes.md#guthitype), [Office](classes.md#office), [Religious Tradition](classes.md#religioustradition), [Ritual Type](classes.md#ritualtype-2), [Selection Criterion](classes.md#selectioncriterion), [Structure Type](classes.md#structuretype), [Syncretic Type](classes.md#syncretictype) |

### Verification

**IRI:** `https://cair-nepal.org/heritagegraph/Verification` · `hg:Verification`

Process of cross-checking heritage claims against multiple sources.

| | |
|---|---|
| Superclasses | [Documentation Activity](classes.md#documentationactivity) |
| Restrictions | [has note](datatype-properties.md#p3_has_note) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Verification method](datatype-properties.md#verificationmethod) *only* [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral); [Verified assertion](object-properties.md#verifiedassertion) *only* [Belief](classes.md#i2_belief); [Verified by expert](object-properties.md#verifiedbyexpert) *only* [Person](classes.md#e21_person) |
| Used in | in domain of [Verification method](datatype-properties.md#verificationmethod); in domain of [Verified assertion](object-properties.md#verifiedassertion); in domain of [Verified by expert](object-properties.md#verifiedbyexpert) |

### Water Structure

**IRI:** `https://cair-nepal.org/heritagegraph/WaterStructure` · `hg:WaterStructure`

Engineered water supply systems with ritual and civic significance.

| | |
|---|---|
| Superclasses | [Architectural Structure](classes.md#architecturalstructure) |
| Subclasses | [Dhunge Dhara](classes.md#dhungedhara), [Pokhari](classes.md#pokhari) |

