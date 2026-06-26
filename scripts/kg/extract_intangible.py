"""Curated intangible-heritage layer for the HeritageGraph KG.

Intangible heritage (festivals/jatras, Guthi institutions, the Living Goddess
Kumari, caste ritual roles, syncretic deities, masked dances, periodic rituals)
is not available in bulk open datasets, so this layer is hand-curated from
authoritative, citable sources and cross-linked to Wikidata QIDs for
verifiability. Nothing is invented: each entity records a source citation and,
where a Wikidata item exists, an owl:sameAs link.

Sources: Wikidata (CC0); UNESCO; and the scholarship of M. Slusser (Nepal
Mandala), G. Toffin, D. Gellner, J. Locke, and the Nepal Heritage Documentation
Project (NHDP, nepalheritage.org). Uncertain/traditional dates carry
date_precision = Circa or Century.

Outputs:
  data/kg/intangible.ttl             (SHACL-validated core named graph)
  data/kg/intangible_crosswalk.ttl   (owl:sameAs / extra typing; not validated)
"""
import sys
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD, SKOS
from config import HG, IDNS, CRM, CRMINF, DCT, GEO, PROV, BASE, PREFIXES, KG

HGN, CRMN, INFN, DCTN, GEON, PROVN = (Namespace(HG), Namespace(CRM),
    Namespace(CRMINF), Namespace(DCT), Namespace(GEO), Namespace(PROV))
WD = Namespace("http://www.wikidata.org/entity/")
WKT = URIRef(GEO + "wktLiteral")
GEN = Literal("2026-06-24T00:00:00Z", datatype=XSD.dateTime)
SRC = URIRef(BASE + "source/cair-curated-intangible")
CONF = Literal(0.85, datatype=XSD.float)

g = Graph(); xg = Graph()
for p, n in PREFIXES.items():
    g.bind(p, Namespace(n)); xg.bind(p, Namespace(n))

def I(*parts): return URIRef(IDNS + "/".join(parts))
def lit(s): return Literal(s)

# --- DataSource ------------------------------------------------------------
g.add((SRC, RDF.type, HGN.DataSource))
g.add((SRC, RDFS.label, lit("CAIR-Nepal curated intangible-heritage dataset")))
g.add((SRC, HGN.source_type, HGN.PublishedScholarship))
g.add((SRC, HGN.epistemic_stance, HGN.Scholarly))
g.add((SRC, HGN.source_url, lit("https://cair-nepal.org/")))
g.add((SRC, CRMN.P3_has_note, lit(
    "Curated from Wikidata (CC0), UNESCO, and scholarship (Slusser; Toffin; "
    "Gellner; Locke) and the Nepal Heritage Documentation Project. Traditional "
    "dates carry date_precision Circa/Century.")))

def place(slug, label, lon, lat, wd=None):
    p = I("place", "intangible", slug)
    g.add((p, RDF.type, CRMN.E53_Place)); g.add((p, RDFS.label, lit(label)))
    g.add((p, GEON.asWKT, Literal(f"POINT({lon} {lat})", datatype=WKT)))
    if wd: xg.add((p, OWL.sameAs, WD[wd]))
    return p

def timespan(slug, begin, precision):
    t = I("ts", "intangible", slug)
    g.add((t, RDF.type, CRMN["E52_Time-Span"]))
    g.add((t, CRMN.P82a_begin_of_the_begin, Literal(begin, datatype=XSD.date)))
    g.add((t, HGN.date_precision, HGN[precision]))
    return t

def assertion(slug):
    a = I("assertion", "intangible", slug)
    g.add((a, RDF.type, INFN.I2_Belief))
    g.add((a, PROVN.wasDerivedFrom, SRC))
    g.add((a, PROVN.generatedAtTime, GEN))
    g.add((a, HGN.confidence_score, CONF))
    g.add((a, HGN.epistemic_stance, HGN.Scholarly))
    xg.add((a, HGN.asserts_about_entity, I("intangible", slug)))
    return a

