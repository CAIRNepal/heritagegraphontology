#!/usr/bin/env python3
"""Generate the LUX/CIDOC-CRM interoperability evaluation artefacts for the paper.

Produces (in evaluation/lux/):
  coverage_E1.csv          — every external class instantiated in LUX + HG-target flag
  migration_counts_E3.csv  — per-HG-class instance counts in the migrated graph
  crm_mapping.csv          — HG <-> CIDOC-CRM equivalentClass / equivalentProperty axioms
  LUX_EVALUATION.md        — headline numbers + markdown tables (paper-ready)

Tier-2 evaluation (alignment-specific). Tier-1 (core ontology) lives in evaluation/run_*.py.

Coverage (E1) is decided LOCALLY against this repository's core ontology plus
the bridge module: an external class C instantiated in LUX is covered if the
core reuses C directly (declares it as a class) or some HeritageGraph class is
rdfs:subClassOf+ / owl:equivalentClass C in core + module. The endpoint only
supplies per-class instance counts (E1) and the migrated graph (E3).

Usage:
  python evaluation/lux/generate_lux_eval.py            # live endpoint
  python evaluation/lux/generate_lux_eval.py --offline  # instance counts from the
                                                        # committed coverage_E1.csv /
                                                        # migration_counts_E3.csv snapshot
"""
from __future__ import annotations
import argparse, csv, json, ssl, sys, urllib.parse, urllib.request
from pathlib import Path

from rdflib import Graph, OWL, RDF, RDFS, URIRef

# macOS Python.framework ships without a CA bundle; use certifi if present,
# else fall back to an unverified context (the endpoint is a public, read-only store).
try:
    import certifi
    _SSL = ssl.create_default_context(cafile=certifi.where())
except Exception:
    _SSL = ssl._create_unverified_context()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CORE = ROOT / "ontology" / "HeritageGraph.ttl"
BRIDGE = ROOT / "heritagegraph-lux-migration" / "alignment" / "heritagegraph-lux-alignment.ttl"
ENDPOINT = "https://semihyumusak.com.tr/oxigraph/query"
HG = "https://cair-nepal.org/heritagegraph/"
CRM = "http://www.cidoc-crm.org/cidoc-crm/"
NAMESPACES = {
    "hg:": HG, "crm:": CRM,
    "sci:": "http://www.ics.forth.gr/isl/CRMsci/",   # as in the Linked Art context LUX is serialised with
    "dig:": "http://www.ics.forth.gr/isl/CRMdig/",
    "la:": "https://linked.art/ns/terms/",
}
# Types the migrated graph on the endpoint carries from the pre-1.0.0 module
# (aliases of classes the v1.0.0 core reuses directly) -> v1.0.0 class.
LEGACY_TYPES = {
    "hg:Person": "crm:E21_Person",
    "hg:Place": "crm:E53_Place",
    "hg:HumanMadeObject": "crm:E22_Human-Made_Object",
}


def short(u: str) -> str:
    for p, ns in NAMESPACES.items():
        if u.startswith(ns):
            return p + u[len(ns):]
    return u


def expand(c: str) -> URIRef:
    for p, ns in NAMESPACES.items():
        if c.startswith(p):
            return URIRef(ns + c[len(p):])
    return URIRef(c)


def sparql(query: str) -> list[dict]:
    data = urllib.parse.urlencode({"query": query}).encode()
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Accept": "application/sparql-results+json",
                 "Content-Type": "application/x-www-form-urlencoded",
                 "User-Agent": "curl/8.4 (heritagegraph-eval)"})
    with urllib.request.urlopen(req, timeout=120, context=_SSL) as r:
        return json.load(r)["results"]["bindings"]


