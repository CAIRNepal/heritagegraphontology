#!/usr/bin/env python3
"""12: Local pitfall scan over ontology/HeritageGraph.ttl.
The OOPS! web service (Poveda-Villalon et al. 2014, "OOPS! (OntOlogy Pitfall
Scanner!): An On-line Tool for Ontology Evaluation", IJSWIS 10(2)) returned
'unexpected_error'/'wrong_execution' for this file (see raw/09_oops_*.xml),
so the mechanically computable pitfalls from its public catalogue
(https://oops.linkeddata.es/catalogue.jsp) are re-implemented here with SPARQL/
rdflib. Each check below names the OOPS! pitfall it approximates. These are
approximations of the catalogue definitions, not the OOPS! implementation.
Run: venv/bin/python3 evaluation-independent/scripts/12_local_pitfall_scan.py
"""
import re
import rdflib
from rdflib import RDF, RDFS, OWL, URIRef
from rdflib.namespace import SKOS, DCTERMS

g = rdflib.Graph()
g.parse("ontology/HeritageGraph.ttl", format="turtle")
HG = "https://w3id.org/heritagegraph/"

def named(nodes):
    return {n for n in nodes if isinstance(n, URIRef)}

classes = named(g.subjects(RDF.type, OWL.Class))
obj_props = named(g.subjects(RDF.type, OWL.ObjectProperty))
dt_props = named(g.subjects(RDF.type, OWL.DatatypeProperty))
props = obj_props | dt_props

print("== P07: Merging different concepts in the same class (lexical: 'And'/'Or' in local name) ==")
hits = [c for c in classes if re.search(r"(And|Or)[A-Z]", c.split("/")[-1])]
print(f"P07 candidates: {len(hits)}")
for h in hits: print(f"  {h}")

print("\n== P10: Missing disjointness axioms ==")
dis_pairs = len(list(g.subject_objects(OWL.disjointWith)))
alldis = len(list(g.subjects(RDF.type, OWL.AllDisjointClasses)))
print(f"owl:disjointWith triples: {dis_pairs}")
print(f"owl:AllDisjointClasses axioms: {alldis}")
for s in g.subjects(RDF.type, OWL.AllDisjointClasses):
    members = list(g.objects(s, OWL.members))
    for m in members:
        items = list(rdflib.collection.Collection(g, m))
        print(f"  AllDisjointClasses with {len(items)} members: {[str(i).split('/')[-1] for i in items]}")
print(f"named classes: {len(classes)} -> disjointness axiom coverage is limited to the above")

print("\n== P11: Missing domain or range in properties ==")
no_dom = [p for p in props if (p, RDFS.domain, None) not in g]
no_rng = [p for p in props if (p, RDFS.range, None) not in g]
print(f"properties without rdfs:domain: {len(no_dom)}/{len(props)}")
print(f"properties without rdfs:range: {len(no_rng)}/{len(props)}")

print("\n== P13: Inverse relationships not explicitly declared ==")
inv_declared = {s for s, o in g.subject_objects(OWL.inverseOf)} | {o for s, o in g.subject_objects(OWL.inverseOf) if isinstance(o, URIRef)}
print(f"object properties participating in owl:inverseOf: {len(inv_declared & obj_props)}/{len(obj_props)}")

print("\n== P19: Multiple domains or ranges (unintended intersection semantics) ==")
multi_rng = {p: list(g.objects(p, RDFS.range)) for p in props if len(list(g.objects(p, RDFS.range))) > 1}
print(f"properties with >1 rdfs:range: {len(multi_rng)}")
for p, rs in multi_rng.items():
    print(f"  {p} ranges: {[str(r) for r in rs]}")
multi_dom = {p: list(g.objects(p, RDFS.domain)) for p in props if len(list(g.objects(p, RDFS.domain))) > 1}
print(f"properties with >1 rdfs:domain: {len(multi_dom)}")

