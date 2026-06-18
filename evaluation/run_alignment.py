#!/usr/bin/env python3
"""
§4.4 — Alignment and Interoperability
=======================================
Counts and lists:
  - Classes aligned to CIDOC-CRM (via class_uri / skos:exactMatch / rdfs:subClassOf)
  - Properties aligned to CIDOC-CRM (via slot_uri from LinkML YAML source)
  - Properties aligned to PROV-O
  - Other vocabulary alignments (schema.org, AAT, Wikidata, DBpedia, DataCite)

Two-source strategy:
  1. HeritageGraph.ttl — OWL axioms (subClassOf, exactMatch, etc.)
  2. HeritageGraph.yaml — LinkML source (class_uri, slot_uri mappings that are
     NOT emitted as OWL triples in the generated TTL)

Output:  results/alignment_report.txt
         results/alignment_report.csv
"""

import csv
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from rdflib import Graph, RDF, RDFS, OWL, Namespace, URIRef

# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
ONTOLOGY_FILE = SCRIPT_DIR.parent / "ontology" / "HeritageGraph.ttl"
YAML_FILE = SCRIPT_DIR.parent / "ontology" / "HeritageGraph.yaml"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
HG = Namespace("https://w3id.org/heritagegraph/")

# External namespace prefixes to check (in generated TTL)
NAMESPACES = {
    "CIDOC-CRM": "http://www.cidoc-crm.org/cidoc-crm/",
    "CRMsci": "http://www.cidoc-crm.org/crmsci/",
    "CRMdig": "http://www.cidoc-crm.org/crmdig/",
    "CRMinf": "http://www.cidoc-crm.org/crminf/",
    "PROV-O": "http://www.w3.org/ns/prov#",
    "schema.org": "https://schema.org/",
    "AAT": "http://vocab.getty.edu/aat/",
    "Wikidata": "http://www.wikidata.org/entity/",
    "DBpedia": "http://dbpedia.org/ontology/",
    "RICO": "https://www.ica.org/standards/RiC/ontology#",
    "GeoSPARQL": "http://www.opengis.net/ont/geosparql#",
    "OWL-Time": "http://www.w3.org/2006/time#",
    "DataCite": "http://purl.org/spar/datacite/",
    "DCTerms": "http://purl.org/dc/terms/",
    "FOAF": "http://xmlns.com/foaf/0.1/",
    "EDM": "http://www.europeana.eu/schemas/edm/",
}

# Mapping from YAML CURIE prefixes to canonical namespace names
CURIE_PREFIX_MAP = {
    "crm": "CIDOC-CRM",
    "crmsci": "CRMsci",
    "crmdig": "CRMdig",
    "crminf": "CRMinf",
    "prov": "PROV-O",
    "schema": "schema.org",
    "aat": "AAT",
    "wd": "Wikidata",
    "dbo": "DBpedia",
    "rico": "RICO",
    "geo": "GeoSPARQL",
    "time": "OWL-Time",
    "datacite": "DataCite",
    "dcterms": "DCTerms",
    "foaf": "FOAF",
    "edm": "EDM",
    "rdfs": "RDFS",
}


def section(title: str) -> str:
    return f"\n{'=' * 70}\n  {title}\n{'=' * 70}"


# ---------------------------------------------------------------------------
#  Parse LinkML YAML for class_uri / slot_uri mappings
# ---------------------------------------------------------------------------
def parse_yaml_alignments(yaml_path: Path) -> tuple[
    dict[str, list[tuple[str, str]]],   # class_name → [(ns_name, curie)]
    dict[str, list[tuple[str, str]]],   # slot_name → [(ns_name, curie)]
]:
    """
    Lightweight YAML parser that extracts class_uri and slot_uri values.
    We avoid pulling in pyyaml by doing simple regex parsing since the
    structure is predictable LinkML YAML.
    """
    class_alignments: dict[str, list[tuple[str, str]]] = defaultdict(list)
    slot_alignments: dict[str, list[tuple[str, str]]] = defaultdict(list)

    text = yaml_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    current_section = None  # "classes" or "slots"
    current_name = None
    indent_level = 0

    for line in lines:
        stripped = line.strip()

        # Top-level section detection
        if line.startswith("classes:"):
            current_section = "classes"
            current_name = None
            continue
        elif line.startswith("slots:"):
            current_section = "slots"
            current_name = None
            continue
        elif line.startswith("enums:") or line.startswith("prefixes:") or line.startswith("id:"):
            current_section = None
            current_name = None
            continue

        if current_section is None:
            continue

        # Detect class/slot name (2-space indented, ending with colon)
        m = re.match(r"^  (\w[\w\s]*\w|\w+):\s*$", line)
        if m:
            current_name = m.group(1).strip()
            continue

        if current_name is None:
            continue

        # Detect class_uri or slot_uri
        if current_section == "classes":
            m = re.match(r"^\s+class_uri:\s*(\S+)", line)
            if m:
                curie = m.group(1)
                prefix = curie.split(":")[0]
                ns_name = CURIE_PREFIX_MAP.get(prefix)
                if ns_name:
                    class_alignments[current_name].append((ns_name, curie))

        elif current_section == "slots":
            m = re.match(r"^\s+slot_uri:\s*(\S+)", line)
            if m:
                curie = m.group(1)
                prefix = curie.split(":")[0]
                ns_name = CURIE_PREFIX_MAP.get(prefix)
                if ns_name:
                    slot_alignments[current_name].append((ns_name, curie))

    return class_alignments, slot_alignments


