#!/usr/bin/env python3
"""Every example ABox against its expected SHACL outcome (a release gate).

Each examples/*.ttl must have an entry in EXPECTED: an example added without
one fails, so its expected outcome is a decision, not a default. All current
examples are expected to conform to the published shapes (with the ontology
graph mixed in, the pipeline-gate configuration); the deliberately invalid
data lives in the negative tests of independent_abox.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

from rdflib import Graph, OWL, RDF
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "abox-conflicting-assertions.ttl": True,
    "kathmandu-conformant.ttl": True,
    "kathmandu-mini-abox.ttl": True,
    "kathmandu-multilingual.ttl": True,
    "lux-murti-merged.ttl": True,
    "reuse-tenure-beyond-nepal.ttl": True,
}

shapes = Graph().parse(ROOT / "ontology/HeritageGraph.shacl.ttl", format="turtle")
ont = Graph().parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
for s in list(ont.subjects(RDF.type, OWL.NamedIndividual)):
    ont.remove((s, RDF.type, OWL.NamedIndividual))
ok = True
for f in sorted((ROOT / "examples").glob("*.ttl")):
    if f.name not in EXPECTED:
        print(f"  [FAIL] {f.name}: no expected outcome recorded in check_examples.py")
        ok = False
        continue
    conforms, _, text = validate(Graph().parse(f, format="turtle"), shacl_graph=shapes,
                                 ont_graph=ont, inference="none")
    good = conforms == EXPECTED[f.name]
    ok &= good
    print(f"  [{'PASS' if good else 'FAIL'}] {f.name}: conforms={conforms} (expected {EXPECTED[f.name]})")
    if not good:
        print(text[:1500])
print("PASS: every example has its expected SHACL outcome." if ok else "FAIL")
sys.exit(0 if ok else 1)
