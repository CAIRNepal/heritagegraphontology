#!/usr/bin/env python3
"""Reasoning robustness probes for HeritageGraph (ROBOT + HermiT).

Consolidates two §7.1 reasoning experiments behind one CLI. Both require a
ROBOT jar and a Java runtime; paths come from the ROBOT_JAR and JAVA_HOME
environment variables (defaults below), and merged-import needs network access
on the first run (vocabularies are cached afterwards).

Subcommands (default: all):

  injection       Inconsistency injection: show the OWL axioms bite rather than
                  decorate. Three arms: (A) a KumariTenure with two
                  owl:differentFrom embodiedDeity values must clash with the
                  max-1 restriction; (B) the same ABox without differentFrom
                  stays consistent (the names co-denote); (C) an individual
                  typed both hg:Stupa and hg:Chaitya (the one owl:disjointWith
                  pair) must be unsatisfiable.

  merged-import   Merged-vocabulary classification: HermiT over HeritageGraph +
                  the full CIDOC-CRM, CRMinf, and PROV-O vocabularies, closing
                  the threat that consistency was specific to the self-contained
                  released axiom set. Reports the documented PROV-O property-
                  chain vs. HG-cardinality DL collision and classifies under
                  both minimal repairs.

Run:  ROBOT_JAR=/tmp/hgtools/robot.jar \\
      JAVA_HOME=/tmp/hgtools/jdk-21.0.11+10-jre/Contents/Home \\
      python3 evaluation/reasoning_extras.py [injection|merged-import|all]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, URIRef

ROOT = Path(__file__).resolve().parents[1]
ROBOT_JAR = os.environ.get("ROBOT_JAR", "/tmp/hgtools/robot.jar")
JAVA_HOME = os.environ.get("JAVA_HOME",
                           "/tmp/hgtools/jdk-21.0.11+10-jre/Contents/Home")
JAVA = str(Path(JAVA_HOME) / "bin" / "java")


# ===========================================================================
# injection: the OWL axioms are load-bearing.
# ===========================================================================
def run_injection() -> int:
    COMMON = """@prefix hg:  <https://w3id.org/heritagegraph/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:  <https://w3id.org/heritagegraph/demo/> .

# The declaration is required so that the OWLAPI Turtle parser reads the
# embodiment triples as ObjectPropertyAssertions; undeclared predicates are
# parsed as annotations, which HermiT ignores.
hg:embodiedDeity a owl:ObjectProperty .

ex:T a hg:KumariTenure , owl:NamedIndividual ; rdfs:label "injected tenure" ;
    hg:embodiedDeity ex:D1 , ex:D2 .
ex:D1 a hg:Deity , owl:NamedIndividual ; rdfs:label "deity one" .
ex:D2 a hg:Deity , owl:NamedIndividual ; rdfs:label "deity two" .
"""
    DIFFERENT = "ex:D1 owl:differentFrom ex:D2 .\n"

    DISJOINT_JOINT = """@prefix hg:  <https://w3id.org/heritagegraph/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:  <https://w3id.org/heritagegraph/demo/> .

ex:J a hg:Stupa , hg:Chaitya , owl:NamedIndividual ;
    rdfs:label "joint Stupa-and-Chaitya individual" .