def instance_counts(offline: bool) -> list[tuple[str, int]]:
    if offline:
        with (HERE / "coverage_E1.csv").open() as f:
            return [(r["lux_class"], int(r["instances"])) for r in csv.DictReader(f)]
    rows = sparql("""
SELECT ?c (COUNT(?x) AS ?n)
WHERE { ?x a ?c .
  FILTER(STRSTARTS(STR(?c),"http://www.cidoc-crm.org/cidoc-crm/")
    || STRSTARTS(STR(?c),"http://www.ics.forth.gr/isl/CRMdig/")
    || STRSTARTS(STR(?c),"http://www.ics.forth.gr/isl/CRMsci/")
    || STRSTARTS(STR(?c),"https://linked.art/ns/terms/")) }
GROUP BY ?c ORDER BY DESC(?n)""")
    return [(short(b["c"]["value"]), int(b["n"]["value"])) for b in rows]


def e3_counts(offline: bool) -> list[tuple[str, int]]:
    if offline:
        with (HERE / "migration_counts_E3.csv").open() as f:
            return [(LEGACY_TYPES.get(r["v1_class"], r["v1_class"]), int(r["instances"]))
                    for r in csv.DictReader(f)]
    rows = sparql("""SELECT ?t (COUNT(?s) AS ?n) WHERE {
      GRAPH <https://cair-nepal.org/heritagegraph/imported/lux> { ?s a ?t } }
      GROUP BY ?t ORDER BY DESC(?n)""")
    return [(LEGACY_TYPES.get(short(b["t"]["value"]), short(b["t"]["value"])),
             int(b["n"]["value"])) for b in rows]


def covered(graph: Graph, core: Graph, cls: URIRef) -> bool:
    """Directly reused by the core, or reached from an HG class via
    rdfs:subClassOf+ / owl:equivalentClass in core + module."""
    if (cls, RDF.type, OWL.Class) in core:
        return True
    seen, todo = set(), [cls]
    while todo:
        c = todo.pop()
        if c in seen:
            continue
        seen.add(c)
        for s in graph.subjects(RDFS.subClassOf, c):
            todo.append(s)
        for s in list(graph.subjects(OWL.equivalentClass, c)) + list(graph.objects(c, OWL.equivalentClass)):
            todo.append(s)
    return any(str(c).startswith(HG) for c in seen - {cls})


def module_stats(bridge: Graph, core: Graph) -> dict:
    count = lambda p: len(list(bridge.subject_objects(p)))
    return {
        "triples": len(bridge),
        "equivalentClass": count(OWL.equivalentClass),
        "equivalentProperty": count(OWL.equivalentProperty),
        "subClassOf": count(RDFS.subClassOf),
        "subPropertyOf": count(RDFS.subPropertyOf),
        "crm_reused_by_core": sorted(short(str(c)) for c in core.subjects(RDF.type, OWL.Class)
                                     if str(c).startswith(CRM)),
    }


