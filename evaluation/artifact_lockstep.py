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
missing_shape = [c.name for c in classes.values()
                 if URIRef(sv.get_uri(c, expand=True)) not in targets]
orphan_shapes = sorted(str(t) for t in targets - class_uris)
report("D classes with SHACL shape", len(classes) - len(missing_shape),
       len(classes), missing_shape)
report("D' orphan SHACL targets", len(targets) - len(orphan_shapes),
       len(targets), orphan_shapes)

# E. Concrete YAML classes + enums <-> JSON Schema $defs (both directions).
concrete = [c for c in classes.values() if not c.abstract]
abstract = [c.name for c in classes.values() if c.abstract]
expected = {c.name for c in concrete} | set(enums)
missing_defs = sorted(expected - set(defs))
orphan_defs = sorted(set(defs) - expected)
report("E concrete classes+enums in JSON Schema",
       len(expected) - len(missing_defs), len(expected), missing_defs)
report("E' orphan JSON Schema defs", len(defs) - len(orphan_defs),
       len(defs), orphan_defs)
print(f"       (abstract classes exempt from JSON Schema by design: "
      f"{len(abstract)}: {', '.join(sorted(abstract))})")

print()
if failures:
    print(f"LOCKSTEP AUDIT FAILED: drift in {failures}")
    sys.exit(1)
print(f"LOCKSTEP AUDIT PASSED: {len(classes)} classes, {len(slots)} slots, "
      f"{len(enums)} enums from one YAML source are consistently realised "
      f"across OWL, SHACL, and JSON Schema.")
