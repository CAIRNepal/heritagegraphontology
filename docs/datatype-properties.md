# Datatype properties

### begin of the begin

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P82a_begin_of_the_begin` · `crm:P82a_begin_of_the_begin`

### Confidence score

**IRI:** `https://cair-nepal.org/heritagegraph/confidenceScore` · `hg:confidenceScore`

Degree of belief, between 0 and 1, that the asserted value is correct: 1 = certain, 0.5 = undecided, 0 = believed false. The assessor is either the agent the assertion is attributed to (prov:wasAttributedTo) or the activity that generated the assertion (prov:wasGeneratedBy), e.g. an extraction that codes how firmly the source states the claim; hg:confidenceMethod says which, and by what rubric. Scores are comparable only when they share an assessor or a method.

| | |
|---|---|
| Domain | [Belief](classes.md#i2_belief) |
| Range | [xsd:decimal](http://www.w3.org/2001/XMLSchema#decimal)[*>=* `0.0`, *<=* `1.0`] |

### Custodian type

**IRI:** `https://cair-nepal.org/heritagegraph/custodianType` · `hg:custodianType`

Type of custodian (government, academic, community), free text.

| | |
|---|---|
| Domain | [Data Custodian](classes.md#datacustodian) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Data Custodian](classes.md#datacustodian) |
| domainIncludes | hg:DataCustodian |

### Data quality note

**IRI:** `https://cair-nepal.org/heritagegraph/dataQualityNote` · `hg:dataQualityNote`

Notes on data quality, completeness, or uncertainty.

| | |
|---|---|
| Domain | [Belief](classes.md#i2_belief) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |

### Datacite identifier

**IRI:** `https://cair-nepal.org/heritagegraph/persistentIdentifier` · `hg:persistentIdentifier`

Persistent identifier for the source (DOI, archive ID, catalog number).

| | |
|---|---|
| Domain | [Data Source](classes.md#datasource) |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |
| domainIncludes | hg:DataSource |

### Datacite identifier type

**IRI:** `https://cair-nepal.org/heritagegraph/identifierScheme` · `hg:identifierScheme`

Type of identifier (DOI, ISBN, Handle, LocalArchiveID).

| | |
|---|---|
| Domain | [Data Source](classes.md#datasource) |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |
| domainIncludes | hg:DataSource |

### Datacite resource type

**IRI:** `https://cair-nepal.org/heritagegraph/resourceType` · `hg:resourceType`

High-level DataCite resource type (Dataset, Text, Image, Audio, Interview).

| | |
|---|---|
| Domain | [Data Source](classes.md#datasource) |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |
| domainIncludes | hg:DataSource |

### end of the end

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P82b_end_of_the_end` · `crm:P82b_end_of_the_end`

### endedAtTime

**IRI:** `http://www.w3.org/ns/prov#endedAtTime` · `prov:endedAtTime`

The time at which an activity ended. See also prov:startedAtTime.

### Epoch date gregorian

**IRI:** `https://cair-nepal.org/heritagegraph/epochDateGregorian` · `hg:epochDateGregorian`

Proleptic Gregorian (ISO 8601, astronomical year numbering) date on which the era began, in the era's own reckoning (Bikram Sambat counts from year 1, e.g. -0056-04-14, a nominal back-projection of the modern solar reckoning rather than an attested date; Nepal Sambat counts elapsed years from year 0, 0879-10-24 = 20 October 879 Julian). Its month and day only indicate the approximate new-year season: the actual new year varies (Bikram Sambat 13-15 April, solar; Nepal Sambat late October to November, lunisolar), so it must not be used for day-level conversion. A value ending in -01-01 marks a calendar whose new year is 1 January, for which year conversion is exact.

| | |
|---|---|
| Domain | [Calendar System](classes.md#calendarsystem) |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Calendar System](classes.md#calendarsystem) |
| domainIncludes | hg:CalendarSystem |

### Expertise area

**IRI:** `https://cair-nepal.org/heritagegraph/expertiseArea` · `hg:expertiseArea`

Areas of expertise (e.g., Licchavi inscriptions, Sanskrit epigraphy, Newari archaeology).

| | |
|---|---|
| Domain | [Person](classes.md#e21_person) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |

### generatedAtTime

**IRI:** `http://www.w3.org/ns/prov#generatedAtTime` · `prov:generatedAtTime`

The time at which an entity was completely created and is available for use.

### has note

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P3_has_note` · `crm:P3_has_note`

Quantification: one to many (0,n:0,1)

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
- P3(x,y,z) ⇒ [P3(x,y) ∧ E55(z)]

| | |
|---|---|
| Used in | used in axioms of [Architectural Element](classes.md#architecturalelement); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Calendar System](classes.md#calendarsystem); used in axioms of [Caste Group](classes.md#castegroup); used in axioms of [Custody Period](classes.md#custodyperiod); used in axioms of [Data Custodian](classes.md#datacustodian); used in axioms of [Data Source](classes.md#datasource); used in axioms of [Deity](classes.md#deity); used in axioms of [Endowment](classes.md#endowment); used in axioms of [Endowment Event](classes.md#endowmentevent); used in axioms of [Guthi](classes.md#guthi); used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Iconographic Object](classes.md#iconographicobject); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Office](classes.md#office); used in axioms of [Religious Tradition](classes.md#religioustradition); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Structure Type](classes.md#structuretype); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship); used in axioms of [Tenure](classes.md#tenure); used in axioms of [Verification](classes.md#verification) |

### Identifier

**IRI:** `http://purl.org/dc/terms/identifier` · `dcterms:identifier`

An unambiguous reference to the resource within a given context.

### inLanguage

**IRI:** `http://schema.org/inLanguage` · `schema1:inLanguage`

The language of the content or performance or used in an action. Please use one of the language codes from the [IETF BCP 47 standard](http://tools.ietf.org/html/bcp47). See also [[availableLanguage]].

| | |
|---|---|
| Used in | used in axioms of [Data Source](classes.md#datasource); used in axioms of [Heritage information object](classes.md#informationobject) |

### Institutional affiliation

**IRI:** `https://cair-nepal.org/heritagegraph/institutionalAffiliation` · `hg:institutionalAffiliation`

Institutional affiliation (e.g., Tribhuvan University, Nepal Heritage Society).

| | |
|---|---|
| Domain | [Person](classes.md#e21_person) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |

### Is critical for festival

**IRI:** `https://cair-nepal.org/heritagegraph/isCriticalForFestival` · `hg:isCriticalForFestival`

Whether this ritual is essential for the festival's completion.

| | |
|---|---|
| Domain | [Kumari Selection Event](classes.md#kumariselectionevent) |
| Range | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |
| Used in | used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |
| domainIncludes | hg:KumariSelectionEvent |

### Last known existence date

**IRI:** `https://cair-nepal.org/heritagegraph/lastKnownExistenceDate` · `hg:lastKnownExistenceDate`

Latest date when this structure is documented as existing (ISO 8601).

| | |
|---|---|
| Domain | [Architectural Structure](classes.md#architecturalstructure) |
| Range | [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |
| domainIncludes | hg:ArchitecturalStructure |

### Lunar date tithi

**IRI:** `https://cair-nepal.org/heritagegraph/lunarDateTithi` · `hg:lunarDateTithi`

Lunar day (tithi) by which the practice is timed, in free text (e.g. 'Bhadra Shukla Chaturdashi').

| | |
|---|---|
| Domain | [Ritual Event](classes.md#ritualevent) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent |

### obsolete curator ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/curator` · `hg:curator`

Person or organization curating the dataset.

### obsolete dataset name ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/dataset_name` · `hg:dataset_name`

Human-readable name of the dataset.

### obsolete dataset version ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/dataset_version` · `hg:dataset_version`

Version identifier of the dataset instance.

### obsolete generated date ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/generated_date` · `hg:generated_date`

Date the dataset serialization was generated (ISO 8601).

### obsolete license ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/license` · `hg:license`

License under which the dataset is released.

### obsolete schema version ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/schema_version` · `hg:schema_version`

HeritageGraph schema version the dataset conforms to.

### obsolete selection criteria met ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/selectionCriteriaMet` · `hg:selectionCriteriaMet`

DEPRECATED free-text list; use hg:hasCriterion -> SelectionCriterion subclasses instead. Retained for backward compatibility.

| | |
|---|---|
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |

### place is defined by

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P168_place_is_defined_by` · `crm:P168_place_is_defined_by`

Quantification: one to many, dependent (0,n:1,1)

Scope note:
This property associates an instance of E53 Place with an instance of E94 Space Primitive that defines it. Syntactic variants or use of different scripts may result in multiple instances of E94 Space Primitive defining exactly the same place. Transformations between different reference systems always result in new definitions of places approximating each other and not in alternative definitions.

Examples:
- The centroid from https://sws.geonames.org/735927 (E53) place is defined by 40°31'17.9"N 21°15'48.3"E (E94). [A single point for approximating the centre of the city of Kastoria, Greece]
- Martin’s coordinates for Kastoria (E53) place is defined by 40°30'23"N 21°14'53"E, 40°31'40"N 21°16'43"E (E94). [A square covering the built settlement structure of Kastoria, Greece]
- Martin’s centroid for Kastoria (E53) place is defined by 40°31'01.5"N 21°15'48"E (E94). [A point in the lake of Kastoria in the centre of the area covered by the city]
- The position measured by Alexander von Humboldt for the Plaza Mayor in Cumaná, Sucre, Venezuela 1799-1800AD (E53) place is defined by 10°27'52"N 66°30'02"W (E94). [West of the Observatory of Paris = 64°09'51"W of Greenwich, actually 1.1km east of today’s Plaza Andrés Eloy Blanco of Cumaná] (Humboldt, 1859)

In First Order Logic:
- P168(x,y) ⇒ E53(x)
- P168(x,y) ⇒ E94(y)

### Place type

**IRI:** `https://cair-nepal.org/heritagegraph/placeType` · `hg:placeType`

Type of place (city, village, region), free text.

| | |
|---|---|
| Domain | [Place](classes.md#e53_place) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |

### Proposition object literal

**IRI:** `https://cair-nepal.org/heritagegraph/propositionLiteralValue` · `hg:propositionLiteralValue`

Object of the proposition when it is a literal value (e.g. a date).

| | |
|---|---|
| Domain | [Proposition](classes.md#proposition) |
| Range | [rdfs:Literal](http://www.w3.org/2000/01/rdf-schema#Literal) |
| Used in | used in axioms of [Proposition](classes.md#proposition) |
| domainIncludes | hg:Proposition |

### Proposition predicate

**IRI:** `https://cair-nepal.org/heritagegraph/propositionPredicate` · `hg:propositionPredicate`

Property (URI/CURIE) claimed of the subject, e.g. crm:P108i_was_produced_by (plays the role of rdf:predicate).

| | |
|---|---|
| Domain | [Proposition](classes.md#proposition) |
| Range | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) |
| Used in | used in axioms of [Proposition](classes.md#proposition) |
| domainIncludes | hg:Proposition |

### Reconciliation status

**IRI:** `https://cair-nepal.org/heritagegraph/reconciliationStatus` · `hg:reconciliationStatus`

Status of multi-source reconciliation of the asserted value: confirmed (independent sources agree), conflicting (sources disagree; see the competing assertions), or unverified (single source, not yet checked).

| | |
|---|---|
| Domain | [Belief](classes.md#i2_belief) |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |

### Recorded date

**IRI:** `https://cair-nepal.org/heritagegraph/recordedDate` · `hg:recordedDate`

The date as written in the source, in the calendar given by hg:calendarSystem (e.g. '2072' for a Bikram Sambat year, 'NS 1135 Kaulaathwa', 'VS 2021'). It is never put into an xsd:dateTime: the converted Gregorian bounds go in crm:P82a_begin_of_the_begin / crm:P82b_end_of_the_end.

| | |
|---|---|
| Domain | [Time-Span](classes.md#e52_time-span) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |

### Recurrence pattern

**IRI:** `https://cair-nepal.org/heritagegraph/recurrencePattern` · `hg:recurrencePattern`

How the practice this occurrence belongs to recurs (e.g. annual, monthly), in free text. It describes the practice, not the occurrence: each occurrence is its own RitualEvent with its own time-span.

| | |
|---|---|
| Domain | [Ritual Event](classes.md#ritualevent) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent |

### Role duty

**IRI:** `https://cair-nepal.org/heritagegraph/roleDuty` · `hg:roleDuty`

The ritual duty held (e.g. building the festival chariot, performing the daily worship).

| | |
|---|---|
| Domain | [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| domainIncludes | hg:HereditaryRoleTenure |

### Route description

**IRI:** `https://cair-nepal.org/heritagegraph/routeDescription` · `hg:routeDescription`

Text description of the procession route.

| | |
|---|---|
| Domain | [Ritual Event](classes.md#ritualevent) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |
| domainIncludes | hg:RitualEvent |

### Source citation

**IRI:** `https://cair-nepal.org/heritagegraph/sourceCitation` · `hg:sourceCitation`

Formal citation of source.

| | |
|---|---|
| Domain | [Data Source](classes.md#datasource) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |
| domainIncludes | hg:DataSource |

### Source url

**IRI:** `https://cair-nepal.org/heritagegraph/sourceUrl` · `hg:sourceUrl`

URL or digital identifier for source.

| | |
|---|---|
| Domain | [Data Source](classes.md#datasource) |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |
| domainIncludes | hg:DataSource |

### startedAtTime

**IRI:** `http://www.w3.org/ns/prov#startedAtTime` · `prov:startedAtTime`

The time at which an activity started. See also prov:endedAtTime.

### Succession rule

**IRI:** `https://cair-nepal.org/heritagegraph/successionRule` · `hg:successionRule`

Rule by which the duty passes on (e.g. eldest son of the lineage; within the caste group).

| | |
|---|---|
| Domain | [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Hereditary Role Tenure](classes.md#hereditaryroletenure) |
| domainIncludes | hg:HereditaryRoleTenure |

### Traditional role

**IRI:** `https://cair-nepal.org/heritagegraph/traditionalRole` · `hg:traditionalRole`

Hereditary occupation or ritual duty.

| | |
|---|---|
| Domain | [Caste Group](classes.md#castegroup) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Caste Group](classes.md#castegroup) |
| domainIncludes | hg:CasteGroup |

### Used equipment

**IRI:** `https://cair-nepal.org/heritagegraph/usedEquipment` · `hg:usedEquipment`

Equipment used in documentation.

| | |
|---|---|
| Domain | [Documentation Activity](classes.md#documentationactivity) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |
| domainIncludes | hg:DocumentationActivity |

### Used method

**IRI:** `https://cair-nepal.org/heritagegraph/usedMethod` · `hg:usedMethod`

Documentation method used.

| | |
|---|---|
| Domain | [Documentation Activity](classes.md#documentationactivity) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |
| domainIncludes | hg:DocumentationActivity |

### value

**IRI:** `http://www.w3.org/ns/prov#value` · `prov:value`

Provides a value that is a direct representation of an entity.

### Verification method

**IRI:** `https://cair-nepal.org/heritagegraph/verificationMethod` · `hg:verificationMethod`

Method used for verification (cross-check, expert review, field visit).

| | |
|---|---|
| Domain | [Verification](classes.md#verification) |
| Range | [rdf:PlainLiteral](http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral) |
| Used in | used in axioms of [Verification](classes.md#verification) |
| domainIncludes | hg:Verification |

### Year offset from gregorian

**IRI:** `https://cair-nepal.org/heritagegraph/yearOffsetFromGregorian` · `hg:yearOffsetFromGregorian`

Number of years this calendar runs ahead of the Gregorian (Common Era) year at the start of its year (e.g. 57 for Bikram Sambat, -879 for Nepal Sambat). Because the calendar's new year does not fall on 1 January (see hg:epochDateGregorian), a year-precision date Y converts to the two-year interval [Y - offset, Y - offset + 1] CE; the single year Y - offset is correct only for dates between the calendar's new year and 31 December. A calendar whose new year is 1 January converts to Y - offset exactly.

| | |
|---|---|
| Domain | [Calendar System](classes.md#calendarsystem) |
| Range | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) |
| Used in | used in axioms of [Calendar System](classes.md#calendarsystem) |
| domainIncludes | hg:CalendarSystem |

