#!/usr/bin/env python3
"""Execute demonstrator SELECT CQs over TBox+ABox; run SHACL conformance + negative tests.

Updated for the 0.1.0 artifact lineage: class/property IRIs follow the
released TTL (KumariTenure, crminf:I2_Belief, camelCase slot IRIs, native CRM
property reuse), the demonstrator is examples/kathmandu-mini-abox.ttl,
and validation mirrors the pipeline gate (ont_graph mixed in, inference="none";
owl:NamedIndividual declarations stripped from the in-memory copy only, to
avoid the known pySHACL slowdown -- see scripts/finalize_artifacts.py).
"""
from pathlib import Path
from rdflib import Graph, RDF, OWL, URIRef
from pyshacl import validate
ROOT = str(Path(__file__).resolve().parents[1]) + "/"
PFX = """PREFIX hg:<https://cair-nepal.org/heritagegraph/>
PREFIX crm:<http://www.cidoc-crm.org/cidoc-crm/>
PREFIX crminf:<http://www.cidoc-crm.org/extensions/crminf/>
PREFIX prov:<http://www.w3.org/ns/prov#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>"""

g = Graph()
g.parse(ROOT + "ontology/HeritageGraph.ttl", format="turtle")
g.parse(ROOT + "examples/kathmandu-mini-abox.ttl", format="turtle")
print("TBox+ABox triples:", len(g))
CQ = {
"CQ-A1 conflicting source-attributed build dates":
 PFX + """SELECT ?value ?source ?agent ?conf WHERE {
  ?a a crminf:I2_Belief ; hg:assertsAbout ?e ;
     prov:value ?value ; prov:wasDerivedFrom ?source ;
     prov:wasAttributedTo ?agent ; hg:confidenceScore ?conf . }""",
"CQ-A2 event-mediated construction (temple/style/place)":
 PFX + """SELECT ?temple ?style ?place WHERE {
  ?p a crm:E12_Production ; crm:P108_has_produced ?temple .
  ?temple hg:hasArchitecturalStyle ?style ; crm:P55_has_current_location ?place . }""",
"CQ-A3 Guthi custody (+ ritual, where recorded)":
 PFX + """SELECT ?guthi ?asset ?ritual WHERE {
  ?guthi a hg:Guthi ; crm:P50i_is_current_keeper_of ?asset .
  OPTIONAL { ?guthi hg:performsRitual ?ritual } }""",
"CQ-A4 Kumari (Living-Goddess) tenure (deity + institution)":
 PFX + """SELECT ?tenure ?deity ?inst WHERE {
  ?tenure a hg:KumariTenure ; hg:embodiedDeity ?deity ;
          hg:supportedByInstitution ?inst . }""",
"CQ-A5 syncretic equivalence + type":
 PFX + """SELECT ?primary ?equiv ?type WHERE {
  ?s a hg:SyncreticRelationship ; crm:P140_assigned_attribute_to ?primary ;
     crm:P141_assigned ?equiv ; hg:syncreticType ?type . }""",
"CQ-A6 recurring ritual pattern":
 PFX + """SELECT ?ritual ?pat WHERE { ?ritual a hg:RitualEvent ; hg:recurrencePattern ?pat . }""",
}
print("\n== SELECT competency queries (rows returned) ==")
for name, q in CQ.items():
    rows = list(g.query(q))
    print(f"[{len(rows)} rows] {name}")
    for r in rows[:2]:
        print("     -> " + " | ".join(str(x).replace('https://cair-nepal.org/heritagegraph/example/', '').replace('https://cair-nepal.org/heritagegraph/', 'hg:').replace('http://vocab.getty.edu/aat/', 'aat:') for x in r))

# SHACL validation setup: shapes + ontology graph (pipeline-gate configuration).
shapes = Graph(); shapes.parse(ROOT + "ontology/HeritageGraph.shacl.ttl", format="turtle")
ont = Graph(); ont.parse(ROOT + "ontology/HeritageGraph.ttl", format="turtle")
for s in list(ont.subjects(RDF.type, OWL.NamedIndividual)):
    ont.remove((s, RDF.type, OWL.NamedIndividual))

