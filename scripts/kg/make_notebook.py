"""Generate the 'Get to Know a Dataset' notebook for the HeritageGraph KG,
mirroring the AWS Registry of Open Data template structure."""
import json, sys

cells = []
def md(t): cells.append({"cell_type": "markdown", "metadata": {}, "id": f"cell-{len(cells):02d}", "source": t})
def code(t): cells.append({"cell_type": "code", "metadata": {}, "id": f"cell-{len(cells):02d}", "source": t, "outputs": [], "execution_count": None})

md("""# Get to Know a Dataset: HeritageGraph — A Knowledge Graph of Nepal's Cultural Heritage

This notebook is a guided tour of the [**HeritageGraph**](https://registry.opendata.aws/heritagegraph) dataset: an RDF knowledge graph of Nepal's tangible and intangible cultural heritage, built on the [HeritageGraph ontology](https://cairnepal.github.io/heritagegraphontology/) (CIDOC-CRM aligned) and populated from trusted open sources. More usage examples, tutorials, and documentation for this dataset and others can be found at the [Registry of Open Data on AWS](https://registry.opendata.aws/).

The KG contains **~7,850 tangible heritage entities** (temples, stupas, monasteries, traditional water spouts, monuments) plus a curated **intangible-heritage** layer (festivals, Guthi institutions, the Living-Goddess Kumari, caste ritual roles, deities and syncretic relationships) — every entity carrying machine-readable **provenance** and a link back to its source.""")

md("""### Q: How have you organized your dataset? Help us understand the key prefix structure of your S3 bucket.

At the top level of our S3 bucket we use a single key prefix `heritagegraph/`, which contains:

1. `LICENSE.txt` and `README.md` — licensing and dataset documentation.
2. `ontology/` — the **schema (TBox)**: the HeritageGraph OWL ontology (`HeritageGraph.ttl`), its SHACL shapes (`HeritageGraph.shacl.ttl`), and the LinkML source. The schema is documented at `https://cairnepal.github.io/heritagegraphontology/`.
3. `kg/` — the **data (ABox)** as RDF Turtle, split into one file per **named graph / source**, so each source can be used under its own license:
   - `wikidata.ttl` — entities from Wikidata (**CC0**)
   - `osm.ttl` — physical features from OpenStreetMap (**ODbL**)
   - `unesco.ttl` — UNESCO World Heritage cultural components
   - `intangible.ttl` — curated intangible heritage (cited + Wikidata-linked)
   - `crosswalk.ttl` — `owl:sameAs` links to Wikidata/OSM and provenance back-links
   - `intangible_crosswalk.ttl` — intangible-layer `owl:sameAs` / typing links
4. `examples/` — SPARQL competency questions, sample results and build statistics.

Instance IRIs are minted under `https://data.cair-nepal.org/heritagegraph/`. Let's connect and list the structure.""")

code('''# This notebook requires the following additional libraries
# (install with pip/conda as preferred for your environment):
#
#   rdflib >= 7.0.0
#   matplotlib >= 3.8.0
#   boto3 >= 1.34.0

import io, os, re
from collections import Counter

import boto3
from botocore import UNSIGNED
from botocore.config import Config
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace''')

code('''# The HeritageGraph KG is published as RDF Turtle named-graph files.
# Set BUCKET to the public S3 bucket once it is provisioned by the Registry of
# Open Data. Until then, this notebook transparently falls back to the bundled
# heritagegraph/kg directory alongside this notebook.

BUCKET     = "[BUCKET_NAME]"            # e.g. "cair-nepal-heritagegraph"
KG_PREFIX  = "heritagegraph/kg/"
LOCAL_DIR  = "heritagegraph/kg"         # bundled alongside this notebook
GRAPH_FILES = [
    "wikidata.ttl", "osm.ttl", "unesco.ttl", "intangible.ttl",
    "crosswalk.ttl", "intangible_crosswalk.ttl",
]

# Public buckets do not require signed requests.
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
USING_S3 = not BUCKET.startswith("[")

def read_ttl(name):
    """Return the bytes of a Turtle file from S3 (if configured) or locally."""
    if USING_S3:
        return s3.get_object(Bucket=BUCKET, Key=KG_PREFIX + name)["Body"].read()
    with open(os.path.join(LOCAL_DIR, name), "rb") as fh:
        return fh.read()

if USING_S3:
    for item in s3.list_objects_v2(Bucket=BUCKET, Prefix="heritagegraph/", Delimiter="/").get("CommonPrefixes", []):
        print(item["Prefix"])
else:
    print("Local mode — prefix structure under heritagegraph/:")
    for entry in ["LICENSE.txt", "README.md", "ontology/", "kg/", "examples/"]:
        print(" ", entry)
    print("  kg/ files:")
    for f in GRAPH_FILES:
        print("   ", f)''')

