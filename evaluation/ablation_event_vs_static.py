#!/usr/bin/env python3
"""Ablation: event-mediated representation vs. static property attachment.

Addresses the reviewer request for evidence that event mediation is better
than attaching contingent properties directly to objects, rather than merely
different. The experiment holds the FACT SET constant and varies only the
representation:

  * Event-mediated graph: the released demonstrator ABox
    (examples/kathmandu-mini-abox.ttl) loaded as-is. Facts about the
    Kasthamandap are carried by a crm:E12_Production event, a
    crm:E14_Condition_Assessment event, and two crminf:I2_Belief assertions.

  * Static-baseline graph: the same Kasthamandap facts flattened onto the
    object as direct, unqualified property values -- the representation
    available without event mediation or assertion reification. The baseline
    is deliberately charitable: every fact that CAN be attached statically IS
    attached (builder, style, location, both claimed construction dates, the
    2015 condition value).

Four natural-language questions are then posed to BOTH graphs, each as the
best-effort SPARQL translation available in that representation. For the
static graph we additionally run a DEGRADED variant of each failing query
(dropping the qualifying variables) to show what survives flattening -- i.e.
that the baseline is lossy, not a strawman.

Run:  python3 evaluation/ablation_event_vs_static.py
"""
from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[1]

PFX = """PREFIX hg:  <https://w3id.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX crminf: <http://www.ics.forth.gr/isl/CRMinf/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX ex:  <https://w3id.org/heritagegraph/demo/>
PREFIX st:  <https://w3id.org/heritagegraph/demo/static/>
"""

# ---------------------------------------------------------------------------
# Graph A: event-mediated (released demonstrator, unmodified).
# ---------------------------------------------------------------------------
event_g = Graph()
event_g.parse(ROOT / "examples/kathmandu-mini-abox.ttl", format="turtle")

# ---------------------------------------------------------------------------
# Graph B: static baseline -- the same Kasthamandap facts, attached directly.
# A per-value source/date CANNOT be expressed in this idiom without
# re-introducing reification, which is exactly the pattern under ablation.
# ---------------------------------------------------------------------------
static_g = Graph()
static_g.parse(data="""
@prefix hg:  <https://w3id.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix ex:  <https://w3id.org/heritagegraph/demo/> .
@prefix st:  <https://w3id.org/heritagegraph/demo/static/> .
@prefix aat: <http://vocab.getty.edu/aat/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Kasthamandap a hg:Temple ;
    rdfs:label "Kasthamandap" ;
    hg:hasArchitecturalStyle aat:300004829 ;
    crm:P55_has_current_location ex:KathmanduDurbarSquare ;
    st:builtBy ex:LicchaviBuilders ;
    st:constructionDate "12th century CE", "7th century CE" ;
    st:conditionState "Damaged" .
ex:LicchaviBuilders a crm:E39_Actor ; rdfs:label "Builders (tradition)" .
""", format="turtle")

# ---------------------------------------------------------------------------
# Paired questions. Each entry: (label, event-form query, static-form query,
# optional degraded static query showing what survives flattening).
# ---------------------------------------------------------------------------
QUESTIONS = [
    (
        "Q1  Who built the Kasthamandap?",
        PFX + """SELECT ?agent WHERE {
          ?p a crm:E12_Production ; crm:P108_has_produced ex:Kasthamandap ;
             crm:P14_carried_out_by ?agent . }""",
        PFX + """SELECT ?agent WHERE { ex:Kasthamandap st:builtBy ?agent . }""",
        None,
    ),
    (
        "Q2  What condition was identified for it, and by an assessment over which time-span?",
        PFX + """SELECT ?state ?ts WHERE {
          ?ca a crm:E14_Condition_Assessment ; crm:P34_concerned ex:Kasthamandap ;
              crm:P35_has_identified ?state ; crm:P4_has_time-span ?ts . }""",
        PFX + """SELECT ?state ?ts WHERE {
          ex:Kasthamandap st:conditionState ?state ; st:assessedOver ?ts . }""",
        PFX + """SELECT ?state WHERE { ex:Kasthamandap st:conditionState ?state . }""",
    ),
    (
        "Q3  Which construction dates are claimed, from which source, with what confidence?",
        PFX + """SELECT ?value ?source ?conf WHERE {
          ?a a crminf:I2_Belief ; hg:assertsAbout ex:Kasthamandap ;
             prov:value ?value ; prov:wasDerivedFrom ?source ;
             hg:confidenceScore ?conf . }""",
        PFX + """SELECT ?value ?source ?conf WHERE {
          ex:Kasthamandap st:constructionDate ?value .
          ?value st:derivedFrom ?source ; st:confidence ?conf . }""",
        PFX + """SELECT ?value WHERE { ex:Kasthamandap st:constructionDate ?value . }""",
    ),
    (
        "Q4  Which agent stands behind which of the two conflicting dates?",
        PFX + """SELECT ?value ?agent WHERE {
          ?a a crminf:I2_Belief ; hg:assertsAbout ex:Kasthamandap ;
             prov:value ?value ; prov:wasAttributedTo ?agent . }""",
        PFX + """SELECT ?value ?agent WHERE {
          ex:Kasthamandap st:constructionDate ?value .
          ?value st:attributedTo ?agent . }""",
        None,
    ),
]

print(f"Event graph: {len(event_g)} triples (released demonstrator, unmodified)")
print(f"Static baseline: {len(static_g)} triples (same facts, flattened)\n")
print(f"{'Question':<88}{'event':>7}{'static':>8}{'degraded':>10}")
print("-" * 113)
event_answered = static_answered = 0
for label, q_event, q_static, q_degraded in QUESTIONS:
    n_e = len(list(event_g.query(q_event)))
    n_s = len(list(static_g.query(q_static)))
    n_d = len(list(static_g.query(q_degraded))) if q_degraded else None
    event_answered += n_e > 0
    static_answered += n_s > 0
    print(f"{label:<88}{n_e:>7}{n_s:>8}{('' if n_d is None else n_d):>10}")
print("-" * 113)
print(f"Fully answered: event-mediated {event_answered}/4, static baseline {static_answered}/4.")
print("""
Reading: the static baseline answers Q1 and, in degraded form, can still list
a condition value (Q2) and two indistinguishable date literals (Q3) -- but the
assessment's time-span, the per-claim source, the confidence, and the
claim-to-agent attribution are unrepresentable without reintroducing the
event/assertion structure under ablation. The two conflicting dates survive
as bare literals that cannot be told apart, weighed, or traced.""")
