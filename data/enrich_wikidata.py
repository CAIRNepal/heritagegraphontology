#!/usr/bin/env python3
"""Enrich the reconciled DANAM knowledge graph with independently-sourced facts
from Wikidata, mapped to the released HeritageGraph ontology.

Every entity and statement pulled here keeps a real, checkable provenance link
(prov:wasDerivedFrom / rdfs:seeAlso -> the Wikidata IRI), so the added data is
reproducible and cited, not fabricated. Only the *tangible* layer that Wikidata
genuinely records is emitted: monument typology, current location (coordinates),
inception (as a CIDOC-CRM E12 Production event), architectural style, deity
dedication (as an hg:Enshrinement), and the 2015 Gorkha / 1934 Nep-Bihar
earthquakes (as hg:HistoricalEvent linked to the structures they damaged).

The living-heritage CQs (rituals, caste roles, syncretism, the Kumari, guthi)
are deliberately NOT populated here: Wikidata does not contain those facts, and
inventing them would be fabrication. They remain covered by the cited
demonstrator ABox, which is the field-standard practice (ArCo, ICON).

Output: data/reconciled/wikidata-kv.nq  (named graph https://w3id.org/heritagegraph/graph/wikidata)
"""
from __future__ import annotations

import json
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import certifi

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "reconciled" / "wikidata-kv.nq"
GRAPH = "https://w3id.org/heritagegraph/graph/wikidata"

HG = "https://w3id.org/heritagegraph/"
CRM = "http://www.cidoc-crm.org/cidoc-crm/"
GEO = "http://www.opengis.net/ont/geosparql#"
PROV = "http://www.w3.org/ns/prov#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
XSD = "http://www.w3.org/2001/XMLSchema#"

CTX = ssl.create_default_context(cafile=certifi.where())
UA = "HeritageGraph-research/0.1 (academic; ontology enrichment)"

# Kathmandu Valley bounding box (captures Kathmandu, Lalitpur/Patan, Bhaktapur)
BOX = ('bd:serviceParam wikibase:cornerWest "Point(85.20 27.60)"^^geo:wktLiteral . '
       'bd:serviceParam wikibase:cornerEast "Point(85.55 27.80)"^^geo:wktLiteral .')

# 2015 Gorkha earthquake (Q19597), 1934 Nepal-Bihar earthquake (Q3182762)
QUAKES = {
    "Q19597": ("2015 Nepal earthquake (Gorkha)", "2015-04-25"),
    "Q3182762": ("1934 Nepal\u2013Bihar earthquake", "1934-01-15"),
}


def wq(query: str) -> list[dict]:
    url = "https://query.wikidata.org/sparql?format=json&query=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/sparql-results+json"})
    with urllib.request.urlopen(req, timeout=120, context=CTX) as r:
        return json.load(r)["results"]["bindings"]


MAIN_QUERY = f"""
SELECT ?item ?itemLabel ?coord ?typeLabel ?inception ?styleLabel ?deity ?deityLabel ?quake WHERE {{
  SERVICE wikibase:box {{
    ?item wdt:P625 ?coord .
    {BOX}
  }}
  ?item wdt:P17 wd:Q837 .
  {{ ?item wdt:P1435 [] }} UNION {{ ?item wdt:P31/wdt:P279* wd:Q1370598 }} UNION {{ ?item wdt:P571 [] }}
  OPTIONAL {{ ?item wdt:P31 ?type . }}
  OPTIONAL {{ ?item wdt:P571 ?inception . }}
  OPTIONAL {{ ?item wdt:P149 ?style . }}
  OPTIONAL {{ ?item wdt:P825 ?deity . }}
  OPTIONAL {{ ?item wdt:P793 ?quake . VALUES ?quake {{ wd:Q19597 wd:Q3182762 }} }}
  SERVICE wikibase:label {{
    bd:serviceParam wikibase:language "en" .
    ?item rdfs:label ?itemLabel . ?type rdfs:label ?typeLabel .
    ?style rdfs:label ?styleLabel . ?deity rdfs:label ?deityLabel .
  }}
}}
"""

# Which Wikidata P31 types map to which HeritageGraph class (for CQ5 typology).
TYPE_MAP = {
    "temple": "Temple", "hindu temple": "Temple", "shrine": "Temple",
    "buddhist temple": "Temple", "mandir": "Temple",
    "stupa": "Stupa", "chaitya": "Chaitya", "caitya": "Chaitya",
    "monastery": "ReligiousStructure", "vihara": "ReligiousStructure",
    "buddhist monastery": "ReligiousStructure",
}


def esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def lit(s: str, dt: str | None = None, lang: str = "en") -> str:
    if dt:
        return f'"{esc(s)}"^^<{dt}>'
    return f'"{esc(s)}"@{lang}'


