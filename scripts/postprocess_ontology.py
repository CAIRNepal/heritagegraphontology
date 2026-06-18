#!/usr/bin/env python3
"""Post-process HeritageGraph.ttl to repair two LinkML generation gaps:
   (1) materialise owl:disjointWith from the YAML's disjoint_with (gen-owl drops it);
   (2) remove self-referential skos:*Match loops (caused by redundant class_uri).
Idempotent. Run after gen-owl / regenerate_ontology_artifacts.py.
"""
from pathlib import Path
import yaml
from rdflib import Graph, OWL, URIRef
from rdflib.namespace import SKOS
ROOT=Path(__file__).resolve().parents[1]
TTL=ROOT/"ontology"/"HeritageGraph.ttl"; YAML=ROOT/"ontology"/"HeritageGraph.yaml"
HG="https://w3id.org/heritagegraph/"
d=yaml.safe_load(open(YAML)); classes=d.get("classes",{})
g=Graph(); g.parse(TTL,format="turtle")

# (2) drop self-referential mapping loops (s == o)
match_preds=(SKOS.exactMatch,SKOS.closeMatch,SKOS.broadMatch,SKOS.narrowMatch,SKOS.relatedMatch)
removed=0
for p in match_preds:
    for s,o in list(g.subject_objects(p)):
        if s==o:
            g.remove((s,p,o)); removed+=1
print(f"Removed {removed} self-referential skos match loops")

# (1) add owl:disjointWith (dedup unordered pairs); only for class pairs that both exist
existing={URIRef(HG+c) for c in classes}
pairs=set()
for cname,cdef in classes.items():
    if not isinstance(cdef,dict): continue
    dw=cdef.get("disjoint_with") or []
    if isinstance(dw,str): dw=[dw]
    a=URIRef(HG+cname)
    for other in dw:
        b=URIRef(HG+other)
        if a in existing and b in existing and a!=b:
            pairs.add(frozenset((a,b)))
added=0
for pr in pairs:
    a,b=tuple(pr)
    if (a,OWL.disjointWith,b) not in g and (b,OWL.disjointWith,a) not in g:
        g.add((a,OWL.disjointWith,b)); added+=1
print(f"Added {added} owl:disjointWith axioms (from {sum(1 for c in classes if isinstance(classes[c],dict) and classes[c].get('disjoint_with'))} disjoint_with declarations)")

g.serialize(destination=TTL,format="turtle")
print("Wrote", TTL)
