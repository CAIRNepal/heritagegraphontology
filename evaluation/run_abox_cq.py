#!/usr/bin/env python3
"""Run the ABox competency-question SELECT queries against the populated KG.

Loads the TBox + the merged source named graphs (Wikidata + OSM + UNESCO +
intangible + DANAM, with their crosswalks) and executes one SELECT per CQ from
scripts/kg/queries/abox/CQ*.rq. Each query is ANSWERED if it returns >=1 row,
DATA-GAP if it returns 0 rows AND its header declares `# DATA-GAP: <reason>`
(an honestly-acknowledged absence), or EMPTY if it unexpectedly returns nothing.
Up to 3 sample bindings are captured per query.

Writes release/evaluation/abox_cq_report.txt and .csv.

Env:
  ABOX_SOURCES  comma-separated graph stems to load (default: the full merged set)
"""
from __future__ import annotations

import csv
import os
import re
from datetime import datetime
from pathlib import Path

from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]
TBOX = ROOT / "ontology" / "HeritageGraph.ttl"
KG = ROOT / "data" / "kg"
QUERY_DIR = ROOT / "scripts" / "kg" / "queries" / "abox"
RELEASE = ROOT / "release" / "evaluation"
RELEASE.mkdir(parents=True, exist_ok=True)

DEFAULT_SOURCES = ["wikidata", "osm", "unesco", "intangible", "danam",
                   "crosswalk", "intangible_crosswalk", "danam_crosswalk"]

HDR_TITLE = re.compile(r"^#\s*(CQ\d+)\s*:\s*(.*)$")
HDR_GAP = re.compile(r"^#\s*DATA-GAP:\s*(.*)$")


def load_graph() -> Graph:
    g = Graph()
    g.parse(TBOX, format="turtle")
    stems = os.environ.get("ABOX_SOURCES")
    stems = stems.split(",") if stems else DEFAULT_SOURCES
    for stem in stems:
        f = KG / f"{stem}.ttl"
        if f.exists():
            g.parse(f, format="turtle")
    return g


def parse_query(path: Path) -> tuple[str, str, str]:
    """Return (title, datagap_reason, sparql) for one .rq file."""
    title, gap = "", ""
    for line in path.read_text(encoding="utf-8").splitlines():
        m = HDR_TITLE.match(line)
        if m:
            title = m.group(2).strip(); continue
        m = HDR_GAP.match(line)
        if m:
            gap = m.group(1).strip()
    return title, gap, path.read_text(encoding="utf-8")


def fmt_binding(row, variables) -> str:
    parts = []
    for v in variables:
        val = row[v] if v in row.labels else None
        if val is not None:
            s = str(val)
            s = s.rsplit("/", 1)[-1] if s.startswith("http") else s
            parts.append(f"{v}={s}")
    return "; ".join(parts)


def main() -> int:
    g = load_graph()
    queries = sorted(QUERY_DIR.glob("CQ*.rq"))

    header = [
        "ABox Competency-Question Execution (populated KG)",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        f"TBox: {TBOX.relative_to(ROOT)}",
        f"Sources: {', '.join(DEFAULT_SOURCES)}",
        f"Triples loaded: {len(g)}",
        f"Queries: {len(queries)} (from {QUERY_DIR.relative_to(ROOT)})",
        "",
    ]
    lines, rows = [], []
    answered = datagap = empty = failed = 0

    for path in queries:
        cq = path.stem
        title, gap, sparql = parse_query(path)
        try:
            res = g.query(sparql)
            variables = [str(v) for v in res.vars] if res.vars else []
            results = list(res)
            n = len(results)
            samples = [fmt_binding(r, variables) for r in results[:3]]
            if n > 0:
                status = "ANSWERED"; answered += 1
            elif gap:
                status = "DATA-GAP"; datagap += 1
            else:
                status = "EMPTY"; empty += 1
        except Exception as exc:                       # noqa: BLE001
            status = "FAIL"; n = 0; samples = []; failed += 1
            gap = gap or f"query error: {exc}"

        lines.append(f"[{status:8}] {cq}: {title}  -> {n} row(s)")
        if status == "DATA-GAP":
            lines.append(f"             DATA-GAP: {gap}")
        for s in samples:
            lines.append(f"             • {s}")
        rows.append({
            "cq": cq, "title": title, "status": status, "rows": n,
            "datagap_reason": gap if status in ("DATA-GAP", "FAIL") else "",
            "sample_bindings": " || ".join(samples),
        })

    summary = (f"SUMMARY: {answered}/{len(queries)} CQs answered (non-empty) over "
               f"the populated KG; {datagap} DATA-GAP; "
               f"{empty} unexpected-empty; {failed} failed.")
    report = header + lines + ["", summary]

    (RELEASE / "abox_cq_report.txt").write_text("\n".join(report), encoding="utf-8")
    with (RELEASE / "abox_cq_report.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["cq", "title", "status", "rows",
                                           "datagap_reason", "sample_bindings"])
        w.writeheader(); w.writerows(rows)

    print("\n".join(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
