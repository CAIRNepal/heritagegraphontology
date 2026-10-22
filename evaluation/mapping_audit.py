#!/usr/bin/env python3
"""External-mapping audit for HeritageGraph, with its negative control.

Two subcommands (default: audit):

  audit             Full-pass audit of every external mapping triple in
                    HeritageGraph.ttl and the LUX alignment module
                    (heritagegraph-lux-migration/alignment/heritagegraph-lux-alignment.ttl).
                    Enumerates all triples
                    <hg-term, mapping-predicate, external-term> for the mapping
                    predicates (skos:exactMatch / closeMatch / broadMatch /
                    relatedMatch / narrowMatch, rdfs:subClassOf,
                    rdfs:subPropertyOf, owl:equivalentClass,
                    owl:equivalentProperty) and verifies each one:
                      1. existence -- the target term is defined in its source
                         vocabulary (document-level fetch+parse, with a
                         term-level HTTP-dereference fallback);
                      2. category  -- class-valued mappings point at classes,
                         property-valued mappings at properties.
                    Additionally, every CIDOC-CRM / CRMinf / CRMsci IRI used
                    anywhere in either file (any position, not only mapping
                    targets) must be defined in the official RDFS release.
                    Targets that cannot be fetched (e.g. Getty AAT throttling)
                    can be verified by hand and recorded in
                    mapping_manual_verification.csv. Writes
                    results/mapping_audit.csv (one row per mapping) for the
                    rater's semantic-adequacy verdicts and exits non-zero if
                    any target is not in its vocabulary, any category
                    mismatches, or any CRM-family term is undefined. Network
                    fetches are cached under results/.vocab_cache.

  negative-control  Seeds the TBox with deliberately wrong mappings from four
                    failure classes and runs the same machine tier over them,
                    confirming the protocol catches nonexistent targets and
                    category mismatches (F1-F3) and, by design, cannot catch a
                    semantically wrong but category-compatible target (F4) --
                    the error class the single rater exists to catch. This is
                    why the single-rater limitation is reported as a real threat.

Run:  python3 evaluation/mapping_audit.py [audit|negative-control]
"""

from __future__ import annotations

import argparse
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
LUX = ROOT / "heritagegraph-lux-migration" / "alignment" / "heritagegraph-lux-alignment.ttl"
SOURCES = {"core": TTL, "lux": LUX}
MANUAL = Path(__file__).resolve().parent / "mapping_manual_verification.csv"
CRM_FAMILY = ("http://www.cidoc-crm.org/cidoc-crm/",
              "http://www.cidoc-crm.org/extensions/crminf/",
              "http://www.cidoc-crm.org/extensions/crmsci/")
RESULTS = Path(__file__).resolve().parent / "results"
CACHE = RESULTS / ".vocab_cache"
CACHE.mkdir(parents=True, exist_ok=True)

HG = "https://cair-nepal.org/heritagegraph/"
CRM = "http://www.cidoc-crm.org/cidoc-crm/"
MAPPING_PREDS = [SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
                 SKOS.relatedMatch, SKOS.narrowMatch,
                 RDFS.subClassOf, RDFS.subPropertyOf,
                 OWL.equivalentClass, OWL.equivalentProperty]