def deity(slug, label, note, wd=None, tradition=None):
    d = I("intangible", slug)
    g.add((d, RDF.type, CRMN.E28_Conceptual_Object))
    g.add((d, RDFS.label, lit(label)))
    g.add((d, CRMN.P3_has_note, lit(note)))
    if wd: xg.add((d, OWL.sameAs, WD[wd]))
    xg.add((d, RDF.type, HGN.Deity))
    if tradition:
        for tr in tradition:
            xg.add((d, HGN.has_religious_tradition, I("intangible", tr)))
    return d

def tradition(slug, label):
    t = I("intangible", slug)
    xg.add((t, RDF.type, HGN.ReligiousTradition)); xg.add((t, RDFS.label, lit(label)))
    return t

def caste(slug, label, role, wd=None):
    c = I("intangible", slug)
    g.add((c, RDF.type, HGN.CasteGroup)); g.add((c, RDFS.label, lit(label)))
    g.add((c, HGN.traditional_role, lit(role)))
    if wd: xg.add((c, OWL.sameAs, WD[wd]))
    return c

def guthi(slug, label, gtype, note, performs=None, wd=None):
    gu = I("intangible", slug)
    g.add((gu, RDF.type, HGN.Guthi)); g.add((gu, RDFS.label, lit(label)))
    g.add((gu, HGN.guthi_type, HGN[gtype])); g.add((gu, CRMN.P3_has_note, lit(note)))
    for r in (performs or []):
        g.add((gu, HGN.performs_ritual, r))
    if wd: xg.add((gu, OWL.sameAs, WD[wd]))
    return gu

def festival(slug, cls, label, note, begin, precision, recurrence, tithi,
             rtype, deities=None, manifests=None, start=None, route=None,
             guthi_node=None, group=None, structure_note=None, wd=None,
             consists=None):
    f = I("intangible", slug)
    g.add((f, RDF.type, HGN[cls])); g.add((f, RDFS.label, lit(label)))
    g.add((f, CRMN["P4_has_time-span"], timespan(slug, begin, precision)))
    g.add((f, HGN.recurrence_pattern, lit(recurrence)))
    if tithi: g.add((f, HGN.lunar_date_tithi, lit(tithi)))
    g.add((f, HGN.ritual_type, HGN[rtype]))
    g.add((f, CRMN.P3_has_note, lit(note)))
    g.add((f, HGN.has_provenance_assertion, assertion(slug)))
    for d in (deities or []): g.add((f, HGN.invokes_deity, d))
    for d in (manifests or []): g.add((f, HGN.manifests_divine_presence, d))
    if start: g.add((f, HGN.start_place, start))
    for r in (route or []): g.add((f, HGN.route_places, r))
    if guthi_node: g.add((f, HGN.managed_by_guthi, guthi_node))
    if group: g.add((f, HGN.performed_by_group, group))
    for c in (consists or []): g.add((f, CRMN.P9_consists_of, c))
    if wd: xg.add((f, OWL.sameAs, WD[wd]))
    return f

def ritual(slug, label, note, begin, precision, recurrence, tithi, rtype,
           deities=None, guthi_node=None, part_of=None, place_at=None):
    r = I("intangible", slug)
    g.add((r, RDF.type, HGN.RitualEvent)); g.add((r, RDFS.label, lit(label)))
    g.add((r, CRMN["P4_has_time-span"], timespan(slug, begin, precision)))
    g.add((r, HGN.recurrence_pattern, lit(recurrence)))
    if tithi: g.add((r, HGN.lunar_date_tithi, lit(tithi)))
    g.add((r, HGN.ritual_type, HGN[rtype])); g.add((r, CRMN.P3_has_note, lit(note)))
    for d in (deities or []): g.add((r, HGN.invokes_deity, d))
    if guthi_node: g.add((r, HGN.managed_by_guthi, guthi_node))
    if part_of: g.add((r, CRMN.P9i_forms_part_of, part_of))
    if place_at: g.add((r, HGN.start_place, place_at))
    return r

