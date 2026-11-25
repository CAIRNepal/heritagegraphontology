#!/usr/bin/env python3
"""CQ traceability and mutation analysis (a report, not a release gate).

The 32 CQs are an instantiability check: each asks whether the ontology can
represent and retrieve one documented kind of fact, with a demonstrator
witness (often a single one). This script measures how much the suite tests:

1. Traceability: which HeritageGraph classes and properties each CQ uses,
   and how many demonstrator instances each term has
   (results/cq_traceability.csv).
2. Mutation analysis (results/cq_mutation.csv), three operators, each scored
   per CQ as killed / applicable mutants (a mutant is killed when the CQ's
   answer set no longer equals its gold):
   a. ABox deletion: delete each demonstrator triple in turn.
   b. IRI swap: replace each HeritageGraph term in the query with each of its
      siblings: the HG terms that share a direct superclass (classes) or a
      direct superproperty (properties). A mutant that raises an error is
      invalid, not killed; kills that return no rows at all are reported
      separately from kills that return different rows.
   c. TBox deletion: delete each rdfs:subClassOf / rdfs:subPropertyOf axiom
      between HeritageGraph terms (asserted arm: the queries' rdfs:subClassOf*
      paths read the TBox).

    python3 evaluation/cq_coverage.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, URIRef

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evaluation"))
from run_abox_cq32 import (ABOX, EXPECTED, PAIRS, QUERIES, TBOX, actual_rows,  # noqa: E402
                           load_queries, sameas_alias)

HG = "https://cair-nepal.org/heritagegraph/"
RESULTS = ROOT / "evaluation" / "results"


def hg_terms(sparql: str) -> set[str]:
    return set(re.findall(r"hg:([A-Za-z][A-Za-z0-9_]*)", sparql))


def main() -> int:
    tbox = Graph().parse(TBOX, format="turtle")
    abox = Graph().parse(ABOX, format="turtle")
    alias = sameas_alias(abox)
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    queries = load_queries(QUERIES)
    gold = {cq: sorted({tuple(r) for r in expected[f"CQ{cq}"]["expected"]}) for cq, _, _ in queries}

    enums = {str(c)[len(HG):] for c in tbox.subjects(OWL.oneOf, None) if str(c).startswith(HG)}
    classes = {str(c)[len(HG):] for c in tbox.subjects(RDF.type, OWL.Class)
               if str(c).startswith(HG) and (c, OWL.deprecated, None) not in tbox
               and "#" not in str(c)} - enums
    props = {str(p)[len(HG):] for t in (OWL.ObjectProperty, OWL.DatatypeProperty)
             for p in tbox.subjects(RDF.type, t)
             if str(p).startswith(HG) and (p, OWL.deprecated, None) not in tbox}

    def run(g: Graph, cq: int, sparql: str) -> list:
        return [tuple(r) for r in actual_rows(g, sparql, alias, PAIRS.get(cq))]

    base = Graph(); base += tbox; base += abox
    for cq, _, sparql in queries:
        assert run(base, cq, sparql) == gold[cq], f"CQ{cq} does not pass on the unmutated graph"

    # 1. traceability
    used = defaultdict(list)
    for cq, _, sparql in queries:
        for t in hg_terms(sparql):
            used[t].append(f"CQ{cq}")
    inst = defaultdict(int)
    for s, p, o in abox:
        if p == RDF.type and str(o).startswith(HG):
            inst[str(o)[len(HG):]] += 1
        elif str(p).startswith(HG):
            inst[str(p)[len(HG):]] += 1
        if isinstance(o, URIRef) and str(o).startswith(HG) and "#" in str(o)[len(HG):]:
            inst[str(o)[len(HG):].split("#")[0]] += 1       # an enumeration value in use
    with open(RESULTS / "cq_traceability.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["term", "kind", "used_in_cqs", "demonstrator_uses"])
        for t in sorted(classes | props | enums):
            w.writerow([f"hg:{t}", "enumeration" if t in enums else "class" if t in classes else "property",
                        " ".join(used.get(t, [])), inst.get(t, 0)])
    cls_cq = sum(1 for t in classes if t in used)
    prp_cq = sum(1 for t in props if t in used)
    cls_inst = sum(1 for t in classes if inst.get(t))
    prp_inst = sum(1 for t in props if inst.get(t))
    en_cq = sum(1 for t in enums if t in used or any(f"{t}#" in q for _, _, q in queries))
    en_inst = sum(1 for t in enums if inst.get(t))
    print(f"Traceability: classes in a CQ {cls_cq}/{len(classes)}, instantiated {cls_inst}/{len(classes)}; "
          f"properties in a CQ {prp_cq}/{len(props)}, used in data {prp_inst}/{len(props)}; "
          f"enumerations in a CQ {en_cq}/{len(enums)}, a value used in data {en_inst}/{len(enums)}")

    # 2a. ABox deletion
    killed_by = defaultdict(int)
    critical = 0
    triples = list(abox)
    for t in triples:
        g = Graph(); g += tbox; g += abox; g.remove(t)
        hit = [cq for cq, _, sparql in queries if run(g, cq, sparql) != gold[cq]]
        critical += bool(hit)
        for cq in hit:
            killed_by[cq] += 1
    print(f"ABox deletion: {critical}/{len(triples)} triples ({100 * critical // len(triples)}%) "
          f"are needed by at least one CQ")

    # 2b. IRI swap
    def siblings(t: str) -> set[str]:
        term = URIRef(HG + t)
        rel = RDFS.subClassOf if t in classes else RDFS.subPropertyOf
        pool = classes if t in classes else props
        parents = {o for o in tbox.objects(term, rel) if isinstance(o, URIRef)}
        return {str(x)[len(HG):] for par in parents for x in tbox.subjects(rel, par)
                if str(x).startswith(HG) and str(x)[len(HG):] in pool} - {t}

    swap_k, swap_n, swap_empty, swap_invalid = (defaultdict(int) for _ in range(4))
    no_sibling = set()
    for cq, _, sparql in queries:
        for t in hg_terms(sparql):
            if t not in classes and t not in props:
                continue
            sibs = sorted(siblings(t))
            if not sibs:
                no_sibling.add(t)
            for other in sibs:
                mutant = re.sub(rf"hg:{re.escape(t)}\b", f"hg:{other}", sparql)
                try:
                    got = run(base, cq, mutant)
                except Exception:
                    swap_invalid[cq] += 1
                    continue
                swap_n[cq] += 1
                if got != gold[cq]:
                    swap_k[cq] += 1
                    swap_empty[cq] += not got
    # 2c. TBox deletion
    axioms = [(s, p, o) for p in (RDFS.subClassOf, RDFS.subPropertyOf)
              for s, o in tbox.subject_objects(p)
              if isinstance(o, URIRef) and str(s).startswith(HG) and str(o).startswith(HG)]
    tbox_k = defaultdict(int)
    for ax in axioms:
        g = Graph(); g += tbox; g += abox; g.remove(ax)
        for cq, _, sparql in queries:
            tbox_k[cq] += run(g, cq, sparql) != gold[cq]

    with open(RESULTS / "cq_mutation.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cq", "gold_rows", "abox_triples_needed", "sibling_swaps_killed",
                    "of_which_empty_result", "sibling_swaps", "tbox_axioms_needed"])
        for cq, _, _ in queries:
            w.writerow([f"CQ{cq}", len(gold[cq]), killed_by[cq], swap_k[cq], swap_empty[cq],
                        swap_n[cq], tbox_k[cq]])
    k, n, e = sum(swap_k.values()), sum(swap_n.values()), sum(swap_empty.values())
    print(f"Sibling swap: {k}/{n} valid mutants killed ({100 * k // max(n, 1)}%), {e} of them by an "
          f"empty result; {sum(swap_invalid.values())} invalid; {len(no_sibling)} query terms have no "
          f"sibling")
    print(f"TBox deletion: {len(axioms)} HG subClassOf/subPropertyOf axioms; "
          f"{sum(1 for cq in tbox_k if tbox_k[cq])}/32 CQs need at least one")
    sizes = defaultdict(int)
    for cq in gold:
        sizes[len(gold[cq])] += 1
    print(f"Gold-set sizes (rows: CQs): {dict(sorted(sizes.items()))}")
    print("Reports: results/cq_traceability.csv, results/cq_mutation.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
