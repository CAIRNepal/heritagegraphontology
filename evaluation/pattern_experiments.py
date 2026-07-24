#!/usr/bin/env python3
"""Design-pattern baseline & ablation experiments for HeritageGraph.

Consolidates six standalone modelling-comparison experiments behind one CLI.
Each holds the FACT SET constant and varies only the representation, showing
that the HeritageGraph pattern recovers what a charitable baseline loses.
Together they back the pattern-justification claims of the evaluation section.

Subcommands (default: all):
  ablation       event-mediated representation vs. static property attachment
  tenure         KumariTenure period vs. the plain-CRM actor-role idiom
  sameas         reified SyncreticRelationship vs. owl:sameAs identity collapse
  custodianship  institutional depth: custody transfer, hereditary roles, endowment
  supersession   belief supersession chain + structured Proposition content
  multicalendar  resolving a tithi-scheduled ritual across BS / NS / Gregorian

Each SHACL check uses the same pipeline-gate configuration (ont_graph mixed in,
inference="none", owl:NamedIndividual declarations stripped from the in-memory
ontology copy only).

Run:  python3 evaluation/pattern_experiments.py [ablation|tenure|sameas|
                                                  custodianship|supersession|
                                                  multicalendar|all]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rdflib import Graph, OWL, RDF

ROOT = Path(__file__).resolve().parents[1]


def _ont_for_shacl() -> Graph:
    """Released ontology with owl:NamedIndividual declarations stripped from the
    in-memory copy only (the pipeline-gate SHACL configuration)."""
    ont = Graph()
    ont.parse(ROOT / "ontology" / "HeritageGraph.ttl", format="turtle")
    for s in list(ont.subjects(RDF.type, OWL.NamedIndividual)):
        ont.remove((s, RDF.type, OWL.NamedIndividual))
    return ont


def _shapes() -> Graph:
    g = Graph()
    g.parse(ROOT / "ontology" / "HeritageGraph.shacl.ttl", format="turtle")
    return g


# ===========================================================================
# ablation: event-mediated representation vs. static property attachment.
# ===========================================================================
def run_ablation() -> int:
    """Ablation: event-mediated representation vs. static property attachment.

    Holds the fact set constant and varies only the representation. The static
    baseline is deliberately charitable: every fact that CAN be attached
    statically IS attached. A degraded variant of each failing static query
    shows what survives flattening, so the baseline is lossy, not a strawman.
    """
    PFX = """PREFIX hg:  <https://w3id.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX crminf: <http://www.ics.forth.gr/isl/CRMinf/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX ex:  <https://w3id.org/heritagegraph/demo/>
PREFIX st:  <https://w3id.org/heritagegraph/demo/static/>
"""

    event_g = Graph()
    event_g.parse(ROOT / "examples/kathmandu-mini-abox.ttl", format="turtle")

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
    return 0


# ===========================================================================
# tenure: KumariTenure period vs. the plain-CRM actor-role idiom.
# ===========================================================================
def run_tenure() -> int:
    """Baseline comparison: KumariTenure period vs. the plain-CRM actor-role
    idiom. The claim under test is that conventional actor-role modelling
    conflates the enduring person with the temporary sacred office. Three paired
    questions plus a SHACL constraint check on 'exactly one deity per office'.
    """
    from pyshacl import validate

    PFX = """PREFIX hg:  <https://w3id.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX ex:  <https://w3id.org/heritagegraph/demo/>
