#!/usr/bin/env python3
"""Design-pattern baseline & ablation experiments for HeritageGraph.

Consolidates the modelling-comparison experiments behind one CLI. Each holds
the FACT SET constant and varies only the representation, and reports where the
representations differ (in some, e.g. tenure, a strong baseline expresses the
same facts and the difference lies elsewhere: shipped constraints, typed
events, query size). Together they back the pattern claims of the evaluation.

Subcommands (default: all):
  ablation       event-mediated representation vs. static property attachment
  tenure         KumariTenure vs. the CIDOC-CRM role idiom and Wikidata P39 qualifiers
  sameas         reified SyncreticRelationship vs. owl:sameAs identity collapse
  custodianship  custody periods, endowment and hereditary office (exact answers)
  supersession   belief supersession chain + structured Proposition content
  multicalendar  resolving a tithi-scheduled ritual across BS / NS / Gregorian
  reuse          the Tenure pattern applied outside Nepal (RQ3)

Each SHACL check uses the same pipeline-gate configuration (ont_graph mixed in,
inference="none", owl:NamedIndividual declarations stripped from the in-memory
ontology copy only).

Run:  python3 evaluation/pattern_experiments.py [ablation|tenure|sameas|
                                                  custodianship|supersession|
                                                  multicalendar|reuse|all]
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
    PFX = """PREFIX hg:  <https://cair-nepal.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX crminf: <http://www.cidoc-crm.org/extensions/crminf/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX ex:  <https://cair-nepal.org/heritagegraph/example/>
PREFIX st:  <https://cair-nepal.org/heritagegraph/example/static/>
"""

    event_g = Graph()
    event_g.parse(ROOT / "examples/kathmandu-mini-abox.ttl", format="turtle")

    static_g = Graph()
    static_g.parse(data="""
@prefix hg:  <https://cair-nepal.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix ex:  <https://cair-nepal.org/heritagegraph/example/> .
@prefix st:  <https://cair-nepal.org/heritagegraph/example/static/> .
@prefix aat: <http://vocab.getty.edu/aat/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Kasthamandap a hg:Temple ;
    rdfs:label "Kasthamandap" ;
    hg:hasArchitecturalStyle <https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Pagoda> ;
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
    """The Kumari tenure against the two strongest established idioms, on the
    same facts (holder, office, deity, residence, period, opening and closing
    events, supporting institution):
      A. HeritageGraph: hg:KumariTenure (the released demonstrator).
      B. CIDOC-CRM role idiom: an E7 activity carried out by the person in the
         role of the Kumari office (crm:P14 with P14.1 "in the role of", in the
         official property-class encoding crm:PC14_carried_out_by /
         P01_has_domain / P02_has_range, published in CIDOC's PC extension),
         with P4 time-span, P7 place, P15 "was influenced by" for the deity (CRM
         has no embodiment property) and opening/closing E5 events linked by
         P182.
      C. Wikidata qualifier model: position held (P39) on a statement node
         with start time (P580), end time (P582), end cause (P1534), location
         (P276) and "represents" (P1268) for the deity.
    For each question the report gives whether each arm's answer matches the
    facts (yes, partial or NO) and the number of triple patterns its query
    needs, counted from the parsed SPARQL; the experiment states, rather
    than assumes, where the arms differ. It fails only if the HeritageGraph arm
    misses an answer or the constraint check behaves unexpectedly."""
    from pyshacl import validate

    PFX = """PREFIX hg:  <https://cair-nepal.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX ex:  <https://cair-nepal.org/heritagegraph/example/>
PREFIX b:   <https://cair-nepal.org/heritagegraph/example/baseline/>
PREFIX p:   <http://www.wikidata.org/prop/>
PREFIX ps:  <http://www.wikidata.org/prop/statement/>
PREFIX pq:  <http://www.wikidata.org/prop/qualifier/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""
    hg_g = Graph()
    hg_g.parse(ROOT / "examples/kathmandu-mini-abox.ttl", format="turtle")
    hg_g.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")

    CRM_ROLE = """@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix ex:  <https://cair-nepal.org/heritagegraph/example/> .
@prefix b:   <https://cair-nepal.org/heritagegraph/example/baseline/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
b:KumariService a crm:E7_Activity ;
    crm:P01i_is_domain_of b:pc1 , b:pc2 ;
    crm:P4_has_time-span b:ts ;
    crm:P7_took_place_at ex:KumariGhar ;
    crm:P15_was_influenced_by ex:Taleju .
b:pc1 a crm:PC14_carried_out_by ; crm:P02_has_range ex:KumariPerson ;
    crm:P14.1_in_the_role_of b:KumariOffice .
b:pc2 a crm:PC14_carried_out_by ; crm:P02_has_range ex:GuthiSansthan ;
    crm:P14.1_in_the_role_of b:SupportingInstitution .
b:KumariOffice a crm:E55_Type . b:SupportingInstitution a crm:E55_Type .
b:ts a crm:E52_Time-Span ;
    crm:P82a_begin_of_the_begin "2017-09-28T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2025-09-30T00:00:00"^^xsd:dateTime .
b:Enthronement a crm:E5_Event ; crm:P2_has_type b:KumariEnthronement ;
    crm:P182_ends_before_or_with_the_start_of b:KumariService .
b:KumariService crm:P182_ends_before_or_with_the_start_of b:Retirement .
b:Retirement a crm:E5_Event ; crm:P2_has_type b:KumariRetirement .
b:KumariEnthronement a crm:E55_Type . b:KumariRetirement a crm:E55_Type .
"""
    WIKIDATA = """@prefix p:  <http://www.wikidata.org/prop/> .
@prefix ps: <http://www.wikidata.org/prop/statement/> .
@prefix pq: <http://www.wikidata.org/prop/qualifier/> .
@prefix ex: <https://cair-nepal.org/heritagegraph/example/> .
@prefix b:  <https://cair-nepal.org/heritagegraph/example/baseline/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:KumariPerson p:P39 b:stmt .
b:stmt ps:P39 b:KumariOffice ;
    pq:P580 "2017-09-28T00:00:00"^^xsd:dateTime ;
    pq:P582 "2025-09-30T00:00:00"^^xsd:dateTime ;
    pq:P1534 b:KumariRetirement ;
    pq:P276 ex:KumariGhar ;
    pq:P1268 ex:Taleju .
