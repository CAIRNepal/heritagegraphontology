#!/usr/bin/env bash
# =============================================================================
# discover_lux_endpoints.sh — probe LUX for live data endpoints.
# =============================================================================
# LUX (Yale) does not advertise a single canonical bulk-download URL. This
# script probes the URLs that Yale's own data-pipeline harvester references,
# plus the standard IIIF Change Discovery / ActivityStreams locations, and
# reports which are reachable. Run this BEFORE configuring .env so you wire
# the migration to a URL that actually serves content.
#
# Usage:
#   bash discover_lux_endpoints.sh                          # default: text
#   bash discover_lux_endpoints.sh json > endpoints.json    # machine-readable
# =============================================================================
set -u

OUTPUT_FORMAT="${1:-text}"

probe() {
    # $1 = label, $2 = URL, $3 = expected content snippet (optional)
    local label="$1" url="$2" expect="${3:-}"
    local code body_snippet ct size

    # Note: we use --head where possible (cheap) and fall back to a small GET.
    code=$(curl -sS -o /tmp/lux_probe_body -w '%{http_code}' \
                --max-time 20 \
                -H 'Accept: application/ld+json, application/json, application/activity+json, application/n-quads, text/turtle, */*;q=0.1' \
                "$url" 2>/dev/null || echo "000")
    ct=$(curl -sS -I --max-time 10 "$url" 2>/dev/null | awk 'tolower($1)=="content-type:"{print $2}' | tr -d '\r')
    size=$(stat -c '%s' /tmp/lux_probe_body 2>/dev/null || echo 0)
    body_snippet=$(head -c 200 /tmp/lux_probe_body | tr '\n' ' ' | tr -d '\r')

    local match="?"
    if [[ -n "$expect" ]]; then
        if echo "$body_snippet" | grep -qi "$expect"; then match="MATCH"
        else match="MISS"; fi
    fi

    if [[ "$OUTPUT_FORMAT" == "json" ]]; then
        printf '{"label":"%s","url":"%s","status":%s,"content_type":"%s","size":%s,"expect_match":"%s","body_snippet":"%s"}\n' \
            "$label" "$url" "$code" "${ct:-unknown}" "$size" "$match" "${body_snippet//\"/\\\"}"
    else
        local marker
        case "$code" in
            2*) marker="✅" ;;
            3*) marker="↪️" ;;
            4*|5*) marker="❌" ;;
            *) marker="⚠️" ;;
        esac
        printf '%s  %-50s  HTTP %s  %-30s  %s\n' "$marker" "$label" "$code" "${ct:-no-content-type}" "$url"
        if [[ -n "$expect" && "$match" != "MATCH" && "$code" =~ ^2 ]]; then
            printf '    └─ expected /%s/ — got: %s…\n' "$expect" "${body_snippet:0:140}"
        fi
    fi
    rm -f /tmp/lux_probe_body
}

if [[ "$OUTPUT_FORMAT" != "json" ]]; then
    cat <<'BANNER'
=============================================================
 LUX endpoint probe (CAIR Nepal HeritageGraph migration)
=============================================================
 Probing the URLs that should serve LUX data. ✅ = reachable
 and content-type matches; ❌ = 4xx/5xx; ⚠️ = no response.
=============================================================
BANNER
fi

# ---- 1. Top-level LUX site ---------------------------------------------------
probe "LUX homepage"                  "https://lux.collections.yale.edu/"                                        "lux"

# ---- 2. REST API roots -------------------------------------------------------
probe "REST API root"                 "https://lux.collections.yale.edu/api/"
probe "Search API: objects"           "https://lux.collections.yale.edu/api/search/objects?q=*&pageSize=1"        "orderedItems"
probe "Search API: people"            "https://lux.collections.yale.edu/api/search/people?q=*&pageSize=1"         "orderedItems"
probe "Search API: places"            "https://lux.collections.yale.edu/api/search/places?q=*&pageSize=1"         "orderedItems"
probe "Search API: concepts"          "https://lux.collections.yale.edu/api/search/concepts?q=*&pageSize=1"       "orderedItems"
probe "Search API: events"            "https://lux.collections.yale.edu/api/search/events?q=*&pageSize=1"
probe "Search API: works"             "https://lux.collections.yale.edu/api/search/works?q=*&pageSize=1"
probe "Search API: sets"              "https://lux.collections.yale.edu/api/search/sets?q=*&pageSize=1"

# ---- 3. Sample record fetch (proves /data/{type}/{uuid} works) --------------
probe "Sample object (any HMO)"       "https://lux.collections.yale.edu/data/object/0000000-0000-0000-0000-000000000000"  "HumanMadeObject"
# A known-good test UUID would replace this. Run the search call above and
# pick a real id from orderedItems, then re-run with that uuid:
#   probe "Real object"  "https://lux.collections.yale.edu/data/object/<real-uuid>"  "HumanMadeObject"

# ---- 4. IIIF Change Discovery / ActivityStreams ------------------------------
probe ".well-known activity-streams"  "https://lux.collections.yale.edu/.well-known/activity-streams"           "OrderedCollection"
probe "/data/activity-stream"         "https://lux.collections.yale.edu/data/activity-stream"                    "OrderedCollection"
probe "/activity-stream"              "https://lux.collections.yale.edu/activity-stream"                          "OrderedCollection"
probe "/api/activity-stream"          "https://lux.collections.yale.edu/api/activity-stream"                      "OrderedCollection"
probe "IIIF Registry entry (lookup)"  "https://registry.iiif.io/lux"                                              ""

# ---- 5. JSON-LD context (must work for our migration) -----------------------
probe "Linked Art JSON-LD context"    "https://linked.art/ns/v1/linked-art.json"                                  "@context"

# ---- 6. Speculative dump locations (these will likely 404) ------------------
probe "guess: data/dump/latest"       "https://lux.collections.yale.edu/data/dump/latest.nq.gz"
probe "guess: linked-art subdomain"   "https://linked-art.lux.collections.yale.edu/data/dump/latest.nq.gz"
probe "guess: AWS S3 bucket"          "https://lux-prod-data.s3.amazonaws.com/latest.nq.gz"

# ---- 7. Yale Library data-static repo (some institutions publish there) -----
probe "GitHub: project-lux org"       "https://github.com/project-lux"                                            "data-pipeline"
probe "GitHub: lux-data-static repo"  "https://github.com/project-lux/lux-data-static"

if [[ "$OUTPUT_FORMAT" != "json" ]]; then
    cat <<'FOOTER'
=============================================================
 Interpretation:
 - If "Search API: objects" returns ✅, REST crawl works
   (migrate_lux_to_hg.py --mode crawl).
 - If "/data/activity-stream" (or one of its siblings) returns
   ✅ with OrderedCollection, the official IIIF Change Discovery
   path is open — use ActivityStreams mode.
 - If both fail, you'll need to email Yale (see LUX_DATA_DOWNLOAD.md).
=============================================================
FOOTER
fi
