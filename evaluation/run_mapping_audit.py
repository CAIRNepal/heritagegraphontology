#!/usr/bin/env python3
"""Full-pass audit of every external mapping triple in HeritageGraph.ttl.

Enumerates all triples <hg-term, mapping-predicate, external-term> for the
mapping predicates (skos:exactMatch / closeMatch / broadMatch,
rdfs:subClassOf, rdfs:subPropertyOf) and verifies each one:

1. existence  — the target term is defined in its source vocabulary
   (document-level: fetch and parse the vocabulary, check the term occurs
   as a subject; term-level fallback: HTTP status of the dereferenced URI);
2. category   — class-valued mappings point at classes, property-valued
   mappings at properties (checked where the vocabulary document is parsed).

Results land in results/mapping_audit.csv with one row per mapping for
manual (rater) verdicts. Network fetches are cached under results/.vocab_cache.
"""

from __future__ import annotations

import csv
import ssl
import sys
import urllib.request
from pathlib import Path

import certifi

SSL_CTX = ssl.create_default_context(cafile=certifi.where())

from rdflib import Graph, OWL, RDF, RDFS, SKOS, URIRef

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
RESULTS = Path(__file__).resolve().parent / "results"
CACHE = RESULTS / ".vocab_cache"
CACHE.mkdir(parents=True, exist_ok=True)

HG = "https://w3id.org/heritagegraph/"
MAPPING_PREDS = [SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
                 SKOS.relatedMatch, SKOS.narrowMatch,
                 RDFS.subClassOf, RDFS.subPropertyOf]

# vocabularies checkable at document level: prefix -> (fetch URL, format)
DOCS = {
    "http://www.cidoc-crm.org/cidoc-crm/":
        ("http://www.cidoc-crm.org/cidoc-crm/", "xml"),
    "http://www.cidoc-crm.org/extensions/crminf/":
        ("http://www.cidoc-crm.org/extensions/crminf/", "xml"),
    "http://www.cidoc-crm.org/extensions/crmsci/":
        ("http://www.cidoc-crm.org/extensions/crmsci/", "xml"),
    "http://www.w3.org/ns/prov#": ("http://www.w3.org/ns/prov.ttl", "turtle"),
    "http://www.w3.org/2006/time#": ("http://www.w3.org/2006/time.ttl", "turtle"),
    "http://www.w3.org/2004/02/skos/core#":
        ("http://www.w3.org/2004/02/skos/core.rdf", "xml"),
    "http://www.opengis.net/ont/geosparql#":
        ("http://schemas.opengis.net/geosparql/1.0/geosparql_vocab_all.rdf", "xml"),
    "http://purl.org/dc/terms/":
        ("https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_terms.ttl", "turtle"),
    "http://purl.org/spar/datacite/": ("http://purl.org/spar/datacite.ttl", "turtle"),
    "http://xmlns.com/foaf/0.1/": ("http://xmlns.com/foaf/spec/index.rdf", "xml"),
    "http://www.europeana.eu/schemas/edm/":
        ("https://www.europeana.eu/schemas/edm/", "xml"),
    "https://schema.org/":
        ("https://schema.org/version/latest/schemaorg-current-https.ttl", "turtle"),
    "http://schema.org/":
        ("https://schema.org/version/latest/schemaorg-current-http.ttl", "turtle"),
}

CLASS_TYPES = {OWL.Class, RDFS.Class}
PROP_TYPES = {OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty,
              RDF.Property, URIRef("http://www.w3.org/2002/07/owl#FunctionalProperty")}


def fetch(url: str, name: str) -> bytes | None:
    path = CACHE / name
    if path.exists():
        return path.read_bytes()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "heritagegraph-audit/1.0",
                                                   "Accept": "application/rdf+xml, text/turtle;q=0.9, */*;q=0.1"})
        data = urllib.request.urlopen(req, timeout=60, context=SSL_CTX).read()
        path.write_bytes(data)
        return data
    except Exception as exc:
        print(f"  [warn] cannot fetch {url}: {exc}", file=sys.stderr)
        return None


def load_vocab(prefix: str) -> Graph | None:
    url, fmt = DOCS[prefix]
    data = fetch(url, prefix.replace("/", "_").replace(":", "") + "." + fmt)
    if data is None:
        return None
    g = Graph()
    try:
        g.parse(data=data, format=fmt)
        return g
    except Exception as exc:
        print(f"  [warn] cannot parse {url}: {exc}", file=sys.stderr)
        return None


