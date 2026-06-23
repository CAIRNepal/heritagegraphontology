#!/usr/bin/env python3
"""Regenerate HeritageGraph release artefacts from LinkML with full post-processing."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml
from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.collection import Collection
from rdflib.namespace import DCTERMS, PROV, SKOS, VOID

from interop_fixes import fix_object_property_types, fix_skos_mappings

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "ontology" / "HeritageGraph.yaml"
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
SHACL = ROOT / "ontology" / "HeritageGraph.shacl.ttl"
REGEN = ROOT / "ontology" / "HeritageGraph.regen.ttl"
ALIGNMENT = ROOT / "ontology" / "HeritageGraph-alignment.ttl"
EDM_PROFILE = ROOT / "ontology" / "HeritageGraph-edm.ttl"
METADATA = ROOT / "ontology" / "heritagegraph-metadata.ttl"
ABOX = ROOT / "examples" / "abox-conflicting-assertions.ttl"
DOCS_TTL = ROOT / "docs" / "ontology.ttl"
REVIEW_OWL = ROOT / "ontology" / "review.owl"
CHANGELOG = ROOT / "CHANGELOG.md"

HG = Namespace("https://w3id.org/heritagegraph/")
ONTOLOGY_IRI = URIRef("https://w3id.org/heritagegraph/ontology")
VERSION_IRI = URIRef("https://w3id.org/heritagegraph/ontology/1.0.0")
ALIGNMENT_IRI = URIRef("https://w3id.org/heritagegraph/alignment")
EDM_IRI = URIRef("https://w3id.org/heritagegraph/edm-profile")
DATASET_IRI = URIRef("https://w3id.org/heritagegraph/dataset")

CRM = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
CRMINF = Namespace("http://www.cidoc-crm.org/extensions/crminf/")
EDM = Namespace("http://www.europeana.eu/schemas/edm/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
LOCALCONTEXTS = Namespace("https://voc.localcontexts.org/")

IMPORTS = [
    URIRef("http://www.cidoc-crm.org/cidoc-crm/"),
    URIRef("http://www.cidoc-crm.org/extensions/crminf/"),
    URIRef("http://www.w3.org/ns/prov#"),
    URIRef("http://www.w3.org/2006/time#"),
    URIRef("http://www.opengis.net/ont/geosparql#"),
    URIRef("http://www.europeana.eu/schemas/edm/"),
]

# EDM class projection for Europeana aggregation pipelines.
EDM_CLASS_MAP = {
    HG.HumanMadeObject: EDM.PhysicalThing,
    HG.ArchitecturalStructure: EDM.PhysicalThing,
    HG.IconographicObject: EDM.PhysicalThing,
    HG.ArchitecturalElement: EDM.PhysicalThing,
    HG.Production: EDM.Event,
    HG.RitualEvent: EDM.Event,
    HG.Festival: EDM.Event,
    HG.DocumentationActivity: EDM.Event,
    HG.TransferOfCustody: EDM.Event,
    HG.ConditionAssessment: EDM.Event,
    HG.HistoricalEvent: EDM.Event,
    HG.DestructionEvent: EDM.Event,
    HG.Actor: EDM.Agent,
    HG.Person: EDM.Agent,
    HG.Guthi: EDM.Agent,
    HG.DataCustodian: EDM.Agent,
    HG.DataSource: EDM.WebResource,
    HG.InformationObject: EDM.WebResource,
    HG.OralHistoryRecording: EDM.WebResource,
    HG.FieldSurveyDataset: EDM.WebResource,
    HG.ArchivalRecord: EDM.WebResource,
    HG.Place: EDM.Place,
    HG.TimeSpan: EDM.TimeSpan,
    HG.Deity: EDM.Concept,
    HG.ReligiousTradition: EDM.Concept,
}

# Wikidata high-confidence class bridges (alignment module only).
WIKIDATA_EQUIV = {
    HG.Temple: URIRef("http://www.wikidata.org/entity/Q44539"),
    HG.Murti: URIRef("http://www.wikidata.org/entity/Q2594295"),
    HG.HumanMadeObject: URIRef("http://www.wikidata.org/entity/Q838948"),
}

EXTERNAL_CLASS_URI_PREFIXES = (
    "crm:",
    "crminf:",
    "crmsci:",
    "crmdig:",
    "prov:",
    "time:",
    "rico:",
)


def load_schema() -> dict:
    with SCHEMA.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def expand_curie(curie: str, prefixes: dict[str, str]) -> URIRef | None:
    if not curie or ":" not in curie:
        return None
    prefix, local = curie.split(":", 1)
    if prefix not in prefixes:
        return None
    base = prefixes[prefix]
    if prefix == "crm" and local.startswith("E") and "_" in local:
        return URIRef(base + local)
    if prefix == "crminf" and local[0] in "IEJ":
        return URIRef(base + local)
    return URIRef(base + local)


def hg_class_uri(name: str) -> URIRef:
    return URIRef(f"https://w3id.org/heritagegraph/{name}")


def generate_ttl() -> None:
    cmd = [
        "linkml",
        "generate",
        "owl",
        str(SCHEMA),
        "-f",
        "ttl",
        "--default-permissible-value-type",
        "http://www.w3.org/2002/07/owl#NamedIndividual",
        "--no-mergeimports",
    ]
    result = subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
    lines = result.stdout.splitlines(keepends=True)
    start = next(i for i, line in enumerate(lines) if line.startswith("@prefix "))
    REGEN.write_text("".join(lines[start:]), encoding="utf-8")


def apply_exact_mapping_subclass_axioms(g: Graph, schema: dict) -> int:
    prefixes = schema.get("prefixes", {})
    classes = schema.get("classes", {})
    count = 0
    for name, spec in classes.items():
        if not isinstance(spec, dict):
            continue
        hg = hg_class_uri(name)
        if (hg, RDF.type, OWL.Class) not in g:
            continue
        for curie in spec.get("exact_mappings", []) or []:
            if not any(curie.startswith(p) for p in EXTERNAL_CLASS_URI_PREFIXES):
                continue
            target = expand_curie(curie, prefixes)
            if target:
                g.add((hg, RDFS.subClassOf, target))
                count += 1
    return count


def apply_class_uri_subclass_axioms(g: Graph, schema: dict) -> int:
    prefixes = schema.get("prefixes", {})
    classes = schema.get("classes", {})
    count = 0
    for name, spec in classes.items():
        if not isinstance(spec, dict):
            continue
        curie = spec.get("class_uri")
        if not curie or not any(curie.startswith(p) for p in EXTERNAL_CLASS_URI_PREFIXES):
            continue
        target = expand_curie(curie, prefixes)
        hg = hg_class_uri(name)
        if target and (hg, RDF.type, OWL.Class) in g:
            g.add((hg, RDFS.subClassOf, target))
            count += 1
    return count


def apply_union_axioms(g: Graph, schema: dict) -> int:
    classes = schema.get("classes", {})
    count = 0
    for name, spec in classes.items():
        if not isinstance(spec, dict):
            continue
        members = spec.get("union_of")
        if not members:
            continue
        hg = hg_class_uri(name)
        if (hg, RDF.type, OWL.Class) not in g:
            continue
        member_nodes = [hg_class_uri(m) for m in members]
        for o in list(g.objects(hg, OWL.unionOf)):
            g.remove((hg, OWL.unionOf, o))
        list_head = BNode()
        Collection(g, list_head, member_nodes)
        g.add((hg, OWL.unionOf, list_head))
        count += 1
    return count


def apply_disjoint_axioms(g: Graph, schema: dict) -> int:
    """Emit owl:disjointWith from LinkML `disjoint_with` (the LinkML OWL generator
    does not emit these). Only emitted between two declared owl:Class nodes; added
    symmetrically and de-duplicated so each unordered pair appears once."""
    classes = schema.get("classes", {})
    seen: set[frozenset[URIRef]] = set()
    count = 0
    for name, spec in classes.items():
        if not isinstance(spec, dict):
            continue
        targets = spec.get("disjoint_with")
        if not targets:
            continue
        hg = hg_class_uri(name)
        if (hg, RDF.type, OWL.Class) not in g:
            continue
        for target_name in targets:
            other = hg_class_uri(target_name)
            if (other, RDF.type, OWL.Class) not in g:
                continue
            pair = frozenset((hg, other))
            if hg == other or pair in seen:
                continue
            seen.add(pair)
            g.add((hg, OWL.disjointWith, other))
            count += 1
    return count


def apply_enum_concept_schemes(g: Graph, schema: dict) -> int:
    enums = schema.get("enums", {})
    count = 0
    for enum_name, enum_spec in enums.items():
        if not isinstance(enum_spec, dict):
            continue
        scheme = URIRef(f"https://w3id.org/heritagegraph/scheme/{enum_name}")
        g.add((scheme, RDF.type, SKOS.ConceptScheme))
        g.add((scheme, DCTERMS.title, Literal(enum_name)))
        g.add((scheme, SKOS.inScheme, ONTOLOGY_IRI))
        desc = enum_spec.get("description")
        if desc:
            g.add((scheme, SKOS.definition, Literal(desc)))
        for value_name, value_spec in enum_spec.get("permissible_values", {}).items():
            if not isinstance(value_spec, dict):
                continue
            meaning = value_spec.get("meaning", f"heritageGraph:{value_name}")
            ind = expand_curie(meaning, schema.get("prefixes", {})) or hg_class_uri(value_name)
            if (ind, RDF.type, OWL.NamedIndividual) in g or (ind, RDF.type, OWL.Class) in g:
                g.remove((ind, SKOS.inScheme, None))
                g.add((ind, RDF.type, SKOS.Concept))
                g.add((ind, SKOS.inScheme, scheme))
                g.add((ind, SKOS.prefLabel, Literal(value_name)))
                vdesc = value_spec.get("description")
                if vdesc:
                    g.add((ind, SKOS.definition, Literal(vdesc)))
                count += 1
    return count


# External slot_uri prefixes emitted as rdfs:subPropertyOf in the release TTL.
PROPERTY_ALIGNMENT_PREFIXES = (
    "prov:",
    "crm:",
    "crminf:",
    "datacite:",
    "dcterms:",
    "geo:",
)


def apply_property_alignments(g: Graph, schema: dict) -> int:
    prefixes = schema.get("prefixes", {})
    slots = schema.get("slots", {})
    count = 0
    for name, spec in slots.items():
        if not isinstance(spec, dict):
            continue
        curie = spec.get("slot_uri")
        if not curie or curie.startswith(("heritageGraph:", "rdfs:")):
            continue
        if not any(curie.startswith(p) for p in PROPERTY_ALIGNMENT_PREFIXES):
            continue
        target = expand_curie(curie, prefixes)
        prop = URIRef(f"https://w3id.org/heritagegraph/{name}")
        if not target:
            continue
        if (prop, RDF.type, OWL.ObjectProperty) in g or (
            prop, RDF.type, OWL.DatatypeProperty
        ) in g:
            g.add((prop, RDFS.subPropertyOf, target))
            count += 1
    return count


def bind_release_prefixes(g: Graph, schema: dict) -> None:
    """Ensure commonly referenced external namespaces serialize with stable prefixes."""
    skip = {
        "heritageGraph", "linkml", "schema", "wgs84", "orcid",
        "localcontexts", "tgn", "crmdig", "rdf", "rdfs", "owl", "xsd",
    }
    preferred = {
        "dcterms": "http://purl.org/dc/terms/",
        "dct": "http://purl.org/dc/terms/",
        "schema": "http://schema.org/",
        "pav": "http://purl.org/pav/",
        "void": "http://rdfs.org/ns/void#",
        "datacite": "http://purl.org/spar/datacite/",
    }
    for prefix, uri in preferred.items():
        g.bind(prefix, Namespace(uri))
    for prefix, uri in schema.get("prefixes", {}).items():
        if prefix in skip or prefix in preferred:
            continue
        g.bind(prefix, Namespace(uri))


def normalize_serialized_ttl(ttl: str) -> str:
    """Normalise LinkML-specific prefix aliases to paper-facing names."""
    ttl = ttl.replace("@prefix schema1:", "@prefix schema:")
    ttl = re.sub(r"\bschema1:", "schema:", ttl)
    return ttl


def apply_vocab_mappings_from_yaml(g: Graph, schema: dict) -> int:
    """Emit SKOS mapping triples declared in YAML but missing from LinkML output."""
    prefixes = schema.get("prefixes", {})
    skos_preds = {
        "exact_mappings": SKOS.exactMatch,
        "close_mappings": SKOS.closeMatch,
        "broad_mappings": SKOS.broadMatch,
    }
    count = 0
    for section, uri_fn in (
        ("classes", hg_class_uri),
        ("slots", lambda name: URIRef(f"https://w3id.org/heritagegraph/{name}")),
    ):
        for name, spec in (schema.get(section) or {}).items():
            if not isinstance(spec, dict):
                continue
            subject = uri_fn(name)
            for key, pred in skos_preds.items():
                for curie in spec.get(key, []) or []:
                    target = expand_curie(curie, prefixes)
                    if not target:
                        continue
                    if any(
                        (subject, sk, target) in g
                        for sk in (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch)
                    ):
                        continue
                    g.add((subject, pred, target))
                    count += 1
    return count


def validate_prefix_coverage(g: Graph, schema: dict) -> list[str]:
    """Return warnings when TTL uses namespaces absent from YAML prefix declarations."""

    def norm(uri: str) -> str:
        return uri.rstrip("#/")

    declared = {norm(str(v)) for v in schema.get("prefixes", {}).values()}
    warnings: list[str] = []
    seen: set[str] = set()
    for _s, _p, o in g:
        if not isinstance(o, URIRef):
            continue
        uri = str(o)
        if uri.startswith("https://w3id.org/heritagegraph/"):
            continue
        base = norm(uri.rsplit("#", 1)[0] if "#" in uri else uri.rsplit("/", 1)[0])
        if base in seen:
            continue
        seen.add(base)
        if any(base == norm(d) or base.startswith(norm(d)) or norm(d).startswith(base) for d in declared):
            continue
        if base.startswith(
            (
                "http://www.w3.org/1999/02/22-rdf-syntax-ns",
                "http://www.w3.org/2000/01/rdf-schema",
                "http://www.w3.org/2002/07/owl",
                "http://www.w3.org/2001/XMLSchema",
                "https://w3id.org/linkml",
                "https://creativecommons.org/licenses",
            )
        ):
            continue
        warnings.append(f"namespace used in TTL but not declared in YAML prefixes: {base}")
    return warnings


def apply_missing_definitions(g: Graph, schema: dict) -> None:
    defaults = {
        "ConditionTypeEnum": "Controlled vocabulary for physical condition categories of heritage objects.",
        "ExistenceStatusEnum": "Controlled vocabulary for whether a heritage object or structure still exists.",
        "RitualTypeEnum": "Controlled vocabulary for ritual and festival activity types in Nepalese living heritage.",
        "DatePrecisionEnum": "Controlled vocabulary for temporal precision of heritage dates.",
        "SyncreticTypeEnum": "Controlled vocabulary for types of syncretic theological relationships between deities.",
        "PhysicalHeritageThing": "Union of tangible heritage object classes: structures, iconographic objects, and architectural elements.",
    }
    classes = schema.get("classes", {})
    enums = schema.get("enums", {})
    for name, text in defaults.items():
        uri = hg_class_uri(name)
        if (uri, RDF.type, OWL.Class) in g and not list(g.objects(uri, SKOS.definition)):
            source = classes.get(name) or enums.get(name) or {}
            desc = source.get("description") if isinstance(source, dict) else None
            g.add((uri, SKOS.definition, Literal(desc or text)))


def postprocess_ttl(src: Path, dest: Path, schema: dict) -> Graph:
    g = Graph()
    g.parse(src, format="turtle")

    onts = list(g.subjects(RDF.type, OWL.Ontology))
    if not onts:
        raise RuntimeError("No owl:Ontology node found in generated TTL")
    old = onts[0]
    for p, o in list(g.predicate_objects(old)):
        g.add((ONTOLOGY_IRI, p, o))
        g.remove((old, p, o))
    g.add((ONTOLOGY_IRI, RDF.type, OWL.Ontology))
    for o in list(g.objects(ONTOLOGY_IRI, OWL.versionIRI)):
        g.remove((ONTOLOGY_IRI, OWL.versionIRI, o))
    g.add((ONTOLOGY_IRI, OWL.versionIRI, VERSION_IRI))
    g.add((ONTOLOGY_IRI, OWL.versionInfo, Literal("1.0.0")))
    # Normalise descriptive metadata to a single canonical value each: LinkML
    # (license literal) + YAML annotations can otherwise leave duplicate/string
    # variants (e.g. several dcterms:license triples) that surface in the docs.
    for pred in (DCTERMS.title, DCTERMS.creator, DCTERMS.publisher,
                 DCTERMS.license, DCTERMS.modified):
        for o in list(g.objects(ONTOLOGY_IRI, pred)):
            g.remove((ONTOLOGY_IRI, pred, o))
    g.add((ONTOLOGY_IRI, DCTERMS.title, Literal("HeritageGraph Ontology")))
    g.add((ONTOLOGY_IRI, DCTERMS.creator, Literal("CAIR-Nepal")))
    g.add((ONTOLOGY_IRI, DCTERMS.publisher, Literal("CAIR-Nepal")))
    g.add((ONTOLOGY_IRI, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")))
    g.add((ONTOLOGY_IRI, DCTERMS.modified, Literal(date.today().isoformat())))

    for o in list(g.objects(ONTOLOGY_IRI, OWL.imports)):
        g.remove((ONTOLOGY_IRI, OWL.imports, o))
    for imp in IMPORTS:
        g.add((ONTOLOGY_IRI, OWL.imports, imp))

    for s in list(g.subjects(SKOS.inScheme, None)):
        for o in list(g.objects(s, SKOS.inScheme)):
            if str(o).startswith("file:///"):
                g.remove((s, SKOS.inScheme, o))
                g.add((s, SKOS.inScheme, ONTOLOGY_IRI))

    apply_class_uri_subclass_axioms(g, schema)
    apply_exact_mapping_subclass_axioms(g, schema)
    apply_union_axioms(g, schema)
    apply_disjoint_axioms(g, schema)
    apply_enum_concept_schemes(g, schema)
    apply_property_alignments(g, schema)
    apply_vocab_mappings_from_yaml(g, schema)
    apply_missing_definitions(g, schema)
    fix_object_property_types(g, schema)
    fix_skos_mappings(g)

    person = HG.Person
    if (person, RDF.type, OWL.Class) in g:
        g.add((person, RDFS.subClassOf, FOAF.Person))

    missing = verify_declared_axioms(g, schema)
    if missing:
        raise SystemExit(
            "Declared axioms missing from generated OWL (the LinkML OWL generator "
            "dropped them and no postprocess restored them):\n  - "
            + "\n  - ".join(missing)
        )

    bind_release_prefixes(g, schema)
    ttl = normalize_serialized_ttl(g.serialize(format="turtle"))
    dest.write_text(ttl, encoding="utf-8")
    print(f"Wrote {dest} ({len(g)} triples)")
    for warning in validate_prefix_coverage(g, schema):
        print(f"  ⚠️  {warning}")
    return g


def verify_declared_axioms(g: Graph, schema: dict) -> list[str]:
    """Guard against the LinkML OWL generator silently dropping declared axioms.

    Cross-checks every disjoint_with / union_of / inverse / *_mapping declared in
    the YAML against the post-processed graph and returns a list of any that are
    absent. The release build aborts if this list is non-empty."""
    prefixes = schema.get("prefixes", {})

    def expand(curie: str) -> URIRef | None:
        if ":" not in curie:
            return hg_class_uri(curie)
        p, local = curie.split(":", 1)
        return URIRef(prefixes[p] + local) if p in prefixes else None

    def slot_uri(name: str) -> URIRef:
        return URIRef(f"https://w3id.org/heritagegraph/{name}")

    missing: list[str] = []
    classes = schema.get("classes", {})
    slots = schema.get("slots", {})

    for name, spec in classes.items():
        if not isinstance(spec, dict):
            continue
        a = hg_class_uri(name)
        for target in spec.get("disjoint_with", []) or []:
            b = hg_class_uri(target)
            if (a, OWL.disjointWith, b) not in g and (b, OWL.disjointWith, a) not in g:
                missing.append(f"disjointWith: {name} <-> {target}")
        if spec.get("union_of") and (a, OWL.unionOf, None) not in g:
            missing.append(f"unionOf: {name}")

    for name, spec in slots.items():
        if not isinstance(spec, dict):
            continue
        inv = spec.get("inverse")
        if inv:
            a, b = slot_uri(name), slot_uri(inv)
            if (a, OWL.inverseOf, b) not in g and (b, OWL.inverseOf, a) not in g:
                missing.append(f"inverseOf: {name} <-> {inv}")

    mapping_preds = (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
                     RDFS.subClassOf, RDFS.subPropertyOf, OWL.equivalentClass)
    for section, uri_fn in (("classes", hg_class_uri), ("slots", slot_uri)):
        for name, spec in (schema.get(section) or {}).items():
            if not isinstance(spec, dict):
                continue
            subj = uri_fn(name)
            for key in ("exact_mappings", "close_mappings", "broad_mappings"):
                for curie in spec.get(key, []) or []:
                    tgt = expand(curie)
                    if tgt is None:
                        continue
                    if not any((subj, p, tgt) in g for p in mapping_preds):
                        missing.append(f"{key}: {section}:{name} -> {curie}")
    return missing


def write_alignment_ttl(g_main: Graph) -> None:
    ag = Graph()
    ag.parse(data=g_main.serialize(format="turtle"), format="turtle")
    ag.add((ALIGNMENT_IRI, RDF.type, OWL.Ontology))
    ag.add((ALIGNMENT_IRI, OWL.imports, ONTOLOGY_IRI))
    ag.add((ALIGNMENT_IRI, RDFS.label, Literal("HeritageGraph alignment module")))
    ag.add((ALIGNMENT_IRI, SKOS.definition, Literal(
        "Formal OWL alignment axioms for CRM, PROV, FOAF, and Wikidata federation."
    )))

    for s, o in g_main.subject_objects(RDFS.subClassOf):
        if str(s).startswith(str(HG)) and str(o).startswith("http"):
            ag.add((s, RDFS.subClassOf, o))

    for hg_cls, wd in WIKIDATA_EQUIV.items():
        if (hg_cls, RDF.type, OWL.Class) in ag:
            ag.add((hg_cls, OWL.equivalentClass, wd))

    prefixes = load_schema().get("prefixes", {})
    for name, spec in load_schema().get("slots", {}).items():
        if not isinstance(spec, dict):
            continue
        curie = spec.get("slot_uri")
        if not curie or not curie.startswith("prov:"):
            continue
        target = expand_curie(curie, prefixes)
        prop = URIRef(f"https://w3id.org/heritagegraph/{name}")
        if target and (prop, RDF.type, OWL.ObjectProperty) in ag:
            ag.add((prop, OWL.equivalentProperty, target))

    ag.serialize(destination=ALIGNMENT, format="turtle")
    print(f"Wrote {ALIGNMENT} ({len(ag)} triples)")


def write_edm_profile() -> None:
    eg = Graph()
    eg.bind("heritageGraph", HG)
    eg.bind("edm", EDM)
    eg.bind("owl", OWL)
    eg.bind("rdfs", RDFS)
    eg.bind("skos", SKOS)
    eg.add((EDM_IRI, RDF.type, OWL.Ontology))
    eg.add((EDM_IRI, OWL.imports, ONTOLOGY_IRI))
    eg.add((EDM_IRI, RDFS.label, Literal("HeritageGraph EDM projection profile")))
    eg.add((EDM_IRI, SKOS.definition, Literal(
        "Europeana Data Model projection for HeritageGraph core classes."
    )))

    for hg_cls, edm_cls in EDM_CLASS_MAP.items():
        eg.add((hg_cls, RDFS.subClassOf, edm_cls))
        eg.add((hg_cls, SKOS.closeMatch, edm_cls))

    eg.serialize(destination=EDM_PROFILE, format="turtle")
    print(f"Wrote {EDM_PROFILE} ({len(eg)} triples)")


def write_metadata_ttl(g_main: Graph) -> None:
    mg = Graph()
    mg.bind("void", VOID)
    mg.bind("dcterms", DCTERMS)
    mg.bind("heritageGraph", HG)
    mg.add((DATASET_IRI, RDF.type, VOID.Dataset))
    mg.add((DATASET_IRI, DCTERMS.title, Literal("HeritageGraph Ontology Dataset")))
    mg.add((DATASET_IRI, DCTERMS.creator, Literal("CAIR-Nepal")))
    mg.add((DATASET_IRI, VOID.vocabulary, ONTOLOGY_IRI))
    mg.add((DATASET_IRI, VOID.vocabulary, ALIGNMENT_IRI))
    mg.add((DATASET_IRI, VOID.vocabulary, EDM_IRI))
    mg.add((DATASET_IRI, VOID.triples, Literal(len(g_main), datatype=URIRef("http://www.w3.org/2001/XMLSchema#integer"))))
    mg.add((DATASET_IRI, VOID.inDataset, DATASET_IRI))
    mg.add((ONTOLOGY_IRI, DCTERMS.isPartOf, DATASET_IRI))
    mg.serialize(destination=METADATA, format="turtle")
    print(f"Wrote {METADATA} ({len(mg)} triples)")


def write_abox_example() -> None:
    ABOX.parent.mkdir(parents=True, exist_ok=True)
    content = """@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix crminf: <http://www.cidoc-crm.org/extensions/crminf/> .
