#!/usr/bin/env python3
"""OWL 2 DL consistency check via HermiT (owlready2). Archives release log."""

from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from rdflib import Graph, OWL

ROOT = Path(__file__).resolve().parents[1]
OWL_SOURCE = ROOT / "ontology" / "review.owl"
STRIPPED = Path(__file__).resolve().parent / "HeritageGraph.hermit-check.owl"
RELEASE_LOG = ROOT / "release" / "evaluation" / "hermit_consistency_log.txt"
RESULTS_LOG = Path(__file__).resolve().parent / "results" / "hermit_consistency_log.txt"


def java_available() -> bool:
    try:
        proc = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
        )
        return proc.returncode == 0
    except FileNotFoundError:
        return False


def strip_imports(src: Path, dest: Path) -> None:
    g = Graph()
    g.parse(src, format="xml")
    for triple in list(g.triples((None, OWL.imports, None))):
        g.remove(triple)
    g.serialize(destination=dest, format="xml")


def run_hermit() -> tuple[bool, str]:
    from owlready2 import default_world, get_ontology, sync_reasoner_hermit

    strip_imports(OWL_SOURCE, STRIPPED)
    default_world.set_backend(filename=":memory:")
    onto = get_ontology(STRIPPED.resolve().as_uri()).load()
    class_count = len(list(onto.classes()))
    with onto:
        sync_reasoner_hermit(infer_property_values=False)
    unsat = list(default_world.inconsistent_classes())
    lines = [
        "HeritageGraph OWL 2 DL Consistency Check (HermiT)",
        f"Date: {datetime.now().isoformat()}",
        f"Source: {OWL_SOURCE} (imports stripped for local classification)",
        f"Classes classified: {class_count}",
        f"Unsatisfiable classes: {len(unsat)}",
        "",
    ]
    if unsat:
        lines.append("Unsatisfiable:")
        for cls in unsat:
            lines.append(f"  - {cls}")
        return False, "\n".join(lines)
    lines.append("Result: CONSISTENT (no unsatisfiable classes)")
    return True, "\n".join(lines)


def main() -> int:
    RELEASE_LOG.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_LOG.parent.mkdir(parents=True, exist_ok=True)

    if not java_available():
        msg = (
            "HermiT check skipped: Java runtime not found.\n"
            "Install Java 17+ or run this script in CI (ubuntu-latest).\n"
            "Manual steps: release/evaluation/HERMIT_INSTRUCTIONS.md\n"
        )
        RELEASE_LOG.write_text(msg, encoding="utf-8")
        RESULTS_LOG.write_text(msg, encoding="utf-8")
        print(msg)
        return 0

    if not OWL_SOURCE.exists():
        print(f"Missing {OWL_SOURCE}; run regenerate_ontology_artifacts.py first.", file=sys.stderr)
        return 1

    try:
        ok, report = run_hermit()
    except Exception as exc:
        report = f"HermiT check FAILED: {exc}\n"
        RELEASE_LOG.write_text(report, encoding="utf-8")
        RESULTS_LOG.write_text(report, encoding="utf-8")
        print(report, file=sys.stderr)
        return 1

    RELEASE_LOG.write_text(report, encoding="utf-8")
    shutil.copy2(RELEASE_LOG, RESULTS_LOG)
    print(report)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
