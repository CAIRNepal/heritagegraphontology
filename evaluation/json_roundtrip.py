#!/usr/bin/env python3
"""JSON data -> RDF -> ontology: the schema-first path, end to end.

examples/kathmandu-multilingual.json (a Container with language maps, an
array of notes, an enumeration value, a reference to a union-class value
and plain 1.0.x-style strings) is
converted with scripts/json_to_rdf.py, and the RDF must
  1. carry each language-map entry as a language-tagged literal and each
     enumeration value as the individual's IRI (checked triple by triple);
  2. conform to the SHACL shapes (pyshacl, ontology graph mixed in);
  3. be HermiT-consistent with the OWL (ontology and data in one graph).
Two invalid files must be refused before conversion: a language map with a
malformed tag, and a language map on a code field (source_url).
Exit status is non-zero on any failure.
"""
from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from rdflib import Graph, Literal, OWL, RDF, URIRef
from pyshacl import validate
from linkml_runtime import SchemaView

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from json_to_rdf import CONTAINER, convert  # noqa: E402

ROBOT_JAR = os.environ.get("ROBOT_JAR", "/tmp/hgtools/robot.jar")
JAVA = str(Path(os.environ.get("JAVA_HOME", "/opt/homebrew/opt/openjdk")) / "bin" / "java")
HG = "https://cair-nepal.org/heritagegraph/"
EX = HG + "example/mljson/"
RDFS_LABEL = URIRef("http://www.w3.org/2000/01/rdf-schema#label")
P3 = URIRef("http://www.cidoc-crm.org/cidoc-crm/P3_has_note")

ok = True


def check(name: str, cond: bool) -> None:
    global ok
    ok &= cond
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")


sv = SchemaView(str(CONTAINER))
data = json.loads((ROOT / "examples" / "kathmandu-multilingual.json").read_text(encoding="utf-8"))
g = convert(data, sv)
print(f"converted examples/kathmandu-multilingual.json: {len(g)} triples")

print("1. triples")
deity, guthi, source = URIRef(EX + "Deity"), URIRef(EX + "Guthi"), URIRef(EX + "Source")
check("label map -> \"Taleju Bhawani\"@en and \"तलेजु भवानी\"@ne",
      {(deity, RDFS_LABEL, Literal("Taleju Bhawani", lang="en")),
       (deity, RDFS_LABEL, Literal("तलेजु भवानी", lang="ne"))} <= set(g))
check("note map with an array -> two @en notes and one @ne note",
      sorted((str(o), o.language) for o in g.objects(deity, P3)) ==
      sorted([("Test note one.", "en"), ("Test note two.", "en"), ("परीक्षण टिप्पणी", "ne")]))
check("plain-string note stays an untagged literal",
      (source, P3, Literal("A plain-string note, as in 1.0.x data.")) in g)
check("assertion_content map -> prov:value @en and @ne (one per language)",
      sorted(o.language for o in g.objects(URIRef(EX + "Claim"),
                                            URIRef("http://www.w3.org/ns/prov#value"))) == ["en", "ne"])
check("reference to a union-class value (asserts_about) -> IRI",
      (URIRef(EX + "Claim"), URIRef(HG + "assertsAbout"), deity) in g)
check("enum value -> individual IRI (GuthiType#TempleGuthi)",
      (guthi, URIRef(HG + "guthiType"), URIRef(HG + "GuthiType#TempleGuthi")) in g)
check("no placeholder or Container triple left",
      not any("urn:hg-langmap" in str(o) for o in g.objects())
      and not any(str(t).endswith("Container") for t in g.objects(None, RDF.type)))

print("2. SHACL")
shapes = Graph(); shapes.parse(ROOT / "ontology/HeritageGraph.shacl.ttl", format="turtle")
ont = Graph(); ont.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
for s in list(ont.subjects(RDF.type, OWL.NamedIndividual)):
    ont.remove((s, RDF.type, OWL.NamedIndividual))
conforms, _, txt = validate(g, shacl_graph=shapes, ont_graph=ont, inference="none")
check("converted RDF conforms to the shapes", conforms)
if not conforms:
    print(txt[:1500])

print("3. OWL (HermiT)")
merged = Graph(); merged.parse(ROOT / "ontology/HeritageGraph.ttl", format="turtle")
merged += g
merged.remove((None, OWL.imports, None))
with tempfile.TemporaryDirectory() as td:
    src = Path(td) / "m.ttl"
    merged.serialize(src, format="turtle")
    proc = subprocess.run([JAVA, "-jar", ROBOT_JAR, "reason", "--reasoner", "hermit",
                           "--input", str(src), "--output", str(Path(td) / "r.ttl")],
                          capture_output=True, text=True)
check("ontology + converted RDF is consistent", proc.returncode == 0)
if proc.returncode != 0:
    print((proc.stdout + proc.stderr)[-800:])

print("4. refused before conversion")
bad_tag = copy.deepcopy(data)
bad_tag["deities"][0]["name"] = {"english!": "Taleju"}
bad_code = copy.deepcopy(data)
bad_code["data_sources"][0]["source_url"] = {"en": "https://example.org"}
for name, d in (("language map with a malformed tag", bad_tag),
                ("language map on a code field (source_url)", bad_code)):
    try:
        convert(d, sv)
        refused = False
    except ValueError as e:
        refused = "JSON Schema validation failed" in str(e)
    check(name, refused)

print("PASS: JSON data with language maps reaches RDF that conforms and is consistent."
      if ok else "FAIL")
sys.exit(0 if ok else 1)
