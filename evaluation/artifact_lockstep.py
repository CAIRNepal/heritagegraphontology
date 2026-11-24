#!/usr/bin/env python3
"""Artifact-lockstep audit: measure the schema-first single-source claim.

Addresses the reviewer observation that the LinkML schema-first workflow is
demonstrated but its claimed benefit is not evidenced. The claim that *can*
be measured without a user study is the one the paper actually makes about
the artefacts: that OWL, SHACL, and JSON Schema are generated from a single
YAML source and therefore stay in lockstep (no term drift between the
logical model and its validation and programming interfaces).

This script checks that property term by term, treating the YAML schema
(via linkml-runtime SchemaView) as the reference:

  A  Classes -> OWL      every YAML class URI is declared owl:Class.
  B  Slots   -> OWL      every YAML slot URI is declared or used in OWL.
  C  Enums   -> OWL      every YAML enum is an owl:oneOf class whose member
                         count equals the YAML permissible-value count.
  D  Classes -> SHACL    every YAML class URI is the sh:targetClass of a
                         node shape, and no shape targets a URI outside the
                         YAML class set (no orphan shapes).
  E  Classes -> JSON     every *concrete* class and every enum has a $defs
                         entry; abstract classes (mixins, unions) are exempt
                         because instance payloads cannot instantiate them,
                         and no $defs entry lacks a YAML counterpart.
  P  Prefixes            the JSON/YAML wrapper schema binds every core prefix.
  L  Language-tagged text in all three artefacts: a slot whose OWL range is
                         rdf:PlainLiteral (text that may carry a language tag)
                         accepts a JSON-LD language map in every JSON field
                         and xsd:string or rdf:langString in every SHACL
                         shape; a code slot (xsd:string in OWL) accepts
                         neither. Sample instances check the JSON side.

Exit status is non-zero if any drift is found, so the audit can gate the
release pipeline.

Run:  python3 evaluation/artifact_lockstep.py
      (an interpreter with linkml-runtime and rdflib; the release-pipeline
      interpreter satisfies this)
"""
import json
import sys
from pathlib import Path

import rdflib
from rdflib import OWL, RDF, URIRef
from rdflib.collection import Collection
from linkml_runtime import SchemaView

ROOT = Path(__file__).resolve().parents[1]
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")

sv = SchemaView(str(ROOT / "ontology/HeritageGraph.yaml"))
classes = sv.all_classes()
slots = sv.all_slots()
enums = sv.all_enums()

owl_g = rdflib.Graph()
owl_g.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
shacl_g = rdflib.Graph()
shacl_g.parse(ROOT / "ontology/HeritageGraph.shacl.ttl", format="turtle")
# The JSON Schema is generated from the serialization wrapper (core schema +
# the LinkML tree_root Container and its Metadata header, since 1.1.0), so its
# $defs are compared against the wrapper's classes.
cv = SchemaView(str(ROOT / "ontology/HeritageGraph-container.yaml"))
wrapper_only = {n: c for n, c in cv.all_classes().items() if n not in classes}
json_schema = json.loads((ROOT / "ontology/HeritageGraph.schema.json").read_text())
defs = json_schema.get("$defs", json_schema.get("definitions", {}))

failures = []


def report(check: str, ok_count: int, total: int, drift: list) -> None:
    status = "OK " if not drift else "DRIFT"
    print(f"[{status}] {check}: {ok_count}/{total}"
          + (f"  drift: {drift[:10]}" if drift else ""))
    if drift:
        failures.append(check)


# A. YAML classes -> OWL classes.
owl_classes = {s for s in owl_g.subjects(RDF.type, OWL.Class)
               if isinstance(s, URIRef)}
drift = [c.name for c in classes.values()
         if URIRef(sv.get_uri(c, expand=True)) not in owl_classes]
report("A classes in OWL", len(classes) - len(drift), len(classes), drift)

# A'. No active (non-deprecated) HeritageGraph class in OWL without a YAML class
#     or enum (enumerations are owl:oneOf classes).
HG_NS = sv.schema.prefixes[sv.schema.default_prefix].prefix_reference
deprecated = {s for s, o in owl_g.subject_objects(OWL.deprecated)
              if str(o).lower() == "true"}
yaml_class_uris = ({URIRef(sv.get_uri(c, expand=True)) for c in classes.values()}
                   | {URIRef(sv.get_uri(e, expand=True)) for e in enums.values()})
active_hg = {c for c in owl_classes if str(c).startswith(HG_NS) and c not in deprecated}
drift = sorted(str(c) for c in active_hg - yaml_class_uris)
report("A' active HG OWL classes in YAML", len(active_hg) - len(drift), len(active_hg), drift)

# W. Wrapper-only terms (Container, Metadata and their attributes) appear in
# OWL only as owl:deprecated stubs: they are JSON/YAML serialization devices.
wterms, absent = [], []
for c in wrapper_only.values():
    wterms.append(URIRef(cv.get_uri(c, expand=True)))
    wterms += [URIRef(HG_NS + n) for n, a in (c.attributes or {}).items()
               if not (a.annotations and "since" in a.annotations)]
    # collections added after 1.0.x were never OWL terms: they must stay out of the OWL
    absent += [URIRef(HG_NS + n) for n, a in (c.attributes or {}).items()
              if a.annotations and "since" in a.annotations]
