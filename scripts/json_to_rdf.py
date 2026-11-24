#!/usr/bin/env python3
"""Convert a HeritageGraph JSON (or YAML) data file to RDF that conforms to
the published ontology and shapes.

    python3 scripts/json_to_rdf.py data.json out.ttl

The data file is a Container (ontology/HeritageGraph-container.yaml): one
collection per class, validated first against ontology/HeritageGraph.schema.json.
The conversion is LinkML's own (linkml-convert), with three corrections that
make its output match the OWL and SHACL release:

1. Language maps. A text field may be a JSON-LD language map,
   {"en": "Taleju Bhawani", "ne": "तलेजु भवानी"}; LinkML has no
   language-tagged strings, so each map becomes one rdf:langString literal
   per entry ("Taleju Bhawani"@en, "तलेजु भवानी"@ne).
2. Enumerations. LinkML writes an enum value as a plain string
   (hg:guthiType "TempleGuthi"); the ontology's values are individuals, so it
   becomes the individual's IRI: the value's `meaning` where declared, else
   <https://cair-nepal.org/heritagegraph/GuthiType#TempleGuthi>, as in the
   OWL and the SHACL sh:in lists.
3. References to union/abstract classes. LinkML cannot hold a reference
   whose range class has no identifier (asserts_about: AssertionSubject, a
   union of identified classes): it drops the value. Such references are set
   aside before the LinkML step and written back as IRIs.
4. The Container node and its collection links are dropped: they are a
   serialization device (owl:deprecated in the ontology), not data.

The published JSON Schema is the validator (LinkML's own validation is
switched off: it does not know language maps or the references in 3).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from rdflib import Graph, Literal, URIRef
from linkml_runtime import SchemaView

ROOT = Path(__file__).resolve().parents[1]
CONTAINER = ROOT / "ontology" / "HeritageGraph-container.yaml"
JSON_SCHEMA = ROOT / "ontology" / "HeritageGraph.schema.json"
HG_NS = "https://cair-nepal.org/heritagegraph/"
BCP47 = re.compile(r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{1,8})*$")


def _uri(sv: SchemaView, curie: str) -> URIRef:
    return URIRef(sv.expand_curie(curie))


def _is_langmap(v) -> bool:
    return (isinstance(v, dict) and v and "id" not in v
            and all(isinstance(k, str) and BCP47.match(k) for k in v)
            and all(isinstance(x, str) or (isinstance(x, list) and all(isinstance(y, str) for y in x))
                    for x in v.values()))


def convert(data: dict, sv: SchemaView) -> Graph:
    # 0. validate against the published JSON Schema
    import jsonschema
    schema = json.loads(JSON_SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(jsonschema.Draft201909Validator(schema).iter_errors(data), key=str)
    if errors:
        raise ValueError("JSON Schema validation failed:\n  " +
                         "\n  ".join(f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors[:10]))

    slots = sv.all_slots()
    # reference slots whose range class has no identifier slot (see 3.)
    no_id = {c for c in sv.all_classes() if sv.get_identifier_slot(c) is None}
    ref_slots = {n for n, sl in slots.items()
                 if sl.range in no_id and not sl.inlined and not sl.inlined_as_list}
    refs: list[tuple[str, str, str]] = []   # (subject id, slot, object id)
    # 1. replace each language map by a placeholder string LinkML can carry
    tagged: dict[str, list[Literal]] = {}

    def walk(node):
        if isinstance(node, list):
            return [walk(x) for x in node]
        if not isinstance(node, dict):
            return node
        out = {}
        for k, v in node.items():
            if k in ref_slots and "id" in node and isinstance(v, (str, list)):
                refs.extend((node["id"], k, x) for x in ([v] if isinstance(v, str) else v))
                continue
            if _is_langmap(v) and k in slots:
                token = f"urn:hg-langmap:{len(tagged)}"
                tagged[token] = [Literal(t, lang=lang) for lang, vals in v.items()
                                 for t in ([vals] if isinstance(vals, str) else vals)]
                out[k] = [token] if slots[k].multivalued else token
            else:
                out[k] = walk(v)
        return out

    stripped = walk(data)

    # LinkML's conversion
    with tempfile.TemporaryDirectory() as td:
        # LinkML's classes also enforce `required`; the set-aside reference
        # slots are made optional in a temporary copy of the schema (the
        # published JSON Schema has already enforced them)
        core = yaml.safe_load((CONTAINER.parent / "HeritageGraph.yaml").read_text(encoding="utf-8"))
        for n in ref_slots:
            if n in (core.get("slots") or {}):
                core["slots"][n]["required"] = False
        for c in (core.get("classes") or {}).values():
            for n, u in ((c or {}).get("slot_usage") or {}).items():
                if n in ref_slots and isinstance(u, dict):
                    u["required"] = False
            for n, a in ((c or {}).get("attributes") or {}).items():
                if n in ref_slots and isinstance(a, dict):
                    a["required"] = False
        (Path(td) / "HeritageGraph.yaml").write_text(yaml.safe_dump(core, allow_unicode=True), encoding="utf-8")
        container = Path(td) / CONTAINER.name
        container.write_text(CONTAINER.read_text(encoding="utf-8"), encoding="utf-8")
        src, dst = Path(td) / "data.json", Path(td) / "data.ttl"
        src.write_text(json.dumps(stripped, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run(["linkml-convert", "--no-validate", "-s", str(container),
                               "-C", "Container", "-t", "ttl", str(src), "-o", str(dst)],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"linkml-convert failed:\n{proc.stderr[-2000:]}")
        g = Graph()
        g.parse(dst, format="turtle")

    # 1. placeholders -> language-tagged literals
    for s, p, o in list(g):
        if isinstance(o, Literal) and str(o) in tagged:
            g.remove((s, p, o))
            for lit in tagged[str(o)]:
                g.add((s, p, lit))

    # 3. references set aside -> IRIs
    for subj, slot, obj in refs:
        g.add((_uri(sv, subj), _uri(sv, str(slots[slot].slot_uri)), _uri(sv, obj)))

    # 2. enum strings -> the enumeration individuals' IRIs
    enum_of: dict[URIRef, str] = {}
    for name, sl in slots.items():
        rng = sl.range
        if sl.slot_uri and rng in sv.all_enums():
            enum_of[_uri(sv, str(sl.slot_uri))] = rng
    for s, p, o in list(g):
        if p in enum_of and isinstance(o, Literal):
            e = sv.get_enum(enum_of[p])
            pv = (e.permissible_values or {}).get(str(o))
            if pv is None:
                raise ValueError(f"{o!r} is not a value of {e.name}")
            iri = _uri(sv, str(pv.meaning)) if pv.meaning else URIRef(f"{HG_NS}{e.name}#{o}")
            g.remove((s, p, o))
            g.add((s, p, iri))

    # 4. drop the Container node
    if "id" in data:
        g.remove((_uri(sv, data["id"]), None, None))
    for prefix, uri in sv.schema.prefixes.items():
        g.bind("hg" if prefix == "heritageGraph" else prefix, uri.prefix_reference)
    return g


def main() -> int:
    if len(sys.argv) != 3:
        sys.exit(__doc__.split("\n\n")[1])
    path, out = Path(sys.argv[1]), Path(sys.argv[2])
    text = path.read_text(encoding="utf-8")
    data = json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)
    g = convert(data, SchemaView(str(CONTAINER)))
    g.serialize(out, format="turtle")
    print(f"wrote {out}: {len(g)} triples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
