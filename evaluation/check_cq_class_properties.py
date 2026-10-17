#!/usr/bin/env python3
"""Every class-property pattern in the competency questions must be declared.

For each query in examples/queries/cq-abox-32.rq, every triple pattern
`?x p ?y` whose subject the same query types with a constant class
(`?x a C`) must use a property the SHACL shapes declare for C or for one of
its superclasses (rdfs:subClassOf in the released ontology). A subject typed
with several classes passes if any of them declares the property. Property
paths are checked element-wise: each alternative of `p1|p2` must be declared,
the first step of a sequence applies to the subject, and an inverse step
`^p` is checked against the class of the object instead.

A CQ that only works because the shapes are open (a property the schema never
declares for that class) fails the check, so the schema, the queries and the
demonstrator cannot drift apart. Classes with no NodeShape (external classes
the schema does not shape) are reported and skipped.

Exit status is non-zero if any undeclared class-property pair is found.

Run:  python3 evaluation/check_cq_class_properties.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Variable
from rdflib.paths import AlternativePath, InvPath, MulPath, SequencePath
from rdflib.plugins.sparql.parser import parseQuery
from rdflib.plugins.sparql.algebra import translateQuery

ROOT = Path(__file__).resolve().parents[1]
QUERIES = ROOT / "examples/queries/cq-abox-32.rq"
SH = Namespace("http://www.w3.org/ns/shacl#")


def load_shapes() -> tuple[dict[URIRef, set[URIRef]], Graph]:
    shapes = Graph()
    shapes.parse(ROOT / "ontology/HeritageGraph.shacl.ttl", format="turtle")
    onto = Graph()
    onto.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
    declared: dict[URIRef, set[URIRef]] = {}
    for ns in shapes.subjects(RDF.type, SH.NodeShape):
        targets = set(shapes.objects(ns, SH.targetClass)) or {ns}
        paths = {shapes.value(ps, SH.path) for ps in shapes.objects(ns, SH.property)}
        for t in targets:
            declared.setdefault(t, set()).update(p for p in paths if isinstance(p, URIRef))
    return declared, onto


def split_queries(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"^# (CQ\d+):.*$", text, flags=re.M)
    return [(parts[i], parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def triples(node) -> list[tuple]:
    """All triple patterns in a translated algebra tree (BGPs and paths)."""
    out = []
    if isinstance(node, dict):
        if node.get("triples") is not None and getattr(node, "name", "") == "BGP":
            out.extend(node["triples"])
        for v in node.values():
            out.extend(triples(v))
    elif isinstance(node, (list, tuple)):
        for v in node:
            out.extend(triples(v))
    return out


def steps(subject, path, obj) -> list[tuple]:
    """(subject, property) pairs a path constrains: alternatives each, the
    first step of a sequence, inverse steps flipped onto the object."""
    if isinstance(path, URIRef):
        return [(subject, path)]
    if isinstance(path, AlternativePath):
        return [s for a in path.args for s in steps(subject, a, obj)]
    if isinstance(path, SequencePath):
        return steps(subject, path.args[0], None)
    if isinstance(path, InvPath):
        return steps(obj, path.arg, subject) if obj is not None else []
    if isinstance(path, MulPath):
        return steps(subject, path.path, obj)
    return []


def main() -> int:
    declared, onto = load_shapes()

    def supers(c: URIRef) -> set[URIRef]:
        return {c} | {s for s in onto.transitive_objects(c, RDFS.subClassOf) if isinstance(s, URIRef)}

    # negative control: a declared property on a class that does not carry it
    control = ("CONTROL", "PREFIX hg: <https://cair-nepal.org/heritagegraph/>\n"
               "SELECT ?t WHERE { ?t a hg:Temple ; hg:embodiedDeity ?d . }")
    failures, checked, skipped = [], 0, set()
    for cq, body in split_queries(QUERIES.read_text(encoding="utf-8")) + [control]:
        algebra = translateQuery(parseQuery(body)).algebra
        tps = triples(algebra)
        types: dict = {}
        for s, p, o in tps:
            if p == RDF.type and isinstance(s, Variable) and isinstance(o, URIRef):
                types.setdefault(s, set()).add(o)
        for s, p, o in tps:
            if p == RDF.type:
                continue
            for subj, prop in steps(s, p, o):
                if subj not in types or prop == RDF.type:
                    continue
                classes = types[subj]
                shaped = {c for c in classes if any(x in declared for x in supers(c))}
                if not shaped:
                    skipped.update(classes)
                    continue
                checked += 1
                if not any(prop in declared.get(x, ()) for c in shaped for x in supers(c)):
                    failures.append(f"{cq}: ?{subj} a {', '.join(sorted(c.n3(onto.namespace_manager) for c in shaped))}"
                                    f" uses {prop.n3(onto.namespace_manager)}, which no shape declares for it")
    caught = any(f.startswith("CONTROL:") for f in failures)
    failures = [f for f in failures if not f.startswith("CONTROL:")]
    print(f"Class-property patterns checked in {QUERIES.name}: {checked - 1}")
    print(f"negative control (?t a hg:Temple ; hg:embodiedDeity ?d): {'caught' if caught else 'NOT caught'}")
    if not caught:
        failures.append("negative control not caught")
    if skipped:
        print("  skipped (no NodeShape): " + ", ".join(sorted(c.n3(onto.namespace_manager) for c in skipped)))
    for f in failures:
        print("  UNDECLARED:", f)
    if failures:
        print(f"FAIL: {len(failures)} class-property pattern(s) rely on open shapes.")
        return 1
    print("PASS: every class-property pattern in the CQs is declared in the shapes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