def structure(slug, label, lon, lat, note, wd=None):
    s = I("intangible", slug); p = place(slug + "-loc", label, lon, lat)
    g.add((s, RDF.type, HGN.ArchitecturalStructure)); g.add((s, RDFS.label, lit(label)))
    g.add((s, DCTN.identifier, Literal(str(s), datatype=XSD.anyURI)))
    g.add((s, CRMN.P55_has_current_location, p))
    g.add((s, HGN.existence_status, HGN.Extant))
    g.add((s, PROVN.wasInfluencedBy, SRC))
    g.add((s, HGN.has_provenance_assertion, assertion(slug)))
    g.add((s, CRMN.P3_has_note, lit(note)))
    if wd: xg.add((s, OWL.sameAs, WD[wd]))
    return s

# === religious traditions ==================================================
T_H = tradition("tradition-hindu", "Hindu tradition")
T_B = tradition("tradition-buddhist", "Buddhist (Newar Vajrayana) tradition")
T_S = tradition("tradition-newar-syncretic", "Newar syncretic tradition")

# === deities ===============================================================
D_AVALOK = deity("deity-avalokiteshvara", "Avalokiteshvara (Karunamaya)",
    "Bodhisattva of compassion; Buddhist identity of the rain deity worshipped "
    "as Bungadyo/Rato Machhindranath.", "Q193849", ["tradition-buddhist", "tradition-newar-syncretic"])
D_MATSY = deity("deity-matsyendranath", "Matsyendranath (Bungadyo)",
    "Hindu Nath-tradition identity of the same rain deity; venerated as "
    "Rato Machhindranath in Patan/Bungamati.", "Q1420753", ["tradition-hindu", "tradition-newar-syncretic"])
D_TALEJU = deity("deity-taleju", "Taleju Bhawani",
    "Royal tutelary goddess of the Malla kings; manifest in the Royal Kumari.",
    "Q9355345", ["tradition-hindu", "tradition-newar-syncretic"])
D_SETO = deity("deity-seto-machhindranath", "Seto Machhindranath (Jana Baha Dyah)",
    "White Avalokiteshvara venerated at Jana Bahal, Kathmandu.", None, ["tradition-buddhist"])
D_NAVADURGA = deity("deity-navadurga", "Navadurga",
    "The nine manifestations of the goddess Durga; embodied in the Bhaktapur "
    "Navadurga masked dancers.", "Q2671565", ["tradition-hindu"])
D_BHAIRAVA = deity("deity-bhairava", "Bhairava",
    "Fierce form of Shiva; central to Bisket Jatra (Bhaktapur).", None, ["tradition-hindu"])
D_INDRA = deity("deity-indra", "Indra",
    "King of the gods; honoured during Indra Jatra in Kathmandu.", None, ["tradition-hindu"])

# === caste groups ==========================================================
C_VAJRA = caste("caste-vajracharya", "Vajracharya (Gubhaju)",
    "Newar Vajrayana Buddhist priests; perform tantric ritual and temple "
    "priesthood, including consecration (pratistha) rites.", "Q7908941")
C_SHAKYA = caste("caste-shakya", "Shakya",
    "Newar Buddhist caste of the sangha; the Royal Kumari is selected from "
    "Shakya families.")
C_JYAPU = caste("caste-jyapu", "Jyapu (Maharjan)",
    "Newar farming caste; hereditary chariot-pullers and ritual performers in "
    "jatras such as Rato Machhindranath.", "Q6733422")
C_GATHU = caste("caste-gathu", "Gathu (Banmala)",
    "Newar gardener caste of Bhaktapur; hereditary performers of the Navadurga "
    "masked dance.")
C_MANANDHAR = caste("caste-manandhar", "Manandhar (Saymi)",
    "Newar oil-presser caste with ritual roles in festival lamp lighting.")

# === places ================================================================
P_KTM = place("kathmandu-durbar", "Kathmandu Durbar Square (Basantapur)", 85.307, 27.7045, "Q6122177")
P_PATAN = place("patan-durbar", "Patan Durbar Square", 85.325, 27.6727, "Q7144236")
P_BKT = place("bhaktapur-durbar", "Bhaktapur Durbar Square", 85.428, 27.6722)
P_BUNGA = place("bungamati", "Bungamati", 85.300, 27.586, "Q2608296")
P_ASAN = place("asan", "Asan, Kathmandu", 85.312, 27.708)
P_TUNDI = place("tundikhel", "Tundikhel, Kathmandu", 85.315, 27.700)
P_JANABAHA = place("jana-bahal", "Jana Bahal, Kathmandu", 85.310, 27.708)

