# Pilot Run — What was migrated and how to query it

First end-to-end pilot run executed against the production stack on
`server42.dnsbilisim.net` (Oxigraph 0.4.4). This document records what the
imported dataset looks like, where the data lives, and how to query it.

Use this as the reference for downstream consumers of the migrated graph;
the operational details of how the pipeline runs are in
[`docs/DEPLOY_SERVER.md`](DEPLOY_SERVER.md) and
[`docs/MIGRATION_PLAN.md`](MIGRATION_PLAN.md).


## Run parameters

| Setting | Value |
|---|---|
| `RING_MODE` | `crawl` (no public Yale bulk dump available) |
| `LUX_FILTER` | `religious heritage` |
| `LIMIT_PER_QUERY` | `10000` (pilot ring) |
| `BATCH_SIZE` | `50000` |
| `VALIDATION_MODE` | `strict` |
| LUX records fetched | **20,871** (across all 8 search scopes) |


## Where the data lives

The triple store ends up with **three named graphs**. Nothing is loaded into
the default graph; queries that don't specify `GRAPH` see the union of all
named graphs because the server is started with `--union-default-graph`.

| Graph IRI | Triples | Purpose |
|---|---:|---|
| `<https://lux.collections.yale.edu/>` | **3,467,368** | Raw LUX records, unchanged. Original CIDOC-CRM types (`crm:E22_Human-Made_Object`, etc.) and predicates. |
| `<https://w3id.org/heritagegraph/imported/lux>` | **98,131** | Migration output — HG-typed instances with `owl:sameAs` back to the LUX original. |
| `<https://w3id.org/heritagegraph/alignment/lux>` | 273 | The LUX↔HG alignment ontology (`heritagegraph-lux-alignment.ttl`). |


## What the imported graph contains

The migration produced **32,342 HG instances** spread across five HG classes:

| HG class | Instances |
|---|---:|
| `hg:Person` | 25,281 |
| `hg:Group` | 3,558 |
| `hg:Place` | 3,281 |
| `hg:HumanMadeObject` | 137 |
| `hg:Set` | 85 |

Every imported instance carries at minimum:

- `rdf:type <hg-class>`
- `owl:sameAs <original-LUX-IRI>` — link back to the raw record
- `hg:name "<label>"` — when the LUX record had `rdfs:label`

Predicate breakdown of the 98 K imported triples:

| Predicate | Count |
|---|---:|
| `hg:name` | 33,277 |
| `owl:sameAs` | 32,342 |
| `rdf:type` | 32,342 |
| `hg:has_architectural_style` | 148 |
| `hg:used_materials` | 8 |
| `hg:was_produced_by_event` | 8 |
| `hg:place_coordinates` | 6 |


### Known gap — Activity and Work branches did not land

The transform stage logs report `+21275 triples` for the `activity`, `work`,
and `set` templates, but the imported graph contains zero `hg:Production`,
`hg:LinguisticObject`, `hg:DigitalObject`, `hg:VisualItem` (etc.) instances.
The raw LUX graph contains 188 K `E33_Linguistic_Object`, 25 K
`D1_Digital_Object`, 136 K `E65_Creation`, and 20 K `E7_Activity` records —
none of which the pilot run materialised under the HG namespace.

Two contributing causes are known:

1. The `activity` template UNION-matches only specific CIDOC-CRM event
   subclasses (`E12_Production`, `E11_Modification`, `E9_Move`, …) — but the
   crawl returned `E65_Creation`, `E13_Attribute_Assignment`, and
   `E7_Activity`, none of which the template covers.
2. The transform script's `_target_count` accounting is approximate; the
   "+N triples" reported per template can over-state actual inserts when a
   batch breaks before `_target_count` is updated. This needs a dedicated
   review.

Treat the Person / Group / Place / HumanMadeObject / Set instances as the
authoritative pilot output. Other branches require template fixes before
the next run.


## Validation report (P5)

Strict-mode validation passed all hard gates:

