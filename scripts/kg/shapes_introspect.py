import json, sys
from rdflib import Graph, RDF, Namespace, URIRef
from rdflib.namespace import RDFS
SH = Namespace("http://www.w3.org/ns/shacl#")
g = Graph(); g.parse("ontology/HeritageGraph.shacl.ttl", format="turtle")

def coll(g, node):
    out=[]
    while node and node != RDF.nil:
        f=g.value(node, RDF.first)
        if f is not None: out.append(f)
        node=g.value(node, RDF.rest)
    return out

shapes={}
for shape in g.subjects(RDF.type, SH.NodeShape):
    tc=g.value(shape, SH.targetClass)
    if tc is None: continue
    closed = g.value(shape, SH.closed)
    rec={"shape":str(shape),"targetClass":str(tc),
         "closed":bool(closed) and str(closed).lower()=="true","props":[]}
    for ps in g.objects(shape, SH.property):
        p={}
        path=g.value(ps, SH.path); p["path"]=str(path) if path else None
        for k,pred in [("minCount",SH.minCount),("maxCount",SH.maxCount),
                       ("datatype",SH.datatype),("cls",SH["class"]),
                       ("nodeKind",SH.nodeKind)]:
            v=g.value(ps,pred)
            if v is not None: p[k]=str(v)
        inn=g.value(ps, SH["in"])
        if inn is not None: p["in"]=[str(x) for x in coll(g,inn)]
        rec["props"].append(p)
    shapes[str(tc)]=rec

json.dump(shapes, open("data/raw/shapes_spec.json","w"), indent=1)
# print required-property summary
for tc,rec in sorted(shapes.items()):
    req=[p["path"].split("/")[-1].split("#")[-1] for p in rec["props"] if p.get("minCount") and int(p["minCount"])>=1]
    short=tc.split("/")[-1].split("#")[-1]
    print(f'{"C" if rec["closed"] else "o"} {short:38s} req={req}')
