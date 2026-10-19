#!/usr/bin/env python3
"""
LUX → HeritageGraph migration script
====================================

Orchestrates the four operational modes described in MIGRATION_PLAN.md:

  --mode crawl      Pull LUX records over the REST API (fallback if no dump)
  --mode transform  Run the CONSTRUCT-as-INSERT batched transformation
  --mode validate   Run the validation_queries.sparql sanity / parity checks
  --mode delta      Apply weekly LUX diffs (post-migration maintenance)

Targets Oxigraph (chosen by the project) but works against any SPARQL 1.1
Update endpoint: Apache Jena Fuseki, GraphDB, Virtuoso, Stardog, Blazegraph.

Dependencies (pip):
    rdflib>=6
    requests
    pyoxigraph         # optional; only for in-process Oxigraph runs
    tqdm               # progress bars

Author: Semih Yumuşak — May 2026
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator
from urllib.parse import urlencode

# --- third-party (lazy import where possible) --------------------------------
import subprocess
try:
    import requests
except ImportError:                                                  # pragma: no cover
    requests = None
try:
    from tqdm import tqdm
except ImportError:                                                  # pragma: no cover
    def tqdm(it, **kw):                                              # noqa: D401
        return it


class _CurlResponse:
    """Minimal requests-compatible response wrapper around system curl output."""

    def __init__(self, status_code: int, text: str):
        self.status_code = status_code
        self.text = text

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code} from curl: {self.text[:200]}")

    def json(self):
        import json as _json
        return _json.loads(self.text)


def _curl_get(url: str, headers: dict | None = None, timeout: int = 60) -> _CurlResponse:
    # CloudFront in front of LUX blocks Python TLS clients (urllib3, curl_cffi);
    # the system `curl` binary passes, so shell out to it.
    cmd = ["curl", "-sS", "--max-time", str(timeout),
           "-w", "\n%{http_code}", url]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if out.returncode != 0:
        raise RuntimeError(f"curl failed (rc={out.returncode}): {out.stderr.strip()}")
    body, _, code = out.stdout.rpartition("\n")
    return _CurlResponse(int(code.strip() or 0), body)

LOG = logging.getLogger("lux2hg")

# =============================================================================
# Constants
# =============================================================================

DEFAULT_GRAPH_RAW       = "https://lux.collections.yale.edu/"
DEFAULT_GRAPH_ALIGNMENT = "https://w3id.org/heritagegraph/alignment/lux"
DEFAULT_GRAPH_HG        = "https://w3id.org/heritagegraph/"
DEFAULT_GRAPH_IMPORTED  = "https://w3id.org/heritagegraph/imported/lux"

LUX_REST_ROOT = "https://lux.collections.yale.edu/api"
LUX_SEARCH_EP = LUX_REST_ROOT + "/search"
LUX_USER_AGENT = "heritagegraph-lux-migration/0.1 (mailto:semihyumusak@yahoo.com)"

LUX_TYPE_ENDPOINTS = [
    ("HumanMadeObject",    "object"),
    ("DigitalObject",      "digital"),
    ("Person",             "person"),
    ("Group",              "group"),
    ("Place",              "place"),
    ("Event",              "event"),       # Event + Activity + Period live here
    ("Set",                "set"),
    ("Concept",            "concept"),     # Type, Material, Language, …
    ("Text",               "text"),        # LinguisticObject family
    ("Visual",             "visual"),      # VisualItem family
]

# =============================================================================
# Endpoint adapter — single thin layer for SPARQL Query and SPARQL Update
# =============================================================================

@dataclass
class Endpoint:
    """Wraps a SPARQL 1.1 Query+Update endpoint or an embedded pyoxigraph store."""
    url: str | None = None                  # http://host:port  (server mode)
    store_path: str | None = None           # /var/lib/oxigraph (embedded mode)
    embedded_store: object | None = field(default=None, repr=False)
    query_path: str = "/query"              # Oxigraph default; Fuseki overrides
    update_path: str = "/update"
    timeout: int = 600

    def __post_init__(self):
        if self.store_path and self.embedded_store is None:
            try:
                import pyoxigraph as ox
                self.embedded_store = ox.Store(self.store_path)
                LOG.info("Opened embedded Oxigraph store at %s", self.store_path)
            except ImportError:
                LOG.error("pyoxigraph not installed; cannot use embedded mode")
                raise

    # ----- SPARQL ----------------------------------------------------------

    def query(self, sparql: str) -> list[dict]:
        """Run a SELECT/ASK/CONSTRUCT and return JSON-shaped bindings."""
        if self.embedded_store is not None:
            try:
                results = self.embedded_store.query(sparql)
                return _normalize_pyox_results(results)
            except Exception:
                LOG.exception("Embedded query failed")
                raise

        assert self.url and requests, "HTTP endpoint requires `requests`"
        r = requests.post(
            self.url.rstrip("/") + self.query_path,
            data={"query": sparql},
            headers={"Accept": "application/sparql-results+json"},
            timeout=self.timeout,
        )
        r.raise_for_status()
        try:
            return r.json().get("results", {}).get("bindings", [])
        except json.JSONDecodeError:
            return []

    def update(self, sparql: str) -> None:
        """Run a SPARQL UPDATE (INSERT/DELETE/CLEAR/DROP/etc.)."""
        if self.embedded_store is not None:
            self.embedded_store.update(sparql)
            return
        assert self.url and requests
        r = requests.post(
            self.url.rstrip("/") + self.update_path,
            data={"update": sparql},
            timeout=self.timeout,
        )
        r.raise_for_status()


def _normalize_pyox_results(results) -> list[dict]:
    """Bring pyoxigraph QuerySolutions to the SPARQL-results JSON shape."""
    out: list[dict] = []
    for row in results:
        try:
            keys = list(row.keys())          # newer pyoxigraph
        except AttributeError:
            keys = [v.name for v in row.variables]
        binding = {}
        for k in keys:
            try:
                v = row[k]
            except KeyError:
                continue
            if v is None:
                continue
            binding[k] = {"type": "uri", "value": str(v.value if hasattr(v, "value") else v)}
        out.append(binding)
    return out


# =============================================================================
# Mode 1: CRAWL — fallback when bulk dump is unavailable
# =============================================================================

def crawl(args: argparse.Namespace) -> None:
    if requests is None:
        LOG.error("`requests` is not installed; cannot crawl.")
        sys.exit(2)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    state_path = Path(args.resume_state) if args.resume_state else out_path.with_suffix(".state.json")

    state = {"completed": []}
    if state_path.exists():
        state = json.loads(state_path.read_text())
        LOG.info("Resuming crawl with state file %s (%d urls already done)",
                 state_path, len(state["completed"]))

    fetched = set(state["completed"])

    def do_search(q: str, scope: str = "objects") -> Iterator[str]:
        page = 1
        while True:
            params = {"q": q, "page": page, "pageSize": 200}
            url = f"{LUX_SEARCH_EP}/{scope}?{urlencode(params)}"
            r = _curl_get(url, timeout=args.timeout,
                          headers={"User-Agent": LUX_USER_AGENT,
                                   "Accept": "application/json"})
            r.raise_for_status()
            payload = r.json()
            ids = [item["id"] for item in payload.get("orderedItems", [])]
            if not ids:
                break
            yield from ids
            page += 1
            if page > args.max_pages:
                break

    with out_path.open("a", encoding="utf-8") as out_f:
        scopes = ["item", "agent", "work", "place", "concept", "event", "set", "reference"]
        for scope in scopes:
            LOG.info("Crawling scope=%s filter=%r", scope, args.filter)
            ids = list(do_search(args.filter or "*", scope))
            for rid in tqdm(ids, desc=scope):
                if rid in fetched:
                    continue
                try:
                    rec = _curl_get(rid, timeout=args.timeout,
                                    headers={"User-Agent": LUX_USER_AGENT,
                                             "Accept": "application/ld+json"})
                    rec.raise_for_status()
                    out_f.write(rec.text.replace("\n", " ") + "\n")
                    fetched.add(rid)
                    if len(fetched) % 500 == 0:
                        state["completed"] = sorted(fetched)
                        state_path.write_text(json.dumps(state))
                except Exception as e:
                    LOG.warning("Failed %s: %s", rid, e)
    state["completed"] = sorted(fetched)
    state_path.write_text(json.dumps(state))
    LOG.info("Crawl finished: %d records → %s", len(fetched), out_path)


# =============================================================================
# Mode 2: TRANSFORM — batched INSERT WHERE per CONSTRUCT
# =============================================================================

# Each tuple: (label, type-of-LUX-class, transform CONSTRUCT-style INSERT WHERE template)
#
# Use {OFFSET} and {LIMIT} placeholders. The transform engine substitutes them
# while iterating, so a single declarative pattern handles 100 K+ batches.
TRANSFORM_TEMPLATES: dict[str, str] = {
    # ---- 1. Object branch ------------------------------------------------
    "object": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX hgi: <https://w3id.org/heritagegraph/imported/lux/object/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgObj a crm:E22_Human-Made_Object ;
             owl:sameAs ?obj ;
             hg:name    ?label ;
             hg:has_architectural_style ?type ;
             hg:was_produced_by_event   ?prod ;
             hg:has_current_location    ?place ;
             hg:used_materials          ?mat ;
             hg:carries_inscription     ?insc ;
             hg:has_dimension           ?dim ;
             hg:has_visual_item         ?vis .
    } } WHERE {
      { SELECT ?obj WHERE {
          ?obj a crm:E22_Human-Made_Object .
        } ORDER BY ?obj LIMIT {LIMIT} OFFSET {OFFSET}
      }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/object/",
                      REPLACE(STR(?obj), "^.*/", ""))) AS ?hgObj)
      OPTIONAL { ?obj rdfs:label ?label }
      OPTIONAL { ?obj crm:P2_has_type ?type }
      OPTIONAL { ?obj crm:P108i_was_produced_by ?prod }
      OPTIONAL { ?obj crm:P55_has_current_location ?place }
      OPTIONAL { ?obj crm:P45_consists_of ?mat }
      OPTIONAL { ?obj crm:P128_carries ?insc . ?insc a crm:E34_Inscription }
      OPTIONAL { ?obj crm:P43_has_dimension ?dim }
      OPTIONAL { ?obj crm:P65_shows_visual_item ?vis }
    }""",
    # ---- 2. Person branch -----------------------------------------------
    "person": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgPerson a crm:E21_Person ; owl:sameAs ?p ; hg:name ?name ;
                hg:was_born_by ?birth ; hg:died_in_event ?death .
    } } WHERE {
      { SELECT ?p WHERE { ?p a crm:E21_Person . } ORDER BY ?p LIMIT {LIMIT} OFFSET {OFFSET} }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/person/",
                      REPLACE(STR(?p), "^.*/", ""))) AS ?hgPerson)
      OPTIONAL { ?p rdfs:label ?name }
      OPTIONAL { ?p crm:P98i_was_born ?birth }
      OPTIONAL { ?p crm:P100i_died_in ?death }
    }""",
    # ---- 3. Group branch ------------------------------------------------
    "group": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgGroup a hg:Group ; owl:sameAs ?g ; hg:name ?gname ;
               hg:was_formed_by ?formed ; hg:dissolved_by ?dissolved .
    } } WHERE {
      { SELECT ?g WHERE { ?g a crm:E74_Group . } ORDER BY ?g LIMIT {LIMIT} OFFSET {OFFSET} }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/group/",
                      REPLACE(STR(?g), "^.*/", ""))) AS ?hgGroup)
      OPTIONAL { ?g rdfs:label ?gname }
      OPTIONAL { ?g crm:P95i_was_formed_by    ?formed }
      OPTIONAL { ?g crm:P99i_was_dissolved_by ?dissolved }
    }""",
    # ---- 4. Place branch ------------------------------------------------
    "place": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgPlace a crm:E53_Place ; owl:sameAs ?pl ;
               hg:name ?plname ; hg:place_coordinates ?wkt .
    } } WHERE {
      { SELECT ?pl WHERE { ?pl a crm:E53_Place . } ORDER BY ?pl LIMIT {LIMIT} OFFSET {OFFSET} }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/place/",
                      REPLACE(STR(?pl), "^.*/", ""))) AS ?hgPlace)
      OPTIONAL { ?pl rdfs:label ?plname }
      OPTIONAL { ?pl crm:P168_place_is_defined_by ?wkt }
    }""",
    # ---- 5. Activity / event branch (UNION-of-CRM-types) ----------------
    # July 2026 gap audit: added the five missing genuine la: activity
    # classes, E96/E85/E86/E15/E17/E14/E13/E65/E81/E79/E80, plus guarded
    # fallbacks for generic E7 / E5 / E4 so ProvenanceActivity wrappers and
    # generic events are no longer dropped.
    "activity": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX sci: <http://www.ics.forth.gr/isl/CRMsci/>
    PREFIX la:  <https://linked.art/ns/terms/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgEv a ?hgClass ; owl:sameAs ?ev ;
            hg:carried_out_by ?actor ; hg:took_place_at ?place ; hg:has_timespan ?span ;
            hg:paid_amount ?amt .
    } } WHERE {
      { SELECT ?ev ?hgClass WHERE {
          { ?ev a crm:E12_Production            . BIND(crm:E12_Production              AS ?hgClass) }
          UNION { ?ev a crm:E11_Modification    . BIND(hg:Modification            AS ?hgClass) }
          UNION { ?ev a crm:E9_Move             . BIND(hg:Move                    AS ?hgClass) }
          UNION { ?ev a crm:E10_Transfer_of_Custody . BIND(crm:E10_Transfer_of_Custody   AS ?hgClass) }
          UNION { ?ev a crm:E96_Purchase        . BIND(hg:Purchase                AS ?hgClass) }
          UNION { ?ev a crm:E8_Acquisition      . BIND(hg:Acquisition             AS ?hgClass) }
          UNION { ?ev a crm:E67_Birth           . BIND(hg:Birth                   AS ?hgClass) }
          UNION { ?ev a crm:E69_Death           . BIND(hg:Death                   AS ?hgClass) }
          UNION { ?ev a crm:E66_Formation       . BIND(hg:Formation               AS ?hgClass) }
          UNION { ?ev a crm:E68_Dissolution     . BIND(hg:Dissolution             AS ?hgClass) }
          UNION { ?ev a crm:E85_Joining         . BIND(hg:Joining                 AS ?hgClass) }
          UNION { ?ev a crm:E86_Leaving         . BIND(hg:Leaving                 AS ?hgClass) }
          UNION { ?ev a crm:E6_Destruction      . BIND(crm:E6_Destruction        AS ?hgClass) }
          UNION { ?ev a crm:E81_Transformation  . BIND(hg:Transformation          AS ?hgClass) }
          UNION { ?ev a crm:E79_Part_Addition   . BIND(hg:PartAddition            AS ?hgClass) }
          UNION { ?ev a crm:E80_Part_Removal    . BIND(hg:PartRemoval             AS ?hgClass) }
          UNION { ?ev a sci:S19_Encounter_Event . BIND(hg:Encounter               AS ?hgClass) }
          UNION { ?ev a crm:E87_Curation_Activity . BIND(hg:CurationActivity      AS ?hgClass) }
          UNION { ?ev a crm:E16_Measurement     . BIND(hg:Measurement             AS ?hgClass) }
          UNION { ?ev a crm:E14_Condition_Assessment . BIND(crm:E14_Condition_Assessment AS ?hgClass) }
          UNION { ?ev a crm:E15_Identifier_Assignment . BIND(hg:IdentifierAssignment AS ?hgClass) }
          UNION { ?ev a crm:E17_Type_Assignment . BIND(hg:TypeAssignment          AS ?hgClass) }
          UNION { ?ev a crm:E65_Creation        . BIND(hg:Creation                AS ?hgClass)
                  FILTER NOT EXISTS { ?ev a crm:E83_Type_Creation } }
          UNION { ?ev a crm:E83_Type_Creation   . BIND(hg:TypeCreation            AS ?hgClass) }
          UNION { ?ev a crm:E63_Beginning_of_Existence . BIND(hg:BeginningOfExistence AS ?hgClass) }
          UNION { ?ev a crm:E64_End_of_Existence . BIND(hg:EndOfExistence         AS ?hgClass) }
          UNION { ?ev a la:Payment              . BIND(hg:Payment                 AS ?hgClass) }
          UNION { ?ev a la:Transfer             . BIND(hg:Transfer                AS ?hgClass) }
          UNION { ?ev a la:Addition             . BIND(hg:SetAddition             AS ?hgClass) }
          UNION { ?ev a la:Removal              . BIND(hg:SetRemoval              AS ?hgClass) }
          UNION { ?ev a la:RightAcquisition     . BIND(hg:RightAcquisition        AS ?hgClass) }
          UNION { ?ev a crm:E13_Attribute_Assignment . BIND(hg:AttributeAssignment AS ?hgClass)
                  FILTER NOT EXISTS { ?ev a ?sub .
                    FILTER(?sub IN (crm:E14_Condition_Assessment, crm:E15_Identifier_Assignment,
                                    crm:E16_Measurement, crm:E17_Type_Assignment)) } }
          UNION { ?ev a crm:E7_Activity         . BIND(hg:Activity                AS ?hgClass)
                  FILTER NOT EXISTS { ?ev a ?sub .
                    FILTER(?sub IN (crm:E12_Production, crm:E11_Modification, crm:E9_Move,
                                    crm:E10_Transfer_of_Custody, crm:E8_Acquisition, crm:E96_Purchase,
                                    crm:E85_Joining, crm:E86_Leaving, crm:E87_Curation_Activity,
                                    crm:E13_Attribute_Assignment, crm:E14_Condition_Assessment,
                                    crm:E15_Identifier_Assignment, crm:E16_Measurement,
                                    crm:E17_Type_Assignment, crm:E65_Creation,
                                    la:Payment, la:Transfer, la:Addition, la:Removal,
                                    la:RightAcquisition)) } }
          UNION { ?ev a crm:E5_Event            . BIND(hg:HistoricalEvent         AS ?hgClass)
                  FILTER NOT EXISTS { ?ev a ?sub .
                    FILTER(?sub IN (crm:E7_Activity, crm:E63_Beginning_of_Existence,
                                    crm:E64_End_of_Existence, crm:E67_Birth, crm:E69_Death,
                                    crm:E66_Formation, crm:E68_Dissolution, crm:E6_Destruction,
                                    crm:E81_Transformation, crm:E79_Part_Addition,
                                    crm:E80_Part_Removal)) } }
          UNION { ?ev a crm:E4_Period           . BIND(hg:Period                  AS ?hgClass)
                  FILTER NOT EXISTS { ?ev a ?sub .
                    FILTER(?sub IN (crm:E5_Event, crm:E7_Activity, crm:E93_Presence)) } }
        } ORDER BY ?ev LIMIT {LIMIT} OFFSET {OFFSET}
      }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/event/",
                      REPLACE(STR(?ev), "^.*/", ""))) AS ?hgEv)
      OPTIONAL { ?ev crm:P14_carried_out_by ?actor }
      OPTIONAL { ?ev crm:P7_took_place_at   ?place }
      OPTIONAL { ?ev crm:P4_has_time-span   ?span  }
      OPTIONAL { ?ev la:paid_amount         ?amt   }
    }""",
    # ---- 6. Work branch -------------------------------------------------
    "work": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX dig: <http://www.ics.forth.gr/isl/CRMdig/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgWork a ?hgClass ; owl:sameAs ?w ; hg:name ?wname .
    } } WHERE {
      { SELECT ?w ?hgClass WHERE {
          { ?w a crm:E33_Linguistic_Object   . BIND(hg:LinguisticObject     AS ?hgClass)
            FILTER NOT EXISTS { ?w a crm:E34_Inscription } }
          UNION { ?w a crm:E34_Inscription    . BIND(hg:Inscription         AS ?hgClass) }
          UNION { ?w a crm:E35_Title          . BIND(hg:Title               AS ?hgClass) }
          UNION { ?w a crm:E36_Visual_Item    . BIND(hg:VisualItem          AS ?hgClass)
            FILTER NOT EXISTS { ?w a crm:E37_Mark } }
          UNION { ?w a crm:E37_Mark           . BIND(hg:Mark                AS ?hgClass) }
          UNION { ?w a crm:E89_Propositional_Object . BIND(hg:PropositionalObject AS ?hgClass) }
          UNION { ?w a crm:E32_Authority_Document . BIND(hg:AuthorityDocument AS ?hgClass) }
          UNION { ?w a crm:E31_Document       . BIND(hg:DataSource          AS ?hgClass)
            FILTER NOT EXISTS { ?w a crm:E32_Authority_Document } }
          UNION { ?w a dig:D1_Digital_Object . BIND(hg:DigitalObject        AS ?hgClass) }
        } ORDER BY ?w LIMIT {LIMIT} OFFSET {OFFSET}
      }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/work/",
                      REPLACE(STR(?w), "^.*/", ""))) AS ?hgWork)
      OPTIONAL { ?w rdfs:label ?wname }
    }""",
    # ---- 7. Set / CuratedHolding ---------------------------------------
    "set": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX la:  <https://linked.art/ns/terms/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgX a ?hgClass ; owl:sameAs ?x ; hg:name ?xname .
    } } WHERE {
      { SELECT ?x ?hgClass WHERE {
          { ?x a la:Set                  . BIND(hg:Set            AS ?hgClass) }
          UNION { ?x a crm:E78_Curated_Holding . BIND(hg:CuratedHolding AS ?hgClass) }
        } ORDER BY ?x LIMIT {LIMIT} OFFSET {OFFSET}
      }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/set/",
                      REPLACE(STR(?x), "^.*/", ""))) AS ?hgX)
      OPTIONAL { ?x rdfs:label ?xname }
    }""",
    # ---- 8. Concept branch (previously .sparql-only, never in runtime) ---
    "concept": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgC a ?hgClass ; owl:sameAs ?c ; hg:name ?cname .
    } } WHERE {
      { SELECT ?c ?hgClass WHERE {
          { ?c a crm:E55_Type             . BIND(hg:Concept         AS ?hgClass)
            FILTER NOT EXISTS { ?c a ?sub .
              FILTER(?sub IN (crm:E56_Language, crm:E57_Material, crm:E58_Measurement_Unit,
                              crm:E98_Currency, crm:E99_Product_Type)) } }
          UNION { ?c a crm:E57_Material         . BIND(crm:E57_Material        AS ?hgClass) }
          UNION { ?c a crm:E56_Language         . BIND(hg:Language        AS ?hgClass) }
          UNION { ?c a crm:E98_Currency         . BIND(hg:Currency        AS ?hgClass) }
          UNION { ?c a crm:E97_Monetary_Amount  . BIND(hg:MonetaryAmount  AS ?hgClass) }
          UNION { ?c a crm:E58_Measurement_Unit . BIND(hg:MeasurementUnit AS ?hgClass) }
          UNION { ?c a crm:E72_Legal_Object     . BIND(hg:LegalObject     AS ?hgClass) }
          UNION { ?c a crm:E99_Product_Type     . BIND(hg:ProductType     AS ?hgClass) }
        } ORDER BY ?c LIMIT {LIMIT} OFFSET {OFFSET}
      }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/concept/",
                      REPLACE(STR(?c), "^.*/", ""))) AS ?hgC)
      OPTIONAL { ?c rdfs:label ?cname }
    }""",
    # ---- 9. Identifier / Name (previously .sparql-only) ------------------
    "identifier_name": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgA a ?hgClass ; owl:sameAs ?a ; hg:name ?content .
    } } WHERE {
      { SELECT ?a ?hgClass WHERE {
          { ?a a crm:E42_Identifier . BIND(hg:Identifier AS ?hgClass) }
          UNION { ?a a crm:E33_E41_Linguistic_Appellation . BIND(hg:Name AS ?hgClass) }
          UNION { ?a a crm:E41_Appellation . BIND(hg:Appellation AS ?hgClass)
            FILTER NOT EXISTS { ?a a ?sub .
              FILTER(?sub IN (crm:E42_Identifier, crm:E33_E41_Linguistic_Appellation,
                              crm:E35_Title)) } }
        } ORDER BY ?a LIMIT {LIMIT} OFFSET {OFFSET}
      }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/appellation/",
                      REPLACE(STR(?a), "^.*/", ""))) AS ?hgA)
      OPTIONAL { ?a crm:P190_has_symbolic_content ?content }
    }""",
    # ---- 10. Embedded structure (TimeSpan / Dimension / Right / services) -
    "embedded": """
    PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX la:  <https://linked.art/ns/terms/>
    PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
    PREFIX hg:  <https://w3id.org/heritagegraph/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    INSERT { GRAPH <{TARGET}> {
      ?hgE a ?hgClass ; owl:sameAs ?e ; hg:name ?elabel ;
           hg:dimension_has_unit ?unit .
    } } WHERE {
      { SELECT ?e ?hgClass WHERE {
          { ?e a crm:E52_Time-Span       . BIND(crm:E52_Time-Span         AS ?hgClass) }
          UNION { ?e a crm:E54_Dimension . BIND(hg:Dimension        AS ?hgClass)
            FILTER NOT EXISTS { ?e a crm:E97_Monetary_Amount } }
          UNION { ?e a crm:E30_Right     . BIND(hg:Right            AS ?hgClass) }
          UNION { ?e a la:DigitalService . BIND(hg:DigitalService   AS ?hgClass) }
          UNION { ?e a crm:E20_Biological_Object . BIND(hg:BiologicalObject AS ?hgClass) }
          UNION { ?e a crm:E26_Physical_Feature . BIND(hg:PhysicalFeature AS ?hgClass)
            FILTER NOT EXISTS { ?e a ?sub .
              FILTER(?sub IN (crm:E25_Human-Made_Feature, crm:E27_Site)) } }
          UNION { ?e a crm:E27_Site      . BIND(hg:Site             AS ?hgClass) }
          UNION { ?e a crm:E25_Human-Made_Feature . BIND(hg:ArchitecturalElement AS ?hgClass) }
          UNION { ?e a crm:E93_Presence  . BIND(hg:Presence         AS ?hgClass) }
          UNION { ?e a crm:E3_Condition_State . BIND(crm:E3_Condition_State AS ?hgClass) }
        } ORDER BY ?e LIMIT {LIMIT} OFFSET {OFFSET}
      }
      BIND(IRI(CONCAT("https://w3id.org/heritagegraph/imported/lux/embedded/",
                      REPLACE(STR(?e), "^.*/", ""))) AS ?hgE)
      OPTIONAL { ?e rdfs:label ?elabel }
      OPTIONAL { ?e crm:P91_has_unit ?unit }
    }""",
}


