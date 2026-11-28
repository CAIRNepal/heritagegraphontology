#!/usr/bin/env python3
"""
§4.5 — Structural Completeness  &  §4.6 — Ontology Metrics
=============================================================
Computes:
  - Class count (HeritageGraph namespace + external)
  - Object property / datatype property counts
  - Union class count
  - Named individual count
  - Label coverage (rdfs:label)
  - Definition coverage (skos:definition or rdfs:comment)
  - Range coverage for properties
  - Domain coverage for properties
  - Class hierarchy depth

Output:  results/metrics_report.txt
         results/metrics_report.csv
"""

import csv
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from rdflib import Graph, RDF, RDFS, OWL, Namespace, URIRef, BNode

# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
ONTOLOGY_FILE = SCRIPT_DIR.parent / "ontology" / "HeritageGraph.ttl"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
HG = Namespace("https://cair-nepal.org/heritagegraph/")
LINKML = Namespace("https://w3id.org/linkml/")


def section(title: str) -> str:
    return f"\n{'=' * 70}\n  {title}\n{'=' * 70}"


def compute_hierarchy_depth(g, cls, visited=None):
    """Compute max depth of a class in the hierarchy."""
    if visited is None:
        visited = set()
    if cls in visited:
        return 0
    visited.add(cls)
    parents = [p for p in g.objects(cls, RDFS.subClassOf) if isinstance(p, URIRef)]
    if not parents:
        return 0
    return 1 + max(compute_hierarchy_depth(g, p, visited) for p in parents)


