# HeritageGraph IRIs on cair-nepal.org (nginx)

Content negotiation for every IRI under `https://cair-nepal.org/heritagegraph/`.

| IRI | `text/html` | `text/turtle` · `application/rdf+xml` · `application/ld+json` · `application/n-triples` |
|---|---|---|
| `/heritagegraph/`, `/heritagegraph/ontology` | `docs/` (WIDOCO documentation) | `docs/ontology.{ttl,owl,jsonld,nt}` (current release) |
| `/heritagegraph/ontology/<version>` | `docs/releases/<version>/` | `docs/releases/<version>/ontology.{ttl,owl,jsonld,nt}` |
| `/heritagegraph/<Term>` (class, property) | `docs/#<Term>` | current release |
| `/heritagegraph/<Enum>`, `/heritagegraph/scheme/<Enum>` | `docs/enum/<Enum>.html` | current release |

All redirects are `303 See Other` with `Vary: Accept`. Enumeration individuals are hash
IRIs (`…/ConditionType#Damaged`): the fragment is never sent to the server, but browsers keep
it across a redirect whose `Location` has no fragment. Enumeration IRIs are therefore
redirected to `docs/enum/<Enum>.html` (one anchor per value, written by
`scripts/gen_enum_pages.py`) without a fragment, and the browser lands on `#Damaged`.

## Files

- `heritagegraph-maps.conf` — `map` blocks (Accept → format → target); include in `http {}`.
- `heritagegraph-locations.conf` — `location` blocks; include in the `cair-nepal.org` `server {}`.
- `cair-nepal.org.conf` — example server block wiring both in.
- `check_conneg.py` — test script (below).

## Deploy

1. Build the site: `make artefacts && make docs` (writes `docs/`, including the
   immutable per-release copy `docs/releases/<version>/` made by
   `scripts/publish_release.py`; it is frozen once the release is tagged).
2. Copy `docs/` to `/srv/heritagegraph/docs/` on the server (or change the `alias` in
   `heritagegraph-locations.conf`). Keep earlier `releases/<version>/` directories.
3. Copy the two `.conf` files to `/etc/nginx/heritagegraph/`, include them as in
   `cair-nepal.org.conf`, then `nginx -t && nginx -s reload`.

## Test

```bash
python3 deploy/nginx/check_conneg.py https://cair-nepal.org/heritagegraph/
```

It requests the ontology IRI, the version IRI, and a class, object property, datatype
property, and enumeration individual taken from `ontology/HeritageGraph.ttl`, with each
Accept type, and checks status, content type, the docs anchor (HTML), that RDF parses and
declares the term, and that the version IRI is served from that release's files. Point it
at a staging server by passing its base URL (e.g. `http://localhost:8080/heritagegraph/`).
