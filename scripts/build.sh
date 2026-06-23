#!/usr/bin/env bash
#
# build.sh — regenerate the HeritageGraph documentation + WebVOWL visualization
# (WIDOCO) for the CORE ontology in ontology/HeritageGraph.ttl.
#
# Run this after ANY change to the core ontology:
#     scripts/build.sh              # writes ./docs (the published site)
#     scripts/build.sh /tmp/preview # writes a throwaway preview, leaves docs/ alone
#
# What it does:
#   1. loads ontology/HeritageGraph.ttl (the OWL release generated from the
#      LinkML source HeritageGraph.yaml) and strips owl:imports so WIDOCO does
#      not try to dereference CIDOC-CRM / PROV-O / EDM / etc. while documenting
#      the local HeritageGraph terms.
#   2. runs WIDOCO (owl2vowl runs inside the container — no local Java needed)
#   3. publishes a single, fresh docs site (HTML + RDF serializations + WebVOWL)
#
# The LUX alignment (ontology/lux/heritagegraph-lux-alignment.ttl) is a SEPARATE
# module and is intentionally NOT documented here.
#
# Requirements: docker, python3 with rdflib (e.g. the repo venv).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ONT="$ROOT/ontology"
OUT="${1:-$ROOT/docs}"
WIDOCO="ghcr.io/dgarijo/widoco:v1.4.23"
PY="${PYTHON:-$ROOT/venv/bin/python}"; command -v "$PY" >/dev/null 2>&1 || PY="python3"
BUILD="$ONT/HeritageGraph.build.ttl"   # gitignored build artifact (imports stripped)

echo "▶ 1/3  preparing core ontology (imports stripped) → $BUILD"
"$PY" - "$ONT/HeritageGraph.ttl" "$BUILD" <<'PY'
import sys
from rdflib import Graph, OWL
g = Graph()
g.parse(sys.argv[1], format="turtle")
for t in list(g.triples((None, OWL.imports, None))):
    g.remove(t)                       # drop imports so WIDOCO documents local terms only
g.serialize(destination=sys.argv[-1], format="turtle")
print(f"   prepared {len(g)} triples from the core ontology")
PY

# Apple Silicon: the Widoco image is amd64-only → run under emulation
PLATFORM=""
case "$(uname -m)" in arm64|aarch64) PLATFORM="--platform linux/amd64" ;; esac

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
chmod 777 "$TMP"

echo "▶ 2/3  running WIDOCO (owl2vowl) on the core ontology"
docker run --rm -u 0 $PLATFORM \
  -v "$BUILD":/input/ontology.ttl \
  -v "$TMP":/output \
  "$WIDOCO" \
  -ontFile /input/ontology.ttl \
  -outFolder /output \
  -lang en -rewriteAll -webVowl

# Widoco may nest everything under a doc/ subfolder depending on version
GEN="$TMP"; [ -d "$TMP/doc" ] && GEN="$TMP/doc"
[ -f "$GEN/index-en.html" ] && mv -f "$GEN/index-en.html" "$GEN/index.html" || true

# Declutter the WebVOWL graph: drop the external CIDOC-CRM/PROV alignment
# super-properties (rdfs:subPropertyOf parents) that owl2vowl pins to a generic
# owl:Thing node, producing a detached "star" disconnected from the real classes.
# Only the visualization JSON is touched — ontology / RDF / HTML are unaffected.
WEBVOWL_JSON="$GEN/webvowl/data/ontology.json"
[ -f "$WEBVOWL_JSON" ] && "$PY" "$ROOT/scripts/declutter_webvowl.py" "$WEBVOWL_JSON"

# Overlay authored narrative sections (abstract / introduction / description /
# references) over WIDOCO's placeholders. WIDOCO regenerates sections on every
# run (-rewriteAll), so the hand-written content is kept in docs-src/sections/
# and re-applied here to survive rebuilds.
SECT_SRC="$ROOT/docs-src/sections"
if [ -d "$SECT_SRC" ] && [ -d "$GEN/sections" ]; then
  echo "   overlaying authored sections from docs-src/sections/"
  for f in "$SECT_SRC"/*.html; do
    [ -e "$f" ] && cp -f "$f" "$GEN/sections/$(basename "$f")"
  done
fi

# Tidy the WIDOCO license badge: by default it embeds the full license URL in
# the shields.io label (License-https://.../by/4.0/-blue.svg). Render the human
# CC-BY-4.0 label instead, keeping the link target unchanged.
INDEX="$GEN/index.html"
if [ -f "$INDEX" ]; then
  "$PY" - "$INDEX" <<'PY'
import sys
p = sys.argv[1]
html = open(p, encoding="utf-8").read()
html = html.replace(
    "https://img.shields.io/badge/License-https://creativecommons.org/licenses/by/4.0/-blue.svg",
    "https://img.shields.io/badge/License-CC--BY--4.0-blue.svg",
)
open(p, "w", encoding="utf-8").write(html)
PY
fi

echo "▶ 3/3  publishing fresh site → $OUT"
mkdir -p "$OUT"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$GEN"/ "$OUT"/
else
  rm -rf "$OUT"/* && cp -R "$GEN"/. "$OUT"/
fi

# Overwrite the bundled WebVOWL MIT license with the ontology's CC BY 4.0 license.
# WIDOCO copies webvowl_1.1.7_patched (which ships the MIT text) on every run;
# this step runs after rsync so the correct license always ends up in the published site.
cat > "$OUT/webvowl/license.txt" <<'LICENSE'
# License

This ontology is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

Copyright (c) 2026 CAIR-Nepal

To view a copy of this license, visit:

https://creativecommons.org/licenses/by/4.0/
LICENSE

# Linked-Art-style JSON-LD term context for compact HeritageGraph JSON-LD.
echo "   generating JSON-LD @context → $OUT/context.jsonld"
"$PY" "$ROOT/scripts/gen_jsonld_context.py" "$OUT/context.jsonld"

# Ship content-negotiation rules alongside the published RDF serializations.
[ -f "$ROOT/.htaccess" ] && cp -f "$ROOT/.htaccess" "$OUT/.htaccess"

echo "✓ done. Open:  $OUT/index.html  (docs) ·  $OUT/webvowl/  (visualization)"