PREFIX ar:  <https://w3id.org/heritagegraph/demo/actorrole/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

    tenure_g = Graph()
    tenure_g.parse(ROOT / "examples/kathmandu-mini-abox.ttl", format="turtle")

    ACTOR_ROLE = """@prefix hg:  <https://w3id.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix ex:  <https://w3id.org/heritagegraph/demo/> .
@prefix ar:  <https://w3id.org/heritagegraph/demo/actorrole/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:KumariPerson a crm:E21_Person ; rdfs:label "Kumari (incumbent)" ;
    crm:P2_has_type ar:KumariRoleType ;
    ar:embodiesDeity ex:Taleju ;
    ar:residesAt ex:KumariGhar ;
    ar:supportedBy ex:KasthamandapGuthi .
ar:KumariRoleType a crm:E55_Type ; rdfs:label "Kumari (role)" .
ex:Taleju a hg:Deity ; rdfs:label "Taleju" .
ex:KumariGhar a hg:ArchitecturalStructure ; rdfs:label "Kumari Ghar" .
ex:KasthamandapGuthi a hg:Guthi ; rdfs:label "Kasthamandap Guthi" .
ex:Sel_2017 a crm:E5_Event ; rdfs:label "Selection event" ;
    crm:P11_had_participant ex:KumariPerson .
ex:Ret_2025 a crm:E5_Event ; rdfs:label "Retirement event" ;
    crm:P11_had_participant ex:KumariPerson .
ex:TS_Tenure2017 a crm:E52_Time-Span ; rdfs:label "2017--2025" .
"""
    role_g = Graph()
    role_g.parse(data=ACTOR_ROLE, format="turtle")

    QUESTIONS = [
        ("Q1 deity embodied, WITH its temporal scope",
         PFX + """SELECT ?deity ?ts WHERE {
           ?tenure a hg:KumariTenure ; hg:embodiedDeity ?deity ;
                   crm:P4_has_time-span ?ts ; hg:hadParticipant ex:KumariPerson . }""",
         PFX + """SELECT ?deity ?ts WHERE {
           ex:KumariPerson ar:embodiesDeity ?deity ; crm:P4_has_time-span ?ts . }""",
         PFX + """SELECT ?deity WHERE { ex:KumariPerson ar:embodiesDeity ?deity . }"""),
        ("Q2 typed events initiating and terminating the office",
         PFX + """SELECT ?sel ?ret WHERE {
           ?sel a hg:KumariSelectionEvent ; hg:initiatedTenure ?tenure .
           ?ret a hg:KumariRetirementEvent ; hg:endedTenureOf ?tenure . }""",
         PFX + """SELECT ?sel ?ret WHERE {
           ?sel a crm:E5_Event ; ar:initiatedOffice ?o .
           ?ret a crm:E5_Event ; ar:terminatedOffice ?o . }""",
         PFX + """SELECT ?ev WHERE { ?ev a crm:E5_Event ;
           crm:P11_had_participant ex:KumariPerson . }"""),
        ("Q3 residence scoped to the office's time-span",
         PFX + """SELECT ?res ?ts WHERE {
           ?tenure a hg:KumariTenure ; hg:residenceStructure ?res ;
                   crm:P4_has_time-span ?ts . }""",
         PFX + """SELECT ?res ?ts WHERE {
           ex:KumariPerson ar:residesAt ?res ; crm:P4_has_time-span ?ts . }""",
         PFX + """SELECT ?res WHERE { ex:KumariPerson ar:residesAt ?res . }"""),
    ]

    print("Paired questions (tenure arm = released demonstrator; actor-role arm ="
          "\ncharitable plain-CRM baseline, same facts)\n")
    for name, q_tenure, q_role, q_degraded in QUESTIONS:
        n_t = len(list(tenure_g.query(q_tenure)))
        n_r = len(list(role_g.query(q_role)))
        n_d = len(list(role_g.query(q_degraded)))
        print(f"{name}")
        print(f"  tenure arm: {n_t} row(s); actor-role arm: {n_r} row(s); "
              f"degraded (scope dropped): {n_d} row(s)")
    assert all(len(list(tenure_g.query(q))) >= 1 for _, q, _, _ in QUESTIONS)

    # C4: constraint enforceability. Inject a second embodied deity into each arm.
    shapes = _shapes()
    ont = _ont_for_shacl()

    TENURE_VIOLATION = """@prefix hg:  <https://w3id.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix ex:  <https://w3id.org/heritagegraph/demo/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:T a hg:KumariTenure ; rdfs:label "tenure" ;
    hg:embodiedDeity ex:D1 , ex:D2 ;
    crm:P11_had_participant ex:P ; crm:P4_has_time-span ex:TS .
ex:D1 a hg:Deity ; rdfs:label "d1" . ex:D2 a hg:Deity ; rdfs:label "d2" .
ex:P a crm:E21_Person ; rdfs:label "p" .
ex:TS a crm:E52_Time-Span ; rdfs:label "ts" .
"""
    ROLE_VIOLATION = ACTOR_ROLE + """
ex:KumariPerson ar:embodiesDeity ex:Vajradevi .
ex:Vajradevi a hg:Deity ; rdfs:label "Vajradevi" .
"""

    tg = Graph(); tg.parse(data=TENURE_VIOLATION, format="turtle")
    c_tenure, _, _ = validate(tg, shacl_graph=shapes, ont_graph=ont,
                              inference="none", abort_on_first=False)
    rg = Graph(); rg.parse(data=ROLE_VIOLATION, format="turtle")
    c_role, _, _ = validate(rg, shacl_graph=shapes, ont_graph=ont,
                            inference="none", abort_on_first=False)
    print("\nC4 'exactly one deity per office' under the published shapes:")
    print(f"  tenure arm, two deities on the tenure node:   "
          f"conforms={c_tenure}  (expected False: violation caught)")
    print(f"  actor-role arm, two deities on the person:    "
          f"conforms={c_role}  (expected True: passes silently -- no node to constrain)")

    if c_tenure or not c_role:
        print("\nFAIL: unexpected constraint behaviour.")
        return 1
    print("\nPASS: the actor-role baseline answers the deity question only with "
          "its temporal scope dropped, cannot express office initiation/"
          "termination, attaches residence timelessly, and offers no bearer for "
          "the one-deity constraint; the tenure node recovers all four.")
    return 0