"""
    crm_g = Graph().parse(data=CRM_ROLE, format="turtle")
    wd_g = Graph().parse(data=WIKIDATA, format="turtle")

    Q = [
        ("Q1 deity, with the period it applies to",
         """SELECT ?deity ?from WHERE { ?t a hg:KumariTenure ; hg:tenureHolder ex:KumariPerson ;
              hg:embodiedDeity ?deity ; crm:P4_has_time-span/crm:P82a_begin_of_the_begin ?from . }""",
         """SELECT ?deity ?from WHERE { ?pc crm:P02_has_range ex:KumariPerson ;
              crm:P14.1_in_the_role_of b:KumariOffice . ?a crm:P01i_is_domain_of ?pc ;
              crm:P15_was_influenced_by ?deity ; crm:P4_has_time-span/crm:P82a_begin_of_the_begin ?from . }""",
         """SELECT ?deity ?from WHERE { ex:KumariPerson p:P39 ?s . ?s ps:P39 b:KumariOffice ;
              pq:P1268 ?deity ; pq:P580 ?from . }"""),
        ("Q2 typed events that began and ended the office",
         """SELECT ?open ?close WHERE { ?t a hg:KumariTenure ; hg:tenureHolder ex:KumariPerson ;
              hg:enthronedThrough ?open . ?open a hg:KumariEnthronementEvent .
              ?close a hg:KumariRetirementEvent ; hg:endedTenureOf ?t . }""",
         """SELECT ?open ?close WHERE { ?o crm:P182_ends_before_or_with_the_start_of ?a ; crm:P2_has_type ?open .
              ?a crm:P182_ends_before_or_with_the_start_of ?c ; crm:P01i_is_domain_of ?pc .
              ?c crm:P2_has_type ?close . ?pc crm:P14.1_in_the_role_of b:KumariOffice . }""",
         """SELECT ?close WHERE { ex:KumariPerson p:P39 ?s . ?s pq:P1534 ?close . }"""),
        ("Q3 residence during the period",
         """SELECT ?res ?from WHERE { ?t a hg:KumariTenure ; hg:tenureHolder ex:KumariPerson ;
              hg:residenceStructure ?res ; crm:P4_has_time-span/crm:P82a_begin_of_the_begin ?from . }""",
         """SELECT ?res ?from WHERE { ?a crm:P01i_is_domain_of ?pc ; crm:P7_took_place_at ?res ;
              crm:P4_has_time-span/crm:P82a_begin_of_the_begin ?from .
              ?pc crm:P02_has_range ex:KumariPerson ; crm:P14.1_in_the_role_of b:KumariOffice . }""",
         """SELECT ?res ?from WHERE { ex:KumariPerson p:P39 ?s . ?s pq:P276 ?res ; pq:P580 ?from . }"""),
        ("Q4 who held the office on 1 January 2020",
         """SELECT ?holder WHERE { ?t a hg:KumariTenure ; hg:tenureHolder ?holder ;
              crm:P4_has_time-span ?ts . ?ts crm:P82a_begin_of_the_begin ?b ; crm:P82b_end_of_the_end ?e .
              FILTER(?b <= "2020-01-01T00:00:00"^^xsd:dateTime && "2020-01-01T00:00:00"^^xsd:dateTime <= ?e) }""",
         """SELECT ?holder WHERE { ?a crm:P01i_is_domain_of ?pc ; crm:P4_has_time-span ?ts .
              ?pc crm:P02_has_range ?holder ; crm:P14.1_in_the_role_of b:KumariOffice .
              ?ts crm:P82a_begin_of_the_begin ?b ; crm:P82b_end_of_the_end ?e .
              FILTER(?b <= "2020-01-01T00:00:00"^^xsd:dateTime && "2020-01-01T00:00:00"^^xsd:dateTime <= ?e) }""",
         """SELECT ?holder WHERE { ?holder p:P39 ?s . ?s ps:P39 b:KumariOffice ; pq:P580 ?b ; pq:P582 ?e .
              FILTER(?b <= "2020-01-01T00:00:00"^^xsd:dateTime && "2020-01-01T00:00:00"^^xsd:dateTime <= ?e) }"""),
        ("Q5 institution supporting the office holder",
         """SELECT ?inst WHERE { ?t a hg:KumariTenure ; hg:tenureHolder ex:KumariPerson ;
              hg:supportedByInstitution ?inst . }""",
         """SELECT ?inst WHERE { ?a crm:P01i_is_domain_of ?pc , ?pk .
              ?pk crm:P02_has_range ex:KumariPerson ; crm:P14.1_in_the_role_of b:KumariOffice .
              ?pc crm:P02_has_range ?inst ; crm:P14.1_in_the_role_of b:SupportingInstitution . }""",
         None),
    ]

    from rdflib.plugins.sparql import prepareQuery
    from rdflib.plugins.sparql.algebra import traverse
    from rdflib.paths import SequencePath

    def n_patterns(q: str) -> int:
        """Triple patterns in the parsed algebra; each hop of a sequence path counts."""
        count = 0
        def visit(node):
            nonlocal count
            if getattr(node, "name", None) == "BGP":
                for t in node.triples:
                    p = t[1]
                    count += len(p.args) if isinstance(p, SequencePath) else 1
        traverse(prepareQuery(PFX + q).algebra, visitPre=visit)
        return count

    # the facts every arm encodes; an arm answers a question when its values match
    import re as _re

    def norm(x):
        if x is None:
            return None
        v = str(x).rsplit("/", 1)[-1]
        return v[:10] if _re.match(r"^\d{4}-\d{2}-\d{2}T", v) else v   # a date-time: its day

    def vals(g, q):
        return {tuple(norm(x) for x in r) for r in g.query(PFX + q)}
    WANT = {"Q1": {("Taleju", "2017-09-28")}, "Q3": {("KumariGhar", "2017-09-28")},
            "Q4": {("KumariPerson",)}, "Q5": {("GuthiSansthan",)}}
    # Q2: the beginning and ending events, as each arm identifies them
    WANT_Q2 = [{("Enth_2017", "Ret_2025")}, {("KumariEnthronement", "KumariRetirement")},
               {("KumariRetirement",)}]           # Wikidata: the end cause only (no start cause)

    print(f"{'question':<46}{'HG':>10}{'CRM role':>12}{'Wikidata':>12}   (answered? / triple patterns)")
    ok = True
    for name, qh, qc, qw in Q:
        key = name[:2]
        res = []
        for arm, (g_, q_) in enumerate(((hg_g, qh), (crm_g, qc), (wd_g, qw))):
            if q_ is None:
                res.append("n/a")
                continue
            v = vals(g_, q_)
            if key == "Q2":
                want = WANT_Q2[arm]
                one_event = len(next(iter(want))) < 2          # this arm can give one of the two only
                verdict = ("partial" if one_event else "yes") if v == want else "NO"
                res.append(f"{verdict}/{n_patterns(q_)}")
                continue
            good = v == WANT[key]
            res.append(f"{'yes' if good else 'NO'}/{n_patterns(q_)}")
        ok &= res[0].startswith("yes")
        print(f"{name:<46}{res[0]:>10}{res[1]:>12}{res[2]:>12}")
    print("""
