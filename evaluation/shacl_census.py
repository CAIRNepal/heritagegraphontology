#!/usr/bin/env python3
"""Constraint census for the published SHACL shapes.

The negative-test suite (evaluation/independent_abox.py) injects twenty-two
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

# Negative-test coverage: component type -> number of the 22 tests hitting it
# (one test, a reconstructed structure without a location, exercises both
# sh:or and the sh:not inside it, so the counts sum to 23).
N_TESTS = 22
NEG_TESTS = {
    "sh:minCount": 6,   # missing custody holder / assigned deity / assertsAbout / time-span / destroyed /
                        # tenure holder (1.0.x hadParticipant only)
    "sh:maxCount": 1,   # two embodied deities on one tenure
    "sh:datatype": 1,   # dcterms:identifier not xsd:anyURI
    "sh:class": 3,      # non-TimeSpan time-span; DocumentationActivity in ritual slot; deity as structure type
    "sh:in": 1,         # guthiType outside the controlled vocabulary
    "sh:nodeKind": 1,   # ritual site given as a blank node
    "sh:or": 5,         # ritual performed by a person; recorded date without its calendar;
                        # a note that is not text; a destruction of a deity;
                        # a reconstructed structure without a location
    "sh:pattern": 1,    # reconciliationStatus outside confirmed|conflicting|unverified
    "sh:lessThanOrEquals": 1,  # time-span ends before it begins
    "sh:uniqueLang": 1,        # two English labels on one deity
    "sh:qualifiedMaxCount": 1, # two untagged labels on one deity
    "sh:not": 1,               # a reconstructed structure without a location (inside the sh:or)
}

direct = {
    "sh:minCount": SH.minCount,
    "sh:maxCount": SH.maxCount,
    "sh:datatype": SH.datatype,
    "sh:class": SH["class"],
    "sh:in": SH["in"],
    "sh:nodeKind": SH.nodeKind,
    "sh:or": SH["or"],
    "sh:pattern": SH.pattern,
    "sh:lessThanOrEquals": SH.lessThanOrEquals,
    "sh:uniqueLang": SH.uniqueLang,
    "sh:qualifiedMaxCount": SH.qualifiedMaxCount,
    "sh:not": SH["not"],
    "sh:minInclusive": SH.minInclusive,
    "sh:maxInclusive": SH.maxInclusive,
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
      f"exercised by the {N_TESTS} negative tests: {len(touched)} ({', '.join(touched)})")
untouched = [k for k in direct if not NEG_TESTS.get(k)]
print(f"Untouched by negative tests: {', '.join(untouched) or 'none'}.")
