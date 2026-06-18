#!/usr/bin/env python3
"""Run ABox CQ sample queries against TBox + kathmandu-mini-abox.ttl."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
TBOX = ROOT / "ontology" / "HeritageGraph.ttl"
ABOX = ROOT / "examples" / "kathmandu-mini-abox.ttl"
QUERIES = ROOT / "examples" / "queries" / "abox-cq-samples.rq"
RELEASE = ROOT / "release" / "evaluation"
RELEASE.mkdir(parents=True, exist_ok=True)


def load_queries(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8")
    blocks: list[tuple[str, str]] = []
    current_name = ""
    current_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("# ") and not line.startswith("# ABox"):
            if current_lines and any(l.strip() for l in current_lines):
                blocks.append((current_name, "\n".join(current_lines)))
            current_name = line[2:].strip()
            current_lines = []
        elif line.startswith("PREFIX") or line.startswith("SELECT") or line.startswith("ASK") or line.strip().startswith("{"):
            current_lines.append(line)
        elif line.strip() and not line.startswith("#"):
            current_lines.append(line)
    if current_lines and any(l.strip() for l in current_lines):
        blocks.append((current_name, "\n".join(current_lines)))
    return blocks


def main() -> int:
    g = Graph()
    g.parse(TBOX, format="turtle")
    g.parse(ABOX, format="turtle")

    report = [
        "ABox CQ Sample Execution",
        f"Date: {datetime.now().isoformat()}",
        f"TBox: {TBOX}",
        f"ABox: {ABOX}",
        f"Triples loaded: {len(g)}",
        "",
    ]
    rows = []

    for name, sparql in load_queries(QUERIES):
        if "SELECT" not in sparql and "ASK" not in sparql:
            continue
        try:
            results = list(g.query(sparql))
            status = "PASS" if results else "EMPTY"
            report.append(f"[{status}] {name}: {len(results)} row(s)")
            rows.append({"query": name, "status": status, "rows": len(results)})
        except Exception as exc:
            report.append(f"[FAIL] {name}: {exc}")
            rows.append({"query": name, "status": "FAIL", "rows": 0, "error": str(exc)})

    out_txt = RELEASE / "abox_cq_report.txt"
    out_csv = RELEASE / "abox_cq_report.csv"
    out_txt.write_text("\n".join(report), encoding="utf-8")
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["query", "status", "rows", "error"], extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(out_txt.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
