#!/usr/bin/env python3
"""Post-process the generated SHACL shapes so that sh:closed does not reject
legitimate uses of the ontology's own vocabulary.

The LinkML-generated shapes are declared sh:closed, which we keep: closedness
catches typo predicates and structural drift. But the generator lists only the
properties attached to a class in the source schema, so three kinds of
legitimate usage were rejected by the closure check rather than by any real
constraint:

1. deliberately domain-less (polymorphic) properties, whose subjects may come
   from several disjoint branches (e.g. holds_custody_of);
2. properties inherited from a superclass but not re-declared on the subclass
   (e.g. carried_out_by on a Production); and
3. triples materialised by RDFS inference along rdfs:subPropertyOf mappings
   (e.g. crm:P7_took_place_at inferred from took_place_at), plus direct
   rdfs:label annotations.

This script therefore extends each closed NodeShape's sh:ignoredProperties
with the ontology's full property vocabulary: every HeritageGraph object and
datatype property, the transitive rdfs:subPropertyOf closure of those
properties (the external CRM/PROV terms they ground into), and rdfs:label.
Closedness then rejects exactly the predicates unknown to the ontology.
minCount/maxCount/datatype/sh:in constraints are unaffected, so the negative
tests still fire.

One deliberate exception: for sibling classes that are NOT separated by
owl:disjointWith (the ontology has exactly one such group, RitualEvent /
DocumentationActivity under HeritageActivity), each sibling's shape keeps
rejecting the properties declared only on the other sibling. SHACL closedness
is the separation mechanism for that group, and this exception preserves it.

Run after `linkml generate shacl` (it is invoked by
regenerate_ontology_artifacts.py).
"""

from __future__ import annotations

from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.collection import Collection

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
SHACL = ROOT / "ontology" / "HeritageGraph.shacl.ttl"
SH = Namespace("http://www.w3.org/ns/shacl#")


def superproperty_closure(g: Graph, props: set[URIRef]) -> set[URIRef]:
    seen, todo = set(), list(props)
    while todo:
        p = todo.pop()
        if p in seen or not isinstance(p, URIRef):
            continue
        seen.add(p)
        todo.extend(o for o in g.objects(p, RDFS.subPropertyOf) if isinstance(o, URIRef))
    return seen


def nondisjoint_sibling_groups(tbox: Graph) -> list[set[URIRef]]:
    hg = "https://w3id.org/heritagegraph/"
    kids_by_parent: dict[URIRef, set[URIRef]] = {}
    for c, p in tbox.subject_objects(RDFS.subClassOf):
        if str(c).startswith(hg) and str(p).startswith(hg):
            kids_by_parent.setdefault(p, set()).add(c)
    disjoint = {frozenset((a, b)) for a, b in tbox.subject_objects(OWL.disjointWith)}
    groups = []
    for kids in kids_by_parent.values():
        if len(kids) < 2:
            continue
        kl = sorted(kids)
        if not any(frozenset((kl[i], kl[j])) in disjoint
                   for i in range(len(kl)) for j in range(i + 1, len(kl))):
            groups.append(kids)
    return groups


def main() -> int:
    tbox = Graph()
    tbox.parse(TTL, format="turtle")

    props = set(tbox.subjects(RDF.type, OWL.ObjectProperty)) | set(
        tbox.subjects(RDF.type, OWL.DatatypeProperty)
    )
    vocabulary = superproperty_closure(tbox, props) | {RDFS.label}

    shapes = Graph()
    shapes.parse(SHACL, format="turtle")
    for prefix, ns in tbox.namespaces():
        shapes.bind(prefix, ns, override=False)

    def declared_paths(shape: URIRef) -> set[URIRef]:
        return {shapes.value(ps, SH.path) for ps in shapes.objects(shape, SH.property)}

    # per-shape exclusions preserving SHACL separation of non-disjoint siblings
    exclusions: dict[URIRef, set[URIRef]] = {}
    for group in nondisjoint_sibling_groups(tbox):
        for cls in group:
            if (cls, RDF.type, SH.NodeShape) not in shapes:
                continue
            others = set()
            for sib in group - {cls}:
                if (sib, RDF.type, SH.NodeShape) in shapes:
                    others |= declared_paths(sib)
            excl = others - declared_paths(cls)
            if excl:
                exclusions[cls] = excl
                names = sorted(str(p).split("/")[-1] for p in excl)
                print(f"Sibling separation kept on {str(cls).split('/')[-1]}: "
                      f"still rejects {len(names)} sibling-only properties")

    patched = 0
    for shape in shapes.subjects(RDF.type, SH.NodeShape):
        if shapes.value(shape, SH.closed) != Literal(True):
            continue
        node = shapes.value(shape, SH.ignoredProperties)
        coll = Collection(shapes, node) if node is not None else None
        existing = set(coll) if coll is not None else set()
        additions = sorted(vocabulary - existing - exclusions.get(shape, set()))
        if not additions:
            continue
        if coll is None:
            head = BNode()
            Collection(shapes, head, additions)
            shapes.add((shape, SH.ignoredProperties, head))
        else:
            for p in additions:
                coll.append(p)
        patched += 1

    shapes.serialize(destination=SHACL, format="turtle")
    print(f"Patched sh:ignoredProperties on {patched} closed shapes; "
          f"vocabulary size {len(vocabulary)} "
          f"({len(props)} HG properties + superproperty closure + rdfs:label).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
