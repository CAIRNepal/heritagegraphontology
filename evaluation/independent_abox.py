#!/usr/bin/env python3
"""Execute demonstrator SELECT CQs over TBox+ABox; run SHACL conformance + negative tests.

Updated for the 0.1.0 artifact lineage: class/property IRIs follow the
released TTL (KumariTenure, crminf:I2_Belief, camelCase slot IRIs, native CRM
property reuse), the demonstrator is examples/kathmandu-mini-abox.ttl,
and validation mirrors the pipeline gate (ont_graph mixed in, inference="none";
owl:NamedIndividual declarations stripped from the in-memory copy only, to
avoid the known pySHACL slowdown -- see scripts/finalize_alpha5_artifacts.py).
"""
from pathlib import Path
from rdflib import Graph, RDF, OWL
from pyshacl import validate
ROOT = str(Path(__file__).resolve().parents[1]) + "/"
PFX = """PREFIX hg:<https://w3id.org/heritagegraph/>
PREFIX crm:<http://www.cidoc-crm.org/cidoc-crm/>
PREFIX crminf:<http://www.ics.forth.gr/isl/CRMinf/>
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
"CQ-A3 Guthi custody + ritual":
 PFX + """SELECT ?guthi ?asset ?ritual WHERE {
  ?guthi a hg:Guthi ; crm:P50i_is_current_keeper_of ?asset ; hg:performsRitual ?ritual . }""",
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
        print("     -> " + " | ".join(str(x).replace('https://w3id.org/heritagegraph/demo/', '').replace('https://w3id.org/heritagegraph/', 'hg:').replace('http://vocab.getty.edu/aat/', 'aat:') for x in r))

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
MINIMAL = """@prefix hg: <https://w3id.org/heritagegraph/> .
@prefix aat: <http://vocab.getty.edu/aat/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <https://w3id.org/heritagegraph/demo/> .
ex:T a hg:Temple ; rdfs:label "T" ; hg:hasArchitecturalStyle aat:300004829 .
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

# Negative tests: inject violations, expect non-conformance.
# One test per modelling concern. The alpha lineage publishes OPEN shapes
# (closedness is deliberately dropped by the pipeline), so the tests exercise
# the constraint types the shapes actually carry: minCount, sh:in, sh:datatype
# and sh:class value-typing.
print("\n== SHACL negative tests (each should be caught) ==")
NEG_PFX = """@prefix hg: <https://w3id.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix crminf: <http://www.ics.forth.gr/isl/CRMinf/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix aat: <http://vocab.getty.edu/aat/> .
@prefix ex: <https://w3id.org/heritagegraph/demo/> .
"""
tests = {
 "Event-mediated: Temple missing hasArchitecturalStyle (minCount)":
  'ex:BadTemple a hg:Temple ; rdfs:label "x" .',
 "Metadata: Temple dcterms:identifier not an xsd:anyURI (datatype)":
  'ex:BadTemple a hg:Temple ; rdfs:label "x" ; hg:hasArchitecturalStyle aat:300004829 ; dcterms:identifier "plain string" .',
 "Institutional: Guthi guthiType outside controlled vocabulary (sh:in)":
  'ex:BadGuthi a hg:Guthi ; rdfs:label "x" ; hg:guthiType hg:NotAGuthiType .',
 "Ritual: RitualEvent time-span not an E52_Time-Span (sh:class)":
  'ex:BadRitual a hg:RitualEvent ; rdfs:label "x" ; crm:P4_has_time-span ex:NotATimeSpan . ex:NotATimeSpan a hg:DataSource .',
 "Syncretic: SyncreticRelationship missing assigned deity (minCount)":
  'ex:BadSyn a hg:SyncreticRelationship ; rdfs:label "x" ; crm:P141_assigned ex:D1 . ex:D1 a hg:Deity ; rdfs:label "d" .',
 "Provenance: Belief (HeritageAssertion) missing assertsAbout (minCount)":
  'ex:BadAssert a crminf:I2_Belief ; rdfs:label "x" .',
 "Living Goddess: KumariTenure missing crm:P4_has_time-span (minCount)":
  '''ex:BadTenure a hg:KumariTenure ; rdfs:label "x" ; hg:embodiedDeity ex:D1 ; hg:residenceStructure ex:H ; crm:P11_had_participant ex:P .
ex:D1 a hg:Deity ; rdfs:label "d" . ex:H a hg:KumariHouse ; rdfs:label "h" . ex:P a crm:E21_Person ; rdfs:label "p" .''',
 "Sibling separation: DocumentationActivity in a ritual-valued slot (sh:class)":
  'ex:G a hg:Guthi ; rdfs:label "g" ; hg:performsRitual ex:Doc . ex:Doc a hg:DocumentationActivity ; rdfs:label "doc" .',
}
caught = 0
for name, ttl in tests.items():
    dg = Graph()
    dg.parse(data=NEG_PFX + ttl, format="turtle")
    c, _, _ = validate(dg, shacl_graph=shapes, ont_graph=ont,
                       inference="none", abort_on_first=False)
    caught += (not c)
    print(f"  [{'CAUGHT' if not c else 'MISSED'}] {name}")
print(f"Negative tests caught: {caught}/{len(tests)}")