Reading: all three idioms state the facts, with these differences.
- Q1: CRM has no embodiment property (P15 'was influenced by' is weaker);
  Wikidata's P1268 'represents' is closer; HeritageGraph states embodiment.
- Q2: CRM types its opening and closing events with P2_has_type and E55s it must
  mint; Wikidata records the end cause (P1534) but has no start-cause qualifier;
  HeritageGraph has typed selection and retirement events.
- Pattern counts (from the parsed queries): the CRM idiom needs the
  property-of-property reification for each role (PC14 / P01 / P02 / P14.1);
  Wikidata has no qualifier for a supporting institution (Q5).
- Constraints: below.""")

    # constraint check: 'exactly one embodied deity per tenure' under the published shapes
    shapes, ont = _shapes(), _ont_for_shacl()
    bad = Graph().parse(data="""@prefix hg: <https://cair-nepal.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix ex: <https://cair-nepal.org/heritagegraph/example/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:T a hg:KumariTenure ; rdfs:label "tenure" ; hg:embodiedDeity ex:D1 , ex:D2 ;
    hg:tenureHolder ex:P ; hg:residenceStructure ex:H ; crm:P4_has_time-span ex:TS .
ex:D1 a hg:Deity ; rdfs:label "d1" . ex:D2 a hg:Deity ; rdfs:label "d2" .
ex:P a crm:E21_Person ; rdfs:label "p" . ex:H a hg:KumariHouse ; rdfs:label "h" .
ex:TS a crm:E52_Time-Span .""", format="turtle")
    c_hg, _, _ = validate(bad, shacl_graph=shapes, ont_graph=ont, inference="none")
    # the CRM idiom can carry the rule too, with a SHACL-SPARQL constraint on
    # activities whose participant acts in the role of the Kumari office
    CRM_SHAPE = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix b: <https://cair-nepal.org/heritagegraph/example/baseline/> .
b:OneDeityShape a sh:NodeShape ; sh:targetClass crm:E7_Activity ;
  sh:sparql [ sh:message "a Kumari service has at most one deity" ; sh:select \"\"\"
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX b: <https://cair-nepal.org/heritagegraph/example/baseline/>
    SELECT $this WHERE { $this crm:P01i_is_domain_of/crm:P14.1_in_the_role_of b:KumariOffice ;
      crm:P15_was_influenced_by ?d1 , ?d2 . FILTER(?d1 != ?d2) } \"\"\" ] ."""
    crm_shapes = Graph().parse(data=CRM_SHAPE, format="turtle")
    crm_ok = Graph().parse(data=CRM_ROLE, format="turtle")
    crm_bad = Graph().parse(data=CRM_ROLE + "b:KumariService crm:P15_was_influenced_by ex:Vajradevi .\n",
                            format="turtle")
    c_crm_ok, _, _ = validate(crm_ok, shacl_graph=crm_shapes, inference="none")
    c_crm, _, _ = validate(crm_bad, shacl_graph=crm_shapes, inference="none")
    print(f"\n'one deity per tenure': HeritageGraph's published shape catches two deities "
          f"(conforms={c_hg}). The CRM idiom can enforce it too, but only with a SHACL-SPARQL "
          f"constraint the data publisher writes over the role reification "
          f"(two influences conforms={c_crm}; one influence conforms={c_crm_ok}). The difference "
          f"is that HeritageGraph ships the rule; expressiveness is equal.")
    ok &= (not c_hg) and (not c_crm) and c_crm_ok
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


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

    PFX = """PREFIX hg:  <https://cair-nepal.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX ex:  <https://cair-nepal.org/heritagegraph/example/>
"""

    BASE = """@prefix hg:  <https://cair-nepal.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:  <https://cair-nepal.org/heritagegraph/example/> .

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
    hg:syncreticType <https://cair-nepal.org/heritagegraph/SyncreticType#Equivalence> ;
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
    """Institutional-depth scenario on HeritageGraph's own patterns: an
    endowment held by a state body that sustains a ritual (hg:Endowment,
    P105, hg:sustains), a dated custody chain opened and closed by transfers of
    custody with an open current period (hg:CustodyPeriod), and a hereditary
    office held by a caste group under that body's mandate
    (hg:HereditaryRoleTenure). Illustrative scenario, separate from the
    demonstrator; the institutions and dates are simplified, not a historical
    record. Fails unless every question is answered and the data conforms.
    """
    from pyshacl import validate

    PFX = """PREFIX hg:  <https://cair-nepal.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX ex:  <https://cair-nepal.org/heritagegraph/example/cust/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

    SCENARIO = """@prefix hg:  <https://cair-nepal.org/heritagegraph/> .
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:  <https://cair-nepal.org/heritagegraph/example/cust/> .

ex:Pavilion a hg:Sattal ; rdfs:label "Public pavilion (illustrative)" .
ex:PrivateGuthi a hg:Guthi ; rdfs:label "Pavilion guthi (illustrative)" ;
    hg:guthiType <https://cair-nepal.org/heritagegraph/GuthiType#TempleGuthi> .
ex:StateBody a hg:StateHeritageAuthority ; rdfs:label "State guthi corporation (illustrative)" .

# custody chain: the guthi, then the state body from 13 April 1964 (open: no end)
ex:T_1964 a crm:E52_Time-Span ;
    crm:P82a_begin_of_the_begin "1964-04-13T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "1964-04-13T23:59:59"^^xsd:dateTime .
ex:Transfer_1964 a crm:E10_Transfer_of_Custody ; rdfs:label "Transfer to the state body" ;
    crm:P30_transferred_custody_of ex:Pavilion ;
    crm:P28_custody_surrendered_by ex:PrivateGuthi ;
    crm:P29_custody_received_by ex:StateBody ;
    crm:P4_has_time-span ex:T_1964 .
ex:CP_Guthi a hg:CustodyPeriod ; rdfs:label "Custody by the guthi" ;
    hg:custodyHolder ex:PrivateGuthi ; hg:custodyObject ex:Pavilion ;
    hg:custodyClosedBy ex:Transfer_1964 ;
    crm:P4_has_time-span ex:T_CP_Guthi .
ex:T_CP_Guthi a crm:E52_Time-Span ;
    crm:P82a_begin_of_the_begin "1900-01-01T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "1964-04-13T00:00:00"^^xsd:dateTime .
ex:CP_State a hg:CustodyPeriod ; rdfs:label "Custody by the state body (current)" ;
    hg:custodyHolder ex:StateBody ; hg:custodyObject ex:Pavilion ;
    hg:custodyOpenedBy ex:Transfer_1964 ;
    crm:P4_has_time-span ex:T_CP_State .
ex:T_CP_State a crm:E52_Time-Span ;
    crm:P82a_begin_of_the_begin "1964-04-13T00:00:00"^^xsd:dateTime .

# endowment held by the state body that sustains a ritual
ex:Festival a hg:Festival ; rdfs:label "City festival (illustrative)" ;
    hg:performedByGroup ex:CarpenterCaste .
ex:Endowment a hg:Endowment ; rdfs:label "Festival land endowment" ;
    crm:P105_right_held_by ex:StateBody ; hg:sustains ex:Festival .

# hereditary office under the state body's mandate
ex:CarpenterCaste a hg:CasteGroup ; rdfs:label "Carpenter caste group (illustrative)" ;
    hg:traditionalRole "hereditary chariot builders" .
ex:ChariotBuilder a hg:RitualOffice ; rdfs:label "Builder of the festival chariot" .
ex:HRT a hg:HereditaryRoleTenure ; rdfs:label "Chariot-building office" ;
    hg:roleHolder ex:CarpenterCaste ; hg:tenureOffice ex:ChariotBuilder ;
    hg:roleDuty "build the festival chariot" ; hg:dutyFor ex:Festival ;
    hg:mandatedBy ex:StateBody ; hg:successionRule "hereditary within the caste group" .
"""

    QUERIES = {
        "Q1 custody holder of the pavilion in 1950 and in 2000 (open current period)":
            PFX + """SELECT ?year ?holder WHERE {
              VALUES ?year { 1950 2000 }
              ?cp a hg:CustodyPeriod ; hg:custodyObject ex:Pavilion ; hg:custodyHolder ?holder ;
                  crm:P4_has_time-span ?ts .
              ?ts crm:P82a_begin_of_the_begin ?from .
              OPTIONAL { ?ts crm:P82b_end_of_the_end ?to }
              FILTER(YEAR(?from) <= ?year && (!BOUND(?to) || ?year < YEAR(?to)))
            } ORDER BY ?year""",
        "Q2 the transfer that opened the current custody (from, to, time-span)":
            PFX + """SELECT ?transfer ?from ?to ?ts WHERE {
              ?cp a hg:CustodyPeriod ; hg:custodyOpenedBy ?transfer .
              FILTER NOT EXISTS { ?cp crm:P4_has_time-span/crm:P82b_end_of_the_end ?end }
              ?transfer crm:P28_custody_surrendered_by ?from ; crm:P29_custody_received_by ?to ;
                        crm:P4_has_time-span ?ts . }""",
        "Q3 hereditary office (holder, office, duty, festival, mandating body)":
            PFX + """SELECT ?holder ?office ?duty ?festival ?body WHERE {
              ?t a hg:HereditaryRoleTenure ; hg:roleHolder ?holder ; hg:tenureOffice ?office ;
                 hg:roleDuty ?duty ; hg:dutyFor ?festival ; hg:mandatedBy ?body . }""",
        "Q4 endowment: holder that sustains the festival, and the group performing it":
            PFX + """SELECT ?endowment ?holder ?festival ?group WHERE {
              ?endowment a hg:Endowment ; crm:P105_right_held_by ?holder ; hg:sustains ?festival .
              ?festival hg:performedByGroup ?group . }""",
    }
    EXPECTED = {
        "Q1": {("1950", "PrivateGuthi"), ("2000", "StateBody")},
        "Q2": {("Transfer_1964", "PrivateGuthi", "StateBody", "T_1964")},
        "Q3": {("CarpenterCaste", "ChariotBuilder", "build the festival chariot", "Festival", "StateBody")},
        "Q4": {("Endowment", "StateBody", "Festival", "CarpenterCaste")},
    }

    g = Graph()
    g.parse(data=SCENARIO, format="turtle")
    print(f"Scenario: {len(g)} triples\n")
    ok = True
    for name, q in QUERIES.items():
        rows = {tuple(str(x).rsplit("/", 1)[-1] for x in r) for r in g.query(q)}
        good = rows == EXPECTED[name[:2]]
        ok &= good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: {sorted(rows)}")
    conforms, _, report = validate(g, shacl_graph=_shapes(), ont_graph=_ont_for_shacl(),
                                   inference="none", abort_on_first=False)
    print(f"  [{'PASS' if conforms else 'FAIL'}] SHACL conformance of the scenario")
    if not conforms:
        print(report[:2000])
    ok &= conforms
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


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

    PFX = """PREFIX hg:     <https://cair-nepal.org/heritagegraph/>
PREFIX crm:    <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX crminf: <http://www.cidoc-crm.org/extensions/crminf/>
PREFIX prov:   <http://www.w3.org/ns/prov#>
PREFIX ex:     <https://cair-nepal.org/heritagegraph/example/>
PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
"""

    SCENARIO = """@prefix hg:     <https://cair-nepal.org/heritagegraph/> .
@prefix crm:    <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix crminf: <http://www.cidoc-crm.org/extensions/crminf/> .
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:     <https://cair-nepal.org/heritagegraph/example/> .

ex:Kasthamandap a hg:Temple ;
    rdfs:label "Kasthamandap" ;
    hg:hasArchitecturalStyle <https://cair-nepal.org/heritagegraph/ArchitecturalStyle#Pagoda> .

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
    hg:confidenceScore "0.4"^^xsd:decimal .

ex:Assert_Date_v2 a crminf:I2_Belief ;
    rdfs:label "Kasthamandap build date, v2" ;
    hg:assertsAbout ex:Kasthamandap ;
    prov:value "12th century CE" ;
    prov:wasDerivedFrom ex:Src_Slusser ;
    prov:wasAttributedTo ex:Slusser ;
    prov:generatedAtTime "1982-01-01T00:00:00"^^xsd:dateTime ;
    prov:wasRevisionOf ex:Assert_Date_v1 ;
    hg:confidenceScore "0.6"^^xsd:decimal .

ex:Assert_Date_v3 a crminf:I2_Belief ;
    rdfs:label "Kasthamandap build date, v3" ;
    hg:assertsAbout ex:Kasthamandap ;
    prov:value "not later than 1143 CE" ;
    prov:wasDerivedFrom ex:Src_Excavation ;
    prov:wasAttributedTo ex:ExcavationTeam ;
    prov:generatedAtTime "2019-01-01T00:00:00"^^xsd:dateTime ;
    prov:wasRevisionOf ex:Assert_Date_v2 ;
    crminf:J4_that ex:Prop_Date ;
    hg:confidenceScore "0.9"^^xsd:decimal .

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
                .replace("https://cair-nepal.org/heritagegraph/example/", "ex:")
                .replace("https://cair-nepal.org/heritagegraph/", "hg:")
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
    yearOffsetFromGregorian / epochDateGregorian / isPrimaryForTradition, and
    the 1.1.0 separation of the recorded date (hg:recordedDate) from its
    converted Gregorian bounds (crm:P82a / crm:P82b).
    Released, shape-conformant scenario, separate from the demonstrator.
    """
    from pyshacl import validate

    PFX = """PREFIX hg:   <https://cair-nepal.org/heritagegraph/>
PREFIX crm:  <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX ex:   <https://cair-nepal.org/heritagegraph/example/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

    SCENARIO = """@prefix hg:   <https://cair-nepal.org/heritagegraph/> .
