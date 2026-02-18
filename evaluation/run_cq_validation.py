#!/usr/bin/env python3
"""
§4.3 & §4.7 — Competency-Question Validation & Traceability Matrix
====================================================================
Loads all CQ SPARQL ASK queries from queries/cq_queries.py,
runs each against HeritageGraph.ttl (TBox-only), and produces:

  results/cq_validation_report.txt   — human-readable pass/fail
  results/cq_validation_report.csv   — machine-readable results
  results/cq_traceability_matrix.csv — full CQ → ontology-element mapping

No instance data required — queries check schema-level elements only.
"""

import csv
import time
from datetime import datetime
from pathlib import Path

from rdflib import Graph

# ---------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
ONTOLOGY_FILE = SCRIPT_DIR.parent / "HeritageGraph.ttl"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Common SPARQL prefixes
# ---------------------------------------------------------------------------
PREFIXES = """
PREFIX heritageGraph: <https://w3id.org/heritagegraph/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# ---------------------------------------------------------------------------
# All 32 Competency Questions with their ASK queries
# ---------------------------------------------------------------------------
CQ_QUERIES: list[dict] = [
    # ── Structural Questions ──
    {
        "id": "CQ1",
        "dimension": "Structural",
        "question": "Which architectural structures were built during [time period] using [architectural style]?",
        "elements": "ArchitecturalStructure, Production, TimeSpan, has_architectural_style, was_produced_by_event, has_timespan, date_earliest, date_latest",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:ArchitecturalStructure a owl:Class .
  heritageGraph:Production a owl:Class .
  heritageGraph:TimeSpan a owl:Class .
  heritageGraph:has_architectural_style a owl:ObjectProperty .
  heritageGraph:was_produced_by_event a owl:ObjectProperty .
  heritageGraph:has_timespan a owl:ObjectProperty .
  heritageGraph:date_earliest a owl:DatatypeProperty .
  heritageGraph:date_latest a owl:DatatypeProperty .
}"""
    },
    {
        "id": "CQ2",
        "dimension": "Structural",
        "question": "Which architectural elements are components of structures used in a ritual?",
        "elements": "ArchitecturalElement, ArchitecturalStructure, RitualEvent, is_component_of, participates_in_ritual",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:ArchitecturalElement a owl:Class .
  heritageGraph:ArchitecturalStructure a owl:Class .
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:is_component_of a owl:ObjectProperty .
  heritageGraph:participates_in_ritual a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ3",
        "dimension": "Structural",
        "question": "Which iconographic objects depict [deity], and where are they located?",
        "elements": "IconographicObject, Deity, Place, depicts_deity, has_current_location",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:IconographicObject a owl:Class .
  heritageGraph:Deity a owl:Class .
  heritageGraph:Place a owl:Class .
  heritageGraph:depicts_deity a owl:ObjectProperty .
  heritageGraph:has_current_location a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ4",
        "dimension": "Structural",
        "question": "Which heritage structures are associated with historical events and time-spans?",
        "elements": "ArchitecturalStructure, HistoricalEvent, TimeSpan, architectural_structures, has_timespan",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:ArchitecturalStructure a owl:Class .
  heritageGraph:HistoricalEvent a owl:Class .
  heritageGraph:TimeSpan a owl:Class .
  heritageGraph:architectural_structures a owl:ObjectProperty .
  heritageGraph:has_timespan a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ5",
        "dimension": "Structural",
        "question": "Which structures in a given area belong to a specific typology?",
        "elements": "ArchitecturalStructure, Place, contains_structure, subclasses of ArchitecturalStructure",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:Place a owl:Class .
  heritageGraph:ArchitecturalStructure a owl:Class .
  heritageGraph:contains_structure a owl:ObjectProperty .
  FILTER EXISTS { ?t rdfs:subClassOf heritageGraph:ArchitecturalStructure }
}"""
    },
    {
        "id": "CQ6",
        "dimension": "Structural",
        "question": "Which heritage shares a common architectural style?",
        "elements": "ArchitecturalStructure, has_architectural_style",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:ArchitecturalStructure a owl:Class .
  heritageGraph:has_architectural_style a owl:ObjectProperty .
}"""
    },
    # ── Ritual / Festival Questions ──
    {
        "id": "CQ7",
        "dimension": "Ritual/Festival",
        "question": "Which sacred structures in [place] are associated with which deities?",
        "elements": "Temple, Enshrinement, Deity, enshrines_deity_through_event, enshrined_deity, enshrined_in_structure, took_place_at",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:Temple a owl:Class .
  heritageGraph:Enshrinement a owl:Class .
  heritageGraph:Deity a owl:Class .
  heritageGraph:enshrines_deity_through_event a owl:ObjectProperty .
  heritageGraph:enshrined_deity a owl:ObjectProperty .
  heritageGraph:enshrined_in_structure a owl:ObjectProperty .
  heritageGraph:took_place_at a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ8",
        "dimension": "Ritual/Festival",
        "question": "Among temples with daily Nitya Puja, which are in poor/endangered condition?",
        "elements": "Temple, RitualEvent, ConditionAssessment, ConditionState, has_condition_assessment, assessed_condition_state, has_condition_type, ritual_type",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:Temple a owl:Class .
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:ConditionAssessment a owl:Class .
  heritageGraph:ConditionState a owl:Class .
  heritageGraph:has_condition_assessment a owl:ObjectProperty .
  heritageGraph:assessed_condition_state a owl:ObjectProperty .
  heritageGraph:has_condition_type a owl:ObjectProperty .
  heritageGraph:ritual_type a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ9",
        "dimension": "Ritual/Festival",
        "question": "Which social/caste groups have hereditary roles in rituals critical for festivals?",
        "elements": "CasteGroup, RitualEvent, performed_by_group, is_critical_for_festival, traditional_role",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:CasteGroup a owl:Class .
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:performed_by_group a owl:DatatypeProperty .
  heritageGraph:is_critical_for_festival a owl:DatatypeProperty .
  heritageGraph:traditional_role a owl:DatatypeProperty .
}"""
    },
    {
        "id": "CQ10",
        "dimension": "Ritual/Festival",
        "question": "Which ritual objects are associated with rituals, and which groups use them?",
        "elements": "IconographicObject, RitualEvent, participates_in_ritual, used_by",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:IconographicObject a owl:Class .
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:participates_in_ritual a owl:ObjectProperty .
  heritageGraph:used_by a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ11",
        "dimension": "Ritual/Festival",
        "question": "Which rituals/festivals are associated with sites/places, which deities they invoke, and recurrence patterns?",
        "elements": "RitualEvent, Festival, ritual_on_structure, took_place_at, invokes_deity, recurrence_pattern",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:Festival a owl:Class .
  heritageGraph:ritual_on_structure a owl:ObjectProperty .
  heritageGraph:took_place_at a owl:ObjectProperty .
  heritageGraph:invokes_deity a owl:ObjectProperty .
  heritageGraph:recurrence_pattern a owl:DatatypeProperty .
}"""
    },
    {
        "id": "CQ12",
        "dimension": "Ritual/Festival",
        "question": "What is the canonical sequence of ritual events within a festival cycle?",
        "elements": "RitualEvent, Festival, occurs_before, occurs_after, carried_out_by, performed_by_group",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:Festival a owl:Class .
  heritageGraph:occurs_before a owl:ObjectProperty .
  heritageGraph:occurs_after a owl:ObjectProperty .
  heritageGraph:carried_out_by a owl:ObjectProperty .
  heritageGraph:performed_by_group a owl:DatatypeProperty .
}"""
    },
    {
        "id": "CQ13",
        "dimension": "Ritual/Festival",
        "question": "Which rituals involve moving sacred presences between sites, and what routes are traversed?",
        "elements": "RitualEvent, route_places, start_place, end_place, route_description",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:route_places a owl:ObjectProperty .
  heritageGraph:start_place a owl:ObjectProperty .
  heritageGraph:end_place a owl:ObjectProperty .
  heritageGraph:route_description a owl:DatatypeProperty .
}"""
    },
    {
        "id": "CQ14",
        "dimension": "Ritual/Festival",
        "question": "How do major crises trigger extraordinary rituals and relate to the ritual calendar?",
        "elements": "HistoricalEvent, RitualEvent, includes_ritual_event, recurrence_pattern",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:HistoricalEvent a owl:Class .
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:includes_ritual_event a owl:ObjectProperty .
  heritageGraph:recurrence_pattern a owl:DatatypeProperty .
}"""
    },
    {
        "id": "CQ15",
        "dimension": "Ritual/Festival",
        "question": "What materials/techniques/sensory elements are used in rituals and how do these vary?",
        "elements": "RitualEvent, Material, Technique, used_materials, used_technique, has_religious_tradition, took_place_at",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:Material a owl:Class .
  heritageGraph:Technique a owl:Class .
  heritageGraph:used_materials a owl:ObjectProperty .
  heritageGraph:used_technique a owl:ObjectProperty .
  heritageGraph:has_religious_tradition a owl:ObjectProperty .
  heritageGraph:took_place_at a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ16",
        "dimension": "Ritual/Festival",
        "question": "How do ritual obligations differ for participant groups?",
        "elements": "RitualEvent, performed_by_group, traditional_role",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:performed_by_group a owl:DatatypeProperty .
  heritageGraph:traditional_role a owl:DatatypeProperty .
}"""
    },
    {
        "id": "CQ17",
        "dimension": "Ritual/Festival",
        "question": "Which rituals/festivals have documented transformations and what drove them?",
        "elements": "RitualEvent, Festival, HeritageAssertion, DataSource, was_derived_from_source, was_attributed_to_agent",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:Festival a owl:Class .
  heritageGraph:HeritageAssertion a owl:Class .
  heritageGraph:DataSource a owl:Class .
  heritageGraph:was_derived_from_source a owl:ObjectProperty .
  heritageGraph:was_attributed_to_agent a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ18",
        "dimension": "Ritual/Festival",
        "question": "How do changes in location, ritual practice, and structure modification reflect transitions?",
        "elements": "ArchitecturalStructure, RitualEvent, HistoricalEvent, has_current_location, participates_in_ritual, has_provenance_assertion",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:ArchitecturalStructure a owl:Class .
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:HistoricalEvent a owl:Class .
  heritageGraph:has_current_location a owl:ObjectProperty .
  heritageGraph:participates_in_ritual a owl:ObjectProperty .
  heritageGraph:has_provenance_assertion a owl:ObjectProperty .
}"""
    },
    # ── Institutional / Syncretism ──
    {
        "id": "CQ19",
        "dimension": "Institutional/Syncretic",
        "question": "Which organizations manage heritage, perform rituals, and hold custody of assets?",
        "elements": "Guthi, managed_by_guthi, performs_ritual, holds_custody_of",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:Guthi a owl:Class .
  heritageGraph:managed_by_guthi a owl:ObjectProperty .
  heritageGraph:performs_ritual a owl:ObjectProperty .
  heritageGraph:holds_custody_of a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ20",
        "dimension": "Institutional/Syncretic",
        "question": "Which structures/objects were commissioned by patrons or communities?",
        "elements": "Production, commissioned_by, produced_object",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:Production a owl:Class .
  heritageGraph:commissioned_by a owl:ObjectProperty .
  heritageGraph:produced_object a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ21",
        "dimension": "Institutional/Syncretic",
        "question": "Which institutions provide economic and ritual support for specific sites, rituals, or living sacred figures?",
        "elements": "Guthi, supported_by_institution, Temple, RitualEvent, LivingGoddessTenure",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:Guthi a owl:Class .
  heritageGraph:supported_by_institution a owl:ObjectProperty .
  heritageGraph:Temple a owl:Class .
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:LivingGoddessTenure a owl:Class .
}"""
    },
    {
        "id": "CQ22",
        "dimension": "Institutional/Syncretic",
        "question": "Which festivals bring together practitioners from multiple traditions around a shared syncretic deity?",
        "elements": "Festival, SyncreticRelationship, assigned_to_deity, assigned_equivalent, performed_by_group, has_religious_tradition",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:Festival a owl:Class .
  heritageGraph:SyncreticRelationship a owl:Class .
  heritageGraph:assigned_to_deity a owl:ObjectProperty .
  heritageGraph:assigned_equivalent a owl:ObjectProperty .
  heritageGraph:performed_by_group a owl:DatatypeProperty .
  heritageGraph:has_religious_tradition a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ23",
        "dimension": "Institutional/Syncretic",
        "question": "Which places or structures function as shared or contested sites for multiple traditions?",
        "elements": "Place, ArchitecturalStructure, has_religious_tradition",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:Place a owl:Class .
  heritageGraph:ArchitecturalStructure a owl:Class .
  heritageGraph:has_religious_tradition a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ24",
        "dimension": "Institutional/Syncretic",
        "question": "Which rituals at Hindu temples and Buddhist monuments invoke the same syncretic deity?",
        "elements": "RitualEvent, Temple, BuddhistMonument, invokes_deity, performed_by_group",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:Temple a owl:Class .
  heritageGraph:BuddhistMonument a owl:Class .
  heritageGraph:invokes_deity a owl:ObjectProperty .
  heritageGraph:performed_by_group a owl:DatatypeProperty .
}"""
    },
    {
        "id": "CQ25",
        "dimension": "Institutional/Syncretic",
        "question": "How do syncretic sacred figures link Hindu, Buddhist, and local practices across places and periods?",
        "elements": "SyncreticRelationship, assigned_to_deity, assigned_equivalent, was_derived_from_source, documented_in_source, Place, TimeSpan",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:SyncreticRelationship a owl:Class .
  heritageGraph:assigned_to_deity a owl:ObjectProperty .
  heritageGraph:assigned_equivalent a owl:ObjectProperty .
  heritageGraph:was_derived_from_source a owl:ObjectProperty .
  heritageGraph:documented_in_source a owl:ObjectProperty .
  heritageGraph:Place a owl:Class .
  heritageGraph:TimeSpan a owl:Class .
}"""
    },
    # ── Living Goddess (Kumari) ──
    {
        "id": "CQ26",
        "dimension": "Living Goddess",
        "question": "Which girl was serving as Living Goddess for which period, at which Kumari Ghar?",
        "elements": "LivingGoddessTenure, Person, ArchitecturalStructure, had_participant, residence_structure, has_timespan",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:LivingGoddessTenure a owl:Class .
  heritageGraph:Person a owl:Class .
  heritageGraph:ArchitecturalStructure a owl:Class .
  heritageGraph:had_participant a owl:ObjectProperty .
  heritageGraph:residence_structure a owl:ObjectProperty .
  heritageGraph:has_timespan a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ27",
        "dimension": "Living Goddess",
        "question": "For a given Kumari-person, which deity is believed to be present, and in which traditions?",
        "elements": "LivingGoddessTenure, Deity, embodied_deity, has_religious_tradition",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:LivingGoddessTenure a owl:Class .
  heritageGraph:Deity a owl:Class .
  heritageGraph:embodied_deity a owl:ObjectProperty .
  heritageGraph:has_religious_tradition a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ28",
        "dimension": "Living Goddess",
        "question": "How does the Kumari institution embody Hindu-Buddhist syncretism in a specific place and period?",
        "elements": "LivingGoddessTenure, SyncreticRelationship, Place, TimeSpan, assigned_to_deity, assigned_equivalent",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:LivingGoddessTenure a owl:Class .
  heritageGraph:SyncreticRelationship a owl:Class .
  heritageGraph:Place a owl:Class .
  heritageGraph:TimeSpan a owl:Class .
  heritageGraph:assigned_to_deity a owl:ObjectProperty .
  heritageGraph:assigned_equivalent a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ29",
        "dimension": "Living Goddess",
        "question": "What daily rituals does a specific Kumari perform, and what is their temporal pattern?",
        "elements": "RitualEvent, LivingGoddessTenure, ritual_type, ritual_on_structure, recurrence_pattern",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:LivingGoddessTenure a owl:Class .
  heritageGraph:ritual_type a owl:ObjectProperty .
  heritageGraph:ritual_on_structure a owl:ObjectProperty .
  heritageGraph:recurrence_pattern a owl:DatatypeProperty .
}"""
    },
    {
        "id": "CQ30",
        "dimension": "Living Goddess",
        "question": "In which festivals and processions does a given Kumari participate, and what is the ritual sequence?",
        "elements": "Festival, RitualEvent, occurs_before, occurs_after, had_participant",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:Festival a owl:Class .
  heritageGraph:RitualEvent a owl:Class .
  heritageGraph:occurs_before a owl:ObjectProperty .
  heritageGraph:occurs_after a owl:ObjectProperty .
  heritageGraph:had_participant a owl:ObjectProperty .
}"""
    },
    {
        "id": "CQ31",
        "dimension": "Living Goddess",
        "question": "Which institution bears economic/ritual responsibility for a given Kumari during her tenure?",
        "elements": "LivingGoddessTenure, supported_by_institution, Guthi",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:LivingGoddessTenure a owl:Class .
  heritageGraph:supported_by_institution a owl:ObjectProperty .
  heritageGraph:Guthi a owl:Class .
}"""
    },
    {
        "id": "CQ32",
        "dimension": "Living Goddess",
        "question": "When and why did an individual stop being Kumari, and what event terminated her divine status?",
        "elements": "LivingGoddessRetirement, ended_tenure_of, has_timespan, note",
        "sparql": PREFIXES + """