def run_evaluation():
    report: list[str] = []
    csv_rows: list[dict] = []

    def log(msg: str):
        report.append(msg)
        print(msg)

    def metric(name: str, value, note: str = ""):
        csv_rows.append({"metric": name, "value": str(value), "note": note})

    log(section("§4.5 / §4.6  Structural Completeness & Ontology Metrics"))
    log(f"Date     : {datetime.now().isoformat()}")
    log(f"Ontology : {ONTOLOGY_FILE}")
    log("")

    g = Graph()
    g.parse(str(ONTOLOGY_FILE), format="turtle")
    total_triples = len(g)
    log(f"  Total triples: {total_triples}")
    metric("total_triples", total_triples)

    # ──────────────────────────────────────────────────────────────────
    # §4.6 — Ontology Metrics
    # ──────────────────────────────────────────────────────────────────
    log(section("§4.6  Ontology Metrics"))

    # owl:deprecated stubs (1.0.x IRIs kept for backward compatibility, e.g.
    # the LinkML Container/Metadata terms) are excluded from every count
    deprecated = {s for s, o in g.subject_objects(OWL.deprecated)
                  if str(o).lower() == "true"}
    log(f"  Deprecated terms (excluded): {len(deprecated)}")
    metric("deprecated_terms_excluded", len(deprecated))

    # Named classes (exclude BNodes)
    all_named_classes = sorted(
        {s for s in g.subjects(RDF.type, OWL.Class)
         if isinstance(s, URIRef) and s not in deprecated},
        key=str
    )
    # HeritageGraph-namespace classes
    hg_classes = [c for c in all_named_classes if str(c).startswith(str(HG))]
    # External (CRM, PROV, etc.)
    ext_classes = [c for c in all_named_classes if not str(c).startswith(str(HG))]

    log(f"\n  Named classes (total)      : {len(all_named_classes)}")
    log(f"  HeritageGraph namespace    : {len(hg_classes)}")
    log(f"  External namespace classes : {len(ext_classes)}")
    metric("classes_total", len(all_named_classes))
    metric("classes_heritagegraph", len(hg_classes))
    metric("classes_external", len(ext_classes))

    # Object properties
    obj_props = sorted(
        {s for s in g.subjects(RDF.type, OWL.ObjectProperty)
         if isinstance(s, URIRef) and s not in deprecated},
        key=str
    )
    hg_obj = [p for p in obj_props if str(p).startswith(str(HG))]
    log(f"  Object properties          : {len(obj_props)} ({len(hg_obj)} HeritageGraph, "
        f"{len(obj_props) - len(hg_obj)} external)")
    metric("object_properties", len(obj_props))
    metric("object_properties_heritagegraph", len(hg_obj))
    metric("object_properties_external", len(obj_props) - len(hg_obj))

    # Datatype properties
    dat_props = sorted(
        {s for s in g.subjects(RDF.type, OWL.DatatypeProperty)
         if isinstance(s, URIRef) and s not in deprecated},
        key=str
    )
    hg_dat = [p for p in dat_props if str(p).startswith(str(HG))]
    log(f"  Datatype properties        : {len(dat_props)} ({len(hg_dat)} HeritageGraph, "
        f"{len(dat_props) - len(hg_dat)} external)")
    metric("datatype_properties", len(dat_props))
    metric("datatype_properties_heritagegraph", len(hg_dat))
    metric("datatype_properties_external", len(dat_props) - len(hg_dat))

    # Union classes — distinguish explicit union class definitions from enum encodings
    all_union_subjects = list(g.subjects(OWL.unionOf, None))

    # Named union classes: direct owl:unionOf or equivalentClass → unionOf pattern
    explicit_union_classes = []
    for cls in hg_classes:
        if list(g.objects(cls, OWL.unionOf)):
            explicit_union_classes.append(cls)
            continue
        for eq in g.objects(cls, OWL.equivalentClass):
            if isinstance(eq, BNode) and list(g.objects(eq, OWL.unionOf)):
                explicit_union_classes.append(cls)
                break

    # Enums and other unionOf uses
    enum_union_count = sum(1 for s in all_union_subjects
                          if isinstance(s, URIRef) and "Enum" in str(s).split("/")[-1])
    anon_union_count = sum(1 for s in all_union_subjects if isinstance(s, BNode))

    log(f"  Union classes (all unionOf): {len(all_union_subjects)}")
    log(f"    ├ Named union classes    : {len(explicit_union_classes)}")
    for uc in explicit_union_classes:
        log(f"    │   → {str(uc).split('/')[-1]}")
    log(f"    ├ Enum-as-union classes  : {enum_union_count}")
    log(f"    └ Anonymous union uses   : {anon_union_count}")
    metric("union_classes_total", len(all_union_subjects))
    metric("union_classes_named", len(explicit_union_classes), "Paper counts these")

    # Named individuals
    named_individuals = {s for s in g.subjects(RDF.type, OWL.NamedIndividual) if isinstance(s, URIRef)}
    log(f"  Named individuals          : {len(named_individuals)}")
    metric("named_individuals", len(named_individuals))

    # Annotation properties
    ann_props = {s for s in g.subjects(RDF.type, OWL.AnnotationProperty)
                 if isinstance(s, URIRef) and s not in deprecated}
    log(f"  Annotation properties      : {len(ann_props)}")
    metric("annotation_properties", len(ann_props))

    # ──────────────────────────────────────────────────────────────────
    # §4.5 — Structural Completeness
    # ──────────────────────────────────────────────────────────────────
    log(section("§4.5  Structural Completeness"))

    # Label coverage
    classes_with_label = [c for c in all_named_classes if list(g.objects(c, RDFS.label))]
    log(f"\n  Classes with rdfs:label            : {len(classes_with_label)}/{len(all_named_classes)}")
    metric("classes_with_label", f"{len(classes_with_label)}/{len(all_named_classes)}")

    # Definition coverage
    classes_with_def = [
        c for c in all_named_classes
        if list(g.objects(c, SKOS.definition)) or list(g.objects(c, RDFS.comment))
    ]
    log(f"  Classes with definition            : {len(classes_with_def)}/{len(all_named_classes)}")
    metric("classes_with_definition", f"{len(classes_with_def)}/{len(all_named_classes)}")

    # Classes missing definitions
    missing_def = [c for c in all_named_classes if c not in classes_with_def]
    if missing_def:
        log(f"\n  Classes MISSING definition ({len(missing_def)}):")
        for c in missing_def[:15]:
            short = str(c).split("/")[-1].split("#")[-1]
            log(f"    - {short}")
        if len(missing_def) > 15:
            log(f"    ... and {len(missing_def) - 15} more")

    # Property range coverage
    obj_with_range = [p for p in obj_props if list(g.objects(p, RDFS.range))]
    dat_with_range = [p for p in dat_props if list(g.objects(p, RDFS.range))]
    log(f"\n  Object props with rdfs:range       : {len(obj_with_range)}/{len(obj_props)}")
    log(f"  Datatype props with rdfs:range     : {len(dat_with_range)}/{len(dat_props)}")
    metric("obj_props_with_range", f"{len(obj_with_range)}/{len(obj_props)}")
    metric("dat_props_with_range", f"{len(dat_with_range)}/{len(dat_props)}")

    # Property domain coverage
    obj_with_domain = [p for p in obj_props if list(g.objects(p, RDFS.domain))]
    dat_with_domain = [p for p in dat_props if list(g.objects(p, RDFS.domain))]
    log(f"  Object props with rdfs:domain      : {len(obj_with_domain)}/{len(obj_props)}")
    log(f"  Datatype props with rdfs:domain    : {len(dat_with_domain)}/{len(dat_props)}")
    metric("obj_props_with_domain", f"{len(obj_with_domain)}/{len(obj_props)}")
    metric("dat_props_with_domain", f"{len(dat_with_domain)}/{len(dat_props)}")

    # Properties with labels
    props_with_label = [p for p in (obj_props + dat_props) if list(g.objects(p, RDFS.label))]
    total_props = len(obj_props) + len(dat_props)
    log(f"  Properties with rdfs:label         : {len(props_with_label)}/{total_props}")
    metric("props_with_label", f"{len(props_with_label)}/{total_props}")

    # ──────────────────────────────────────────────────────────────────
    # Class Hierarchy Analysis
    # ──────────────────────────────────────────────────────────────────
    log(section("Class Hierarchy Analysis"))

    # Root classes (no named superclass)
    roots = []
    for cls in hg_classes:
        named_parents = [p for p in g.objects(cls, RDFS.subClassOf) if isinstance(p, URIRef)]
        if not named_parents:
            roots.append(cls)

    log(f"\n  Root classes (no named parent): {len(roots)}")
    for r in roots[:20]:
        short = str(r).split("/")[-1]
        log(f"    - {short}")

    # Max hierarchy depth
    max_depth = 0
    deepest_class = None
    for cls in hg_classes:
        d = compute_hierarchy_depth(g, cls)
        if d > max_depth:
            max_depth = d
            deepest_class = cls
    log(f"\n  Max hierarchy depth: {max_depth}")
    if deepest_class:
        log(f"  Deepest class: {str(deepest_class).split('/')[-1]}")
    metric("max_hierarchy_depth", max_depth)

    # Subclass count per parent
    parent_children: dict[str, int] = defaultdict(int)
    for cls in hg_classes:
        for parent in g.objects(cls, RDFS.subClassOf):
            if isinstance(parent, URIRef):
                parent_children[str(parent).split("/")[-1]] += 1

    if parent_children:
        log(f"\n  Classes with subclasses:")
        for parent, count in sorted(parent_children.items(), key=lambda x: -x[1])[:15]:
            log(f"    {parent:<40} {count} subclass(es)")

    # ──────────────────────────────────────────────────────────────────
    # Full class list
    # ──────────────────────────────────────────────────────────────────
    log(section("Full Class List (HeritageGraph namespace)"))
    for i, cls in enumerate(hg_classes, 1):
        short = str(cls).split("/")[-1]
        has_label = "✅" if cls in classes_with_label else "❌"
        has_def = "✅" if cls in classes_with_def else "❌"
        log(f"  {i:>3}. {short:<40} label:{has_label}  def:{has_def}")

    # No hard-coded "paper claims" table: the live numbers go to
    # results/metrics.json, which the paper should read instead of restating
    # numbers by hand (a stale literal cannot then contradict the artefact).
    import json as _json
    shapes = Graph()
    shapes.parse(SCRIPT_DIR.parent / "ontology" / "HeritageGraph.shacl.ttl", format="turtle")
    SHNS = "http://www.w3.org/ns/shacl#"
    enum_classes = {c for c in g.subjects(OWL.oneOf, None) if str(c).startswith(str(HG))}
    live = {
        "classes_heritagegraph": len([c for c in hg_classes if c not in enum_classes]),
        "enumerations_heritagegraph": len(enum_classes),
        "classes_external": len(ext_classes),
        "object_properties_heritagegraph": len(hg_obj),
        "object_properties_external": len(obj_props) - len(hg_obj),
        "datatype_properties_heritagegraph": len(hg_dat),
        "datatype_properties_external": len(dat_props) - len(hg_dat),
        "union_classes": len(explicit_union_classes),
        "named_individuals": len(named_individuals),
        "shacl_node_shapes": len(set(shapes.subjects(RDF.type, URIRef(SHNS + "NodeShape")))),
        "owl_triples": len(g),
    }
    (RESULTS_DIR / "metrics.json").write_text(_json.dumps(live, indent=2) + "\n", encoding="utf-8")
    log(section("Live metrics (results/metrics.json)"))
    for k, v in live.items():
        log(f"  {k:<36} {v:>6}")

    # Write outputs
    report_path = RESULTS_DIR / "metrics_report.txt"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(f"\n📄 Report saved to: {report_path}")

    csv_path = RESULTS_DIR / "metrics_report.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["metric", "value", "note"])
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"📊 CSV saved to:    {csv_path}")


if __name__ == "__main__":
    run_evaluation()
