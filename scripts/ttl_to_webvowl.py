#!/usr/bin/env python3
"""Convert HeritageGraph TTL (core + LUX bridge) into WebVOWL JSON.

A dependency-light, offline replacement for owl2vowl (which needs a JVM). It
renders the *named* class hierarchy, object/datatype properties, equivalences
and external CRM/Linked-Art classes — enough to inspect the whole ontology in
WebVOWL. Anonymous restriction superclasses (owl:Restriction blank nodes) are
intentionally skipped to keep the graph readable.

Usage:
    python scripts/ttl_to_webvowl.py ontology/HeritageGraph.ttl ontology/lux/heritagegraph-lux-alignment.ttl \
           -o docs/webvowl/data/ontology.json
"""
from __future__ import annotations

import argparse
import json
from datetime import date

from rdflib import Graph, RDF, RDFS, OWL, URIRef, BNode
from rdflib.namespace import SKOS

HG = "https://cair-nepal.org/heritagegraph/"
THING = OWL.Thing
LITERAL = RDFS.Literal
_REST_FILLERS = (OWL.someValuesFrom, OWL.allValuesFrom, OWL.onClass)


def local_name(iri: str) -> str:
    for sep in ("#", "/"):
        if sep in iri:
            cand = iri.rsplit(sep, 1)[-1]
            if cand:
                return cand
    return iri


def base_iri(iri: str) -> str:
    for sep in ("#", "/"):
        if sep in iri:
            return iri.rsplit(sep, 1)[0]
    return iri


def label_block(g: Graph, s: URIRef) -> dict:
    for lab in g.objects(s, RDFS.label):
        return {"IRI-based": local_name(str(s)), "en": str(lab)}
    return {"IRI-based": local_name(str(s)), "undefined": local_name(str(s))}


def annotations(g: Graph, s: URIRef) -> dict:
    ann: dict = {}
    for defn in g.objects(s, SKOS.definition):
        ann.setdefault("definition", []).append(
            {"identifier": "definition", "language": "en", "value": str(defn), "type": "label"}
        )
    for com in g.objects(s, RDFS.comment):
        ann.setdefault("comment", []).append(
            {"identifier": "comment", "language": "en", "value": str(com), "type": "label"}
        )
    return ann


