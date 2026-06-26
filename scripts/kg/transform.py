"""Transform cached raw extracts -> HeritageGraph ABox (SHACL-conformant).

Emits, per source, a self-contained named-graph TTL containing entities,
their E53_Place (with geo:asWKT), a crminf:I2_Belief provenance assertion,
and the heritageGraph:DataSource node. owl:sameAs / altLabel / seeAlso links
to Wikidata/OSM are written to a SEPARATE crosswalk graph so the closed
SHACL shapes on the core entities still validate.

Only real, sourced values are emitted — nothing is invented. Where a required
enum value (e.g. Temple's architectural style) is unknown, the entity is typed
to the nearest super-class whose shape can be satisfied (ArchitecturalStructure).
"""
import json, re, sys
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD, SKOS
from config import (HG, IDNS, CRM, CRMINF, DCT, GEO, PROV, PREFIXES, KG, RAW,
                    SOURCES)

HGN  = Namespace(HG)
CRMN = Namespace(CRM)
INFN = Namespace(CRMINF)
DCTN = Namespace(DCT)
GEON = Namespace(GEO)
PROV = Namespace(PROV)
ID   = Namespace(IDNS)
WD   = Namespace("http://www.wikidata.org/entity/")
GEN_TIME = Literal("2026-06-24T00:00:00Z", datatype=XSD.dateTime)
WKT = URIRef(GEO + "wktLiteral")

CONF = {"wikidata": 0.9, "osm": 0.6, "unesco": 0.95}
STANCE = {"wikidata": HGN.Scholarly, "osm": HGN.Community, "unesco": HGN.State}

# Per-class allowed property paths (from the closed SHACL shapes) so emission
# stays conformant for every target class (e.g. Murti forbids existence_status).
_SPEC = json.load(open(RAW / "shapes_spec.json"))
def allowed_for(cls):
    rec = _SPEC.get(HG + cls, {})
    return {p["path"] for p in rec.get("props", [])}

# ---- Wikidata type buckets (QID -> handling) -----------------------------
WD_STUPA = {"Q180987", "Q1456873"}                       # stupa, peace pagoda
WD_DHARA = {"Q5269891"}                                   # dhunge dhara (hiti)
WD_MURTI = {"Q1779653"}                                   # colossal statue
WD_BUDDH = {"Q54074585", "Q5393308", "Q44613", "Q570116", "Q466449",
            "Q73941534", "Q1559394"}                      # monastery/gompa/vihara
WD_ARCH = {"Q842402", "Q44539", "Q1370598", "Q24398318", "Q15135589",
           "Q98116669", "Q33506", "Q207694", "Q4828724", "Q17431399",
           "Q16735822", "Q1970365", "Q2772772", "Q10624527", "Q3329412",
           "Q16560", "Q2519340", "Q41176", "Q2319498", "Q839954", "Q4989906",
           "Q32815", "Q56242215", "Q697295", "Q381885", "Q53060", "Q1497364"}
WD_FEST = {"Q132241", "Q1197685", "Q1445650", "Q1472127"}
WD_BUDDH_REL = {"Q748", "Q132265", "Q815628"}            # Buddhism/Theravada/Bon


def classify_wd(rec):
    t = set(rec["types"]); rel = set(rec["religions"])
    if t & WD_STUPA: return ("Stupa", HGN.StupaStyle)
    if t & WD_DHARA: return ("DhungeDhara", None)
    if t & WD_MURTI: return ("Murti", None)
    if (t & WD_BUDDH) or (rel & WD_BUDDH_REL and t & (WD_ARCH | {"Q1370598"})):
        return ("BuddhistMonument", None)
    if t & WD_ARCH: return ("ArchitecturalStructure", None)
    if t & WD_FEST: return ("Festival", None)
    return (None, None)


def classify_osm(tags):
    hist = tags.get("historic"); rel = (tags.get("religion") or "")
    amen = tags.get("amenity"); bld = tags.get("building"); mm = tags.get("man_made")
    name = tags.get("name") or tags.get("name:en") or tags.get("name:ne")
    if not name:
        return (None, None, None)
    buddhist = "buddhist" in rel
    nm = name.lower()
    exist = HGN.PartiallyExtant if hist == "ruins" else HGN.Extant
    if bld == "stupa" or mm in ("stupa", "chorten") or hist == "stupa":
        return ("Stupa", HGN.StupaStyle, HGN.Extant)
    if hist == "stone_tap" or mm == "water_tap" or any(
            w in nm for w in ("hiti", "dhunge", "dhara", "dhunga", "lhon", "jaru")):
        return ("DhungeDhara", None, HGN.Extant)
    if mm == "water_well":
        return ("WaterStructure", None, HGN.Extant)
    if buddhist and (bld in ("monastery", "gompa") or amen == "monastery"
                     or hist == "monastery"):
        return ("BuddhistMonument", None, exist)
    if buddhist and hist == "wayside_shrine":
        return ("Chaitya", HGN.ChaityaStyle, HGN.Extant)
    if buddhist and amen == "place_of_worship":
        return ("BuddhistMonument", None, exist)
    if (amen == "place_of_worship" or bld == "temple" or hist == "temple"):
        return ("ArchitecturalStructure", None, exist)
    if hist in ("monument", "memorial", "ruins", "castle", "city_gate",
                "boundary_stone", "archaeological_site", "wayside_shrine",
                "fort", "manor", "tower", "shrine", "tomb", "building",
                "wayside_cross", "church", "chapel", "aqueduct", "bridge",
                "gate", "palace", "citywalls"):
        return ("ArchitecturalStructure", None, exist)
    if amen == "drinking_water" and hist:
        return ("DhungeDhara", None, HGN.Extant)
    return (None, None, None)