def write_csv(path: Path, header: list[str], rows: list[tuple]):
    with path.open("w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--offline", action="store_true",
                    help="take instance counts from the committed snapshot CSVs")
    args = ap.parse_args()

    core = Graph().parse(str(CORE), format="turtle")
    bridge = Graph().parse(str(BRIDGE), format="turtle")
    merged = core + bridge

    counts = instance_counts(args.offline)
    cov = [(c, n, "YES" if covered(merged, core, expand(c)) else "NO") for c, n in counts]
    e3 = e3_counts(args.offline)
    eqc = sorted((short(str(s)), short(str(o))) for s, o in bridge.subject_objects(OWL.equivalentClass))
    eqp = sorted((short(str(s)), short(str(o))) for s, o in bridge.subject_objects(OWL.equivalentProperty))
    stats = module_stats(bridge, core)

    write_csv(HERE / "coverage_E1.csv", ["lux_class", "instances", "covered"], cov)
    write_csv(HERE / "migration_counts_E3.csv", ["v1_class", "instances"], e3)
    write_csv(HERE / "crm_mapping.csv", ["hg_term", "axiom", "crm_term"],
              [(s, "equivalentClass", o) for s, o in eqc] + [(s, "equivalentProperty", o) for s, o in eqp])

    n_cls = len(cov); n_cov = sum(1 for _, _, c in cov if c == "YES")
    inst = sum(n for _, n, _ in cov); inst_cov = sum(n for _, n, c in cov if c == "YES")
    migrated = sum(n for _, n in e3)
    source = ("the committed snapshot of the live endpoint" if args.offline
              else f"the live endpoint `{ENDPOINT}`")

    L = []
    L.append("# LUX / CIDOC-CRM Interoperability Evaluation (Tier 2)\n")
    L.append("Auto-generated by `evaluation/lux/generate_lux_eval.py`. Instance counts come from "
             f"{source}; coverage is decided locally against `ontology/HeritageGraph.ttl` + "
             "`heritagegraph-lux-migration/alignment/heritagegraph-lux-alignment.ttl`.\n")
    L.append("## Headline results\n")
    L.append(f"- **E1 Coverage:** {n_cov}/{n_cls} external (CIDOC-CRM/CRMdig/CRMsci/Linked-Art) "
             f"class types instantiated in LUX have a HeritageGraph target "
             f"(**{100*n_cov/n_cls:.1f}%**); **{inst_cov:,}/{inst:,}** typed instances covered "
             f"(**{100*inst_cov/inst:.2f}%**).")
    L.append(f"- **E3 Migration:** {migrated:,} LUX records re-typed into {len(e3)} HeritageGraph classes "
             "in graph `…/imported/lux`.")
    L.append(f"- **E4 Mapping:** {stats['equivalentClass']} `owl:equivalentClass` + "
             f"{stats['equivalentProperty']} `owl:equivalentProperty` axioms to CIDOC-CRM.")
    L.append(f"- **Module:** {stats['triples']} triples; {stats['subClassOf']} `rdfs:subClassOf`, "
             f"{stats['subPropertyOf']} `rdfs:subPropertyOf`. The core reuses "
             f"{len(stats['crm_reused_by_core'])} CIDOC-CRM class IRIs directly "
             f"({', '.join(stats['crm_reused_by_core'])}).\n")

    L.append("## E1 — Coverage of external classes present in LUX\n")
    L.append("| LUX class (instantiated) | Instances | HG target |")
    L.append("|---|--:|:--:|")
    for c, n, cv in cov:
        L.append(f"| `{c}` | {n:,} | {cv} |")

    L.append("\n## E3 — Migrated instances per HeritageGraph class\n")
    L.append("| v1.0.0 class | Instances |")
    L.append("|---|--:|")
    for c, n in e3:
        L.append(f"| `{c}` | {n:,} |")
    L.append(f"| **total** | **{migrated:,}** |")
    L.append("\nThe migrated graph on the endpoint was produced with the pre-1.0.0 module, "
             "which typed persons, places, and human-made objects with HeritageGraph aliases "
             "of the CIDOC-CRM classes the v1.0.0 core reuses directly; they are reported here "
             "under the v1.0.0 class.")

    L.append("\n## E4 — HeritageGraph ↔ CIDOC-CRM equivalence axioms\n")
    L.append("| HeritageGraph term | Axiom | CIDOC-CRM term |")
    L.append("|---|---|---|")
    for s, o in eqc:
        L.append(f"| `{s}` | equivalentClass | `{o}` |")
    for s, o in eqp:
        L.append(f"| `{s}` | equivalentProperty | `{o}` |")
    (HERE / "LUX_EVALUATION.md").write_text("\n".join(L) + "\n")

    print(f"wrote: coverage_E1.csv ({n_cls} rows), migration_counts_E3.csv ({len(e3)} rows), "
          f"crm_mapping.csv ({len(eqc)+len(eqp)} rows), LUX_EVALUATION.md")
    print(f"E1 coverage: {n_cov}/{n_cls} class types ({100*n_cov/n_cls:.1f}%), "
          f"{inst_cov:,}/{inst:,} instances ({100*inst_cov/inst:.2f}%) | E3 migrated: {migrated:,}")
    print(f"module: {stats['triples']} triples, {stats['equivalentClass']} equivalentClass, "
          f"{stats['equivalentProperty']} equivalentProperty, {stats['subClassOf']} subClassOf, "
          f"{stats['subPropertyOf']} subPropertyOf; core reuses "
          f"{len(stats['crm_reused_by_core'])} CRM classes directly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
