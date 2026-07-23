#!/usr/bin/env python3
"""Demonstrate the identity collapse that owl:sameAs causes for syncretism.

Addresses the reviewer request to *show*, not merely assert, that modelling
the Avalokitesvara--Matsyendranath equivalence with owl:sameAs collapses the
two identities, whereas the reified SyncreticRelationship preserves them.

Two graphs carry the same domain facts (two deities, each with its own
religious tradition, plus one equivalence claim from one source):

  Graph S: the equivalence as owl:sameAs.
  Graph R: the equivalence as a SyncreticRelationship
           (crm:P140/P141 + syncreticType + prov:wasDerivedFrom).

Both graphs are expanded with the same OWL-RL closure (owlrl), and three
questions are posed to each:

  Q1  Which deities belong to the Hindu tradition?           (leakage probe)
  Q2  How many traditions does each deity carry?             (merge probe)
  Q3  Who asserted the equivalence, and of what type?        (provenance probe)

Run:  evaluation/.venv/bin/python evaluation/sameas_vs_reified.py
"""
from rdflib import Graph
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