# ===========================================================================
# sameas: reified SyncreticRelationship vs. owl:sameAs identity collapse.
# ===========================================================================
def run_sameas() -> int:
    """Demonstrate the identity collapse that owl:sameAs causes for syncretism,
    versus the reified SyncreticRelationship which preserves the two identities.
    Both graphs carry the same domain facts, are expanded with OWL-RL closure,
    and answered with a leakage probe, a merge probe, and a provenance probe.
    """
    from owlrl import DeductiveClosure, OWLRL_Semantics

    PFX = """PREFIX hg:  <https://w3id.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX ex:  <https://w3id.org/heritagegraph/demo/>
"""

    BASE = """@prefix hg:  <https://w3id.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:  <https://w3id.org/heritagegraph/demo/> .

ex:Avalokitesvara a hg:Deity ; rdfs:label "Avalokiteshvara" ;
    hg:hasReligiousTradition ex:Buddhist .
ex:Matsyendranath a hg:Deity ; rdfs:label "Matsyendranath" ;
    hg:hasReligiousTradition ex:Hindu .
ex:Buddhist a hg:ReligiousTradition ; rdfs:label "Buddhist" .
ex:Hindu a hg:ReligiousTradition ; rdfs:label "Hindu" .
ex:Src_Slusser a hg:DataSource ; rdfs:label "Slusser, Nepal Mandala (1982)" .
"""

    SAMEAS = "ex:Avalokitesvara owl:sameAs ex:Matsyendranath .\n"

    REIFIED = """ex:Syn a hg:SyncreticRelationship ; rdfs:label "equivalence claim" ;
    crm:P140_assigned_attribute_to ex:Avalokitesvara ;
    crm:P141_assigned ex:Matsyendranath ;
    hg:syncreticType "Equivalence" ;
    prov:wasDerivedFrom ex:Src_Slusser .
"""

    def closed(ttl: str) -> Graph:
        g = Graph()
        g.parse(data=ttl, format="turtle")
        DeductiveClosure(OWLRL_Semantics).expand(g)
        return g

    g_same = closed(BASE + SAMEAS)
    g_reif = closed(BASE + REIFIED)

    Q1 = PFX + "SELECT DISTINCT ?d WHERE { ?d hg:hasReligiousTradition ex:Hindu . }"
    Q2 = PFX + """SELECT ?d (COUNT(DISTINCT ?t) AS ?n) WHERE {
  ?d a hg:Deity ; hg:hasReligiousTradition ?t . } GROUP BY ?d"""
    Q3 = PFX + """SELECT ?type ?source WHERE {
  ?s a hg:SyncreticRelationship ; hg:syncreticType ?type ;
     prov:wasDerivedFrom ?source . }"""

    def short(x):
        return str(x).split("/")[-1]

    for label, g in (("owl:sameAs", g_same), ("SyncreticRelationship", g_reif)):
        print(f"== {label} (post OWL-RL closure: {len(g)} triples) ==")
        hindu = sorted(short(r.d) for r in g.query(Q1))
        print(f"  Q1 Hindu-tradition deities: {hindu}")
        for r in g.query(Q2):
            print(f"  Q2 {short(r.d)}: {r.n} tradition(s)")
        prov_rows = list(g.query(Q3))
        print(f"  Q3 equivalence type+source: "
              f"{[(str(r.type), short(r.source)) for r in prov_rows] or 'UNANSWERABLE (0 rows)'}")
        print()

    print("""Reading: under owl:sameAs the closure merges the individuals, so the
Buddhist deity leaks into the Hindu tradition (and vice versa), every deity
carries both traditions, and the equivalence itself -- being a logical
identity, not a node -- can carry neither type nor source. The reified
pattern keeps each deity in exactly one tradition and makes the claim's
type and provenance queryable.""")
    return 0


