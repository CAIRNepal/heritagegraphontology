#!/usr/bin/env python3
"""Publish HeritageGraph's mappings to other vocabularies as an SSSOM mapping set.

    python3 scripts/gen_sssom.py            # write ontology/mappings/HeritageGraph.sssom.tsv
    python3 scripts/gen_sssom.py --check    # gate: the committed file is up to date

One row per mapping from a HeritageGraph term to an external term, read from
the released core (skos:exactMatch/closeMatch/broadMatch/narrowMatch/
relatedMatch, and rdfs:subClassOf/subPropertyOf to an external term) and
from the LUX alignment module (the same predicates, plus owl:equivalentClass/
equivalentProperty). The mappings were curated by hand by the ontology's
authors (the rationale is kept as comments in ontology/HeritageGraph.yaml and
the module), so mapping_justification is semapv:ManualMappingCuration.
reviewer_label is set only when an independent rater has accepted the mapping in
evaluation/mapping_rater_verdicts.csv (verdict accept / reject / revise); a rejected mapping
is left out of the SSSOM set (it stays in the ontology until its authors change it), and the generator never fills in a verdict itself. Deprecated terms
are skipped, and a mapping stated in both the core and the LUX module is one row.
"""
from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

from rdflib import Graph, OWL, RDFS, URIRef
from rdflib.namespace import SKOS

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "ontology" / "HeritageGraph.ttl"
LUX = ROOT / "heritagegraph-lux-migration" / "alignment" / "heritagegraph-lux-alignment.ttl"
RATER = ROOT / "evaluation" / "mapping_rater_verdicts.csv"
OUT = ROOT / "ontology" / "mappings" / "HeritageGraph.sssom.tsv"
HG = "https://cair-nepal.org/heritagegraph/"

CURIE_MAP = {
    "hg": HG,
    "crm": "http://www.cidoc-crm.org/cidoc-crm/",
    "crminf": "http://www.cidoc-crm.org/extensions/crminf/",
    "crmsci": "http://www.cidoc-crm.org/extensions/crmsci/",
    "prov": "http://www.w3.org/ns/prov#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "aat": "http://vocab.getty.edu/aat/",
    "wikidata": "http://www.wikidata.org/entity/",
    "schema": "http://schema.org/",
    "dbo": "http://dbpedia.org/ontology/",
    "rico": "https://www.ica.org/standards/RiC/ontology#",
    "la": "https://linked.art/ns/terms/",
    "dcterms": "http://purl.org/dc/terms/",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "time": "http://www.w3.org/2006/time#",
    "semapv": "https://w3id.org/semapv/vocab/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "sci": "http://www.ics.forth.gr/isl/CRMsci/",
    "dig": "http://www.ics.forth.gr/isl/CRMdig/",
    "lclabel": "https://localcontexts.org/label/",
}
PREDICATES = {
    SKOS.exactMatch: "skos:exactMatch", SKOS.closeMatch: "skos:closeMatch",
    SKOS.broadMatch: "skos:broadMatch", SKOS.narrowMatch: "skos:narrowMatch",
    SKOS.relatedMatch: "skos:relatedMatch", RDFS.subClassOf: "rdfs:subClassOf",
    RDFS.subPropertyOf: "rdfs:subPropertyOf", OWL.equivalentClass: "owl:equivalentClass",
    OWL.equivalentProperty: "owl:equivalentProperty",
}
COLUMNS = ["subject_id", "subject_label", "predicate_id", "object_id", "mapping_justification",
           "author_label", "reviewer_label", "comment"]


def curie(u: URIRef) -> str:
    s = str(u)
    for p, ns in sorted(CURIE_MAP.items(), key=lambda kv: -len(kv[1])):
        if s.startswith(ns) and s != ns:
            return f"{p}:{s[len(ns):]}"
    return s


def mappings(g: Graph, labels: Graph):
    for pred, pid in PREDICATES.items():
        for s, o in g.subject_objects(pred):
            if not (isinstance(s, URIRef) and isinstance(o, URIRef)):
                continue
            if not str(s).startswith(HG) or str(o).startswith(HG):
                continue  # HeritageGraph term -> external term only
            if (s, OWL.deprecated, None) in labels or (s, OWL.deprecated, None) in g:
                continue  # deprecated terms are not mapped anew
            label = next((str(l) for src in (labels, g) for l in src.objects(s, RDFS.label)
                          if getattr(l, "language", None) in ("en", None)), "")
            yield curie(s), label, pid, curie(o)


def rater_verdicts() -> dict:
    if not RATER.exists():
        return {}
    with open(RATER, newline="", encoding="utf-8") as f:
        return {(r["subject_id"], r["predicate_id"], r["object_id"]): r
                for r in csv.DictReader(f) if r.get("verdict", "").strip()}


def build() -> str:
    core = Graph().parse(CORE, format="turtle")
    lux = Graph().parse(LUX, format="turtle")
    verdicts = rater_verdicts()
    sources: dict = {}
    for row in mappings(core, core):
        sources.setdefault(row, set()).add("core")
    for row in mappings(lux, core):
        sources.setdefault(row, set()).add("LUX module")
    rows = sorted(sources)
    out = io.StringIO()
    out.write("# mapping_set_id: https://cair-nepal.org/heritagegraph/mappings/HeritageGraph.sssom.tsv\n")
    out.write("# mapping_set_description: Mappings from HeritageGraph terms (core and the LUX alignment module) "
              "to external vocabularies.\n")
    out.write("# license: https://creativecommons.org/licenses/by/4.0/\n")
    out.write("# curie_map:\n")
    for p, ns in CURIE_MAP.items():
        out.write(f"#   {p}: {ns}\n")
    w = csv.writer(out, delimiter="\t", lineterminator="\n")
    w.writerow(COLUMNS)
    for sid, label, pid, oid in rows:
        v = verdicts.get((sid, pid, oid), {})
        verdict = v.get("verdict", "").strip().lower()
        if verdict and verdict not in ("accept", "reject", "revise"):
            print(f"WARNING: unknown rater verdict {verdict!r} for {sid} {pid} {oid} "
                  f"(use accept, reject or revise); published without a reviewer", file=sys.stderr)
        if verdict == "reject":
            continue  # a rater rejected the mapping: not published
        comment = "stated in: " + ", ".join(sorted(sources[(sid, label, pid, oid)]))
        if verdict:
            comment += f"; rater verdict: {verdict}" + (f" ({v['note']})" if v.get("note") else "")
        w.writerow([sid, label, pid, oid, "semapv:ManualMappingCuration",
                    "HeritageGraph authors (CAIR-Nepal)",
                    v.get("rater", "") if verdict == "accept" else "", comment])
    return out.getvalue()


def main() -> int:
    text = build()
    n = text.count("\n") - text.count("\n#") - 2
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"STALE: {OUT.relative_to(ROOT)} differs from the ontology's mappings; "
                  f"run python3 scripts/gen_sssom.py", file=sys.stderr)
            return 1
        print(f"OK: {OUT.name} is up to date ({n} mappings)")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({n} mappings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
