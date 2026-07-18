#!/usr/bin/env python3
"""08: Hierarchy depth, annotation completeness, and OntoQA-style richness
metrics computed directly over ontology/HeritageGraph.ttl with rdflib.

Definitions used (cited in the report):
- Subclass hierarchy depth: longest path of asserted rdfs:subClassOf edges
  between NAMED classes (blank-node restrictions excluded), from a root
  (named class with no named asserted superclass) to a leaf.
- Annotation completeness: fraction of declared entities per type having
  rdfs:label / (skos:definition or rdfs:comment).
- OntoQA (Tartir et al. 2005, "OntoQA: Metric-Based Ontology Quality Analysis"):
  * Relationship Richness RR = |P| / (|P| + |H|), P = named object properties
    (non-inheritance relations), H = named-class-to-named-class subClassOf edges.
  * Inheritance Richness IR = |H| / |C|, average subclass edges per named class.
  * Attribute Richness AR = |ATT| / |C|, ATT = declared datatype properties.
  * Class Richness CR = |C_used| / |C|, classes that have at least one instance.
- Tangledness (Gangemi et al. 2005): named classes with >1 named asserted parent.
Run: venv/bin/python3 evaluation-independent/scripts/08_structure_annotations_ontoqa.py
"""
import rdflib
from rdflib import RDF, RDFS, OWL, URIRef
from rdflib.namespace import SKOS

g = rdflib.Graph()
g.parse("ontology/HeritageGraph.ttl", format="turtle")
print(f"# rdflib {rdflib.__version__} over ontology/HeritageGraph.ttl ({len(g)} triples)")

def named(nodes):
    return {n for n in nodes if isinstance(n, URIRef)}

classes = named(g.subjects(RDF.type, OWL.Class))
obj_props = named(g.subjects(RDF.type, OWL.ObjectProperty))
dt_props = named(g.subjects(RDF.type, OWL.DatatypeProperty))
ann_props = named(g.subjects(RDF.type, OWL.AnnotationProperty))
named_individuals = named(g.subjects(RDF.type, OWL.NamedIndividual))

print(f"declared owl:Class (named): {len(classes)}")
print(f"declared owl:ObjectProperty: {len(obj_props)}")
print(f"declared owl:DatatypeProperty: {len(dt_props)}")
print(f"declared owl:AnnotationProperty: {len(ann_props)}")
print(f"declared owl:NamedIndividual: {len(named_individuals)}")

# individuals = subjects typed with a class that is not an OWL/RDFS meta-class
meta = {OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty,
        OWL.Ontology, OWL.NamedIndividual, OWL.Restriction, RDFS.Datatype}
inds = set()
ind_types = {}
for s, o in g.subject_objects(RDF.type):
    if isinstance(s, URIRef) and isinstance(o, URIRef) and o not in meta:
        inds.add(s)
        ind_types.setdefault(s, set()).add(o)
print(f"individuals (URI subjects with a non-meta rdf:type): {len(inds)}")
tcount = {}
for s, ts in ind_types.items():
    for t in ts:
        tcount[t] = tcount.get(t, 0) + 1
print("instance types (top):")
for t, c in sorted(tcount.items(), key=lambda x: -x[1]):
    print(f"  {c:5d}  {t}")

# --- subclass hierarchy over NAMED classes ---
sub_edges = [(s, o) for s, o in g.subject_objects(RDFS.subClassOf)
             if isinstance(s, URIRef) and isinstance(o, URIRef)]
H = len(sub_edges)
print(f"named-to-named rdfs:subClassOf edges (H): {H}")
all_sub_edges = list(g.subject_objects(RDFS.subClassOf))
print(f"all rdfs:subClassOf triples (incl. restrictions): {len(all_sub_edges)}")

children = {}
parents = {}
hier_nodes = set()
for s, o in sub_edges:
    children.setdefault(o, set()).add(s)
    parents.setdefault(s, set()).add(o)
    hier_nodes |= {s, o}

roots = {n for n in hier_nodes if n not in parents}
print(f"hierarchy roots (named, no named parent): {len(roots)}")
for r in sorted(roots):
    print(f"  ROOT: {r}")