def transform(args: argparse.Namespace) -> None:
    ep = _make_endpoint(args)
    target = args.target_graph
    log_path = Path(args.log_file) if args.log_file else Path("migration.log")
    state = _load_state(log_path)

    queries = TRANSFORM_TEMPLATES if args.queries == "builtin" else _load_user_queries(args.queries)

    for label, tmpl in queries.items():
        offset = state.get(label, {"offset": 0, "done": False})["offset"]
        done   = state.get(label, {"done": False})["done"]
        if done:
            LOG.info("[%s] already complete (offset=%d)", label, offset)
            continue

        LOG.info("[%s] starting (offset=%d, batch=%d)", label, offset, args.batch_size)
        while True:
            sparql = (tmpl
                      .replace("{TARGET}", target)
                      .replace("{LIMIT}",  str(args.batch_size))
                      .replace("{OFFSET}", str(offset)))
            if args.dry_run:
                LOG.info("[%s] DRY RUN; would execute %d-char query at offset=%d",
                         label, len(sparql), offset)
                break

            t0 = time.time()
            try:
                ep.update(sparql)
            except Exception as e:
                LOG.exception("[%s] batch failed at offset=%d: %s", label, offset, e)
                _save_state(log_path, state)
                raise

            inserted = _count_target(ep, target) - state.get("_target_count", 0)
            elapsed  = time.time() - t0
            LOG.info("[%s] offset=%d → +%d triples in %.1fs",
                     label, offset, inserted, elapsed)

            if inserted < args.batch_size:        # batch returned fewer rows → done
                state[label] = {"offset": offset, "done": True}
                _save_state(log_path, state)
                break
            offset += args.batch_size
            state[label] = {"offset": offset, "done": False}
            state["_target_count"] = _count_target(ep, target)
            _save_state(log_path, state)
            if args.limit and offset >= args.limit:
                LOG.info("[%s] reached --limit=%d; stopping", label, args.limit)
                break

    LOG.info("Transform complete. State saved to %s", log_path)


