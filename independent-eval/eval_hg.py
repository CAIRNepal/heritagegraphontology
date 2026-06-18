#!/usr/bin/env python3
"""
Independent evaluation of the HeritageGraph ontology.

Written from scratch (not derived from the repo's evaluation/run_*.py) to
re-evaluate HeritageGraph.ttl on its own terms. Six dimensions:
  A. Structural profile
  B. Logical consistency & OWL-RL reasoning
  C. Modelling-quality heuristics (pitfalls)
  D. Annotation / documentation completeness
  E. Alignment & interoperability
  F. Competency-question coverage (TBox) + SHACL shape coverage + a synthetic
     ABox demonstration with real SPARQL answers (incl. a multi-vocal query).

Everything is computed from the published artefacts; no value is hard-coded.
"""
from __future__ import annotations
from pathlib import Path
import rdflib
from rdflib import Graph, RDF, RDFS, OWL, Namespace, URIRef, Literal, BNode
from rdflib.namespace import SKOS, XSD
import owlrl

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "HeritageGraph.ttl"
SHACL = ROOT / "HeritageGraph.shacl.ttl"
HG = "https://w3id.org/heritagegraph/"
ONT = URIRef(HG + "ontology")

SH = Namespace("http://www.w3.org/ns/shacl#")
CRM = "http://www.cidoc-crm.org/cidoc-crm/"
CRMINF = "http://www.cidoc-crm.org/crminf/"
CRMSCI = "http://www.cidoc-crm.org/crmsci/"
PROV = "http://www.w3.org/ns/prov#"
GEO = "http://www.opengis.net/ont/geosparql#"
TIME = "http://www.w3.org/2006/time#"
AAT = "http://vocab.getty.edu/aat/"
WD = "http://www.wikidata.org/entity/"
SCHEMA = "http://schema.org/"
EDM = "http://www.europeana.eu/schemas/edm/"
FOAF = "http://xmlns.com/foaf/0.1/"
RICO = "https://www.ica.org/standards/RiC/ontology#"
DBO = "http://dbpedia.org/ontology/"
DCT = "http://purl.org/dc/terms/"
DATACITE = "http://purl.org/spar/datacite/"

EXT_NS = {
    "CIDOC-CRM": CRM, "CRMinf": CRMINF, "CRMsci": CRMSCI, "PROV-O": PROV,
    "GeoSPARQL": GEO, "OWL-Time": TIME, "AAT": AAT, "Wikidata": WD,
    "Schema.org": SCHEMA, "EDM": EDM, "FOAF": FOAF, "RICO": RICO,
    "DBpedia": DBO, "DCTerms": DCT, "DataCite": DATACITE,
    "SKOS": str(SKOS), "RDFS": str(RDFS),
}

def hg(u) -> bool:
    return isinstance(u, URIRef) and str(u).startswith(HG) and u != ONT

def localname(u) -> str:
    s = str(u)
    return s.split("#")[-1].split("/")[-1]

def line(c="="): print(c * 72)

