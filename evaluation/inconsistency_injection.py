#!/usr/bin/env python3
"""Inconsistency injection: show the tenure cardinality axioms are load-bearing.

Addresses the reviewer request to demonstrate that the OWL axioms "bite rather
than decorate". KumariTenure carries an unqualified owl:maxCardinality 1
restriction on embodiedDeity (single-deity embodiment per tenure). Under OWL
open-world semantics a tenure with two embodiedDeity values is NOT by itself
inconsistent -- the reasoner merges the two names -- so the test has two arms:

  Arm A (expected INCONSISTENT): a tenure with two embodiedDeity values that
        are declared owl:differentFrom each other. HermiT must derive a clash
        with the max-1 restriction.
  Arm B (control, expected CONSISTENT): the same ABox without
        owl:differentFrom. HermiT must instead infer that the two names
        co-denote, exactly as OWL semantics prescribe.
  Arm C (expected INCONSISTENT): an individual typed both hg:Stupa and
        hg:Chaitya, the one asserted owl:disjointWith pair. HermiT must
        report the joint instance unsatisfiable-membership, showing the
        single disjointness axiom is likewise load-bearing.

Requires: a ROBOT jar and a Java runtime. Paths are taken from the
ROBOT_JAR and JAVA_HOME environment variables, with the defaults below.

Run:  ROBOT_JAR=/tmp/hgtools/robot.jar \
      JAVA_HOME=/tmp/hgtools/jdk-21.0.11+10-jre/Contents/Home \
      python3 evaluation/inconsistency_injection.py
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROBOT_JAR = os.environ.get("ROBOT_JAR", "/tmp/hgtools/robot.jar")
JAVA_HOME = os.environ.get("JAVA_HOME", "/tmp/hgtools/jdk-21.0.11+10-jre/Contents/Home")
JAVA = str(Path(JAVA_HOME) / "bin" / "java")

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
    sys.exit(0)
print("\nFAIL: unexpected verdict in at least one arm.")
sys.exit(1)