md("""### Q: What data formats are present in your dataset? What kinds of data are stored using these formats?

The dataset is distributed as **RDF 1.1 Turtle** (`.ttl`) — a compact, human-readable serialization of the *Resource Description Framework*. The data is a **graph** of `subject – predicate – object` triples, e.g.:

```turtle
<.../id/unesco/swayambhu> a heritageGraph:Stupa ;
    rdfs:label "Swayambhunath" ;
    crm:P55_has_current_location <.../place/unesco/swayambhu> .
<.../place/unesco/swayambhu> geo:asWKT "POINT(85.2903 27.7149)"^^geo:wktLiteral .
```

We chose RDF/Turtle because cultural-heritage data is **highly interconnected and semantically rich**, and RDF:
- models entities, events and relationships natively (the schema is aligned to **CIDOC-CRM**, the ISO standard for cultural-heritage information);
- carries **provenance** as first-class data (every fact links to its source via `prov:` and `crminf:I2_Belief`);
- supports **named graphs**, so each source keeps its own license and can be queried in isolation or in union;
- is queryable with **SPARQL**, the W3C standard graph query language.

**Tooling.** Python users can work with the data using [`rdflib`](https://rdflib.readthedocs.io/). For server-side querying at scale, load the files into a triplestore such as [**Amazon Neptune**](https://aws.amazon.com/neptune/) (which speaks SPARQL natively), [Apache Jena Fuseki](https://jena.apache.org/), or [GraphDB](https://graphdb.ontotext.com/). The accompanying SHACL shapes (`ontology/HeritageGraph.shacl.ttl`) let you validate any extension of the graph.""")

md("""### Q: Can you show us an example of downloading and loading data from your dataset?

Let's load the named-graph Turtle files into a single in-memory `rdflib.Graph` for analysis, and look at how many triples and entities we have.""")

code('''# Load all named-graph files into one rdflib Graph for analysis
g = Graph()
for name in GRAPH_FILES:
    g.parse(data=read_ttl(name), format="turtle")

HG  = Namespace("https://cair-nepal.org/heritagegraph/")
print(f"Loaded {len(g):,} triples from {len(GRAPH_FILES)} named-graph files")''')

code('''# How many heritage entities of each ontology class?
q = """
PREFIX hg: <https://cair-nepal.org/heritagegraph/>
SELECT ?cls (COUNT(?s) AS ?n) WHERE {
  ?s a ?cls . FILTER(STRSTARTS(STR(?cls), STR(hg:)))
} GROUP BY ?cls ORDER BY DESC(?n)
"""
rows = [(str(r.cls).split("/")[-1], int(r.n)) for r in g.query(q)]
for cls, n in rows:
    print(f"{n:6,}  {cls}")''')

md("""### Q: A picture is worth a thousand words. Show us a visual from your dataset.

First, the distribution of heritage entities by class. Then — because heritage is inherently *spatial* — a map of every geolocated entity across Nepal, coloured by source.""")

code('''# 1) Entity counts per class (exclude the controlled-vocabulary / DataSource rows)
SKIP = {"DataSource"}
data = [(c, n) for c, n in rows if c not in SKIP and not c.endswith("Enum")]
labels, counts = zip(*data)

plt.figure(figsize=(11, 6), dpi=100)
plt.barh(labels[::-1], counts[::-1], color="#2c7fb8", edgecolor="white")
plt.xscale("log")
plt.title("HeritageGraph: entities per class", fontsize=15, fontweight="bold", pad=15)
plt.xlabel("Number of entities (log scale)")
for ax in [plt.gca()]:
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
plt.tight_layout(); plt.show()''')