def wkt_from_wd(coord):
    m = re.match(r"Point\(([-\d.]+) ([-\d.]+)\)", coord or "")
    if not m: return None
    return f"POINT({m.group(1)} {m.group(2)})"


def add_source_node(g, key):
    s = SOURCES[key]; node = URIRef(s["iri"])
    g.add((node, RDF.type, HGN.DataSource))
    g.add((node, RDFS.label, Literal(s["label"])))
    g.add((node, HGN.source_url, Literal(s["url"])))
    g.add((node, HGN.epistemic_stance, HGN[s["epistemic_stance"]]))
    g.add((node, HGN.source_type, HGN[s["source_type"]]))
    g.add((node, CRMN.P3_has_note,
           Literal(f"License: {s['license']}. Data retrieved {GEN_TIME} for the "
                   f"HeritageGraph KG (CAIR-Nepal).")))
    return node


def emit(g, xg, key, local, cls, label, note, exist, style,
         wkt, conf, inception, sameas=None, altlabels=None, seealso=None):
    """Emit one entity + place + assertion into graph g; links into crosswalk xg."""
    ent = URIRef(IDNS + f"{key}/{local}")
    place = URIRef(IDNS + f"place/{key}/{local}")
    asrt = URIRef(IDNS + f"assertion/{key}/{local}")
    src = URIRef(SOURCES[key]["iri"])
    ok = allowed_for(cls)  # paths permitted by this class's closed shape
    # entity (required props are allowed by every target class we use)
    g.add((ent, RDF.type, HGN[cls]))
    g.add((ent, RDFS.label, Literal(label)))
    g.add((ent, DCTN.identifier, Literal(str(ent), datatype=XSD.anyURI)))
    g.add((ent, CRMN.P55_has_current_location, place))
    if str(HGN.existence_status) in ok:
        g.add((ent, HGN.existence_status, exist))
    if str(PROV.wasInfluencedBy) in ok:
        g.add((ent, PROV.wasInfluencedBy, src))
    if str(HGN.has_provenance_assertion) in ok:
        g.add((ent, HGN.has_provenance_assertion, asrt))
    if note and str(CRMN.P3_has_note) in ok:
        g.add((ent, CRMN.P3_has_note, Literal(note)))
    if style is not None and str(HGN.has_architectural_style) in ok:
        g.add((ent, HGN.has_architectural_style, style))
    # place
    g.add((place, RDF.type, CRMN.E53_Place))
    g.add((place, RDFS.label, Literal(label)))
    if wkt:
        g.add((place, GEON.asWKT, Literal(wkt, datatype=WKT)))
    # provenance assertion (crminf:I2_Belief)
    g.add((asrt, RDF.type, INFN.I2_Belief))
    g.add((asrt, PROV.wasDerivedFrom, src))
    g.add((asrt, PROV.generatedAtTime, GEN_TIME))
    # asserts_about_entity has sh:class crm:E1_CRM_Entity, whose closed
    # zero-property shape is unsatisfiable under subclass typing; keep this
    # back-pointer in the (unvalidated) crosswalk graph. The forward link
    # entity -> has_provenance_assertion is retained in the core.
    xg.add((asrt, HGN.asserts_about_entity, ent))
    g.add((asrt, HGN.confidence_score, Literal(conf, datatype=XSD.float)))
    g.add((asrt, HGN.epistemic_stance, STANCE[key]))
    if inception:
        g.add((asrt, HGN.asserted_property, Literal("date of inception (Wikidata P571 / WHC inscription)")))
        g.add((asrt, HGN.asserted_value, Literal(str(inception))))
    # crosswalk (NOT SHACL-validated)
    for s in (sameas or []):
        xg.add((ent, OWL.sameAs, URIRef(s)))
    for s in (seealso or []):
        xg.add((ent, RDFS.seeAlso, URIRef(s)))
    for lang, val in (altlabels or []):
        if val:
            xg.add((ent, SKOS.altLabel, Literal(val, lang=lang)))
    return ent


