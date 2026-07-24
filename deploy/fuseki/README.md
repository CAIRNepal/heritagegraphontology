# Public HeritageGraph SPARQL endpoint (Fuseki + Caddy)

A read-only, HTTPS SPARQL query endpoint over the reconciled DANAM knowledge
graph (`data/reconciled/danam-heritagegraph.nq`, ~130k quads) loaded together
with the released ontology (`ontology/HeritageGraph.ttl`).

- **Fuseki** serves the TDB2 dataset with *query-only* endpoints (no update, no
  writable graph store) — see `config/heritagegraph.ttl`.
- **Caddy** terminates HTTPS with automatic Let's Encrypt certificates and
  blocks the Fuseki admin interface — see `Caddyfile`.

## Prerequisites

- A small Linux VM (1–2 vCPU, 2–4 GB RAM is plenty; ~1 GB disk for the DB).
- Docker + Docker Compose plugin installed.
- A domain name with a DNS **A** (and optionally **AAAA**) record pointing at the
  VM's public IP. Ports **80** and **443** open in the firewall.

## Deploy

```bash
# 1. Copy this deploy/ folder AND the repo's ontology/ + data/reconciled/ to the VM
#    (load.sh reads ../../ontology and ../../data/reconciled relative to itself,
#     so keep the repo layout, or adjust the paths in load.sh).

# 2. Configure
cp .env.example .env
$EDITOR .env            # set DOMAIN and FUSEKI_ADMIN_PASSWORD

# 3. Build the TDB2 database from the ontology + reconciled data (one-off)
chmod +x load.sh
./load.sh               # prints the final triple count when finished

# 4. Start the endpoint
docker compose up -d

# 5. Verify (from anywhere)
curl -s -H 'Accept: application/sparql-results+json' \
  --data-urlencode 'query=SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }' \
  https://YOUR_DOMAIN/heritagegraph/sparql
```

## Endpoint URLs

- SPARQL query (GET/POST): `https://YOUR_DOMAIN/heritagegraph/sparql`
- Fuseki query UI (YASGUI):  `https://YOUR_DOMAIN/heritagegraph/`
- Admin API (`/$/*`): **blocked** by the proxy.

## Reloading data

TDB2 takes an exclusive lock, so stop Fuseki before reloading:

```bash
docker compose stop fuseki
./load.sh
docker compose up -d fuseki
```

To load from scratch, delete `./databases/heritagegraph` first.

## Notes

- Pin `apache/jena-fuseki` (compose) and `apache/jena` (load.sh) to the **same,
  current** release tag before deploying.
- The demonstrator ABox uses the same vocabulary, so you can also add
  `examples/kathmandu-mini-abox.ttl` as another named graph in `load.sh` if you
  want both the modelled demonstrator and the DANAM data behind one endpoint.
- Pair this live endpoint with an archival copy on **Zenodo** (persistent DOI)
  and a **VoID/DCAT** dataset description for full FAIR coverage; point your
  `w3id.org/heritagegraph` redirect at the ontology and this landing page.