def run_evaluation():
    report: list[str] = []
    csv_rows: list[dict] = []

    def log(msg: str):
        report.append(msg)
        print(msg)

    log(section("§4.4  Alignment & Interoperability"))
    log(f"Date     : {datetime.now().isoformat()}")
    log(f"Ontology : {ONTOLOGY_FILE}")
    log(f"YAML src : {YAML_FILE}")
    log("")

    # ── Load TTL ──────────────────────────────────────────────────────────
    g = Graph()
    g.parse(str(ONTOLOGY_FILE), format="turtle")
    log(f"  Parsed {len(g)} triples from TTL")

    # ── Load YAML alignments ─────────────────────────────────────────────
    yaml_class_align, yaml_slot_align = parse_yaml_alignments(YAML_FILE)
    log(f"  Parsed {sum(len(v) for v in yaml_class_align.values())} class_uri "
        f"and {sum(len(v) for v in yaml_slot_align.values())} slot_uri "
        f"mappings from YAML\n")

    # Collect all named classes and properties from TTL
    named_classes = {s for s in g.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}
    obj_props = {s for s in g.subjects(RDF.type, OWL.ObjectProperty) if isinstance(s, URIRef)}
    dat_props = {s for s in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(s, URIRef)}

    # ──────────────────────────────────────────────────────────────────────
    # 1. Class Alignments  (TTL axioms + YAML class_uri)
    # ──────────────────────────────────────────────────────────────────────
    log(section("1. Class Alignments (TTL axioms + YAML class_uri)"))

    alignment_predicates = [
        RDFS.subClassOf,
        SKOS.exactMatch,
        SKOS.closeMatch,
        SKOS.broadMatch,
        SKOS.narrowMatch,
        OWL.equivalentClass,
    ]

    class_alignments: dict[str, list[tuple[str, str, str]]] = defaultdict(list)

    # 1a. From TTL: classes whose URI is in an external namespace
    for cls in named_classes:
        uri = str(cls)
        for ns_name, ns_uri in NAMESPACES.items():
            if uri.startswith(ns_uri):
                class_alignments[ns_name].append((uri, "class_uri", uri))

        # From TTL: alignment predicates
        for pred in alignment_predicates:
            for obj in g.objects(cls, pred):
                if isinstance(obj, URIRef):
                    obj_uri = str(obj)
                    for ns_name, ns_uri in NAMESPACES.items():
                        if obj_uri.startswith(ns_uri):
                            pred_short = str(pred).split("/")[-1].split("#")[-1]
                            class_alignments[ns_name].append((uri, pred_short, obj_uri))

        # From TTL: skos:exactMatch
        for obj in g.objects(cls, SKOS.exactMatch):
            if isinstance(obj, URIRef):
                obj_uri = str(obj)
                for ns_name, ns_uri in NAMESPACES.items():
                    if obj_uri.startswith(ns_uri):
                        class_alignments[ns_name].append((uri, "skos:exactMatch", obj_uri))

    # 1b. From YAML: class_uri mappings
    for cls_name, mappings in yaml_class_align.items():
        hg_uri = str(HG) + cls_name
        for ns_name, curie in mappings:
            class_alignments[ns_name].append((hg_uri, "class_uri(YAML)", curie))

    for ns_name in sorted(class_alignments.keys()):
        items = class_alignments[ns_name]
        unique = list(set(items))
        unique_classes = set(i[0] for i in unique)
        log(f"\n  {ns_name}: {len(unique_classes)} class(es) aligned")
        for cls_uri, pred, target in sorted(unique)[:25]:
            short_cls = cls_uri.split("/")[-1].split("#")[-1]
            short_target = target.split("/")[-1].split("#")[-1]
            log(f"    {short_cls:<35} → {pred:<20} → {short_target}")
            csv_rows.append({
                "type": "class", "element": cls_uri, "predicate": pred,
                "target": target, "namespace": ns_name,
            })

    # ──────────────────────────────────────────────────────────────────────
    # 2. Property Alignments  (TTL URIs + YAML slot_uri)
    # ──────────────────────────────────────────────────────────────────────
    log(section("2. Property Alignments (TTL + YAML slot_uri)"))

    # slot_name → (ns_name, curie, prop_type)
    prop_alignments: dict[str, list[tuple[str, str, str]]] = defaultdict(list)

    # 2a. From TTL: properties whose URI is in an external namespace
    all_props = obj_props | dat_props
    for prop in all_props:
        uri = str(prop)
        for ns_name, ns_uri in NAMESPACES.items():
            if uri.startswith(ns_uri):
                prop_type = "ObjectProperty" if prop in obj_props else "DatatypeProperty"
                prop_alignments[ns_name].append((uri, uri, prop_type))

    # 2b. From YAML: slot_uri mappings (the primary source of truth)
    for slot_name, mappings in yaml_slot_align.items():
        hg_uri = str(HG) + slot_name
        # Determine property type from TTL
        prop_type = "ObjectProperty" if URIRef(hg_uri) in obj_props else (
            "DatatypeProperty" if URIRef(hg_uri) in dat_props else "Unknown"
        )
        for ns_name, curie in mappings:
            prop_alignments[ns_name].append((slot_name, curie, prop_type))

    for ns_name in sorted(prop_alignments.keys()):
        items = prop_alignments[ns_name]
        unique = list(set(items))
        log(f"\n  {ns_name}: {len(unique)} propert(ies) aligned")
        for slot_name, curie, prop_type in sorted(unique):
            log(f"    {slot_name:<40} → {curie:<30} ({prop_type})")
            csv_rows.append({
                "type": "property", "element": slot_name, "predicate": "slot_uri",
                "target": curie, "namespace": ns_name,
            })

    # ──────────────────────────────────────────────────────────────────────
    # 3. Summary Table
    # ──────────────────────────────────────────────────────────────────────
    log(section("3. Alignment Summary"))

    all_ns_classes = {}
    for ns_name, items in class_alignments.items():
        all_ns_classes[ns_name] = len(set(i[0] for i in items))

    all_ns_props = {}
    for ns_name, items in prop_alignments.items():
        all_ns_props[ns_name] = len(set(i[0] for i in items))

    all_ns = sorted(set(list(all_ns_classes.keys()) + list(all_ns_props.keys())))
    log(f"\n  {'Namespace':<20} {'Classes':>10} {'Properties':>12}")
    log(f"  {'-' * 44}")
    total_c = 0
    total_p = 0
    for ns in all_ns:
        c = all_ns_classes.get(ns, 0)
        p = all_ns_props.get(ns, 0)
        total_c += c
        total_p += p
        log(f"  {ns:<20} {c:>10} {p:>12}")
    log(f"  {'-' * 44}")
    log(f"  {'TOTAL':<20} {total_c:>10} {total_p:>12}")

    # Paper claims vs actual
    crm_c = all_ns_classes.get("CIDOC-CRM", 0)
    crm_ext_c = crm_c + all_ns_classes.get("CRMinf", 0) + all_ns_classes.get("CRMsci", 0)
    crm_p = all_ns_props.get("CIDOC-CRM", 0)
    prov_p = all_ns_props.get("PROV-O", 0)

    log(f"\n  Paper §4.4 claims vs Actual:")
    log(f"    {'Metric':<40} {'Paper':>8} {'Actual':>8}  {'Match':>6}")
    log(f"    {'-' * 64}")
    ext_subclass = sum(
        1 for s, o in g.subject_objects(RDFS.subClassOf)
        if isinstance(s, URIRef) and str(s).startswith(str(HG))
        and isinstance(o, URIRef) and not str(o).startswith(str(HG))
        and "owl#" not in str(o)
    )
    rows = [
        ("CIDOC-CRM aligned classes (SKOS/slot)", 32, crm_c),
        ("External rdfs:subClassOf axioms (TTL)", 31, ext_subclass),
        ("CRM-family (CRM+CRMinf+CRMsci) classes", 35, crm_ext_c),
        ("CIDOC-CRM aligned properties (slot_uri)", 42, crm_p),
        ("PROV-O aligned properties (slot_uri)", 9, prov_p),
    ]
    for label, paper, actual in rows:
        match = "✅" if paper == actual else "❌"
        log(f"    {label:<40} {paper:>8} {actual:>8}  {match:>6}")

    # Write outputs
    report_path = RESULTS_DIR / "alignment_report.txt"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(f"\n📄 Report saved to: {report_path}")

    csv_path = RESULTS_DIR / "alignment_report.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["type", "element", "predicate", "target", "namespace"])
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"📊 CSV saved to:    {csv_path}")


if __name__ == "__main__":
    run_evaluation()
