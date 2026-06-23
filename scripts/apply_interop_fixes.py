#!/usr/bin/env python3
"""Apply idempotent interoperability fixes to the released HeritageGraph.ttl in place.

This operates directly on the hand-finished release artefact
(``ontology/HeritageGraph.ttl``) so that disjointness axioms and other content not
reproduced by ``gen-owl`` are preserved. The same transforms are wired into
``regenerate_ontology_artifacts.py`` for the (source) regeneration path.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from rdflib import Graph, RDF, OWL, URIRef
from rdflib.namespace import SKOS

from interop_fixes import fix_object_property_types, fix_skos_mappings, HG

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "ontology" / "HeritageGraph.yaml"
TTL = ROOT / "ontology" / "HeritageGraph.ttl"


def _counts(g: Graph) -> dict:
    return {
        "triples": len(g),
        "exactMatch": sum(1 for _ in g.triples((None, SKOS.exactMatch, None))),
        "closeMatch": sum(1 for _ in g.triples((None, SKOS.closeMatch, None))),
        "objectProps": sum(1 for s in g.subjects(RDF.type, OWL.ObjectProperty)
                           if isinstance(s, URIRef) and str(s).startswith(HG)),
        "datatypeProps": sum(1 for s in g.subjects(RDF.type, OWL.DatatypeProperty)
                             if isinstance(s, URIRef) and str(s).startswith(HG)),
        "disjointWith": sum(1 for _ in g.triples((None, OWL.disjointWith, None))),
    }


def main() -> int:
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    g = Graph()
    g.parse(TTL, format="turtle")
    before = _counts(g)

    retyped = fix_object_property_types(g, schema)
    dropped, demoted = fix_skos_mappings(g)

    g.serialize(destination=TTL, format="turtle")
    after = _counts(g)

    print(f"Re-typed datatype->object properties : {retyped}")
    print(f"Dropped exactMatch (also subClassOf) : {dropped}")
    print(f"Demoted exactMatch -> closeMatch     : {demoted}")
    print("            before   after")
    for k in before:
        print(f"  {k:14} {before[k]:6}  {after[k]:6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