drift = [str(u) for u in wterms if u not in deprecated]
drift += [f"{u} (new collection in OWL)" for u in absent if (u, None, None) in owl_g]
report("W wrapper-only terms deprecated in OWL", len(wterms) - len(drift), len(wterms), drift)

# B. YAML slots -> OWL properties (declared, or used in an axiom).
owl_props = set()
for t in (OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty):
    owl_props |= {s for s in owl_g.subjects(RDF.type, t)
                  if isinstance(s, URIRef)}
drift = []
for s in slots.values():
    u = URIRef(sv.get_uri(s, expand=True))
    if (u not in owl_props
            and not any(owl_g.triples((u, None, None)))
            and not any(owl_g.triples((None, u, None)))):
        drift.append(s.name)
report("B slots in OWL", len(slots) - len(drift), len(slots), drift)

# C. YAML enums -> OWL owl:oneOf classes with matching member counts.
drift = []
for e in enums.values():
    u = URIRef(sv.get_uri(e, expand=True))
    one_of = next(owl_g.objects(u, OWL.oneOf), None)
    n = len(list(Collection(owl_g, one_of))) if one_of is not None else 0
    if n != len(e.permissible_values):
        drift.append(f"{e.name}({n}!={len(e.permissible_values)})")
report("C enums in OWL (member counts)", len(enums) - len(drift),
       len(enums), drift)

# D. YAML classes <-> SHACL target classes (both directions).
targets = {t for t in shacl_g.objects(None, SH.targetClass)
           if isinstance(t, URIRef)}
class_uris = {URIRef(sv.get_uri(c, expand=True)) for c in classes.values()}
# abstract/mixin classes whose IRI is an external term (prov:Entity, crm:E74,
# ...) have no shape of their own since 1.1.0: their property shapes are
# repeated in every concrete subclass, and a shape would constrain all
# third-party instances of the external class
def _shape_exempt(c) -> bool:
    return bool(c.abstract or c.mixin) and not sv.get_uri(c, expand=True).startswith(
        sv.schema.prefixes[sv.schema.default_prefix].prefix_reference)
missing_shape = [c.name for c in classes.values()
                 if URIRef(sv.get_uri(c, expand=True)) not in targets and not _shape_exempt(c)]
orphan_shapes = sorted(str(t) for t in targets - class_uris)
n_shape = sum(1 for c in classes.values() if not _shape_exempt(c))
report("D classes with SHACL shape", n_shape - len(missing_shape),
       n_shape, missing_shape)
report("D' orphan SHACL targets", len(targets) - len(orphan_shapes),
       len(targets), orphan_shapes)

# E. Concrete YAML classes + enums <-> JSON Schema $defs (both directions).
json_classes = cv.all_classes()
concrete = [c for c in json_classes.values() if not c.abstract]
abstract = [c.name for c in json_classes.values() if c.abstract]
expected = {c.name for c in concrete} | set(cv.all_enums())
missing_defs = sorted(expected - set(defs))
orphan_defs = sorted(set(defs) - expected)
report("E concrete classes+enums in JSON Schema",
       len(expected) - len(missing_defs), len(expected), missing_defs)
report("E' orphan JSON Schema defs", len(defs) - len(orphan_defs),
       len(defs), orphan_defs)
# E''. Every "$ref" in the JSON Schema resolves to a $defs entry.
import re as _re
_txt = json.dumps(json_schema)
_refs = sorted(set(_re.findall(r'"#/\$defs/([^"]+)"', _txt)))
drift = [r for r in _refs if r not in defs]
report("E'' JSON Schema $refs resolve", len(_refs) - len(drift), len(_refs), drift)
print(f"       (abstract classes exempt from JSON Schema by design: "
      f"{len(abstract)}: {', '.join(sorted(abstract))})")

# P. The serialization wrapper binds every prefix the core schema binds, to
# the same IRI: LinkML takes prefixes from the root schema only, so a missing
# binding makes linkml-convert write <crm:P3_has_note> as a literal IRI.
core_px = {k: v.prefix_reference for k, v in sv.schema.prefixes.items()}
wrap_px = {k: v.prefix_reference for k, v in cv.schema.prefixes.items()}
drift = sorted(k for k, v in core_px.items() if wrap_px.get(k) != v)
report("P container schema binds the core prefixes", len(core_px) - len(drift), len(core_px), drift)

# L. Language-tagged text: OWL, SHACL and JSON Schema agree slot by slot.
RDFNS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
XSD_STRING = URIRef("http://www.w3.org/2001/XMLSchema#string")
PLAIN = URIRef(RDFNS + "PlainLiteral")
LANGSTRING = URIRef(RDFNS + "langString")


def owl_text_kind(u):
    vals = set(owl_g.objects(u, rdflib.RDFS.range))
    vals |= {owl_g.value(r, OWL.allValuesFrom) for r in owl_g.subjects(OWL.onProperty, u)}
    if PLAIN in vals:
        return "text"
    if XSD_STRING in vals:
        return "code"
    return None


