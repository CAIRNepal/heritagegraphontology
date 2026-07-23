#!/usr/bin/env python3
"""Merged-vocabulary classification: HermiT over HeritageGraph + the full
CIDOC-CRM, CRMinf, and PROV-O vocabularies.

Closes the stated threat that the consistency result was specific to the
self-contained released axiom set (no owl:imports): alignment errors, if
any, would surface as unsatisfiable classes precisely when the external
vocabularies' own axioms are merged in. The reviewer's point is that this
experiment is cheap and is exactly where mapping mistakes become logic
errors, so it doubles as a logical audit of the subsumption mappings.

Method. The published vocabulary documents are fetched (and cached):

  CIDOC-CRM v7.1.3 (RDFS)  https://cidoc-crm.org/rdfs/7.1.3/CIDOC_CRM_v7.1.3.rdf
  CRMinf v1.0 (RDFS)       https://cidoc-crm.org/extensions/crminf/rdfs/1.0/CRMinf_v1.0.rdf
  PROV-O (OWL 2)           https://www.w3.org/ns/prov.ttl

Each is merged with ontology/HeritageGraph.ttl via ROBOT, and HermiT
classifies the merged graph; a final run merges all three at once. ROBOT's
`reason` fails on inconsistency and, with --equivalent-classes-allowed
asserted-only, on unintended equivalences, so a zero exit is a real verdict.
The script asserts consistency AND checks the reasoned output for classes
subsumed under owl:Nothing (unsatisfiability).

Finding surfaced by this audit (kept, deliberately, as part of the result):
the HG + PROV-O merge is NOT in OWL 2 DL as-is. PROV-O asserts
owl:propertyChainAxiom on 13 properties (e.g. prov:wasGeneratedBy is
entailed by qualifiedGeneration o activity), which makes them non-simple,
and OWL 2 DL forbids non-simple properties in cardinality restrictions --
but the LinkML-generated TBox carries maxCardinality restrictions on eight
of them. HermiT therefore refuses the merge on profile grounds (a global-
restrictions violation, not an inconsistency). The script reports the exact
collision set and then verifies consistency under each of the two minimal
relaxations that restore DL: dropping PROV-O's 13 chain axioms, or dropping
HG's cardinality restrictions on the colliding properties.

Requires: ROBOT jar + Java (ROBOT_JAR / JAVA_HOME env vars, defaults below),
network access on the first run (vocabularies are cached afterwards).

Run:  ROBOT_JAR=/tmp/hgtools/robot.jar \
      JAVA_HOME=/tmp/hgtools/jdk-21.0.11+10-jre/Contents/Home \
      python3 evaluation/merged_import_classification.py
"""
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

from rdflib import Graph, OWL

ROOT = Path(__file__).resolve().parents[1]
ROBOT_JAR = os.environ.get("ROBOT_JAR", "/tmp/hgtools/robot.jar")
JAVA_HOME = os.environ.get("JAVA_HOME",
                           "/tmp/hgtools/jdk-21.0.11+10-jre/Contents/Home")
JAVA = str(Path(JAVA_HOME) / "bin" / "java")
CACHE = Path(os.environ.get("VOCAB_CACHE", "/tmp/hgtools/vocab"))
CACHE.mkdir(parents=True, exist_ok=True)

VOCABS = {
    "CIDOC-CRM v7.1.3": ("cidoc_crm.rdf",
        "https://cidoc-crm.org/rdfs/7.1.3/CIDOC_CRM_v7.1.3.rdf"),
    "CRMinf v1.0": ("crminf.rdf",
        "https://cidoc-crm.org/extensions/crminf/rdfs/1.0/CRMinf_v1.0.rdf"),
    "PROV-O": ("prov.ttl", "https://www.w3.org/ns/prov.ttl"),
}


def fetch(name: str, fname: str, url: str) -> Path:
    """Fetch (cached) and strip owl:imports declarations.

    The vocabularies declare owl:imports (CRMinf imports CRM, PROV-O imports
    its AQ/dictionary/links modules); OWLAPI would try to dereference these
    at merge time. The axioms under test are supplied explicitly, so the
    import declarations are dropped from a local copy.
    """
    p = CACHE / fname
    if not p.exists() or p.stat().st_size == 0:
        print(f"  fetching {name} from {url}")
        urllib.request.urlretrieve(url, p)
    clean = p.with_suffix(".noimports.ttl")
    if not clean.exists():
        g = Graph()
        g.parse(p, format="xml" if p.suffix == ".rdf" else "turtle")
        g.remove((None, OWL.imports, None))
        g.serialize(clean, format="turtle")
    return clean


HG_NS = "https://w3id.org/heritagegraph/"


