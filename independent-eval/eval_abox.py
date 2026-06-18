#!/usr/bin/env python3
"""Execute demonstrator SELECT CQs over TBox+ABox; run SHACL conformance + negative tests."""
from rdflib import Graph
from pyshacl import validate
ROOT="/Users/nirajkarki/cair/heritagegraphontology/"
PFX="""PREFIX hg:<https://w3id.org/heritagegraph/>
PREFIX crm:<http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>"""

g=Graph(); g.parse(ROOT+"HeritageGraph.ttl",format="turtle"); g.parse(ROOT+"examples/kathmandu-mini-abox.ttl",format="turtle")
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
shapes=Graph(); shapes.parse(ROOT+"HeritageGraph.shacl.ttl",format="turtle")
conforms,_,txt=validate(g, shacl_graph=shapes, inference="rdfs", abort_on_first=False)
print(f"\n== SHACL conformance (valid ABox): conforms={conforms} ==")
if not conforms:
    print(txt[:1500])

# Negative tests: inject violations, expect non-conformance
print("\n== SHACL negative tests (each should be caught) ==")
tests={
 "Temple missing has_architectural_style":
  '@prefix hg:<https://w3id.org/heritagegraph/> . @prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#> . @prefix xsd:<http://www.w3.org/2001/XMLSchema#> . @prefix crm:<http://www.cidoc-crm.org/cidoc-crm/> . @prefix ex:<https://w3id.org/heritagegraph/demo/> . ex:BadTemple a hg:Temple ; rdfs:label "x" ; dcterms:identifier "u"^^xsd:anyURI ; crm:P55_has_current_location ex:KathmanduDurbarSquare . ex:KathmanduDurbarSquare a crm:E53_Place .',
 "Guthi missing guthi_type":
  '@prefix hg:<https://w3id.org/heritagegraph/> . @prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#> . ex:BadGuthi a hg:Guthi ; rdfs:label "x" . @prefix ex:<https://w3id.org/heritagegraph/demo/> .',
 "RitualEvent missing time-span":
  '@prefix hg:<https://w3id.org/heritagegraph/> . @prefix rdfs:<http://www.w3.org/2000/01/rdf-schema#> . @prefix ex:<https://w3id.org/heritagegraph/demo/> . ex:BadRitual a hg:RitualEvent ; rdfs:label "x" .',
}
import re
for name,ttl in tests.items():
    dg=Graph()
    try:
        dg.parse(data=ttl, format="turtle")
        c,_,_=validate(dg, shacl_graph=shapes, inference="none", abort_on_first=False)
        print(f"  [{'CAUGHT' if not c else 'MISSED'}] {name}")
    except Exception as e:
        print(f"  [parse-skip] {name}: {e}")
