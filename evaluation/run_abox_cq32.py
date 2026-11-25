#!/usr/bin/env python3
"""Expected-vs-actual competency-question harness for HeritageGraph.

Runs all 32 competency questions as instance-level SPARQL 1.1 SELECT queries
against the released ontology (ontology/HeritageGraph.ttl) loaded together with
the demonstrator ABox (examples/kathmandu-mini-abox.ttl), and compares each
query's returned bindings against a frozen, domain-grounded expected answer set
(evaluation/cq_expected.json). Every predicate/class IRI in the queries is
declared in the released ontology, and the ABox validates against the published
SHACL shapes.

Pass criterion (deliberately stronger than mere non-emptiness): a CQ passes iff
the set of returned bindings equals its expected answer set exactly -- no
missing rows and no unexpected rows (an ArCo-style expected-vs-actual test,
after Carriero et al. 2020; and ICON-style, Sartini et al. 2023). This makes the
suite a re-runnable regression oracle: any change to the schema, the queries, or
the demonstrator data that alters an answer fails the test.

A negative control (--self-test, on by default) perturbs one expected answer and
confirms the harness reports a mismatch, demonstrating the oracle discriminates
rather than trivially confirming itself.

Writes a per-CQ report (txt + csv) and a LaTeX table body for the paper
appendix. This is the single canonical CQ runner for the paper.

The optional --entailment mode runs a complementary analysis instead of the
expected-vs-actual harness: it executes all 32 CQs twice -- over the asserted
graph (TBox + ABox) and over its OWL-RL deductive closure -- and reports which
answer sets grow under entailment, alongside a structural census of the suite
(triple patterns per CQ from the parsed SPARQL algebra, and how many CQs join
across two or more design patterns). The default no-argument invocation is
unchanged, so the CI/Makefile path still runs the expected-vs-actual oracle."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path

from rdflib import Graph, URIRef

ROOT = Path(__file__).resolve().parents[1]
TBOX = ROOT / "ontology" / "HeritageGraph.ttl"
ABOX = ROOT / "examples" / "kathmandu-mini-abox.ttl"
QUERIES = ROOT / "examples" / "queries" / "cq-abox-32.rq"
EXPECTED = Path(__file__).resolve().parent / "cq_expected.json"
RESULTS = Path(__file__).resolve().parent / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

DIMENSIONS = {
    range(1, 7): "Structural",
    range(7, 19): "Ritual/Festival",
    range(19, 26): "Institutional/Syncretic",
    range(26, 33): "Living Goddess",
}

# IRI prefixes stripped to their local names when canonicalising bindings, so
# the expected file and the query output are compared on stable short forms.
PREFIXES = [
    "https://cair-nepal.org/heritagegraph/example/",
    "https://cair-nepal.org/heritagegraph/",
    "http://vocab.getty.edu/aat/",
    "http://www.cidoc-crm.org/cidoc-crm/",
    "http://www.cidoc-crm.org/extensions/crminf/",
    "http://www.w3.org/ns/prov#",
    "http://www.w3.org/2000/01/rdf-schema#",
]


def dimension(cq: int) -> str:
    for r, name in DIMENSIONS.items():
        if cq in r:
            return name
    return "?"


def short(term) -> str | None:
    if term is None:
        return None
    s = str(term)
    if isinstance(term, URIRef):
        for p in PREFIXES:
            if s.startswith(p):
                return s[len(p):]
    return s


def load_queries(path: Path) -> list[tuple[int, str, str]]:
    text = path.read_text(encoding="utf-8")
    blocks: list[tuple[int, str, str]] = []
    for m in re.finditer(
        r"^# CQ(\d+): (.*?)\n(.*?)(?=^# CQ\d+:|\Z)", text, re.M | re.S
    ):
        blocks.append((int(m.group(1)), m.group(2).strip(), m.group(3).strip()))
    return blocks


# Symmetric-pair CQs: (?x, ?y) and (?y, ?x) are one answer, and a pair whose
# two members are the same resource (modulo owl:sameAs) is no answer.
PAIRS = {6: ("a", "b"), 22: ("group1", "group2"), 23: ("tradition1", "tradition2")}


def sameas_alias(abox: Graph) -> dict:
    """owl:sameAs aliases (the demonstrator's Wikidata links) mapped back to
    the demonstrator resource they were asserted equal to. Built from the
    asserted ABox only, so its direction is fixed."""
    from rdflib import OWL
    alias = {o: s for s, o in abox.subject_objects(OWL.sameAs)}
    # collision-safe: an alias linked to two resources would merge them
    targets = [o for _, o in abox.subject_objects(OWL.sameAs)]
    assert len(targets) == len(set(targets)), "an owl:sameAs alias names two demonstrator resources"
    assert not set(alias) & set(alias.values()), "owl:sameAs chains are not supported by the alias map"
    return alias


def actual_rows(graph: Graph, sparql: str, alias: dict | None = None,
                pair: tuple[str, str] | None = None) -> list[list]:
    """Bindings modulo owl:sameAs, as a duplicate-free sorted list: every
    alias is replaced by its demonstrator resource before comparison; for a
    symmetric-pair CQ the pair is put in a canonical order and identical
    members drop the row."""
    alias = alias or {}
    res = graph.query(sparql)
    out = set()
    names = [str(v) for v in res.vars]
    for row in res:
        vals = [short(alias.get(row[v], row[v])) for v in res.vars]
        if pair:
            i, j = names.index(pair[0]), names.index(pair[1])
            if vals[i] == vals[j]:
                continue
            if (vals[i] or "") > (vals[j] or ""):
                vals[i], vals[j] = vals[j], vals[i]
        out.add(tuple(vals))
    return sorted(list(r) for r in out)


# Pattern vocabulary for the multi-pattern census (used by --entailment): a CQ
# "touches" a pattern when its text mentions one of the pattern's signature terms.
PATTERN_TERMS = {
    "event-mediated": ["E12_Production", "E14_Condition_Assessment", "E3_Condition_State",
                       "Consecration", "Enshrinement", "E10_Transfer_of_Custody",
                       "P108_has_produced", "P34_concerned", "P44_has_condition"],
    "ritual": ["RitualEvent", "Festival", "performsRitual", "participatesInRitual",
               "invokesDeity", "P9i_forms_part_of", "ritualType", "performedByGroup",
               "ritualCriticality", "P183"],
    "institutional": ["Guthi", "guthiType", "CasteGroup", "traditionalRole",
                      "managedByGuthi", "transferredToGuthi", "P107",
                      "Endowment", "P105_right_held_by", "HereditaryRoleTenure",
                      "mandatedBy", "CustodyPeriod", "custodyHolder"],
    "syncretic": ["SyncreticRelationship", "syncreticType", "Deity", "assignedDeity",
                  "P141_assigned", "religiousTradition"],
    "living-goddess": ["Kumari", "embodiedDeity", "KumariTenure", "tenure",
                       "selectionRitual", "disqualifi"],
    "provenance": ["I2_Belief", "assertsAbout", "wasDerivedFrom", "wasAttributedTo",
                   "confidenceScore", "DataSource", "mentionedInSource"],
}


def run_entailment() -> int:
    """CQs under entailment: asserted triples vs. OWL-RL closure, plus a
    structural census of the query suite. Executes all 32 CQs over the asserted
    graph and over its OWL-RL deductive closure and reports which answer sets
    grow, then emits per-CQ triple-pattern counts (from the parsed SPARQL
    algebra) and how many CQs join across two or more design patterns."""
    from rdflib.plugins.sparql import prepareQuery
    from rdflib.plugins.sparql.algebra import traverse
    from owlrl import DeductiveClosure, OWLRL_Semantics

    def bgp_size(sparql: str) -> int:
        """Count triple patterns in the parsed algebra (BGPs + property paths)."""
        q = prepareQuery(sparql)
        count = 0

        def visit(node):
            nonlocal count
            if hasattr(node, "name"):
                if node.name == "BGP":
                    count += len(node.triples)
                elif node.name == "TriplesBlock":
                    count += len(node.triples)
            return None

        traverse(q.algebra, visitPre=visit)
        return count

    asserted = Graph()
    asserted.parse(TBOX, format="turtle")
    asserted.parse(ABOX, format="turtle")
    print(f"Asserted graph (TBox + ABox): {len(asserted)} triples")
    alias = sameas_alias(Graph().parse(ABOX, format="turtle"))

    closed = Graph()
    for t in asserted:
        closed.add(t)
    DeductiveClosure(OWLRL_Semantics).expand(closed)
    print(f"OWL-RL closure:               {len(closed)} triples\n")

    queries = load_queries(QUERIES)
    assert len(queries) == 32

    gained, unchanged, errors = [], [], []
    print(f"{'CQ':<5} {'tp':>3} {'patterns':>9} {'asserted':>9} {'closure':>8} {'delta':>6}")
    for cq, question, sparql in queries:
        touched = [p for p, terms in PATTERN_TERMS.items()
                   if any(t in sparql or t in question for t in terms)]
        try:
            tp = bgp_size(sparql)
        except Exception:
            tp = -1
        try:
            # modulo owl:sameAs, as the oracle: the Wikidata aliases are not new answers
            n_a = len(actual_rows(asserted, sparql, alias, PAIRS.get(cq)))
            n_c = len(actual_rows(closed, sparql, alias, PAIRS.get(cq)))
        except Exception as e:
            errors.append((cq, str(e)))
            continue
        delta = n_c - n_a
        print(f"CQ{cq:<3} {tp:>3} {len(touched):>9} {n_a:>9} {n_c:>8} {delta:>+6}")
        (gained if delta else unchanged).append((cq, n_a, n_c, touched))

    multi = [(cq, q, s) for cq, q, s in queries
             if len([p for p, terms in PATTERN_TERMS.items()
                     if any(t in s or t in q for t in terms)]) >= 2]
    tps = {cq: bgp_size(s) for cq, q, s in queries}

    print()
    print(f"Triple patterns per CQ: min {min(tps.values())}, "
          f"median {sorted(tps.values())[len(tps)//2]}, max {max(tps.values())}")
    print(f"CQs joining >=2 design patterns: {len(multi)}/32 "
          f"({', '.join('CQ%d' % cq for cq, _, _ in multi)})")
    print(f"CQs whose answer set GROWS under OWL-RL entailment (modulo owl:sameAs): {len(gained)}/32")
    for cq, n_a, n_c, touched in gained:
        print(f"  CQ{cq}: {n_a} -> {n_c} rows  (patterns: {', '.join(touched) or '-'})")
    print(f"CQs unchanged under entailment: {len(unchanged)}/32")
    if errors:
        print(f"Query errors: {errors}")
        return 1

    # --- Property-hierarchy demo ------------------------------------------
    # A CRM-only consumer question ("which actors performed which activities?",
    # crm:P14i_performed) whose demonstrator answers are asserted exclusively
    # through the HeritageGraph specialisation hg:performsRitual, declared
    # rdfs:subPropertyOf crm:P14i_performed. Zero rows over asserted triples,
    # non-empty under closure: the property hierarchy is doing the retrieval.
    DEMO = """PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
SELECT ?actor ?activity WHERE { ?actor crm:P14i_performed ?activity . }"""
    d_a = list(asserted.query(DEMO))
    d_c = list(closed.query(DEMO))
    print()
    print("Property-hierarchy demo: crm:P14i_performed (CRM vocabulary only)")
    print(f"  asserted graph: {len(d_a)} row(s); OWL-RL closure: {len(d_c)} row(s)")
    for r in d_c:
        print("   -> " + " | ".join(
            str(x).replace("https://cair-nepal.org/heritagegraph/example/", "") for x in r))
    if d_a or not d_c:
        print("DEMO FAILED: expected 0 asserted rows and >0 closure rows")
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-self-test",
        action="store_true",
        help="skip the negative-control discrimination check",
    )
    parser.add_argument(
        "--entailment",
        action="store_true",
        help="run the OWL-RL entailment + structural-census analysis instead "
             "of the expected-vs-actual harness",
    )
    args = parser.parse_args()

    if args.entailment:
        return run_entailment()

    g = Graph()
    g.parse(TBOX, format="turtle")
    g.parse(ABOX, format="turtle")
    alias = sameas_alias(Graph().parse(ABOX, format="turtle"))
    # second arm: the same CQs over the OWL-RL closure must give the same
    # answers (modulo owl:sameAs): the gold does not depend on whether the
    # consumer reasons
    from owlrl import DeductiveClosure, OWLRL_Semantics
    entailed = Graph()
    entailed += g
    DeductiveClosure(OWLRL_Semantics).expand(entailed)

    queries = load_queries(QUERIES)
    assert len(queries) == 32, f"expected 32 queries, found {len(queries)}"
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    assert len(expected) == 32, f"expected 32 gold entries, found {len(expected)}"

    lines = [
        "All-32 CQ expected-vs-actual execution",
        f"Date: {datetime.now().isoformat()}",
        f"TBox: {TBOX.name}",
        f"ABox: {ABOX.name}",
        f"Triples loaded: {len(g)}",
        "Pass criterion: returned bindings == expected answer set (exact match, modulo owl:sameAs),",
        "over the asserted graph AND over its OWL-RL closure.",
        "",
    ]
    rows = []
    passed = 0
    for cq, question, sparql in queries:
        gold = [list(r) for r in expected[f"CQ{cq}"]["expected"]]
        gold_sorted = sorted({tuple(r) for r in gold})
        gold_sorted = [list(r) for r in gold_sorted]
        got = actual_rows(g, sparql, alias, PAIRS.get(cq))
        got_e = actual_rows(entailed, sparql, alias, PAIRS.get(cq))
        match = got == gold_sorted and got_e == gold_sorted
        passed += bool(match)
        status = "PASS" if match else "FAIL"
        detail = ""
        for arm, rows_ in (("asserted", got), ("OWL-RL", got_e)):
            if rows_ != gold_sorted:
                missing = [r for r in gold_sorted if r not in rows_]
                unexpected = [r for r in rows_ if r not in gold_sorted]
                detail += f"  [{arm}] missing={missing} unexpected={unexpected}"
        lines.append(
            f"CQ{cq:<3} [{status}] expected={len(gold_sorted):<2} "
            f"actual={len(got):<2} {question}{detail}"
        )
        rows.append(
            (f"CQ{cq}", dimension(cq), question, len(gold_sorted), len(got), status)
        )

    lines += ["", f"Total: {passed}/32 CQs match their expected answer set."]

    # Negative control: mutate a query so it can no longer retrieve the intended
    # answer, and confirm the oracle reports a mismatch. This proves the suite
    # fails when a CQ is *not* answered, rather than trivially confirming an ABox
    # built to make every query non-empty.
    self_test_ok = None
    if not args.no_self_test:
        cq11 = next(q for q in queries if q[0] == 11)
        gold11 = sorted([list(r) for r in expected["CQ11"]["expected"]])
        # Break the recurrence-pattern hop with a predicate no triple uses.
        broken = cq11[2].replace(
            "hg:recurrencePattern ?pattern", "hg:doesNotExistPattern ?pattern"
        )
        broken_rows = actual_rows(g, broken, alias)
        broken_rows_e = actual_rows(entailed, broken, alias)
        self_test_ok = broken_rows != gold11 and broken_rows_e != gold11
        lines += [
            "",
            "Negative control (CQ11 with a broken predicate, both arms): "
            f"actual={len(broken_rows)} vs expected={len(gold11)} -> "
            f"{'mismatch detected (oracle discriminates)' if self_test_ok else 'NOT detected -- oracle is trivial'}",
        ]

    report = "\n".join(lines)
    (RESULTS / "abox_cq32_report.txt").write_text(report + "\n", encoding="utf-8")
    with open(RESULTS / "abox_cq32_report.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cq", "dimension", "question", "expected_rows", "actual_rows", "status"])
        w.writerows(rows)

    # LaTeX table body for the paper appendix (CQ, question, expected, match).
    tex = []
    current_dim = None
    for cq, dim, question, exp, act, status in rows:
        if dim != current_dim:
            tex.append(f"\\multicolumn{{4}}{{l}}{{\\textit{{{dim}}}}} \\\\")
            current_dim = dim
        mark = "\\checkmark" if status == "PASS" else "\\ding{55}"
        q = question.replace("&", "\\&")
        tex.append(f"{cq} & {q} & {exp} & {mark} \\\\")
    (RESULTS / "abox_cq32_table.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")

    print(report)
    ok = passed == 32 and (self_test_ok in (None, True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