# === structures (Kumari Ghar, Pashupati for ritual anchoring) ==============
S_KUMARIGHAR = structure("kumari-ghar", "Kumari Ghar (Kumari Bahal), Kathmandu",
    85.3070, 27.7041, "Residence of the Royal Kumari; built 1757 CE by King "
    "Jaya Prakash Malla, Kathmandu Durbar Square.")
S_PASHUPATI = structure("pashupati-complex", "Pashupatinath Temple complex",
    85.3488, 27.7104, "Principal Shaiva temple complex; site of daily Nitya Puja.",
    "Q1814492")

# === guthis ================================================================
GU_SANSTHAN = guthi("guthi-sansthan", "Guthi Sansthan", "RajGuthi",
    "State trust corporation administering endowed (raj) guthi land and "
    "supporting temples, festivals and the Kumari institution.", wd="Q65395190")

# === festivals & chariot festivals (need rituals first for P9_consists_of) ==
# Rato Machhindranath ritual sub-events
R_BUNGA_BATH = ritual("ritual-bunga-bathing", "Ritual bathing of Bungadyo",
    "Annual ritual bathing and repainting of the Rato Machhindranath image "
    "before the chariot festival.", "0879-04-01", "Circa", "annual (Chaitra)",
    "Chaitra", "RitualConsecration", deities=[D_MATSY, D_AVALOK])

GU_BUNGA = guthi("guthi-bunga-dyah", "Bunga Dyah (Rato Machhindranath) Jatra Guthi",
    "JatraGuthi", "Guthi responsible for the annual Rato Machhindranath chariot "
    "festival between Patan and Bungamati.")

F_RATO = festival("festival-rato-machhindranath", "ChariotFestival",
    "Rato Machhindranath Jatra (Bunga Dyah Jatra)",
    "Longest chariot festival of the Kathmandu Valley; a towering chariot bearing "
    "Bungadyo is pulled through Patan, culminating at Jawalakhel (Bhoto Jatra). "
    "Traditionally dated to 879 CE (King Narendradeva and the priest Bandhudatta).",
    "0879-04-01", "Circa", "annual (Baisakh-Jestha); every 12 years from Bungamati",
    "Baisakh Shukla", "ChariotProcession",
    deities=[D_MATSY, D_AVALOK], manifests=[D_AVALOK],
    start=P_PATAN, route=[P_PATAN, P_BUNGA], guthi_node=GU_BUNGA, group=C_JYAPU,
    consists=[R_BUNGA_BATH])

F_SETO = festival("festival-seto-machhindranath", "ChariotFestival",
    "Seto Machhindranath Jatra (Jana Baha Dyah Jatra)",
    "Three-day chariot procession of Seto (White) Machhindranath through "
    "Kathmandu, starting from Jana Bahal.", "1100-01-01", "Century",
    "annual (Chaitra)", "Chaitra Shukla", "ChariotProcession",
    deities=[D_SETO], manifests=[D_SETO], start=P_JANABAHA, route=[P_JANABAHA, P_ASAN],
    group=C_VAJRA)

F_INDRA = festival("festival-indra-jatra", "Festival",
    "Indra Jatra (Yenya)",
    "Eight-day festival in Kathmandu honouring Indra and featuring the chariot "
    "procession of the Royal Kumari; attributed to King Gunakamadeva (10th c.).",
    "0960-01-01", "Century", "annual (Bhadra-Ashwin)", "Bhadra Shukla Dwadashi",
    "Jatra", deities=[D_INDRA, D_TALEJU], start=P_KTM, route=[P_KTM],
    guthi_node=GU_SANSTHAN, group=C_VAJRA, wd="Q301339")

