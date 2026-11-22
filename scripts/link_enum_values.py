#!/usr/bin/env python3
"""Connect enumeration values to their enumeration class in the OntoReview graph.

OntoReview's class graph draws the enumeration values (SKOS concepts) as nodes
but only draws subclass, equivalence and property edges, so the values float
unconnected. This adds one labelled `type` edge (rdf:type) from every value to
the enumeration class it belongs to (the owl:oneOf class in the ontology), in
every published file that carries OntoReview's data (`window.ONTOREVIEW = {...}`:
ontoreview-data.js and the inlined copy in standalone.html).

Run: python3 scripts/link_enum_values.py [docs-dir]   (scripts/build.sh runs it)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from rdflib import Graph, OWL, RDF
from rdflib.collection import Collection

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
MARK = "window.ONTOREVIEW="


def enum_membership() -> dict[str, tuple[str, str]]:
    """value IRI -> (enumeration class IRI, class local name)"""
    g = Graph()
    g.parse(TTL, format="turtle")
    out = {}
    for cls, lst in g.subject_objects(OWL.oneOf):
        for ind in Collection(g, lst):
            out[str(ind)] = (str(cls), str(cls).rstrip("/").rsplit("/", 1)[-1])
    return out


def link(data: dict, members: dict) -> int:
    graph = data.get("graph") or {}
    nodes = {n["data"]["id"] for n in graph.get("nodes", [])}
    edges = graph.setdefault("edges", [])
    have = {e["data"]["id"] for e in edges}
    added = 0
    for value, (cls, name) in members.items():
        if value not in nodes or cls not in nodes:
            continue
        eid = f"t|{value}|{cls}"
        if eid in have:
            continue
        edges.append({"data": {"id": eid, "source": value, "target": cls, "type": "prop",
                               "label": "type", "href": f"classes.html#{name}",
                               "prop": str(RDF.type), "inv": None}})
        added += 1
    return added


def patch(path: Path, members: dict) -> int:
    text = path.read_text(encoding="utf-8")
    i = text.find(MARK)
    if i < 0:
        return 0
    start = i + len(MARK)
    data, end = json.JSONDecoder().raw_decode(text, start)
    n = link(data, members)
    if n:
        path.write_text(text[:start] + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + text[end:],
                        encoding="utf-8")
    return n


def main(argv: list[str]) -> int:
    docs = Path(argv[0]) if argv else ROOT / "docs"
    members = enum_membership()
    for name in ("ontoreview-data.js", "standalone.html"):
        p = docs / name
        if p.exists():
            print(f"   {name}: linked {patch(p, members)} enumeration value(s) to their class")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
