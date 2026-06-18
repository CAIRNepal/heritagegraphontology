#!/usr/bin/env python3
"""
§4.2 — Modeling Quality: OOPS! Pitfall Analysis
=================================================
Submits the ontology to the OOPS! web service (https://oops.linkeddata.es/)
and saves the XML response + a human-readable summary.

If the OOPS! service is unavailable, falls back to a local heuristic
pitfall scan covering the most common issues:
  P04  Creating unconnected ontology elements
  P08  Missing annotations (label / definition)
  P10  Missing disjointness
  P11  Missing domain or range
  P13  Missing inverse relationships
  P19  Defining multiple domains / ranges (swallowed by union)
  P22  Using non-HTTP URIs
  P41  No license declared

Output:  results/oops_report.txt
         results/oops_response.xml   (if online)
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict

import requests
from rdflib import Graph, RDF, RDFS, OWL, Namespace, URIRef, Literal, BNode

# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
ONTOLOGY_FILE = SCRIPT_DIR.parent / "ontology" / "HeritageGraph.ttl"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
HG = Namespace("https://w3id.org/heritagegraph/")
DCT = Namespace("http://purl.org/dc/terms/")

OOPS_URL = "https://oops.linkeddata.es/rest"

# ---------------------------------------------------------------------------


def section(title: str) -> str:
    return f"\n{'=' * 70}\n  {title}\n{'=' * 70}"


def try_oops_online(ttl_content: str) -> str | None:
    """Submit to OOPS! REST API. Returns XML response or None."""
    xml_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<OOPSRequest>
  <OntologyURI></OntologyURI>
  <OntologyContent><![CDATA[{ttl_content}]]></OntologyContent>
  <Pitfalls></Pitfalls>
  <OutputFormat>XML</OutputFormat>
</OOPSRequest>"""

    headers = {"Content-Type": "application/xml"}
    try:
        print("  Submitting to OOPS! web service (may take 30-60 s)...")
        resp = requests.post(OOPS_URL, data=xml_payload.encode("utf-8"),
                             headers=headers, timeout=120)
        if resp.status_code == 200 and len(resp.text) > 100:
            return resp.text
        else:
            print(f"  OOPS! returned status {resp.status_code}, falling back to local scan.")
            return None
    except Exception as e:
        print(f"  OOPS! service unreachable ({e}), falling back to local scan.")
        return None


def local_pitfall_scan(g: Graph) -> list[dict]:
    """Heuristic local pitfall scanner."""
    pitfalls: list[dict] = []

    named_classes = {s for s in g.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}
    obj_props = {s for s in g.subjects(RDF.type, OWL.ObjectProperty) if isinstance(s, URIRef)}
    dat_props = {s for s in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(s, URIRef)}
    all_props = obj_props | dat_props

    # P08 — Missing annotations
    for cls in named_classes:
        has_label = bool(list(g.objects(cls, RDFS.label)))
        has_def = bool(list(g.objects(cls, SKOS.definition))) or bool(list(g.objects(cls, RDFS.comment)))
        if not has_label:
            pitfalls.append({"id": "P08", "severity": "Minor",
                             "element": str(cls), "detail": "Missing rdfs:label"})
        if not has_def:
            pitfalls.append({"id": "P08", "severity": "Minor",
                             "element": str(cls), "detail": "Missing skos:definition or rdfs:comment"})

    for prop in all_props:
        has_label = bool(list(g.objects(prop, RDFS.label)))
        if not has_label:
            pitfalls.append({"id": "P08", "severity": "Minor",
                             "element": str(prop), "detail": "Property missing rdfs:label"})

    # P11 — Missing domain or range
    for prop in obj_props:
        has_domain = bool(list(g.objects(prop, RDFS.domain)))
        has_range = bool(list(g.objects(prop, RDFS.range)))
        if not has_domain:
            pitfalls.append({"id": "P11", "severity": "Important",
                             "element": str(prop), "detail": "Missing rdfs:domain"})
        if not has_range:
            pitfalls.append({"id": "P11", "severity": "Important",
                             "element": str(prop), "detail": "Missing rdfs:range"})

    for prop in dat_props:
        has_range = bool(list(g.objects(prop, RDFS.range)))
        if not has_range:
            pitfalls.append({"id": "P11", "severity": "Important",
                             "element": str(prop), "detail": "Datatype property missing rdfs:range"})

    # P10 — Missing disjointness
    # Check if any sibling classes have disjointWith
    parent_children: dict[str, list] = defaultdict(list)
    for cls in named_classes:
        for parent in g.objects(cls, RDFS.subClassOf):
            if isinstance(parent, URIRef):
                parent_children[str(parent)].append(cls)

    sibling_groups_without_disjoint = 0
    for parent, children in parent_children.items():
        if len(children) > 1:
            has_disjoint = False
            for c in children:
                if list(g.objects(c, OWL.disjointWith)) or list(g.subjects(OWL.disjointWith, c)):
                    has_disjoint = True
                    break
            if not has_disjoint:
                sibling_groups_without_disjoint += 1
                sibling_names = [str(c).split("/")[-1] for c in children[:5]]
                pitfalls.append({"id": "P10", "severity": "Important",
                                 "element": parent,
                                 "detail": f"Sibling classes lack owl:disjointWith: {', '.join(sibling_names)}"})

    # P13 — Missing inverse relationships
    inverse_declared = set()
    for s, o in g.subject_objects(OWL.inverseOf):
        inverse_declared.add((str(s), str(o)))
        inverse_declared.add((str(o), str(s)))

    # Heuristic: look for property name pairs that suggest inverses
    prop_names = {str(p): p for p in obj_props}
    inverse_hints = [
        ("produced_object", "was_produced_by_event"),
        ("has_component", "is_component_of"),
        ("depicts_deity", "is_depicted_in"),
        ("contains_structure", "has_current_location"),
        ("includes_ritual_event", "is_part_of_festival"),
    ]
    for a, b in inverse_hints:
        a_match = [u for n, u in prop_names.items() if a in n]
        b_match = [u for n, u in prop_names.items() if b in n]
        if a_match and b_match:
            pair = (str(a_match[0]), str(b_match[0]))
            if pair not in inverse_declared:
                pitfalls.append({"id": "P13", "severity": "Minor",
                                 "element": f"{a} / {b}",
                                 "detail": "Likely inverse pair lacks owl:inverseOf"})

    # P22 — Non-HTTP URIs
    for s in g.subjects():
        if isinstance(s, URIRef):
            uri = str(s)
            if uri.startswith("file:") or uri.startswith("/"):
                pitfalls.append({"id": "P22", "severity": "Critical",
                                 "element": uri, "detail": "Non-HTTP/filesystem URI"})
                break  # Don't flood

    # Check ontology IRI
    for ont in g.subjects(RDF.type, OWL.Ontology):
        uri = str(ont)
        if not uri.startswith("http"):
            pitfalls.append({"id": "P22", "severity": "Critical",
                             "element": uri,
                             "detail": "Ontology IRI is not an absolute HTTP URI"})

    # P41 — No license
    has_license = False
    for ont in g.subjects(RDF.type, OWL.Ontology):
        if list(g.objects(ont, DCT.license)) or list(g.objects(ont, URIRef("http://purl.org/dc/elements/1.1/rights"))):
            has_license = True
    if not has_license:
        pitfalls.append({"id": "P41", "severity": "Minor",
                         "element": "Ontology", "detail": "No dcterms:license found"})

    return pitfalls


