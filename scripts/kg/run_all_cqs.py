"""Run every competency-question SPARQL block from cq_sparql.md against the live
Fuseki KG (TBox + ABox + all named graphs) and report results."""
import re, subprocess, sys, json
from config import ROOT, USER_AGENT

EP = "http://localhost:3030/heritagegraph/sparql"
GRAPHS = [
    "https://cair-nepal.org/heritagegraph/ontology",
    "https://data.cair-nepal.org/heritagegraph/graph/wikidata",
    "https://data.cair-nepal.org/heritagegraph/graph/openstreetmap",
    "https://data.cair-nepal.org/heritagegraph/graph/unesco",
    "https://data.cair-nepal.org/heritagegraph/graph/intangible",
    "https://data.cair-nepal.org/heritagegraph/graph/crosswalk",
]


def run(query):
    args = ["curl", "-sS", EP, "--data-urlencode", f"query={query}",
            "-H", "Accept: application/sparql-results+json",
            "-H", f"User-Agent: {USER_AGENT}"]
    for g in GRAPHS:
        args += ["--data-urlencode", f"default-graph-uri={g}",
                 "--data-urlencode", f"named-graph-uri={g}"]
    out = subprocess.run(args, capture_output=True)
    try:
        return json.loads(out.stdout)
    except Exception:
        return {"_error": out.stdout.decode()[:200]}


def parse():
    text = (ROOT / "cq_sparql.md").read_text()
    # pair each "CQn. ..." heading with the following ```sparql block```
    items = []
    pattern = re.compile(r"^(CQ\d+)\.\s*(.+?)\s*$", re.M)
    blocks = re.compile(r"```sparql\s*(.*?)```", re.S)
    # build index of heading positions
    heads = [(m.start(), m.group(1), m.group(2)) for m in pattern.finditer(text)]
    for m in blocks.finditer(text):
        # find the nearest preceding heading
        pos = m.start()
        head = max((h for h in heads if h[0] < pos), key=lambda h: h[0], default=None)
        if head:
            items.append((head[1], head[2], m.group(1).strip()))
    return items


def main():
    items = parse()
    passed = failed = 0
    print(f"Running {len(items)} competency-question queries against the live KG\n")
    for cq, question, query in items:
        res = run(query)
        if "_error" in res:
            status = "ERROR " + res["_error"]
        elif "boolean" in res:
            ok = res["boolean"]
            status = "PASS (true)" if ok else "FAIL (false)"
            passed += ok; failed += (not ok)
        else:
            n = len(res.get("results", {}).get("bindings", []))
            status = f"{n} rows"
        q = question if len(question) <= 84 else question[:81] + "..."
        print(f"{cq:6s} {status:14s} {q}")
    print(f"\nASK results: {passed} passed, {failed} failed (of {passed+failed} ASK queries)")


if __name__ == "__main__":
    main()