code('''# 2) Map every geolocated entity across Nepal, coloured by source named graph.
#    We read the WKT POINT geometry on each entity's E53_Place, and the source
#    via prov:wasInfluencedBy.
q = """
PREFIX hg:   <https://cair-nepal.org/heritagegraph/>
PREFIX crm:  <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX geo:  <http://www.opengis.net/ont/geosparql#>
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT ?wkt ?src WHERE {
  ?s crm:P55_has_current_location ?p ; prov:wasInfluencedBy ?src .
  ?p geo:asWKT ?wkt .
}
"""
pat = re.compile(r"POINT\\(([-0-9.]+) ([-0-9.]+)\\)")
pts = {}
for r in g.query(q):
    m = pat.match(str(r.wkt))
    if not m:
        continue
    src = str(r.src).split("/")[-1]
    pts.setdefault(src, []).append((float(m.group(1)), float(m.group(2))))

plt.figure(figsize=(12, 7), dpi=100)
colors = {"wikidata": "#d95f02", "openstreetmap": "#1b9e77",
          "unesco-whc": "#7570b3", "cair-curated-intangible": "#e7298a"}
for src, coords in sorted(pts.items(), key=lambda kv: -len(kv[1])):
    xs, ys = zip(*coords)
    plt.scatter(xs, ys, s=6, alpha=0.5, label=f"{src} ({len(coords):,})",
                color=colors.get(src, "#666666"))
plt.title("Geolocated cultural heritage across Nepal", fontsize=15, fontweight="bold", pad=15)
plt.xlabel("Longitude"); plt.ylabel("Latitude")
plt.legend(markerscale=2, fontsize=9, loc="lower right")
plt.gca().set_aspect(1.0)
plt.tight_layout(); plt.show()''')

md("""### Q: What is one question that you have answered using these data?

**Question: which are the oldest dated heritage structures in Nepal, and how confident are we?**

Every dated fact in the KG is recorded as a provenance assertion (`crminf:I2_Belief`) with a `confidence_score` and an `epistemic_stance`, so we can answer this *and* report how trustworthy each date is.""")

code('''q = """
PREFIX hg:     <https://cair-nepal.org/heritagegraph/>
PREFIX rdfs:   <http://www.w3.org/2000/01/rdf-schema#>
PREFIX crminf: <http://www.cidoc-crm.org/extensions/crminf/>
SELECT ?label ?date ?conf WHERE {
  ?s rdfs:label ?label ; hg:has_provenance_assertion ?a .
  ?a hg:asserted_value ?date ; hg:confidence_score ?conf .
} ORDER BY ?date LIMIT 12
"""
print(f"{'date':>12}  {'conf':>4}  label")
print("-" * 60)
for r in g.query(q):
    year = str(r.date)[:10]
    print(f"{year:>12}  {float(r.conf):>4.2f}  {r.label}")''')

md("""The oldest entries — Changu Narayan (4th century CE), Kumbheshwar and the Hiranya Varna Mahavihar (the Golden Temple) — are among the monuments scholars regard as the valley's earliest, and each date is tied to a citable source with an explicit confidence. This is the kind of *provenance-aware* querying RDF makes natural: the answer comes with its evidence.""")

md("""### Q: What is one unanswered question that you think could be answered using these data?

**Challenge: reconstruct the living ritual landscape of the Kathmandu Valley by linking the *intangible* to the *tangible* in space and time.**

The KG already connects festivals and processions (e.g. *Rato Machhindranath Jatra*, *Indra Jatra*) to the deities they invoke, the Guthi institutions that fund them, and the caste groups that perform them. It separately contains thousands of geolocated temples, *dhunge dhara* (stone water spouts), *patis* and stupas. A compelling open task is to **fuse these layers**: infer and map the processional *routes* that connect named start/end places to the physical monuments along the way, align them to the lunar festival calendar, and surface where ritual practice and built heritage are most densely entangled (and therefore most at risk after events such as the 2015 earthquake).

**Advice for someone tackling this:** start from the `start_place`/`route_places` of the intangible layer, spatially join to nearby `crm:E53_Place` geometries via the `geo:asWKT` coordinates, and use the `owl:sameAs` crosswalk to pull richer context from Wikidata/OSM. The SHACL shapes let you validate any new links you assert, and the provenance model lets you keep community, scholarly and state sources distinguishable. Contributions of field-survey or oral-history data (e.g. via the Nepal Heritage Documentation Project) would extend the intangible layer substantially.""")

md("# DATA PROVIDER: PLEASE REMEMBER TO CLEAR ALL OUTPUTS BEFORE COMMITTING TO YOUR GITHUB REPOSITORY")

nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
    "cells": cells,
}
out = sys.argv[1] if len(sys.argv) > 1 else "get-to-know-the-heritagegraph-kg.ipynb"
with open(out, "w") as fh:
    json.dump(nb, fh, indent=1)
print("wrote", out, "with", len(cells), "cells")
