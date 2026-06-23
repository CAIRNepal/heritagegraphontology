#!/usr/bin/env python3
"""Declutter a WebVOWL ontology.json produced by WIDOCO/owl2vowl.

The HeritageGraph properties are aligned upward to CIDOC-CRM (crm:P...) and
PROV-O (prov:was...) via rdfs:subPropertyOf. Because owl:imports are stripped
before documentation, those external super-properties have no domain/range, so
WebVOWL renders each as a standalone node pinned to a generic owl:Thing — the
detached "star" cluster.

This script removes those external alignment super-properties (and any generic
owl:Thing nodes left unreferenced as a result) from the *visualization only*.
The ontology, the RDF serializations, and the HTML cross-reference are untouched;
the alignment is still visible on each local property (skos:broadMatch / parent
links remain in the property's tooltip annotations).

Usage: declutter_webvowl.py path/to/webvowl/data/ontology.json
"""
import json
import sys

# Namespaces of the external alignment parents we don't want drawn as nodes.
EXTERNAL_PREFIXES = (
    "http://www.cidoc-crm.org/",   # CIDOC-CRM (crm:P..., crminf:, crmsci:)
    "http://www.w3.org/ns/prov",   # PROV-O (prov:was..., generated, used, ...)
    "http://purl.org/pav",         # PAV
)


def is_external(iri: str) -> bool:
    return any(iri.startswith(p) for p in EXTERNAL_PREFIXES)


def is_generic_thing(ca: dict) -> bool:
    iri = str(ca.get("iri", ""))
    label = ca.get("label")
    if isinstance(label, dict):
        label = label.get("IRI-based") or label.get("undefined")
    return iri.endswith("owl#Thing") or label == "Thing"


def main(path: str) -> None:
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)

    prop_attr = d.get("propertyAttribute", [])
    # 1. drop external alignment super-properties
    drop_ids = {p["id"] for p in prop_attr if is_external(str(p.get("iri", "")))}
    if not drop_ids:
        print("declutter: nothing to remove")
        return

    kept_attr = [p for p in prop_attr if p["id"] not in drop_ids]
    # scrub dangling subproperty references to removed nodes
    for p in kept_attr:
        if isinstance(p.get("subproperty"), list):
            p["subproperty"] = [s for s in p["subproperty"] if s not in drop_ids]
            if not p["subproperty"]:
                p.pop("subproperty")
    d["propertyAttribute"] = kept_attr
    d["property"] = [p for p in d.get("property", []) if p["id"] not in drop_ids]

    # 2. figure out which class nodes are still referenced
    referenced = set()
    for p in kept_attr:
        for key in ("domain", "range"):
            v = p.get(key)
            if v is not None:
                referenced.add(v)
    rel_keys = (
        "superClasses", "subClasses", "equivalent", "complement",
        "intersection", "union", "disjointUnion", "instances", "individuals",
    )
    for ca in d.get("classAttribute", []):
        for key in rel_keys:
            v = ca.get(key)
            if isinstance(v, list):
                referenced.update(x for x in v if isinstance(x, (str, int)))
            elif v is not None:
                referenced.add(v)

    # 3. remove generic owl:Thing nodes that are now unreferenced
    thing_drop = {
        ca["id"] for ca in d.get("classAttribute", [])
        if is_generic_thing(ca) and ca["id"] not in referenced
    }
    if thing_drop:
        d["classAttribute"] = [c for c in d["classAttribute"] if c["id"] not in thing_drop]
        d["class"] = [c for c in d.get("class", []) if c["id"] not in thing_drop]

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=4)

    print(
        f"declutter: removed {len(drop_ids)} external alignment properties "
        f"and {len(thing_drop)} orphan owl:Thing nodes → {path}"
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: declutter_webvowl.py path/to/ontology.json")
    main(sys.argv[1])
