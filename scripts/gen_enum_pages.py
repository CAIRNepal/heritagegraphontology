#!/usr/bin/env python3
"""Write one HTML page per enumeration, with an anchor for every value.

Enumeration individuals are hash IRIs (https://cair-nepal.org/heritagegraph/
ConditionType#Damaged). A browser never sends the fragment to the server, but
it keeps it across a redirect whose Location has no fragment of its own. The
nginx rules therefore send HTML requests for an enumeration IRI to
docs/enum/<Enum>.html (no fragment), and the browser lands on #Damaged there.
Each page carries id="<value>" for every permissible value (per-enumeration
pages keep value names that clash with class names, e.g. Stupa, apart).

Run: python3 scripts/gen_enum_pages.py [docs-dir]   (default: ./docs)
"""
from __future__ import annotations

import html
import sys
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS
from rdflib.collection import Collection
from rdflib.namespace import SKOS, VANN

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "ontology" / "HeritageGraph.ttl"


def text(g: Graph, node, *preds) -> str:
    for p in preds:
        v = g.value(node, p)
        if v is not None:
            return str(v)
    return ""


def main(argv: list[str]) -> int:
    docs = Path(argv[0]) if argv else ROOT / "docs"
    g = Graph()
    g.parse(TTL, format="turtle")
    ont = next(g.subjects(RDF.type, OWL.Ontology))
    ns = str(g.value(ont, VANN.preferredNamespaceUri))
    out = docs / "enum"
    out.mkdir(parents=True, exist_ok=True)
    n_pages = n_values = 0
    for cls, lst in sorted(g.subject_objects(OWL.oneOf)):
        if not str(cls).startswith(ns):
            continue
        name = str(cls)[len(ns):]
        scheme = next((s for s in g.subjects(RDF.type, SKOS.ConceptScheme)
                       if str(s) == f"{ns}scheme/{name}"), None)
        rows = []
        for ind in Collection(g, lst):
            iri = str(ind)
            value = text(g, ind, SKOS.prefLabel) or iri.rsplit("#", 1)[-1]
            anchor = iri.rsplit("#", 1)[-1] if iri.startswith(f"{ns}{name}#") else value
            rows.append(
                f'<tr id="{html.escape(anchor)}"><td><code>{html.escape(value)}</code></td>'
                f'<td><a href="{html.escape(iri)}">{html.escape(iri)}</a></td>'
                f"<td>{html.escape(text(g, ind, SKOS.definition, RDFS.comment))}</td></tr>")
            n_values += 1
        page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(name)} — HeritageGraph enumeration</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem auto; max-width: 60rem; padding: 0 1rem; }}
table {{ border-collapse: collapse; width: 100%; }}
td, th {{ border-bottom: 1px solid #ccc; padding: .4rem .6rem; text-align: left; vertical-align: top; }}
tr:target {{ background: #fff3bf; }}
</style></head>
<body>
<h1>{html.escape(name)}</h1>
<p><code>{html.escape(str(cls))}</code></p>
<p>{html.escape(text(g, cls, SKOS.definition, RDFS.comment))}</p>
{f'<p>Concept scheme: <code>{html.escape(str(scheme))}</code></p>' if scheme is not None else ''}
<table>
<thead><tr><th>Value</th><th>IRI</th><th>Definition</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
<p><a href="../#{html.escape(name)}">{html.escape(name)} in the HeritageGraph documentation</a></p>
</body></html>
"""
        (out / f"{name}.html").write_text(page, encoding="utf-8")
        n_pages += 1
    print(f"wrote {n_pages} enumeration page(s) with {n_values} value anchor(s) -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
