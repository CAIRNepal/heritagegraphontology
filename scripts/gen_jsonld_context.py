#!/usr/bin/env python3
"""Generate a Linked-Art-style JSON-LD term context for HeritageGraph.

Maps each class and property local name to its IRI so JSON-LD producers/consumers
can emit compact HeritageGraph documents. Object properties are declared with
``"@type": "@id"`` (their values are IRIs); datatype properties carry their
XSD datatype where one is declared. Written to ``docs/context.jsonld``.
"""

from __future__ import annotations

import json
import sys
from collections import OrderedDict
from pathlib import Path

from rdflib import Graph, RDF, RDFS, OWL, URIRef
from rdflib.namespace import XSD

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
OUT = ROOT / "docs" / "context.jsonld"

HG = "https://w3id.org/heritagegraph/"

PREFIXES = OrderedDict([
    ("heritageGraph", HG),
    ("crm", "http://www.cidoc-crm.org/cidoc-crm/"),
    ("crminf", "http://www.cidoc-crm.org/crminf/"),
    ("crmsci", "http://www.cidoc-crm.org/crmsci/"),
    ("prov", "http://www.w3.org/ns/prov#"),
    ("time", "http://www.w3.org/2006/time#"),
    ("geo", "http://www.opengis.net/ont/geosparql#"),
    ("edm", "http://www.europeana.eu/schemas/edm/"),
    ("foaf", "http://xmlns.com/foaf/0.1/"),
    ("skos", "http://www.w3.org/2004/02/skos/core#"),
    ("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
    ("dcterms", "http://purl.org/dc/terms/"),
    ("xsd", "http://www.w3.org/2001/XMLSchema#"),
])

# XSD datatype -> JSON-LD type token (kept as CURIE).
DATATYPE_TOKEN = {
    str(XSD.string): None,            # plain string: no @type needed
    str(XSD.dateTime): "xsd:dateTime",
    str(XSD.date): "xsd:date",
    str(XSD.gYear): "xsd:gYear",
    str(XSD.boolean): "xsd:boolean",
    str(XSD.integer): "xsd:integer",
    str(XSD.float): "xsd:float",
    str(XSD.double): "xsd:double",
    str(XSD.decimal): "xsd:decimal",
    str(XSD.anyURI): "@id",
}


def local(uri: str) -> str:
    return uri[len(HG):]


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT
    g = Graph()
    g.parse(TTL, format="turtle")

    terms: "OrderedDict[str, object]" = OrderedDict()

    classes = sorted(str(s) for s in g.subjects(RDF.type, OWL.Class)
                     if isinstance(s, URIRef) and str(s).startswith(HG)
                     and "/scheme/" not in str(s))
    for c in classes:
        terms[local(c)] = f"heritageGraph:{local(c)}"

    def add_props(prop_type, is_object):
        props = sorted(str(s) for s in g.subjects(RDF.type, prop_type)
                       if isinstance(s, URIRef) and str(s).startswith(HG))
        for p in props:
            name = local(p)
            if name in terms:
                continue
            entry = {"@id": f"heritageGraph:{name}"}
            if is_object:
                entry["@type"] = "@id"
            else:
                rng = next((str(o) for o in g.objects(URIRef(p), RDFS.range)), None)
                token = DATATYPE_TOKEN.get(rng, None) if rng else None
                if token:
                    entry["@type"] = token
            terms[name] = entry

    add_props(OWL.ObjectProperty, True)
    add_props(OWL.DatatypeProperty, False)

    context = OrderedDict()
    context.update(PREFIXES)
    context["@version"] = 1.1
    context.update(terms)

    out.write_text(json.dumps({"@context": context}, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    n_obj = sum(1 for v in terms.values() if isinstance(v, dict) and v.get("@type") == "@id")
    print(f"Wrote {out}: {len(classes)} classes, {len(terms) - len(classes)} properties "
          f"({n_obj} object-valued)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