# ===========================================================================
# custodianship: institutional depth (custody transfer, roles, endowment).
# ===========================================================================
def run_custodianship() -> int:
    """Institutional-depth scenario exercising custody transfer through
    crm:E10_Transfer_of_Custody, hereditary caste roles, and endowment support.
    The scenario is released and shape-conformant, separate from the demonstrator
    (whose published triple counts stay untouched).
    """
    from pyshacl import validate

    PFX = """PREFIX hg:  <https://w3id.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX ex:  <https://w3id.org/heritagegraph/demo/>
"""

    SCENARIO = """@prefix hg:  <https://w3id.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix aat: <http://vocab.getty.edu/aat/> .
@prefix ex:  <https://w3id.org/heritagegraph/demo/> .

# Structure under custody.
ex:Kasthamandap a hg:Temple ; rdfs:label "Kasthamandap" ;
    hg:hasArchitecturalStyle aat:300004829 .

# Institutions: a private temple guthi and the state corporation.
ex:PrivateGuthi a hg:Guthi ; rdfs:label "Kasthamandap private Guthi" ;
    hg:guthiType "TempleGuthi" .
ex:GuthiSansthan a hg:Guthi ; rdfs:label "Guthi Sansthan (state corporation)" ;
    hg:guthiType "RajGuthi" ;
    crm:P50i_is_current_keeper_of ex:Kasthamandap ;
    hg:performsRitual ex:IndraJatra .

# Custody transfer following the Guthi Corporation Act (2021 B.S. / 1964 CE).
ex:TS_1964 a crm:E52_Time-Span ; rdfs:label "1964 CE (2021 B.S.)" .
ex:Transfer_1964 a crm:E10_Transfer_of_Custody ;
    rdfs:label "Nationalisation of the Kasthamandap guthi endowment" ;
    crm:P30_transferred_custody_of ex:Kasthamandap ;
    crm:P28_custody_surrendered_by ex:PrivateGuthi ;
    crm:P29_custody_received_by ex:GuthiSansthan ;
    hg:transferredToGuthi ex:GuthiSansthan ;
    crm:P4_has_time-span ex:TS_1964 .

# Ritual sustained by the endowment, performed by a hereditary caste group.
ex:IndraJatra a hg:RitualEvent ; rdfs:label "Indra Jatra" ;
    hg:performedByGroup ex:Manandhars .
ex:Manandhars a hg:CasteGroup ; rdfs:label "Manandhar community" ;
    hg:traditionalRole "hereditary chariot pullers and oil pressers" ;
    crm:P107_has_current_or_former_member ex:MemberPerson .
ex:MemberPerson a crm:E21_Person ; rdfs:label "Guthiyar (member)" .
"""

    QUERIES = {
        "Q1 custody transfer (object, from, to, time-span)":
            PFX + """SELECT ?obj ?from ?to ?ts WHERE {
              ?t a crm:E10_Transfer_of_Custody ;
                 crm:P30_transferred_custody_of ?obj ;
                 crm:P28_custody_surrendered_by ?from ;
                 crm:P29_custody_received_by ?to ;
                 crm:P4_has_time-span ?ts . }""",
        "Q2 current keeper after the transfer":
            PFX + """SELECT ?keeper WHERE {
              ?keeper crm:P50i_is_current_keeper_of ex:Kasthamandap . }""",
        "Q3 hereditary roles (group, role, ritual, member)":
            PFX + """SELECT ?group ?role ?ritual ?member WHERE {
              ?ritual hg:performedByGroup ?group .
              ?group hg:traditionalRole ?role ;
                     crm:P107_has_current_or_former_member ?member . }""",
        "Q4 endowment: keeper that also sustains the ritual cycle":
            PFX + """SELECT ?guthi ?asset ?ritual WHERE {
              ?guthi a hg:Guthi ;
                     crm:P50i_is_current_keeper_of ?asset ;
                     hg:performsRitual ?ritual . }""",
    }

    g = Graph()
    g.parse(data=SCENARIO, format="turtle")
    print(f"Scenario: {len(g)} triples\n")
    for name, q in QUERIES.items():
        rows = list(g.query(q))
        print(f"[{len(rows)} row(s)] {name}")
        for r in rows:
            print("   -> " + " | ".join(
                str(x).replace("https://w3id.org/heritagegraph/demo/", "") for x in r))
    print()

    shapes = _shapes()
    ont = _ont_for_shacl()
    conforms, _, report = validate(g, shacl_graph=shapes, ont_graph=ont,
                                   inference="none", abort_on_first=False)
    print(f"SHACL conformance of the scenario: conforms={conforms}")
    if not conforms:
        print(report[:2000])
    return 0


