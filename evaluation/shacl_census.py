#!/usr/bin/env python3
"""Constraint census for the published SHACL shapes.

The negative-test suite (evaluation/independent_abox.py) injects twenty-six
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

from rdflib import BNode, Graph, Namespace, RDF
from rdflib.collection import Collection

ROOT = Path(__file__).resolve().parents[1]
SH = Namespace("http://www.w3.org/ns/shacl#")

g = Graph()
g.parse(ROOT / "ontology" / "HeritageGraph.shacl.ttl", format="turtle")

node_shapes = set(g.subjects(RDF.type, SH.NodeShape))
prop_shapes = set(g.objects(None, SH.property))
print(f"Shape graph: {len(g)} triples, {len(node_shapes)} sh:NodeShapes, "
      f"{len(prop_shapes)} property shapes (sh:property links)")

# Negative-test coverage: component type -> number of the 26 tests hitting it
# (one test, a reconstructed structure without a location, exercises both
# sh:or and the sh:not inside it, so the counts sum to 27).
N_TESTS = 26
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
    "sh:sparql": 2,            # a misspelt hg: property; a conflicting belief with no rival
    "sh:minLength": 1,         # an empty label
    "sh:maxInclusive": 1,      # a confidence score above 1
}

# every constraint parameter in the SHACL namespace that the shapes use (not
# targets, names, descriptions, ordering or the parts of a SPARQL constraint)
NOT_COMPONENTS = {"path", "property", "targetClass", "targetNode", "targetSubjectsOf", "targetObjectsOf",
                  "name", "description", "order", "group", "message", "severity", "select", "prefixes",
                  "deactivated", "qualifiedValueShapesDisjoint", "qualifiedValueShape", "flags"}
preds = sorted({p for p in g.predicates() if str(p).startswith(str(SH))
                and str(p)[len(str(SH)):] not in NOT_COMPONENTS})
direct = {f"sh:{str(p)[len(str(SH)):]}": p for p in preds}


def canon(o) -> str:
    if isinstance(o, BNode):
        try:
            return "(" + " ".join(canon(m) for m in Collection(g, o)) + ")"
        except Exception:
            return "[" + ";".join(sorted(f"{p.n3()} {canon(v)}" for p, v in g.predicate_objects(o))) + "]"
    return o.n3()


paths = {canon(o) for o in g.objects(None, SH.path)}
print(f"Distinct property paths constrained: {len(paths)}")
print(f"\n{'component':<22}{'occurrences':>12}{'distinct':>10}{'negative tests':>16}")
total = 0
for name, pred in direct.items():
    occ = list(g.subject_objects(pred))
    # a distinct constraint: the same component, value and path counts once,
    # however many class shapes repeat it
    distinct = {(canon(g.value(s_, SH.path)) if g.value(s_, SH.path) is not None else "node", canon(o))
                for s_, o in occ}
    print(f"{name:<22}{len(occ):>12}{len(distinct):>10}{NEG_TESTS.get(name, 0):>16}")
    total += len(occ)

touched = [k for k in direct if NEG_TESTS.get(k)]
print(f"\nTotal component occurrences: {total}")
print(f"Component types present: {len(direct)}; "
      f"exercised by the {N_TESTS} negative tests: {len(touched)} ({', '.join(touched)})")
untouched = [k for k in direct if not NEG_TESTS.get(k)]
print(f"Untouched by negative tests: {', '.join(untouched) or 'none'}.")
missing = [k for k in NEG_TESTS if k not in direct]
if missing:
    raise SystemExit(f"census lists negative tests for components the shapes do not use: {missing}")
