"""Unit tests for the release generator (scripts/finalize_alpha5_artifacts.py).

Each test exercises one post-processing function on a small synthetic input,
or one invariant of the committed artefacts, so that a regression points at
the function that caused it. Run:  python -m pytest tests/
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from rdflib import BNode, Graph, Literal, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.collection import Collection
from rdflib.namespace import XSD

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import finalize_alpha5_artifacts as fin  # noqa: E402

HG = Namespace("https://cair-nepal.org/heritagegraph/")
CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
PROV = Namespace("http://www.w3.org/ns/prov#")
SH = Namespace("http://www.w3.org/ns/shacl#")


@pytest.fixture(scope="module")
def sv():
    from linkml_runtime import SchemaView
    return SchemaView(str(fin.SCHEMA))


@pytest.fixture(scope="module")
def csv():
    from linkml_runtime import SchemaView
    s = SchemaView(str(fin.CONTAINER_SCHEMA))
    fin.load_lexical_forms(s)
    return s


@pytest.fixture(scope="module")
def core():
    return Graph().parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")


@pytest.fixture(scope="module")
def shapes():
    return Graph().parse(ROOT / "ontology/HeritageGraph.shacl.ttl", format="turtle")


# --- B2: CIDOC-CRM quantifications ------------------------------------------
@pytest.mark.parametrize("prop,max_one", [
    ("P3_has_note", False),             # (0,n:0,1): many notes per item
    ("P7_took_place_at", False),        # (1,n:0,n)
    ("P4_has_time-span", True),         # (1,1:0,n)
    ("P108i_was_produced_by", True),    # inverse of (1,n:1,1)
    ("P9i_forms_part_of", False),       # inverse of (0,n:0,n)
    ("P55_has_current_location", False),
])
def test_crm_quantification(prop, max_one):
    assert fin.crm_max_one()[CRM[prop]] is max_one


def test_reused_max_one_allowed():
    q = fin.crm_max_one()
    assert fin.reused_max_one_allowed(HG.embodiedDeity, q)          # HG's own: a design choice
    assert not fin.reused_max_one_allowed(PROV.wasGeneratedBy, q)   # owner sets none
    assert fin.reused_max_one_allowed(CRM["P82a_begin_of_the_begin"], q)  # unquantified: kept


def test_relax_reused_max_cardinality_drops_and_keeps():
    g = Graph()
    for p, keep in ((CRM.P3_has_note, False), (CRM["P4_has_time-span"], True), (HG.ownProp, True)):
        r = BNode()
        g.add((HG.C, RDFS.subClassOf, r)); g.add((r, RDF.type, OWL.Restriction))
        g.add((r, OWL.onProperty, p)); g.add((r, OWL.maxCardinality, Literal(1)))
    fin.relax_reused_max_cardinality(g)
    left = {g.value(r, OWL.onProperty) for r in g.subjects(OWL.maxCardinality, None)}
    assert left == {CRM["P4_has_time-span"], HG.ownProp}


# --- B1: language-tagged text -----------------------------------------------
def test_relax_text_ranges(csv):
    g = Graph()
    g.add((HG.routeDescription, RDFS.range, XSD.string))   # free text
    g.add((HG.sourceUrl, RDFS.range, XSD.string))          # lexical_form: code
    fin.relax_text_ranges(g)
    assert (HG.routeDescription, RDFS.range, RDF.PlainLiteral) in g
    assert (HG.sourceUrl, RDFS.range, XSD.string) in g


def test_text_shapes_accept_langstring(shapes):
    def accepts(path):
        out = set()
        for ps in shapes.subjects(SH.path, path):
            dts = set(shapes.objects(ps, SH.datatype))
            for lst in shapes.objects(ps, SH["or"]):
                for m in Collection(shapes, lst):
                    dts |= set(shapes.objects(m, SH.datatype))
            if dts:
                out.add(RDF.langString in dts)
        return out
    assert accepts(CRM.P3_has_note) == {True}
    assert accepts(URIRef("http://www.w3.org/2000/01/rdf-schema#label")) == {True}
    assert accepts(HG.sourceUrl) == {False}


# --- M1: no axioms on external terms; the bridge -----------------------------
def test_owner_states():
    assert fin._owner_states(CRM.E21_Person, RDFS.subClassOf, CRM.E39_Actor)
    assert not fin._owner_states(CRM.E12_Production, RDFS.subClassOf, PROV.Activity)


def test_core_has_no_unowned_external_axioms(core):
    logical = (RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range,
               OWL.equivalentClass, OWL.inverseOf, OWL.disjointWith)
    bad = [(s, p, o) for p in logical for s, o in core.subject_objects(p)
           if isinstance(s, URIRef) and not str(s).startswith(str(HG))
           and not fin._owner_states(s, p, o)]
    assert bad == []


def test_bridge_rule(sv, tmp_path, monkeypatch):
    monkeypatch.setattr(fin, "BRIDGE_OUT", tmp_path / "bridge.ttl")
    fin.write_crm_prov_bridge(sv)
    b = Graph().parse(tmp_path / "bridge.ttl", format="turtle")
    assert (CRM.E12_Production, RDFS.subClassOf, PROV.Activity) in b
    assert (CRM.E6_Destruction, RDFS.subClassOf, PROV.Activity) in b   # inherited mixin
    assert (CRM.E39_Actor, RDFS.subClassOf, PROV.Agent) in b
    assert not any(str(s).startswith(str(HG)) for s in b.subjects(RDFS.subClassOf, None))
    # every class it uses is declared: the module is OWL 2 DL on its own
    used = set(b.subjects(RDFS.subClassOf, None)) | set(b.objects(None, RDFS.subClassOf))
    assert all((c, RDF.type, OWL.Class) in b for c in used)


# --- M2: birth/death shortcuts ------------------------------------------------
def test_birth_death_are_chains_not_p4(core):
    for p, step in ((HG.birthTimespan, CRM.P98i_was_born), (HG.deathTimespan, CRM.P100i_died_in)):
        assert (p, RDFS.subPropertyOf, CRM["P4_has_time-span"]) not in core
        chain = list(Collection(core, core.value(p, OWL.propertyChainAxiom)))
        assert chain == [step, CRM["P4_has_time-span"]]
    assert (HG.publicationTimespan, RDFS.subPropertyOf, CRM["P4_has_time-span"]) not in core


# --- M3: CRM grounding --------------------------------------------------------
def test_crm_superclasses_emitted(sv, core):
    for cn, c in sv.all_classes().items():
        ann = c.annotations.get("crm_superclass") if c.annotations else None
        if ann is not None:
            sub = fin.uri_for(sv, str(c.class_uri))
            assert (sub, RDFS.subClassOf, fin.uri_for(sv, str(ann.value))) in core, cn
    assert not any(str(o).startswith(str(CRM)) for o in core.objects(HG.Deity, RDFS.subClassOf))


# --- M4: SyncreticRelationship is the act ----------------------------------------
def test_syncretic_is_activity(core):
    sups = set(core.objects(HG.SyncreticRelationship, RDFS.subClassOf))
    assert PROV.Activity in sups and CRM.E13_Attribute_Assignment in sups
    assert PROV.Entity not in sups


# --- M5: value restrictions and disjoint kinds -----------------------------------
def test_drop_reused_value_restrictions():
    g = Graph()
    cases = ((CRM.P50i_is_current_keeper_of, HG.ArchitecturalStructure, False),
             (HG.performsRitual, HG.RitualEvent, True),
             (CRM["P4_has_time-span"], CRM["E52_Time-Span"], True))
    for p, v, _ in cases:
        r = BNode()
        g.add((HG.C, RDFS.subClassOf, r)); g.add((r, OWL.onProperty, p)); g.add((r, OWL.allValuesFrom, v))
    fin.drop_reused_value_restrictions(g)
    left = {g.value(r, OWL.onProperty) for r in g.subjects(OWL.allValuesFrom, None)}
    assert left == {p for p, _, keep in cases if keep}


def test_disjoint_kinds(sv):
    g = Graph()
    fin.add_disjoint_kinds(g, sv)
    groups = [list(Collection(g, g.value(n, OWL.members)))
              for n in g.subjects(RDF.type, OWL.AllDisjointClasses)]
    assert len(groups) == 2                     # the kinds, and the concepts pairwise
    concepts = next(m for m in groups if HG.Deity in m)
    assert {HG.Deity, HG.Office, HG.ReligiousTradition} <= set(concepts)
    kinds = next(m for m in groups if HG.Deity not in m)
    assert len(kinds) == 6


def test_no_stupa_chaitya_disjointness(core):
    assert (HG.Stupa, OWL.disjointWith, HG.Chaitya) not in core
    assert (HG.Chaitya, OWL.disjointWith, HG.Stupa) not in core


def test_style_values_deprecated_not_removed(core):
    for v, cls in (("Stupa", HG.Stupa), ("Chaitya", HG.Chaitya)):
        ind = URIRef(f"{HG}ArchitecturalStyle#{v}")
        assert (ind, OWL.deprecated, Literal(True)) in core
        assert (ind, URIRef("http://purl.org/dc/terms/isReplacedBy"), cls) in core


# --- build directives never leak into the release ------------------------------
@pytest.mark.parametrize("directive", ["lexical_form", "owl_property_chain",
                                       "crm_superclass", "disjoint_kind"])
def test_no_build_directive_in_release(core, shapes, directive):
    assert (None, HG[directive], None) not in core
    assert (None, HG[directive], None) not in shapes


# --- JSON Schema ---------------------------------------------------------------
def test_json_schema_valid_and_resolvable():
    import jsonschema
    js = json.loads((ROOT / "ontology/HeritageGraph.schema.json").read_text())
    jsonschema.Draft201909Validator.check_schema(js)
    import re
    refs = set(re.findall(r'"#/\$defs/([^"]+)"', json.dumps(js)))
    assert refs <= set(js["$defs"])


def test_resolve_abstract_refs(csv):
    js = {"$defs": {"A": {"properties": {"x": {"$ref": "#/$defs/AssertionSubject"}}}},
          "properties": {"ritual_assessments": {"items": {"$ref": "#/$defs/RitualAssessment"}}}}
    js["$defs"]["FearlessnessAssessment"] = {}
    fin.resolve_abstract_refs(js, csv)
    assert js["$defs"]["A"]["properties"]["x"] == {"type": "string"}
    assert js["properties"]["ritual_assessments"]["items"] == {
        "anyOf": [{"$ref": "#/$defs/FearlessnessAssessment"}]}


def test_container_collections_accept_subclasses():
    js = json.loads((ROOT / "ontology/HeritageGraph.schema.json").read_text())
    refs = [a["$ref"] for a in js["properties"]["historical_events"]["items"]["anyOf"]]
    assert "#/$defs/HistoricalEvent" in refs and "#/$defs/DestructionEvent" in refs
    temple = [a["$ref"] for a in js["properties"]["structures"]["items"]["anyOf"]]
    assert "#/$defs/Temple" in temple


def test_location_rule_on_every_structure_shape(shapes):
    # the Temple class shape (other shapes, e.g. the deprecated-property warning, also target hg:Temple)
    temple_shape = next(s for s in shapes.subjects(SH.targetClass, HG.Temple) if (s, SH["or"], None) in shapes)
    paths = set()
    for lst in shapes.objects(temple_shape, SH["or"]):
        for m in Collection(shapes, lst):
            paths |= set(shapes.objects(m, SH.path))
    assert {HG.existenceStatus, CRM.P55_has_current_location} <= paths


# --- M11-M14: tenure pattern, offices, state bodies, access protocols ---------
def test_tenure_pattern(core):
    for c in (HG.KumariTenure, HG.HereditaryRoleTenure, HG.CustodyPeriod):
        assert (c, RDFS.subClassOf, HG.Tenure) in core
    assert (HG.Tenure, RDFS.subClassOf, CRM.E4_Period) in core
    for sub, sup in ((HG.roleHolder, HG.tenureHolder), (HG.custodyHolder, HG.tenureHolder),
                     (HG.assumesRole, HG.tenureOffice), (HG.custodyOpenedBy, HG.tenureOpenedBy),
                     (HG.enthronedThrough, HG.tenureOpenedBy), (HG.retiredThrough, HG.tenureClosedBy),
                     (HG.custodyClosedBy, HG.tenureClosedBy)):
        assert (sub, RDFS.subPropertyOf, sup) in core, sub


def test_offices_and_state_bodies(core):
    assert (HG.KumariRole, RDFS.subClassOf, HG.RitualOffice) in core
    assert (HG.RitualOffice, RDFS.subClassOf, HG.Office) in core
    assert (HG.Office, RDFS.subClassOf, CRM.E55_Type) in core
    assert (HG.StateHeritageAuthority, RDFS.subClassOf, CRM.E74_Group) in core


def test_no_health_or_real_minor_in_definitions():
    text = (ROOT / "ontology/HeritageGraph.yaml").read_text(encoding="utf-8").lower()
    for word in ("menstruation", "blood", "scars", "samita"):
        assert word not in text, word


def test_access_protocol_on_mixins(shapes, core):
    paths = set(shapes.objects(None, SH.path))
    assert HG.accessProtocol in paths
    # the closed list sits on the HG subproperty; dcterms:accessRights stays open
    assert URIRef("http://purl.org/dc/terms/accessRights") not in paths
    assert (HG.accessProtocol, RDFS.subPropertyOf, URIRef("http://purl.org/dc/terms/accessRights")) in core


def test_structure_types_are_terms_not_classes(core):
    for gone in ("Vihara", "Dyochhen", "AgamChhen", "Pitha"):
        assert (HG[gone], RDF.type, OWL.Class) not in core
    assert (HG.structureType, RDFS.subPropertyOf, CRM.P2_has_type) in core
    assert (HG.StructureType, RDFS.subClassOf, CRM.E55_Type) in core


def test_custody_object_range_does_not_force_heritage_class(core):
    # a plain crm:E22 in custody must not be entailed a PhysicalHeritageThing
    # (that class is in a disjoint kind): the OWL range is the union base class
    rng = set(core.objects(HG.custodyObject, RDFS.range))
    assert HG.PhysicalHeritageThing not in rng
    for r in rng:
        for x in core.objects(r, OWL.intersectionOf):
            assert HG.PhysicalHeritageThing not in set(Collection(core, x))


@pytest.mark.parametrize("value,ok", [
    ("2024-01-01T12:00:00", True), ("2024-01-01T12:00:00Z", True),
    ("2024-01-01T12:00:00.5Z", True), ("2024-01-01T12:00:00.123+05:45", True),
    ("-0044-03-15T00:00:00", True), ("2024-01-01T12:00:00+14:00", True),
    ("2024-01-01", False), ("2024-01-01T12:00:00\\5Z", False), ("2024-01-01T12:00", False),
])
def test_xsd_datetime_pattern(value, ok):
    """The JSON Schema date-time pattern accepts every xsd:dateTime lexical form,
    fractional seconds included, and rejects what is not one."""
    import re
    assert bool(re.match(fin.XSD_DATETIME, value)) is ok


def test_schema_uses_the_pattern():
    """The released JSON Schema carries the same pattern (one backslash before the dot)."""
    text = (ROOT / "ontology" / "HeritageGraph.schema.json").read_text(encoding="utf-8")
    assert json.dumps(fin.XSD_DATETIME) in text
    assert '"format": "date-time"' not in text
