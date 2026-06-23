#!/usr/bin/env python3
"""Render a focused visualization of the HeritageGraph <-> CIDOC-CRM/LUX alignment.

Unlike the full merged WebVOWL (which has a noisy owl:Thing hub), this shows ONLY
the alignment edges — every HG class and the external (CRM/CRMdig/CRMsci/Linked-Art)
class it maps to, coloured by axiom type (equivalentClass vs subClassOf).

Outputs (in evaluation/lux/):
  alignment_graph.html  — interactive, self-contained (vis-network via CDN); open in a browser
  alignment_graph.dot   — Graphviz source; render with:  dot -Tpdf alignment_graph.dot -o alignment.pdf

Usage:  python evaluation/lux/alignment_viz.py
"""
from __future__ import annotations
import json
from pathlib import Path
from rdflib import Graph, RDFS, OWL, URIRef

HERE = Path(__file__).resolve().parent
BRIDGE = HERE.parents[1] / "ontology" / "lux" / "heritagegraph-lux-alignment.ttl"
HG = "https://w3id.org/heritagegraph/"
CRM = "http://www.cidoc-crm.org/cidoc-crm/"


def short(u: str) -> str:
    return (u.replace(HG, "").replace(CRM, "crm:")
            .replace("http://www.ics.forth.gr/isl/CRMsci/", "sci:")
            .replace("http://www.ics.forth.gr/isl/CRMdig/", "dig:")
            .replace("https://linked.art/ns/terms/", "la:"))


def collect():
    g = Graph().parse(str(BRIDGE), format="turtle")
    ext = lambda o: isinstance(o, URIRef) and not str(o).startswith(HG)
    eqc = [(str(s), str(o)) for s, _, o in g.triples((None, OWL.equivalentClass, None)) if ext(o)]
    sc = [(str(s), str(o)) for s, _, o in g.triples((None, RDFS.subClassOf, None))
          if ext(o) and str(s).startswith(HG)]
    return eqc, sc


def build(eqc, sc):
    nodes, ids = {}, {}
    def nid(uri, group):
        if uri not in ids:
            ids[uri] = len(ids)
            nodes[ids[uri]] = {"id": ids[uri], "label": short(uri), "group": group}
        return ids[uri]
    edges = []
    for s, o in eqc:
        edges.append({"from": nid(s, "hg"), "to": nid(o, "ext"),
                      "kind": "equivalentClass"})
    for s, o in sc:
        edges.append({"from": nid(s, "hg"), "to": nid(o, "ext"),
                      "kind": "subClassOf"})
    return list(nodes.values()), edges


HTML = """<!doctype html><html><head><meta charset="utf-8">
<title>HeritageGraph ↔ CIDOC-CRM / LUX alignment</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
 body{{margin:0;font-family:system-ui,sans-serif}}
 #net{{width:100vw;height:92vh;border-bottom:1px solid #ccc}}
 #legend{{padding:8px 14px;font-size:14px}}
 .sw{{display:inline-block;width:14px;height:14px;border-radius:3px;vertical-align:middle;margin:0 4px 0 14px}}
</style></head><body>
<div id="legend">
 <b>HeritageGraph ↔ CIDOC-CRM / LUX alignment</b>
 <span class="sw" style="background:#4f7cff"></span>HeritageGraph class
 <span class="sw" style="background:#ff9f40"></span>CIDOC-CRM / LUX class
 <span class="sw" style="background:#2ecc71"></span>owl:equivalentClass
 <span class="sw" style="background:#999"></span>rdfs:subClassOf
</div>
<div id="net"></div>
<script>
const nodes=new vis.DataSet(NODES.map(n=>({{id:n.id,label:n.label,
  color:n.group==="hg"?"#4f7cff":"#ff9f40",font:{{color:"#fff",size:14}},shape:"box"}})));
const edges=new vis.DataSet(EDGES.map(e=>({{from:e.from,to:e.to,arrows:e.kind==="subClassOf"?"to":"",
  color:{{color:e.kind==="equivalentClass"?"#2ecc71":"#999"}},width:e.kind==="equivalentClass"?3:1}})));
new vis.Network(document.getElementById("net"),{{nodes,edges}},{{
  physics:{{stabilization:true,barnesHut:{{springLength:160,avoidOverlap:0.4}}}},
  interaction:{{hover:true,tooltipDelay:120}}}});
</script></body></html>"""


def dot(nodes, edges):
    L = ["digraph alignment {", "  rankdir=LR; node [shape=box,style=filled,fontname=Helvetica];"]
    for n in nodes:
        fill = "#cfe0ff" if n["group"] == "hg" else "#ffe3c2"
        L.append(f'  n{n["id"]} [label="{n["label"]}",fillcolor="{fill}"];')
    for e in edges:
        if e["kind"] == "equivalentClass":
            L.append(f'  n{e["from"]} -> n{e["to"]} [dir=none,color="#2ecc71",penwidth=2,label="≡"];')
        else:
            L.append(f'  n{e["from"]} -> n{e["to"]} [color="#888"];')
    L.append("}")
    return "\n".join(L)


def main():
    eqc, sc = collect()
    nodes, edges = build(eqc, sc)
    html = (HTML.replace("NODES", json.dumps(nodes)).replace("EDGES", json.dumps(edges))
            .replace("{{", "{").replace("}}", "}"))   # template used doubled braces
    (HERE / "alignment_graph.html").write_text(html)
    (HERE / "alignment_graph.dot").write_text(dot(nodes, edges))
    hg = sum(1 for n in nodes if n["group"] == "hg")
    print(f"wrote alignment_graph.html and alignment_graph.dot  "
          f"({hg} HG nodes, {len(nodes)-hg} external nodes, "
          f"{len(eqc)} equivalentClass + {len(sc)} subClassOf edges)")


if __name__ == "__main__":
    main()
