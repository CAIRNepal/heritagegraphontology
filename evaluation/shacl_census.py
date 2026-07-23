#!/usr/bin/env python3
"""Constraint census for the published SHACL shapes.

The negative-test suite (evaluation/independent_abox.py) injects eight
single violations; on its own that is an anecdote. This script supplies the
systematic statement behind it: how many constraints of each SHACL component
type the published shape graph carries, and which of those component types
the negative suite exercises.

Counted over ontology/HeritageGraph.shacl.ttl (occurrences of each
constraint component across all property shapes; sh:class is counted both
directly on property shapes and inside the sh:or disjunctions the release
pipeline rewrites union ranges into).
"""
from pathlib import Path

from rdflib import Graph, Namespace, RDF
from rdflib.collection import Collection

ROOT = Path(__file__).resolve().parents[1]
SH = Namespace("http://www.w3.org/ns/shacl#")

g = Graph()
g.parse(ROOT / "ontology" / "HeritageGraph.shacl.ttl", format="turtle")

node_shapes = set(g.subjects(RDF.type, SH.NodeShape))
prop_shapes = set(g.objects(None, SH.property))
print(f"Shape graph: {len(g)} triples, {len(node_shapes)} sh:NodeShapes, "
      f"{len(prop_shapes)} property shapes (sh:property links)")

# Negative-test coverage: component type -> number of the 8 tests hitting it.
NEG_TESTS = {
    "sh:minCount": 4,   # missing style / assigned deity / assertsAbout / time-span
    "sh:datatype": 1,   # dcterms:identifier not xsd:anyURI
    "sh:in": 1,         # guthiType outside the controlled vocabulary
    "sh:class": 2,      # non-TimeSpan time-span; DocumentationActivity in ritual slot
}

direct = {
    "sh:minCount": SH.minCount,
    "sh:maxCount": SH.maxCount,
    "sh:datatype": SH.datatype,
    "sh:class": SH["class"],
    "sh:in": SH["in"],
    "sh:nodeKind": SH.nodeKind,
    "sh:or": SH["or"],
}

print(f"\n{'component':<14}{'occurrences':>12}{'negative tests':>16}")
total = 0
for name, pred in direct.items():
    n = len(list(g.subject_objects(pred)))
    if name == "sh:class":
        # also count sh:class occurrences inside sh:or disjunction members
        in_or = 0
        for _, lst in g.subject_objects(SH["or"]):
            for member in Collection(g, lst):
                in_or += len(list(g.objects(member, SH["class"])))
        note = f" ({n - in_or} direct + {in_or} inside sh:or)" if in_or else ""
        print(f"{name:<14}{n:>12}{NEG_TESTS.get(name, 0):>16}{note}")
    else:
        print(f"{name:<14}{n:>12}{NEG_TESTS.get(name, 0):>16}")
    total += n

touched = [k for k in direct if NEG_TESTS.get(k)]
print(f"\nTotal component occurrences: {total}")
print(f"Component types present: {len(direct)}; "
      f"exercised by the 8 negative tests: {len(touched)} ({', '.join(touched)})")
print("Untouched by negative tests: sh:maxCount, sh:nodeKind, sh:or.")
