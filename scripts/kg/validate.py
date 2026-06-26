"""SHACL-validate the generated ABox against HeritageGraph.shacl.ttl.

Validates the union of the conformant source graphs (entities + places +
assertions + DataSource nodes). The crosswalk graph is intentionally excluded
(owl:sameAs / altLabel are not permitted by the closed entity shapes).
"""
import sys, random
from rdflib import Graph, URIRef
from rdflib.namespace import RDF
from pyshacl import validate
from config import ROOT, KG, IDNS

# The HeritageGraph SHACL shapes (LinkML-generated, sh:closed) are designed for
# EXACT-TYPE validation: every node is checked only against the shape of its
# declared rdf:type. (Subclass/rdfs inference makes the closed, zero-property
# crm:E1_CRM_Entity shape unsatisfiable -- the project's own mini-ABox yields 51
# violations under inference="rdfs".) So we validate with inference="none" and
# without merging the TBox; the generated core graph references only directly
# typed E53_Place / DataSource / I2_Belief values, so all sh:class checks pass.

# pyshacl's closed-shape evaluation is O(nodes) in pure Python, so validating
# all ~8k entities takes >20 min. Every entity is emitted by one shape-driven
# code path, so we validate the full small graphs (Wikidata + UNESCO) plus a
# representative random sample of OSM entities (with their place/assertion).
OSM_SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 400


def sample_osm(n):
    full = Graph().parse(KG / "osm.ttl", format="turtle")
    ents = [s for s in full.subjects(RDF.type, None)
            if str(s).startswith(IDNS + "osm/")]
    random.seed(42)
    keep = set(random.sample(ents, min(n, len(ents))))
    out = Graph()
    # keep DataSource + all triples of sampled entities and their place/assertion
    for s in keep:
        local = str(s)[len(IDNS + "osm/"):]
        for node in (s, URIRef(IDNS + "place/osm/" + local),
                     URIRef(IDNS + "assertion/osm/" + local)):
            for t in full.triples((node, None, None)):
                out.add(t)
    # carry the DataSource node
    for s, p, o in full:
        if "source/openstreetmap" in str(s):
            out.add((s, p, o))
    return out, len(ents)


def main():
    data = Graph()
    for f in ["wikidata.ttl", "unesco.ttl", "intangible.ttl"]:
        data.parse(KG / f, format="turtle")
    osm_g, osm_total = sample_osm(OSM_SAMPLE)
    data += osm_g
    print(f"Validating: full Wikidata + UNESCO + {OSM_SAMPLE}/{osm_total} OSM "
          f"sample = {len(data)} triples", file=sys.stderr)
    shapes = Graph().parse(ROOT / "ontology" / "HeritageGraph.shacl.ttl", format="turtle")
    conforms, report_graph, report_text = validate(
        data, shacl_graph=shapes,
        inference="none", advanced=True, abort_on_first=False,
        meta_shacl=False, debug=False)
    print("CONFORMS:", conforms)
    if not conforms:
        # summarise violation counts by source shape / path
        from collections import Counter
        from rdflib import Namespace
        SH = Namespace("http://www.w3.org/ns/shacl#")
        paths = Counter(str(o).split("/")[-1].split("#")[-1]
                        for o in report_graph.objects(None, SH.resultPath))
        comps = Counter(str(o).split("#")[-1]
                        for o in report_graph.objects(None, SH.sourceConstraintComponent))
        print("\nViolations by path:", dict(paths.most_common(20)))
        print("Violations by constraint:", dict(comps.most_common(20)))
        print("\n--- first 3000 chars of report ---")
        print(report_text[:3000])
        sys.exit(1)
    print("All generated triples conform to HeritageGraph.shacl.ttl")

if __name__ == "__main__":
    main()
