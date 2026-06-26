"""UNESCO World Heritage — Nepal *cultural* components (authoritative public facts).

Nepal has two cultural World Heritage properties: the Kathmandu Valley
(ref. 121bis, inscribed 1979) comprising seven monument zones, and Lumbini
(ref. 666, inscribed 1997). Natural properties (Sagarmatha, Chitwan) are out
of scope for this cultural-heritage KG.

Facts (name, WHC reference, inscription year, coordinates, component class)
are sourced from the UNESCO World Heritage Centre (https://whc.unesco.org/).
The crosswalk to Wikidata QIDs is recorded for linkage/verification.
"""
import json, sys
from config import RAW

UNESCO = [
    # Kathmandu Valley (ref 121bis, 1979) — 7 monument zones
    {"id": "hanuman-dhoka", "label": "Hanuman Dhoka Durbar Square",
     "kind": "structure", "lat": 27.7045, "lon": 85.3070,
     "property": "Kathmandu Valley", "ref": "121bis-001", "inscribed": 1979,
     "wikidata": "Q1566083",
     "note": "Royal palace square, Kathmandu; UNESCO World Heritage monument zone."},
    {"id": "patan-durbar", "label": "Patan Durbar Square",
     "kind": "structure", "lat": 27.6727, "lon": 85.3250,
     "property": "Kathmandu Valley", "ref": "121bis-002", "inscribed": 1979,
     "wikidata": "Q2363972",
     "note": "Royal palace square, Lalitpur; UNESCO World Heritage monument zone."},
    {"id": "bhaktapur-durbar", "label": "Bhaktapur Durbar Square",
     "kind": "structure", "lat": 27.6722, "lon": 85.4280,
     "property": "Kathmandu Valley", "ref": "121bis-003", "inscribed": 1979,
     "wikidata": "Q2891639",
     "note": "Royal palace square, Bhaktapur; UNESCO World Heritage monument zone."},
    {"id": "swayambhu", "label": "Swayambhunath",
     "kind": "stupa", "lat": 27.7149, "lon": 85.2903,
     "property": "Kathmandu Valley", "ref": "121bis-004", "inscribed": 1979,
     "wikidata": "Q714056",
     "note": "Ancient Buddhist stupa complex; UNESCO World Heritage monument zone."},
    {"id": "bauddhanath", "label": "Boudhanath",
     "kind": "stupa", "lat": 27.7215, "lon": 85.3620,
     "property": "Kathmandu Valley", "ref": "121bis-005", "inscribed": 1979,
     "wikidata": "Q839176",
     "note": "One of the largest Buddhist stupas; UNESCO World Heritage monument zone."},
    {"id": "pashupati", "label": "Pashupatinath Temple",
     "kind": "structure", "lat": 27.7104, "lon": 85.3488,
     "property": "Kathmandu Valley", "ref": "121bis-006", "inscribed": 1979,
     "wikidata": "Q1814492",
     "note": "Sacred Hindu temple complex on the Bagmati; UNESCO World Heritage monument zone."},
    {"id": "changu-narayan", "label": "Changu Narayan",
     "kind": "structure", "lat": 27.7163, "lon": 85.4297,
     "property": "Kathmandu Valley", "ref": "121bis-007", "inscribed": 1979,
     "wikidata": "Q1066544",
     "note": "Oldest Hindu temple in the valley; UNESCO World Heritage monument zone."},
    # Lumbini (ref 666, 1997)
    {"id": "lumbini", "label": "Lumbini, the Birthplace of the Lord Buddha",
     "kind": "structure", "lat": 27.4833, "lon": 83.2767,
     "property": "Lumbini", "ref": "666", "inscribed": 1997,
     "wikidata": "Q5379",
     "note": "Sacred birthplace of Siddhartha Gautama; UNESCO World Heritage Site."},
]


def main():
    path = RAW / "unesco.json"
    json.dump(UNESCO, open(path, "w"), ensure_ascii=False, indent=1)
    print(f"Wrote {len(UNESCO)} UNESCO cultural WHS components -> {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