# Conformance 1: full demonstrator ABox.
abox = Graph(); abox.parse(ROOT + "examples/kathmandu-mini-abox.ttl", format="turtle")
conforms, _, txt = validate(abox, shacl_graph=shapes, ont_graph=ont,
                            inference="none", abort_on_first=False)
print(f"\n== SHACL conformance (full demonstrator ABox): conforms={conforms} ==")
if not conforms:
    print(txt[:1500])

# Conformance 2: minimal valid instance quartet.
MINIMAL = """@prefix hg: <https://cair-nepal.org/heritagegraph/> .
@prefix aat: <http://vocab.getty.edu/aat/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <https://cair-nepal.org/heritagegraph/example/> .
ex:T a hg:Temple ; rdfs:label "T" ; hg:hasArchitecturalStyle <https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Pagoda> .
ex:G a hg:Guthi ; rdfs:label "G" .
ex:R a hg:RitualEvent ; rdfs:label "R" .
ex:D a hg:DataSource ; rdfs:label "D" .
"""
mg = Graph(); mg.parse(data=MINIMAL, format="turtle")
conforms, _, txt = validate(mg, shacl_graph=shapes, ont_graph=ont,
                            inference="none", abort_on_first=False)
print(f"== SHACL conformance (minimal valid instance): conforms={conforms} ==")
if not conforms:
    print(txt[:1500])

# Conformance 3: multilingual text and many-valued CIDOC CRM properties
# (language-tagged labels and notes, a note plus a citation, a procession over
# two places, one production and one custody transfer of two objects).
ml = Graph(); ml.parse(ROOT + "examples/kathmandu-multilingual.ttl", format="turtle")
conforms_ml, _, txt = validate(ml, shacl_graph=shapes, ont_graph=ont,
                               inference="none", abort_on_first=False)
print(f"== SHACL conformance (multilingual, many-valued fixture): conforms={conforms_ml} ==")
if not conforms_ml:
    print(txt[:1500])

