#!/usr/bin/env python3
"""After `make artefacts`, the regenerated artefacts must equal the committed ones.

Compares each generated file in the working tree with the version committed
at HEAD (git show HEAD:<path>): RDF files as graphs (blank nodes compared by
their tree structure, so serialisation order does not matter; the build date
in dcterms:modified is ignored), JSON as parsed data, text files byte for
byte. A hand edit of a generated file, or a generator change not followed by
a regeneration, fails here. (check_yaml_ttl_sync.py only hashes the YAML.)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from rdflib import BNode, Graph

ROOT = Path(__file__).resolve().parents[1]
RDF_FILES = ["ontology/HeritageGraph.ttl", "ontology/HeritageGraph.shacl.ttl",
             "ontology/HeritageGraph-crm-prov-bridge.ttl"]
JSON_FILES = ["ontology/HeritageGraph.schema.json"]
TEXT_FILES = ["cq_sparql.md", "ontology/mappings/HeritageGraph.sssom.tsv"]


def committed(path: str) -> str:
    return subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT).decode("utf-8")


def canon(g: Graph) -> set[str]:
    def node(n, depth=0):
        if isinstance(n, BNode):
            if depth > 60:
                return "<deep>"
            return "[" + ";".join(sorted(f"{p} {node(o, depth + 1)}"
                                         for p, o in g.predicate_objects(n))) + "]"
        return n.n3()
    out = {f"{s.n3()} {p} {node(o)}" for s, p, o in g
           if not isinstance(s, BNode) and "modified" not in str(p)}
    # top-level blank nodes (no triple points to them, e.g. [] a owl:AllDisjointClasses)
    referenced = {o for o in g.objects() if isinstance(o, BNode)}
    for b in {s for s in g.subjects() if isinstance(s, BNode)} - referenced:
        out.add("TOP " + node(b))
    return out


ok = True
for f in RDF_FILES:
    fmt = "xml" if f.endswith(".owl") else "turtle"
    a = canon(Graph().parse(data=committed(f), format=fmt))
    b = canon(Graph().parse(ROOT / f, format=fmt))
    same = a == b
    ok &= same
    print(f"  [{'OK' if same else 'DIFFERS'}] {f}" + ("" if same else
          f": {len(a - b)} committed-only, {len(b - a)} regenerated-only statement(s)"))
for f in JSON_FILES:
    same = json.loads(committed(f)) == json.loads((ROOT / f).read_text(encoding="utf-8"))
    ok &= same
    print(f"  [{'OK' if same else 'DIFFERS'}] {f}")
for f in TEXT_FILES:
    same = committed(f) == (ROOT / f).read_text(encoding="utf-8")
    ok &= same
    print(f"  [{'OK' if same else 'DIFFERS'}] {f}")
print("PASS: the committed artefacts are what the generators produce." if ok else
      "FAIL: a committed artefact differs from its regeneration")
sys.exit(0 if ok else 1)
