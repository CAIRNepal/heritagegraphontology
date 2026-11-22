#!/usr/bin/env bash
#
# build.sh — regenerate the HeritageGraph documentation site with OntoReview
# (https://pypi.org/project/ontoreview/) for the CORE ontology in
# ontology/HeritageGraph.ttl, configured by ontoreview.toml.
#
# Run this after ANY change to the core ontology:
#     scripts/build.sh              # writes ./docs (the published site)
#     scripts/build.sh /tmp/preview # writes a throwaway preview, leaves docs/ alone
#
# What it does:
#   1. runs `ontoreview build`: term pages, class graph, quality report
#      (HermiT consistency, ROBOT, OOPS!, OntoCheck, IRI checks, cross-domain
#      interoperability), changelog against the previous release, and the
#      ontology in TTL / RDF/XML / JSON-LD / N-Triples;
#   2. publishes the site to OUT, keeping releases/ (the immutable per-version
#      copies served at the version IRIs), and adds the enumeration-value pages
#      and the JSON-LD @context.
#
# The LUX alignment (heritagegraph-lux-migration/alignment/heritagegraph-lux-alignment.ttl) is a SEPARATE
# module and is intentionally NOT documented here.
#
# Requirements: ontoreview (ONTOREVIEW=<path to the executable>, default `ontoreview`),
# python3 with rdflib (e.g. the repo venv), and for the ROBOT report and HermiT
# check either ROBOT_JAR=<robot.jar> with Java, a `robot` on PATH, or Docker.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/docs}"
PY="${PYTHON:-$ROOT/venv/bin/python}"; command -v "$PY" >/dev/null 2>&1 || PY="python3"
ONTOREVIEW="${ONTOREVIEW:-ontoreview}"
command -v "$ONTOREVIEW" >/dev/null 2>&1 || { echo "ontoreview not found (pip install ontoreview==1.0.0, or set ONTOREVIEW)" >&2; exit 1; }

WORK="$(mktemp -d)"; trap 'rm -rf "$WORK" 2>/dev/null || true' EXIT
ARGS=(--config "$ROOT/ontoreview.toml" --output "$WORK/site")

# ROBOT for the ROBOT report and the HermiT check: a jar (CI), a robot on PATH, or OntoReview's Docker fallback
if [ -n "${ROBOT_JAR:-}" ] && [ -f "$ROBOT_JAR" ]; then
  JAVA_BIN="${JAVA_HOME:+$JAVA_HOME/bin/}java"
  printf '#!/usr/bin/env bash\nexec %q -jar %q "$@"\n' "$JAVA_BIN" "$(cd "$(dirname "$ROBOT_JAR")" && pwd)/$(basename "$ROBOT_JAR")" > "$WORK/robot"
  chmod +x "$WORK/robot"
  ARGS+=(--robot "$WORK/robot")
fi

# changelog against the previous release (owl:priorVersion → docs/releases/<version>/ontology.ttl)
PRIOR="$("$PY" - "$ROOT/ontology/HeritageGraph.ttl" <<'PY'
import sys
from rdflib import Graph, OWL, RDF
g = Graph(); g.parse(sys.argv[1], format="turtle")
ont = next(g.subjects(RDF.type, OWL.Ontology))
p = g.value(ont, OWL.priorVersion)
print(str(p).rstrip("/").rsplit("/", 1)[-1] if p else "")
PY
)"
if [ -n "$PRIOR" ] && [ -f "$ROOT/docs/releases/$PRIOR/ontology.ttl" ]; then
  ARGS+=(--previous "$ROOT/docs/releases/$PRIOR/ontology.ttl")
fi

# python.org builds of Python on macOS ship without CA certificates; OntoReview's
# network checks (OOPS!, OLS) then fail, so point them at certifi when available
ORPY="$(dirname "$(command -v "$ONTOREVIEW")")/python"
if [ -z "${SSL_CERT_FILE:-}" ] && [ -x "$ORPY" ]; then
  CA="$("$ORPY" -c 'import certifi; print(certifi.where())' 2>/dev/null || true)"
  [ -n "$CA" ] && export SSL_CERT_FILE="$CA" REQUESTS_CA_BUNDLE="$CA"
fi

echo "▶ 1/2  ontoreview build (previous release: ${PRIOR:-none})"
"$ONTOREVIEW" build "$ROOT/ontology/HeritageGraph.ttl" "${ARGS[@]}"

# OntoReview also writes self-hosting scaffolding (Docker, nginx, its own Pages
# workflow); the site is deployed by this repository's CI and served by
# deploy/nginx, so those files are left out of the published folder
SITE="$WORK/site"
rm -rf "$SITE/.github" "$SITE/deploy" "$SITE/Dockerfile" "$SITE/docker-compose.yml" \
       "$SITE/.dockerignore" "$SITE/DEPLOY.md" "$SITE/nginx.conf.example" "$SITE/w3id.htaccess" \
       "$SITE/.ontoreview-build"

echo "▶ 2/2  publishing site → $OUT"
mkdir -p "$OUT"
if command -v rsync >/dev/null 2>&1; then
  # releases/ holds the immutable per-version copies served at version IRIs
  rsync -a --delete --exclude releases/ "$SITE"/ "$OUT"/
else
  find "$OUT" -mindepth 1 -maxdepth 1 ! -name releases -exec rm -rf {} + && cp -R "$SITE"/. "$OUT"/
fi
# OntoReview's graph leaves enumeration values unconnected; link each to its class
"$PY" "$ROOT/scripts/link_enum_values.py" "$OUT"
"$PY" "$ROOT/scripts/publish_release.py" "$OUT"
"$PY" "$ROOT/scripts/gen_enum_pages.py" "$OUT"

# Linked-Art-style JSON-LD term context for compact HeritageGraph JSON-LD.
echo "   generating JSON-LD @context → $OUT/context.jsonld"
"$PY" "$ROOT/scripts/gen_jsonld_context.py" "$OUT/context.jsonld"

# Ship content-negotiation rules alongside the published RDF serializations.
[ -f "$ROOT/.htaccess" ] && cp -f "$ROOT/.htaccess" "$OUT/.htaccess"
touch "$OUT/.nojekyll"

echo "✓ done. Open:  $OUT/index.html"
