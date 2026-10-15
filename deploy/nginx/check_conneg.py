#!/usr/bin/env python3
"""Check content negotiation for the HeritageGraph IRIs on a deployed server.

Given the base URL under which the namespace is served (normally the namespace
itself, http://cair-nepal.org/heritagegraph/; for a local test e.g.
http://localhost:8080/heritagegraph/), requests the ontology IRI, the version
IRI, and a sample of term IRIs (a class, an object property, a datatype
property, and an enumeration individual, taken from ontology/HeritageGraph.ttl)
with each Accept type:

  text/html             -> 200 text/html; term IRIs 303 to the term's docs anchor
  text/turtle           -> 200 text/turtle, parses, contains the expected node
  application/rdf+xml   -> 200 application/rdf+xml, parses, contains it
  application/ld+json   -> 200 application/ld+json, parses, contains it

The version IRI must resolve into docs/releases/<version>/ and its RDF must carry
that owl:versionIRI. IRIs are requested at their path relative to the namespace,
appended to the base URL, so the check runs against a staging server too.

Run:  python3 deploy/nginx/check_conneg.py http://cair-nepal.org/heritagegraph/
"""
from __future__ import annotations

import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from rdflib import Graph, OWL, RDF, URIRef
from rdflib.namespace import VANN

ROOT = Path(__file__).resolve().parents[2]
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
ACCEPTS = {
    "text/html": ("text/html", None),
    "text/turtle": ("text/turtle", "turtle"),
    "application/rdf+xml": ("application/rdf+xml", "xml"),
    "application/ld+json": ("application/ld+json", "json-ld"),
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url: str, accept: str, hops: int = 5):
    """Follow redirects by hand; return (chain of (status, url), final body,
    final content type)."""
    chain = []
    for _ in range(hops):
        req = urllib.request.Request(url, headers={"Accept": accept,
                                                   "User-Agent": "hg-conneg-check"})
        try:
            with OPENER.open(req, timeout=30) as r:
                chain.append((r.status, url))
                return chain, r.read(), r.headers.get_content_type()
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308):
                loc = e.headers["Location"]
                chain.append((e.code, url))
                url = urllib.parse.urljoin(url, loc)
                continue
            chain.append((e.code, url))
            return chain, b"", e.headers.get_content_type()
    return chain, b"", ""


def sample(g: Graph, ns: str) -> list[tuple[str, URIRef]]:
    def first(kind) -> URIRef:
        return sorted(s for s in g.subjects(RDF.type, kind)
                      if isinstance(s, URIRef) and str(s).startswith(ns)
                      and "#" not in str(s)[len(ns):])[0]
    individual = sorted(s for s in g.subjects(RDF.type, OWL.NamedIndividual)
                        if str(s).startswith(ns))[0]
    return [("class", first(OWL.Class)), ("object property", first(OWL.ObjectProperty)),
            ("datatype property", first(OWL.DatatypeProperty)),
            ("enumeration individual", individual)]


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print(__doc__)
        return 2
    base = argv[0].rstrip("/") + "/"
    g = Graph()
    g.parse(TTL, format="turtle")
    ont = next(g.subjects(RDF.type, OWL.Ontology))
    ns = str(g.value(ont, VANN.preferredNamespaceUri))
    version_iri = g.value(ont, OWL.versionIRI)
    version = str(version_iri).rstrip("/").rsplit("/", 1)[-1]

    targets = [("ontology IRI", ont), ("version IRI", version_iri)] + sample(g, ns)
    failures = 0
    for label, iri in targets:
        local = str(iri)[len(ns):]
        path, _, fragment = local.partition("#")
        url = base + path
        print(f"\n{label}: <{iri}>  (GET {url})")
        for accept, (want_type, fmt) in ACCEPTS.items():
            chain, body, ctype = fetch(url, accept)
            status = chain[-1][0] if chain else None
            problems = []
            if status != 200:
                problems.append(f"final status {status}")
            if ctype != want_type:
                problems.append(f"content type {ctype!r}, want {want_type!r}")
            if label == "version IRI" and f"/releases/{version}/" not in chain[-1][1]:
                problems.append("not served from this release's files")
            if accept == "text/html" and label not in ("ontology IRI", "version IRI"):
                if not any(url_.endswith(f"#{path}") for _, url_ in chain):
                    problems.append(f"no redirect to the docs anchor #{path}")
            if fmt and status == 200:
                try:
                    rg = Graph()
                    rg.parse(data=body, format=fmt)
                    if label == "version IRI":
                        if (None, OWL.versionIRI, version_iri) not in rg:
                            problems.append("owl:versionIRI missing")
                    elif (iri, RDF.type, None) not in rg:
                        problems.append("term/ontology not declared in the response")
                except Exception as exc:
                    problems.append(f"does not parse: {exc.__class__.__name__}")
            hops = " -> ".join(f"{s}" for s, _ in chain)
            verdict = "OK  " if not problems else "FAIL"
            failures += bool(problems)
            print(f"  [{verdict}] {accept:<22} {hops:<10} {chain[-1][1] if chain else ''}"
                  + (f"   ({'; '.join(problems)})" if problems else ""))
        if fragment:
            print(f"  note: '#{fragment}' is a fragment and is not sent to the server; "
                  f"the IRI resolves like <{ns}{path}>")
    print(f"\n{'PASS' if not failures else f'FAIL: {failures} check(s) failed'}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
