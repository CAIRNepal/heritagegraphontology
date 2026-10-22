#!/usr/bin/env python3
"""Reasoning robustness probes for HeritageGraph (ROBOT + HermiT).

Consolidates two §7.1 reasoning experiments behind one CLI. Both require a
ROBOT jar and a Java runtime; paths come from the ROBOT_JAR and JAVA_HOME
environment variables (defaults below), and merged-import needs network access
on the first run (vocabularies are cached afterwards).

Subcommands (default: all):

  entailments     Classify the released ontology with HermiT and print the number
                  of asserted rdfs:subClassOf axioms and of inferred subsumptions
                  between named classes (excluding owl:Thing).

  injection       Inconsistency injection: show the OWL axioms bite rather than
                  decorate. Three arms: (A) a KumariTenure with two
                  owl:differentFrom embodiedDeity values must clash with the
                  max-1 restriction; (B) the same ABox without differentFrom
                  stays consistent (the names co-denote); (C) an individual
                  typed both hg:Stupa and hg:Chaitya (the one owl:disjointWith
                  pair) must be unsatisfiable.

  merged-import   Merged-vocabulary classification: HermiT over HeritageGraph +
                  the full CIDOC-CRM, CRMinf, CRMsci, and PROV-O vocabularies, closing
                  the threat that consistency was specific to the self-contained
                  released axiom set. Reports the documented PROV-O property-
                  chain vs. HG-cardinality DL collision and classifies under
                  both minimal repairs.

  no-external-superclass  Core + LUX module + CIDOC-CRM (+ CRMinf, CRMsci) must not give
                  an external class a HeritageGraph superclass, or an enumeration
                  individual an extra HeritageGraph type.

  tenure-not-event  The same merge plus the demonstrator ABox must not infer that a
                  KumariTenure is a crm:E5_Event.

  lux-conservativity  Probe instances of every class/property pair the LUX module maps,
                  classified with the module and CIDOC-CRM, must not be typed against
                  CRM's disjointness (E2/E77 stated; E18/E28 from the scope notes) or
                  with a core class that core + CIDOC-CRM alone do not entail.

Run:  ROBOT_JAR=/tmp/hgtools/robot.jar \\
      JAVA_HOME=/tmp/hgtools/jdk-21.0.11+10-jre/Contents/Home \\
      python3 evaluation/reasoning_extras.py [injection|merged-import|all]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
import urllib.request
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, URIRef
from rdflib.collection import Collection

ROOT = Path(__file__).resolve().parents[1]
ROBOT_JAR = os.environ.get("ROBOT_JAR", "/tmp/hgtools/robot.jar")
JAVA_HOME = os.environ.get("JAVA_HOME",
                           "/tmp/hgtools/jdk-21.0.11+10-jre/Contents/Home")
JAVA = str(Path(JAVA_HOME) / "bin" / "java")


# ===========================================================================
# injection: the OWL axioms are load-bearing.
# ===========================================================================
def run_injection() -> int:
    COMMON = """@prefix hg:  <https://cair-nepal.org/heritagegraph/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:  <https://cair-nepal.org/heritagegraph/example/> .

# The declaration is required so that the OWLAPI Turtle parser reads the
# embodiment triples as ObjectPropertyAssertions; undeclared predicates are
# parsed as annotations, which HermiT ignores.
hg:embodiedDeity a owl:ObjectProperty .

ex:T a hg:KumariTenure , owl:NamedIndividual ; rdfs:label "injected tenure" ;
    hg:embodiedDeity ex:D1 , ex:D2 .
ex:D1 a hg:Deity , owl:NamedIndividual ; rdfs:label "deity one" .
ex:D2 a hg:Deity , owl:NamedIndividual ; rdfs:label "deity two" .
"""
    DIFFERENT = "ex:D1 owl:differentFrom ex:D2 .\n"

    DISJOINT_JOINT = """@prefix hg:  <https://cair-nepal.org/heritagegraph/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:  <https://cair-nepal.org/heritagegraph/example/> .