# Negative tests: inject violations, expect non-conformance.
# One test per modelling concern. The alpha lineage publishes OPEN shapes
# (closedness is deliberately dropped by the pipeline), so the tests exercise
# the constraint components the shapes actually carry: minCount, maxCount,
# sh:in, sh:datatype, sh:nodeKind, sh:or and sh:class value-typing. A test
# counts as caught only if the report contains a violation of the component
# it targets.
print("\n== SHACL negative tests (each should be caught) ==")
NEG_PFX = """@prefix hg: <https://cair-nepal.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix crminf: <http://www.cidoc-crm.org/extensions/crminf/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix aat: <http://vocab.getty.edu/aat/> .
@prefix ex: <https://cair-nepal.org/heritagegraph/example/> .
"""
TENURE_OK = ('''ex:BadTenure a hg:KumariTenure ; rdfs:label "x" ; hg:residenceStructure ex:H ; hg:tenureHolder ex:P ;
    crm:P4_has_time-span ex:TS .
ex:D1 a hg:Deity ; rdfs:label "d" . ex:H a hg:KumariHouse ; rdfs:label "h" . ex:P a crm:E21_Person ; rdfs:label "p" .
ex:TS a crm:E52_Time-Span .''')
tests = {
 # 1.1.0: hasArchitecturalStyle is no longer required (archives often record
 # no style), so the event-mediated minCount test now targets the custody
 # period's required holder.
 "Event-mediated: CustodyPeriod missing custodyHolder (minCount)":
  ('ex:BadCustody a hg:CustodyPeriod ; rdfs:label "x" ; hg:custodyObject ex:T ; crm:P4_has_time-span ex:TS .\n'
   'ex:T a hg:Temple ; rdfs:label "t" . ex:TS a crm:E52_Time-Span .', "MinCount"),
 "Metadata: Temple dcterms:identifier not an xsd:anyURI (datatype)":
  ('ex:BadTemple a hg:Temple ; rdfs:label "x" ; hg:hasArchitecturalStyle <https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Pagoda> ; dcterms:identifier "plain string" .', "Datatype"),
 "Institutional: Guthi guthiType outside controlled vocabulary (sh:in)":
  ('ex:BadGuthi a hg:Guthi ; rdfs:label "x" ; hg:guthiType <https://cair-nepal.org/heritagegraph/RitualType#Jatra> .', "In"),
 "Ritual: RitualEvent time-span not an E52_Time-Span (sh:class)":
  ('ex:BadRitual a hg:RitualEvent ; rdfs:label "x" ; crm:P4_has_time-span ex:NotATimeSpan . ex:NotATimeSpan a hg:DataSource .', "Class"),
 "Syncretic: SyncreticRelationship missing assigned deity (minCount)":
  ('ex:BadSyn a hg:SyncreticRelationship ; rdfs:label "x" ; crm:P141_assigned ex:D1 . ex:D1 a hg:Deity ; rdfs:label "d" .', "MinCount"),
 "Provenance: Belief (HeritageAssertion) missing assertsAbout (minCount)":
  ('ex:BadAssert a crminf:I2_Belief ; rdfs:label "x" .', "MinCount"),
 "Living Goddess: KumariTenure missing crm:P4_has_time-span (minCount)":
  ('''ex:BadTenure a hg:KumariTenure ; rdfs:label "x" ; hg:embodiedDeity ex:D1 ; hg:residenceStructure ex:H ; hg:tenureHolder ex:P .
ex:D1 a hg:Deity ; rdfs:label "d" . ex:H a hg:KumariHouse ; rdfs:label "h" . ex:P a crm:E21_Person ; rdfs:label "p" .''', "MinCount"),
 "Sibling separation: DocumentationActivity in a ritual-valued slot (sh:class)":
  ('ex:G a hg:Guthi ; rdfs:label "g" ; hg:performsRitual ex:Doc . ex:Doc a hg:DocumentationActivity ; rdfs:label "doc" .', "Class"),
 "Living Goddess: KumariTenure with two embodied deities (maxCount)":
  (TENURE_OK + ' ex:BadTenure hg:embodiedDeity ex:D1 , ex:D2 . ex:D2 a hg:Deity ; rdfs:label "d2" .', "MaxCount"),
 "Ritual: ritual site given as an unidentified blank node (nodeKind IRI)":
  ('ex:BadRitual a hg:RitualEvent ; rdfs:label "x" ; crm:P8_took_place_on_or_within [ a hg:Temple ; rdfs:label "t" ; hg:hasArchitecturalStyle <https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Pagoda> ] .', "NodeKind"),
 "Institutional: ritual performed by a person, not a Guthi or caste group (sh:or)":
  ('ex:BadRitual a hg:RitualEvent ; rdfs:label "x" ; hg:performedByGroup ex:P . ex:P a crm:E21_Person ; rdfs:label "p" .', "Or"),
 "Provenance: reconciliationStatus outside confirmed|conflicting|unverified (sh:pattern)":
  ('ex:BadStatus a crminf:I2_Belief ; rdfs:label "x" ; hg:assertsAbout ex:D1 ; hg:reconciliationStatus "maybe" .\n'
   'ex:D1 a hg:Deity ; rdfs:label "d" .', "Pattern"),
 "Calendar: time-span ends before it begins (sh:lessThanOrEquals)":
  ('ex:BadSpan a crm:E52_Time-Span ; crm:P82a_begin_of_the_begin "2016-01-01T00:00:00"^^xsd:dateTime ;'
   ' crm:P82b_end_of_the_end "2015-01-01T00:00:00"^^xsd:dateTime .', "LessThanOrEquals"),
 "Calendar: recorded date without its calendar (sh:or)":
  ('ex:BadRecord a crm:E52_Time-Span ; hg:recordedDate "2072" ;'
   ' crm:P82a_begin_of_the_begin "2015-04-14T00:00:00"^^xsd:dateTime .', "Or"),
 # Labels may come in several languages, but one per language tag.
 "Labels: two English labels on one deity (sh:uniqueLang)":
  ('ex:BadDeity a hg:Deity ; rdfs:label "Taleju"@en , "Tulaja"@en .', "UniqueLang"),
 "Labels: two untagged labels on one deity (sh:qualifiedMaxCount)":
  ('ex:BadDeity a hg:Deity ; rdfs:label "Taleju" , "Tulaja" .', "QualifiedMaxCount"),
 # Free text accepts xsd:string or rdf:langString, nothing else.
 "Text: a note given as a number, not text (sh:or string|langString)":
  ('ex:BadRitual a hg:RitualEvent ; rdfs:label "x" ; crm:P3_has_note 42 .', "Or"),
 "Destruction: a destruction that destroyed a deity, not a physical thing (sh:or)":
  ('ex:BadDestr a crm:E6_Destruction ; rdfs:label "x" ; crm:P13_destroyed ex:D1 . ex:D1 a hg:Deity ; rdfs:label "d" .', "Or"),
 "Destruction: a destruction that names nothing destroyed (minCount)":
  ('ex:BadDestr a crm:E6_Destruction ; rdfs:label "x" .', "MinCount"),
 "Existence: a reconstructed temple with no current location (node-level sh:or)":
  ('ex:BadTemple a hg:Temple ; rdfs:label "t" ; hg:existenceStatus <https://cair-nepal.org/heritagegraph/ExistenceStatus#Reconstructed> .', "Or"),
 "Tenure: a 1.0.x-style Kumari tenure giving its holder only with hadParticipant (minCount)":
  (TENURE_OK.replace("hg:tenureHolder ex:P", "hg:hadParticipant ex:P") + ' ex:BadTenure hg:embodiedDeity ex:D1 . ex:D1 a hg:Deity ; rdfs:label "d" .', "MinCount"),
 "Typing: a structure type given as a deity, not a StructureType term (sh:class)":
  ('ex:BadStructure a hg:ReligiousStructure ; rdfs:label "s" ; hg:structureType ex:D1 . ex:D1 a hg:Deity ; rdfs:label "d" .', "Class"),
 "Open shapes: a misspelt HeritageGraph property, hg:hasArchitecturalStyel (SHACL-SPARQL)":
  ('ex:D1 a hg:Deity ; rdfs:label "d" ; hg:hasArchitecturalStyel ex:X .', "SPARQL"),
 "Provenance: a belief marked conflicting with no rival belief about its subject (SHACL-SPARQL)":
  ('ex:B1 a crminf:I2_Belief ; rdfs:label "b" ; hg:assertsAbout ex:D1 ; hg:reconciliationStatus "conflicting" . '
   'ex:D1 a hg:Deity ; rdfs:label "d" .', "SPARQL"),
 "Text: an empty label (minLength)":
  ('ex:D1 a hg:Deity ; rdfs:label "" .', "MinLength"),
 "Provenance: a confidence score above 1 (maxInclusive)":
  ('ex:B1 a crminf:I2_Belief ; rdfs:label "b" ; hg:assertsAbout ex:D1 ; hg:confidenceScore "1.5"^^xsd:decimal . '
   'ex:D1 a hg:Deity ; rdfs:label "d" .', "MaxInclusive"),
}
# The property each test must violate: a test counts as caught only when a
# result has the expected constraint component ON THE EXPECTED PATH (a
# different, unintended violation of the same component does not count).
HG_ = "https://cair-nepal.org/heritagegraph/"
CRM_ = "http://www.cidoc-crm.org/cidoc-crm/"
EXPECTED_PATH = {
 "Event-mediated: CustodyPeriod missing custodyHolder (minCount)": HG_ + "custodyHolder",
 "Metadata: Temple dcterms:identifier not an xsd:anyURI (datatype)": "http://purl.org/dc/terms/identifier",
 "Institutional: Guthi guthiType outside controlled vocabulary (sh:in)": HG_ + "guthiType",
 "Ritual: RitualEvent time-span not an E52_Time-Span (sh:class)": CRM_ + "P4_has_time-span",
 "Syncretic: SyncreticRelationship missing assigned deity (minCount)": CRM_ + "P140_assigned_attribute_to",
 "Provenance: Belief (HeritageAssertion) missing assertsAbout (minCount)": HG_ + "assertsAbout",
 "Living Goddess: KumariTenure missing crm:P4_has_time-span (minCount)": CRM_ + "P4_has_time-span",
 "Sibling separation: DocumentationActivity in a ritual-valued slot (sh:class)": HG_ + "performsRitual",
 "Living Goddess: KumariTenure with two embodied deities (maxCount)": HG_ + "embodiedDeity",
 "Ritual: ritual site given as an unidentified blank node (nodeKind IRI)": CRM_ + "P8_took_place_on_or_within",
 "Institutional: ritual performed by a person, not a Guthi or caste group (sh:or)": HG_ + "performedByGroup",
 "Provenance: reconciliationStatus outside confirmed|conflicting|unverified (sh:pattern)": HG_ + "reconciliationStatus",
 "Calendar: time-span ends before it begins (sh:lessThanOrEquals)": CRM_ + "P82a_begin_of_the_begin",
 "Calendar: recorded date without its calendar (sh:or)": "None",  # node-level sh:or: no result path
 "Labels: two English labels on one deity (sh:uniqueLang)": "http://www.w3.org/2000/01/rdf-schema#label",
 "Labels: two untagged labels on one deity (sh:qualifiedMaxCount)": "http://www.w3.org/2000/01/rdf-schema#label",
 "Text: a note given as a number, not text (sh:or string|langString)": CRM_ + "P3_has_note",
 "Destruction: a destruction that destroyed a deity, not a physical thing (sh:or)": CRM_ + "P13_destroyed",
 "Destruction: a destruction that names nothing destroyed (minCount)": CRM_ + "P13_destroyed",
 "Existence: a reconstructed temple with no current location (node-level sh:or)": "None",  # node-level sh:or: no result path
 "Tenure: a 1.0.x-style Kumari tenure giving its holder only with hadParticipant (minCount)": HG_ + "tenureHolder",
 "Typing: a structure type given as a deity, not a StructureType term (sh:class)": HG_ + "structureType",
 "Open shapes: a misspelt HeritageGraph property, hg:hasArchitecturalStyel (SHACL-SPARQL)": HG_ + "hasArchitecturalStyel",
 "Provenance: a belief marked conflicting with no rival belief about its subject (SHACL-SPARQL)": "None",
 "Text: an empty label (minLength)": "http://www.w3.org/2000/01/rdf-schema#label",
 "Provenance: a confidence score above 1 (maxInclusive)": HG_ + "confidenceScore",
}
SH_NS = "http://www.w3.org/ns/shacl#"
caught = 0
for name, (ttl, component) in tests.items():
    dg = Graph()
    dg.parse(data=NEG_PFX + ttl, format="turtle")
    c, rg, _ = validate(dg, shacl_graph=shapes, ont_graph=ont,
                        inference="none", abort_on_first=False)
    comps = sorted({str(o)[len(SH_NS):].removesuffix("ConstraintComponent")
                    for o in rg.objects(None, URIRef(SH_NS + "sourceConstraintComponent"))})
    hits = {(str(rg.value(r, URIRef(SH_NS + "sourceConstraintComponent")))[len(SH_NS):]
             .removesuffix("ConstraintComponent"), str(rg.value(r, URIRef(SH_NS + "resultPath"))))
            for r in rg.subjects(URIRef(SH_NS + "sourceConstraintComponent"), None)}
    hit = (component, EXPECTED_PATH[name]) in hits
    caught += hit
    print(f"  [{'CAUGHT' if hit else 'MISSED'}] {name}  -> violated: {', '.join(comps) or 'none'}")
print(f"Negative tests caught: {caught}/{len(tests)}")
if not (conforms_ml and caught == len(tests)):
    raise SystemExit(1)
