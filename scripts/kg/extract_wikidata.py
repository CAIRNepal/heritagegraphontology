"""Extract Nepal cultural-heritage entities from Wikidata (CC0) -> data/raw/wikidata.json.

Pulls instances (incl. subclasses) of heritage-relevant types located in Nepal,
with labels (en + ne), coordinates, type, inception date, heritage designation,
religion, image and Wikidata QID for provenance/crosswalk.
"""
import json, sys
from config import WDQS, RAW
from fetch import post_form

# Heritage-relevant top types; subclasses captured via wdt:P279*
TYPES = [
    "wd:Q44539",    # temple
    "wd:Q842402",   # Hindu temple
    "wd:Q2654225",  # Buddhist temple
    "wd:Q570116",   # tourist monastery / gompa (vihara family)
    "wd:Q178065",   # stupa
    "wd:Q16970",    # church building
    "wd:Q1370598",  # place of worship
    "wd:Q132241",   # festival
    "wd:Q33506",    # museum
    "wd:Q839954",   # archaeological site
    "wd:Q19844914", # university building (kept out below; placeholder)
    "wd:Q4989906",  # monument
    "wd:Q24398318", # religious building
    "wd:Q1081138",  # historic site
]

QUERY = """
SELECT ?item
  (SAMPLE(?lab_en) AS ?itemLabel) (SAMPLE(?lab_ne) AS ?itemLabelNe)
  (SAMPLE(?d) AS ?desc) (SAMPLE(?c) AS ?coord)
  (SAMPLE(?inc) AS ?inception) (SAMPLE(?img) AS ?image)
  (GROUP_CONCAT(DISTINCT ?type; separator="|") AS ?types)
  (GROUP_CONCAT(DISTINCT ?her;  separator="|") AS ?heritage)
  (GROUP_CONCAT(DISTINCT ?rel;  separator="|") AS ?religions)
  (GROUP_CONCAT(DISTINCT ?sty;  separator="|") AS ?styles)
WHERE {
  VALUES ?t { %TYPES% }
  ?item wdt:P31/wdt:P279* ?t ; wdt:P17 wd:Q837 ; wdt:P31 ?type .
  OPTIONAL { ?item wdt:P625 ?c }
  OPTIONAL { ?item wdt:P571 ?inc }
  OPTIONAL { ?item wdt:P18  ?img }
  OPTIONAL { ?item wdt:P1435 ?her }
  OPTIONAL { ?item wdt:P140  ?rel }
  OPTIONAL { ?item wdt:P149  ?sty }
  OPTIONAL { ?item rdfs:label ?lab_en . FILTER(LANG(?lab_en)="en") }
  OPTIONAL { ?item rdfs:label ?lab_ne . FILTER(LANG(?lab_ne)="ne") }
  OPTIONAL { ?item schema:description ?d . FILTER(LANG(?d)="en") }
}
GROUP BY ?item
"""


def run(query):
    raw = post_form(WDQS, {"query": query},
                    "application/sparql-results+json", timeout=180)
    return json.loads(raw)


def main():
    q = QUERY.replace("%TYPES%", " ".join(TYPES))
    print("Querying Wikidata...", file=sys.stderr)
    res = run(q)
    rows = res["results"]["bindings"]
    qid = lambda u: u.rsplit("/", 1)[-1] if u else u
    qids = lambda s: [qid(x) for x in s.split("|") if x] if s else []
    out = []
    for b in rows:
        g = lambda k: b.get(k, {}).get("value")
        out.append({
            "qid": qid(g("item")),
            "label_en": g("itemLabel"),
            "label_ne": g("itemLabelNe"),
            "description": g("desc"),
            "coord": g("coord"),          # 'Point(lon lat)'
            "inception": g("inception"),
            "image": g("image"),
            "types": qids(g("types")),
            "heritage": qids(g("heritage")),
            "religions": qids(g("religions")),
            "styles": qids(g("styles")),
        })
    path = RAW / "wikidata.json"
    json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
    print(f"Wrote {len(out)} Wikidata entities -> {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