def convert(sources: list[str]) -> dict:
    g = Graph()
    for src in sources:
        g.parse(src, format="turtle")

    # ---- collect classes (named owl:Class + any URIRef used as class) --------
    classes: set[URIRef] = set()
    for c in g.subjects(RDF.type, OWL.Class):
        if isinstance(c, URIRef):
            classes.add(c)
    # external classes referenced as super/equivalent/domain/range
    for pred in (RDFS.subClassOf, OWL.equivalentClass):
        for _, _, o in g.triples((None, pred, None)):
            if isinstance(o, URIRef):
                classes.add(o)

    classes.add(THING)  # WebVOWL anchors domain-/range-less properties on owl:Thing

    obj_props = {p for p in g.subjects(RDF.type, OWL.ObjectProperty) if isinstance(p, URIRef)}
    dat_props = {p for p in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(p, URIRef)}

    # range datatypes referenced by datatype properties become Datatype nodes
    datatypes: set[URIRef] = {LITERAL}
    for p in dat_props:
        for r in g.objects(p, RDFS.range):
            if isinstance(r, URIRef) and r not in classes:
                datatypes.add(r)

    # Domain/range inferred from owl:Restriction usage (LinkML emits restrictions
    # on classes rather than global rdfs:domain). prop -> set(restricting classes).
    restr_domain: dict[URIRef, set] = {}
    restr_range: dict[URIRef, set] = {}
    for c in classes:
        for restr in g.objects(c, RDFS.subClassOf):
            if isinstance(restr, BNode) and (restr, RDF.type, OWL.Restriction) in g:
                p = g.value(restr, OWL.onProperty)
                if not isinstance(p, URIRef):
                    continue
                restr_domain.setdefault(p, set()).add(c)
                for fill_pred in _REST_FILLERS:
                    f = g.value(restr, fill_pred)
                    if isinstance(f, URIRef):
                        restr_range.setdefault(p, set()).add(f)

    # ---- assign ids ----------------------------------------------------------
    node_id: dict[URIRef, str] = {}
    nid = 0
    for c in sorted(classes) + sorted(datatypes):
        node_id[c] = str(nid)
        nid += 1
    prop_id: dict[URIRef, str] = {}
    pid = 0
    for p in sorted(obj_props) + sorted(dat_props):
        prop_id[p] = str(pid)
        pid += 1

    def is_external(iri: URIRef) -> bool:
        return not str(iri).startswith(HG)

    # ---- build class + classAttribute arrays --------------------------------
    cls_arr, clsattr_arr = [], []
    for c in sorted(classes):
        ctype = "owl:Thing" if c == THING else "owl:Class"
        cls_arr.append({"id": node_id[c], "type": ctype})
        supers = [node_id[o] for o in g.objects(c, RDFS.subClassOf)
                  if isinstance(o, URIRef) and o in node_id]
        equiv = [node_id[o] for o in g.objects(c, OWL.equivalentClass)
                 if isinstance(o, URIRef) and o in node_id]
        attrs = []
        if is_external(c):
            attrs.append("external")
        attr = {
            "iri": str(c),
            "baseIri": base_iri(str(c)),
            "instances": 0,
            "label": label_block(g, c),
            "id": node_id[c],
        }
        if supers:
            attr["superClasses"] = supers
        if equiv:
            attr["equivalent"] = equiv
        if attrs:
            attr["attributes"] = attrs
        ann = annotations(g, c)
        if ann:
            attr["annotations"] = ann
        clsattr_arr.append(attr)

    for d in sorted(datatypes):
        cls_arr.append({"id": node_id[d], "type": "rdfs:Datatype"})
        clsattr_arr.append({
            "iri": str(d), "baseIri": base_iri(str(d)), "instances": 0,
            "label": label_block(g, d), "id": node_id[d], "attributes": ["datatype", "external"],
        })

    # ---- build property + propertyAttribute arrays ---------------------------
    prop_arr, propattr_arr = [], []

    def pick(uris: set) -> URIRef | None:
        """A single representative domain/range; None when ambiguous (-> Thing)."""
        cands = sorted(u for u in uris if u in node_id)
        return cands[0] if len(cands) == 1 else None

    def prop_entry(p: URIRef, ptype: str, kind: str):
        prop_arr.append({"id": prop_id[p], "type": ptype})
        attr = {
            "iri": str(p), "baseIri": base_iri(str(p)),
            "label": label_block(g, p), "id": prop_id[p],
        }
        dom = next((o for o in g.objects(p, RDFS.domain) if isinstance(o, URIRef) and o in node_id), None)
        rng = next((o for o in g.objects(p, RDFS.range) if isinstance(o, URIRef) and o in node_id), None)
        if dom is None:
            dom = pick(restr_domain.get(p, set())) or THING
        if rng is None:
            rng = pick(restr_range.get(p, set())) or (LITERAL if kind == "datatype" else THING)
        attr["domain"] = node_id[dom]
        attr["range"] = node_id[rng]
        sub = [prop_id[o] for o in g.objects(p, RDFS.subPropertyOf) if o in prop_id]
        if sub:
            attr["subproperty"] = sub
        attrs = [kind]
        if is_external(p):
            attrs.append("external")
        attr["attributes"] = attrs
        ann = annotations(g, p)
        if ann:
            attr["annotations"] = ann
        propattr_arr.append(attr)

    for p in sorted(obj_props):
        prop_entry(p, "owl:objectProperty", "object")
    for p in sorted(dat_props):
        prop_entry(p, "owl:datatypeProperty", "datatype")

    header = {
        "languages": ["en", "undefined"],
        "baseIris": [HG],
        "iri": HG,
        "title": {"IRI-based": "HeritageGraph", "en": "HeritageGraph (core + LUX/CIDOC-CRM bridge)"},
        "labels": {"IRI-based": "HeritageGraph", "en": "HeritageGraph"},
        "description": {"en": "CAIR Nepal HeritageGraph ontology merged with the LUX "
                              "(Yale Linked Art / CIDOC-CRM) interoperability bridge."},
        "other": {"created": [{"identifier": "created", "language": "en",
                               "value": date.today().isoformat(), "type": "label"}]},
    }

    return {
        "_comment": "Generated by scripts/ttl_to_webvowl.py from "
                    + ", ".join(sources) + f" on {date.today().isoformat()}",
        "header": header,
        "namespace": [],
        "metrics": {
            "classCount": len(cls_arr),
            "objectPropertyCount": len(obj_props),
            "datatypePropertyCount": len(dat_props),
        },
        "class": cls_arr,
        "classAttribute": clsattr_arr,
        "property": prop_arr,
        "propertyAttribute": propattr_arr,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sources", nargs="+", help="TTL files to merge (core first)")
    ap.add_argument("-o", "--output", action="append", required=True,
                    help="output JSON path (repeatable)")
    args = ap.parse_args()
    data = convert(args.sources)
    for out in args.output:
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
        print(f"wrote {out}  "
              f"(classes={len(data['class'])}, properties={len(data['property'])})")


if __name__ == "__main__":
    main()
