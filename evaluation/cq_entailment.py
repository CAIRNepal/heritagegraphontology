#!/usr/bin/env python3
"""CQs under entailment: asserted triples vs. OWL-RL closure, plus a
structural census of the query suite.

Addresses the reviewer observation that executing the 32 CQs with rdflib and
no reasoning demonstrates retrieval, not semantic capability: not a single
answer was shown to depend on subsumption, inverse expansion, or the
property hierarchy. The suggested design is cheap and decisive either way:
run all 32 CQs twice, over the asserted graph (TBox + demonstrator ABox, as
published) and over the OWL-RL deductive closure of the same graph, and
report which CQs change. If answers grow, the axiomatisation demonstrably
contributes to answering; if nothing changes, that is itself a finding about
how much the axioms contribute to this suite.

Also emits the census the reviewer asked for: per-CQ triple-pattern counts
(from the parsed SPARQL algebra, not regex) and how many CQs join across
two or more design patterns.

Run:  evaluation/.venv/bin/python evaluation/cq_entailment.py
"""
import re
import sys
from pathlib import Path

from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.algebra import traverse
from owlrl import DeductiveClosure, OWLRL_Semantics

ROOT = Path(__file__).resolve().parents[1]
TBOX = ROOT / "ontology" / "HeritageGraph.ttl"
ABOX = ROOT / "examples" / "kathmandu-mini-abox.ttl"
QUERIES = ROOT / "examples" / "queries" / "cq-abox-32.rq"

# Pattern vocabulary for the multi-pattern census: a CQ "touches" a pattern
# when its text mentions one of the pattern's signature terms.
PATTERN_TERMS = {
    "event-mediated": ["E12_Production", "E14_Condition_Assessment", "E3_Condition_State",
                       "Consecration", "Enshrinement", "E10_Transfer_of_Custody",
                       "P108_has_produced", "P34_concerned", "P44_has_condition"],
    "ritual": ["RitualEvent", "Festival", "performsRitual", "participatesInRitual",
               "invokesDeity", "P9i_forms_part_of", "ritualType", "performedByGroup",
               "ritualCriticality", "P120"],
    "institutional": ["Guthi", "guthiType", "CasteGroup", "traditionalRole",
                      "managedByGuthi", "transferredToGuthi", "P107"],
    "syncretic": ["SyncreticRelationship", "syncreticType", "Deity", "assignedDeity",
                  "P141_assigned", "religiousTradition"],
    "living-goddess": ["Kumari", "embodiedDeity", "KumariTenure", "tenure",
                       "selectionRitual", "disqualifi"],
    "provenance": ["I2_Belief", "assertsAbout", "wasDerivedFrom", "wasAttributedTo",
                   "confidenceScore", "DataSource", "mentionedInSource"],
}


def load_queries(path: Path):
    text = path.read_text(encoding="utf-8")
    return [(int(m.group(1)), m.group(2).strip(), m.group(3).strip())
            for m in re.finditer(r"^# CQ(\d+): (.*?)\n(.*?)(?=^# CQ\d+:|\Z)",
                                 text, re.M | re.S)]


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
        n_a = len(set(map(tuple, asserted.query(sparql))))
        n_c = len(set(map(tuple, closed.query(sparql))))
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
print(f"CQs whose answer set GROWS under OWL-RL entailment: {len(gained)}/32")
for cq, n_a, n_c, touched in gained:
    print(f"  CQ{cq}: {n_a} -> {n_c} rows  (patterns: {', '.join(touched) or '-'})")
print(f"CQs unchanged under entailment: {len(unchanged)}/32")
if errors:
    print(f"Query errors: {errors}")
    sys.exit(1)

# --- Property-hierarchy demo -----------------------------------------------
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
        str(x).replace("https://w3id.org/heritagegraph/demo/", "") for x in r))
if d_a or not d_c:
    print("DEMO FAILED: expected 0 asserted rows and >0 closure rows")
    sys.exit(1)