print("\n== P22: Using different naming conventions ==")
def convention(local):
    if "_" in local: return "snake_case"
    if re.match(r"^[a-z]+([A-Z][a-z0-9]*)+$", local): return "camelCase"
    if re.match(r"^[A-Z][a-z0-9]+([A-Z][a-z0-9]*)*$", local): return "PascalCase"
    if re.match(r"^[a-z0-9]+$", local): return "lowercase"
    return "other"
from collections import Counter
cls_conv = Counter(convention(c.split("/")[-1]) for c in classes if c.startswith(HG))
prp_conv = Counter(convention(p.split("/")[-1]) for p in props if p.startswith(HG))
print(f"class IRI conventions (heritageGraph namespace): {dict(cls_conv)}")
print(f"property IRI conventions (heritageGraph namespace): {dict(prp_conv)}")
mixed = [p.split("/")[-1] for p in props if p.startswith(HG) and convention(p.split("/")[-1]) == "snake_case"]
print(f"snake_case property local names (sample up to 15): {sorted(mixed)[:15]}")

print("\n== P24: Using recursive definitions (entity used in its own definition) ==")
rec = []
for c in classes:
    for r in g.objects(c, RDFS.subClassOf):
        if not isinstance(r, URIRef):
            for o in g.objects(r, OWL.allValuesFrom):
                if o == c: rec.append((c, "allValuesFrom self"))
            for o in g.objects(r, OWL.someValuesFrom):
                if o == c: rec.append((c, "someValuesFrom self"))
print(f"P24 candidates (class restricted to itself): {len(rec)}")
for c, why in rec: print(f"  {c} ({why})")

print("\n== P25: Relationship declared inverse to itself ==")
selfinv = [s for s, o in g.subject_objects(OWL.inverseOf) if s == o]
print(f"self-inverse properties: {len(selfinv)}")

print("\n== P34/P38: Untyped classes / no ontology declaration ==")
used_as_class = set()
for s, o in g.subject_objects(RDFS.subClassOf):
    if isinstance(s, URIRef): used_as_class.add(s)
    if isinstance(o, URIRef): used_as_class.add(o)
for o in g.objects(None, RDF.type):
    if isinstance(o, URIRef) and o not in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty,
        OWL.AnnotationProperty, OWL.Ontology, OWL.NamedIndividual, OWL.Restriction,
        RDFS.Datatype, OWL.AllDisjointClasses):
        used_as_class.add(o)
for r in g.subjects(RDF.type, OWL.Restriction):
    for o in g.objects(r, OWL.allValuesFrom):
        if isinstance(o, URIRef) and not str(o).startswith(str(rdflib.XSD)): used_as_class.add(o)
untyped = {c for c in used_as_class
           if (c, RDF.type, OWL.Class) not in g and (c, RDF.type, RDFS.Class) not in g
           and not str(c).startswith(str(rdflib.XSD)) and c != OWL.Thing and c != RDFS.Literal}
print(f"IRIs used as classes but not declared owl:Class: {len(untyped)}")
for c in sorted(untyped): print(f"  {c}")
print(f"owl:Ontology declared: {(None, RDF.type, OWL.Ontology) in g}")

print("\n== P41: No license declared ==")
lic = list(g.objects(None, DCTERMS.license))
print(f"dcterms:license values: {[str(x) for x in lic]}")

print("\n== P36/P37: Ontology IRI vs file, hash vs slash (informational) ==")
for o in g.subjects(RDF.type, OWL.Ontology):
    print(f"ontology IRI: {o}")

print("\n== deprecated entities ==")
dep = list(g.subjects(OWL.deprecated, None))
for d in dep:
    print(f"owl:deprecated: {d} = {list(g.objects(d, OWL.deprecated))}")
    refs = [(s, p) for s, p, o in g if o == d and p != RDF.type]
    onprop = [r for r in g.subjects(OWL.onProperty, d)]
    print(f"  referenced as object by {len(refs)} triples; used in {len(onprop)} restrictions")