# ===========================================================================
# supersession: belief supersession chain + structured Proposition content.
# ===========================================================================
def run_supersession() -> int:
    """Supersession chain (prov:wasRevisionOf) + structured-content Proposition
    (crminf:J4_that). Exercises version supersession -- 'the current assertion
    is the one with no incoming revision' -- and machine-readable claim content.
    Released, shape-conformant scenario, separate from the demonstrator.
    """
    from pyshacl import validate

    PFX = """PREFIX hg:     <https://w3id.org/heritagegraph/>
PREFIX crm:    <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX crminf: <http://www.ics.forth.gr/isl/CRMinf/>
PREFIX prov:   <http://www.w3.org/ns/prov#>
PREFIX ex:     <https://w3id.org/heritagegraph/demo/>
PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
"""

    SCENARIO = """@prefix hg:     <https://w3id.org/heritagegraph/> .
@prefix crm:    <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix crminf: <http://www.ics.forth.gr/isl/CRMinf/> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:     <https://w3id.org/heritagegraph/demo/> .

ex:Kasthamandap a hg:Temple ;
    rdfs:label "Kasthamandap" ;
    hg:hasArchitecturalStyle <http://vocab.getty.edu/aat/300004829> .

ex:Src_Early a hg:DataSource ; rdfs:label "Early gazetteer attribution" .
ex:Src_Slusser a hg:DataSource ; rdfs:label "Slusser, Nepal Mandala (1982)" .
ex:Src_Excavation a hg:DataSource ;
    rdfs:label "Post-earthquake excavation report (2019)" .

ex:Historian a crm:E39_Actor ; rdfs:label "Attributing historian" .
ex:Slusser a crm:E39_Actor ; rdfs:label "M. S. Slusser" .
ex:ExcavationTeam a crm:E39_Actor ; rdfs:label "DoA excavation team" .

ex:Assert_Date_v1 a crminf:I2_Belief ;
    rdfs:label "Kasthamandap build date, v1" ;
    hg:assertsAbout ex:Kasthamandap ;
    prov:value "7th century CE" ;
    prov:wasDerivedFrom ex:Src_Early ;
    prov:wasAttributedTo ex:Historian ;
    prov:generatedAtTime "1966-01-01T00:00:00"^^xsd:dateTime ;
    hg:confidenceScore "0.4"^^xsd:float .

ex:Assert_Date_v2 a crminf:I2_Belief ;
    rdfs:label "Kasthamandap build date, v2" ;
    hg:assertsAbout ex:Kasthamandap ;
    prov:value "12th century CE" ;
    prov:wasDerivedFrom ex:Src_Slusser ;
    prov:wasAttributedTo ex:Slusser ;
    prov:generatedAtTime "1982-01-01T00:00:00"^^xsd:dateTime ;
    prov:wasRevisionOf ex:Assert_Date_v1 ;
    hg:confidenceScore "0.6"^^xsd:float .

ex:Assert_Date_v3 a crminf:I2_Belief ;
    rdfs:label "Kasthamandap build date, v3" ;
    hg:assertsAbout ex:Kasthamandap ;
    prov:value "not later than 1143 CE" ;
    prov:wasDerivedFrom ex:Src_Excavation ;
    prov:wasAttributedTo ex:ExcavationTeam ;
    prov:generatedAtTime "2019-01-01T00:00:00"^^xsd:dateTime ;
    prov:wasRevisionOf ex:Assert_Date_v2 ;
    crminf:J4_that ex:Prop_Date ;
    hg:confidenceScore "0.9"^^xsd:float .

ex:Prop_Date a hg:Proposition ;
    rdfs:label "Kasthamandap completed by 1143 CE" ;
    hg:propositionSubject ex:Kasthamandap ;
    hg:propositionPredicate "http://www.cidoc-crm.org/cidoc-crm/P82b_end_of_the_end"^^xsd:anyURI ;
    hg:propositionLiteralValue "1143" .
"""

    Q1_CHAIN = PFX + """SELECT ?belief ?value ?source ?conf WHERE {
  ex:Assert_Date_v3 prov:wasRevisionOf* ?belief .
  ?belief prov:value ?value ; prov:wasDerivedFrom ?src ; hg:confidenceScore ?conf .
  ?src rdfs:label ?source .
} ORDER BY ?belief"""

    Q2_CURRENT = PFX + """SELECT ?belief ?value ?status WHERE {
  ?belief a crminf:I2_Belief ; hg:assertsAbout ex:Kasthamandap ; prov:value ?value .
  BIND(IF(EXISTS { ?later prov:wasRevisionOf ?belief }, "superseded", "current") AS ?status)
} ORDER BY ?belief"""

    Q3_PROPOSITION = PFX + """SELECT ?subj ?pred ?obj ?conf WHERE {
  ?belief a crminf:I2_Belief ; crminf:J4_that ?p ; hg:confidenceScore ?conf .
  FILTER NOT EXISTS { ?later prov:wasRevisionOf ?belief }
  ?p hg:propositionSubject ?subj ;
     hg:propositionPredicate ?pred ;
     hg:propositionLiteralValue ?obj .
}"""

    def short(x) -> str:
        return (str(x)
                .replace("https://w3id.org/heritagegraph/demo/", "ex:")
                .replace("https://w3id.org/heritagegraph/", "hg:")
                .replace("http://www.cidoc-crm.org/cidoc-crm/", "crm:"))

    g = Graph()
    g.parse(ROOT / "ontology" / "HeritageGraph.ttl", format="turtle")
    g.parse(data=SCENARIO, format="turtle")

    print("Q1: supersession chain from the head (wasRevisionOf*)")
    rows = list(g.query(Q1_CHAIN))
    for r in rows:
        print("  " + " | ".join(short(x) for x in r))
    assert len(rows) == 3, "expected the full 3-belief chain"

    print("\nQ2: current vs. superseded verdict per belief")
    rows = list(g.query(Q2_CURRENT))
    status = {}
    for r in rows:
        print("  " + " | ".join(short(x) for x in r))
        status[short(r[0])] = str(r[2])
    assert status == {"ex:Assert_Date_v1": "superseded",
                      "ex:Assert_Date_v2": "superseded",
                      "ex:Assert_Date_v3": "current"}, status

    print("\nQ3: structured content (Proposition) of the current belief")
    rows = list(g.query(Q3_PROPOSITION))
    for r in rows:
        print("  " + " | ".join(short(x) for x in r))
    assert len(rows) == 1 and short(rows[0][0]) == "ex:Kasthamandap"

    shapes = _shapes()
    ont = _ont_for_shacl()
    data = Graph()
    data.parse(data=SCENARIO, format="turtle")
    conforms, _, txt = validate(data, shacl_graph=shapes, ont_graph=ont,
                                inference="none", abort_on_first=False)
    print(f"\nSHACL conformance of the scenario: conforms={conforms}")
    if not conforms:
        print(txt[:2000])
        return 1

    print("\nPASS: the supersession chain is traversable, the current belief is "
          "derivable from the absence of an incoming revision, and the current "
          "claim's content is retrievable as a structured Proposition rather "
          "than prose.")
    return 0