# longest path via DFS with cycle guard
import sys
sys.setrecursionlimit(10000)
memo = {}
def depth(n, stack):
    if n in memo:
        return memo[n]
    if n in stack:
        print(f"  CYCLE detected at {n}")
        return 0
    stack.add(n)
    d = 1 + max((depth(c, stack) for c in children.get(n, ())), default=0)
    stack.discard(n)
    memo[n] = d
    return d

maxd = max((depth(r, set()) for r in roots), default=0)
print(f"max asserted subclass hierarchy depth (nodes on longest root->leaf path): {maxd}")

leaves = {n for n in hier_nodes if n not in children}
def depth_up(n, stack):
    if n in stack:
        return 0
    ps = parents.get(n)
    if not ps:
        return 1
    stack.add(n)
    d = 1 + max(depth_up(p, stack) for p in ps)
    stack.discard(n)
    return d
leaf_depths = [depth_up(l, set()) for l in leaves]
print(f"leaf classes: {len(leaves)}; avg leaf depth: {sum(leaf_depths)/len(leaf_depths):.3f}")

multi = {n: ps for n, ps in parents.items() if len(ps) > 1}
print(f"tangledness: named classes with >1 named parent: {len(multi)}")
for n, ps in sorted(multi.items()):
    print(f"  MULTI: {n} -> {sorted(ps)}")

isolated = classes - hier_nodes
print(f"declared classes not in named subclass hierarchy: {len(isolated)}")

# --- annotation completeness ---
def coverage(ents, label):
    n = len(ents)
    if n == 0:
        print(f"{label}: n=0 (no entities of this type)")
        return
    lab = sum(1 for e in ents if (e, RDFS.label, None) in g)
    dfn = sum(1 for e in ents if (e, SKOS.definition, None) in g or (e, RDFS.comment, None) in g)
    print(f"{label}: n={n} rdfs:label={lab} ({100*lab/n:.1f}%) skos:definition|rdfs:comment={dfn} ({100*dfn/n:.1f}%)")

coverage(classes, "classes")
coverage(obj_props, "object properties")
coverage(dt_props, "datatype properties")
coverage(ann_props, "annotation properties")
coverage(named_individuals, "named individuals")

# --- OntoQA ---
C = len(classes)
P = len(obj_props)
ATT = len(dt_props)
rr = P / (P + H)
ir = H / C
ar = ATT / C
used = {t for t in tcount if t in classes}
cr = len(used) / C
print(f"OntoQA RR = P/(P+H) = {P}/({P}+{H}) = {rr:.4f}")
print(f"OntoQA IR = H/C = {H}/{C} = {ir:.4f}")
print(f"OntoQA AR = ATT/C = {ATT}/{C} = {ar:.4f}")
print(f"OntoQA CR = classes-with-instances/C = {len(used)}/{C} = {cr:.4f}")

# --- domain/range coverage of properties (declared rdfs:domain / rdfs:range) ---
for props, lbl in ((obj_props, "object"), (dt_props, "datatype")):
    dom = sum(1 for p in props if (p, RDFS.domain, None) in g)
    rng = sum(1 for p in props if (p, RDFS.range, None) in g)
    print(f"{lbl} properties with rdfs:domain: {dom}/{len(props)}; rdfs:range: {rng}/{len(props)}")

# --- inverse / characteristics ---
inv = len(list(g.subject_objects(OWL.inverseOf)))
print(f"owl:inverseOf triples: {inv}")
for ch in (OWL.FunctionalProperty, OWL.InverseFunctionalProperty, OWL.TransitiveProperty,
           OWL.SymmetricProperty):
    print(f"{ch.split('#')[-1]}: {len(named(g.subjects(RDF.type, ch)))}")

# equivalence/mapping annotations to external vocabularies
for p in (OWL.equivalentClass, OWL.equivalentProperty, SKOS.exactMatch, SKOS.closeMatch,
          SKOS.broadMatch, SKOS.narrowMatch, SKOS.relatedMatch, RDFS.subPropertyOf):
    print(f"{p.n3(g.namespace_manager)} triples: {len(list(g.subject_objects(p)))}")