@prefix crm:  <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <https://cair-nepal.org/heritagegraph/example/> .

# --- Religious traditions the calendars serve ---------------------------
ex:HinduTradition a hg:ReligiousTradition ; rdfs:label "Hindu tradition" .
ex:NewarBuddhistTradition a hg:ReligiousTradition ;
    rdfs:label "Newar Buddhist tradition" .

# --- The three calendar systems -----------------------------------------
# Offset semantics (per schema): CE = calendar year - yearOffsetFromGregorian.
# Epoch convention: epochDateGregorian is the proleptic Gregorian date on which
# the year numbered (CE year of the epoch + offset) begins. For Bikram Sambat
# that is year 1 (57 BCE = astronomical year -56; a nominal back-projection of
# the modern solar reckoning, not a historically attested date); for Nepal
# Sambat it is year 0 (879 CE; N.S. 1 began in 880, N.S. 1146 in 2025).
ex:BikramSambat a hg:CalendarSystem ; rdfs:label "Bikram Sambat" ;
    hg:epochDateGregorian "-0056-04-14" ;      # 57 BCE, mid-April new year
    hg:yearOffsetFromGregorian 57 ;
    hg:isPrimaryForTradition ex:HinduTradition ;
    crm:P3_has_note "Solar calendar of Nepal; new year at Mesh Sankranti (Baisakh 1, 13-15 April)." .
