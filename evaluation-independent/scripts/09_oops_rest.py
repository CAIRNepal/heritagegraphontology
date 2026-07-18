#!/usr/bin/env python3
"""09: Submit ontology/HeritageGraph.ttl content to the OOPS! REST API
(https://oops.linkeddata.es/rest) and save the raw XML response.
OOPS! expects RDF/XML content, so the Turtle is converted with rdflib first
(purely syntactic transformation; no triples added or removed).
Run: venv/bin/python3 evaluation-independent/scripts/09_oops_rest.py <out_xml>
"""
import sys, urllib.request
import xml.sax.saxutils as sx
import rdflib

g = rdflib.Graph()
g.parse("ontology/HeritageGraph.ttl", format="turtle")
rdfxml = g.serialize(format="xml")
print(f"converted to RDF/XML: {len(g)} triples, {len(rdfxml)} chars")

body = f"""<?xml version="1.0" encoding="UTF-8"?>
<OOPSRequest>
  <OntologyUrl></OntologyUrl>
  <OntologyContent>{sx.escape(rdfxml)}</OntologyContent>
  <Pitfalls></Pitfalls>
  <OutputFormat>XML</OutputFormat>
</OOPSRequest>"""

req = urllib.request.Request(
    "https://oops.linkeddata.es/rest",
    data=body.encode("utf-8"),
    headers={"Content-Type": "application/xml"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=300) as r:
    out = r.read().decode("utf-8", errors="replace")
    print(f"HTTP {r.status}")

with open(sys.argv[1], "w") as f:
    f.write(out)
print(f"saved {len(out)} chars to {sys.argv[1]}")
