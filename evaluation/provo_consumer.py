#!/usr/bin/env python3
"""PROV-O interoperability: can a generic PROV consumer traverse the beliefs?

Addresses the reviewer observation that the PROV-O alignment was validated
only implicitly (the contradiction query happens to use prov: predicates)
and that no test shows toolchain interoperability, i.e. that a consumer
which knows nothing about HeritageGraph can walk the provenance layer.

Two consumers are tested against the released demonstrator ABox, in both
cases with the HeritageGraph vocabulary deliberately withheld:

  1. A vocabulary-blind SPARQL consumer. The ABox is merged with the
     ontology TBox and closed under RDFS semantics, so the alignment
     axioms (crminf:I2_Belief rdfs:subClassOf prov:Entity,
     crm:E39_Actor rdfs:subClassOf prov:Agent, hg:DataSource
     rdfs:subClassOf prov:Entity, ...) materialise PROV-level types.
     Three queries mentioning ONLY prov: terms (plus rdfs:label) then
     retrieve the beliefs with their attribution, derivation, and
     generation times.

  2. The reference PROV toolchain. The PROV-visible projection of the
     closed graph (triples whose predicate is in the prov: namespace,
     rdf:type triples targeting prov: classes, and labels) is handed to
     the `prov` library -- the W3C-maintained reference implementation of
     the PROV data model -- via its PROV-O (RDF) deserialiser. The test
     then traverses the resulting ProvDocument through the library's own
     record API (no SPARQL, no rdflib): entities, agents, attribution and
     derivation edges, and, for each belief, the walk
     belief -> wasAttributedTo -> agent and belief -> wasDerivedFrom ->
     source must succeed.

Scope stated honestly: what a PROV-blind consumer recovers is the
epistemic core of each belief (claim value, asserting agent, source
document, generation time). The domain-facing join -- WHAT the belief is
about (hg:assertsAbout) and its confidence score -- is HeritageGraph
vocabulary by design, invisible at the pure-PROV level.

Run:  evaluation/.venv/bin/python evaluation/provo_consumer.py
"""
import sys
import tempfile
from pathlib import Path

from rdflib import Graph, Namespace, RDF, RDFS, URIRef
from owlrl import DeductiveClosure, RDFS_Semantics

ROOT = Path(__file__).resolve().parents[1]
PROV = Namespace("http://www.w3.org/ns/prov#")

# --- Stage 1: RDFS closure over ABox + TBox --------------------------------
g = Graph()
g.parse(ROOT / "examples/kathmandu-mini-abox.ttl", format="turtle")
abox_size = len(g)
g.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
DeductiveClosure(RDFS_Semantics).expand(g)
print(f"ABox {abox_size} triples + TBox, RDFS-closed: {len(g)} triples\n")