ex:NepalSambat a hg:CalendarSystem ; rdfs:label "Nepal Sambat" ;
    hg:epochDateGregorian "0879-10-24" ;       # epoch 20 Oct 879 Julian = 24 Oct proleptic Gregorian
    hg:yearOffsetFromGregorian -879 ;
    hg:isPrimaryForTradition ex:NewarBuddhistTradition ;
    crm:P3_has_note "Lunisolar Newar calendar; new year at Mha Puja (Oct/Nov)." .
ex:GregorianCalendar a hg:CalendarSystem ; rdfs:label "Gregorian calendar" ;
    hg:epochDateGregorian "0001-01-01" ;
    hg:yearOffsetFromGregorian 0 .

# --- Two dated occurrences, each documented in three calendars -----------
# Each occurrence has its exact (Gregorian) time-span; each source record is
# a time-span with the date as written (hg:recordedDate), its calendar, and its
# converted Gregorian interval (crm:P82a/P82b). The exact time-span falls
# within (crm:P86) each record's interval, which scopes the resolution query.
ex:IndraJatra a hg:Festival ; rdfs:label "Indra Jatra" ;
    hg:lunarDateTithi "Bhadra Shukla Dwadashi" ;
    hg:recurrencePattern "annual (lunar-tithi)" .
ex:ShreePanchami a hg:Festival ; rdfs:label "Shree Panchami" ;
    hg:lunarDateTithi "Magh Shukla Panchami" ;
    hg:recurrencePattern "annual (lunar-tithi)" .

ex:IndraJatra_2015 a hg:RitualEvent ;
    rdfs:label "Indra Jatra, 2015 occurrence" ;
    crm:P9i_forms_part_of ex:IndraJatra ;
    crm:P4_has_time-span ex:TS_IJ_Exact .
