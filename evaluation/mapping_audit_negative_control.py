#!/usr/bin/env python3
"""Negative control for the mapping audit: does the protocol catch bad mappings?

The full-pass audit (run_mapping_audit.py) machine-checks target existence
and class/property category compatibility, with a single rater judging
semantic adequacy. A fair question is whether that protocol would have
caught a deliberately wrong mapping at all. This script answers it by
seeding the TBox with faulty mappings from four failure classes and running
the same machine tier over them:

  F1  nonexistent target      hg:Temple broadMatch crm:E999_Nonexistent_Class
  F2  class -> property        hg:Temple broadMatch crm:P4_has_time-span
  F3  property -> class        hg:performsRitual subPropertyOf crm:E5_Event
  F4  wrong but plausible      hg:Temple broadMatch crm:E39_Actor
      (semantically wrong, yet the target exists and is a class)

Expected outcome, stated in advance: the machine tier flags F1 (target not
in vocabulary), F2, and F3 (category mismatch), and does NOT flag F4 —
existence and category checks cannot detect a semantically wrong but
category-compatible target. F4 is precisely the error class that only the
rater tier can catch, which is why the single-rater limitation is a real
threat and is reported as such rather than argued away.

Run:  evaluation/.venv/bin/python evaluation/mapping_audit_negative_control.py
"""
import sys
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, SKOS, URIRef

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_mapping_audit import (CLASS_TYPES, DOCS, PROP_TYPES,  # noqa: E402
                               load_vocab)

ROOT = Path(__file__).resolve().parents[1]
HG = "https://w3id.org/heritagegraph/"
CRM = "http://www.cidoc-crm.org/cidoc-crm/"

SEEDS = [
    ("F1 nonexistent target",
     URIRef(HG + "Temple"), SKOS.broadMatch,
     URIRef(CRM + "E999_Nonexistent_Class"), "NOT-IN-VOCAB"),
    ("F2 class mapped to a property",
     URIRef(HG + "Temple"), SKOS.broadMatch,
     URIRef(CRM + "P4_has_time-span"), "CATEGORY-MISMATCH"),
    ("F3 property mapped to a class",
     URIRef(HG + "performsRitual"), RDFS.subPropertyOf,
     URIRef(CRM + "E5_Event"), "CATEGORY-MISMATCH"),
    ("F4 wrong but category-compatible",
     URIRef(HG + "Temple"), SKOS.broadMatch,
     URIRef(CRM + "E39_Actor"), "UNDETECTED (rater tier only)"),
]

tbox = Graph()
tbox.parse(ROOT / "ontology" / "HeritageGraph.ttl", format="turtle")
hg_classes = set(tbox.subjects(RDF.type, OWL.Class))
hg_props = (set(tbox.subjects(RDF.type, OWL.ObjectProperty))
            | set(tbox.subjects(RDF.type, OWL.DatatypeProperty)))

crm_vocab = load_vocab(CRM)
if crm_vocab is None:
    print("FATAL: cannot load the CIDOC-CRM vocabulary document "
          "(network needed on first run; cached afterwards).")
    sys.exit(2)

print("Machine tier of the audit protocol, applied to seeded faulty mappings")
print(f"{'seed':<36}{'verdict':<22}expected")
ok = True
for label, s, p, o, expected in SEEDS:
    defined = (o, None, None) in crm_vocab
    if not defined:
        verdict = "NOT-IN-VOCAB"
    else:
        types = set(crm_vocab.objects(o, RDF.type))
        kind = ("class" if types & CLASS_TYPES
                else "property" if types & PROP_TYPES else "other")
        subj_kind = ("class" if s in hg_classes
                     else "property" if s in hg_props else "other")
        verdict = ("CATEGORY-MISMATCH" if kind in ("class", "property")
                   and kind != subj_kind else "UNDETECTED (rater tier only)")
    match = verdict == expected
    ok &= match
    print(f"{label:<36}{verdict:<22}{expected}  [{'OK' if match else 'FAIL'}]")

if ok:
    print("\nPASS (as pre-registered): the machine tier catches nonexistent "
          "targets and category mismatches (F1-F3) and, by design, cannot "
          "catch a semantically wrong but category-compatible target (F4). "
          "F4-class errors are exactly what the rater tier exists for; the "
          "single-rater limitation therefore remains a real, reported threat.")
    sys.exit(0)
print("\nFAIL: at least one seed produced an unexpected verdict.")
sys.exit(1)