ASK WHERE {
  heritageGraph:LivingGoddessRetirement a owl:Class .
  heritageGraph:ended_tenure_of a owl:ObjectProperty .
  heritageGraph:has_timespan a owl:ObjectProperty .
  heritageGraph:note a owl:DatatypeProperty .
}"""
    },
]


def run_evaluation():
    report: list[str] = []
    csv_rows: list[dict] = []

    def log(msg: str):
        report.append(msg)
        print(msg)

    bar = "=" * 70
    log(f"\n{bar}")
    log("  §4.3 / §4.7  Competency-Question Validation & Traceability")
    log(f"{bar}")
    log(f"Date     : {datetime.now().isoformat()}")
    log(f"Ontology : {ONTOLOGY_FILE}")
    log(f"Queries  : {len(CQ_QUERIES)}")
    log("")

    # Parse ontology
    g = Graph()
    g.parse(str(ONTOLOGY_FILE), format="turtle")
    log(f"  Parsed {len(g)} triples\n")

    # Run each CQ
    passed = 0
    failed = 0
    dim_stats: dict[str, dict] = {}

    log(f"{'ID':<6} {'Dim':<22} {'Result':<8} Question")
    log("-" * 100)

    for cq in CQ_QUERIES:
        cq_id = cq["id"]
        dim = cq["dimension"]
        question = cq["question"]

        t0 = time.time()
        try:
            result = bool(g.query(cq["sparql"]))
        except Exception as e:
            result = False
            log(f"  ERROR on {cq_id}: {e}")
        elapsed = round(time.time() - t0, 3)

        status = "✅ PASS" if result else "❌ FAIL"
        if result:
            passed += 1
        else:
            failed += 1

        short_q = question[:60] + "..." if len(question) > 60 else question
        log(f"{cq_id:<6} {dim:<22} {status:<8} {short_q}")

        csv_rows.append({
            "cq_id": cq_id,
            "dimension": dim,
            "question": question,
            "ontology_elements": cq["elements"],
            "ask_result": result,
            "time_ms": int(elapsed * 1000),
        })

        # Dimension stats
        if dim not in dim_stats:
            dim_stats[dim] = {"pass": 0, "fail": 0}
        dim_stats[dim]["pass" if result else "fail"] += 1

    # Summary
    total = passed + failed
    log("")
    log(f"\n{bar}")
    log("  Summary")
    log(f"{bar}")
    log(f"  Total CQs  : {total}")
    log(f"  Passed     : {passed}  ({100 * passed / total:.1f}%)")
    log(f"  Failed     : {failed}  ({100 * failed / total:.1f}%)")
    log("")
    log("  By Dimension:")
    for dim, stats in dim_stats.items():
        dtotal = stats["pass"] + stats["fail"]
        log(f"    {dim:<25} {stats['pass']}/{dtotal} passed")

    # Write report
    report_path = RESULTS_DIR / "cq_validation_report.txt"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(f"\n📄 Report saved to: {report_path}")

    # Write CSV (traceability matrix)
    csv_path = RESULTS_DIR / "cq_traceability_matrix.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "cq_id", "dimension", "question", "ontology_elements", "ask_result", "time_ms"
        ])
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"📊 Traceability matrix saved to: {csv_path}")


if __name__ == "__main__":
    run_evaluation()