ex:J a hg:Stupa , hg:Chaitya , owl:NamedIndividual ;
    rdfs:label "joint Stupa-and-Chaitya individual" .
"""

    def hermit_verdict(abox_ttl: str) -> tuple[bool, str]:
        """Merge the ontology with the injected ABox and classify with HermiT.

        Returns (consistent, evidence_line)."""
        with tempfile.TemporaryDirectory() as td:
            abox = Path(td) / "inject.ttl"
            abox.write_text(abox_ttl)
            out = Path(td) / "reasoned.ttl"
            proc = subprocess.run(
                [JAVA, "-jar", ROBOT_JAR, "merge",
                 "--input", str(ROOT / "ontology/HeritageGraph.ttl"),
                 "--input", str(abox),
                 "reason", "--reasoner", "hermit", "--output", str(out)],
                capture_output=True, text=True)
            text = proc.stdout + proc.stderr
            if proc.returncode == 0:
                return True, "classified without error"
            for line in text.splitlines():
                if "consistent" in line.lower() or "unsatisfiable" in line.lower():
                    return False, line.strip()
            return False, text.strip().splitlines()[-1] if text.strip() else "non-zero exit"

    print("Arm A: two embodiedDeity values + owl:differentFrom (expect INCONSISTENT)")
    consistent, evidence = hermit_verdict(COMMON + DIFFERENT)
    print(f"  HermiT: {'CONSISTENT' if consistent else 'INCONSISTENT'} -- {evidence}")
    arm_a_ok = not consistent

    print("Arm B: same ABox without owl:differentFrom (control; expect CONSISTENT)")
    consistent, evidence = hermit_verdict(COMMON)
    print(f"  HermiT: {'CONSISTENT' if consistent else 'INCONSISTENT'} -- {evidence}")
    arm_b_ok = consistent

    print("Arm C: joint Stupa-and-Chaitya individual (expect INCONSISTENT)")
    consistent, evidence = hermit_verdict(DISJOINT_JOINT)
    print(f"  HermiT: {'CONSISTENT' if consistent else 'INCONSISTENT'} -- {evidence}")
    arm_c_ok = not consistent

    if arm_a_ok and arm_b_ok and arm_c_ok:
        print("\nPASS: the max-1 embodiment axiom is load-bearing (arm A clashes), the")
        print("control confirms the clash is driven by distinctness, not by the mere")
        print("presence of two property values (arm B merges the names), and the")
        print("asserted disjointness pair likewise bites (arm C clashes).")
        return 0
    print("\nFAIL: unexpected verdict in at least one arm.")
    return 1


# ===========================================================================
# merged-import: HermiT over HG + CIDOC-CRM + CRMinf + CRMsci + PROV-O.
# ===========================================================================
HG_NS = "https://cair-nepal.org/heritagegraph/"
PROV_NS = "http://www.w3.org/ns/prov#"
CACHE = Path(os.environ.get("VOCAB_CACHE", "/tmp/hgtools/vocab"))

VOCABS = {
    "CIDOC-CRM v7.1.3": ("cidoc_crm.rdf",
        "https://cidoc-crm.org/rdfs/7.1.3/CIDOC_CRM_v7.1.3.rdf"),
    "CRMinf v1.0": ("crminf.rdf",
        "https://cidoc-crm.org/extensions/crminf/rdfs/1.0/CRMinf_v1.0.rdf"),
    "CRMsci v2.0": ("crmsci.rdf",
        "https://cidoc-crm.org/extensions/crmsci/rdfs/2.0/CRMsci_v2.0.rdf"),
    "PROV-O": ("prov.ttl", "https://www.w3.org/ns/prov.ttl"),
}

# Namespace each vocabulary document declares its terms in. A merge only tests
# the alignment if HG's terms in that namespace are the very terms the
# document declares; _coverage() checks this before classifying.
VOCAB_NS = {
    "CIDOC-CRM v7.1.3": "http://www.cidoc-crm.org/cidoc-crm/",
    "CRMinf v1.0": "http://www.cidoc-crm.org/extensions/crminf/",
    "CRMsci v2.0": "http://www.cidoc-crm.org/extensions/crmsci/",
    "PROV-O": PROV_NS,
}


def _fetch(name: str, fname: str, url: str) -> Path:
    """Fetch (cached) and strip owl:imports declarations.

    The vocabularies declare owl:imports (CRMinf imports CRM, PROV-O imports
    its AQ/dictionary/links modules); OWLAPI would try to dereference these
    at merge time. The axioms under test are supplied explicitly, so the
    import declarations are dropped from a local copy.
    """
    p = CACHE / fname
    if not p.exists() or p.stat().st_size == 0:
        print(f"  fetching {name} from {url}")
        try:
            import certifi, ssl
            ctx = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            ctx = None
        with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
            p.write_bytes(r.read())
    clean = p.with_suffix(".noimports.ttl")
    if not clean.exists():
        g = Graph()
        g.parse(p, format="xml" if p.suffix == ".rdf" else "turtle")
        g.remove((None, OWL.imports, None))
        g.serialize(clean, format="turtle")
    return clean


def _classify(label: str, inputs: list[Path]) -> bool:
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


def _coverage(name: str, hg_path: Path, vocab_path: Path) -> bool:
    """HG terms in the vocabulary's namespace that the loaded document declares.

    Fails if HG uses no term in that namespace, or a term the document does
    not declare: either way the merge would classify HG's terms in isolation
    (e.g. after a namespace mismatch) and test nothing about the alignment."""
    ns = VOCAB_NS[name]
    hg_g = Graph()
    hg_g.parse(hg_path, format="turtle")
    used = {t for triple in hg_g for t in triple
            if isinstance(t, URIRef) and str(t).startswith(ns) and str(t) != ns}
    v = Graph()
    v.parse(vocab_path, format="turtle")
    declared = {s for s in v.subjects(RDF.type, None) if isinstance(s, URIRef)}
    missing = sorted(str(t)[len(ns):] for t in used - declared)
    print(f"  [{name}] HG terms in {ns}: {len(used)}; declared by the loaded "
          f"document: {len(used) - len(missing)}"
          + (f"; NOT declared: {', '.join(missing)}" if missing else ""))
    return bool(used) and not missing


def run_merged_import() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    hg = ROOT / "ontology/HeritageGraph.ttl"
    ok = True
    paths = {}
    for name, (fname, url) in VOCABS.items():
        paths[name] = _fetch(name, fname, url)

    print("Term coverage (does each merge load the terms HG actually uses?):")
    for name, p in paths.items():
        ok &= _coverage(name, hg, p)

    print("Pairwise merges with HeritageGraph:")
    for name, p in list(paths.items()):
        if name == "PROV-O":
            continue
        ok &= _classify(f"HG + {name}", [hg, p])

    # --- PROV-O: report the DL collision, then classify under both repairs ---
    print("PROV-O: DL global-restrictions check:")
    prov_g = Graph()
    prov_g.parse(paths["PROV-O"], format="turtle")
    chains = {s for s in prov_g.subjects(OWL.propertyChainAxiom, None)}
    hg_g = Graph()
    hg_g.parse(hg, format="turtle")
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
    ok &= _classify("HG + PROV-O (chain axioms dropped)", [hg, prov_nochain])

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
    ok &= _classify("HG (prov cardinalities relaxed) + PROV-O",
                    [hg_relaxed, paths["PROV-O"]])

    print("Full merge (chain axioms dropped from PROV-O):")
    ok &= _classify("HG + CRM + CRMinf + CRMsci + PROV-O",
                    [hg, paths["CIDOC-CRM v7.1.3"], paths["CRMinf v1.0"],
                     paths["CRMsci v2.0"], prov_nochain])

    if ok:
        print("\nPASS: HermiT classifies every DL-admissible merged graph "
              "consistent, with no unsatisfiable classes and no unintended class "
              "equivalences; the one obstruction is the documented DL profile "
              "collision between PROV-O's property chains and HG's cardinality "
              "restrictions, not a semantic clash.")
        return 0
    print("\nFAIL: at least one merged classification did not come back clean.")
    return 1


# ===========================================================================
# entailments: what HermiT adds to the released axiom set.
# ===========================================================================
def run_entailments() -> int:
    """Classify the released ontology with HermiT (ROBOT reason, imports
    stripped) and count subsumptions. "Asserted rdfs:subClassOf axioms" counts
    every rdfs:subClassOf triple in the file (including those whose superclass
    is a restriction or class expression); the entailment count is the named
    class pairs (both sides IRIs) in ROBOT's reasoned output that are not
    asserted, excluding the trivial C rdfs:subClassOf owl:Thing."""
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "hg.ttl"
        out = Path(td) / "reasoned.ttl"
        g = Graph()
        g.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
        g.remove((None, OWL.imports, None))
        g.serialize(src, format="turtle")
        proc = subprocess.run([JAVA, "-jar", ROBOT_JAR, "reason", "--reasoner", "hermit",
                               "--input", str(src), "--output", str(out)],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            print("HermiT: ontology is inconsistent or has unsatisfiable classes")
            return 1
        reasoned = Graph()
        reasoned.parse(out, format="turtle")

    def named(graph: Graph) -> set:
        return {(s, o) for s, o in graph.subject_objects(RDFS.subClassOf)
                if isinstance(s, URIRef) and isinstance(o, URIRef) and s != o}

    asserted_all = len(list(g.subject_objects(RDFS.subClassOf)))
    new = named(reasoned) - named(g)
    thing = sorted(s for s, o in new if o == OWL.Thing)
    inferred = sorted((s, o) for s, o in new if o != OWL.Thing)
    print(f"Asserted rdfs:subClassOf axioms: {asserted_all} "
          f"(of which between named classes: {len(named(g))})")
    print(f"Inferred subsumptions between named classes (excluding owl:Thing): {len(inferred)}")
    print(f"  (plus {len(thing)} trivial C rdfs:subClassOf owl:Thing, not counted)")
    for s, o in inferred:
        print(f"    {str(s).rsplit('/', 1)[-1]}  rdfs:subClassOf  {str(o).rsplit('/', 1)[-1]}")
    return 0


# ===========================================================================
# no-external-superclass: HeritageGraph must not redefine external terms.
# ===========================================================================
LUX_MODULE = ROOT / "heritagegraph-lux-migration" / "alignment" / "heritagegraph-lux-alignment.ttl"
EXTERNAL_CLASS_NS = (
    "http://www.cidoc-crm.org/cidoc-crm/",
    "http://www.cidoc-crm.org/extensions/",
    "http://www.w3.org/ns/prov#",
    "https://linked.art/ns/terms/",
    "http://www.ics.forth.gr/isl/CRMdig/",
)


def _hijacks(extra_ttl: str = "") -> tuple[list[str], int, int]:
    """Classify core + LUX module + CIDOC-CRM 7.1.3 + CRMinf + CRMsci with
    HermiT (subclass and class-assertion inferences) and return the
    violations: an external class with a HeritageGraph superclass, or an
    enumeration individual with a HeritageGraph type other than its own
    enumeration class. Also returns the numbers of external classes and
    enumeration individuals examined."""
    paths = [_fetch(n, *VOCABS[n]) for n in ("CIDOC-CRM v7.1.3", "CRMinf v1.0", "CRMsci v2.0")]
    core = Graph()
    core.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
    enum_members: dict[URIRef, set[URIRef]] = {}
    for cls, lst in core.subject_objects(OWL.oneOf):
        for ind in Collection(core, lst):
            enum_members.setdefault(ind, set()).add(cls)
    with tempfile.TemporaryDirectory() as td:
        merged = Graph()
        for p in [ROOT / "ontology/HeritageGraph.ttl", LUX_MODULE] + paths:
            merged.parse(p, format="turtle")
        if extra_ttl:
            merged.parse(data=extra_ttl, format="turtle")
        merged.remove((None, OWL.imports, None))
        src, out = Path(td) / "merged.ttl", Path(td) / "reasoned.ttl"
        merged.serialize(src, format="turtle")
        proc = subprocess.run([JAVA, "-jar", ROBOT_JAR, "reason", "--reasoner", "hermit",
                               "--equivalent-classes-allowed", "all",
                               "--axiom-generators", "SubClass EquivalentClass ClassAssertion",
                               "--input", str(src), "--output", str(out)],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            return [f"merged graph not classifiable: {proc.stdout[-300:]}{proc.stderr[-300:]}"], 0, 0
        reasoned = Graph()
        reasoned.parse(out, format="turtle")
    # transitive named-class closure over asserted + inferred axioms
    sup: dict[URIRef, set[URIRef]] = {}
    for g in (merged, reasoned):
        for s, o in g.subject_objects(RDFS.subClassOf):
            if isinstance(s, URIRef) and isinstance(o, URIRef):
                sup.setdefault(s, set()).add(o)
        for s, o in g.subject_objects(OWL.equivalentClass):
            if isinstance(s, URIRef) and isinstance(o, URIRef):
                sup.setdefault(s, set()).add(o); sup.setdefault(o, set()).add(s)

    def ancestors(c: URIRef) -> set[URIRef]:
        seen, todo = set(), [c]
        while todo:
            x = todo.pop()
            for y in sup.get(x, ()):
                if y not in seen:
                    seen.add(y); todo.append(y)
        return seen - {c}

    hg = lambda u: str(u).startswith(HG_NS)
    violations = []
    ext_classes = {c for g in (merged, reasoned) for c in g.subjects(RDF.type, OWL.Class)
                   if isinstance(c, URIRef) and str(c).startswith(EXTERNAL_CLASS_NS)}
    for c in sorted(ext_classes):
        bad = sorted(str(a) for a in ancestors(c) if hg(a))
        if bad:
            violations.append(f"{c} has HeritageGraph superclass(es): {', '.join(bad)}")
    for ind, own in sorted(enum_members.items()):
        types = {t for g in (merged, reasoned) for t in g.objects(ind, RDF.type) if isinstance(t, URIRef)}
        hg_types = {t for t in types | {a for t in types for a in ancestors(t)} if hg(t)}
        bad = sorted(str(t) for t in hg_types - own)
        if bad:
            violations.append(f"enumeration individual {ind} gains HeritageGraph type(s): {', '.join(bad)}")
    return violations, len(ext_classes), len(enum_members)


def run_no_external_superclass() -> int:
    """Fail if core + LUX module + CIDOC-CRM 7.1.3 (+ CRMinf, CRMsci) entail
    that an external class gains a HeritageGraph superclass or that an
    enumeration individual gains a HeritageGraph type beyond its own
    enumeration; a negative control re-injects Deity ≡ crm:E28_Conceptual_Object
    and must be caught."""
    CACHE.mkdir(parents=True, exist_ok=True)
    violations, n_cls, n_ind = _hijacks()
    print(f"core + LUX module + CIDOC-CRM 7.1.3 + CRMinf + CRMsci, classified with HermiT: "
          f"{n_cls} external classes, {n_ind} enumeration individuals examined")
    for v in violations:
        print("  VIOLATION:", v)
    control, _, _ = _hijacks(
        "<https://cair-nepal.org/heritagegraph/Deity> "
        "<http://www.w3.org/2002/07/owl#equivalentClass> "
        "<http://www.cidoc-crm.org/cidoc-crm/E28_Conceptual_Object> .")
    caught = any("E28_Conceptual_Object" in v or "E55_Type" in v for v in control)
    print(f"negative control (Deity ≡ crm:E28_Conceptual_Object): "
          f"{len(control)} violation(s) -> {'caught' if caught else 'NOT caught'}")
    if violations or not caught:
        print("FAIL")
        return 1
    print("PASS: no external class gains a HeritageGraph superclass and no enumeration "
          "individual gains a HeritageGraph type beyond its own enumeration.")
    return 0


# ===========================================================================
# tenure-not-event: KumariTenure stays a period, not a crm:E5_Event.
# ===========================================================================
E5_EVENT = URIRef("http://www.cidoc-crm.org/cidoc-crm/E5_Event")
KUMARI_TENURE = URIRef(HG_NS + "KumariTenure")
TENURE_PROBE = URIRef(HG_NS + "example/ProbeTenure")


def _tenure_events(extra_ttl: str = "") -> tuple[list[str], int]:
    """Classify core + LUX module + CIDOC-CRM 7.1.3 + CRMinf + CRMsci + the
    demonstrator ABox + one probe tenure that uses every property the core
    restricts on KumariTenure, and return the KumariTenure individuals (and
    the class itself) that HermiT infers to be crm:E5_Event, plus the number
    of tenure individuals examined."""
    paths = [_fetch(n, *VOCABS[n]) for n in ("CIDOC-CRM v7.1.3", "CRMinf v1.0", "CRMsci v2.0")]
    with tempfile.TemporaryDirectory() as td:
        merged = Graph()
        for p in [ROOT / "ontology/HeritageGraph.ttl", LUX_MODULE,
                  ROOT / "examples/kathmandu-mini-abox.ttl"] + paths:
            merged.parse(p, format="turtle")
        # the probe tenure: one fresh value for every restricted property
        props = {merged.value(r, OWL.onProperty) for r in merged.objects(KUMARI_TENURE, RDFS.subClassOf)
                 if (r, RDF.type, OWL.Restriction) in merged}
        merged.add((TENURE_PROBE, RDF.type, KUMARI_TENURE))
        for i, prop in enumerate(sorted(p for p in props if p is not None)):
            if (prop, RDF.type, OWL.ObjectProperty) in merged:
                merged.add((TENURE_PROBE, prop, URIRef(f"{TENURE_PROBE}_v{i}")))
        if extra_ttl:
            merged.parse(data=extra_ttl, format="turtle")
        merged.remove((None, OWL.imports, None))
        src, out = Path(td) / "merged.ttl", Path(td) / "reasoned.ttl"
        merged.serialize(src, format="turtle")
        proc = subprocess.run([JAVA, "-jar", ROBOT_JAR, "reason", "--reasoner", "hermit",
                               "--equivalent-classes-allowed", "all", "--include-indirect", "true",
                               "--axiom-generators", "SubClass ClassAssertion",
                               "--input", str(src), "--output", str(out)],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            return [f"merged graph not classifiable: {proc.stdout[-300:]}{proc.stderr[-300:]}"], 0
        reasoned = Graph()
        reasoned.parse(out, format="turtle")
    tenures = sorted(set(merged.subjects(RDF.type, KUMARI_TENURE)))
    bad = [f"{t} inferred crm:E5_Event" for t in tenures if (t, RDF.type, E5_EVENT) in reasoned]
    if (KUMARI_TENURE, RDFS.subClassOf, E5_EVENT) in reasoned:
        bad.append(f"{KUMARI_TENURE} inferred rdfs:subClassOf crm:E5_Event")
    return bad, len(tenures)


def run_tenure_not_event() -> int:
    """Fail if the merged classification types a KumariTenure as crm:E5_Event
    (the paper broad-matches it to crm:E4_Period deliberately); a negative
    control re-injects hadParticipant ≡ crm:P11_had_participant (domain E5)
    and must be caught."""
    CACHE.mkdir(parents=True, exist_ok=True)
    violations, n = _tenure_events()
    print(f"core + LUX module + CIDOC-CRM 7.1.3 + CRMinf + CRMsci + demonstrator, classified with "
          f"HermiT: {n} KumariTenure individual(s) examined (incl. a probe using every restricted property)")
    for v in violations:
        print("  VIOLATION:", v)
    control, _ = _tenure_events(
        f"<{HG_NS}hadParticipant> <http://www.w3.org/2002/07/owl#equivalentProperty> "
        "<http://www.cidoc-crm.org/cidoc-crm/P11_had_participant> .")
    caught = bool(control)
    print(f"negative control (hadParticipant ≡ crm:P11_had_participant): "
          f"{len(control)} violation(s) -> {'caught' if caught else 'NOT caught'}")
    if violations or not caught:
        print("FAIL")
        return 1
    print("PASS: no KumariTenure is inferred to be a crm:E5_Event.")
    return 0


# ===========================================================================
# lux-conservativity: the LUX module must not give HeritageGraph data CRM
# types that contradict CIDOC-CRM or the core ontology.
# ===========================================================================
CRM_NS = "http://www.cidoc-crm.org/cidoc-crm/"
E2, E77, E18, E28 = (URIRef(CRM_NS + c) for c in
                     ("E2_Temporal_Entity", "E77_Persistent_Item", "E18_Physical_Thing", "E28_Conceptual_Object"))
PROBE_NS = HG_NS + "example/lux-probe/"


def _lux_probe_abox(module: Graph) -> tuple[Graph, dict]:
    """One subject/object pair per (class, slot) whose property the module maps
    to an external property, plus one per module-declared property with an
    rdfs:domain/rdfs:range. Subjects are typed with the class, objects with the
    slot range (or the property range)."""
    from linkml_runtime import SchemaView
    mapped = {s for p in (OWL.equivalentProperty, RDFS.subPropertyOf)
              for s, o in module.subject_objects(p)
              if str(s).startswith(HG_NS) and not str(o).startswith(HG_NS)}
    sv = SchemaView(str(ROOT / "ontology/HeritageGraph.yaml"))
    abox, where = Graph(), {}
    i = 0
    for c in sv.all_classes():
        c_iri = URIRef(sv.get_uri(sv.get_class(c), expand=True))
        for s in sv.class_induced_slots(c):
            prop = URIRef(sv.get_uri(s, expand=True))
            if prop not in mapped:
                continue
            i += 1
            subj, obj = URIRef(f"{PROBE_NS}s{i}"), URIRef(f"{PROBE_NS}o{i}")
            abox.add((subj, RDF.type, c_iri)); abox.add((subj, prop, obj))
            if s.range in sv.all_classes():
                abox.add((obj, RDF.type, URIRef(sv.get_uri(sv.get_class(s.range), expand=True))))
            where[subj] = f"{c} {s.name} (subject)"; where[obj] = f"{c} {s.name} (object, range {s.range})"
    for prop in mapped:
        dom, rng = module.value(prop, RDFS.domain), module.value(prop, RDFS.range)
        if dom is None and rng is None:
            continue
        i += 1
        subj, obj = URIRef(f"{PROBE_NS}s{i}"), URIRef(f"{PROBE_NS}o{i}")
        abox.add((subj, prop, obj))
        if isinstance(dom, URIRef): abox.add((subj, RDF.type, dom))
        if isinstance(rng, URIRef): abox.add((obj, RDF.type, rng))
        n = str(prop)[len(HG_NS):]
        where[subj] = f"{n} (subject)"; where[obj] = f"{n} (object)"
    return abox, where


def _reason_types(graphs: list, abox: Graph) -> dict:
    with tempfile.TemporaryDirectory() as td:
        merged = Graph()
        for p in graphs:
            merged.parse(p, format="turtle") if isinstance(p, Path) else merged.__iadd__(p)
        merged += abox
        merged.remove((None, OWL.imports, None))
        src, out = Path(td) / "merged.ttl", Path(td) / "reasoned.ttl"
        merged.serialize(src, format="turtle")
        proc = subprocess.run([JAVA, "-jar", ROBOT_JAR, "reason", "--reasoner", "hermit",
                               "--equivalent-classes-allowed", "all", "--include-indirect", "true",
                               "--axiom-generators", "ClassAssertion",
                               "--input", str(src), "--output", str(out)],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"not classifiable: {proc.stdout[-300:]}{proc.stderr[-300:]}")
        reasoned = Graph(); reasoned.parse(out, format="turtle")
    return {x: {t for g in (merged, reasoned) for t in g.objects(x, RDF.type) if isinstance(t, URIRef)}
            for x in set(abox.subjects())}


def _lux_violations(module: Graph) -> tuple[list[str], int]:
    """C1 stated disjointness (E2 scope note: E2 Temporal Entity is disjoint from
    E77 Persistent Item); C2 scope-note definitions (E18 physical vs E28
    non-material); C3 conservativity w.r.t. the core (no class declared by the
    core is entailed for an instance unless core + CIDOC-CRM already entail it)."""
    vocabs = [_fetch(n, *VOCABS[n]) for n in ("CIDOC-CRM v7.1.3", "CRMinf v1.0", "CRMsci v2.0")]
    core_ttl = ROOT / "ontology/HeritageGraph.ttl"
    core = Graph(); core.parse(core_ttl, format="turtle")
    core_classes = {c for c in core.subjects(RDF.type, OWL.Class) if isinstance(c, URIRef)}
    abox, where = _lux_probe_abox(module)
    base = _reason_types([core_ttl] + vocabs, abox)
    full = _reason_types([core_ttl, module] + vocabs, abox)
    out = []
    for x, types in full.items():
        if x not in where:
            continue
        if E2 in types and E77 in types:
            out.append(f"C1 {where[x]}: both crm:E2_Temporal_Entity and crm:E77_Persistent_Item")
        if E18 in types and E28 in types:
            out.append(f"C2 {where[x]}: both crm:E18_Physical_Thing and crm:E28_Conceptual_Object")
        asserted = set(abox.objects(x, RDF.type))
        if asserted and asserted <= core_classes:   # C3 concerns instances of core classes only
            for t in sorted((types - base.get(x, set())) & core_classes):
                out.append(f"C3 {where[x]}: gains core class {t}")
    return sorted(set(out)), len(where)


def run_lux_conservativity() -> int:
    """Fail if the LUX module, loaded with CIDOC-CRM (+ CRMinf, CRMsci), types
    probe instances of HeritageGraph classes against CIDOC-CRM's disjointness
    (C1, C2) or with core classes the core does not entail (C3); a negative
    control re-adds documentedBy ⊑ crm:P94i_was_created_by and must be caught."""
    CACHE.mkdir(parents=True, exist_ok=True)
    module = Graph(); module.parse(LUX_MODULE, format="turtle")
    violations, n = _lux_violations(module)
    print(f"LUX module + core + CIDOC-CRM 7.1.3 + CRMinf + CRMsci, HermiT: {n} probe instances "
          f"(every mapped class/property pair)")
    for v in violations:
        print("  VIOLATION:", v)
    control = Graph(); control += module
    control.add((URIRef(HG_NS + "documentedBy"), RDFS.subPropertyOf,
                 URIRef(CRM_NS + "P94i_was_created_by")))
    c_viol, _ = _lux_violations(control)
    caught = len(c_viol) > len(violations)
    print(f"negative control (documentedBy ⊑ crm:P94i_was_created_by): "
          f"{len(c_viol) - len(violations)} additional violation(s) -> {'caught' if caught else 'NOT caught'}")
    if violations or not caught:
        print("FAIL")
        return 1
    print("PASS: the LUX module assigns no CRM type that contradicts CIDOC-CRM's disjointness "
          "and no core class the core does not entail.")
    return 0


PROBES = {
    "injection": run_injection,
    "merged-import": run_merged_import,
    "entailments": run_entailments,
    "no-external-superclass": run_no_external_superclass,
    "tenure-not-event": run_tenure_not_event,
    "lux-conservativity": run_lux_conservativity,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("probe", nargs="?", default="all",
                        choices=list(PROBES) + ["all"],
                        help="which probe to run (default: all)")
    args = parser.parse_args()

    if args.probe != "all":
        return PROBES[args.probe]()

    failures = []
    for name, fn in PROBES.items():
        print(f"\n{'=' * 78}\n== {name}\n{'=' * 78}")
        try:
            if fn() not in (0, None):
                failures.append(name)
        except Exception as exc:
            failures.append(name)
            print(f"[{name}] FAILED: {exc}")
    print(f"\n{'=' * 78}")
    if failures:
        print(f"FAILED probes: {', '.join(failures)}")
        return 1
    print("All reasoning probes passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
