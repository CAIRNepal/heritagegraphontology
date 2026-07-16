#!/usr/bin/env python3
"""Run all 32 competency questions as instance-level SELECT queries against
TBox + examples/kathmandu-mini-abox.ttl. A CQ passes when its query returns
at least one binding. Writes a per-CQ report (txt + csv) and a LaTeX table
body for the paper appendix."""

from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
TBOX = ROOT / "ontology" / "HeritageGraph.ttl"
ABOX = ROOT / "examples" / "kathmandu-mini-abox.ttl"
QUERIES = ROOT / "examples" / "queries" / "cq-abox-32.rq"
RESULTS = Path(__file__).resolve().parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

DIMENSIONS = {
    range(1, 7): "Structural",
    range(7, 19): "Ritual/Festival",
    range(19, 26): "Institutional/Syncretic",
    range(26, 33): "Living Goddess",
}


def dimension(cq: int) -> str:
    for r, name in DIMENSIONS.items():
        if cq in r:
            return name
    return "?"


def load_queries(path: Path) -> list[tuple[int, str, str]]:
    text = path.read_text(encoding="utf-8")
    blocks: list[tuple[int, str, str]] = []
    for m in re.finditer(
        r"^# CQ(\d+): (.*?)\n(.*?)(?=^# CQ\d+:|\Z)", text, re.M | re.S
    ):
        blocks.append((int(m.group(1)), m.group(2).strip(), m.group(3).strip()))
    return blocks


def main() -> int:
    g = Graph()
    g.parse(TBOX, format="turtle")
    g.parse(ABOX, format="turtle")

    queries = load_queries(QUERIES)
    assert len(queries) == 32, f"expected 32 queries, found {len(queries)}"

    lines = [
        "All-32 CQ ABox Execution",
        f"Date: {datetime.now().isoformat()}",
        f"TBox: {TBOX.name}",
        f"ABox: {ABOX.name}",
        f"Triples loaded: {len(g)}",
        "",
    ]
    rows = []
    passed = 0
    for cq, question, sparql in queries:
        results = list(g.query(sparql))
        n = len(results)
        status = "PASS" if n else "EMPTY"
        passed += bool(n)
        lines.append(f"CQ{cq:<3} [{status}] rows={n:<3} {question}")
        rows.append((f"CQ{cq}", dimension(cq), question, n, status))

    lines += ["", f"Total: {passed}/32 CQs return at least one binding."]
    report = "\n".join(lines)
    (RESULTS / "abox_cq32_report.txt").write_text(report + "\n", encoding="utf-8")
    with open(RESULTS / "abox_cq32_report.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cq", "dimension", "question", "rows", "status"])
        w.writerows(rows)

    print(report)
    return 0 if passed == 32 else 1


if __name__ == "__main__":
    raise SystemExit(main())