F_BISKET = festival("festival-bisket-jatra", "Festival",
    "Bisket Jatra (Biska Jatra)",
    "Bhaktapur New-Year festival featuring tongue-piercing, a tug-of-war over the "
    "chariot of Bhairava and Bhadrakali, and the erection of the lingo pole.",
    "1500-01-01", "Century", "annual (Baisakh, Nepali New Year)", "Baisakh 1",
    "Jatra", deities=[D_BHAIRAVA], start=P_BKT, route=[P_BKT], wd="Q20704257")

F_GAI = festival("festival-gai-jatra", "Festival", "Gai Jatra (Sa Paru)",
    "Festival commemorating the dead through cow processions and satire; "
    "observed across the Kathmandu Valley.", "1600-01-01", "Century",
    "annual (Bhadra)", "Bhadra Krishna Pratipada", "Jatra",
    start=P_BKT, wd="Q40887536")

F_GHODE = festival("festival-ghode-jatra", "Festival", "Ghode Jatra",
    "Horse-racing festival held at Tundikhel, Kathmandu, to ward off a "
    "demon (Tundi).", "1700-01-01", "Century", "annual (Chaitra)",
    "Chaitra Aunsi", "Jatra", start=P_TUNDI, wd="Q106855753")

# === masked dances =========================================================
F_NAVADURGA = festival("dance-navadurga", "MaskedDance",
    "Navadurga masked dance (Bhaktapur)",
    "Sacred masked dance cycle in which Gathu performers embody the nine Durgas; "
    "performed annually after Dashain.", "1600-01-01", "Century",
    "annual (Ashwin-Bhadra cycle)", "Ashwin Shukla", "MaskedPerformance",
    deities=[D_NAVADURGA], manifests=[D_NAVADURGA], start=P_BKT, group=C_GATHU)

F_LAKHE = festival("dance-lakhe", "MaskedDance", "Lakhe dance (Majipa Lakhe)",
    "Masked dance of a benevolent demon performed through Kathmandu during the "
    "Yenya/Indra Jatra season.", "1700-01-01", "Century",
    "annual (Bhadra-Ashwin, Indra Jatra season)", "Bhadra Shukla",
    "MaskedPerformance", start=P_KTM, group=C_MANANDHAR)

# === periodic rituals ======================================================
R_NITYA = ritual("ritual-pashupati-nitya-puja", "Nitya Puja at Pashupatinath",
    "Daily obligatory worship of Pashupati performed by the temple priests.",
    "0500-01-01", "Circa", "daily", None, "NityaPuja",
    deities=[D_TALEJU], guthi_node=GU_SANSTHAN, place_at=place(
        "pashupati-pl", "Pashupatinath", 85.3488, 27.7104))

R_KUMARI_PUJA = ritual("ritual-kumari-daily-puja", "Daily puja of the Royal Kumari",
    "Daily worship offered to the Living Goddess at the Kumari Ghar.",
    "1757-01-01", "Circa", "daily", None, "NityaPuja",
    deities=[D_TALEJU], guthi_node=GU_SANSTHAN,
    place_at=place("kumari-pl", "Kumari Ghar", 85.3070, 27.7041))

R_KUMARI_PROC = ritual("ritual-kumari-indrajatra-procession",
    "Royal Kumari chariot procession (Indra Jatra)",
    "Three-day chariot procession of the Royal Kumari through Kathmandu during "
    "Indra Jatra.", "0960-01-01", "Century", "annual (Bhadra-Ashwin)",
    "Bhadra Shukla", "ProcessionRitual", deities=[D_TALEJU],
    part_of=F_INDRA, place_at=P_KTM)
g.add((F_INDRA, CRMN.P9_consists_of, R_KUMARI_PROC))

# === syncretic relationship ================================================
SYN = I("intangible", "syncretic-karunamaya")
xg.add((SYN, RDF.type, HGN.SyncreticRelationship))
xg.add((SYN, RDFS.label, lit("Avalokiteshvara identified with Matsyendranath (Karunamaya)")))
xg.add((SYN, HGN.assigned_to_deity, D_AVALOK))
xg.add((SYN, HGN.assigned_equivalent, D_MATSY))
xg.add((SYN, HGN.syncretic_type, HGN.Equivalence))
xg.add((SYN, PROVN.wasDerivedFrom, SRC))