def main() -> int:
    g = Graph(); g.parse(TTL, format="turtle")
    print("INDEPENDENT EVALUATION OF HeritageGraph")
    print(f"Source: {TTL}")
    line()
    asserted = len(g)
    print(f"Asserted triples: {asserted}")

    # ---- A. Structural profile ---------------------------------------------
    classes = {s for s in g.subjects(RDF.type, OWL.Class) if hg(s)}
    obj_props = {s for s in g.subjects(RDF.type, OWL.ObjectProperty) if hg(s)}
    dat_props = {s for s in g.subjects(RDF.type, OWL.DatatypeProperty) if hg(s)}
    individuals = {s for s in g.subjects(RDF.type, OWL.NamedIndividual) if hg(s)}
    unions = [s for s in g.subjects(OWL.unionOf, None)]
    named_unions = {s for s in unions if hg(s)}

    # enumerations: HG classes that type >=1 named individual
    enum_of = {}
    for ind in individuals:
        for t in g.objects(ind, RDF.type):
            if hg(t) and t in classes:
                enum_of.setdefault(t, set()).add(ind)
    enum_classes = set(enum_of)
    enum_values = sum(len(v) for v in enum_of.values())

    # subclass axioms among HG classes; external subClassOf
    subclass_internal = []
    subclass_external = 0
    parents = {}
    for s, o in g.subject_objects(RDFS.subClassOf):
        if not hg(s) or isinstance(o, BNode):
            continue
        if hg(o):
            subclass_internal.append((s, o)); parents.setdefault(s, set()).add(o)
        else:
            subclass_external += 1

    # hierarchy depth within HG
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def depth(c):
        ps = [p for p in parents.get(c, ()) if p in classes]
        return 1 + (max((depth(p) for p in ps), default=0))
    max_depth = max((depth(c) for c in classes), default=0)

    # inverse pairs, disjointness, cardinality restrictions
    inverse_pairs = len(list(g.subject_objects(OWL.inverseOf)))
    disjoint = len(list(g.subject_objects(OWL.disjointWith))) + \
               len(list(g.subjects(RDF.type, OWL.AllDisjointClasses)))
    min_card = len(list(g.subject_objects(OWL.minCardinality))) + \
               len(list(g.subject_objects(OWL.minQualifiedCardinality)))
    max_card = len(list(g.subject_objects(OWL.maxCardinality))) + \
               len(list(g.subject_objects(OWL.maxQualifiedCardinality)))

    line("-"); print("A. STRUCTURAL PROFILE")
    print(f"  Named classes (HG ns)        : {len(classes)}")
    print(f"  Object properties (HG ns)    : {len(obj_props)}")
    print(f"  Datatype properties (HG ns)  : {len(dat_props)}")
    print(f"  Named individuals (HG ns)    : {len(individuals)}")
    print(f"  Enumerations (typed classes) : {len(enum_classes)}  -> values: {enum_values}")
    print(f"  owl:unionOf (named subjects) : {len(named_unions)} (total unionOf: {len(unions)})")
    print(f"  Internal subClassOf axioms   : {len(subclass_internal)}")
    print(f"  External subClassOf axioms   : {subclass_external}")
    print(f"  Max class-hierarchy depth    : {max_depth}")
    print(f"  Inverse property pairs       : {inverse_pairs}")
    print(f"  owl:disjointWith axioms      : {disjoint}")
    print(f"  min-cardinality restrictions : {min_card}")
    print(f"  max-cardinality restrictions : {max_card}")

    # ---- D. Annotation completeness ----------------------------------------
    def has(s, p): return (s, p, None) in g
    cls_label = sum(has(c, RDFS.label) for c in classes)
    cls_def = sum(has(c, SKOS.definition) or has(c, RDFS.comment) for c in classes)
    op_range = sum(has(p, RDFS.range) for p in obj_props)
    dp_range = sum(has(p, RDFS.range) for p in dat_props)
    op_domain = sum(has(p, RDFS.domain) for p in obj_props)

    line("-"); print("D. ANNOTATION / DOCUMENTATION COMPLETENESS")
    print(f"  Classes with rdfs:label      : {cls_label}/{len(classes)}")
    print(f"  Classes with definition      : {cls_def}/{len(classes)}")
    print(f"  Object props with rdfs:range : {op_range}/{len(obj_props)}")
    print(f"  Datatype props with range    : {dp_range}/{len(dat_props)}")
    print(f"  Object props with rdfs:domain: {op_domain}/{len(obj_props)}")

    # ---- C. Modelling-quality heuristics -----------------------------------
    props_no_domain = [p for p in obj_props | dat_props if not has(p, RDFS.domain)]
    props_no_range = [p for p in obj_props | dat_props if not has(p, RDFS.range)]
    # sibling groups lacking disjointness
    children_by_parent = {}
    for c, p in subclass_internal:
        children_by_parent.setdefault(p, set()).add(c)
    disj_index = set()
    for a, b in g.subject_objects(OWL.disjointWith):
        disj_index.add(frozenset((a, b)))
    sib_groups_no_disjoint = 0
    for p, kids in children_by_parent.items():
        if len(kids) < 2:
            continue
        kids = list(kids)
        covered = any(frozenset((kids[i], kids[j])) in disj_index
                      for i in range(len(kids)) for j in range(i + 1, len(kids)))
        if not covered:
            sib_groups_no_disjoint += 1
    cls_no_anno = sum(not (has(c, RDFS.label) and (has(c, SKOS.definition) or has(c, RDFS.comment))) for c in classes)

    line("-"); print("C. MODELLING-QUALITY HEURISTICS (pitfall-style)")
    print(f"  Properties missing rdfs:domain : {len(props_no_domain)}")
    print(f"  Properties missing rdfs:range  : {len(props_no_range)}")
    print(f"  Sibling groups w/o disjointness: {sib_groups_no_disjoint}")
    print(f"  Classes missing label+definition: {cls_no_anno}")

    # ---- E. Alignment & interoperability -----------------------------------
    MAP_PREDS = [SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch, SKOS.narrowMatch,
                 OWL.equivalentClass, OWL.equivalentProperty, RDFS.subClassOf,
                 RDFS.subPropertyOf]
    align = {ns: {"classes": set(), "props": set()} for ns in EXT_NS}
    all_props = obj_props | dat_props
    for s, p, o in g:
        if p not in MAP_PREDS or not isinstance(o, URIRef) or not hg(s):
            continue
        for ns_name, ns_uri in EXT_NS.items():
            if str(o).startswith(ns_uri):
                if s in classes:
                    align[ns_name]["classes"].add(s)
                elif s in all_props:
                    align[ns_name]["props"].add(s)
                break
    line("-"); print("E. ALIGNMENT & INTEROPERABILITY")
    tot_c = set(); tot_p = set()
    print(f"  {'Namespace':<12}{'Classes':>8}{'Props':>7}")
    for ns_name in EXT_NS:
        c, pr = align[ns_name]["classes"], align[ns_name]["props"]
        if c or pr:
            print(f"  {ns_name:<12}{len(c):>8}{len(pr):>7}")
            tot_c |= c; tot_p |= pr
    print(f"  {'-'*27}")
    print(f"  {'aligned (distinct)':<12}{len(tot_c):>8}{len(tot_p):>7}")
    vocab_used = sum(1 for ns in EXT_NS if align[ns]["classes"] or align[ns]["props"])
    print(f"  External vocabularies used   : {vocab_used}")

    # ---- B. Reasoning / consistency (OWL-RL) -------------------------------
    gr = Graph(); gr.parse(TTL, format="turtle")
    before = len(gr)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(gr)
    after = len(gr)
    nothing = list(gr.subjects(RDFS.subClassOf, OWL.Nothing))
    unsat = [c for c in nothing if hg(c)]
    line("-"); print("B. LOGICAL CONSISTENCY & OWL-RL REASONING")
    print(f"  Triples before closure       : {before}")
    print(f"  Triples after closure        : {after}")
    print(f"  Inferred triples             : {after - before}")
    print(f"  Unsatisfiable HG classes     : {len(unsat)}")
    print(f"  (any class subClassOf Nothing: {len(nothing)})")

    # ---- F1. SHACL shape coverage ------------------------------------------
    sg = Graph(); sg.parse(SHACL, format="turtle")
    node_shapes = set(sg.subjects(RDF.type, SH.NodeShape))
    targeted = {o for o in sg.objects(None, SH.targetClass)}
    prop_constraints = len(list(sg.subject_objects(SH.path)))
    line("-"); print("F1. SHACL SHAPE COVERAGE")
    print(f"  sh:NodeShape                 : {len(node_shapes)}")
    print(f"  distinct sh:targetClass      : {len(targeted)}")
    print(f"  property constraints (sh:path): {prop_constraints}")

    # ---- F2. Competency-question coverage (independent TBox set) ------------
    cl = {localname(c) for c in classes}
    pr = {localname(p) for p in all_props}
    def ok(items):
        return all((x in cl or x in pr) for x in items)
    CQS = [
        ("CQ-i1 Event-mediated construction",
         ["Production", "produced_object", "carried_out_by", "has_timespan"]),
        ("CQ-i2 Condition history via events",
         ["ConditionAssessment", "ConditionState"]),
        ("CQ-i3 Custody transfer to a Guthi",
         ["TransferOfCustody", "Guthi"]),
        ("CQ-i4 Consecration makes a deity present",
         ["Consecration", "Murti", "Deity"]),
        ("CQ-i5 Enshrinement of a deity in a temple",
         ["Enshrinement", "Temple", "Deity"]),
        ("CQ-i6 Living-Goddess tenure as bounded period",
         ["LivingGoddessTenure", "embodied_deity", "has_timespan"]),
        ("CQ-i7 Selection initiates / Retirement ends tenure",
         ["LivingGoddessSelection", "LivingGoddessRetirement"]),
        ("CQ-i8 Provenance-aware syncretism",
         ["SyncreticRelationship", "Deity"]),
        ("CQ-i9 Deity religious tradition",
         ["Deity", "ReligiousTradition"]),
        ("CQ-i10 Guthi performs ritual / holds custody",
         ["Guthi", "RitualEvent"]),
        ("CQ-i11 Assertion-level provenance",
         ["HeritageAssertion", "was_derived_from_source", "DataSource"]),
        ("CQ-i12 Multi-calendar temporal model",
         ["CalendarSystem"]),
        ("CQ-i13 Ritual sequencing",
         ["RitualEvent", "occurs_before", "occurs_after"]),
        ("CQ-i14 Procession route geography",
         ["RitualEvent", "route_places", "start_place", "end_place"]),
        ("CQ-i15 Iconography depicts a deity",
         ["IconographicObject", "depicts_deity", "Deity"]),
    ]
    line("-"); print("F2. COMPETENCY-QUESTION COVERAGE (independent, TBox)")
    passed = 0
    for name, items in CQS:
        miss = [x for x in items if not (x in cl or x in pr)]
        status = "PASS" if not miss else "FAIL"
        if not miss: passed += 1
        extra = "" if not miss else f"  missing={miss}"
        print(f"  [{status}] {name}{extra}")
    print(f"  Coverage: {passed}/{len(CQS)} ({100*passed//len(CQS)}%)")

    # ---- F3. Synthetic ABox demonstration (real SPARQL answers) ------------
    line("-"); print("F3. SYNTHETIC ABOX DEMONSTRATION (real SPARQL)")
    ex = Namespace("https://example.org/hg-demo/")
    H = Namespace(HG)
    a = Graph(); a += g  # TBox + our tiny ABox
    a.bind("ex", ex); a.bind("hg", H)
    def U(n): return H[n]
    # two conflicting, source-attributed assertions about one temple's build date
    a.add((ex.KasthamandapA, RDF.type, U("HeritageAssertion")))
    a.add((ex.KasthamandapA, U("asserts_about_entity"), ex.Kasthamandap))
    a.add((ex.KasthamandapA, U("was_derived_from_source"), ex.Src_Slusser))
    a.add((ex.KasthamandapA, U("asserted_value"), Literal("12th century")))
    a.add((ex.KasthamandapB, RDF.type, U("HeritageAssertion")))
    a.add((ex.KasthamandapB, U("asserts_about_entity"), ex.Kasthamandap))
    a.add((ex.KasthamandapB, U("was_derived_from_source"), ex.Src_DoA))
    a.add((ex.KasthamandapB, U("asserted_value"), Literal("7th century")))
    a.add((ex.Kasthamandap, RDF.type, U("Temple")))
    # a Living Goddess tenure
    a.add((ex.Ten1, RDF.type, U("LivingGoddessTenure")))
    a.add((ex.Ten1, U("embodied_deity"), ex.Taleju))
    a.add((ex.Taleju, RDF.type, U("Deity")))

    q_conflict = """PREFIX hg:<%s> SELECT ?v ?src WHERE {
        ?asr a hg:HeritageAssertion ;
             hg:asserts_about_entity ?e ;
             hg:asserted_value ?v ;
             hg:was_derived_from_source ?src . }""" % HG
    rows = list(a.query(q_conflict))
    print(f"  Multi-vocal/conflicting-assertion query -> {len(rows)} row(s):")
    for v, src in rows:
        print(f"      value={v}  source={localname(src)}")
    q_ten = """PREFIX hg:<%s> SELECT ?t ?d WHERE {
        ?t a hg:LivingGoddessTenure ; hg:embodied_deity ?d . }""" % HG
    rows2 = list(a.query(q_ten))
    print(f"  Living-Goddess tenure query -> {len(rows2)} row(s)")

    # ---- F4. pySHACL validation of the synthetic ABox ----------------------
    try:
        from pyshacl import validate
        conforms, _, _ = validate(a, shacl_graph=sg, inference="none",
                                  abort_on_first=False, meta_shacl=False)
        print(f"  pySHACL validation of synthetic ABox: conforms={conforms}")
    except Exception as e:
        print(f"  pySHACL validation skipped: {e}")
    line()
    print("DONE.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