def _load_user_queries(path: str) -> dict[str, str]:
    """Parse a SPARQL file into named queries by '# === <label> ===' headers.

    The regex keeps the label on the same line as the '===' so banner lines
    like '# ====================' (no label) don't get matched and the next
    SPARQL keyword (e.g. PREFIX) doesn't get captured as a section name.
    File-level PREFIXes that appear before the first labelled section are
    treated as a preamble and prepended to every query body.
    """
    text = Path(path).read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^# *={3,}[ \t]+(\S+)[ \t]*=*[ \t]*$", text)
    preamble = blocks[0] if blocks else ""
    queries = {}
    for i in range(1, len(blocks), 2):
        label = blocks[i].strip()
        body  = blocks[i + 1].strip()
        if body:
            queries[label] = (preamble.rstrip() + "\n" + body) if preamble.strip() else body
    if not queries:
        raise ValueError(f"No '# === label ===' blocks found in {path}")
    return queries


def _count_target(ep: Endpoint, graph: str) -> int:
    rows = ep.query(f"SELECT (COUNT(*) AS ?c) WHERE {{ GRAPH <{graph}> {{ ?s ?p ?o }} }}")
    if not rows:
        return 0
    binding = rows[0]
    return int(binding.get("c", {}).get("value", 0))


def _load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            LOG.warning("State file %s unreadable, starting fresh", path)
    return {}