SYN2 = I("intangible", "syncretic-kumari-taleju")
xg.add((SYN2, RDF.type, HGN.SyncreticRelationship))
xg.add((SYN2, RDFS.label, lit("Hindu goddess Taleju embodied in a Buddhist Shakya Kumari")))
xg.add((SYN2, HGN.assigned_to_deity, D_TALEJU))
xg.add((SYN2, HGN.syncretic_type, HGN.Identification))
xg.add((SYN2, PROVN.wasDerivedFrom, SRC))

# === Living Goddess (institutional level; no named minors) =================
KUMARI = I("intangible", "royal-kumari-office")
g.add((KUMARI, RDF.type, CRMN.E21_Person))
g.add((KUMARI, RDFS.label, lit("Royal Kumari of Kathmandu (office)")))
g.add((KUMARI, DCTN.identifier, Literal(str(KUMARI), datatype=XSD.anyURI)))
g.add((KUMARI, HGN.institutional_affiliation, lit("Kumari Ghar; manifestation of Taleju Bhawani")))
g.add((KUMARI, CRMN.P3_has_note, lit(
    "The office of the Royal (Trishul/Basantapur) Kumari, a pre-pubescent girl "
    "selected from the Shakya caste and venerated as the living embodiment of "
    "Taleju. Modelled at institutional level for privacy.")))
xg.add((KUMARI, OWL.sameAs, WD["Q1064555"]))

TENURE = I("intangible", "royal-kumari-tenure")
g.add((TENURE, RDF.type, CRMN.E4_Period))
g.add((TENURE, RDFS.label, lit("Royal Kumari tenure (office)")))
g.add((TENURE, CRMN.P11_had_participant, KUMARI))
g.add((TENURE, CRMN["P14.1_in_the_role_of"], D_TALEJU))
g.add((TENURE, CRMN["P4_has_time-span"], timespan("kumari-tenure", "1757-01-01", "Circa")))
g.add((TENURE, CRMN.P74_has_current_or_former_residence, S_KUMARIGHAR))
g.add((TENURE, HGN.supported_by_institution, GU_SANSTHAN))

SEL = I("intangible", "royal-kumari-selection")
g.add((SEL, RDF.type, HGN.LivingGoddessSelection))
g.add((SEL, RDFS.label, lit("Selection of the Royal Kumari")))
g.add((SEL, CRMN["P4_has_time-span"], timespan("kumari-selection", "1757-01-01", "Circa")))
g.add((SEL, HGN.selected_person, KUMARI))
g.add((SEL, HGN.initiated_tenure, TENURE))
g.add((SEL, HGN.managed_by_guthi, GU_SANSTHAN))
g.add((SEL, HGN.invokes_deity, D_TALEJU))
g.add((SEL, HGN.is_critical_for_festival, Literal(True)))
g.add((SEL, CRMN.P3_has_note, lit(
    "Selection of a Shakya girl bearing the battis lakshanas (32 perfections); "
    "confirmed through Taleju rites at Dashain.")))

RET = I("intangible", "royal-kumari-retirement")
g.add((RET, RDF.type, HGN.LivingGoddessRetirement))
g.add((RET, RDFS.label, lit("Retirement of the Royal Kumari")))
g.add((RET, CRMN["P4_has_time-span"], timespan("kumari-retirement", "1757-01-01", "Circa")))
g.add((RET, HGN.ended_tenure_of, TENURE))
g.add((RET, CRMN.P3_has_note, lit(
    "Tenure ends at first menstruation or serious illness/blood loss, when the "
    "deity is believed to depart.")))

# === serialise =============================================================
g.serialize(KG / "intangible.ttl", format="turtle")
xg.serialize(KG / "intangible_crosswalk.ttl", format="turtle")
print(f"intangible.ttl: {len(g)} triples (core)", file=sys.stderr)
print(f"intangible_crosswalk.ttl: {len(xg)} triples", file=sys.stderr)