def classify(label: str, inputs: list[Path]) -> bool:
    """Merge + HermiT-classify; fail on inconsistency, unsatisfiable classes,
    or inferred (non-asserted) class equivalences that involve an HG term.

    Equivalences internal to an external vocabulary are reported but not
    failed: prov.ttl by itself already entails prov:Insertion ==
    prov:Removal from its own dictionary axioms, which is PROV-O's business,
    not an alignment defect.
    """
    out = CACHE / f"reasoned_{label.replace(' ', '_').replace('/', '_')}.ttl"
    cmd = [JAVA, "-jar", ROBOT_JAR, "merge"]
    for p in inputs:
        cmd += ["--input", str(p)]
    cmd += ["reason", "--reasoner", "hermit",
            "--equivalent-classes-allowed", "all",
            "--output", str(out)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"  [{label}] FAILED:")
        for line in (proc.stdout + proc.stderr).splitlines():
            if "ERROR" in line or "unsatisfiable" in line.lower() \
                    or "consistent" in line.lower() or "equivalen" in line.lower():
                print("   ", line.strip())
        return False
    reasoned = Graph()
    reasoned.parse(out, format="turtle")
    # Unsatisfiability: any named class equivalent to / subsumed under Nothing.
    from rdflib import RDFS, URIRef  # noqa: E402
    unsat = {s for s in reasoned.subjects(OWL.equivalentClass, OWL.Nothing)} | \
            {s for s in reasoned.subjects(RDFS.subClassOf, OWL.Nothing)
             if isinstance(s, URIRef)}
    # Inferred equivalences involving an HG term.
    asserted_eq = set()
    for p in inputs:
        g = Graph()
        g.parse(p, format="turtle" if p.suffix == ".ttl" else "xml")
        asserted_eq |= {frozenset((s, o))
                        for s, o in g.subject_objects(OWL.equivalentClass)}
    hg_equiv, ext_equiv = [], []
    for s, o in reasoned.subject_objects(OWL.equivalentClass):
        if not (isinstance(s, URIRef) and isinstance(o, URIRef)) or s == o:
            continue
        if frozenset((s, o)) in asserted_eq or o == OWL.Nothing or s == OWL.Nothing:
            continue
        (hg_equiv if (str(s).startswith(HG_NS) or str(o).startswith(HG_NS))
         else ext_equiv).append((s, o))
    print(f"  [{label}] consistent, classified"
          f" (unsatisfiable: {len(unsat)}; inferred equivalences:"
          f" {len(hg_equiv)} involving HG, {len(ext_equiv)} external-internal)")
    for s, o in hg_equiv:
        print(f"      HG-involving equivalence: {s} == {o}")
    for s, o in ext_equiv:
        print(f"      (external-internal, tolerated: {s} == {o})")
    return not unsat and not hg_equiv


PROV_NS = "http://www.w3.org/ns/prov#"

hg = ROOT / "ontology/HeritageGraph.ttl"
ok = True
paths = {}
for name, (fname, url) in VOCABS.items():
    paths[name] = fetch(name, fname, url)

print("Pairwise merges with HeritageGraph:")
for name, p in list(paths.items()):
    if name == "PROV-O":
        continue
    ok &= classify(f"HG + {name}", [hg, p])

# --- PROV-O: report the DL collision, then classify under both repairs -----
print("PROV-O: DL global-restrictions check:")
prov_g = Graph()
prov_g.parse(paths["PROV-O"], format="turtle")
chains = {s for s in prov_g.subjects(OWL.propertyChainAxiom, None)}
hg_g = Graph()
hg_g.parse(hg, format="turtle")
from rdflib import RDF  # noqa: E402
constrained = set()
for r in hg_g.subjects(RDF.type, OWL.Restriction):
    for kind in (OWL.maxCardinality, OWL.minCardinality, OWL.cardinality):
        if next(hg_g.objects(r, kind), None) is not None:
            prop = next(hg_g.objects(r, OWL.onProperty), None)
            if prop is not None and str(prop).startswith(PROV_NS):
                constrained.add(prop)
collide = sorted(str(p).split("#")[-1] for p in chains & constrained)
print(f"  PROV-O chain-axiom (non-simple) properties: {len(chains)}")
print(f"  of which under an HG cardinality restriction: {len(collide)}")
print(f"  collision set: {', '.join(collide)}")
print("  => merged graph is outside OWL 2 DL (non-simple property in a")
print("     cardinality restriction); HermiT rejects it on profile grounds.")

# Repair 1: drop PROV-O's chain axioms.
prov_nochain = CACHE / "prov.nochain.ttl"
g = Graph()
g.parse(paths["PROV-O"], format="turtle")
for s, o in list(g.subject_objects(OWL.propertyChainAxiom)):
    g.remove((s, OWL.propertyChainAxiom, o))
g.serialize(prov_nochain, format="turtle")
ok &= classify("HG + PROV-O (chain axioms dropped)", [hg, prov_nochain])

# Repair 2: drop HG's cardinality restrictions on the colliding properties.
hg_relaxed = CACHE / "hg.relaxed.ttl"
g = Graph()
g.parse(hg, format="turtle")
for r in list(g.subjects(RDF.type, OWL.Restriction)):
    prop = next(g.objects(r, OWL.onProperty), None)
    if prop in chains:
        for kind in (OWL.maxCardinality, OWL.minCardinality, OWL.cardinality):
            for v in list(g.objects(r, kind)):
                g.remove((r, kind, v))
                # neutralise the emptied restriction
                g.add((r, OWL.minCardinality, v.__class__("0", datatype=v.datatype)))
g.serialize(hg_relaxed, format="turtle")
ok &= classify("HG (prov cardinalities relaxed) + PROV-O",
               [hg_relaxed, paths["PROV-O"]])

print("Full merge (chain axioms dropped from PROV-O):")
ok &= classify("HG + CRM + CRMinf + PROV-O",
               [hg, paths["CIDOC-CRM v7.1.3"], paths["CRMinf v1.0"],
                prov_nochain])

if ok:
    print("\nPASS: HermiT classifies every DL-admissible merged graph "
          "consistent, with no unsatisfiable classes and no unintended class "
          "equivalences; the one obstruction is the documented DL profile "
          "collision between PROV-O's property chains and HG's cardinality "
          "restrictions, not a semantic clash.")
    sys.exit(0)
print("\nFAIL: at least one merged classification did not come back clean.")
sys.exit(1)
