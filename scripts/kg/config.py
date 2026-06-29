"""Shared configuration for the HeritageGraph KG build pipeline.

Schema/TBox namespace stays on w3id.org (published, best practice).
Instance/ABox IRIs are minted under a CAIR-Nepal domain the project controls.
"""
from pathlib import Path

# --- namespaces -----------------------------------------------------------
HG     = "https://cair-nepal.org/heritagegraph/"            # schema (classes/props)
BASE   = "https://data.cair-nepal.org/heritagegraph/" # instance base
IDNS   = BASE + "id/"                                  # minted entity IRIs
SRCNS  = BASE + "source/"                              # DataSource IRIs
GRAPH  = BASE + "graph/"                               # named graph IRIs

CRM     = "http://www.cidoc-crm.org/cidoc-crm/"
CRMINF  = "http://www.cidoc-crm.org/extensions/crminf/"
DCT     = "http://purl.org/dc/terms/"
DATACITE= "http://purl.org/spar/datacite/"
GEO     = "http://www.opengis.net/ont/geosparql#"
PROV    = "http://www.w3.org/ns/prov#"
SKOS    = "http://www.w3.org/2004/02/skos/core#"
TIME    = "http://www.w3.org/2006/time#"
OWL     = "http://www.w3.org/2002/07/owl#"
RDFS    = "http://www.w3.org/2000/01/rdf-schema#"
XSD     = "http://www.w3.org/2001/XMLSchema#"

PREFIXES = {
    "hg": HG, "hgd": IDNS, "hgsrc": SRCNS, "crm": CRM, "crminf": CRMINF,
    "dct": DCT, "datacite": DATACITE, "geo": GEO, "prov": PROV, "skos": SKOS,
    "time": TIME, "owl": OWL, "rdfs": RDFS, "xsd": XSD,
    "wd": "http://www.wikidata.org/entity/",
    "osm": "https://www.openstreetmap.org/",
    "danam": "https://danam.cats.uni-heidelberg.de/report/",
}

# --- paths ----------------------------------------------------------------
ROOT   = Path(__file__).resolve().parents[2]
RAW    = ROOT / "data" / "raw"
KG     = ROOT / "data" / "kg"
RAW.mkdir(parents=True, exist_ok=True)
KG.mkdir(parents=True, exist_ok=True)

# --- HTTP -----------------------------------------------------------------
USER_AGENT = "HeritageGraphKG/1.0 (https://cair-nepal.org; info@cair-nepal.org)"
WDQS    = "https://query.wikidata.org/sparql"
OVERPASS= "https://overpass-api.de/api/interpreter"

# --- source / dataset metadata (provenance) -------------------------------
SOURCES = {
    "wikidata": {
        "iri": SRCNS + "wikidata",
        "label": "Wikidata",
        "url": "https://www.wikidata.org/",
        "license": "CC0-1.0",
        "epistemic_stance": "Scholarly",
        "source_type": "PublishedScholarship",
        "graph": GRAPH + "wikidata",
    },
    "osm": {
        "iri": SRCNS + "openstreetmap",
        "label": "OpenStreetMap",
        "url": "https://www.openstreetmap.org/",
        "license": "ODbL-1.0",
        "epistemic_stance": "Community",
        "source_type": "CommunityNarrative",
        "graph": GRAPH + "openstreetmap",
    },
    "unesco": {
        "iri": SRCNS + "unesco-whc",
        "label": "UNESCO World Heritage Centre",
        "url": "https://whc.unesco.org/",
        "license": "Attribution (UNESCO WHC)",
        "epistemic_stance": "State",
        "source_type": "PublishedScholarship",
        "graph": GRAPH + "unesco",
    },
    # DANAM is NON-COMMERCIAL / academic, citation-required (Brosius & Michaels,
    # eds.). Its named graph is kept separate and must NOT be relicensed into the
    # CC BY AWS Open Data release. See DISCOVERY_DANAM.md (Phase 0, option B).
    "danam": {
        "iri": SRCNS + "danam",
        "label": "DANAM — Nepal Heritage Documentation Project (Heidelberg)",
        "url": "https://danam.cats.uni-heidelberg.de/",
        "license": ("Non-commercial academic/educational use only. Cite: "
                    "Christiane Brosius and Axel Michaels (eds.), Nepal Heritage "
                    "Documentation Project (https://danam.cats.uni-heidelberg.de)."),
        "epistemic_stance": "Scholarly",
        "source_type": "PublishedScholarship",
        "graph": GRAPH + "danam",
    },
}

# DANAM required attribution string (embedded in the provenance note).
DANAM_CITATION = ("Christiane Brosius and Axel Michaels (eds.), Nepal Heritage "
                  "Documentation Project (DANAM), "
                  "https://danam.cats.uni-heidelberg.de")
