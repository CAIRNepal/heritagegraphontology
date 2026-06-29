"""Extract Nepal monument records from DANAM (Nepal Heritage Documentation
Project, Heidelberg) -> data/raw/danam.json.

DANAM runs on Arches v7 (CIDOC-CRM aligned). The public, anonymous interface is
the Arches search API (`/search/resources?format=json`); per-resource JSON-LD
export returns HTTP 500 for anonymous users, so we harvest the paged search
results. Each raw page is cached under data/raw/danam/ so re-runs are idempotent
and incremental (cached pages are not re-fetched unless DANAM_REFRESH=1).

DANAM terms: data is citation-required and for NON-COMMERCIAL academic use only
(Brosius & Michaels, eds.; see SOURCES["danam"] and DISCOVERY_DANAM.md). This
extractor only caches and reshapes; nothing is invented. Politeness: descriptive
User-Agent with contact, >=1 req/s (configurable via DANAM_RATE), backoff on error.

Env:
  DANAM_MAX_PAGES   cap pages harvested (default: all). Useful for bounded builds.
  DANAM_RATE        seconds between requests (default 1.2; floor 1.0).
  DANAM_REFRESH=1   ignore the page cache and re-fetch.
"""
import json, os, re, sys, time, subprocess
from config import RAW, USER_AGENT

# Arches paginates this endpoint via `paging-filter` (the 1-based page number),
# NOT `page`. Each page returns a fixed slice of hits.
SEARCH = ("https://danam.cats.uni-heidelberg.de/search/resources"
          "?format=json&paging-filter={page}")
RESOURCE_URL = "https://danam.cats.uni-heidelberg.de/report/{rid}"

RAW_DIR = RAW / "danam"
RATE = max(1.0, float(os.environ.get("DANAM_RATE", "1.2")))
MAX_PAGES = int(os.environ["DANAM_MAX_PAGES"]) if os.environ.get("DANAM_MAX_PAGES") else None
REFRESH = os.environ.get("DANAM_REFRESH") == "1"

_TAG = re.compile(r"<[^>]+>")
_WS = re.compile(r"\s+")
_CODE = re.compile(r"\b([A-Z]{2,4}\d{2,5})\b")


def strip_html(s):
    if not s:
        return None
    s = _TAG.sub(" ", s)
    s = (s.replace("&nbsp;", " ").replace("&amp;", "&")
          .replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'"))
    return _WS.sub(" ", s).strip() or None


def fetch_page(page):
    """Return parsed JSON for a search page, using the on-disk cache."""
    cache = RAW_DIR / f"page_{page:04d}.json"
    if cache.exists() and cache.stat().st_size > 0 and not REFRESH:
        return json.load(open(cache))
    url = SEARCH.format(page=page)
    last = ""
    for attempt in range(1, 6):
        time.sleep(RATE)
        try:
            out = subprocess.run(
                ["curl", "-sS", "-m", "60", url,
                 "-H", f"User-Agent: {USER_AGENT}",
                 "-H", "Accept: application/json"],
                capture_output=True, check=True).stdout
            data = json.loads(out)
            cache.write_bytes(out)
            return data
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            last = str(e)
            backoff = RATE * (2 ** attempt)
            print(f"  page {page} attempt {attempt} failed ({e}); "
                  f"backoff {backoff:.1f}s", file=sys.stderr)
            time.sleep(backoff)
    raise RuntimeError(f"DANAM page {page} failed after retries: {last}")


def parse_displayname(name):
    """'IAST Name at X || देवनागरी || LAL2750' -> (label, devanagari, code)."""
    parts = [p.strip() for p in (name or "").split("||")]
    label = parts[0] if parts else None
    deva = next((p for p in parts[1:] if re.search(r"[ऀ-ॿ]", p)), None)
    code = None
    for p in parts:
        m = _CODE.search(p)
        if m:
            code = m.group(1); break
    if code and label:                      # drop a trailing bare code from label
        label = _CODE.sub("", label).strip(" |-") or label
    return label, deva, code


def coord(src):
    pts = src.get("points") or []
    if pts and isinstance(pts, list):
        p = pts[0].get("point") or {}
        if p.get("lat") is not None and p.get("lon") is not None:
            return float(p["lon"]), float(p["lat"])
    return None, None


def reshape(src):
    rid = src.get("resourceinstanceid")
    name = src.get("displayname")
    label, deva, code = parse_displayname(name)
    lon, lat = coord(src)
    return {
        "rid": rid,
        "code": code,                        # DANAM monument code, e.g. LAL2750
        "label": label,
        "label_ne": deva,
        "description": strip_html(src.get("displaydescription")),
        "lon": lon, "lat": lat,
        "graph_id": src.get("graph_id"),     # DANAM resource model
        "root_ontology_class": src.get("root_ontology_class"),
        "resource_url": RESOURCE_URL.format(rid=rid) if rid else None,
    }


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    first = fetch_page(1)
    res = first["results"]["hits"]
    total = res["total"]["value"] if isinstance(res["total"], dict) else res["total"]
    page_size = max(1, len(res["hits"]))
    n_pages = (total + page_size - 1) // page_size
    if MAX_PAGES:
        n_pages = min(n_pages, MAX_PAGES)
    print(f"DANAM: {total} resources, {page_size}/page -> {n_pages} pages "
          f"(rate {RATE}s){' [capped]' if MAX_PAGES else ''}", file=sys.stderr)

    out, seen = [], set()
    for page in range(1, n_pages + 1):
        data = first if page == 1 else fetch_page(page)
        hits = data["results"]["hits"]["hits"]
        for h in hits:
            rec = reshape(h["_source"])
            if rec["rid"] and rec["rid"] not in seen:
                seen.add(rec["rid"]); out.append(rec)
        if page % 25 == 0 or page == n_pages:
            print(f"  page {page}/{n_pages}  ({len(out)} records)", file=sys.stderr)

    path = RAW / "danam.json"
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
    geo = sum(1 for r in out if r["lat"] is not None)
    print(f"Wrote {len(out)} DANAM records ({geo} geolocated) -> {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
