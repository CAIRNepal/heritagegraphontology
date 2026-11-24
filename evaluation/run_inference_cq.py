#!/usr/bin/env python3
"""Competency questions answered only under reasoning (review C-3: what do the
OWL axioms contribute beyond SHACL and JSON Schema?).

Runs examples/queries/cq-inference.rq over the released ontology plus the
demonstrator ABox twice: over the asserted triples and over their OWL 2 RL
closure (owlrl), with answers counted modulo owl:sameAs. A query passes iff the closure's bindings equal the frozen
expected set in evaluation/cq_inference_expected.json (exact match, as in
run_abox_cq32.py) AND the asserted triples alone return strictly fewer rows,
i.e. the answer depends on the ontology's axioms. Writes
results/inference_cq_report.txt.

  python3 evaluation/run_inference_cq.py            # check
  python3 evaluation/run_inference_cq.py --freeze   # rewrite the expected sets
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import owlrl
from rdflib import OWL, Graph

ROOT = Path(__file__).resolve().parents[1]
QUERIES = ROOT / "examples" / "queries" / "cq-inference.rq"
EXPECTED = Path(__file__).resolve().parent / "cq_inference_expected.json"
RESULTS = Path(__file__).resolve().parent / "results"
PREFIXES = ["https://cair-nepal.org/heritagegraph/example/",
            "https://cair-nepal.org/heritagegraph/"]


def short(t) -> str:
    s = str(t)
    for p in PREFIXES:
        if s.startswith(p):
            return s[len(p):]
    return s


def load_queries() -> list[tuple[str, str, str]]:
    text = QUERIES.read_text(encoding="utf-8")
    return [(m.group(1), m.group(2).strip(), m.group(3).strip())
            for m in re.finditer(r"^# (IQ\d+): (.*?)\n(.*?)(?=^# IQ\d+:|\Z)", text, re.M | re.S)]


def rows(g: Graph, q: str, alias: dict) -> list[tuple[str, ...]]:
    """Bindings modulo owl:sameAs: the demonstrator links resources to Wikidata
    with owl:sameAs, so the closure repeats each answer under the Wikidata IRI;
    every alias is mapped back to its demonstrator resource."""
    res = g.query(q)
    return sorted({tuple(short(alias.get(r[v], r[v])) for v in res.vars) for r in res})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--freeze", action="store_true")
    args = ap.parse_args()
    asserted = Graph()
    asserted.parse(ROOT / "ontology" / "HeritageGraph.ttl", format="turtle")
    asserted.parse(ROOT / "examples" / "kathmandu-mini-abox.ttl", format="turtle")
    alias = {o: s_ for s_, o in asserted.subject_objects(OWL.sameAs)}
    closure = Graph()
    closure += asserted
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(closure)
    expected = {} if args.freeze or not EXPECTED.exists() else json.loads(EXPECTED.read_text())
    out, ok = [f"Inference CQs: asserted {len(asserted)} triples, OWL 2 RL closure {len(closure)} triples"], True
    frozen = {}
    for qid, question, sparql in load_queries():
        a, c = rows(asserted, sparql, alias), rows(closure, sparql, alias)
        frozen[qid] = {"question": question, "expected": [list(r) for r in c]}
        exp = sorted(tuple(r) for r in expected.get(qid, {}).get("expected", []))
        exact = args.freeze or c == exp
        needs_reasoning = len(a) < len(c)
        passed = exact and needs_reasoning
        ok &= passed
        out.append(f"{qid} [{'PASS' if passed else 'FAIL'}] asserted={len(a)} closure={len(c)} "
                   f"expected={len(exp) if not args.freeze else len(c)}  {question}")
        if not exact:
            out.append(f"     missing={sorted(set(exp) - set(c))} unexpected={sorted(set(c) - set(exp))}")
        if not needs_reasoning:
            out.append("     the asserted triples already answer it: not reasoning-dependent")
    if args.freeze:
        EXPECTED.write_text(json.dumps(frozen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        out.append(f"froze {len(frozen)} expected answer sets to {EXPECTED.name}")
    out.append("PASS: every inference CQ is answered exactly, and only under reasoning." if ok
               else "FAIL: see above.")
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "inference_cq_report.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
