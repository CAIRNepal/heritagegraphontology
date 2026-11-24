#!/usr/bin/env python3
"""Competency questions answered only with HeritageGraph's axioms (review C-3:
what do the OWL axioms contribute beyond SHACL and JSON Schema?).

Runs examples/queries/cq-inference.rq over the demonstrator ABox three ways:
  asserted    the ABox alone, no reasoning;
  vocab-only  OWL 2 RL closure (owlrl) of ABox + the official CIDOC-CRM 7.1.3,
              CRMinf 1.0 and PROV-O files (ontology/imports/);
  with HG     OWL 2 RL closure of ABox + those vocabularies + HeritageGraph.
Answers are counted modulo owl:sameAs (the demonstrator's Wikidata links). A
query passes iff "with HG" equals its frozen expected set, "vocab-only" equals
its frozen set (so a fact newly asserted in the ABox is noticed), and
"vocab-only" has strictly fewer rows: the extra answers are due to
HeritageGraph's own axioms, not to the reused vocabularies. Writes
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
IMPORTS = ROOT / "ontology" / "imports"
VOCABS = [("CIDOC_CRM_v7.1.3.rdf", "xml"), ("CRMinf_v1.0.rdf", "xml"), ("prov-o.ttl", "turtle")]
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
    """Bindings modulo owl:sameAs: every Wikidata alias is mapped back to the
    demonstrator resource it was asserted equal to (the map is built from the
    asserted ABox only, so its direction is fixed)."""
    res = g.query(q)
    return sorted({tuple(short(alias.get(r[v], r[v])) for v in res.vars) for r in res})


def closure(*graphs: Graph) -> Graph:
    g = Graph()
    for x in graphs:
        g += x
    g.remove((None, OWL.imports, None))
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    return g


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--freeze", action="store_true")
    args = ap.parse_args()
    abox = Graph().parse(ROOT / "examples" / "kathmandu-mini-abox.ttl", format="turtle")
    vocab = Graph()
    for f, fmt in VOCABS:
        vocab.parse(IMPORTS / f, format=fmt)
    hg = Graph().parse(ROOT / "ontology" / "HeritageGraph.ttl", format="turtle")
    alias = {o: s_ for s_, o in abox.subject_objects(OWL.sameAs)}
    without_hg = closure(abox, vocab)
    with_hg = closure(abox, vocab, hg)
    expected = {} if args.freeze or not EXPECTED.exists() else json.loads(EXPECTED.read_text())
    out = [f"Inference CQs: ABox {len(abox)} triples; vocab-only closure {len(without_hg)}; "
           f"with-HG closure {len(with_hg)}"]
    ok, frozen = True, {}
    for qid, question, sparql in load_queries():
        a = rows(abox, sparql, alias)
        v = rows(without_hg, sparql, alias)
        h = rows(with_hg, sparql, alias)
        frozen[qid] = {"question": question, "expected": [list(r) for r in h],
                       "expected_vocab_only": [list(r) for r in v]}
        e = expected.get(qid, {})
        exp_h = sorted(tuple(r) for r in e.get("expected", []))
        exp_v = sorted(tuple(r) for r in e.get("expected_vocab_only", []))
        exact = args.freeze or (h == exp_h and v == exp_v)
        due_to_hg = len(v) < len(h) and len(a) <= len(v)
        passed = exact and due_to_hg
        ok &= passed
        out.append(f"{qid} [{'PASS' if passed else 'FAIL'}] asserted={len(a)} vocab-only={len(v)} "
                   f"with-HG={len(h)}  {question}")
        if not exact:
            out.append(f"     with-HG missing={sorted(set(exp_h) - set(h))} unexpected={sorted(set(h) - set(exp_h))}")
            out.append(f"     vocab-only missing={sorted(set(exp_v) - set(v))} unexpected={sorted(set(v) - set(exp_v))}")
        if not due_to_hg:
            out.append("     HeritageGraph's axioms add no answer: not HG-dependent")
    if args.freeze:
        EXPECTED.write_text(json.dumps(frozen, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        out.append(f"froze {len(frozen)} expected answer sets to {EXPECTED.name}")
    out.append("PASS: every inference CQ is answered exactly, and only with HeritageGraph's axioms."
               if ok else "FAIL: see above.")
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "inference_cq_report.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