# ===========================================================================
# multicalendar: resolve a tithi-scheduled ritual across BS / NS / Gregorian.
# ===========================================================================
def run_multicalendar() -> int:
    """Multi-calendar experiment: resolve a tithi-scheduled ritual to Gregorian
    dates across Bikram Sambat, Nepal Sambat, and Gregorian records. Exercises
    yearOffsetFromGregorian / epochDateGregorian / isPrimaryForTradition.
    Released, shape-conformant scenario, separate from the demonstrator.
    """
    from pyshacl import validate

    PFX = """PREFIX hg:   <https://w3id.org/heritagegraph/>
PREFIX crm:  <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX ex:   <https://w3id.org/heritagegraph/demo/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

    SCENARIO = """@prefix hg:   <https://w3id.org/heritagegraph/> .
@prefix crm:  <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <https://w3id.org/heritagegraph/demo/> .

# --- Religious traditions the calendars serve ---------------------------
ex:HinduTradition a hg:ReligiousTradition ; rdfs:label "Hindu tradition" .
ex:NewarBuddhistTradition a hg:ReligiousTradition ;
    rdfs:label "Newar Buddhist tradition" .

# --- The three calendar systems -----------------------------------------
# Offset semantics (per schema): CE = calendar year - yearOffsetFromGregorian.
ex:BikramSambat a hg:CalendarSystem ; rdfs:label "Bikram Sambat" ;
    hg:epochDateGregorian "-0056-04-14" ;      # 57 BCE, mid-April new year
    hg:yearOffsetFromGregorian 57 ;
    hg:isPrimaryForTradition ex:HinduTradition ;
    crm:P3_has_note "Lunisolar civil calendar of Nepal; new year in mid-April (Baisakh 1)." .