ex:TS_IJ_Exact a crm:E52_Time-Span ;
    rdfs:label "Indra Jatra 2015 start, Gregorian record" ;
    hg:recordedDate "2015-09-25" ; hg:calendarSystem ex:GregorianCalendar ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Exact> ;
    crm:P82a_begin_of_the_begin "2015-09-25T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2015-09-25T23:59:59"^^xsd:dateTime ;
    crm:P86_falls_within ex:TS_IJ_BS , ex:TS_IJ_NS ;
    rdfs:seeAlso ex:TS_IJ_BS , ex:TS_IJ_NS .
ex:TS_IJ_BS a crm:E52_Time-Span ;
    rdfs:label "Indra Jatra 2015, Bikram Sambat record (B.S. 2072)" ;
    hg:recordedDate "2072" ; hg:calendarSystem ex:BikramSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2015-04-14T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2016-04-12T23:59:59"^^xsd:dateTime ;
    crm:P3_has_note "B.S. 2072 runs from 1 Baisakh (14 April 2015) to the end of Chaitra (12 April 2016)." .
ex:TS_IJ_NS a crm:E52_Time-Span ;
    rdfs:label "Indra Jatra 2015, Nepal Sambat record (N.S. 1135)" ;
    hg:recordedDate "1135" ; hg:calendarSystem ex:NepalSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2014-10-24T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2015-11-11T23:59:59"^^xsd:dateTime ;
    crm:P3_has_note "N.S. 1135 runs from Mha Puja 2014 (24 October) to the day before Mha Puja 2015 (12 November)." .

# Boundary case: a Magh date. B.S. 2072 - 57 = 2015, but the occurrence is in
# 2016: only the two-year interval rule admits it.
ex:ShreePanchami_2016 a hg:RitualEvent ;
    rdfs:label "Shree Panchami, 2016 occurrence" ;
    crm:P9i_forms_part_of ex:ShreePanchami ;
    crm:P4_has_time-span ex:TS_SP_Exact .
ex:TS_SP_Exact a crm:E52_Time-Span ;
    rdfs:label "Shree Panchami 2016, Gregorian record" ;
    hg:recordedDate "2016-02-12" ; hg:calendarSystem ex:GregorianCalendar ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Exact> ;
    crm:P82a_begin_of_the_begin "2016-02-12T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2016-02-12T23:59:59"^^xsd:dateTime ;
    crm:P86_falls_within ex:TS_SP_BS , ex:TS_SP_NS ;
    rdfs:seeAlso ex:TS_SP_BS , ex:TS_SP_NS ;
    # the naively converted record is cited for the occurrence, not claimed to
    # contain it (crm:P86 would assert a falsehood)
    rdfs:seeAlso ex:TS_SP_BS_naive .
ex:TS_SP_BS a crm:E52_Time-Span ;
    rdfs:label "Shree Panchami 2016, Bikram Sambat record (B.S. 2072, Magh)" ;
    hg:recordedDate "2072" ; hg:calendarSystem ex:BikramSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2015-04-14T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2016-04-12T23:59:59"^^xsd:dateTime .
ex:TS_SP_NS a crm:E52_Time-Span ;
    rdfs:label "Shree Panchami 2016, Nepal Sambat record (N.S. 1136)" ;
    hg:recordedDate "1136" ; hg:calendarSystem ex:NepalSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2015-11-12T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2016-10-30T23:59:59"^^xsd:dateTime .
# Conversion-error case: the same B.S. year converted naively as one
# Gregorian calendar year (Y - 57, 1 January to 31 December).
ex:TS_SP_BS_naive a crm:E52_Time-Span ;
    rdfs:label "Shree Panchami 2016, B.S. 2072 record converted naively (ERROR CASE)" ;
    hg:recordedDate "2072" ; hg:calendarSystem ex:BikramSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2015-01-01T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2015-12-31T23:59:59"^^xsd:dateTime .
# Correct conversions (positive controls for the full-bound check): B.S. 2073
# began on 13 April 2016, N.S. 1138 at Mha Puja, 20 October 2017.
ex:TS_BS_2073 a crm:E52_Time-Span ; rdfs:label "B.S. 2073 (correct conversion)" ;
    hg:recordedDate "2073" ; hg:calendarSystem ex:BikramSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2016-04-13T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2017-04-13T23:59:59"^^xsd:dateTime .
ex:TS_NS_1138 a crm:E52_Time-Span ; rdfs:label "N.S. 1138 (correct conversion)" ;
    hg:recordedDate "1138" ; hg:calendarSystem ex:NepalSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2017-10-20T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2018-11-07T23:59:59"^^xsd:dateTime .
# Conversion-error case for Nepal Sambat: N.S. 1138 begun two months early.
ex:TS_NS_early a crm:E52_Time-Span ; rdfs:label "N.S. 1138 record begun two months early (ERROR CASE)" ;
    hg:recordedDate "1138" ; hg:calendarSystem ex:NepalSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2017-08-20T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2018-08-19T23:59:59"^^xsd:dateTime .
# Conversion-error case: a month late (B.S. 2072 begun on 14 May 2015).
ex:TS_BS_month_late a crm:E52_Time-Span ;
    rdfs:label "B.S. 2072 record begun a month late (ERROR CASE)" ;
    hg:recordedDate "2072" ; hg:calendarSystem ex:BikramSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2015-05-14T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2016-05-13T23:59:59"^^xsd:dateTime .
# Conversion-error case the year-only check cannot see: the right Gregorian
# years (2015-2016) but the wrong months (as if B.S. began in October).
ex:TS_BS_wrong_months a crm:E52_Time-Span ;
    rdfs:label "B.S. 2072 record converted with the wrong new year (ERROR CASE)" ;
    hg:recordedDate "2072" ; hg:calendarSystem ex:BikramSambat ;
    hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
    crm:P82a_begin_of_the_begin "2015-10-01T00:00:00"^^xsd:dateTime ;
    crm:P82b_end_of_the_end "2016-09-30T23:59:59"^^xsd:dateTime .
