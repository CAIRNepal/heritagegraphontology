from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

try:
    from rdflib import BNode, Graph, Literal, RDF, RDFS, OWL, URIRef  # type: ignore
except Exception:  # pragma: no cover
    Graph = None  # type: ignore
    BNode = None  # type: ignore
    Literal = None  # type: ignore
    RDF = None  # type: ignore
    RDFS = None  # type: ignore
    OWL = None  # type: ignore
    URIRef = None  # type: ignore


HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")


def _as_list(x: Any) -> List[Any]:
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]


def _join(xs: Iterable[Any]) -> str:
    out: List[str] = []
    for x in xs:
        if x is None:
            continue
        if isinstance(x, (str, int, float, bool)):
            out.append(str(x))
        else:
            out.append(str(x))
    return ", ".join([s for s in out if s.strip()])


def _get(d: Dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def _autosize(ws, min_width: int = 12, max_width: int = 60) -> None:
    for col_cells in ws.columns:
        max_len = 0
        col = col_cells[0].column
        for cell in col_cells:
            val = "" if cell.value is None else str(cell.value)
            max_len = max(max_len, len(val))
        ws.column_dimensions[get_column_letter(col)].width = max(min_width, min(max_width, max_len + 2))


def _style_header(ws, row: int = 1) -> None:
    for cell in ws[row]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"


def _write_table(ws, headers: List[str], rows: List[List[Any]]) -> None:
    ws.append(headers)
    for r in rows:
        ws.append(r)
    _style_header(ws, 1)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    _autosize(ws)


def load_linkml_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_overview(schema: Dict[str, Any], yaml_path: Path, owl_path: Optional[Path]) -> List[Tuple[str, str]]:
    imports = _as_list(schema.get("imports"))
    annotations = schema.get("annotations") or {}
    lines: List[Tuple[str, str]] = [
        ("Schema / Ontology", str(schema.get("name") or schema.get("id") or "")),
        ("Version", str(schema.get("version") or "")),
        ("Description", str(schema.get("description") or "")),
        ("Default prefix", str(schema.get("default_prefix") or "")),
        ("Prefixes", _join((schema.get("prefixes") or {}).keys())),
        ("Imports (LinkML)", _join(imports)),
        ("Ontology IRI", str(annotations.get("owl:ontologyIRI") or "")),
        ("Version IRI", str(annotations.get("owl:versionIRI") or "")),
        ("OWL imports", str(annotations.get("owl:imports") or "")),
        ("YAML source", str(yaml_path.name)),
        ("OWL source", str(owl_path.name if owl_path else "")),
        ("Generated at", dt.datetime.now().isoformat(timespec="seconds")),
    ]
    return lines


def extract_classes(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [{"class": k, **(v or {})} for k, v in (schema.get("classes") or {}).items()]


def extract_slots(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [{"slot": k, **(v or {})} for k, v in (schema.get("slots") or {}).items()]


def extract_enums(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    enums = schema.get("enums") or {}
    out: List[Dict[str, Any]] = []
    for enum_name, enum_def in enums.items():
        pvs = (enum_def or {}).get("permissible_values") or {}
        for value_label, pv_def in pvs.items():
            pv_def = pv_def or {}
            out.append(
                {
                    "enum": enum_name,
                    "value": value_label,
                    "meaning": pv_def.get("meaning"),
                    "description": pv_def.get("description"),
                    "exact_mappings": _join(_as_list(pv_def.get("exact_mappings"))),
                    "close_mappings": _join(_as_list(pv_def.get("close_mappings"))),
                    "broad_mappings": _join(_as_list(pv_def.get("broad_mappings"))),
                    "narrow_mappings": _join(_as_list(pv_def.get("narrow_mappings"))),
                }
            )
    return out


def build_slot_domain_index(schema: Dict[str, Any]) -> Dict[str, List[str]]:
    idx: Dict[str, List[str]] = {}
    for cname, cdef in (schema.get("classes") or {}).items():
        for slot in _as_list((cdef or {}).get("slots")):
            idx.setdefault(str(slot), []).append(cname)
    return idx


def extract_provenance_summary(schema: Dict[str, Any]) -> List[List[str]]:
    focus = [
        "HeritageAssertion",
        "DataSource",
        "DocumentationActivity",
        "Verification",
        "InformationObject",
    ]
    rows: List[List[str]] = []
    classes = schema.get("classes") or {}
    for cname in focus:
        cdef = classes.get(cname) or {}
        rows.append(
            [
                cname,
                str(cdef.get("class_uri") or ""),
                str(cdef.get("description") or ""),
                _join(_as_list(cdef.get("slots"))),
            ]
        )
    return rows


def parse_cq_dimensions_from_tex(tex_path: Path) -> List[Dict[str, str]]:
    """
    Parse the CQ dimensions table in sw_template.tex (if present).

    Expected row style (from your template):
      Structural & ... & ArchitecturalStructure, Production, ConditionAssessment, Style & 7 \\
    """
    try:
        text = tex_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    # Narrow to the cq_dimensions table area if possible
    start = text.find(r"\label{tab:cq_dimensions}")
    if start != -1:
        text = text[start : start + 12000]

    rows: List[Dict[str, str]] = []
    for m in re.finditer(r"^([^%].*?)\\\\\s*$", text, flags=re.MULTILINE):
        line = m.group(1).strip()
        if "&" not in line:
            continue
        parts = [p.strip() for p in line.split("&")]
        if len(parts) != 4:
            continue

        dimension, focus, components, cq_count = parts
        # Skip header lines
        if dimension.lower().startswith(r"\textbf"):
            continue
        # Drop latex commands inside fields a bit
        dimension = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", dimension).strip()
        focus = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", focus).strip()
        components = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", components).strip()
        cq_count = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", cq_count).strip()
        if not dimension or dimension.startswith("\\"):
            continue
        # CQ count should be numeric-ish
        if not re.search(r"\d", cq_count):
            continue

        rows.append(
            {
                "dimension": dimension,
                "analytical_focus": focus,
                "ontological_components": components,
                "cq_count": cq_count,
            }
        )
    return rows


def _normalize_texttt_chunk(raw: str) -> List[str]:
    """Split a \\texttt{...} body into candidate identifiers (underscores unescaped)."""
    s = raw.replace(r"\_", "_").strip()
    parts: List[str] = []
    for chunk in re.split(r",\s*", s):
        t = chunk.strip()
        if not t:
            continue
        parts.append(t)
    return parts


def _mention_maps_class_or_slot(
    token: str,
    class_names: set,
    slot_names: set,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Map a TeX token to a schema class or slot name if possible.
    Returns (class_name, slot_name) with at most one non-None.
    """
    if not token or token.startswith("http"):
        return None, None
    # owl:sameAs, prov:foo, crm:E12_Production, Bhadra Shukla ... 
    low = token.lower()
    if low.startswith("owl:") or low.startswith("prov:"):
        return None, None
    if re.match(r"^E\d+_", token):  # E7_Activity in prose
        return None, None
    if " " in token and "_" not in token:
        return None, None

    local = token
    if ":" in local:
        local = local.split(":", 1)[-1]

    if local in class_names:
        return local, None
    if local in slot_names:
        return None, local

    # ritual:Consecration -> Consecration
    if local.replace("_", "").isalnum() and "_" in local and local in slot_names:
        return None, local

    return None, None


def parse_paper_subsubsections(
    tex_path: Path,
    class_names: set,
    slot_names: set,
) -> List[Dict[str, Any]]:
    """
    Parse \\\\subsubsection{Title} blocks from sw_template.tex (Conceptual Modelling section).
    Captures \\\\label, first paragraph as summary, and schema-aligned \\\\texttt{...} mentions.
    """
    try:
        full = tex_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    start = full.find(r"\subsection{Conceptual Modelling}")
    end = full.find(r"\subsection{Competency Questions}")
    if start == -1 or end == -1 or start >= end:
        text = full
    else:
        text = full[start:end]

    blocks = list(
        re.finditer(
            r"\\subsubsection\{([^}]+)\}\s*(?:\\label\{([^}]+)\}\s*)?(.*?)(?=\\subsubsection|\\subsection|\Z)",
            text,
            flags=re.DOTALL,
        )
    )

    out: List[Dict[str, Any]] = []
    for m in blocks:
        title = (m.group(1) or "").strip()
        tex_label = (m.group(2) or "").strip()
        body = m.group(3) or ""
        # Summary: first non-empty line of prose (skip blanks after label)
        summary = ""
        for line in body.splitlines():
            s = line.strip()
            if not s or s.startswith("%"):
                continue
            if s.startswith("\\begin") or s.startswith("\\end"):
                continue
            # strip simple LaTeX wrapper for snippet
            summary = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})*", "", s)
            summary = re.sub(r"\s+", " ", summary).strip()
            if summary and len(summary) > 400:
                summary = summary[:397] + "..."
            break

        matched_classes: List[str] = []
        matched_slots: List[str] = []
        seen_c: set = set()
        seen_s: set = set()

        for mm in re.finditer(r"\\texttt\{([^}]+)\}", body):
            for chunk in _normalize_texttt_chunk(mm.group(1)):
                cls, slot = _mention_maps_class_or_slot(chunk, class_names, slot_names)
                if cls and cls not in seen_c:
                    seen_c.add(cls)
                    matched_classes.append(cls)
                elif slot and slot not in seen_s:
                    seen_s.add(slot)
                    matched_slots.append(slot)
                else:
                    inner = re.match(r"^([A-Za-z][A-Za-z0-9_]*).*", chunk)
                    if inner:
                        cls2, slot2 = _mention_maps_class_or_slot(inner.group(1), class_names, slot_names)
                        if cls2 and cls2 not in seen_c:
                            seen_c.add(cls2)
                            matched_classes.append(cls2)
                        elif slot2 and slot2 not in seen_s:
                            seen_s.add(slot2)
                            matched_slots.append(slot2)

        components = ", ".join(matched_classes + matched_slots)
        out.append(
            {
                "title": title,
                "tex_label": tex_label,
                "summary": summary,
                "components": components,
                "n_classes": len(matched_classes),
                "n_slots": len(matched_slots),
            }
        )

    return out


def build_modules_sheet_rows(
    schema: Dict[str, Any],
    tex_path: Optional[Path],
) -> List[List[Any]]:
    """
    Build a supervisor-friendly 'Modules' sheet:
    - Paper \\\\subsubsection headings from sw_template.tex (exact titles + labels)
    - 'Layers' derived from the modeling narrative
    - 'CQ dimensions' parsed from the cq_dimensions table (if available)
    """
    class_names = set((schema.get("classes") or {}).keys())
    slot_names = set((schema.get("slots") or {}).keys())

    layers = [
        {
            "type": "Layer",
            "name": "Tangible layer",
            "focus": "Physical heritage entities (structures, iconographic objects, elements)",
            "components": ", ".join([c for c in ["HumanMadeObject", "ArchitecturalStructure", "Temple", "BuddhistMonument", "IconographicObject", "Murti", "Paubha", "ArchitecturalElement", "PhysicalHeritageThing"] if c in class_names]),
        },
        {
            "type": "Layer",
            "name": "Event layer",
            "focus": "Events mediate historically contingent relationships",
            "components": ", ".join([c for c in ["Production", "RitualEvent", "Festival", "Consecration", "Enshrinement", "TransferOfCustody", "ConditionAssessment", "HistoricalEvent", "DestructionEvent"] if c in class_names]),
        },
        {
            "type": "Layer",
            "name": "Time/Space",
            "focus": "Temporal and spatial anchoring for entities and events",
            "components": ", ".join([c for c in ["TimeSpan", "CalendarSystem", "Place"] if c in class_names]),
        },
        {
            "type": "Layer",
            "name": "Provenance",
            "focus": "Source- and agent-attributed documentation and assertions",
            "components": ", ".join([c for c in ["HeritageAssertion", "DataSource", "DocumentationActivity", "InformationObject", "Verification", "DataCustodian"] if c in class_names]),
        },
        {
            "type": "Layer",
            "name": "Social institutions",
            "focus": "Groups, people, and custodial structures (e.g., Guthi)",
            "components": ", ".join([c for c in ["Guthi", "CasteGroup", "Person", "Actor"] if c in class_names]),
        },
    ]

    # Parse CQ dimensions table if possible
    cq_dims: List[Dict[str, str]] = []
    subsubsections: List[Dict[str, Any]] = []
    if tex_path and tex_path.exists():
        cq_dims = parse_cq_dimensions_from_tex(tex_path)
        subsubsections = parse_paper_subsubsections(tex_path, class_names, slot_names)

    rows: List[List[Any]] = []

    enum_names = set((schema.get("enums") or {}).keys())

    for sec in subsubsections:
        comps = sec["components"] or ""
        nc = int(sec["n_classes"])
        ns = int(sec["n_slots"])
        # Paper uses legacy CRM-prefixed \\texttt{} and some property nicknames; align to actual schema.
        if "Institutional Infrastructure" in sec["title"]:
            extras: List[str] = []
            for cname in ("Guthi", "Person", "Actor"):
                if cname in class_names and cname not in comps:
                    extras.append(cname)
                    nc += 1
            for sname in ("performs_ritual", "holds_custody_of", "has_membership", "guthi_type"):
                if sname in slot_names and sname not in comps:
                    extras.append(sname)
                    ns += 1
            if "GuthiTypeEnum" in enum_names and "GuthiTypeEnum" not in comps:
                extras.append("GuthiTypeEnum (enum)")
            if extras:
                comps = ", ".join([p for p in comps.split(", ") if p] + extras)

        rows.append(
            [
                "Paper subsection",
                sec["title"],
                sec["summary"],
                comps,
                nc,
                ns,
                f"sw_template.tex ({sec['tex_label'] or 'no label'})",
            ]
        )

    for item in layers:
        comps = item["components"]
        # Add quick counts for convenience
        comp_list = [c.strip() for c in comps.split(",") if c.strip()]
        class_count = sum(1 for c in comp_list if c in class_names)
        slot_count = sum(1 for s in comp_list if s in slot_names)
        rows.append([item["type"], item["name"], item["focus"], comps, class_count, slot_count, "sw_template.tex"])

    for d in cq_dims:
        comps = d["ontological_components"]
        comp_list = [c.strip() for c in comps.split(",") if c.strip()]
        class_count = sum(1 for c in comp_list if c in class_names)
        rows.append(
            [
                "CQ Dimension",
                d["dimension"],
                d["analytical_focus"],
                comps,
                class_count,
                0,
                "sw_template.tex",
            ]
        )

    # If parsing failed, still include a minimal supervisor view
    if not cq_dims:
        rows.append(
            [
                "CQ Dimension",
                "Syncretic",
                "Cross-traditional equivalences, provenance of theological claims",
                "SyncreticRelationship, Deity, HeritageAssertion, DataSource",
                int("SyncreticRelationship" in class_names) + int("Deity" in class_names) + int("HeritageAssertion" in class_names) + int("DataSource" in class_names),
                0,
                "fallback",
            ]
        )
        rows.append(
            [
                "CQ Dimension",
                "Living Goddess",
                "Divine embodiment, lifecycle events, tenure reasoning",
                "LivingGoddessTenure, LivingGoddessSelection, LivingGoddessRetirement, Person, Deity",
                int("LivingGoddessTenure" in class_names)
                + int("LivingGoddessSelection" in class_names)
                + int("LivingGoddessRetirement" in class_names)
                + int("Person" in class_names)
                + int("Deity" in class_names),
                0,
                "fallback",
            ]
        )

    return rows


@dataclass(frozen=True)
class OwlRestriction:
    owl_class: str
    on_property: str
    restriction_type: str
    filler: str


def _qname(g: Graph, uri: Any) -> str:
    if uri is None:
        return ""
    try:
        if isinstance(uri, Literal):
            return str(uri)
        if isinstance(uri, BNode):
            return "_:bnode"
        return g.namespace_manager.normalizeUri(uri)
    except Exception:
        return str(uri)


def parse_owl_restrictions(owl_path: Path) -> List[OwlRestriction]:
    if Graph is None:
        return []
    g = Graph()
    # review.owl appears to be TTL
    g.parse(str(owl_path), format="turtle")

    restrictions: List[OwlRestriction] = []

    # Find: ?class rdfs:subClassOf [ a owl:Restriction ; owl:onProperty ?p ; ... ]
    for cls, _, sc in g.triples((None, RDFS.subClassOf, None)):
        if not isinstance(sc, BNode):
            continue
        if (sc, RDF.type, OWL.Restriction) not in g:
            continue

        prop = next((o for _, _, o in g.triples((sc, OWL.onProperty, None))), None)
        if prop is None:
            continue

        # Prefer "allValuesFrom", else someValuesFrom, else cardinalities.
        handled = False
        for pred, rtype in [
            (OWL.allValuesFrom, "allValuesFrom"),
            (OWL.someValuesFrom, "someValuesFrom"),
            (OWL.hasValue, "hasValue"),
        ]:
            filler = next((o for _, _, o in g.triples((sc, pred, None))), None)
            if filler is not None:
                restrictions.append(
                    OwlRestriction(
                        owl_class=_qname(g, cls),
                        on_property=_qname(g, prop),
                        restriction_type=rtype,
                        filler=_qname(g, filler),
                    )
                )
                handled = True
        if handled:
            continue

        for pred, rtype in [
            (OWL.minCardinality, "minCardinality"),
            (OWL.maxCardinality, "maxCardinality"),
            (OWL.cardinality, "cardinality"),
        ]:
            val = next((o for _, _, o in g.triples((sc, pred, None))), None)
            if val is not None:
                restrictions.append(
                    OwlRestriction(
                        owl_class=_qname(g, cls),
                        on_property=_qname(g, prop),
                        restriction_type=rtype,
                        filler=str(val),
                    )
                )
    return restrictions


def export_to_excel(
    schema: Dict[str, Any],
    yaml_path: Path,
    owl_path: Optional[Path],
    tex_path: Optional[Path],
    out_path: Path,
) -> None:
    wb = Workbook()

    # Overview
    ws = wb.active
    ws.title = "Overview"
    ws.append(["Field", "Value"])
    for k, v in build_overview(schema, yaml_path, owl_path):
        ws.append([k, v])
    _style_header(ws, 1)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 100

    # Classes
    classes = extract_classes(schema)
    class_rows: List[List[Any]] = []
    for c in classes:
        slot_usage = c.get("slot_usage") or {}
        required = [s for s, su in (slot_usage or {}).items() if (su or {}).get("required") is True]
        minc = []
        maxc = []
        for s, su in (slot_usage or {}).items():
            su = su or {}
            if "minimum_cardinality" in su:
                minc.append(f"{s}={su.get('minimum_cardinality')}")
            if "maximum_cardinality" in su:
                maxc.append(f"{s}={su.get('maximum_cardinality')}")

        class_rows.append(
            [
                c.get("class", ""),
                c.get("class_uri", ""),
                c.get("is_a", ""),
                c.get("description", ""),
                _join(_as_list(c.get("disjoint_with"))),
                _join(_as_list(c.get("union_of"))),
                _join(_as_list(c.get("slots"))),
                _join(required),
                _join(minc),
                _join(maxc),
                _join(_as_list(c.get("exact_mappings"))),
                _join(_as_list(c.get("close_mappings"))),
                _join(_as_list(c.get("broad_mappings"))),
            ]
        )

    ws = wb.create_sheet("Classes")
    _write_table(
        ws,
        [
            "Class",
            "class_uri",
            "Parent (is_a)",
            "Description",
            "Disjoint with",
            "Union of",
            "Slots (properties)",
            "Required (slot_usage)",
            "Min cardinality (slot_usage)",
            "Max cardinality (slot_usage)",
            "Exact mappings",
            "Close mappings",
            "Broad mappings",
        ],
        class_rows,
    )

    # Slots
    slots = extract_slots(schema)
    domain_idx = build_slot_domain_index(schema)
    slot_rows: List[List[Any]] = []
    for s in slots:
        slot_rows.append(
            [
                s.get("slot", ""),
                s.get("slot_uri", ""),
                _join(domain_idx.get(s.get("slot", ""), [])),
                s.get("range", ""),
                str(s.get("multivalued", "")),
                s.get("inverse", ""),
                s.get("is_a", ""),
                s.get("description", ""),
                _join(_as_list(s.get("exact_mappings"))),
                _join(_as_list(s.get("broad_mappings"))),
            ]
        )
    ws = wb.create_sheet("Slots")
    _write_table(
        ws,
        [
            "Slot",
            "slot_uri",
            "Domain (used by classes)",
            "Range",
            "Multivalued",
            "Inverse",
            "is_a",
            "Description",
            "Exact mappings",
            "Broad mappings",
        ],
        slot_rows,
    )

    # Enums
    enum_rows = extract_enums(schema)
    ws = wb.create_sheet("Enums")
    _write_table(
        ws,
        [
            "Enum",
            "Value",
            "Meaning (IRI/curie)",
            "Description",
            "Exact mappings",
            "Close mappings",
            "Broad mappings",
            "Narrow mappings",
        ],
        [
            [
                r["enum"],
                r["value"],
                r["meaning"],
                r["description"],
                r["exact_mappings"],
                r["close_mappings"],
                r["broad_mappings"],
                r["narrow_mappings"],
            ]
            for r in enum_rows
        ],
    )

    # Provenance
    ws = wb.create_sheet("Provenance")
    _write_table(
        ws,
        ["Focus class", "class_uri", "Description", "Key slots"],
        extract_provenance_summary(schema),
    )

    # Modules (from sw_template.tex structure)
    ws = wb.create_sheet("Modules")
    _write_table(
        ws,
        ["Type", "Name", "Focus", "Ontological components", "#Classes matched", "#Slots matched", "Source"],
        build_modules_sheet_rows(schema, tex_path),
    )

    # OWL Restrictions (from review.owl)
    ws = wb.create_sheet("OWL Restrictions")
    if owl_path and owl_path.exists():
        restrictions = parse_owl_restrictions(owl_path)
        rows = [[r.owl_class, r.on_property, r.restriction_type, r.filler] for r in restrictions]
        _write_table(ws, ["Class", "onProperty", "Restriction", "Filler/value"], rows)
    else:
        _write_table(ws, ["Class", "onProperty", "Restriction", "Filler/value"], [])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)


def main() -> int:
    ap = argparse.ArgumentParser(description="Export HeritageGraph YAML/OWL to Excel workbook.")
    ap.add_argument("--yaml", default="ontology/HeritageGraph.yaml", help="Path to LinkML YAML schema")
    ap.add_argument("--owl", default="ontology/HeritageGraph.ttl", help="Path to OWL Turtle file (optional)")
    ap.add_argument("--tex", default="sw_template.tex", help="Path to SW paper template tex (optional)")
    ap.add_argument("--out", default="HeritageGraph_ontology.xlsx", help="Output .xlsx path")
    args = ap.parse_args()

    yaml_path = Path(args.yaml)
    owl_path = Path(args.owl) if args.owl else None
    tex_path = Path(args.tex) if args.tex else None
    out_path = Path(args.out)

    schema = load_linkml_yaml(yaml_path)
    export_to_excel(
        schema,
        yaml_path,
        owl_path if owl_path and owl_path.exists() else None,
        tex_path if tex_path and tex_path.exists() else None,
        out_path,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

