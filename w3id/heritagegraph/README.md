# HeritageGraph Ontology

Permanent identifiers for the HeritageGraph ontology — an event-centric
cultural-heritage ontology (CIDOC-CRM / PROV-O aligned) for Kathmandu Valley
living heritage, developed by CAIR-Nepal.

| IRI | Resolves to |
|---|---|
| `https://w3id.org/heritagegraph/` (namespace) | ontology document (content-negotiated) |
| `https://w3id.org/heritagegraph/ontology` (ontology IRI) | ontology document (content-negotiated) |
| `https://w3id.org/heritagegraph/ontology/<version>` (version IRIs) | ontology document (content-negotiated) |
| any term IRI in the namespace | ontology document (content-negotiated) |

Content negotiation: `text/turtle`, `application/rdf+xml`, `application/n-triples`,
`application/ld+json`; default is the HTML documentation at
<https://cairnepal.github.io/heritagegraphontology/>.

- Source repository: <https://github.com/CAIRNepal/heritagegraphontology>
- Organization: CAIR-Nepal — <https://cair-nepal.org>
- Contacts: [@nirajkark](https://github.com/nirajkark) (Niraj Karki),
  [CAIRNepal](https://github.com/CAIRNepal) organization
- License of the ontology: CC BY 4.0

## Deployment status

**Not yet deployed.** The `heritagegraph` namespace is not registered at
w3id.org yet; the IRIs above currently return 404. To activate them, submit
this directory (`.htaccess` + `README.md`) as a pull request adding
`heritagegraph/` to <https://github.com/perma-id/w3id.org>. The redirect
targets (GitHub Pages documentation and RDF serializations) are already
live and were verified to return HTTP 200.