def http_exists(uri: str) -> str:
    """Term-level fallback: dereference the URI, report the HTTP status."""
    probe = uri
    if uri.startswith("http://www.wikidata.org/entity/"):
        probe = ("https://www.wikidata.org/wiki/Special:EntityData/"
                 + uri.rsplit("/", 1)[1] + ".json")
    elif uri.startswith("http://vocab.getty.edu/"):
        probe = uri + ".json"  # Getty rejects HEAD on term URIs
    try:
        req = urllib.request.Request(probe, method="GET",
                                     headers={"User-Agent": "heritagegraph-audit/1.0",
                                              "Accept": "*/*"})
        resp = urllib.request.urlopen(req, timeout=30, context=SSL_CTX)
        return f"http:{resp.status}"
    except urllib.error.HTTPError as e:
        if e.code in (405, 406):  # HEAD not allowed: retry GET
            try:
                req = urllib.request.Request(probe, headers={"User-Agent": "heritagegraph-audit/1.0"})
                resp = urllib.request.urlopen(req, timeout=30, context=SSL_CTX)
                return f"http:{resp.status}"
            except Exception as e2:
                return f"http-error:{e2}"
        return f"http:{e.code}"
    except Exception as e:
        return f"http-error:{e}"


def main() -> int:
    tbox = Graph()
    tbox.parse(TTL, format="turtle")
    hg_classes = set(tbox.subjects(RDF.type, OWL.Class))
    hg_props = (set(tbox.subjects(RDF.type, OWL.ObjectProperty))
                | set(tbox.subjects(RDF.type, OWL.DatatypeProperty)))

    mappings = []
    for pred in MAPPING_PREDS:
        for s, o in tbox.subject_objects(pred):
            if (str(s).startswith(HG) and isinstance(o, URIRef)
                    and not str(o).startswith(HG)):
                mappings.append((s, pred, o))
    mappings.sort(key=lambda m: (str(m[1]), str(m[0])))
    print(f"External mapping triples: {len(mappings)}")

    vocabs: dict[str, Graph | None] = {}
    rows = []
    for s, p, o in mappings:
        target = str(o)
        prefix = next((pf for pf in DOCS if target.startswith(pf)), None)
        exists, kind = "unverified", ""
        if prefix:
            if prefix not in vocabs:
                vocabs[prefix] = load_vocab(prefix)
            vg = vocabs[prefix]
            if vg is not None:
                defined = (o, None, None) in vg
                exists = "defined" if defined else "NOT-IN-VOCAB"
                if defined:
                    types = set(vg.objects(o, RDF.type))
                    if types & CLASS_TYPES:
                        kind = "class"
                    elif types & PROP_TYPES:
                        kind = "property"
                    else:
                        kind = "other"
        if exists in ("unverified", "NOT-IN-VOCAB"):
            status = http_exists(target)
            if status.startswith("http:2") or status.startswith("http:3"):
                exists = exists if exists == "NOT-IN-VOCAB" else "resolves"
            elif exists == "unverified":
                exists = f"unreachable({status})"

        subj_kind = "class" if s in hg_classes else ("property" if s in hg_props else "other")
        kind_ok = (kind == "" or kind == "other" or kind == subj_kind)
        rows.append({
            "subject": str(s).replace(HG, "hg:"),
            "predicate": str(p).split("#")[-1].split("/")[-1],
            "target": target,
            "subject_kind": subj_kind,
            "target_kind": kind or "n/a",
            "target_exists": exists,
            "category_ok": "yes" if kind_ok else "MISMATCH",
            "rater_verdict": "",
        })

    out = RESULTS / "mapping_audit.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    n_def = sum(r["target_exists"] in ("defined", "resolves") for r in rows)
    n_miss = sum(r["target_exists"] == "NOT-IN-VOCAB" for r in rows)
    n_unv = len(rows) - n_def - n_miss
    n_kind = sum(r["category_ok"] == "MISMATCH" for r in rows)
    print(f"targets defined/resolving: {n_def}, not in vocabulary: {n_miss}, "
          f"unverified: {n_unv}, category mismatches: {n_kind}")
    print(f"Report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