@prefix heritageGraph: <https://w3id.org/heritagegraph/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Example ABox: conflicting assertions about syncretic deity identity.
# Demonstrates multi-vocal heritage representation (Part 6 pattern).

heritageGraph:example_Pashupatinath a heritageGraph:Temple ;
    rdfs:label "Pashupatinath Temple (example)"@en .

heritageGraph:example_Matsyendranath a heritageGraph:Deity ;
    rdfs:label "Matsyendranath (example)"@en .

heritageGraph:example_Avalokiteshvara a heritageGraph:Deity ;
    rdfs:label "Avalokiteshvara (example)"@en .

heritageGraph:example_oral_source a heritageGraph:OralHistoryRecording ;
    rdfs:label "Guthi elder interview (example)"@en ;
    heritageGraph:source_type heritageGraph:OralHistory ;
    heritageGraph:epistemic_stance heritageGraph:Community ;
    heritageGraph:community_attribution "Jyapu Mahaguthi tradition-bearers (fictional example)" ;
    heritageGraph:traditional_knowledge_notice "TK Notice — community attribution required for ritual narratives." .

heritageGraph:example_scholarly_source a heritageGraph:ArchivalRecord ;
    rdfs:label "Published syncretism study (example)"@en ;
    heritageGraph:source_type heritageGraph:PublishedScholarship ;
    heritageGraph:epistemic_stance heritageGraph:Scholarly .