ex:NepalSambat a hg:CalendarSystem ; rdfs:label "Nepal Sambat" ;
    hg:epochDateGregorian "0879-10-20" ;       # epoch 20 Oct 879 CE
    hg:yearOffsetFromGregorian -879 ;
    hg:isPrimaryForTradition ex:NewarBuddhistTradition ;
    crm:P3_has_note "Lunisolar Newar calendar; new year at Mha Puja (Oct/Nov)." .
ex:GregorianCalendar a hg:CalendarSystem ; rdfs:label "Gregorian calendar" ;
    hg:epochDateGregorian "0001-01-01" ;
    hg:yearOffsetFromGregorian 0 .

# --- The tithi-scheduled ritual and one documented occurrence -----------
ex:IndraJatra a hg:Festival ; rdfs:label "Indra Jatra" ;
    hg:lunarDateTithi "Bhadra Shukla Dwadashi" ;
    hg:recurrencePattern "annual (lunar-tithi)" .

ex:IndraJatra_2015 a hg:RitualEvent ;
    rdfs:label "Indra Jatra, 2015 occurrence" ;
    crm:P9i_forms_part_of ex:IndraJatra ;
    crm:P4_has_time-span ex:TS_IJ_Gregorian .

# Three source records of the same occurrence, each in its own calendar.
ex:TS_IJ_Gregorian a crm:E52_Time-Span ;
    rdfs:label "Indra Jatra start, Gregorian record" ;
    crm:P82a_begin_of_the_begin "2015-09-25"^^xsd:date ;
    hg:calendarSystem ex:GregorianCalendar ;
    hg:datePrecision "Exact" .
ex:TS_IJ_BikramSambat a crm:E52_Time-Span ;
    rdfs:label "Indra Jatra start, Bikram Sambat record (B.S. 2072)" ;
    crm:P82a_begin_of_the_begin "2072-01-01"^^xsd:date ;
    hg:calendarSystem ex:BikramSambat ;
    hg:datePrecision "Year" ;
    crm:P3_has_note "Year-precision record; B.S. 2072 spans 2015-04-14 to 2016-04-12 CE." .
ex:TS_IJ_NepalSambat a crm:E52_Time-Span ;
    rdfs:label "Indra Jatra start, Nepal Sambat record (N.S. 1135)" ;
    crm:P82a_begin_of_the_begin "1135-01-01"^^xsd:date ;
    hg:calendarSystem ex:NepalSambat ;
    hg:datePrecision "Year" ;
    crm:P3_has_note "Year-precision record; N.S. 1135 spans Oct 2014 to Nov 2015 CE." .

# The two calendar-specific records document the dated occurrence.
ex:IndraJatra_2015 crm:P3_has_note
    "Also recorded as B.S. 2072 (TS_IJ_BikramSambat) and N.S. 1135 (TS_IJ_NepalSambat)." .
