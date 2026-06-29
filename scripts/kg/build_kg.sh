#!/usr/bin/env bash
# End-to-end HeritageGraph KG build: extract -> transform -> validate -> load.
# Reproducible. Requires: python venv (rdflib, pyshacl), curl, Docker.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source venv/bin/activate 2>/dev/null || true
cd scripts/kg

echo "== 1/8  extract Wikidata (CC0) =="; python extract_wikidata.py
echo "== 2/8  extract OpenStreetMap (ODbL) =="; python extract_osm.py
echo "== 3/8  extract UNESCO WHS =="; python extract_unesco.py
echo "== 4/8  build curated intangible layer =="; python extract_intangible.py
# DANAM (non-commercial/academic; cite Brosius & Michaels). Paged Arches search
# API, cached under data/raw/danam/. Set DANAM_MAX_PAGES to bound the harvest
# (default: all ~518 pages; cached pages are not re-fetched).
echo "== 5/8  extract DANAM (NHDP, non-commercial) =="; python extract_danam.py
# shapes_spec.json (git-ignored) drives transform's closed-shape gating; regenerate.
echo "== 6/8  introspect SHACL shapes -> data/raw/shapes_spec.json =="
( cd "$ROOT" && python scripts/kg/shapes_introspect.py >/dev/null )
echo "== 7/8  transform -> ABox =="; python transform.py
echo "== 8/8  SHACL validate (Wikidata+UNESCO+intangible+DANAM + OSM sample) =="
python validate.py "${OSM_SAMPLE:-400}"
echo
echo "Now load into Fuseki:  bash scripts/kg/load_fuseki.sh"
echo "Then run queries:      python scripts/kg/run_cq.py"