heritageGraph:assertion_community_001 a heritageGraph:HeritageAssertion ;
    rdfs:label "Community claim: Matsyendranath embodies Avalokiteshvara"@en ;
    heritageGraph:assertion_content "Matsyendranath is understood as Avalokiteshvara in Newar Buddhist practice." ;
    heritageGraph:asserts_about_entity heritageGraph:example_Matsyendranath ;
    heritageGraph:was_derived_from_source heritageGraph:example_oral_source ;
    heritageGraph:was_attributed_to_agent heritageGraph:example_guthi_elder ;
    heritageGraph:generated_at_time "2024-03-15T10:00:00"^^xsd:dateTime ;
    heritageGraph:confidence_score "0.85"^^xsd:float ;
    heritageGraph:epistemic_stance heritageGraph:Community ;
    heritageGraph:conflicts_with_assertion heritageGraph:assertion_scholarly_001 .

heritageGraph:assertion_scholarly_001 a heritageGraph:HeritageAssertion ;
    rdfs:label "Scholarly claim: distinct figures with ritual conflation"@en ;
    heritageGraph:assertion_content "Matsyendranath and Avalokiteshvara are historically distinct; equivalence is ritual-not ontological." ;
    heritageGraph:asserts_about_entity heritageGraph:example_Matsyendranath ;
    heritageGraph:was_derived_from_source heritageGraph:example_scholarly_source ;
    heritageGraph:generated_at_time "2023-11-02T09:30:00"^^xsd:dateTime ;
    heritageGraph:confidence_score "0.70"^^xsd:float ;
    heritageGraph:epistemic_stance heritageGraph:Scholarly ;
    heritageGraph:conflicts_with_assertion heritageGraph:assertion_community_001 .