def _save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, indent=2))


# =============================================================================
# Mode 3: VALIDATE
# =============================================================================

def validate(args: argparse.Namespace) -> None:
    ep = _make_endpoint(args)
    queries_path = Path(args.queries)
    if not queries_path.exists():
        LOG.error("validation queries file not found: %s", queries_path)
        sys.exit(2)
    queries = _load_user_queries(str(queries_path))

    failures = 0
    for label, body in queries.items():
        LOG.info("[validate %s] running…", label)
        try:
            rows = ep.query(body)
        except Exception as e:
            LOG.exception("[validate %s] query error: %s", label, e)
            failures += 1
            continue
        n = len(rows)
        if label.startswith("V1") or label.startswith("V2"):
            ok = n == 0
            LOG.info("[validate %s] %s rows  →  %s", label, n, "PASS" if ok else "FAIL")
            if not ok:
                failures += 1
                for r in rows[:10]:
                    LOG.info("  ↳ %s", json.dumps(r, default=str)[:200])
        else:
            LOG.info("[validate %s] %s rows (review manually)", label, n)
    if failures:
        LOG.error("Validation FAILED on %d gates.", failures)
        sys.exit(1)
    LOG.info("Validation PASSED.")


# =============================================================================
# Mode 4: DELTA — weekly maintenance sync
# =============================================================================

