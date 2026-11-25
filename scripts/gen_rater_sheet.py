#!/usr/bin/env python3
"""Build the sheet an independent rater fills in to judge HeritageGraph's mappings.

    python3 scripts/gen_rater_sheet.py

Writes evaluation/rater/mapping_rater_sheet.csv: one row per mapping in the
published SSSOM set (ontology/mappings/HeritageGraph.sssom.tsv), with what a
rater needs to judge it without opening the ontology: the HeritageGraph term's
label and definition, the mapping predicate, and the external term's official
label and definition (from the vocabulary snapshots in ontology/imports/ where
the term is there). The rater fills in `verdict` (accept / reject / revise),
`suggested_predicate` (for revise), `rater`, `date` and `note`.

`second_rater` marks a fixed 30% sample of the core mappings for a second,
independent rater (chosen by a hash of the mapping, so the sample does not
depend on the order of rows or on who runs the script). Agreement between the
two is computed by evaluation/rater_agreement.py (Cohen's kappa).

The completed first-rater sheet is copied to evaluation/mapping_rater_verdicts.csv
(the columns gen_sssom.py and mapping_audit.py read), so accepted mappings get
a reviewer in the SSSOM set and rejected ones leave it.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from rdflib import Graph, URIRef, RDFS
from rdflib.namespace import SKOS

ROOT = Path(__file__).resolve().parents[1]
SSSOM = ROOT / "ontology" / "mappings" / "HeritageGraph.sssom.tsv"
CORE = ROOT / "ontology" / "HeritageGraph.ttl"
LUX = ROOT / "heritagegraph-lux-migration" / "alignment" / "heritagegraph-lux-alignment.ttl"
IMPORTS = ROOT / "ontology" / "imports"
OUT = ROOT / "evaluation" / "rater" / "mapping_rater_sheet.csv"
SAMPLE = 0.30
COLUMNS = ["subject_id", "subject_label", "subject_definition", "predicate_id", "object_id",
           "object_label", "object_definition", "scope", "second_rater",
           "verdict", "suggested_predicate", "rater", "date", "note"]


def curie_map() -> dict:
    out = {}
    for line in SSSOM.read_text(encoding="utf-8").splitlines():
        if line.startswith("#   ") and ": " in line:
            p, ns = line[4:].split(": ", 1)
            out[p.strip()] = ns.strip()
    return out


def expand(curie: str, cmap: dict) -> URIRef:
    p, _, local = curie.partition(":")
    return URIRef(cmap[p] + local) if p in cmap else URIRef(curie)


def text(g: Graph, s: URIRef, preds) -> str:
    for p in preds:
        vals = [o for o in g.objects(s, p) if getattr(o, "language", None) in ("en", None)]
        if vals:
            return " ".join(str(vals[0]).split())
    return ""


def main() -> int:
    cmap = curie_map()
    hg = Graph().parse(CORE, format="turtle")
    hg += Graph().parse(LUX, format="turtle")
    ext = Graph()
    meta = json.loads((IMPORTS / "sources.json").read_text(encoding="utf-8"))
    for src in meta["sources"]:
        ext.parse(IMPORTS / src["file"], format=src["format"])
    defs = (SKOS.definition, RDFS.comment)
    rows = []
    with open(SSSOM, encoding="utf-8") as f:
        reader = csv.DictReader((l for l in f if not l.startswith("#")), delimiter="\t")
        for r in reader:
            s, o = expand(r["subject_id"], cmap), expand(r["object_id"], cmap)
            core = "core" in r["comment"].replace("LUX module", "")
            key = f'{r["subject_id"]} {r["predicate_id"]} {r["object_id"]}'
            second = core and int(hashlib.sha256(key.encode()).hexdigest(), 16) % 1000 < SAMPLE * 1000
            rows.append({
                "subject_id": r["subject_id"], "subject_label": r["subject_label"],
                "subject_definition": text(hg, s, defs),
                "predicate_id": r["predicate_id"], "object_id": r["object_id"],
                "object_label": text(ext, o, (RDFS.label, SKOS.prefLabel)) or text(hg, o, (RDFS.label,)),
                "object_definition": text(ext, o, defs) or "(not in the local snapshots: look it up)",
                "scope": "core" if core else "LUX module",
                "second_rater": "yes" if second else "",
                **{c: "" for c in ("verdict", "suggested_predicate", "rater", "date", "note")},
            })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    n_core = sum(r["scope"] == "core" for r in rows)
    n_second = sum(r["second_rater"] == "yes" for r in rows)
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(rows)} mappings ({n_core} core), "
          f"{n_second} marked for the second rater")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
