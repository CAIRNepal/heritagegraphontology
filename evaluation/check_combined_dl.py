#!/usr/bin/env python3
"""OWL 2 DL profile + HermiT consistency of the ontology combined with each example ABox.

For the ontology alone and for ontology + each example in examples/, the inputs
are parsed into ONE rdflib graph (owl:imports stripped, as the released Turtle
is self-contained) and serialised to a single Turtle file, which is then checked
with ROBOT:

    robot validate-profile --profile DL     (must report "in profile")
    robot reason --reasoner HermiT           (must be consistent, no unsatisfiable classes)

The single-graph parse matters: merging separately parsed files with
`robot merge` lets OWLAPI type each file's undeclared predicates on its own, so
a predicate the ontology declares as an object property but the data uses with
a literal is silently read as an annotation property and the punning violation
disappears. One graph exposes it.

Requires Java and the ROBOT jar (1.9.8): set ROBOT_JAR (default
/tmp/hgtools/robot.jar) and optionally JAVA_HOME. Combined files and ROBOT
output are written to evaluation/results/combined/. Exit status is non-zero if
any combination is outside OWL 2 DL or inconsistent.

Run:  ROBOT_JAR=/path/to/robot.jar python3 evaluation/check_combined_dl.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from rdflib import Graph, OWL

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
EXAMPLES = ROOT / "examples"
OUT = Path(__file__).resolve().parent / "results" / "combined"

ROBOT_JAR = os.environ.get("ROBOT_JAR", "/tmp/hgtools/robot.jar")
JAVA = (str(Path(os.environ["JAVA_HOME"]) / "bin" / "java")
        if os.environ.get("JAVA_HOME") else shutil.which("java") or "java")

SKIPPED = {
    "lux-murti-merged.ttl": "needs the LUX bridge module, which is built on the "
                            "pre-1.0.0 schema lineage (out of scope until migrated)",
}


def robot(*args: str) -> tuple[int, str]:
    proc = subprocess.run([JAVA, "-jar", ROBOT_JAR, *args],
                          capture_output=True, text=True)
    # drop JVM start-up noise (deprecation warnings, JAVA_TOOL_OPTIONS echo)
    lines = [l for l in (proc.stdout + proc.stderr).splitlines()
             if l.strip() and not l.startswith(("WARNING:", "Picked up "))]
    return proc.returncode, "\n".join(lines)


def combine(name: str, abox: Path | None) -> Path:
    g = Graph()
    g.parse(TTL, format="turtle")
    if abox is not None:
        g.parse(abox, format="turtle")
    g.remove((None, OWL.imports, None))
    path = OUT / f"{name}.ttl"
    g.serialize(destination=path, format="turtle")
    return path


def check(name: str, abox: Path | None) -> bool:
    combined = combine(name, abox)
    print(f"\n=== {name}  ({combined.relative_to(ROOT)})")
    rc_p, profile = robot("validate-profile", "--profile", "DL", "--input", str(combined))
    print(f"-- robot validate-profile --profile DL  (exit {rc_p})")
    print(profile)
    rc_r, reason = robot("reason", "--reasoner", "HermiT", "--input", str(combined),
                         "--output", str(OUT / f"{name}.reasoned.ttl"))
    print(f"-- robot reason --reasoner HermiT  (exit {rc_r})")
    if reason:
        print(reason)
    print("consistent, no unsatisfiable classes" if rc_r == 0
          else "INCONSISTENT or unsatisfiable classes")
    ok = rc_p == 0 and "[Ontology and imports closure in profile]" in profile and rc_r == 0
    print(f"=> {'PASS' if ok else 'FAIL'}: {name}")
    return ok


def main() -> int:
    if not Path(ROBOT_JAR).is_file():
        print(f"ROBOT jar not found at {ROBOT_JAR} (set ROBOT_JAR)", file=sys.stderr)
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    results = {"ontology": check("ontology", None)}
    for abox in sorted(EXAMPLES.glob("*.ttl")):
        if abox.name in SKIPPED:
            print(f"\n=== SKIPPED {abox.name}: {SKIPPED[abox.name]}")
            continue
        results[abox.stem] = check(f"ontology+{abox.stem}", abox)

    print("\nSummary:")
    for name, ok in results.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    for name, why in SKIPPED.items():
        print(f"  [SKIP] {name}: {why}")
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