heritageGraph:example_guthi_elder a heritageGraph:Person ;
    rdfs:label "Guthi elder (example)"@en .

heritageGraph:example_syncretic_link a heritageGraph:SyncreticRelationship ;
    rdfs:label "Syncretic equivalence claim (example)"@en ;
    heritageGraph:assigned_to_deity heritageGraph:example_Matsyendranath ;
    heritageGraph:assigned_equivalent heritageGraph:example_Avalokiteshvara ;
    heritageGraph:syncretic_type heritageGraph:Equivalence ;
    heritageGraph:was_derived_from_source heritageGraph:example_oral_source ;
    heritageGraph:confidence_score "0.80"^^xsd:float ;
    heritageGraph:reconciliation_status "contested" .
"""
    ABOX.write_text(content, encoding="utf-8")
    print(f"Wrote {ABOX}")


def write_changelog() -> None:
    text = """# Changelog

## [1.0.0] - 2026-06-05

### Added
- Full OWL `rdfs:subClassOf` axioms for all external `class_uri` mappings (CRM, CRMinf, CRMsci, PROV, OWL-Time).
- Named `owl:unionOf` for `PhysicalHeritageThing`, `HeritageEvent`, and `AssertableEntity`.
- SKOS `ConceptScheme` publication for all controlled enumerations.
- `HeritageGraph-alignment.ttl` alignment module (CRM/PROV/FOAF/Wikidata bridges).
- `HeritageGraph-edm.ttl` Europeana Data Model projection profile.
- `heritagegraph-metadata.ttl` VoID dataset description.
- `examples/abox-conflicting-assertions.ttl` demonstrating multi-vocal assertions.
- `owl:versionIRI` and Dublin Core ontology metadata.
- Local Contexts label slot, ORCID identifier slot, and enum/class definitions completed.
- Expanded `owl:imports` (CRM, CRMinf, PROV, OWL-Time, GeoSPARQL, EDM).

