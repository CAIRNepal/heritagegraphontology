#!/usr/bin/env python3
"""TGDK-style ontology evaluation battery for HeritageGraph 0.1.0-alpha.5.

Executes the standard ontology-evaluation practices expected by venues such
as TGDK / SWJ for ontology (resource) papers, and writes a consolidated
report to evaluation/results/tgdk_eval_report.txt:

  1. Structural & schema metrics (OntoQA/OQuaRE-style)
  2. OOPS!-style pitfall scan (local implementation of the checkable pitfalls)
  3. Competency-question coverage (32 CQs, Grüninger & Fox paradigm)
  4. SHACL conformance of the demonstrator ABox
  5. Logical consistency (OWL 2 RL closure; DL reasoner noted separately)
  6. FAIR / FOOPS!-style metadata checklist
"""
from __future__ import annotations

import io
import re
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import rdflib
from rdflib import OWL, RDF, RDFS
from rdflib.namespace import DCTERMS, SKOS
from linkml_runtime import SchemaView

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "ontology" / "HeritageGraph.yaml"
OWL_TTL = ROOT / "ontology" / "HeritageGraph.ttl"
SHACL_TTL = ROOT / "ontology" / "HeritageGraph.shacl.ttl"
ABOX = ROOT / "examples" / "kathmandu-mini-abox-alpha5.ttl"
OUT = ROOT / "evaluation" / "results" / "tgdk_eval_report.txt"

HG = "https://w3id.org/heritagegraph/"
buf = io.StringIO()
def w(line=""):
    print(line)
    buf.write(line + "\n")


def section_metrics(sv: SchemaView, g: rdflib.Graph) -> None:
    w("=" * 72)
    w("1. STRUCTURAL & SCHEMA METRICS (OntoQA / OQuaRE style)")
    w("=" * 72)
    classes = {c: sv.get_class(c) for c in sv.all_classes()}
    slots = sv.all_slots()
    concrete = [c for c, o in classes.items() if not o.mixin and not o.abstract]
    w(f"Classes: {len(classes)} total ({len(concrete)} concrete, "
      f"{sum(1 for o in classes.values() if o.abstract)} abstract, "
      f"{sum(1 for o in classes.values() if o.mixin)} mixins)")
    w(f"Slots: {len(slots)}   Enums: {len(sv.all_enums())}   "
      f"Enum values: {sum(len(e.permissible_values or {}) for e in sv.all_enums().values())}")
    obj_props = len(list(g.subjects(RDF.type, OWL.ObjectProperty)))
    dt_props = len(list(g.subjects(RDF.type, OWL.DatatypeProperty)))
    w(f"OWL export: {len(g)} triples, {obj_props} object properties, {dt_props} datatype properties")

    # inheritance metrics over is_a
    depths = {}
    def depth(c):
        if c in depths: return depths[c]
        p = classes[c].is_a
        depths[c] = 1 + depth(p) if p in classes else (1 if p else 0)
        return depths[c]
    for c in classes: depth(c)
    kids = Counter(o.is_a for o in classes.values() if o.is_a)
    multi = [c for c, o in classes.items() if o.is_a and len(o.mixins or []) > 0]
    H = sum(kids.values())
    w(f"Inheritance: max depth {max(depths.values())}, mean depth "
      f"{sum(depths.values())/len(depths):.2f}; subclass edges H={H}; "
      f"mean branching {H/max(1,len(kids)):.2f}; "
      f"tangledness (is_a + >=1 mixin): {len(multi)} classes")
    # OntoQA richness
    P = sum(1 for s in slots.values() if s.range in classes)  # object-valued relations
    w(f"Relationship richness RR = P/(P+H) = {P}/({P}+{H}) = {P/(P+H):.2f}")
    w(f"Inheritance richness IR = H/C = {H/len(classes):.2f}")
    attrs = sum(1 for s in slots.values() if s.range not in classes)
    w(f"Attribute richness AR = attributes/C = {attrs}/{len(classes)} = {attrs/len(classes):.2f}")
    # annotation & mapping coverage
    with_desc = sum(1 for o in classes.values() if o.description)
    with_alias = sum(1 for o in classes.values() if o.aliases)
    mapped = sum(1 for o in classes.values() if any(
        [o.exact_mappings, o.close_mappings, o.broad_mappings, o.narrow_mappings, o.related_mappings]))
    sdesc = sum(1 for s in slots.values() if s.description)
    w(f"Documentation coverage: classes with definition {with_desc}/{len(classes)} "
      f"({100*with_desc/len(classes):.0f}%), slots with definition {sdesc}/{len(slots)} "
      f"({100*sdesc/len(slots):.0f}%), classes with altLabels {with_alias}")
    w(f"External mapping coverage (classes): {mapped}/{len(classes)} ({100*mapped/len(classes):.0f}%)")
    minted = sum(1 for o in classes.values()
                 if str(o.class_uri or '').startswith('heritageGraph:') or not o.class_uri)
    w(f"Minted vs reused class IRIs: {minted} minted / {len(classes)-minted} external-identity")
    # axiom inventory in export
    w("Axiom inventory (OWL export): "
      f"subClassOf={len(list(g.subject_objects(RDFS.subClassOf)))}, "
      f"subPropertyOf={len(list(g.subject_objects(RDFS.subPropertyOf)))}, "
      f"inverseOf={len(list(g.subject_objects(OWL.inverseOf)))}, "
      f"disjointWith={len(list(g.subject_objects(OWL.disjointWith)))}, "
      f"equivalentClass(union defs)={len(list(g.subject_objects(OWL.equivalentClass)))}, "
      f"deprecated={len(list(g.subject_objects(OWL.deprecated)))}")


