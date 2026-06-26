#!/usr/bin/env python3
"""Idempotent interoperability post-processing for the HeritageGraph OWL artefact.

Two transforms are applied to the in-memory rdflib graph:

1. ``fix_object_property_types`` — re-types properties whose effective range is
   entirely class-valued (including LinkML ``any_of`` class unions) as
   ``owl:ObjectProperty``. LinkML's ``gen-owl`` mis-emits such slots as
   ``owl:DatatypeProperty`` (e.g. ``performed_by_group``).

2. ``fix_skos_mappings`` — enforces SKOS hygiene:
     (A) where a class asserts both ``skos:exactMatch X`` and
         ``rdfs:subClassOf X`` for the same target, the redundant/contradictory
         ``exactMatch`` is dropped (the structural ``subClassOf`` is kept);
     (B) where a class still carries more than one ``skos:exactMatch``, the single
         best 1:1 target is kept (authority priority: Getty AAT > Wikidata >
         schema.org > DBpedia > other) and the rest are demoted to
         ``skos:closeMatch``.

Both functions are idempotent and safe to run repeatedly.
"""

from __future__ import annotations

from rdflib import Graph, RDF, RDFS, OWL, URIRef
from rdflib.namespace import SKOS

HG = "https://cair-nepal.org/heritagegraph/"

# Authority priority for picking the single 1:1 exactMatch target (lower = better).
_EXACT_PRIORITY = [
    "http://vocab.getty.edu/aat/",      # Getty AAT — cultural-heritage authority hub
    "http://www.wikidata.org/entity/",  # Wikidata — stable, broad coverage
    "http://schema.org/",               # schema.org
    "http://dbpedia.org/",              # DBpedia
]


def _priority(uri: str) -> int:
    for i, prefix in enumerate(_EXACT_PRIORITY):
        if uri.startswith(prefix):
            return i
    return len(_EXACT_PRIORITY)


def _class_names(schema: dict) -> set[str]:
    return set((schema.get("classes") or {}).keys())


def fix_object_property_types(g: Graph, schema: dict) -> int:
    """Re-type class-ranged slots mis-emitted as datatype properties. Returns count."""
    classes = _class_names(schema)
    changed = 0
    for name, spec in (schema.get("slots") or {}).items():
        if not isinstance(spec, dict):
            continue
        ranges: list[str] = []
        if "any_of" in spec and isinstance(spec["any_of"], list):
            for branch in spec["any_of"]:
                if isinstance(branch, dict) and "range" in branch:
                    ranges.append(branch["range"])
        elif "range" in spec:
            ranges.append(spec["range"])
        if not ranges or not all(r in classes for r in ranges):
            continue
        prop = URIRef(HG + name)
        if (prop, RDF.type, OWL.DatatypeProperty) in g:
            g.remove((prop, RDF.type, OWL.DatatypeProperty))
            g.add((prop, RDF.type, OWL.ObjectProperty))
            changed += 1
    return changed


def fix_skos_mappings(g: Graph) -> tuple[int, int]:
    """Apply SKOS exactMatch hygiene. Returns (dropped_subclass_dupes, demoted)."""
    # Rule A: drop exactMatch where the same subject also rdfs:subClassOf the target.
    dropped = 0
    for s, o in list(g.subject_objects(SKOS.exactMatch)):
        if (s, RDFS.subClassOf, o) in g or (s, OWL.equivalentClass, o) in g:
            g.remove((s, SKOS.exactMatch, o))
            dropped += 1

    # Rule B: collapse remaining multi-exactMatch to a single 1:1 target.
    demoted = 0
    by_subject: dict[URIRef, list[URIRef]] = {}
    for s, o in g.subject_objects(SKOS.exactMatch):
        by_subject.setdefault(s, []).append(o)
    for s, targets in by_subject.items():
        uniq = sorted(set(targets), key=lambda u: (_priority(str(u)), str(u)))
        if len(uniq) <= 1:
            continue
        keep = uniq[0]
        for o in uniq[1:]:
            g.remove((s, SKOS.exactMatch, o))
            g.add((s, SKOS.closeMatch, o))
            demoted += 1
    return dropped, demoted


__all__ = ["fix_object_property_types", "fix_skos_mappings", "HG"]
