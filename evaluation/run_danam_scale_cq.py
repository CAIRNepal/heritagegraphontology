#!/usr/bin/env python3
"""Answerability of the 32 competency questions over independently-sourced data.

Loads the released ontology (ontology/HeritageGraph.ttl) together with two
independent third-party knowledge graphs, both mapped to the released ontology:

  * data/reconciled/danam-heritagegraph.nq  -- ~130k triples reconciled from the
    DANAM / OpenStreetMap / Wikidata pipeline (tangible monuments + provenance);
  * data/reconciled/wikidata-kv.nq          -- Kathmandu Valley heritage facts
    pulled live from Wikidata (build dates, typology, styles, deity dedication),
    each statement carrying prov:wasDerivedFrom its Wikidata IRI (see
    data/enrich_wikidata.py).

It then runs the same 32 SPARQL queries used for the demonstrator
(examples/queries/cq-abox-32.rq). Unlike the demonstrator harness this is an
*answerability at scale over independent data* probe, so it reports the number
of bindings each CQ returns rather than an expected-vs-actual verdict: the
tangible and provenance layers are populated densely, whereas the
ritual/institutional/Living-Goddess layers -- which no structured dataset
records -- stay covered by the cited demonstrator ABox. This script measures
exactly that boundary."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from rdflib import Graph, ConjunctiveGraph

ROOT = Path(__file__).resolve().parents[1]
TBOX = ROOT / "ontology" / "HeritageGraph.ttl"
DATA = ROOT / "data" / "reconciled" / "danam-heritagegraph.nq"
WIKIDATA = ROOT / "data" / "reconciled" / "wikidata-kv.nq"
QUERIES = ROOT / "examples" / "queries" / "cq-abox-32.rq"

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
    return [
        (int(m.group(1)), m.group(2).strip(), m.group(3).strip())
        for m in re.finditer(r"^# CQ(\d+): (.*?)\n(.*?)(?=^# CQ\d+:|\Z)", text, re.M | re.S)
    ]


def main() -> int:
    print(f"Loading ontology {TBOX.name} ...")
    cg = ConjunctiveGraph()
    cg.parse(TBOX, format="turtle")
    print(f"Loading DANAM graph {DATA.name} ...")
    cg.parse(DATA, format="nquads")
    if WIKIDATA.exists():
        print(f"Loading Wikidata enrichment {WIKIDATA.name} ...")
        cg.parse(WIKIDATA, format="nquads")
    # Flatten to a single graph so default-graph CQ patterns see all data.
    g = Graph()
    for s, p, o in cg.triples((None, None, None)):
        g.add((s, p, o))
    print(f"Total triples (ontology + data, flattened): {len(g)}\n")

    queries = load_queries(QUERIES)
    answered = 0
    by_dim: Counter = Counter()
    dim_total: Counter = Counter()
    print(f"{'CQ':<5}{'dim':<24}{'rows':>8}  question")
    for cq, question, sparql in queries:
        rows = len(list(g.query(sparql)))
        dim = dimension(cq)
        dim_total[dim] += 1
        if rows:
            answered += 1
            by_dim[dim] += 1
        print(f"CQ{cq:<3}{dim:<24}{rows:>8}  {question[:60]}")

    print(f"\nAnswered (>=1 binding): {answered}/32 over the reconciled DANAM graph")
    print("By dimension (answered / total):")
    for dim in ["Structural", "Ritual/Festival", "Institutional/Syncretic", "Living Goddess"]:
        print(f"  {dim:<26} {by_dim[dim]}/{dim_total[dim]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