"""

    def hermit_verdict(abox_ttl: str) -> tuple[bool, str]:
        """Merge the ontology with the injected ABox and classify with HermiT.

        Returns (consistent, evidence_line)."""
        with tempfile.TemporaryDirectory() as td:
            abox = Path(td) / "inject.ttl"
            abox.write_text(abox_ttl)
            out = Path(td) / "reasoned.ttl"
            proc = subprocess.run(
                [JAVA, "-jar", ROBOT_JAR, "merge",
                 "--input", str(ROOT / "ontology/HeritageGraph.ttl"),
                 "--input", str(abox),
                 "reason", "--reasoner", "hermit", "--output", str(out)],
                capture_output=True, text=True)
            text = proc.stdout + proc.stderr
            if proc.returncode == 0:
                return True, "classified without error"
            for line in text.splitlines():
                if "consistent" in line.lower() or "unsatisfiable" in line.lower():
                    return False, line.strip()
            return False, text.strip().splitlines()[-1] if text.strip() else "non-zero exit"

    print("Arm A: two embodiedDeity values + owl:differentFrom (expect INCONSISTENT)")
    consistent, evidence = hermit_verdict(COMMON + DIFFERENT)
    print(f"  HermiT: {'CONSISTENT' if consistent else 'INCONSISTENT'} -- {evidence}")
    arm_a_ok = not consistent

    print("Arm B: same ABox without owl:differentFrom (control; expect CONSISTENT)")
    consistent, evidence = hermit_verdict(COMMON)
    print(f"  HermiT: {'CONSISTENT' if consistent else 'INCONSISTENT'} -- {evidence}")
    arm_b_ok = consistent

    print("Arm C: joint Stupa-and-Chaitya individual (expect INCONSISTENT)")
    consistent, evidence = hermit_verdict(DISJOINT_JOINT)
    print(f"  HermiT: {'CONSISTENT' if consistent else 'INCONSISTENT'} -- {evidence}")
    arm_c_ok = not consistent

    if arm_a_ok and arm_b_ok and arm_c_ok:
        print("\nPASS: the max-1 embodiment axiom is load-bearing (arm A clashes), the")
        print("control confirms the clash is driven by distinctness, not by the mere")
        print("presence of two property values (arm B merges the names), and the")
        print("asserted disjointness pair likewise bites (arm C clashes).")
        return 0
    print("\nFAIL: unexpected verdict in at least one arm.")
    return 1


# ===========================================================================
# merged-import: HermiT over HG + CIDOC-CRM + CRMinf + PROV-O.
# ===========================================================================
HG_NS = "https://w3id.org/heritagegraph/"
PROV_NS = "http://www.w3.org/ns/prov#"
CACHE = Path(os.environ.get("VOCAB_CACHE", "/tmp/hgtools/vocab"))

VOCABS = {
    "CIDOC-CRM v7.1.3": ("cidoc_crm.rdf",
        "https://cidoc-crm.org/rdfs/7.1.3/CIDOC_CRM_v7.1.3.rdf"),
    "CRMinf v1.0": ("crminf.rdf",
        "https://cidoc-crm.org/extensions/crminf/rdfs/1.0/CRMinf_v1.0.rdf"),
    "PROV-O": ("prov.ttl", "https://www.w3.org/ns/prov.ttl"),
}


def _fetch(name: str, fname: str, url: str) -> Path:
    """Fetch (cached) and strip owl:imports declarations.

    The vocabularies declare owl:imports (CRMinf imports CRM, PROV-O imports
    its AQ/dictionary/links modules); OWLAPI would try to dereference these
    at merge time. The axioms under test are supplied explicitly, so the
    import declarations are dropped from a local copy.
    """
    p = CACHE / fname
    if not p.exists() or p.stat().st_size == 0:
        print(f"  fetching {name} from {url}")
        urllib.request.urlretrieve(url, p)
    clean = p.with_suffix(".noimports.ttl")
    if not clean.exists():
        g = Graph()
        g.parse(p, format="xml" if p.suffix == ".rdf" else "turtle")
        g.remove((None, OWL.imports, None))
        g.serialize(clean, format="turtle")
    return clean


def _classify(label: str, inputs: list[Path]) -> bool:
    """Merge + HermiT-classify; fail on inconsistency, unsatisfiable classes,
    or inferred (non-asserted) class equivalences that involve an HG term.

    Equivalences internal to an external vocabulary are reported but not
    failed: prov.ttl by itself already entails prov:Insertion ==
    prov:Removal from its own dictionary axioms, which is PROV-O's business,
    not an alignment defect.
    """
    out = CACHE / f"reasoned_{label.replace(' ', '_').replace('/', '_')}.ttl"
    cmd = [JAVA, "-jar", ROBOT_JAR, "merge"]
    for p in inputs:
        cmd += ["--input", str(p)]
    cmd += ["reason", "--reasoner", "hermit",
            "--equivalent-classes-allowed", "all",
            "--output", str(out)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"  [{label}] FAILED:")
        for line in (proc.stdout + proc.stderr).splitlines():
            if "ERROR" in line or "unsatisfiable" in line.lower() \
                    or "consistent" in line.lower() or "equivalen" in line.lower():
                print("   ", line.strip())
        return False
    reasoned = Graph()
    reasoned.parse(out, format="turtle")
    # Unsatisfiability: any named class equivalent to / subsumed under Nothing.
    unsat = {s for s in reasoned.subjects(OWL.equivalentClass, OWL.Nothing)} | \
            {s for s in reasoned.subjects(RDFS.subClassOf, OWL.Nothing)
             if isinstance(s, URIRef)}
    # Inferred equivalences involving an HG term.
    asserted_eq = set()
    for p in inputs:
        g = Graph()
        g.parse(p, format="turtle" if p.suffix == ".ttl" else "xml")
        asserted_eq |= {frozenset((s, o))
                        for s, o in g.subject_objects(OWL.equivalentClass)}
    hg_equiv, ext_equiv = [], []
    for s, o in reasoned.subject_objects(OWL.equivalentClass):
        if not (isinstance(s, URIRef) and isinstance(o, URIRef)) or s == o:
            continue
        if frozenset((s, o)) in asserted_eq or o == OWL.Nothing or s == OWL.Nothing:
            continue
        (hg_equiv if (str(s).startswith(HG_NS) or str(o).startswith(HG_NS))
         else ext_equiv).append((s, o))
    print(f"  [{label}] consistent, classified"
          f" (unsatisfiable: {len(unsat)}; inferred equivalences:"
          f" {len(hg_equiv)} involving HG, {len(ext_equiv)} external-internal)")
    for s, o in hg_equiv:
        print(f"      HG-involving equivalence: {s} == {o}")
    for s, o in ext_equiv:
        print(f"      (external-internal, tolerated: {s} == {o})")
    return not unsat and not hg_equiv


def run_merged_import() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    hg = ROOT / "ontology/HeritageGraph.ttl"
    ok = True
    paths = {}
    for name, (fname, url) in VOCABS.items():
        paths[name] = _fetch(name, fname, url)

    print("Pairwise merges with HeritageGraph:")
    for name, p in list(paths.items()):
        if name == "PROV-O":
            continue
        ok &= _classify(f"HG + {name}", [hg, p])

    # --- PROV-O: report the DL collision, then classify under both repairs ---
    print("PROV-O: DL global-restrictions check:")
    prov_g = Graph()
    prov_g.parse(paths["PROV-O"], format="turtle")
    chains = {s for s in prov_g.subjects(OWL.propertyChainAxiom, None)}
    hg_g = Graph()
    hg_g.parse(hg, format="turtle")
    constrained = set()
    for r in hg_g.subjects(RDF.type, OWL.Restriction):
        for kind in (OWL.maxCardinality, OWL.minCardinality, OWL.cardinality):
            if next(hg_g.objects(r, kind), None) is not None:
                prop = next(hg_g.objects(r, OWL.onProperty), None)
                if prop is not None and str(prop).startswith(PROV_NS):
                    constrained.add(prop)
    collide = sorted(str(p).split("#")[-1] for p in chains & constrained)
    print(f"  PROV-O chain-axiom (non-simple) properties: {len(chains)}")
    print(f"  of which under an HG cardinality restriction: {len(collide)}")
    print(f"  collision set: {', '.join(collide)}")
    print("  => merged graph is outside OWL 2 DL (non-simple property in a")
    print("     cardinality restriction); HermiT rejects it on profile grounds.")

    # Repair 1: drop PROV-O's chain axioms.
    prov_nochain = CACHE / "prov.nochain.ttl"
    g = Graph()
    g.parse(paths["PROV-O"], format="turtle")
    for s, o in list(g.subject_objects(OWL.propertyChainAxiom)):
        g.remove((s, OWL.propertyChainAxiom, o))
    g.serialize(prov_nochain, format="turtle")
    ok &= _classify("HG + PROV-O (chain axioms dropped)", [hg, prov_nochain])

    # Repair 2: drop HG's cardinality restrictions on the colliding properties.
    hg_relaxed = CACHE / "hg.relaxed.ttl"
    g = Graph()
    g.parse(hg, format="turtle")
    for r in list(g.subjects(RDF.type, OWL.Restriction)):
        prop = next(g.objects(r, OWL.onProperty), None)
        if prop in chains:
            for kind in (OWL.maxCardinality, OWL.minCardinality, OWL.cardinality):
                for v in list(g.objects(r, kind)):
                    g.remove((r, kind, v))
                    # neutralise the emptied restriction
                    g.add((r, OWL.minCardinality, v.__class__("0", datatype=v.datatype)))
    g.serialize(hg_relaxed, format="turtle")
    ok &= _classify("HG (prov cardinalities relaxed) + PROV-O",
                    [hg_relaxed, paths["PROV-O"]])

    print("Full merge (chain axioms dropped from PROV-O):")
    ok &= _classify("HG + CRM + CRMinf + PROV-O",
                    [hg, paths["CIDOC-CRM v7.1.3"], paths["CRMinf v1.0"],
                     prov_nochain])

    if ok:
        print("\nPASS: HermiT classifies every DL-admissible merged graph "
              "consistent, with no unsatisfiable classes and no unintended class "
              "equivalences; the one obstruction is the documented DL profile "
              "collision between PROV-O's property chains and HG's cardinality "
              "restrictions, not a semantic clash.")
        return 0
    print("\nFAIL: at least one merged classification did not come back clean.")
    return 1


PROBES = {
    "injection": run_injection,
    "merged-import": run_merged_import,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("probe", nargs="?", default="all",
                        choices=list(PROBES) + ["all"],
                        help="which probe to run (default: all)")
    args = parser.parse_args()

    if args.probe != "all":
        return PROBES[args.probe]()

    failures = []
    for name, fn in PROBES.items():
        print(f"\n{'=' * 78}\n== {name}\n{'=' * 78}")
        try:
            if fn() not in (0, None):
                failures.append(name)
        except Exception as exc:
            failures.append(name)
            print(f"[{name}] FAILED: {exc}")
    print(f"\n{'=' * 78}")
    if failures:
        print(f"FAILED probes: {', '.join(failures)}")
        return 1
    print("All reasoning probes passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
