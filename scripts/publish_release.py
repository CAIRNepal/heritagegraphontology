#!/usr/bin/env python3
"""Write the immutable per-release copy of the ontology served at its version IRI.

The version IRI (e.g. http://cair-nepal.org/heritagegraph/ontology/1.0.0) must
return that exact release's files, independent of later releases. This script
reads ontology/HeritageGraph.ttl, takes the version from its owl:versionIRI,
and writes <docs>/releases/<version>/ontology.{ttl,owl,nt,jsonld} plus a small
index.html linking them (deploy/nginx/heritagegraph.conf routes the version
IRI there). Once the release is tagged in git (v<version> or <version>), it
refuses to overwrite the copy with different content unless --force is given,
so a published release cannot change silently (dcterms:modified, which the
pipeline stamps on every run, is ignored). Before the tag, the copy tracks the
release candidate.

Run: python3 scripts/publish_release.py [docs-dir] [--force]   (default: ./docs)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from rdflib import Graph, OWL, RDF
from rdflib.namespace import DCTERMS
from rdflib.compare import isomorphic

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
FORMATS = {"ttl": "turtle", "owl": "xml", "nt": "nt", "jsonld": "json-ld"}


def tagged(version: str) -> bool:
    tags = subprocess.run(["git", "tag", "-l", f"v{version}", version], cwd=ROOT,
                          capture_output=True, text=True).stdout.split()
    return bool(tags)


def main(argv: list[str]) -> int:
    force = "--force" in argv
    args = [a for a in argv if a != "--force"]
    docs = Path(args[0]) if args else ROOT / "docs"

    g = Graph()
    g.parse(TTL, format="turtle")
    ont = next(g.subjects(RDF.type, OWL.Ontology))
    version_iri = str(g.value(ont, OWL.versionIRI))
    version = version_iri.rstrip("/").rsplit("/", 1)[-1]
    out = docs / "releases" / version

    existing = out / "ontology.ttl"
    if existing.exists() and not force and tagged(version):
        old = Graph()
        old.parse(existing, format="turtle")
        new = Graph()
        for t in g:
            new.add(t)
        for graph in (old, new):
            graph.remove((None, DCTERMS.modified, None))
        if not isomorphic(old, new):
            print(f"release {version} already published with different content; "
                  f"bump the version or pass --force", file=sys.stderr)
            return 1

    out.mkdir(parents=True, exist_ok=True)
    for ext, fmt in FORMATS.items():
        g.serialize(destination=out / f"ontology.{ext}", format=fmt, encoding="utf-8")
    links = "\n".join(f'<li><a href="ontology.{ext}">ontology.{ext}</a></li>' for ext in FORMATS)
    (out / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>HeritageGraph Ontology {version}</title></head>
<body>
<h1>HeritageGraph Ontology, release {version}</h1>
<p>Version IRI: <code>{version_iri}</code><br>
Ontology IRI: <code>{ont}</code></p>
<p>Serializations of this release:</p>
<ul>
{links}
</ul>
<p>Documentation of the current release: <a href="../../">HeritageGraph documentation</a>.</p>
</body></html>
""", encoding="utf-8")
    print(f"published release {version} -> {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
