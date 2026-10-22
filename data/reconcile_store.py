#!/usr/bin/env python3
"""Reconcile the initial DANAM pipeline vocabulary to the current released
HeritageGraph ontology.

Reads the N-Quads export of the Fuseki/TDB2 `heritagegraph` store
(data/reconciled/store_export.nq) and rewrites every ontology term from the
initial pipeline namespace (https://cair-nepal.org/heritagegraph/, snake_case)
to the current released ontology (https://cair-nepal.org/heritagegraph/, camelCase),
using data/reconcile_crosswalk.json. The initial pipeline and the released
ontology use the SAME namespace string; they are told apart by provenance only
(every vocabulary IRI in the input is an initial-pipeline term, and the output
is written in one pass and never re-read). As a guard, every namespace IRI in
the output must be a term the released ontology declares (class, property, or
enumeration individual); an unmapped initial-pipeline term that would
otherwise pass through unnoticed fails the run. Specifically it:

  * drops the old cair-nepal ontology T-Box graph (we use the real ontology);
  * drops predicates removed from the current ontology (epistemic_stance);
  * rewrites class and property IRIs per the crosswalk (incl. two CRM targets
    for the syncretic-assignment predicates);
  * converts remaining cair-nepal enumeration-value IRIs (e.g. .../NityaPuja)
    on enumeration-ranged predicates to the released enumeration individuals
    (https://cair-nepal.org/heritagegraph/RitualType#NityaPuja, or the value's
    declared meaning IRI such as an AAT concept), as the ontology's object
    properties and SHACL sh:in lists require; values not in the enumeration
    are reported. Old IRIs on other predicates become string literals;
  * types hg:confidenceScore values as xsd:decimal (the released range is
    xsd:decimal[0, 1]) and xsd:date values of datetime-ranged slots
    (crm:P82a/P82b, lastKnownExistenceDate) as xsd:dateTime (xsd:date is
    outside the OWL 2 datatype map);
  * turns the free-text hg:propositionPredicate descriptions listed in
    proposition_predicate_map into the xsd:anyURI of the property they name
    (the released range);
  * replaces external predicates listed in external_predicate_map (e.g. the
    RDFS-less CIDOC-CRM "property of a property" P14.1) by the released term;
  * appends a declarations graph (DECL_GRAPH) declaring every external class
    and property the data uses that the released ontology does not declare,
    so ontology + data is an OWL 2 DL ontology.

Instance IRIs (https://data.cair-nepal.org/...) are a data namespace, not
ontology terms, and are left unchanged. Output is written as N-Quads to
data/reconciled/danam-heritagegraph.nq (named graphs preserved). The input
store is never modified."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CROSSWALK = ROOT / "reconcile_crosswalk.json"
SRC = ROOT / "reconciled" / "store_export.nq"
OUT = ROOT / "reconciled" / "danam-heritagegraph.nq"

OLD_NS = "https://cair-nepal.org/heritagegraph/"
VOCAB_IRI = re.compile(r"<https://cair-nepal\.org/heritagegraph/([^>]+)>")
QUAD = re.compile(r"^(\S+) (\S+) (.*) (<[^>]+>) \.\s*$")
DECL_GRAPH = "https://data.cair-nepal.org/heritagegraph/graph/declarations"
BUILTIN_NS = ("http://www.w3.org/1999/02/22-rdf-syntax-ns#",
              "http://www.w3.org/2000/01/rdf-schema#", "http://www.w3.org/2002/07/owl#")
SCHEMA = ROOT.parent / "ontology" / "HeritageGraph.yaml"
TTL = ROOT.parent / "ontology" / "HeritageGraph.ttl"
XSD_FLOAT = "^^<http://www.w3.org/2001/XMLSchema#float>"
XSD_DECIMAL = "^^<http://www.w3.org/2001/XMLSchema#decimal>"
XSD_DATE = re.compile(r'"(\d{4}-\d{2}-\d{2})"\^\^<http://www\.w3\.org/2001/XMLSchema#date>')


def enum_tables() -> tuple[dict[str, str], dict[tuple[str, str], str], str, set[str]]:
    """(predicate IRI -> enum name, (enum, value) -> individual IRI, score
    predicate, datetime-ranged predicates),
    read from the LinkML source and checked against the released OWL."""
    from linkml_runtime import SchemaView
    from rdflib import Graph, OWL, RDF, URIRef
    sv = SchemaView(str(SCHEMA))
    owl = Graph()
    owl.parse(TTL, format="turtle")
    by_pred = {}
    for name, slot in sv.all_slots().items():
        rng = slot.range
        if rng in sv.all_enums() and slot.slot_uri:
            by_pred[sv.expand_curie(str(slot.slot_uri))] = rng
    ns = sv.schema.prefixes[sv.schema.default_prefix].prefix_reference
    values = {}
    for en, e in sv.all_enums().items():
        for vn, pv in (e.permissible_values or {}).items():
            iri = sv.expand_curie(str(pv.meaning)) if pv.meaning else f"{ns}{en}#{vn}"
            if (URIRef(iri), RDF.type, OWL.NamedIndividual) not in owl:
                raise SystemExit(f"enumeration individual not in the released OWL: {iri}")
            values[(en, vn)] = iri
    score = sv.expand_curie(str(sv.get_slot("confidence_score").slot_uri))
    datetime_preds = {sv.expand_curie(str(s.slot_uri)) for s in sv.all_slots().values()
                      if s.range == "datetime" and s.slot_uri}
    return by_pred, values, score, datetime_preds


def build_iri_map(cw: dict) -> dict[str, str]:
    m: dict[str, str] = {}
    for local, target in cw["class_map"].items():
        m[f"<{OLD_NS}{local}>"] = f"<{target}>"
    for local, target in cw["predicate_map"].items():
        m[f"<{OLD_NS}{local}>"] = f"<{target}>"
    return m


def escape_literal(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main() -> int:
    cw = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    iri_map = build_iri_map(cw)
    drop_preds = {f"<{p}>" for p in cw["drop_predicates"]}
    exclude_graph_suffixes = tuple(f"<{g}> ." for g in cw["exclude_graphs"])

    mapped_locals = set(cw["class_map"]) | set(cw["predicate_map"])
    dropped_locals = {p.rsplit("/", 1)[-1] for p in cw["drop_predicates"]}

    enum_by_pred, enum_values, score_pred, datetime_preds = enum_tables()
    value_map = {k: v for k, v in cw.get("enum_value_map", {}).items() if not k.startswith("_")}
    ext_pred_map = {f"<{k}>": f"<{v}>" for k, v in cw.get("external_predicate_map", {}).items()
                    if not k.startswith("_")}
    prop_pred_map = {k: v for k, v in cw.get("proposition_predicate_map", {}).items()
                     if not k.startswith("_")}
    prop_pred_iri = cw["predicate_map"]["asserted_property"]
    used_classes: set[str] = set()
    used_preds: dict[str, set[str]] = {}
    unknown: dict[tuple[str, str], int] = {}

    stats = {
        "in": 0, "kept": 0, "dropped_graph": 0, "dropped_pred": 0,
        "enum_iris": 0, "enum_unknown": 0, "enum_literalised": 0,
        "iri_rewrites": 0, "scores_decimal": 0, "dates_datetime": 0,
        "external_pred_rewrites": 0, "declarations": 0, "proposition_predicates": 0,
    }

    with SRC.open(encoding="utf-8") as fin, OUT.open("w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip() or line.startswith("#"):
                continue
            stats["in"] += 1

            # 1. drop the old ontology T-Box graph
            if line.rstrip().endswith(exclude_graph_suffixes):
                stats["dropped_graph"] += 1
                continue
            # 2. drop predicates removed from the current ontology
            if any(f" {p} " in line for p in drop_preds):
                stats["dropped_pred"] += 1
                continue

            # the (rewritten) predicate decides how an old enum-value IRI maps
            q = QUAD.match(line)
            pred = iri_map.get(q.group(2), q.group(2)).strip("<>") if q else ""
            enum = enum_by_pred.get(pred)

            # 3. rewrite mapped class/property IRIs (exact <iri> tokens)
            def repl_vocab(mobj: re.Match) -> str:
                token = mobj.group(0)
                local = mobj.group(1)
                if token in iri_map:
                    stats["iri_rewrites"] += 1
                    return iri_map[token]
                if local in mapped_locals or local in dropped_locals:
                    return token  # shouldn't reach here
                # 4. otherwise it's an enum-value individual
                if enum:
                    local = value_map.get(enum, {}).get(local, local)
                    iri = enum_values.get((enum, local))
                    if iri:
                        stats["enum_iris"] += 1
                        return f"<{iri}>"
                    stats["enum_unknown"] += 1
                    unknown[(enum, local)] = unknown.get((enum, local), 0) + 1
                stats["enum_literalised"] += 1
                return f'"{escape_literal(local)}"'

            new_line = VOCAB_IRI.sub(repl_vocab, line)
            q2 = QUAD.match(new_line)
            if q2 and q2.group(2) == f"<{prop_pred_iri}>":
                text = q2.group(3)
                if text.startswith('"') and text.endswith('"') and text[1:-1] in prop_pred_map:
                    typed = (f'"{prop_pred_map[text[1:-1]]}"'
                             f'^^<http://www.w3.org/2001/XMLSchema#anyURI>')
                    new_line = f"{q2.group(1)} {q2.group(2)} {typed} {q2.group(4)} .\n"
                    stats["proposition_predicates"] += 1
                elif not text.endswith("XMLSchema#anyURI>"):
                    raise SystemExit(f"propositionPredicate value not in proposition_predicate_map: {text}")
                q2 = QUAD.match(new_line)
            if q2 and q2.group(2) in ext_pred_map:
                new_line = new_line.replace(f" {q2.group(2)} ", f" {ext_pred_map[q2.group(2)]} ", 1)
                stats["external_pred_rewrites"] += 1
                q2 = QUAD.match(new_line)
            if q2:
                p_iri, obj = q2.group(2).strip("<>"), q2.group(3)
                if p_iri == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type" and obj.startswith("<"):
                    used_classes.add(obj.strip("<>"))
                used_preds.setdefault(p_iri, set()).add("iri" if obj.startswith("<") else "literal")
            if pred == score_pred and XSD_FLOAT in new_line:
                new_line = new_line.replace(XSD_FLOAT, XSD_DECIMAL)
                stats["scores_decimal"] += 1
            if pred in datetime_preds and XSD_DATE.search(new_line):
                new_line = XSD_DATE.sub(
                    r'"\1T00:00:00"^^<http://www.w3.org/2001/XMLSchema#dateTime>', new_line)
                stats["dates_datetime"] += 1
            fout.write(new_line)
            stats["kept"] += 1

        # declarations of external terms the ontology does not declare
        from rdflib import Graph, RDF, URIRef
        owl = Graph()
        owl.parse(TTL, format="turtle")
        declared = {str(s) for s in owl.subjects(RDF.type, None)}
        decl = []
        for c in sorted(used_classes):
            if c not in declared and not c.startswith(BUILTIN_NS):
                decl.append((c, "http://www.w3.org/2002/07/owl#Class"))
        for p_iri, kinds in sorted(used_preds.items()):
            if p_iri in declared or p_iri.startswith(BUILTIN_NS):
                continue
            kind = ("ObjectProperty" if kinds == {"iri"} else
                    "DatatypeProperty" if kinds == {"literal"} else "AnnotationProperty")
            decl.append((p_iri, f"http://www.w3.org/2002/07/owl#{kind}"))
        for s, o in decl:
            fout.write(f"<{s}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <{o}> <{DECL_GRAPH}> .\n")
        stats["declarations"] = len(decl)

    # guard: no initial-pipeline term may survive under the shared namespace
    ns = cw["new_vocab_ns"]
    leaked: dict[str, int] = {}
    pat = re.compile(r"<(" + re.escape(ns) + r"[^>]*)>")
    with OUT.open(encoding="utf-8") as fin:
        for line in fin:
            for iri in pat.findall(line):
                if iri not in declared:
                    leaked[iri] = leaked.get(iri, 0) + 1
    if leaked:
        for iri, n in sorted(leaked.items()):
            print(f"  NOT A RELEASED TERM: <{iri}> ({n}x)")
        raise SystemExit("reconciliation left initial-pipeline terms in the output")

    print("Reconciliation complete:")
    for k in ["in", "kept", "dropped_graph", "dropped_pred", "iri_rewrites",
              "enum_iris", "enum_unknown", "enum_literalised", "scores_decimal",
              "dates_datetime", "proposition_predicates", "external_pred_rewrites",
              "declarations"]:
        print(f"  {k:16} {stats[k]}")
    for (en, vn), n in sorted(unknown.items()):
        print(f"  value not in enumeration {en}: {vn!r} ({n}x, kept as a string literal)")
    print(f"\nOutput: {OUT.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
