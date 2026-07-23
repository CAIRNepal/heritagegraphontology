#!/usr/bin/env python3
"""Multi-calendar experiment: resolve a tithi-scheduled ritual to Gregorian dates.

Addresses the reviewer observation that the multi-calendar temporal model
(claimed in the abstract, contribution 2, and the conclusion) was never
exercised: no CQ, listing, query, or test touched Bikram Sambat, Nepal
Sambat, epochDateGregorian, or yearOffsetFromGregorian.

The scenario is a released, shape-conformant dataset (separate from the
demonstrator, whose published triple counts stay untouched). It instantiates
the three CalendarSystem individuals the model was designed for and dates
one documented occurrence of Indra Jatra (the tithi-scheduled festival,
Bhadra Shukla Dwadashi) through three source records, each in its own
calendar, as archival records actually are:

  - a Gregorian record  (day precision): 2015-09-25
  - a Bikram Sambat record (B.S. 2072, civil/administrative convention)
  - a Nepal Sambat record  (N.S. 1135, Newar chronicle convention)

Semantics being tested. yearOffsetFromGregorian is defined as the offset to
convert a calendar year to a Common Era year (CE = year - offset; +57 for
B.S., -879 for N.S.). Because both calendars are lunisolar with non-January
new years (epochDateGregorian records the epoch, mid-April for B.S., late
October for N.S.), a source-calendar year straddles TWO Gregorian years, so
the sound resolution of a year-precision record is the interval
[year - offset, year - offset + 1], collapsing to a single year only when
the epoch anniversary falls on 01-01. The queries implement exactly that:

  Q1  Per-record resolution: each calendared time-span -> its Gregorian
      year interval, derived in SPARQL from the declared offset and epoch.
  Q2  Cross-calendar co-reference: the unique Gregorian year compatible
      with ALL three records of the occurrence (interval intersection via
      NOT EXISTS), returned with the ritual, its tithi, and the exact
      Gregorian date. B.S. 2072 -> {2015,2016}, N.S. 1135 -> {2014,2015},
      Gregorian -> {2015}; intersection {2015}.
  Q3  Calendar catalogue: each calendar's epoch, offset, and the religious
      tradition it is primary for (exercises isPrimaryForTradition).

The scenario is validated against the published SHACL shapes under the same
configuration as the pipeline gate (ont_graph mixed in, inference="none",
owl:NamedIndividual declarations stripped from the in-memory copy only).

Run:  evaluation/.venv/bin/python evaluation/multicalendar_resolution.py
"""
from pathlib import Path
from rdflib import Graph, RDF, OWL
from pyshacl import validate

ROOT = Path(__file__).resolve().parents[1]

PFX = """PREFIX hg:   <https://w3id.org/heritagegraph/>
PREFIX crm:  <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX ex:   <https://w3id.org/heritagegraph/demo/>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""

SCENARIO = """@prefix hg:   <https://w3id.org/heritagegraph/> .
@prefix crm:  <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix ex:   <https://w3id.org/heritagegraph/demo/> .

# --- Religious traditions the calendars serve ---------------------------
ex:HinduTradition a hg:ReligiousTradition ; rdfs:label "Hindu tradition" .
ex:NewarBuddhistTradition a hg:ReligiousTradition ;
    rdfs:label "Newar Buddhist tradition" .

# --- The three calendar systems -----------------------------------------
# Offset semantics (per schema): CE = calendar year - yearOffsetFromGregorian.
ex:BikramSambat a hg:CalendarSystem ; rdfs:label "Bikram Sambat" ;
    hg:epochDateGregorian "-0056-04-14" ;      # 57 BCE, mid-April new year
    hg:yearOffsetFromGregorian 57 ;
    hg:isPrimaryForTradition ex:HinduTradition ;
    crm:P3_has_note "Lunisolar civil calendar of Nepal; new year in mid-April (Baisakh 1)." .
ex:NepalSambat a hg:CalendarSystem ; rdfs:label "Nepal Sambat" ;
    hg:epochDateGregorian "0879-10-20" ;       # epoch 20 Oct 879 CE
    hg:yearOffsetFromGregorian -879 ;
    hg:isPrimaryForTradition ex:NewarBuddhistTradition ;
    crm:P3_has_note "Lunisolar Newar calendar; new year at Mha Puja (Oct/Nov)." .
ex:GregorianCalendar a hg:CalendarSystem ; rdfs:label "Gregorian calendar" ;
    hg:epochDateGregorian "0001-01-01" ;
    hg:yearOffsetFromGregorian 0 .

# --- The tithi-scheduled ritual and one documented occurrence -----------
ex:IndraJatra a hg:Festival ; rdfs:label "Indra Jatra" ;
    hg:lunarDateTithi "Bhadra Shukla Dwadashi" ;
    hg:recurrencePattern "annual (lunar-tithi)" .

ex:IndraJatra_2015 a hg:RitualEvent ;
    rdfs:label "Indra Jatra, 2015 occurrence" ;
    crm:P9i_forms_part_of ex:IndraJatra ;
    crm:P4_has_time-span ex:TS_IJ_Gregorian .

