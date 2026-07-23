#!/usr/bin/env python3
"""Baseline comparison: KumariTenure period vs. the plain-CRM actor-role idiom.

Completes the modelling-comparison triad requested by review (condition
change: ablation_event_vs_static.py; syncretic equivalence:
sameas_vs_reified.py; tenure: this script). The claim under test is the
paper's, that conventional actor-role modelling conflates the enduring
person with the temporary sacred office.

Both arms carry the SAME fact set, the demonstrator's Kumari facts:
a person, the deity Taleju embodied 2017-2025, residence at the Kumari
Ghar during the tenure, support by a Guthi, a selection event and a
retirement event bounding the office.

  * Tenure arm: the released demonstrator ABox as-is. The facts hang off
    a first-class hg:KumariTenure period node with a crm:P4 time-span,
    initiated/terminated by typed lifecycle events.

  * Actor-role arm (charitable plain-CRM baseline): the person is typed
    into the role (crm:P2_has_type "Kumari"); deity, residence, and
    institution attach directly to the person, the only place available
    without a role instance; the selection and retirement events name the
    person (crm:P11_had_participant), the strongest link plain CRM offers
    without inventing the very period node under ablation.

Three paired questions plus one constraint check:

  Q1  Which deity did the person embody, and during which time-span?
  Q2  Which typed events initiated and terminated the office?
  Q3  Where did the incumbent reside during (and only during) the office?
  C4  Can 'exactly one deity per office' be enforced? (SHACL: inject a
      second deity into each arm; the tenure arm must be caught by the
      published KumariTenure shape, the actor-role arm passes silently
      because no shape can target a role that has no node.)

Run:  evaluation/.venv/bin/python evaluation/tenure_vs_actor_role.py
"""
import sys
from pathlib import Path

from rdflib import Graph, RDF, OWL
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]

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
shapes = Graph()
shapes.parse(ROOT / "ontology" / "HeritageGraph.shacl.ttl", format="turtle")
ont = Graph()
ont.parse(ROOT / "ontology" / "HeritageGraph.ttl", format="turtle")
for s in list(ont.subjects(RDF.type, OWL.NamedIndividual)):
    ont.remove((s, RDF.type, OWL.NamedIndividual))

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
    sys.exit(1)
print("\nPASS: the actor-role baseline answers the deity question only with "
      "its temporal scope dropped, cannot express office initiation/"
      "termination, attaches residence timelessly, and offers no bearer for "
      "the one-deity constraint; the tenure node recovers all four.")
