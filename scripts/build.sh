#!/usr/bin/env bash
#
# build.sh — regenerate the whole HeritageGraph documentation + WebVOWL
# visualization from the modular ontology in ontology/.
#
# Run this after ANY change to the ontology:
#     scripts/build.sh              # writes ./docs (the published site)
#     scripts/build.sh /tmp/preview # writes a throwaway preview, leaves docs/ alone
#
# What it does:
#   1. merges ontology/HeritageGraph.ttl + ontology/heritagegraph-lux-alignment.ttl
#      (owl:imports stripped) into one build artifact — the WHOLE ontology
#   2. runs Widoco (owl2vowl runs inside the container — no local Java needed)
#   3. publishes a single, fresh docs site (HTML + RDF serializations + WebVOWL)
#
# Requirements: docker, python3 with rdflib (e.g. the repo venv).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ONT="$ROOT/ontology"
OUT="${1:-$ROOT/docs}"
WIDOCO="ghcr.io/dgarijo/widoco:v1.4.23"
PY="${PYTHON:-$ROOT/venv/bin/python}"; command -v "$PY" >/dev/null 2>&1 || PY="python3"
MERGED="$ONT/HeritageGraph.merged.ttl"   # gitignored build artifact

echo "▶ 1/3  merging modular ontology → $MERGED"
"$PY" - "$ONT/HeritageGraph.ttl" "$ONT/heritagegraph-lux-alignment.ttl" "$MERGED" <<'PY'
import sys
from rdflib import Graph, OWL
g = Graph()
for src in sys.argv[1:-1]:
    g.parse(src, format="turtle")
for t in list(g.triples((None, OWL.imports, None))):
    g.remove(t)                       # imports already merged in
g.serialize(destination=sys.argv[-1], format="turtle")
print(f"   merged {len(g)} triples from {len(sys.argv)-2} modules")
PY

# Apple Silicon: the Widoco image is amd64-only → run under emulation
PLATFORM=""
case "$(uname -m)" in arm64|aarch64) PLATFORM="--platform linux/amd64" ;; esac

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
chmod 777 "$TMP"

echo "▶ 2/3  running Widoco (owl2vowl) on the merged ontology"
docker run --rm -u 0 $PLATFORM \
  -v "$MERGED":/input/ontology.ttl \
  -v "$TMP":/output \
  "$WIDOCO" \
  -ontFile /input/ontology.ttl \
  -outFolder /output \
  -lang en -rewriteAll -webVowl

# Widoco may nest everything under a doc/ subfolder depending on version
GEN="$TMP"; [ -d "$TMP/doc" ] && GEN="$TMP/doc"
[ -f "$GEN/index-en.html" ] && mv -f "$GEN/index-en.html" "$GEN/index.html" || true

echo "▶ 3/3  publishing fresh site → $OUT"
mkdir -p "$OUT"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$GEN"/ "$OUT"/
else
  rm -rf "$OUT"/* && cp -R "$GEN"/. "$OUT"/
fi

echo "✓ done. Open:  $OUT/webvowl/   (whole ontology) ·  $OUT/index.html  (docs)"
