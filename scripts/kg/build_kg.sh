#!/usr/bin/env bash
# End-to-end HeritageGraph KG build: extract -> transform -> validate -> load.
# Reproducible. Requires: python venv (rdflib, pyshacl), curl, Docker.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source venv/bin/activate 2>/dev/null || true
cd scripts/kg

echo "== 1/5  extract Wikidata (CC0) =="; python extract_wikidata.py
echo "== 2/5  extract OpenStreetMap (ODbL) =="; python extract_osm.py
echo "== 3/6  extract UNESCO WHS =="; python extract_unesco.py
echo "== 4/6  build curated intangible layer =="; python extract_intangible.py
echo "== 5/6  transform -> ABox =="; python transform.py
echo "== 6/6  SHACL validate (sample + intangible) =="; python validate.py "${OSM_SAMPLE:-400}"
echo
echo "Now load into Fuseki:  bash scripts/kg/load_fuseki.sh"
echo "Then run queries:      python scripts/kg/run_cq.py"