def json_has_langmap(pdef):
    alts = pdef.get("anyOf", [])
    return any(a.get("type") == "object" and "propertyNames" in a for a in alts)


def shacl_accepts_langstring(u):
    shapes = [ps for ps in shacl_g.subjects(SH.path, u)]
    ok = []
    for ps in shapes:
        dts = set(shacl_g.objects(ps, SH.datatype))
        for lst in shacl_g.objects(ps, SH["or"]):
            for m in Collection(shacl_g, lst):
                dts |= set(shacl_g.objects(m, SH.datatype))
        if dts:   # shapes with no datatype constraint (e.g. maxCount 0) are neutral
            ok.append(LANGSTRING in dts)
    return shapes, ok


drift, n = [], 0
for s in slots.values():
    if not s.slot_uri:
        continue
    u = URIRef(sv.get_uri(s, expand=True))
    kind = owl_text_kind(u)
    if kind is None:
        continue
    n += 1
    for cname, cdef in defs.items():
        pdef = cdef.get("properties", {}).get(s.name)
        if pdef is not None and json_has_langmap(pdef) != (kind == "text"):
            drift.append(f"{s.name} JSON {cname} ({kind})")
    shapes, ok = shacl_accepts_langstring(u)
    if any(o != (kind == "text") for o in ok):
        drift.append(f"{s.name} SHACL ({kind})")
bad_slots = {d.split()[0] for d in drift}
report("L text vs code slots agree across OWL, SHACL, JSON", n - len(bad_slots), n, drift)

# L'' the other direction: every JSON field that accepts a language map is a
# text slot (explicit range string, no any_of, not lexical_form code or
# any_literal) whose RDF property is a datatype property or rdfs:label, and
# whose SHACL shapes (if any) accept rdf:langString.
RDFS_LABEL = URIRef("http://www.w3.org/2000/01/rdf-schema#label")
drift, opened = [], set()
for cname, cdef in defs.items():
    if cname not in cv.all_classes():
        continue
    for pname, pdef in cdef.get("properties", {}).items():
        if not json_has_langmap(pdef):
            continue
        opened.add(pname)
        sl = cv.induced_slot(pname, cname)
        anns = sl.annotations or {}
        anns = anns if isinstance(anns, dict) else getattr(anns, "_as_dict", {})
        form = getattr(anns.get("lexical_form"), "value", anns.get("lexical_form"))
        form = form.get("value") if isinstance(form, dict) else form
        u = URIRef(cv.get_uri(sl, expand=True)) if sl.slot_uri else None
        why = []
        if sl.range != "string" or sl.any_of or sl.exactly_one_of:
            why.append("not a string slot")
        if form in ("code", "any_literal"):
            why.append(f"lexical_form {form}")
        if u is not None and u != RDFS_LABEL and (u, RDF.type, OWL.ObjectProperty) in owl_g:
            why.append("OWL object property")
        if u is not None and False in shacl_accepts_langstring(u)[1]:
            why.append("SHACL refuses rdf:langString")
        if why:
            drift.append(f"{cname}.{pname}: {', '.join(why)}")
report("L'' every JSON language-map field is a text slot", len(opened) - len({d.split(':')[0].split('.')[1] for d in drift}),
       len(opened), drift)

try:
    import jsonschema
except ImportError:
    jsonschema = None
if jsonschema is not None:
    def valid(cls, inst):
        sch = {"$schema": json_schema["$schema"], "$defs": defs, "$ref": f"#/$defs/{cls}"}
        return not list(jsonschema.Draft201909Validator(sch).iter_errors(inst))
    samples = [
        ("Deity, plain-string name", "Deity", {"id": "ex:d", "name": "Taleju"}, True),
        ("Deity, name as language map", "Deity",
         {"id": "ex:d", "name": {"en": "Taleju Bhawani", "ne": "तलेजु भवानी"}}, True),
        ("Deity, name map with a bad language tag", "Deity",
         {"id": "ex:d", "name": {"english!": "Taleju"}}, False),
        ("Deity, several notes, per language", "Deity",
         {"id": "ex:d", "note": {"en": ["first", "second"], "ne": "टिप्पणी"}}, True),
        ("Deity, one note as a plain string (1.0.x form)", "Deity", {"id": "ex:d", "note": "x"}, True),
        ("DataSource, source_url as a language map (code slot)", "DataSource",
         {"id": "ex:s", "source_url": {"en": "https://example.org"}}, False),
    ]
    bad = [f"{name} (expected {'valid' if exp else 'invalid'})"
           for name, cls, inst, exp in samples if valid(cls, inst) != exp]
    report("L' JSON instances: language maps accepted on text, refused on codes",
           len(samples) - len(bad), len(samples), bad)

print()
if failures:
    print(f"LOCKSTEP AUDIT FAILED: drift in {failures}")
    sys.exit(1)
print(f"LOCKSTEP AUDIT PASSED: {len(classes)} classes, {len(slots)} slots, "
      f"{len(enums)} enums from one YAML source are consistently realised "
      f"across OWL, SHACL, and JSON Schema.")
