#!/usr/bin/env python3
"""Execute demonstrator SELECT CQs over TBox+ABox; run SHACL conformance + negative tests."""
from pathlib import Path
from rdflib import Graph
from pyshacl import validate
ROOT=str(Path(__file__).resolve().parents[1])+"/"
PFX="""PREFIX hg:<https://w3id.org/heritagegraph/>
PREFIX crm:<http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>"""

g=Graph(); g.parse(ROOT+"ontology/HeritageGraph.ttl",format="turtle"); g.parse(ROOT+"examples/kathmandu-mini-abox.ttl",format="turtle")
print("TBox+ABox triples:", len(g))
CQ={
"CQ-A1 conflicting source-attributed build dates":
 PFX+"""SELECT ?value ?source ?agent ?conf WHERE {
  ?a a hg:HeritageAssertion ; hg:asserts_about_entity ?e ;
     hg:asserted_value ?value ; hg:was_derived_from_source ?source ;
     hg:was_attributed_to_agent ?agent ; hg:confidence_score ?conf . }""",
"CQ-A2 event-mediated construction (temple/style/place)":
 PFX+"""SELECT ?temple ?style ?place WHERE {
  ?p a hg:Production ; hg:produced_object ?temple .
  ?temple hg:has_architectural_style ?style ; crm:P55_has_current_location ?place . }""",
"CQ-A3 Guthi custody + ritual":
 PFX+"""SELECT ?guthi ?asset ?ritual WHERE {
  ?guthi a hg:Guthi ; hg:holds_custody_of ?asset ; hg:performs_ritual ?ritual . }""",
"CQ-A4 Living-Goddess tenure (deity + institution)":
 PFX+"""SELECT ?tenure ?deity ?inst WHERE {
  ?tenure a hg:LivingGoddessTenure ; hg:embodied_deity ?deity ;
          hg:supported_by_institution ?inst . }""",
"CQ-A5 syncretic equivalence + type":
 PFX+"""SELECT ?primary ?equiv ?type WHERE {
  ?s a hg:SyncreticRelationship ; hg:assigned_to_deity ?primary ;
     hg:assigned_equivalent ?equiv ; hg:syncretic_type ?type . }""",
"CQ-A6 recurring ritual pattern":
 PFX+"""SELECT ?ritual ?pat WHERE { ?ritual a hg:RitualEvent ; hg:recurrence_pattern ?pat . }""",
}
print("\n== SELECT competency queries (rows returned) ==")
for name,q in CQ.items():
    rows=list(g.query(q))
    print(f"[{len(rows)} rows] {name}")
    for r in rows[:2]:
        print("     -> " + " | ".join(str(x).replace('https://w3id.org/heritagegraph/demo/','').replace('https://w3id.org/heritagegraph/','hg:') for x in r))

# SHACL conformance on the valid ABox
shapes=Graph(); shapes.parse(ROOT+"ontology/HeritageGraph.shacl.ttl",format="turtle")
conforms,_,txt=validate(g, shacl_graph=shapes, inference="rdfs", abort_on_first=False)
print(f"\n== SHACL conformance (valid ABox): conforms={conforms} ==")
if not conforms:
    print(txt[:1500])

# Negative tests: inject violations, expect non-conformance.
# One test per modelling pattern (event-mediated tangible, institutional,
# ritual, syncretic, provenance, Living Goddess lifecycle) plus metadata.
# Bad instances are typed with both the HG class and its mapped external
# class so shape targeting works without a reasoner.
print("\n== SHACL negative tests (each should be caught) ==")
NEG_PFX = """@prefix hg: <https://w3id.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix crminf: <http://www.cidoc-crm.org/extensions/crminf/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <https://w3id.org/heritagegraph/demo/> .
"""
tests={
 "Event-mediated: Temple missing has_architectural_style":
  'ex:BadTemple a hg:Temple ; rdfs:label "x" ; dcterms:identifier "https://example.org/t"^^xsd:anyURI .',
 "Metadata: Temple missing dcterms:identifier":
  'ex:BadTemple a hg:Temple ; rdfs:label "x" ; hg:has_architectural_style hg:Pagoda .',
 "Institutional: Guthi missing guthi_type":
  'ex:BadGuthi a hg:Guthi ; rdfs:label "x" .',
 "Ritual: RitualEvent missing crm:P4_has_time-span":
  'ex:BadRitual a hg:RitualEvent ; rdfs:label "x" .',
 "Syncretic: SyncreticRelationship missing syncretic_type":
  'ex:BadSyn a hg:SyncreticRelationship , crm:E13_Attribute_Assignment ; rdfs:label "x" ; hg:assigned_to_deity ex:D1 ; hg:assigned_equivalent ex:D2 .',
 "Provenance: HeritageAssertion missing derivation source":
  'ex:BadAssert a hg:HeritageAssertion , crminf:I2_Belief ; rdfs:label "x" ; hg:generated_at_time "2026-06-23T00:00:00"^^xsd:dateTime .',
 "Living Goddess: tenure missing crm:P4_has_time-span":
  'ex:BadTenure a hg:LivingGoddessTenure , crm:E4_Period ; rdfs:label "x" ; hg:embodied_deity ex:D1 .',
 "Sibling separation: DocumentationActivity with ritual-only property":
  'ex:BadDoc a hg:DocumentationActivity ; rdfs:label "x" ; crm:P4_has_time-span ex:TS ; hg:ritual_type hg:NityaPuja .',
}
caught=0
for name,ttl in tests.items():
    dg=Graph()
    dg.parse(data=NEG_PFX+ttl, format="turtle")
    c,_,_=validate(dg, shacl_graph=shapes, inference="none", abort_on_first=False)
    caught+=(not c)
    print(f"  [{'CAUGHT' if not c else 'MISSED'}] {name}")
print(f"Negative tests caught: {caught}/{len(tests)}")