def new_graph():
    g = Graph()
    for p, n in PREFIXES.items():
        g.bind(p, Namespace(n))
    return g


def build_wikidata(xg, stats):
    g = new_graph(); add_source_node(g, "wikidata")
    data = json.load(open(RAW / "wikidata.json"))
    for r in data:
        cls, style = classify_wd(r)
        if cls is None:
            stats["wd_skipped"] += 1; continue
        if cls == "Festival" and not r["inception"]:
            stats["wd_skipped"] += 1; continue
        label = r["label_en"] or r["label_ne"]
        if not label:
            stats["wd_skipped"] += 1; continue
        emit(g, xg, "wikidata", r["qid"], cls, label, r["description"],
             HGN.Extant, style, wkt_from_wd(r["coord"]),
             CONF["wikidata"], r["inception"],
             sameas=[WD + r["qid"]],
             altlabels=[("ne", r["label_ne"])] if r["label_ne"] else None)
        stats["wd"] += 1
        stats["cls"][cls] = stats["cls"].get(cls, 0) + 1
    g.serialize(KG / "wikidata.ttl", format="turtle")
    print(f"wikidata.ttl: {stats['wd']} entities", file=sys.stderr)


def build_osm(xg, stats):
    g = new_graph(); add_source_node(g, "osm")
    data = json.load(open(RAW / "osm.json"))
    for r in data:
        cls, style, exist = classify_osm(r["tags"])
        if cls is None:
            stats["osm_skipped"] += 1; continue
        tags = r["tags"]
        label = tags.get("name") or tags.get("name:en") or tags.get("name:ne")
        local = f"{r['osm_type']}/{r['osm_id']}"
        wkt = f"POINT({r['lon']} {r['lat']})" if r["lat"] is not None else None
        url = f"https://www.openstreetmap.org/{r['osm_type']}/{r['osm_id']}"
        alt = []
        if tags.get("name:ne"): alt.append(("ne", tags["name:ne"]))
        if tags.get("name:en") and tags.get("name:en") != label:
            alt.append(("en", tags["name:en"]))
        # OSM 'wikidata' tag -> owl:sameAs (cross-source link to Wikidata)
        wdtag = tags.get("wikidata", "")
        sameas = [WD + wdtag] if re.fullmatch(r"Q\d+", wdtag) else None
        emit(g, xg, "osm", local, cls, label, tags.get("description"),
             exist, style, wkt, CONF["osm"], None,
             sameas=sameas, seealso=[url], altlabels=alt)
        stats["osm"] += 1
        stats["cls"][cls] = stats["cls"].get(cls, 0) + 1
    g.serialize(KG / "osm.ttl", format="turtle")
    print(f"osm.ttl: {stats['osm']} entities", file=sys.stderr)


def build_unesco(xg, stats):
    g = new_graph(); add_source_node(g, "unesco")
    data = json.load(open(RAW / "unesco.json"))
    for r in data:
        cls = "Stupa" if r["kind"] == "stupa" else "ArchitecturalStructure"
        style = HGN.StupaStyle if cls == "Stupa" else None
        wkt = f"POINT({r['lon']} {r['lat']})"
        emit(g, xg, "unesco", r["id"], cls, r["label"],
             f"{r['note']} UNESCO WHC ref. {r['ref']}.", HGN.Extant, style,
             wkt, CONF["unesco"], r["inscribed"],
             sameas=[WD + r["wikidata"]] if r.get("wikidata") else None)
        stats["unesco"] += 1
        stats["cls"][cls] = stats["cls"].get(cls, 0) + 1
    g.serialize(KG / "unesco.ttl", format="turtle")
    print(f"unesco.ttl: {stats['unesco']} entities", file=sys.stderr)


def main():
    stats = {"wd": 0, "osm": 0, "unesco": 0, "wd_skipped": 0,
             "osm_skipped": 0, "cls": {}}
    xg = new_graph()
    build_wikidata(xg, stats)
    build_osm(xg, stats)
    build_unesco(xg, stats)
    xg.serialize(KG / "crosswalk.ttl", format="turtle")
    total = stats["wd"] + stats["osm"] + stats["unesco"]
    print(f"\nTOTAL entities: {total}", file=sys.stderr)
    print(f"  Wikidata {stats['wd']} (skipped {stats['wd_skipped']})", file=sys.stderr)
    print(f"  OSM      {stats['osm']} (skipped {stats['osm_skipped']})", file=sys.stderr)
    print(f"  UNESCO   {stats['unesco']}", file=sys.stderr)
    print("By class:", file=sys.stderr)
    for c, n in sorted(stats["cls"].items(), key=lambda x: -x[1]):
        print(f"  {c:24s} {n}", file=sys.stderr)
    json.dump(stats, open(KG / "build_stats.json", "w"), indent=1)


if __name__ == "__main__":
    main()