| Gate | Result |
|---|---|
| V1 — unmapped LUX classes | **0 rows · PASS** |
| V2 — `owl:sameAs` consistency | **0 rows · PASS** |
| V3 — count parity per class | 67 rows (manual review) |
| V4 — unaligned properties | 36 rows (manual review) |
| V5 — random round-trip sample | 10 rows (manual review) |
| V6 — HG-native preservation | 0 rows |
| V7 — unique-id per record | 0 rows |
| V8 — orphan check | 0 rows |


## Querying the data

The SPARQL endpoint is bound to `0.0.0.0:7878` on the host. Don't expose it
on the public IP without a firewall — random scanners hit the port. For
local exploration use an SSH tunnel:

```bash
ssh -L 7878:localhost:7878 root@server42.dnsbilisim.net
# leave that terminal open, then open http://localhost:7878 in a browser
```

The HTTP UI is the bundled Oxigraph YASGUI-style console. From the CLI:

```bash
curl -s -H 'Accept: application/sparql-results+json' \
     --data-urlencode 'query=<your SPARQL here>' \
     http://localhost:7878/query
```


### Query 1 — Person names (HG side only)

```sparql
PREFIX hg:  <https://w3id.org/heritagegraph/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?person ?name ?luxOriginal
WHERE {
  GRAPH <https://w3id.org/heritagegraph/imported/lux> {
    ?person a hg:Person ;
            hg:name ?name ;
            owl:sameAs ?luxOriginal .
  }
}
LIMIT 25
```

### Query 2 — Places with coordinates

```sparql
PREFIX hg: <https://w3id.org/heritagegraph/>

SELECT ?place ?name ?wkt
WHERE {
  GRAPH <https://w3id.org/heritagegraph/imported/lux> {
    ?place a hg:Place ;
           hg:name ?name .
    OPTIONAL { ?place hg:place_coordinates ?wkt }
  }
}
LIMIT 25
```

### Query 3 — HG → LUX drill-down

Pivot from an imported HG entity to its original LUX record to inspect
the underlying CIDOC-CRM triples that did not get carried into HG:

```sparql
PREFIX hg:  <https://w3id.org/heritagegraph/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?hgGroup ?name ?luxPred ?luxObj
WHERE {
  GRAPH <https://w3id.org/heritagegraph/imported/lux> {
    ?hgGroup a hg:Group ;
             hg:name ?name ;
             owl:sameAs ?luxOriginal .
  }
  GRAPH <https://lux.collections.yale.edu/> {
    ?luxOriginal ?luxPred ?luxObj .
  }
}
LIMIT 20
```

### Query 4 — What was crawled but not mapped

Lists raw LUX classes for which no `owl:sameAs` link exists in the
imported graph (good shopping list for next-iteration templates):

```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>

SELECT ?luxClass (COUNT(DISTINCT ?lux) AS ?missing)
WHERE {
  GRAPH <https://lux.collections.yale.edu/> {
    ?lux a ?luxClass .
  }
  FILTER NOT EXISTS {
    GRAPH <https://w3id.org/heritagegraph/imported/lux> {
      ?hg owl:sameAs ?lux .
    }
  }
}
GROUP BY ?luxClass
ORDER BY DESC(?missing)
LIMIT 20
```


## Bulk export

To pull the imported graph out of the server as Turtle for downstream tools:

```bash
ssh root@server42.dnsbilisim.net \
  "curl -s -G 'http://localhost:7878/store' \
        --data-urlencode 'graph=https://w3id.org/heritagegraph/imported/lux' \
        -H 'Accept: text/turtle'" \
  > imported-lux.ttl
```

The whole imported graph is ~10 MB.


## Next steps

- Fix the `activity` / `work` transform templates so the matching ~470 K
  raw LUX entities get HG counterparts.
- Audit the `_target_count` accounting in `migrate_lux_to_hg.py` so the
  per-template "+N triples" reporting matches reality.
- Replace the broken Oxigraph healthcheck so downstream services can wait
  on `service_healthy` again.
- Snapshot the current store (`make backup`) before the next migration
  attempt; that gives a baseline to diff against.
