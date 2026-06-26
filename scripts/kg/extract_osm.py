"""Extract Nepal cultural-heritage features from OpenStreetMap (ODbL) via Overpass.

Output -> data/raw/osm.json (elements with tags + representative coordinate).
"""
import json, sys
from config import OVERPASS, RAW
from fetch import post_form

# Heritage-relevant feature selection across all of Nepal.
OVERPASS_QL = """
[out:json][timeout:180];
area["ISO3166-1"="NP"][admin_level=2]->.np;
(
  nwr["historic"](area.np);
  nwr["amenity"="place_of_worship"]["religion"~"hindu|buddhist"](area.np);
  nwr["building"="temple"](area.np);
  nwr["building"="stupa"](area.np);
  nwr["building"="monastery"](area.np);
  nwr["man_made"="water_well"](area.np);
  nwr["amenity"="fountain"]["historic"](area.np);
  nwr["man_made"="water_tap"]["heritage"](area.np);
);
out tags center;
"""


def main():
    print("Querying Overpass (Nepal)...", file=sys.stderr)
    raw = post_form(OVERPASS, {"data": OVERPASS_QL}, "application/json", timeout=300)
    if raw[:1] != b"{":
        print("ERROR response:", raw[:300], file=sys.stderr); sys.exit(1)
    res = json.loads(raw)
    out = []
    for el in res.get("elements", []):
        tags = el.get("tags", {})
        if not tags:
            continue
        if el["type"] == "node":
            lat, lon = el.get("lat"), el.get("lon")
        else:
            c = el.get("center", {})
            lat, lon = c.get("lat"), c.get("lon")
        out.append({
            "osm_type": el["type"],
            "osm_id": el["id"],
            "lat": lat, "lon": lon,
            "tags": tags,
        })
    path = RAW / "osm.json"
    json.dump(out, open(path, "w"), ensure_ascii=False)
    print(f"Wrote {len(out)} OSM features -> {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