def section_pitfalls(sv: SchemaView, g: rdflib.Graph) -> None:
    w("")
    w("=" * 72)
    w("2. OOPS!-STYLE PITFALL SCAN (local implementation; web service was")
    w("   unreachable on scan dates — rerun at oops.linkeddata.es when up)")
    w("=" * 72)
    classes = {c: sv.get_class(c) for c in sv.all_classes()}
    slots = sv.all_slots()
    findings: list[tuple[str, str, str]] = []  # (pitfall, level, detail)

    p08c = [c for c, o in classes.items() if not o.description]
    p08s = [s for s, o in slots.items() if not o.description]
    if p08c or p08s:
        findings.append(("P08 missing annotations", "Minor",
                         f"{len(p08c)} classes / {len(p08s)} slots lack definitions: "
                         f"{(p08c + p08s)[:6]}"))
    ndisj = len(list(g.subject_objects(OWL.disjointWith)))
    findings.append(("P10 missing disjointness", "Important",
                     f"only {ndisj} disjointness axiom(s) (Stupa/Chaitya); sibling sets "
                     "(Temple/Stupa/Chaitya, RestHouse kinds, Person/Guthi) undeclared — "
                     "deliberate minimal-commitment stance; must be argued in the paper"))
    inv_missing = [s for s, o in slots.items()
                   if o.range in classes and not o.inverse
                   and s not in ("was_influenced_by", "used", "has_type")]
    findings.append(("P13 missing inverses", "Minor",
                     f"{len(inv_missing)} object slots without declared inverse "
                     "(PROV/CRM one-directional idiom for most; reviewed)"))
    # P22 naming convention
    bad_names = [s for s in slots if not re.fullmatch(r"[a-z][a-z0-9_]*", s)]
    bad_cls = [c for c in classes if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", c)]
    if bad_names or bad_cls:
        findings.append(("P22 naming inconsistency", "Minor", f"{bad_names + bad_cls}"))
    else:
        findings.append(("P22 naming convention", "PASS", "snake_case slots / UpperCamelCase classes uniform"))
    # P04 orphans: classes not referenced by any slot range / is_a / union / container
    referenced = set()
    for o in classes.values():
        if o.is_a: referenced.add(o.is_a)
        referenced.update(o.mixins or []); referenced.update(o.union_of or [])
    for s in slots.values():
        if s.range in classes: referenced.add(s.range)
    for a in sv.get_class("Container").attributes.values():
        if a.range in classes: referenced.add(a.range)
    # a class is connected if it or any ancestor is referenced (leaf
    # subclasses are reachable through their parent's ranges/collections)
    orphans = [c for c in classes
               if c != "Container" and not classes[c].tree_root
               and not any(a in referenced for a in sv.class_ancestors(c, mixins=True))]
    findings.append(("P04 unconnected elements", "PASS" if not orphans else "Minor",
                     f"orphans: {orphans or 'none'}"))
    lic = list(g.objects(None, DCTERMS.license))
    findings.append(("P41/P38 license", "PASS" if lic else "Critical",
                     f"dcterms:license = {lic[0] if lic else 'MISSING'}"))
    for name, level, detail in findings:
        w(f"  [{level:<9}] {name}: {detail}")


def section_cq() -> None:
    w("")
    w("=" * 72)
    w("3. COMPETENCY-QUESTION COVERAGE (Grüninger & Fox)")
    w("=" * 72)
    r = subprocess.run([sys.executable, str(ROOT / "evaluation" / "run_abox_cq32_alpha5.py")],
                       capture_output=True, text=True)
    tail = [l for l in r.stdout.splitlines() if l.startswith("Total")]
    per_dim = Counter()
    for l in r.stdout.splitlines():
        m = re.match(r"CQ(\d+)\s+\[(\w+)\]", l)
        if m:
            cq = int(m.group(1))
            dim = ("Structural" if cq < 7 else "Ritual/Festival" if cq < 19
                   else "Institutional/Syncretic" if cq < 26 else "Living Goddess")
            per_dim[(dim, m.group(2))] += 1
    for (dim, status), n in sorted(per_dim.items()):
        w(f"  {dim:<24} {status}: {n}")
    w(f"  {tail[0] if tail else 'RUNNER FAILED'}")


def section_shacl_consistency(g: rdflib.Graph) -> None:
    w("")
    w("=" * 72)
    w("4. SHACL CONFORMANCE + 5. LOGICAL CONSISTENCY")
    w("=" * 72)
    from pyshacl import validate
    conforms, _, _ = validate(data_graph=str(ABOX), shacl_graph=str(SHACL_TTL),
                              ont_graph=str(OWL_TTL), inference="none")
    w(f"  SHACL (demonstrator ABox vs finalized shapes): "
      f"{'CONFORMS' if conforms else 'NON-CONFORMANT'}")
    from owlrl import DeductiveClosure, OWLRL_Semantics
    cg = rdflib.Graph()
    cg.parse(OWL_TTL, format="turtle"); cg.parse(ABOX, format="turtle")
    DeductiveClosure(OWLRL_Semantics).expand(cg)
    bad = [s for s in cg.subjects(RDF.type, OWL.Nothing) if not str(s).endswith("Nothing")]
    w(f"  OWL 2 RL consistency (TBox+ABox closure {len(cg)} triples): "
      f"{'CONSISTENT' if not bad else 'INCONSISTENT: ' + str(bad[:3])}")
    w("  NOTE: full OWL 2 DL classification (HermiT/Pellet) pending Java runtime;")
    w("  with a single disjointness axiom the DL check is near-vacuous — state this.")


def section_fair(g: rdflib.Graph) -> None:
    w("")
    w("=" * 72)
    w("6. FAIR / FOOPS!-STYLE METADATA CHECKLIST")
    w("=" * 72)
    ont = next(g.subjects(RDF.type, OWL.Ontology))
    def has(p): return bool(list(g.objects(ont, p)))
    VANN = rdflib.Namespace("http://purl.org/vocab/vann/")
    BIBO = rdflib.Namespace("http://purl.org/ontology/bibo/")
    checks = {
        "Ontology IRI is w3id (persistent)": str(ont).startswith("https://w3id.org/"),
        "owl:versionIRI": has(OWL.versionIRI),
        "dcterms:license (as IRI)": any(isinstance(o, rdflib.URIRef) for o in g.objects(ont, DCTERMS.license)),
        "dcterms:creator/publisher": has(DCTERMS.creator) and has(DCTERMS.publisher),
        "dcterms:created & modified": has(DCTERMS.created) and has(DCTERMS.modified),
        "dcterms:bibliographicCitation": has(DCTERMS.bibliographicCitation),
        "bibo:status": has(BIBO.status),
        "vann:preferredNamespacePrefix/Uri": has(VANN.preferredNamespacePrefix) and has(VANN.preferredNamespaceUri),
        "CITATION.cff in repo": (ROOT / "CITATION.cff").exists(),
        "Multiple serializations published (ttl/owl/nt/jsonld)": all(
            (ROOT / "docs" / f"ontology.{ext}").exists() for ext in ("ttl", "owl", "nt", "jsonld")),
        "Machine-readable changelog/docs in repo": (ROOT / "HeritageGraph_URI_FIX_CHANGELOG.md").exists(),
    }
    passed = sum(checks.values())
    for k, v in checks.items():
        w(f"  [{'PASS' if v else 'FAIL'}] {k}")
    w(f"  Local FAIR checklist: {passed}/{len(checks)}")
    w("  OPEN (network/deployment): w3id term-level dereferencing + content")
    w("  negotiation; LOV registry deposit; FOOPS! web score (run once the")
    w("  updated docs/ artifacts are deployed, else it grades the old content).")


def main() -> int:
    sv = SchemaView(str(SCHEMA))
    g = rdflib.Graph(); g.parse(OWL_TTL, format="turtle")
    w(f"TGDK ontology-evaluation battery — HeritageGraph 0.1.0-alpha.5 — {date.today().isoformat()}")
    w(f"Inputs: {SCHEMA.name}, {OWL_TTL.name}, {SHACL_TTL.name}, {ABOX.name}")
    section_metrics(sv, g)
    section_pitfalls(sv, g)
    section_cq()
    section_shacl_consistency(g)
    section_fair(g)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print(f"\nreport written to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