# Three source records of the same occurrence, each in its own calendar.
ex:TS_IJ_Gregorian a crm:E52_Time-Span ;
    rdfs:label "Indra Jatra start, Gregorian record" ;
    crm:P82a_begin_of_the_begin "2015-09-25"^^xsd:date ;
    hg:calendarSystem ex:GregorianCalendar ;
    hg:datePrecision "Exact" .
ex:TS_IJ_BikramSambat a crm:E52_Time-Span ;
    rdfs:label "Indra Jatra start, Bikram Sambat record (B.S. 2072)" ;
    crm:P82a_begin_of_the_begin "2072-01-01"^^xsd:date ;
    hg:calendarSystem ex:BikramSambat ;
    hg:datePrecision "Year" ;
    crm:P3_has_note "Year-precision record; B.S. 2072 spans 2015-04-14 to 2016-04-12 CE." .
ex:TS_IJ_NepalSambat a crm:E52_Time-Span ;
    rdfs:label "Indra Jatra start, Nepal Sambat record (N.S. 1135)" ;
    crm:P82a_begin_of_the_begin "1135-01-01"^^xsd:date ;
    hg:calendarSystem ex:NepalSambat ;
    hg:datePrecision "Year" ;
    crm:P3_has_note "Year-precision record; N.S. 1135 spans Oct 2014 to Nov 2015 CE." .

# The two calendar-specific records document the dated occurrence.
ex:IndraJatra_2015 crm:P3_has_note
    "Also recorded as B.S. 2072 (TS_IJ_BikramSambat) and N.S. 1135 (TS_IJ_NepalSambat)." .
"""

# Interval semantics shared by Q1/Q2: a year-Y record in a calendar with
# offset O and a non-01-01 epoch anniversary resolves to [Y-O, Y-O+1].
QUERIES = {
    "Q1 per-record resolution: source year -> Gregorian year interval":
        PFX + """SELECT ?record ?calendar ?srcYear ?ceLow ?ceHigh WHERE {
          ?record a crm:E52_Time-Span ;
                  crm:P82a_begin_of_the_begin ?d ;
                  hg:calendarSystem ?cal .
          ?cal rdfs:label ?calendar ;
               hg:yearOffsetFromGregorian ?off ;
               hg:epochDateGregorian ?epoch .
          BIND(YEAR(?d) AS ?srcYear)
          BIND(?srcYear - ?off AS ?ceLow)
          BIND(IF(SUBSTR(?epoch, 6) = "01-01", ?ceLow, ?ceLow + 1) AS ?ceHigh)
        } ORDER BY ?ceLow""",
    "Q2 tithi ritual resolved: unique Gregorian year consistent with all records":
        PFX + """SELECT ?ritual ?tithi ?ceYear ?gregorianDate WHERE {
          ?occ crm:P9i_forms_part_of ?series ;
               crm:P4_has_time-span ?tsg .
          ?series rdfs:label ?ritual ; hg:lunarDateTithi ?tithi .
          ?tsg crm:P82a_begin_of_the_begin ?gregorianDate ;
               hg:calendarSystem [ hg:yearOffsetFromGregorian 0 ] .
          BIND(YEAR(?gregorianDate) AS ?ceYear)
          # Every calendared record of this occurrence must admit ?ceYear.
          FILTER NOT EXISTS {
            ?other a crm:E52_Time-Span ;
                   crm:P82a_begin_of_the_begin ?od ;
                   hg:calendarSystem ?ocal .
            ?ocal hg:yearOffsetFromGregorian ?ooff ;
                  hg:epochDateGregorian ?oepoch .
            BIND(YEAR(?od) - ?ooff AS ?lo)
            BIND(IF(SUBSTR(?oepoch, 6) = "01-01", ?lo, ?lo + 1) AS ?hi)
            FILTER(?ceYear < ?lo || ?ceYear > ?hi)
          }
        }""",
    "Q3 calendar catalogue: epoch, offset, primary tradition":
        PFX + """SELECT ?calendar ?epoch ?offset ?tradition WHERE {
          ?cal a hg:CalendarSystem ; rdfs:label ?calendar ;
               hg:epochDateGregorian ?epoch ;
               hg:yearOffsetFromGregorian ?offset .
          OPTIONAL { ?cal hg:isPrimaryForTradition [ rdfs:label ?tradition ] }
        } ORDER BY ?offset""",
}

g = Graph()
g.parse(data=SCENARIO, format="turtle")
print(f"Scenario: {len(g)} triples\n")
for name, q in QUERIES.items():
    rows = list(g.query(q))
    print(f"[{len(rows)} row(s)] {name}")
    for r in rows:
        print("   -> " + " | ".join(
            str(x).replace("https://w3id.org/heritagegraph/demo/", "")
            for x in r))
print()

# SHACL conformance under the pipeline-gate configuration.
shapes = Graph()
shapes.parse(ROOT / "ontology/HeritageGraph.shacl.ttl", format="turtle")
ont = Graph()
ont.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
for s in list(ont.subjects(RDF.type, OWL.NamedIndividual)):
    ont.remove((s, RDF.type, OWL.NamedIndividual))
conforms, _, report = validate(g, shacl_graph=shapes, ont_graph=ont,
                               inference="none", abort_on_first=False)
print(f"SHACL conformance of the scenario: conforms={conforms}")
if not conforms:
    print(report[:2000])