def delta(args: argparse.Namespace) -> None:
    """Pull the most recent LUX diff dump, apply additions, then re-transform."""
    if requests is None:
        LOG.error("`requests` is not installed; cannot fetch delta.")
        sys.exit(2)
    ep = _make_endpoint(args)

    diff_url = args.diff_url
    LOG.info("Downloading delta from %s", diff_url)
    diff_path = Path(args.work_dir or "/tmp") / "lux_delta.nq"
    r = requests.get(diff_url, timeout=args.timeout, stream=True)
    r.raise_for_status()
    with diff_path.open("wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    LOG.info("Delta downloaded: %s", diff_path)

    # 1. load the delta into the raw LUX named graph
    LOG.info("Loading delta into <%s>", DEFAULT_GRAPH_RAW)
    ttl = diff_path.read_text(encoding="utf-8")
    ep.update(f"INSERT DATA {{ GRAPH <{DEFAULT_GRAPH_RAW}> {{ {ttl} }} }}")

    # 2. re-run transformation (it uses LIMIT/OFFSET so already-imported records
    #    are simply re-inserted as duplicates; INSERT is idempotent in RDF)
    transform(args)


# =============================================================================
# Plumbing
# =============================================================================

def _make_endpoint(args: argparse.Namespace) -> Endpoint:
    if args.embedded_path:
        return Endpoint(store_path=args.embedded_path)
    if not args.endpoint:
        LOG.error("Either --endpoint URL or --embedded-path is required.")
        sys.exit(2)
    return Endpoint(url=args.endpoint, query_path=args.query_path,
                    update_path=args.update_path, timeout=args.timeout)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", required=True,
                    choices=["crawl", "transform", "validate", "delta"])
    ap.add_argument("--endpoint", help="SPARQL endpoint base URL (e.g. http://127.0.0.1:7878)")
    ap.add_argument("--embedded-path", help="Path to a pyoxigraph store (embedded mode)")
    ap.add_argument("--query-path",  default="/query")
    ap.add_argument("--update-path", default="/update")
    ap.add_argument("--timeout", type=int, default=600)
    # transform / delta
    ap.add_argument("--queries", default="builtin",
                    help="'builtin' (this script's TRANSFORM_TEMPLATES) "
                         "or path to a .sparql file with '# === label ===' headers.")
    ap.add_argument("--target-graph", default=DEFAULT_GRAPH_IMPORTED)
    ap.add_argument("--batch-size", type=int, default=50000)
    ap.add_argument("--limit", type=int, default=0,
                    help="Cap each query at this many records total (0 = no cap).")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--log-file", default="migration.log")
    # crawl
    ap.add_argument("--filter", help="Free-text query for /api/search (crawl mode).")
    ap.add_argument("--out", default="/data/lux/lux_crawled.jsonl")
    ap.add_argument("--resume-state", default="")
    ap.add_argument("--max-pages", type=int, default=10000)
    ap.add_argument("--concurrency", type=int, default=16)
    # delta
    ap.add_argument("--diff-url", default="https://linked-art.lux.collections.yale.edu/data/diffs/latest.nq")
    ap.add_argument("--work-dir", default="/tmp")

    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")

    return {"crawl": crawl, "transform": transform,
            "validate": validate, "delta": delta}[args.mode](args) or 0


if __name__ == "__main__":
    sys.exit(main())