# vocabularies checkable at document level: prefix -> (fetch URL, format)
DOCS = {
    "http://www.cidoc-crm.org/cidoc-crm/":
        ("http://www.cidoc-crm.org/cidoc-crm/", "xml"),
    "http://www.cidoc-crm.org/extensions/crminf/":
        ("https://cidoc-crm.org/extensions/crminf/rdfs/1.0/CRMinf_v1.0.rdf", "xml"),
    "http://www.cidoc-crm.org/extensions/crmsci/":
        ("https://cidoc-crm.org/extensions/crmsci/rdfs/2.0/CRMsci_v2.0.rdf", "xml"),
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
        # Getty rejects HEAD on term URIs and throttles bursts (HTTP 499/429):
        # try several representations with back-off before giving up.
        import time
        status = ""
        for attempt in range(2):  # first try + one retry
            for probe in (uri + ".json", uri + ".rdf",
                          uri.replace("http://", "https://") + ".json"):
                try:
                    req = urllib.request.Request(probe, headers={
                        "User-Agent": "heritagegraph-audit/1.0 (ontology mapping audit)",
                        "Accept": "application/json, application/rdf+xml;q=0.9, */*;q=0.1"})
                    resp = urllib.request.urlopen(req, timeout=60, context=SSL_CTX)
                    return f"http:{resp.status}"
                except urllib.error.HTTPError as e:
                    status = f"http:{e.code}"
                    if e.code == 404:
                        return status
                except Exception as e:
                    status = f"http-error:{e}"
            time.sleep(5 * (attempt + 1))
        return status
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


LINKED_ART_CONTEXT = "https://linked.art/ns/v1/linked-art.json"
LINKED_ART_NS = ("http://www.ics.forth.gr/isl/CRMdig/", "http://www.ics.forth.gr/isl/CRMsci/",
                 "https://linked.art/ns/terms/")


def linked_art_terms() -> set[str]:
    """IRIs the Linked Art JSON-LD context maps its terms to. CRMdig and CRMsci
    (FORTH namespaces) and la: terms are verified here: they are the IRIs LUX data
    carries, and the FORTH CRMdig IRIs do not dereference."""
    import json
    data = fetch(LINKED_ART_CONTEXT, "linked-art-context.json")
    if data is None:
        return set()
    ctx = json.loads(data)["@context"]
    prefixes = {k: v for k, v in ctx.items() if isinstance(v, str) and v.endswith(("/", "#"))}
    out = set()

    def walk(c):
        for v in c.values():
            iri = v.get("@id") if isinstance(v, dict) else v if isinstance(v, str) else None
            if isinstance(iri, str) and ":" in iri:
                p, _, local = iri.partition(":")
                out.add(prefixes[p] + local if p in prefixes else iri)
            if isinstance(v, dict) and isinstance(v.get("@context"), dict):
                walk(v["@context"])
    walk(ctx)
    return out


def manual_verdicts() -> dict[str, str]:
    """target IRI -> verdict ('exists' / 'missing') recorded by hand."""
    if not MANUAL.exists():
        return {}
    with open(MANUAL, encoding="utf-8") as f:
        return {r["target"]: r["verdict"].strip().lower()
                for r in csv.DictReader(f) if r.get("target")}


def run_audit() -> int:
    graphs = {}
    for name, path in SOURCES.items():
        g = Graph()
        g.parse(path, format="turtle")
        graphs[name] = g
    tbox = graphs["core"] + graphs["lux"]
    hg_classes = set(tbox.subjects(RDF.type, OWL.Class))
    hg_props = (set(tbox.subjects(RDF.type, OWL.ObjectProperty))
                | set(tbox.subjects(RDF.type, OWL.DatatypeProperty)))

    mappings = []
    for source, g in graphs.items():
        for pred in MAPPING_PREDS:
            for s, o in g.subject_objects(pred):
                if (str(s).startswith(HG) and isinstance(o, URIRef)
                        and not str(o).startswith(HG)):
                    mappings.append((source, s, pred, o))
    mappings.sort(key=lambda m: (m[0], str(m[2]), str(m[1])))
    print(f"External mapping triples: {len(mappings)} "
          f"(core {sum(m[0] == 'core' for m in mappings)}, "
          f"LUX module {sum(m[0] == 'lux' for m in mappings)})")
    manual = manual_verdicts()
    la_terms = None

    vocabs: dict[str, Graph | None] = {}
    rows = []
    for source, s, p, o in mappings:
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
        if exists == "unverified" and target.startswith(LINKED_ART_NS):
            if la_terms is None:
                la_terms = linked_art_terms()
            if target in la_terms:
                exists = "defined"
        if exists in ("unverified", "NOT-IN-VOCAB"):
            status = http_exists(target)
            if status.startswith("http:2") or status.startswith("http:3"):
                exists = exists if exists == "NOT-IN-VOCAB" else "resolves"
            elif exists == "unverified":
                exists = f"unreachable({status})"
        if exists.startswith("unreachable") and target in manual:
            exists = ("verified-manually" if manual[target] == "exists"
                      else "NOT-IN-VOCAB")

        subj_kind = "class" if s in hg_classes else ("property" if s in hg_props else "other")
        kind_ok = (kind == "" or kind == "other" or kind == subj_kind)
        rows.append({
            "source": source,
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
    n_man = sum(r["target_exists"] == "verified-manually" for r in rows)
    n_miss = sum(r["target_exists"] == "NOT-IN-VOCAB" for r in rows)
    n_unv = len(rows) - n_def - n_man - n_miss
    n_kind = sum(r["category_ok"] == "MISMATCH" for r in rows)
    print(f"targets defined/resolving: {n_def}, not in vocabulary: {n_miss}, "
          f"unverified: {n_unv}, category mismatches: {n_kind}")
    print(f"Breakdown: audited {len(rows)}; verified automatically {n_def}; "
          f"verified manually {n_man}; failed {n_miss + n_kind} "
          f"({n_miss} not in vocabulary, {n_kind} category mismatches); "
          f"still unverified {n_unv}")
    for r in rows:
        if r["target_exists"].startswith("unreachable"):
            print(f"  unverified: {r['source']}: {r['subject']} {r['predicate']} "
                  f"{r['target']}  [{r['target_exists']}]")
        if r["target_exists"] == "NOT-IN-VOCAB" or r["category_ok"] == "MISMATCH":
            print(f"  FAILED:     {r['source']}: {r['subject']} {r['predicate']} "
                  f"{r['target']}  [{r['target_exists']}, category {r['category_ok']}]")

    # CRM-family term inventory: any position, both files.
    undefined = []
    for prefix in CRM_FAMILY:
        if prefix not in vocabs:
            vocabs[prefix] = load_vocab(prefix)
        vg = vocabs[prefix]
        used = {x for g in graphs.values() for t in g for x in t
                if isinstance(x, URIRef) and str(x).startswith(prefix) and str(x) != prefix}
        if vg is None:
            print(f"  [warn] cannot load {prefix}; {len(used)} term(s) unchecked")
            undefined.append(f"{prefix} (vocabulary not loadable)")
            continue
        missing = sorted(str(x) for x in used if (x, None, None) not in vg)
        print(f"CRM-family inventory {prefix}: {len(used)} term(s) used, "
              f"{len(used) - len(missing)} defined in the official RDFS")
        for m in missing:
            print(f"  UNDEFINED: {m}")
        undefined += missing
    print(f"Report: {out}")
    return 1 if (n_miss or n_kind or undefined) else 0


def run_negative_control() -> int:
    SEEDS = [
        ("F1 nonexistent target",
         URIRef(HG + "Temple"), SKOS.broadMatch,
         URIRef(CRM + "E999_Nonexistent_Class"), "NOT-IN-VOCAB"),
        ("F2 class mapped to a property",
         URIRef(HG + "Temple"), SKOS.broadMatch,
         URIRef(CRM + "P4_has_time-span"), "CATEGORY-MISMATCH"),
        ("F3 property mapped to a class",
         URIRef(HG + "performsRitual"), RDFS.subPropertyOf,
         URIRef(CRM + "E5_Event"), "CATEGORY-MISMATCH"),
        ("F5 non-existent CRM term (former LUX target)",
         URIRef(HG + "CalendarSystem"), SKOS.broadMatch,
         URIRef(CRM + "E29_Designated_Reference_System"), "NOT-IN-VOCAB"),
        ("F4 wrong but category-compatible",
         URIRef(HG + "Temple"), SKOS.broadMatch,
         URIRef(CRM + "E39_Actor"), "UNDETECTED (rater tier only)"),
    ]

    tbox = Graph()
    tbox.parse(ROOT / "ontology" / "HeritageGraph.ttl", format="turtle")
    hg_classes = set(tbox.subjects(RDF.type, OWL.Class))
    hg_props = (set(tbox.subjects(RDF.type, OWL.ObjectProperty))
                | set(tbox.subjects(RDF.type, OWL.DatatypeProperty)))

    crm_vocab = load_vocab(CRM)
    if crm_vocab is None:
        print("FATAL: cannot load the CIDOC-CRM vocabulary document "
              "(network needed on first run; cached afterwards).")
        return 2

    print("Machine tier of the audit protocol, applied to seeded faulty mappings")
    print(f"{'seed':<36}{'verdict':<22}expected")
    ok = True
    for label, s, p, o, expected in SEEDS:
        defined = (o, None, None) in crm_vocab
        if not defined:
            verdict = "NOT-IN-VOCAB"
        else:
            types = set(crm_vocab.objects(o, RDF.type))
            kind = ("class" if types & CLASS_TYPES
                    else "property" if types & PROP_TYPES else "other")
            subj_kind = ("class" if s in hg_classes
                         else "property" if s in hg_props else "other")
            verdict = ("CATEGORY-MISMATCH" if kind in ("class", "property")
                       and kind != subj_kind else "UNDETECTED (rater tier only)")
        match = verdict == expected
        ok &= match
        print(f"{label:<36}{verdict:<22}{expected}  [{'OK' if match else 'FAIL'}]")

    if ok:
        print("\nPASS (as pre-registered): the machine tier catches nonexistent "
              "targets and category mismatches (F1-F3) and, by design, cannot "
              "catch a semantically wrong but category-compatible target (F4). "
              "F4-class errors are exactly what the rater tier exists for; the "
              "single-rater limitation therefore remains a real, reported threat.")
        return 0
    print("\nFAIL: at least one seed produced an unexpected verdict.")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", nargs="?", default="audit",
                        choices=["audit", "negative-control"],
                        help="which pass to run (default: audit)")
    args = parser.parse_args()
    return run_audit() if args.mode == "audit" else run_negative_control()


if __name__ == "__main__":
    raise SystemExit(main())
