#!/usr/bin/env python3
"""Refresh stale Widoco HTML metadata from HeritageGraph.yaml / HeritageGraph.ttl."""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml
from rdflib import Graph, Namespace, RDF

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SCHEMA = ROOT / "ontology" / "HeritageGraph.yaml"
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
ONTOLOGY_IRI = "https://w3id.org/heritagegraph/ontology"
LICENSE = "https://creativecommons.org/licenses/by/4.0/"
REPO = "https://github.com/CAIRNepal/heritagegraphontology"

OWL = Namespace("http://www.w3.org/2002/07/owl#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
DCT = Namespace("http://purl.org/dc/terms/")
PAV = Namespace("http://purl.org/pav/")


def load_meta() -> dict[str, str]:
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    g = Graph()
    g.parse(TTL, format="turtle")
    ont = None
    for s, _, _ in g.triples((None, RDF.type, OWL.Ontology)):
        ont = s
        break
    label = str(g.value(ont, RDFS.label, default=schema.get("name", "HeritageGraph")))
    version = str(g.value(ont, PAV.version, default=schema.get("version", "1.0.0")))
    title = str(g.value(ont, DCT.title, default=f"{label} Ontology"))
    description = schema.get("description", "").strip()
    return {
        "iri": ONTOLOGY_IRI,
        "label": label,
        "title": title,
        "version": version,
        "description": description,
        "license": LICENSE,
        "repo": REPO,
        "date": date.today().isoformat(),
    }


def patch_index_html(meta: dict[str, str]) -> None:
    path = DOCS / "index.html"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "url": meta["iri"],
        "image": f"https://cairnepal.github.io/heritagegraphontology/webvowl/index.html#iri=ontology.json",
        "name": meta["title"],
        "headline": f"Documentation for {meta['title']}",
        "dateReleased": meta["date"],
        "version": meta["version"],
    }
    text = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        f'<script type="application/ld+json">{json.dumps(ld)}</script>',
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = re.sub(r"<dt>Revision:</dt>\s*<dd>.*?</dd>", f"<dt>Revision:</dt>\n<dd>{meta['version']}</dd>", text)
    text = re.sub(
        r'<a href="http://insertlicenseURIhere\.example\.org"',
        f'<a href="{meta["license"]}"',
        text,
    )
    text = re.sub(
        r"<dd> Revision: .*?</dd>",
        f"<dd>{meta['title']}, version {meta['version']}. Namespace: <a href=\"{meta['iri']}\">{meta['iri']}</a>. "
        f"Source: <a href=\"{meta['repo']}\">{meta['repo']}</a>.</dd>",
        text,
    )
    path.write_text(text, encoding="utf-8")
    print(f"Patched {path}")


def write_section(path: Path, heading: str, body: str) -> None:
    html = (
        f'<h2>{heading}</h2><span class="markdown">\n'
        f"{body}</span>\n"
    )
    path.write_text(html, encoding="utf-8")
    print(f"Wrote {path}")


def patch_webvowl_header(meta: dict[str, str]) -> None:
    for rel in ("docs/webvowl/data/ontology.json", "webvowl/data/ontology.json"):
        path = ROOT / rel
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("header", {})
        data["header"]["iri"] = meta["iri"]
        data["header"]["baseIris"] = ["https://w3id.org/heritagegraph", "http://www.w3.org/2000/01/rdf-schema", "http://www.w3.org/2001/XMLSchema"]
        data["header"].setdefault("labels", {})["undefined"] = meta["label"]
        other = data["header"].setdefault("other", {})
        other["definition"] = [{"identifier": "definition", "language": "undefined", "value": meta["description"], "type": "label"}]
        other["version"] = [{"identifier": "version", "language": "undefined", "value": meta["version"], "type": "label"}]
        other["license"] = [{"identifier": "license", "language": "undefined", "value": "CC-BY-4.0", "type": "label"}]
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Patched WebVOWL header in {path}")


def main() -> int:
    if not TTL.exists():
        print(f"Missing {TTL}", file=sys.stderr)
        return 1
    meta = load_meta()
    patch_index_html(meta)
    write_section(
        DOCS / "sections" / "abstract-en.html",
        "Abstract",
        meta["description"],
    )
    intro = (
        f"<em>{meta['label']}</em> ({meta['iri']}) is an event-centric ontology for Nepalese living heritage, "
        "aligned with CIDOC-CRM, CRMinf, PROV-O, GeoSPARQL, OWL-Time, and Europeana EDM. "
        "It models temples, rituals, Guthi institutions, syncretic deity relations, and assertion-level provenance "
        "for multi-vocal heritage knowledge graphs. "
        f"Release version {meta['version']}. Source and evaluation artefacts: {meta['repo']}."
    )
    intro_path = DOCS / "sections" / "introduction-en.html"
    intro_path.write_text(
        '<h2 id="intro" class="list">Introduction <span class="backlink"> back to <a href="#toc">ToC</a></span></h2>\n'
        f'<span class="markdown">\n{intro}</span>\n',
        encoding="utf-8",
    )
    print(f"Wrote {intro_path}")
    patch_webvowl_header(meta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
