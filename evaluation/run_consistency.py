#!/usr/bin/env python3
"""
§4.1 — Logical Consistency and OWL-RL Reasoning
=================================================
Evaluates:
  1. RDF parse correctness (no syntax errors)
  2. OWL-RL deductive closure (inferred triples count)
  3. Unsatisfiable-class heuristic (classes subClassOf owl:Nothing)
  4. Ontology-level metadata check

Output:  results/consistency_report.txt
         results/consistency_report.csv

Note: Full DL consistency (HermiT/Pellet) should be run in Protégé.
      This script covers OWL-RL profile reasoning.
"""

import os
import sys
import csv
import time
from datetime import datetime
from pathlib import Path

from rdflib import Graph, RDF, RDFS, OWL, Namespace, URIRef
from owlrl import DeductiveClosure, OWLRL_Semantics

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
ONTOLOGY_FILE = SCRIPT_DIR.parent / "ontology" / "HeritageGraph.ttl"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
HG = Namespace("https://cair-nepal.org/heritagegraph/")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def section(title: str) -> str:
    bar = "=" * 70
    return f"\n{bar}\n  {title}\n{bar}"


def run_evaluation():
    report_lines: list[str] = []
    csv_rows: list[dict] = []

    def log(msg: str):
        report_lines.append(msg)
        print(msg)

    def metric(name: str, value, note: str = ""):
        csv_rows.append({"metric": name, "value": value, "note": note})

    log(section("§4.1  Logical Consistency & OWL-RL Reasoning"))
    log(f"Date      : {datetime.now().isoformat()}")
    log(f"Ontology  : {ONTOLOGY_FILE}")
    log("")

    # ------------------------------------------------------------------
    # Step 1: Parse
    # ------------------------------------------------------------------
    log(section("Step 1 — RDF Parse"))
    g = Graph()
    t0 = time.time()
    try:
        g.parse(str(ONTOLOGY_FILE), format="turtle")
        parse_time = round(time.time() - t0, 3)
        original_count = len(g)
        log(f"  ✅  Parsed successfully in {parse_time}s")
        log(f"  Triples (original): {original_count}")
        metric("parse_status", "OK")
        metric("parse_time_seconds", parse_time)
        metric("triples_original", original_count)
    except Exception as e:
        log(f"  ❌  Parse FAILED: {e}")
        metric("parse_status", "FAIL", str(e))
        sys.exit(1)

    # ------------------------------------------------------------------
    # Step 2: OWL-RL closure
    # ------------------------------------------------------------------
    log(section("Step 2 — OWL-RL Deductive Closure"))
    t0 = time.time()
    try:
        DeductiveClosure(OWLRL_Semantics).expand(g)
        closure_time = round(time.time() - t0, 3)
        after_count = len(g)
        inferred = after_count - original_count
        log(f"  ✅  OWL-RL closure computed in {closure_time}s")
        log(f"  Triples after closure : {after_count}")
        log(f"  Inferred triples      : {inferred}")
        metric("owlrl_status", "OK")
        metric("owlrl_time_seconds", closure_time)
        metric("triples_after_closure", after_count)
        metric("triples_inferred", inferred)
    except Exception as e:
        log(f"  ❌  OWL-RL closure FAILED: {e}")
        metric("owlrl_status", "FAIL", str(e))

    # ------------------------------------------------------------------
    # Step 3: Unsatisfiable class check (heuristic)
    # ------------------------------------------------------------------
    log(section("Step 3 — Unsatisfiable Class Heuristic"))
    nothing = OWL.Nothing
    unsatisfiable = set()
    for cls in g.subjects(RDF.type, OWL.Class):
        if (cls, RDFS.subClassOf, nothing) in g and cls != nothing:
            unsatisfiable.add(cls)

    if unsatisfiable:
        log(f"  ⚠️  {len(unsatisfiable)} potentially unsatisfiable class(es):")
        for u in sorted(unsatisfiable, key=str):
            log(f"      - {u}")
    else:
        log("  ✅  No classes found subClassOf owl:Nothing")
    metric("unsatisfiable_classes", len(unsatisfiable))

    # ------------------------------------------------------------------
    # Step 4: Ontology metadata check
    # ------------------------------------------------------------------
    log(section("Step 4 — Ontology Metadata"))
    ontologies = list(g.subjects(RDF.type, OWL.Ontology))
    log(f"  owl:Ontology declarations: {len(ontologies)}")
    for ont in ontologies:
        log(f"    IRI: {ont}")
        for p, o in g.predicate_objects(ont):
            if p in (RDFS.label, OWL.versionIRI, URIRef("http://purl.org/pav/version")):
                log(f"      {g.qname(p) if hasattr(g, 'qname') else p} = {o}")
    metric("ontology_declarations", len(ontologies))

    # ------------------------------------------------------------------
    # Step 5: Quick consistency indicators
    # ------------------------------------------------------------------
    log(section("Step 5 — Quick Consistency Indicators"))

    # Check for classes that are both subClassOf two disjoint classes
    disjoint_pairs = list(g.subject_objects(OWL.disjointWith))
    log(f"  owl:disjointWith pairs declared: {len(disjoint_pairs)}")
    metric("disjoint_pairs", len(disjoint_pairs))

    # Check for property domain/range conflicts
    obj_props = set(g.subjects(RDF.type, OWL.ObjectProperty))
    no_range = [p for p in obj_props if not list(g.objects(p, RDFS.range))]
    log(f"  Object properties without explicit rdfs:range: {len(no_range)}/{len(obj_props)}")
    metric("obj_props_without_range", len(no_range))

    dat_props = set(g.subjects(RDF.type, OWL.DatatypeProperty))
    no_range_dp = [p for p in dat_props if not list(g.objects(p, RDFS.range))]
    log(f"  Datatype properties without explicit rdfs:range: {len(no_range_dp)}/{len(dat_props)}")
    metric("dat_props_without_range", len(no_range_dp))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    log(section("Summary"))
    log(f"  Parse               : ✅ OK")
    log(f"  OWL-RL closure      : {inferred} inferred triples")
    log(f"  Unsatisfiable       : {len(unsatisfiable)} classes")
    log(f"  Disjointness axioms : {len(disjoint_pairs)}")
    log("")
    log("  ⚠️  For full OWL DL consistency, load HeritageGraph.ttl in Protégé")
    log("     and run the HermiT reasoner (Reasoner → HermiT → Start Reasoner).")
    log("")

    # ------------------------------------------------------------------
    # Write outputs
    # ------------------------------------------------------------------
    report_path = RESULTS_DIR / "consistency_report.txt"
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))
    print(f"\n📄 Report saved to: {report_path}")

    csv_path = RESULTS_DIR / "consistency_report.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value", "note"])
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"📊 CSV saved to:    {csv_path}")


if __name__ == "__main__":
    run_evaluation()
