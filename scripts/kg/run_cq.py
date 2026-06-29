"""Run competency-question SPARQL against the live Fuseki KG and print results."""
import sys, subprocess
from config import USER_AGENT

ENDPOINT = "http://localhost:3030/heritagegraph/sparql"
DATA = "https://data.cair-nepal.org/heritagegraph/graph/"
# Merge the data named graphs into the default graph for these queries
DEFAULT_GRAPHS = [DATA + g for g in ("wikidata", "openstreetmap", "unesco",
                                     "intangible", "danam", "crosswalk")]
PREFIX = """
PREFIX hg:   <https://cair-nepal.org/heritagegraph/>
PREFIX crm:  <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX crminf:<http://www.cidoc-crm.org/extensions/crminf/>
PREFIX geo:  <http://www.opengis.net/ont/geosparql#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct:  <http://purl.org/dc/terms/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
"""

# Data-level competency questions: each returns REAL bindings from the live KG.
# Numbers map to the natural-language CQs in cq_sparql.md that our open-data
# sources can actually answer (structural / spatial / typological / provenance).
CQS = [
    ("CQ1 (data)  Structures with a documented construction/inception date, chronologically",
     """SELECT ?date ?label ?type WHERE {
        ?s a ?type ; rdfs:label ?label ; hg:has_provenance_assertion ?a .
        ?a hg:asserted_value ?date .
        FILTER(STRSTARTS(STR(?type), STR(hg:)))
     } ORDER BY ?date LIMIT 15"""),

    ("CQ5 (data)  Heritage typologies WITHIN the Kathmandu Valley (geographic bbox)",
     """SELECT ?type (COUNT(?s) AS ?n) WHERE {
        ?s a ?type ; crm:P55_has_current_location ?p . ?p geo:asWKT ?wkt .
        BIND(xsd:double(REPLACE(STR(?wkt),"POINT\\\\(([0-9.]+) ([0-9.]+)\\\\)","$1")) AS ?lon)
        BIND(xsd:double(REPLACE(STR(?wkt),"POINT\\\\(([0-9.]+) ([0-9.]+)\\\\)","$2")) AS ?lat)
        FILTER(?lon > 85.2 && ?lon < 85.55 && ?lat > 27.6 && ?lat < 27.78)
        FILTER(STRSTARTS(STR(?type), STR(hg:)))
     } GROUP BY ?type ORDER BY DESC(?n)"""),

    ("CQ6 (data)  Heritage sharing a common architectural style",
     """SELECT ?style (COUNT(?s) AS ?n) (SAMPLE(?label) AS ?example) WHERE {
        ?s hg:has_architectural_style ?style ; rdfs:label ?label .
     } GROUP BY ?style ORDER BY DESC(?n)"""),

    ("CQ7 (data)  Buddhist monuments in the Kathmandu Valley with coordinates (sample)",
     """SELECT ?label ?wkt WHERE {
        ?s a hg:BuddhistMonument ; rdfs:label ?label ; crm:P55_has_current_location ?p .
        ?p geo:asWKT ?wkt .
        BIND(xsd:double(REPLACE(STR(?wkt),"POINT\\\\(([0-9.]+) ([0-9.]+)\\\\)","$1")) AS ?lon)
        FILTER(?lon > 85.2 && ?lon < 85.55)
     } ORDER BY ?label LIMIT 10"""),

    ("CQ (data)  Traditional water heritage — Dhunge Dhara + water structures (sample)",
     """SELECT ?type ?label ?wkt WHERE {
        VALUES ?type { hg:DhungeDhara hg:WaterStructure hg:Pokhari }
        ?s a ?type ; rdfs:label ?label ; crm:P55_has_current_location ?p .
        OPTIONAL { ?p geo:asWKT ?wkt }
     } LIMIT 12"""),

    ("CQ25 (data)  Cross-source corroboration: one entity attested by >1 source (shared QID)",
     """SELECT ?wd (COUNT(DISTINCT ?e) AS ?nSources)
               (GROUP_CONCAT(DISTINCT ?label; separator=" / ") AS ?labels) WHERE {
        ?e owl:sameAs ?wd ; rdfs:label ?label .
     } GROUP BY ?wd HAVING (COUNT(DISTINCT ?e) > 1) LIMIT 12"""),

    ("CQ (data)  Provenance: assertions by source, confidence and epistemic stance",
     """SELECT ?stance ?conf (COUNT(?a) AS ?n) WHERE {
        ?a a crminf:I2_Belief ; hg:epistemic_stance ?stance ; hg:confidence_score ?conf .
     } GROUP BY ?stance ?conf ORDER BY DESC(?n)"""),

    ("CQ (data)  UNESCO World Heritage components linked to Wikidata + coordinates",
     """SELECT ?label ?wd ?wkt WHERE {
        ?s prov:wasInfluencedBy <https://data.cair-nepal.org/heritagegraph/source/unesco-whc> ;
           rdfs:label ?label ; crm:P55_has_current_location ?p .
        OPTIONAL { ?p geo:asWKT ?wkt } OPTIONAL { ?s owl:sameAs ?wd }
     } ORDER BY ?label"""),

    ("CQ (data)  Whole-KG coverage: heritage entities per source named graph",
     """SELECT ?g (COUNT(DISTINCT ?s) AS ?entities) WHERE {
        GRAPH ?g { ?s a ?c . FILTER(STRSTARTS(STR(?c), STR(hg:))) } }
        GROUP BY ?g ORDER BY DESC(?entities)"""),

    # ---- intangible heritage (curated layer) ----
    ("CQ11 (data)  Festivals/jatras: invoked deity, recurrence and place",
     """SELECT ?festival ?deity ?recurrence WHERE {
        ?f a ?cls ; rdfs:label ?festival ; hg:invokes_deity ?d ; hg:recurrence_pattern ?recurrence .
        ?d rdfs:label ?deity .
        VALUES ?cls { hg:Festival hg:ChariotFestival hg:MaskedDance }
     } ORDER BY ?festival"""),

    ("CQ19 (data)  Which Guthi manages which ritual/festival",
     """SELECT ?guthi ?gtype ?managed WHERE {
        ?g a hg:Guthi ; rdfs:label ?guthi ; hg:guthi_type ?gt .
        BIND(REPLACE(STR(?gt),".*/","") AS ?gtype)
        OPTIONAL { ?f hg:managed_by_guthi ?g ; rdfs:label ?managed }
     } ORDER BY ?guthi"""),

    ("CQ9 (data)  Caste groups and their hereditary ritual roles",
     """SELECT ?caste ?role WHERE {
        ?c a hg:CasteGroup ; rdfs:label ?caste ; hg:traditional_role ?role .
     } ORDER BY ?caste"""),

    ("CQ12 (data)  Festival ritual sequence (sub-events)",
     """SELECT ?festival ?ritual WHERE {
        ?f crm:P9_consists_of ?r ; rdfs:label ?festival . ?r rdfs:label ?ritual .
     }"""),

    ("CQ25 (data)  Syncretic links across Hindu/Buddhist traditions",
     """SELECT ?relation ?primary ?equivalent ?type WHERE {
        ?s a hg:SyncreticRelationship ; rdfs:label ?relation ;
           hg:assigned_to_deity ?d ; hg:syncretic_type ?ty .
        ?d rdfs:label ?primary .
        BIND(REPLACE(STR(?ty),".*/","") AS ?type)
        OPTIONAL { ?s hg:assigned_equivalent ?e . ?e rdfs:label ?equivalent }
     }"""),

    ("CQ26 (data)  Living Goddess (Kumari): person, deity, residence, institution",
     """SELECT ?tenure ?person ?deity ?residence ?institution WHERE {
        ?t a crm:E4_Period ; rdfs:label ?tenure ;
           crm:P11_had_participant ?p ;
           crm:P14.1_in_the_role_of ?d ;
           crm:P74_has_current_or_former_residence ?r ;
           hg:supported_by_institution ?i .
        ?p rdfs:label ?person . ?d rdfs:label ?deity .
        ?r rdfs:label ?residence . ?i rdfs:label ?institution .
     }"""),
]


def run(query):
    args = ["curl", "-sS", ENDPOINT,
            "--data-urlencode", f"query={PREFIX}\n{query}",
            "-H", "Accept: text/csv", "-H", f"User-Agent: {USER_AGENT}"]
    for g in DEFAULT_GRAPHS:
        args += ["--data-urlencode", f"default-graph-uri={g}",
                 "--data-urlencode", f"named-graph-uri={g}"]
    out = subprocess.run(args, capture_output=True, check=True)
    return out.stdout.decode()


def main():
    for title, q in CQS:
        print("\n" + "=" * 78)
        print(title)
        print("-" * 78)
        rows = run(q).strip().splitlines()
        for r in rows[:16]:
            print("  " + r)
        if len(rows) > 16:
            print(f"  ... ({len(rows)-1} rows total)")


if __name__ == "__main__":
    main()
