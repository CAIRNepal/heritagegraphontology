#!/usr/bin/env bash
# Deploy Apache Jena Fuseki via Docker and load the HeritageGraph KG into
# per-source named graphs. Idempotent: recreates the container each run.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
KG="$ROOT/data/kg"
DS="heritagegraph"
PORT="${FUSEKI_PORT:-3030}"
PW="${ADMIN_PASSWORD:-admin}"
IMG="stain/jena-fuseki:latest"
NAME="hg-fuseki"
BASE="http://localhost:${PORT}/${DS}"
HG="https://w3id.org/heritagegraph"
DATA="https://data.cair-nepal.org/heritagegraph"

echo ">> (re)creating Fuseki container"
docker rm -f "$NAME" >/dev/null 2>&1 || true
mkdir -p "$ROOT/data/fuseki"
docker run -d --name "$NAME" -p "${PORT}:3030" \
  -e ADMIN_PASSWORD="$PW" -e FUSEKI_DATASET_1="$DS" \
  -v "$ROOT/data/fuseki:/fuseki" "$IMG" >/dev/null

echo ">> waiting for Fuseki dataset to accept queries"
for i in $(seq 1 90); do
  code=$(curl -s -o /dev/null -w "%{http_code}" -u "admin:${PW}" \
    "${BASE}/sparql" --data-urlencode 'query=ASK{}' 2>/dev/null || true)
  if [ "$code" = "200" ]; then break; fi
  sleep 2
done
[ "$code" = "200" ] || { echo "Fuseki dataset not ready (last code $code)"; exit 1; }

post() { # file graphIRI
  curl -s -o /dev/null -w "%{http_code}" -u "admin:${PW}" -X POST \
    -H "Content-Type: text/turtle" --data-binary "@$1" \
    "${BASE}/data?graph=$2"
}
load() { # file  graphIRI
  echo ">> loading $1 -> <$2>"
  for try in 1 2 3 4 5; do
    code=$(post "${KG}/$1" "$2")
    case "$code" in 200|201|204) echo "   ok ($code)"; return 0;; esac
    echo "   retry $try (HTTP $code)"; sleep 3
  done
  echo "   FAILED loading $1 (HTTP $code)"; exit 1
}

echo ">> loading ontology TBox -> <${HG}/ontology>"
for try in 1 2 3 4 5; do
  code=$(post "${ROOT}/ontology/HeritageGraph.ttl" "${HG}/ontology")
  case "$code" in 200|201|204) echo "   ok ($code)"; break;; esac
  echo "   retry $try (HTTP $code)"; sleep 3
done

load "wikidata.ttl"   "${DATA}/graph/wikidata"
load "osm.ttl"        "${DATA}/graph/openstreetmap"
load "unesco.ttl"     "${DATA}/graph/unesco"
load "intangible.ttl" "${DATA}/graph/intangible"
load "crosswalk.ttl"            "${DATA}/graph/crosswalk"
load "intangible_crosswalk.ttl" "${DATA}/graph/crosswalk"

echo ">> triple counts per graph"
curl -sf -u "admin:${PW}" "${BASE}/sparql" \
  --data-urlencode 'query=SELECT ?g (COUNT(*) AS ?triples) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g ORDER BY DESC(?triples)' \
  -H 'Accept: text/csv'

echo ""
echo "Fuseki UI:    http://localhost:${PORT}/  (admin / ${PW})"
echo "SPARQL:       ${BASE}/sparql"