"""

    QUERIES = {
        "Q1 per-record conversion rule: recorded year -> Gregorian year interval":
            PFX + """SELECT ?record ?calendar ?srcYear ?ceLow ?ceHigh WHERE {
              ?record a crm:E52_Time-Span ;
                      hg:recordedDate ?rec ;
                      hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
                      hg:calendarSystem ?cal .
              ?cal rdfs:label ?calendar ;
                   hg:yearOffsetFromGregorian ?off ;
                   hg:epochDateGregorian ?epoch .
              BIND(xsd:integer(?rec) AS ?srcYear)
              BIND(?srcYear - ?off AS ?ceLow)
              BIND(IF(STRENDS(?epoch, "-01-01"), ?ceLow, ?ceLow + 1) AS ?ceHigh)
            } ORDER BY ?record""",
        "Q2 resolution: each occurrence and the calendar records whose interval does NOT contain it":
            PFX + """SELECT ?occurrence ?date ?conflicting WHERE {
              ?occ rdfs:label ?occurrence ; crm:P4_has_time-span ?exact .
              ?exact crm:P82a_begin_of_the_begin ?date .
              OPTIONAL {
                ?exact rdfs:seeAlso ?rec .
                ?rec crm:P82a_begin_of_the_begin ?rb ; crm:P82b_end_of_the_end ?re .
                FILTER(?date < ?rb || ?date > ?re)
                BIND(?rec AS ?conflicting)
              }
            } ORDER BY ?occurrence ?conflicting""",
        "Q4 conversion check: records whose stored Gregorian bounds disagree with their recorded year":
            PFX + """SELECT ?record ?srcYear ?storedFrom ?storedTo WHERE {
              ?record hg:recordedDate ?rec ;
                      hg:datePrecision <https://cair-nepal.org/heritagegraph/DatePrecision#Year> ;
                      hg:calendarSystem ?cal ;
                      crm:P82a_begin_of_the_begin ?b ; crm:P82b_end_of_the_end ?e .
              ?cal hg:yearOffsetFromGregorian ?off ; hg:epochDateGregorian ?epoch .
              BIND(xsd:integer(?rec) AS ?srcYear)
              BIND(?srcYear - ?off AS ?lo)
              BIND(IF(STRENDS(?epoch, "-01-01"), ?lo, ?lo + 1) AS ?hi)
              BIND(YEAR(?b) AS ?storedFrom)
              BIND(YEAR(?e) AS ?storedTo)
              FILTER(?storedFrom != ?lo || ?storedTo != ?hi)
            } ORDER BY ?record""",
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
                str(x).replace("https://cair-nepal.org/heritagegraph/example/", "")
                for x in r))
    print()

    shapes = _shapes()
    ont = _ont_for_shacl()
    conforms, _, report = validate(g, shacl_graph=shapes, ont_graph=ont,
                                   inference="none", abort_on_first=False)
    print(f"SHACL conformance of the scenario: conforms={conforms}")
    if not conforms:
        print(report[:2000])

    # --- expected results (the experiment fails if any differs) -----------
    def res(name):
        return [tuple(str(x).replace("https://cair-nepal.org/heritagegraph/example/", "")
                      if x is not None else None for x in r)
                for r in g.query(QUERIES[name])]
    q1 = {(r[0], int(r[3]), int(r[4])) for r in res(next(k for k in QUERIES if k.startswith("Q1")))}
    q2 = res(next(k for k in QUERIES if k.startswith("Q2")))
    q4_year_only = [r[0] for r in res(next(k for k in QUERIES if k.startswith("Q4")))]

    # Full-bound conversion check (Q4 above compares years only). The calendar's
    # new year moves from year to year, so the check uses its window, not the
    # epoch's day: Bikram Sambat (solar) begins on 13-15 April; Nepal Sambat
    # (lunisolar) at Mha Puja, between about 13 October and 15 November. A
    # year record's interval must start inside the window of its converted CE
    # year and end on the day before the window of the next year. Limitation:
    # the Nepal Sambat window is a month wide (no per-year Mha Puja table is
    # used), so Nepal Sambat records are checked to within about a month,
    # Bikram Sambat records to within a day or two. A record that does not
    # parse, lacks a bound, a calendar, a known calendar or a date precision
    # is reported, not skipped.
    from datetime import date, datetime, timedelta
    EXN = "https://cair-nepal.org/heritagegraph/example/"
    NEW_YEAR_WINDOW = {EXN + "BikramSambat": ((4, 13), (4, 15)),
                       EXN + "NepalSambat": ((10, 13), (11, 15)),
                       EXN + "GregorianCalendar": ((1, 1), (1, 1))}
    # a lunisolar Nepal Sambat year has 353-385 days (12 or 13 lunar months)
    LENGTH = {EXN + "NepalSambat": (353, 385)}
    bad_bounds, unparseable = [], []
    for rec, recd, prec, cal, off, b, e in g.query(PFX + """
        SELECT ?record ?rec ?prec ?cal ?off ?b ?e WHERE {
          ?record hg:recordedDate ?rec .
          OPTIONAL { ?record hg:datePrecision ?prec }
          OPTIONAL { ?record hg:calendarSystem ?cal .
                     OPTIONAL { ?cal hg:yearOffsetFromGregorian ?off } }
          OPTIONAL { ?record crm:P82a_begin_of_the_begin ?b }
          OPTIONAL { ?record crm:P82b_end_of_the_end ?e } }"""):
        name = str(rec).rsplit("/", 1)[-1]
        if prec is None or cal is None:
            unparseable.append(name)
            continue
        if not str(prec).endswith("#Year"):
            continue                       # only year-precision records are checked here
        if str(cal) not in NEW_YEAR_WINDOW:
            unparseable.append(name)
            continue
        try:
            year = int(str(recd))
        except ValueError:
            unparseable.append(name)
            continue
        if off is None or b is None or e is None or year - int(off) < 1:
            unparseable.append(name)
            continue
        ce = year - int(off)
        (m1, d1), (m2, d2) = NEW_YEAR_WINDOW[str(cal)]
        start = datetime.fromisoformat(str(b)).date()
        end = datetime.fromisoformat(str(e)).date()
        starts_ok = date(ce, m1, d1) <= start <= date(ce, m2, d2)
        ends_ok = date(ce + 1, m1, d1) - timedelta(days=1) <= end <= date(ce + 1, m2, d2) - timedelta(days=1)
        lo, hi = LENGTH.get(str(cal), (0, 10**6))
        if not (starts_ok and ends_ok and lo <= (end - start).days + 1 <= hi):   # days in the year
            bad_bounds.append(name)
    q4 = sorted(bad_bounds)
    print(f"Q4 full-bound check: records whose bounds disagree with their recorded year: {q4}; "
          f"unparseable recorded years: {unparseable}")
    checks = {
        "Q1 BS 2072 -> 2015-2016, NS 1135 -> 2014-2015, NS 1136 -> 2015-2016":
            {("TS_IJ_BS", 2015, 2016), ("TS_IJ_NS", 2014, 2015), ("TS_SP_NS", 2015, 2016)} <= q1,
        "Q2 Indra Jatra 2015 is contained in every record":
            [r[2] for r in q2 if r[0].startswith("Indra Jatra")] == [None],
        "Q2 Shree Panchami 2016 conflicts only with the naive record":
            [r[2] for r in q2 if r[0].startswith("Shree Panchami")] == ["TS_SP_BS_naive"],
        "Q4 (full bounds) flags exactly the four error records (three BS, one NS)":
            q4 == ["TS_BS_month_late", "TS_BS_wrong_months", "TS_NS_early", "TS_SP_BS_naive"],
        "Q4 (full bounds) accepts the correct BS 2073 and NS 1138 records":
            "TS_BS_2073" not in q4 and "TS_NS_1138" not in q4,
        "Q4 (year only) misses the wrong-month record": q4_year_only == ["TS_SP_BS_naive"],
        "every year record parses (none skipped)": not unparseable,
        "boundary case: single-year conversion (Y - 57) misses Shree Panchami 2016":
            2072 - 57 != 2016,
        "SHACL conforms": bool(conforms),
    }
    for name, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    return 0 if all(checks.values()) else 1


# ===========================================================================
# reuse (RQ3): the Tenure pattern outside Nepal.
# ===========================================================================
REUSE_GENERIC = {"Tenure", "Office", "tenureHolder", "tenureOffice", "tenureOpenedBy",
                 "tenureClosedBy", "CustodyPeriod", "custodyHolder", "custodyObject",
                 "custodyOpenedBy", "custodyClosedBy", "StateHeritageAuthority",
                 "accessProtocol", "hasAssertion"}
# enumerations a non-Nepali record may use (values are <hg>Enum#Value)
REUSE_GENERIC_ENUMS = {"AccessProtocol", "DatePrecision", "ExistenceStatus"}
REUSE_QUERY = """
PREFIX hg: <https://cair-nepal.org/heritagegraph/>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?tenure ?holder ?office ?from WHERE {
  ?tenure a/rdfs:subClassOf* hg:Tenure ; ?hp ?holder .
  ?hp rdfs:subPropertyOf* hg:tenureHolder .
  OPTIONAL { ?tenure ?op ?office . ?op rdfs:subPropertyOf* hg:tenureOffice }
  OPTIONAL { ?tenure crm:P4_has_time-span/crm:P82a_begin_of_the_begin ?from }
}"""


def run_reuse() -> int:
    """RQ3: the generic Tenure pattern describes offices and custody outside
    Nepal with no Nepal-specific term, and ONE query ("who held which office
    or custody, from when") answers for the Nepali demonstrator and the
    non-Nepali fixture alike. Checks: (1) the fixture uses only generic
    HeritageGraph terms; (2) it conforms to the SHACL shapes; (3) the generic
    query returns every tenure of both, with holder and office, through the
    subclass and subproperty hierarchy (no per-class query)."""
    from pyshacl import validate
    HG = "https://cair-nepal.org/heritagegraph/"
    fixture = Graph().parse(ROOT / "examples" / "reuse-tenure-beyond-nepal.ttl", format="turtle")
    hg_terms = {str(t)[len(HG):] for tr in fixture for t in tr
                if str(t).startswith(HG) and "/example/" not in str(t)}
    used = {t for t in hg_terms if "#" not in t}
    enum_values = {t for t in hg_terms if "#" in t}
    specific = sorted(used - REUSE_GENERIC)
    specific += sorted(v for v in enum_values if v.split("#")[0] not in REUSE_GENERIC_ENUMS)
    print(f"[reuse] HeritageGraph terms used by the non-Nepali fixture: {sorted(used)}")
    ok = not specific
    print(f"  {'PASS' if ok else 'FAIL'}: only generic pattern terms"
          + (f" (Nepal-specific: {specific})" if specific else ""))
    conforms, _, txt = validate(fixture, shacl_graph=_shapes(), ont_graph=_ont_for_shacl(),
                                inference="none")
    print(f"  {'PASS' if conforms else 'FAIL'}: fixture conforms to the SHACL shapes")
    if not conforms:
        print(txt[:1200])
    ok &= conforms
    g = Graph()
    g.parse(ROOT / "ontology" / "HeritageGraph.ttl", format="turtle")
    g.parse(ROOT / "examples" / "kathmandu-mini-abox.ttl", format="turtle")
    g += fixture
    rows = sorted({tuple(str(x).rsplit("/", 1)[-1] if x is not None else None for x in r)
                   for r in g.query(REUSE_QUERY)}, key=lambda r: [str(v) for v in r])
    for r in rows:
        print(f"    {r}")
    want = {("Tenure_2017", "KumariPerson", "RoyalKumariRole"),
            ("HRT_BarahiChariot", "Barahis", "Office_BungadyahChariotBuilder"),
            ("CP_Kasthamandap_KRC", "KRC", None),
            ("RectorTenure", "PersonR", "RectorOffice"),
            ("MuseumCustody", "Museum", None)}
    got = {r[:3] for r in rows}
    missing = want - got
    print(f"  {'PASS' if not missing else 'FAIL'}: one generic query answers Nepali and non-Nepali "
          f"tenures ({len(got)} tenure rows)" + (f"; missing {sorted(missing, key=str)}" if missing else ""))
    ok &= not missing
    print("PASS: the Tenure pattern is reused outside Nepal without Nepal-specific terms."
          if ok else "FAIL")
    return 0 if ok else 1


EXPERIMENTS = {
    "ablation": run_ablation,
    "tenure": run_tenure,
    "sameas": run_sameas,
    "custodianship": run_custodianship,
    "supersession": run_supersession,
    "multicalendar": run_multicalendar,
    "reuse": run_reuse,
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