PFX = """PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""
BLIND_QUERIES = {
    "B1 attributed claims (entity, value, agent) -- prov terms only":
        PFX + """SELECT ?claim ?value ?agentLabel WHERE {
          ?claim a prov:Entity ; prov:value ?value ;
                 prov:wasAttributedTo ?agent .
          ?agent a prov:Agent ; rdfs:label ?agentLabel .
        } ORDER BY ?claim""",
    "B2 derivation: claim -> source document -- prov terms only":
        PFX + """SELECT ?claim ?srcLabel WHERE {
          ?claim a prov:Entity ; prov:value ?v ;
                 prov:wasDerivedFrom ?src .
          ?src a prov:Entity ; rdfs:label ?srcLabel .
        } ORDER BY ?claim""",
    "B3 full epistemic core (value, agent, source, time) -- prov terms only":
        PFX + """SELECT ?value ?agentLabel ?srcLabel ?t WHERE {
          ?claim a prov:Entity ; prov:value ?value ;
                 prov:wasAttributedTo ?agent ;
                 prov:wasDerivedFrom ?src ;
                 prov:generatedAtTime ?t .
          ?agent rdfs:label ?agentLabel . ?src rdfs:label ?srcLabel .
        } ORDER BY ?value""",
}
print("Consumer 1: vocabulary-blind SPARQL over the RDFS closure")
failures = []
for name, q in BLIND_QUERIES.items():
    rows = list(g.query(q))
    print(f"[{len(rows)} row(s)] {name}")
    for r in rows:
        print("   -> " + " | ".join(
            str(x).replace("https://w3id.org/heritagegraph/demo/", "")
            for x in r))
    if not rows:
        failures.append(name)
print()

# --- Stage 2: the reference PROV toolchain ---------------------------------
# PROV-visible projection: prov-namespace predicates, rdf:type into prov:,
# and labels for the nodes retained.
proj = Graph()
proj.bind("prov", PROV)
keep_nodes = set()
for s, p, o in g:
    if isinstance(p, URIRef) and str(p).startswith(str(PROV)):
        proj.add((s, p, o))
        keep_nodes.add(s)
        keep_nodes.add(o)
    elif p == RDF.type and isinstance(o, URIRef) and str(o).startswith(str(PROV)):
        proj.add((s, p, o))
        keep_nodes.add(s)
for n in keep_nodes:
    for lbl in g.objects(n, RDFS.label):
        proj.add((n, RDFS.label, lbl))
print(f"Consumer 2: reference `prov` library over the PROV projection "
      f"({len(proj)} triples)")

from prov.model import ProvDocument, ProvEntity, ProvAgent
from prov.model import ProvAttribution, ProvDerivation

with tempfile.NamedTemporaryFile(suffix=".ttl", mode="w", delete=False) as f:
    f.write(proj.serialize(format="turtle"))
    tmp = f.name
doc = ProvDocument.deserialize(source=tmp, format="rdf", rdf_format="turtle")

entities = list(doc.get_records(ProvEntity))
agents = list(doc.get_records(ProvAgent))
attributions = list(doc.get_records(ProvAttribution))
derivations = list(doc.get_records(ProvDerivation))
print(f"  ProvDocument parsed: {len(entities)} entities, {len(agents)} agents, "
      f"{len(attributions)} attributions, {len(derivations)} derivations")

# Traverse belief -> agent and belief -> source through the library's API.
attributed = {}
for rec in attributions:
    (_, entity_id), (_, agent_id) = rec.formal_attributes[:2]
    attributed[entity_id] = agent_id
derived = {}
for rec in derivations:
    (_, used_id), (_, source_id) = rec.formal_attributes[:2]
    derived.setdefault(used_id, []).append(source_id)

entity_ids = {e.identifier for e in entities}
agent_ids = {a.identifier for a in agents}
walked = 0
for belief_id, agent_id in sorted(attributed.items(), key=lambda kv: str(kv[0])):
    ok_agent = agent_id in agent_ids
    sources = derived.get(belief_id, [])
    ok_src = all(s in entity_ids for s in sources) and sources
    b = str(belief_id).replace("https://w3id.org/heritagegraph/demo/", "")
    a = str(agent_id).replace("https://w3id.org/heritagegraph/demo/", "")
    ss = [str(s).replace("https://w3id.org/heritagegraph/demo/", "")
          for s in sources]
    print(f"  walk {b} --wasAttributedTo--> {a} "
          f"[agent record: {ok_agent}] --wasDerivedFrom--> {ss} "
          f"[source records: {bool(ok_src)}]")
    if ok_agent and ok_src:
        walked += 1

expected_beliefs = 3   # Assert_BuildA, Assert_BuildB, Assert_RouteChange
if walked < expected_beliefs:
    failures.append(f"generic-consumer walk ({walked}/{expected_beliefs})")
print()
if failures:
    print(f"PROV-O INTEROP FAILED: {failures}")
    sys.exit(1)
print(f"PROV-O INTEROP PASSED: both consumers traverse all "
      f"{expected_beliefs} beliefs (attribution + derivation) without any "
      f"HeritageGraph vocabulary.")