"""

    QUERIES = {
        "Q1 per-record resolution: source year -> Gregorian year interval":
            PFX + """SELECT ?record ?calendar ?srcYear ?ceLow ?ceHigh WHERE {
              ?record a crm:E52_Time-Span ;
                      crm:P82a_begin_of_the_begin ?d ;
                      hg:calendarSystem ?cal .
              ?cal rdfs:label ?calendar ;
                   hg:yearOffsetFromGregorian ?off ;
                   hg:epochDateGregorian ?epoch .
              BIND(YEAR(?d) AS ?srcYear)
              BIND(?srcYear - ?off AS ?ceLow)
              BIND(IF(SUBSTR(?epoch, 6) = "01-01", ?ceLow, ?ceLow + 1) AS ?ceHigh)
            } ORDER BY ?ceLow""",
        "Q2 tithi ritual resolved: unique Gregorian year consistent with all records":
            PFX + """SELECT ?ritual ?tithi ?ceYear ?gregorianDate WHERE {
              ?occ crm:P9i_forms_part_of ?series ;
                   crm:P4_has_time-span ?tsg .
              ?series rdfs:label ?ritual ; hg:lunarDateTithi ?tithi .
              ?tsg crm:P82a_begin_of_the_begin ?gregorianDate ;
                   hg:calendarSystem [ hg:yearOffsetFromGregorian 0 ] .
              BIND(YEAR(?gregorianDate) AS ?ceYear)
              # Every calendared record of this occurrence must admit ?ceYear.
              FILTER NOT EXISTS {
                ?other a crm:E52_Time-Span ;
                       crm:P82a_begin_of_the_begin ?od ;
                       hg:calendarSystem ?ocal .
                ?ocal hg:yearOffsetFromGregorian ?ooff ;
                      hg:epochDateGregorian ?oepoch .
                BIND(YEAR(?od) - ?ooff AS ?lo)
                BIND(IF(SUBSTR(?oepoch, 6) = "01-01", ?lo, ?lo + 1) AS ?hi)
                FILTER(?ceYear < ?lo || ?ceYear > ?hi)
              }
            }""",
        "Q3 calendar catalogue: epoch, offset, primary tradition":
            PFX + """SELECT ?calendar ?epoch ?offset ?tradition WHERE {
              ?cal a hg:CalendarSystem ; rdfs:label ?calendar ;
                   hg:epochDateGregorian ?epoch ;
                   hg:yearOffsetFromGregorian ?offset .
              OPTIONAL { ?cal hg:isPrimaryForTradition [ rdfs:label ?tradition ] }
            } ORDER BY ?offset""",
    }

    g = Graph()
    g.parse(data=SCENARIO, format="turtle")
    print(f"Scenario: {len(g)} triples\n")
    for name, q in QUERIES.items():
        rows = list(g.query(q))
        print(f"[{len(rows)} row(s)] {name}")
        for r in rows:
            print("   -> " + " | ".join(
                str(x).replace("https://w3id.org/heritagegraph/demo/", "")
                for x in r))
    print()

    shapes = _shapes()
    ont = _ont_for_shacl()
    conforms, _, report = validate(g, shacl_graph=shapes, ont_graph=ont,
                                   inference="none", abort_on_first=False)
    print(f"SHACL conformance of the scenario: conforms={conforms}")
    if not conforms:
        print(report[:2000])
    return 0


EXPERIMENTS = {
    "ablation": run_ablation,
    "tenure": run_tenure,
    "sameas": run_sameas,
    "custodianship": run_custodianship,
    "supersession": run_supersession,
    "multicalendar": run_multicalendar,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("experiment", nargs="?", default="all",
                        choices=list(EXPERIMENTS) + ["all"],
                        help="which experiment to run (default: all)")
    args = parser.parse_args()

    if args.experiment != "all":
        return EXPERIMENTS[args.experiment]()

    failures = []
    for name, fn in EXPERIMENTS.items():
        print(f"\n{'=' * 78}\n== {name}\n{'=' * 78}")
        try:
            if fn() not in (0, None):
                failures.append(name)
        except Exception as exc:  # keep going so every experiment is reported
            failures.append(name)
            print(f"[{name}] FAILED: {exc}")
    print(f"\n{'=' * 78}")
    if failures:
        print(f"FAILED experiments: {', '.join(failures)}")
        return 1
    print("All pattern experiments passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
