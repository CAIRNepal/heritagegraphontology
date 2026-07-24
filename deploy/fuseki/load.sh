#!/usr/bin/env bash
# Populate the TDB2 database in ./databases/heritagegraph from the released
# ontology and the reconciled DANAM knowledge graph. Run this ONCE before the
# first `docker compose up`, and again whenever the data changes (after
# stopping the fuseki container, since TDB2 takes an exclusive write lock).
#
# Uses the apache/jena CLI image (which ships tdb2.tdbloader); the apache/jena
# and apache/jena-fuseki tags should match.
set -euo pipefail
cd "$(dirname "$0")"

JENA_IMAGE="apache/jena:5.2.0"          # keep in sync with docker-compose.yml
REPO="$(cd ../.. && pwd)"
DBDIR="$PWD/databases"
LOC="/fuseki/databases/heritagegraph"

mkdir -p "$DBDIR"

echo "==> Loading ontology (into named graph https://w3id.org/heritagegraph/ontology)"
docker run --rm \
  -v "$DBDIR:/fuseki/databases" \
  -v "$REPO/ontology:/staging/ontology:ro" \
  --entrypoint tdb2.tdbloader "$JENA_IMAGE" \
  --loc "$LOC" \
  --graph "https://w3id.org/heritagegraph/ontology" \
  /staging/ontology/HeritageGraph.ttl

echo "==> Loading reconciled DANAM data (quads keep their source graphs)"
docker run --rm \
  -v "$DBDIR:/fuseki/databases" \
  -v "$REPO/data/reconciled:/staging/data:ro" \
  --entrypoint tdb2.tdbloader "$JENA_IMAGE" \
  --loc "$LOC" \
  /staging/data/danam-heritagegraph.nq

echo "==> Done. Triple count:"
docker run --rm \
  -v "$DBDIR:/fuseki/databases" \
  --entrypoint tdb2.tdbquery "$JENA_IMAGE" \
  --loc "$LOC" \
  'SELECT (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } }'
