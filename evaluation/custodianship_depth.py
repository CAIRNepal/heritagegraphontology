#!/usr/bin/env python3
"""Institutional-depth scenario: custody transfer, hereditary roles, endowment.

Addresses the reviewer observation that the institutional pattern was
exercised only by single-pattern retrieval (CQ19/CQ21) and an enum-membership
negative test, with no query touching custody *transfer* through
crm:E10_Transfer_of_Custody, hereditary roles, or endowment support.

The scenario is a released, shape-conformant dataset (separate from the
demonstrator, whose published triple counts stay untouched). It instantiates
a historically grounded situation: after the Guthi Corporation Act (2021 B.S.
/ 1964 CE) many private guthis passed into the state Guthi Sansthan. The
scenario records that transfer as a crm:E10 event and then asks the questions
the institutional pattern claims to answer:

  Q1  Custody transfer: who surrendered custody of what, to whom, and when?
  Q2  Post-transfer custody: who is the current keeper?
  Q3  Hereditary transmission: which caste groups hold which hereditary
      roles in which rituals, and who are their members?
  Q4  Endowment: which institution both keeps the structure and sustains its
      ritual cycle (custody + ritual join)?

The scenario is validated against the published SHACL shapes under the same
configuration as the pipeline gate (ont_graph mixed in, inference="none",
owl:NamedIndividual declarations stripped from the in-memory copy only).

Run:  evaluation/.venv/bin/python evaluation/custodianship_depth.py
"""
from pathlib import Path
from rdflib import Graph, RDF, OWL
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]

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

# SHACL conformance under the pipeline-gate configuration.
shapes = Graph()
shapes.parse(ROOT / "ontology/HeritageGraph.shacl.ttl", format="turtle")
ont = Graph()
ont.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
for s in list(ont.subjects(RDF.type, OWL.NamedIndividual)):
    ont.remove((s, RDF.type, OWL.NamedIndividual))
conforms, _, report = validate(g, shacl_graph=shapes, ont_graph=ont,
                               inference="none", abort_on_first=False)
print(f"SHACL conformance of the scenario: conforms={conforms}")
if not conforms:
    print(report[:2000])