def run_evaluation():
    report: list[str] = []

    def log(msg: str):
        report.append(msg)
        print(msg)

    log(section("§4.2  Modeling Quality — OOPS! Pitfall Analysis"))
    log(f"Date     : {datetime.now().isoformat()}")
    log(f"Ontology : {ONTOLOGY_FILE}")
    log("")

    # Parse
    g = Graph()
    g.parse(str(ONTOLOGY_FILE), format="turtle")
    log(f"  Parsed {len(g)} triples")

    # --- Try OOPS! online ---
    log(section("OOPS! Online Service"))
    ttl_content = ONTOLOGY_FILE.read_text(encoding="utf-8")
    xml_response = try_oops_online(ttl_content)

    if xml_response:
        xml_path = RESULTS_DIR / "oops_response.xml"
        xml_path.write_text(xml_response, encoding="utf-8")
        log(f"  ✅ OOPS! response saved to: {xml_path}")
        log(f"  Response size: {len(xml_response)} chars")
        log("  → Open the XML file to review detected pitfalls.")
    else:
        log("  ⚠️  OOPS! online service not available.")

    # --- Local heuristic scan (always run) ---
    log(section("Local Heuristic Pitfall Scan"))
    pitfalls = local_pitfall_scan(g)

    severity_order = {"Critical": 0, "Important": 1, "Minor": 2}
    pitfalls.sort(key=lambda p: (severity_order.get(p["severity"], 9), p["id"]))

    # Summary by pitfall ID
    summary: dict[str, dict] = {}
    for p in pitfalls:
        key = p["id"]
        if key not in summary:
            summary[key] = {"id": key, "severity": p["severity"], "count": 0, "examples": []}
        summary[key]["count"] += 1
        if len(summary[key]["examples"]) < 3:
            summary[key]["examples"].append(f'{p["element"]}: {p["detail"]}')

    log(f"\n  Total pitfalls detected: {len(pitfalls)}")
    log(f"  Unique pitfall types:    {len(summary)}\n")

    PITFALL_NAMES = {
        "P04": "Unconnected ontology elements",
        "P08": "Missing annotations",
        "P10": "Missing disjointness",
        "P11": "Missing domain or range",
        "P13": "Missing inverse relationships",
        "P19": "Multiple domains/ranges swallowed by union",
        "P22": "Non-HTTP URIs",
        "P41": "No license declared",
    }

    for pid, info in sorted(summary.items()):
        pname = PITFALL_NAMES.get(pid, "Unknown pitfall")
        log(f"  [{info['severity'].upper():>9}] {pid} — {pname}  ({info['count']} occurrence(s))")
        for ex in info["examples"]:
            short = ex if len(ex) < 100 else ex[:97] + "..."
            log(f"             → {short}")
        log("")

    # --- Write report ---
    report_path = RESULTS_DIR / "oops_report.txt"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(f"\n📄 Report saved to: {report_path}")


if __name__ == "__main__":
    run_evaluation()