### Changed
- `documented_in_source` aligned to `prov:wasInfluencedBy` (distinct from assertion `wasDerivedFrom`).
- Manuscript metrics reconciled with released TTL counts.
- Regeneration pipeline centralises all release post-processing.

### Fixed
- Manuscript–artefact metric mismatch (class/property counts).
- Missing `skos:definition` on six classes.
- Stale `docs/ontology.ttl` synchronised from release artefact.
"""
    CHANGELOG.write_text(text, encoding="utf-8")
    print(f"Wrote {CHANGELOG}")


def generate_shacl() -> None:
    cmd = [
        "linkml",
        "generate",
        "shacl",
        str(SCHEMA),
        "-f",
        "ttl",
        "--no-mergeimports",
    ]
    result = subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
    SHACL.write_text(result.stdout, encoding="utf-8")
    print(f"Wrote {SHACL}")


def sync_docs() -> None:
    shutil.copy2(TTL, DOCS_TTL)
    print(f"Synced {DOCS_TTL}")
    docs_owl = ROOT / "docs" / "ontology.owl"
    g = Graph()
    g.parse(TTL, format="turtle")
    g.serialize(destination=docs_owl, format="xml")
    g.serialize(destination=REVIEW_OWL, format="xml")
    print(f"Synced {docs_owl}")
    print(f"Synced {REVIEW_OWL}")


def main() -> int:
    if not SCHEMA.exists():
        print(f"Missing schema: {SCHEMA}", file=sys.stderr)
        return 1

    schema = load_schema()
    generate_ttl()
    g = postprocess_ttl(REGEN, TTL, schema)
    write_alignment_ttl(g)
    write_edm_profile()
    write_metadata_ttl(g)
    write_abox_example()
    write_changelog()
    generate_shacl()
    sync_docs()
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "refresh_docs_metadata.py")],
        cwd=ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