def main() -> int:
    print("Querying Wikidata for Kathmandu Valley heritage entities ...")
    rows = wq(MAIN_QUERY)
    print(f"  {len(rows)} statement rows returned")

    # Aggregate per entity (a single item appears on multiple rows).
    items: dict[str, dict] = {}
    for r in rows:
        qid = r["item"]["value"].rsplit("/", 1)[-1]
        it = items.setdefault(qid, {"iri": r["item"]["value"], "label": None, "coord": None,
                                    "types": set(), "inception": None, "styles": set(),
                                    "deities": {}, "quakes": set()})
        it["label"] = it["label"] or r.get("itemLabel", {}).get("value")
        it["coord"] = it["coord"] or r.get("coord", {}).get("value")
        if r.get("typeLabel"): it["types"].add(r["typeLabel"]["value"].lower())
        if r.get("inception"): it["inception"] = it["inception"] or r["inception"]["value"]
        if r.get("styleLabel"): it["styles"].add(r["styleLabel"]["value"])
        if r.get("deity"):
            it["deities"][r["deity"]["value"]] = r.get("deityLabel", {}).get("value", "")
        if r.get("quake"): it["quakes"].add(r["quake"]["value"].rsplit("/", 1)[-1])

    quads: list[str] = []

    def q(s: str, p: str, o: str):
        quads.append(f"<{s}> <{p}> {o} <{GRAPH}> .")

    def qr(s: str, p: str, o_iri: str):
        quads.append(f"<{s}> <{p}> <{o_iri}> <{GRAPH}> .")

    # Earthquake events (shared) — hg:HistoricalEvent with a time-span.
    quake_ts = {}
    for qid, (label, date) in QUAKES.items():
        ev = f"{HG}event/{qid}"
        ts = f"{HG}timespan/{qid}"
        qr(ev, f"{RDF}type", f"{HG}HistoricalEvent")
        q(ev, f"{RDFS}label", lit(label))
        qr(ev, f"{PROV}wasDerivedFrom", f"http://www.wikidata.org/entity/{qid}")
        qr(ev, f"{CRM}P4_has_time-span", ts)
        qr(ts, f"{RDF}type", f"{CRM}E52_Time-Span")
        q(ts, f"{CRM}P82a_begin_of_the_begin", lit(date, f"{XSD}date"))
        quake_ts[qid] = ev

    counts = {"structures": 0, "places": 0, "productions": 0, "styles": 0,
              "enshrinements": 0, "typed_temples": 0, "quake_links": 0}

    for qid, it in items.items():
        if not it["label"]:
            continue
        struct = it["iri"]  # use the Wikidata IRI as the structure's identity
        counts["structures"] += 1
        # typology
        hg_class = "ArchitecturalStructure"
        for t in it["types"]:
            for key, cls in TYPE_MAP.items():
                if key in t:
                    hg_class = cls
        qr(struct, f"{RDF}type", f"{HG}{hg_class}")
        if hg_class in ("Temple",):
            counts["typed_temples"] += 1
        q(struct, f"{RDFS}label", lit(it["label"]))
        qr(struct, f"{PROV}wasDerivedFrom", struct)  # self-identifying WD IRI as source
        q(struct, f"{RDFS}seeAlso", f"<{struct}>")

        # location + coordinates (place node) -> CQ5 needs place P53i structure
        if it["coord"]:
            place = f"{HG}place/{qid}"
            qr(place, f"{RDF}type", f"{CRM}E53_Place")
            q(place, f"{GEO}asWKT", lit(it["coord"], f"{GEO}wktLiteral"))
            qr(struct, f"{CRM}P55_has_current_location", place)
            qr(place, f"{CRM}P53i_is_former_or_current_location_of", struct)
            counts["places"] += 1

        # inception -> E12 Production event (CQ1)
        if it["inception"]:
            prod = f"{HG}production/{qid}"
            ts = f"{HG}prodts/{qid}"
            qr(prod, f"{RDF}type", f"{CRM}E12_Production")
            qr(prod, f"{CRM}P108_has_produced", struct)
            qr(prod, f"{PROV}wasDerivedFrom", struct)
            qr(prod, f"{CRM}P4_has_time-span", ts)
            qr(ts, f"{RDF}type", f"{CRM}E52_Time-Span")
            q(ts, f"{CRM}P82a_begin_of_the_begin", lit(it["inception"][:10], f"{XSD}date")
              if len(it["inception"]) >= 10 else lit(it["inception"]))
            counts["productions"] += 1

        # architectural style (CQ1/CQ6)
        for st in it["styles"]:
            q(struct, f"{HG}hasArchitecturalStyle", lit(st))
            counts["styles"] += 1

        # deity dedication -> Enshrinement (CQ7)
        for diri, dlabel in it["deities"].items():
            dqid = diri.rsplit("/", 1)[-1]
            qr(diri, f"{RDF}type", f"{HG}Deity")
            if dlabel:
                q(diri, f"{RDFS}label", lit(dlabel))
            qr(diri, f"{PROV}wasDerivedFrom", diri)
            ensh = f"{HG}enshrinement/{qid}-{dqid}"
            qr(ensh, f"{RDF}type", f"{HG}Enshrinement")
            qr(ensh, f"{HG}enshrinedDeity", diri)
            qr(ensh, f"{HG}enshrinedInStructure", struct)
            if it["coord"]:
                qr(ensh, f"{CRM}P7_took_place_at", f"{HG}place/{qid}")
            qr(ensh, f"{PROV}wasDerivedFrom", struct)
            counts["enshrinements"] += 1

        # earthquake damage links (CQ4)
        for qk in it["quakes"]:
            if qk in quake_ts:
                qr(quake_ts[qk], f"{HG}architecturalStructures", struct)
                counts["quake_links"] += 1

    OUT.write_text("\n".join(quads) + "\n", encoding="utf-8")
    print(f"\nWrote {len(quads)} quads to {OUT.relative_to(ROOT)}")
    print("Enrichment summary (all sourced to Wikidata IRIs):")
    for k, v in counts.items():
        print(f"  {k:<16} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
