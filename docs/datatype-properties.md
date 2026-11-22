# Datatype properties

### Assertion content

**IRI:** `http://www.w3.org/ns/prov#value` · `prov:value`

The factual claim being asserted

### Confidence score

**IRI:** `https://cair-nepal.org/heritagegraph/confidenceScore` · `heritageGraph:confidenceScore`

Reliability score for assertion (0.0-1.0)

| | |
|---|---|
| Range | [xsd:decimal](http://www.w3.org/2001/XMLSchema#decimal)[*>=* `0.0`, *<=* `1.0`] |

### curator

**IRI:** `https://cair-nepal.org/heritagegraph/curator` · `heritageGraph:curator`

Person or organization curating the dataset.

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Metadata](classes.md#metadata) |

### Custodian type

**IRI:** `https://cair-nepal.org/heritagegraph/custodianType` · `heritageGraph:custodianType`

Type of custodian (government, academic, community), free text

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Custodian](classes.md#datacustodian) |

### Data quality note

**IRI:** `https://cair-nepal.org/heritagegraph/dataQualityNote` · `heritageGraph:dataQualityNote`

Notes on data quality, completeness, or uncertainty

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |

### Datacite identifier

**IRI:** `https://cair-nepal.org/heritagegraph/persistentIdentifier` · `heritageGraph:persistentIdentifier`

Persistent identifier for the source (DOI, archive ID, catalog number)

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |

### Datacite identifier type

**IRI:** `https://cair-nepal.org/heritagegraph/identifierScheme` · `heritageGraph:identifierScheme`

Type of identifier (DOI, ISBN, Handle, LocalArchiveID)

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |

### Datacite resource type

**IRI:** `https://cair-nepal.org/heritagegraph/resourceType` · `heritageGraph:resourceType`

High-level DataCite resource type (Dataset, Text, Image, Audio, Interview)

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |

### Dataset name

**IRI:** `https://cair-nepal.org/heritagegraph/dataset_name` · `heritageGraph:dataset_name`

Human-readable name of the dataset.

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Metadata](classes.md#metadata) |

### Dataset version

**IRI:** `https://cair-nepal.org/heritagegraph/dataset_version` · `heritageGraph:dataset_version`

Version identifier of the dataset instance.

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Metadata](classes.md#metadata) |

### Date earliest

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P82a_begin_of_the_begin` · `crm:P82a_begin_of_the_begin`

Earliest possible date (for uncertain dates)

### Date latest

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P82b_end_of_the_end` · `crm:P82b_end_of_the_end`

Latest possible date (for uncertain dates)

### Ended at time

**IRI:** `http://www.w3.org/ns/prov#endedAtTime` · `prov:endedAtTime`

Time at which this activity ended.

### Epoch date gregorian

**IRI:** `https://cair-nepal.org/heritagegraph/epochDateGregorian` · `heritageGraph:epochDateGregorian`

The start date of this calendar era in Gregorian ISO format.

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Calendar System](classes.md#calendarsystem) |

### Expertise area

**IRI:** `https://cair-nepal.org/heritagegraph/expertiseArea` · `heritageGraph:expertiseArea`

Areas of expertise (e.g., Lichhavi inscriptions, Sanskrit epigraphy, Newari archaeology)

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |

### Generated at time

**IRI:** `http://www.w3.org/ns/prov#generatedAtTime` · `prov:generatedAtTime`

Time at which this entity was generated (ISO 8601).

### Generated date

**IRI:** `https://cair-nepal.org/heritagegraph/generated_date` · `heritageGraph:generated_date`

Date the dataset serialization was generated (ISO 8601).

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Metadata](classes.md#metadata) |

### ID

**IRI:** `http://purl.org/dc/terms/identifier` · `dcterms:identifier`

Globally unique URI identifier

### Institutional affiliation

**IRI:** `https://cair-nepal.org/heritagegraph/institutionalAffiliation` · `heritageGraph:institutionalAffiliation`

Institutional affiliation (e.g., Tribhuvan University, Nepal Heritage Society)

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |

### Is critical for festival

**IRI:** `https://cair-nepal.org/heritagegraph/isCriticalForFestival` · `heritageGraph:isCriticalForFestival`

Whether this ritual is essential for the festival's completion

| | |
|---|---|
| Range | [xsd:boolean](http://www.w3.org/2001/XMLSchema#boolean) |
| Used in | used in axioms of [Kumari Selection Event](classes.md#kumariselectionevent) |

### Last known existence date

**IRI:** `https://cair-nepal.org/heritagegraph/lastKnownExistenceDate` · `heritageGraph:lastKnownExistenceDate`

Latest date when this structure is documented as existing (ISO 8601)

| | |
|---|---|
| Range | [xsd:dateTime](http://www.w3.org/2001/XMLSchema#dateTime) |
| Used in | used in axioms of [Architectural Structure](classes.md#architecturalstructure) |

### license

**IRI:** `https://cair-nepal.org/heritagegraph/license` · `heritageGraph:license`

License under which the dataset is released.

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Metadata](classes.md#metadata) |

### Lunar date tithi

**IRI:** `https://cair-nepal.org/heritagegraph/lunarDateTithi` · `heritageGraph:lunarDateTithi`

Lunar day (Tithi) for ritual timing

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### note

**IRI:** `http://www.cidoc-crm.org/cidoc-crm/P3_has_note` · `crm:P3_has_note`

Free-text note (description, reason, verification notes)

| | |
|---|---|
| Sub-properties | [Source citation](datatype-properties.md#sourcecitation) |
| Used in | used in axioms of [Architectural Element](classes.md#architecturalelement); used in axioms of [Architectural Structure](classes.md#architecturalstructure); used in axioms of [Calendar System](classes.md#calendarsystem); used in axioms of [Caste Group](classes.md#castegroup); used in axioms of [Data Custodian](classes.md#datacustodian); used in axioms of [Data Source](classes.md#datasource); used in axioms of [Deity](classes.md#deity); used in axioms of [Guthi](classes.md#guthi); used in axioms of [Historical Event](classes.md#historicalevent); used in axioms of [Iconographic Object](classes.md#iconographicobject); used in axioms of [Kumari Retirement Event](classes.md#kumariretirementevent); used in axioms of [Religious Tradition](classes.md#religioustradition); used in axioms of [Ritual Event](classes.md#ritualevent); used in axioms of [Syncretic Relationship](classes.md#syncreticrelationship); used in axioms of [Verification](classes.md#verification) |

### obsolete selection criteria met ~~deprecated~~

**IRI:** `https://cair-nepal.org/heritagegraph/selectionCriteriaMet` · `heritageGraph:selectionCriteriaMet`

DEPRECATED free-text list; use has_criterion -> SelectionCriterion subclasses instead. Retained for backward compatibility.

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |

### Place coordinates

**IRI:** `http://www.opengis.net/ont/geosparql#asWKT` · `geo:asWKT`

Coordinates as WKT literal

### Place type

**IRI:** `https://cair-nepal.org/heritagegraph/placeType` · `heritageGraph:placeType`

Type of place (city, village, region), free text

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |

### Proposition object literal

**IRI:** `https://cair-nepal.org/heritagegraph/propositionLiteralValue` · `heritageGraph:propositionLiteralValue`

Object of the proposition when it is a literal value (e.g. a date).

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Proposition](classes.md#proposition) |

### Proposition predicate

**IRI:** `https://cair-nepal.org/heritagegraph/propositionPredicate` · `heritageGraph:propositionPredicate`

Property (URI/CURIE) claimed of the subject, e.g. crm:P108i_was_produced_by (plays the role of rdf:predicate).

| | |
|---|---|
| Range | [xsd:anyURI](http://www.w3.org/2001/XMLSchema#anyURI) |
| Used in | used in axioms of [Proposition](classes.md#proposition) |

### Reconciliation status

**IRI:** `https://cair-nepal.org/heritagegraph/reconciliationStatus` · `heritageGraph:reconciliationStatus`

Status of multi-source reconciliation (confirmed, conflicting, unverified)

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |

### Recurrence pattern

**IRI:** `https://cair-nepal.org/heritagegraph/recurrencePattern` · `heritageGraph:recurrencePattern`

Frequency of recurring ritual (e.g., annual, monthly)

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Route description

**IRI:** `https://cair-nepal.org/heritagegraph/routeDescription` · `heritageGraph:routeDescription`

Text description of the procession route

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Ritual Event](classes.md#ritualevent) |

### Schema version

**IRI:** `https://cair-nepal.org/heritagegraph/schema_version` · `heritageGraph:schema_version`

HeritageGraph schema version the dataset conforms to.

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Metadata](classes.md#metadata) |

### Source citation

**IRI:** `https://cair-nepal.org/heritagegraph/sourceCitation` · `heritageGraph:sourceCitation`

Formal citation of source

| | |
|---|---|
| Super-properties | [note](datatype-properties.md#p3_has_note) |
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |

### Source language

**IRI:** `http://schema.org/inLanguage` · `schema1:inLanguage`

Language of the source material

| | |
|---|---|
| Used in | used in axioms of [Data Source](classes.md#datasource); used in axioms of [Information Object](classes.md#informationobject) |

### Source url

**IRI:** `https://cair-nepal.org/heritagegraph/sourceUrl` · `heritageGraph:sourceUrl`

URL or digital identifier for source

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Data Source](classes.md#datasource) |

### Started at time

**IRI:** `http://www.w3.org/ns/prov#startedAtTime` · `prov:startedAtTime`

Time at which this activity started.

### Traditional role

**IRI:** `https://cair-nepal.org/heritagegraph/traditionalRole` · `heritageGraph:traditionalRole`

Hereditary occupation or ritual duty

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Caste Group](classes.md#castegroup) |

### Used equipment

**IRI:** `https://cair-nepal.org/heritagegraph/usedEquipment` · `heritageGraph:usedEquipment`

Equipment used in documentation

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |

### Used method

**IRI:** `https://cair-nepal.org/heritagegraph/usedMethod` · `heritageGraph:usedMethod`

Documentation method used

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Documentation Activity](classes.md#documentationactivity) |

### Verification method

**IRI:** `https://cair-nepal.org/heritagegraph/verificationMethod` · `heritageGraph:verificationMethod`

Method used for verification (cross-check, expert review, field visit)

| | |
|---|---|
| Range | [xsd:string](http://www.w3.org/2001/XMLSchema#string) |
| Used in | used in axioms of [Verification](classes.md#verification) |

### Year offset from gregorian

**IRI:** `https://cair-nepal.org/heritagegraph/yearOffsetFromGregorian` · `heritageGraph:yearOffsetFromGregorian`

Mathematical offset to convert to Common Era (e.g., +57 for BS).

| | |
|---|---|
| Range | [xsd:integer](http://www.w3.org/2001/XMLSchema#integer) |
| Used in | used in axioms of [Calendar System](classes.md#calendarsystem) |

