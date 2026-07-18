#!/usr/bin/env python3
"""01: Parse HeritageGraph.ttl with rdflib; report syntax validity, triple count,
ontology IRI, owl:imports, and all ontology-header annotations.
Run: venv/bin/python3 evaluation-independent/scripts/01_parse_and_header.py
"""
import sys
import rdflib
from rdflib import RDF, OWL

ONT = "ontology/HeritageGraph.ttl"

g = rdflib.Graph()
try:
    g.parse(ONT, format="turtle")
    print(f"PARSE: OK (rdflib {rdflib.__version__}, format=turtle)")
except Exception as e:
    print(f"PARSE: FAILED: {e}")
    sys.exit(1)

print(f"TRIPLES: {len(g)}")

onts = list(g.subjects(RDF.type, OWL.Ontology))
print(f"owl:Ontology declarations: {len(onts)}")
for o in onts:
    print(f"ONTOLOGY_IRI: {o}")
    for p, obj in sorted(g.predicate_objects(o)):
        print(f"  HEADER: {p.n3(g.namespace_manager)} {obj.n3(g.namespace_manager)}")

imports = list(g.objects(None, OWL.imports))
print(f"owl:imports count: {len(imports)}")
for i in imports:
    print(f"  IMPORT: {i}")
