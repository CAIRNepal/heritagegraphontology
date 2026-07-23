#!/usr/bin/env python3
"""Supersession chain + structured Proposition: the untested epistemic machinery.

Two pieces of the belief layer were described in the paper but never
exercised: version supersession (prov:wasRevisionOf, "the latest assertion
is the one with no incoming wasRevisionOf") and the structured-content
Proposition (crminf:J4_that -> subject/predicate/object reification).
This experiment exercises both on one scholarly episode.

Scenario (released, shape-conformant, separate from the demonstrator so the
published counts stay untouched): three successive beliefs about the
construction date of the Kasthamandap, forming a revision chain
A1 <- A2 <- A3 (arrows are prov:wasRevisionOf):

  A1  "7th century CE"        early attribution           confidence 0.4
  A2  "12th century CE"       Slusser's reassessment      confidence 0.6
  A3  "not later than 1143 CE" post-2015-earthquake        confidence 0.9
      excavation dating; carries a machine-readable Proposition
      (subject: Kasthamandap, predicate: crm:P82b_end_of_the_end,
       literal object: "1143") via crminf:J4_that.

Queries:
  Q1  Full supersession chain from the head: every belief on the
      prov:wasRevisionOf+ path with value, source, and confidence.
  Q2  Current vs. superseded: the current belief is the one with no
      incoming wasRevisionOf (FILTER NOT EXISTS); everything else about
      the same subject with an incoming edge is superseded. Both verdicts
      returned in one query.
  Q3  Structured content of the current belief: J4_that -> Proposition ->
      propositionSubject / propositionPredicate / propositionLiteralValue,
      i.e. the claim retrieved as data rather than parsed from prose.

The scenario validates under the published SHACL shapes in the
pipeline-gate configuration (ont_graph mixed in, inference="none",
owl:NamedIndividual declarations stripped from the in-memory copy only).

Run:  evaluation/.venv/bin/python evaluation/supersession_chain.py
"""
import sys
from pathlib import Path

from rdflib import Graph, RDF, OWL
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]

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

# SHACL validation, pipeline-gate configuration.
shapes = Graph()
shapes.parse(ROOT / "ontology" / "HeritageGraph.shacl.ttl", format="turtle")
ont = Graph()
ont.parse(ROOT / "ontology" / "HeritageGraph.ttl", format="turtle")
for s in list(ont.subjects(RDF.type, OWL.NamedIndividual)):
    ont.remove((s, RDF.type, OWL.NamedIndividual))
data = Graph()
data.parse(data=SCENARIO, format="turtle")
conforms, _, txt = validate(data, shacl_graph=shapes, ont_graph=ont,
                            inference="none", abort_on_first=False)
print(f"\nSHACL conformance of the scenario: conforms={conforms}")
if not conforms:
    print(txt[:2000])
    sys.exit(1)

print("\nPASS: the supersession chain is traversable, the current belief is "
      "derivable from the absence of an incoming revision, and the current "
      "claim's content is retrievable as a structured Proposition rather "
      "than prose.")
