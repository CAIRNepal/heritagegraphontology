#!/usr/bin/env python3
"""Finalize HeritageGraph 0.1.0-alpha.5 artifacts.

Addresses the committee-review validation blockers for the alpha.5 lineage:
  1. OWL: gen-owl (--no-use-native-uris) drops `disjoint_with`; this script
     re-injects owl:disjointWith, asserts FAIR metadata as typed triples, and
     ABORTS if any declared axiom (disjointness, inverses, mappings,
     subproperty bridges) is missing from the final graph (axiom-survival
     guard).
  2. SHACL: gen-shacl output fails its own demonstrator (identifier MinCount
     on every node although the node IRI is the identifier; sh:class on
     union_of classes that no generator can satisfy; closed shapes). This
     script repairs the shapes: drops identifier min-counts, rewrites
     sh:class <union class> as sh:or over the union members, and opens the
     closed shapes (documented relaxation).
  3. Runs pyshacl over examples/kathmandu-mini-abox.ttl and aborts
     unless CONFORMANT; writes the report to evaluation/results/.
"""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef
from rdflib.collection import Collection
from rdflib.namespace import DCTERMS, SKOS, XSD
from linkml_runtime import SchemaView

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "ontology" / "HeritageGraph.yaml"
# serialization wrapper (LinkML tree_root Container + Metadata): JSON Schema only
CONTAINER_SCHEMA = ROOT / "ontology" / "HeritageGraph-container.yaml"
OWL_OUT = ROOT / "ontology" / "HeritageGraph.ttl"
SHACL_OUT = ROOT / "ontology" / "HeritageGraph.shacl.ttl"
ABOX = ROOT / "examples" / "kathmandu-mini-abox.ttl"
RESULTS = ROOT / "evaluation" / "results"

def _schema_identity() -> tuple[str, str]:
    """HeritageGraph namespace and ontology IRI, read from the LinkML source
    (default_prefix / prefixes / owl:ontologyIRI annotation) so that the YAML
    is the single place they are defined."""
    import yaml
    data = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    ns = data["prefixes"][data["default_prefix"]]
    return ns, data["annotations"]["owl:ontologyIRI"]


HG_NS, _ONTOLOGY_IRI = _schema_identity()
HG = Namespace(HG_NS)
SH = Namespace("http://www.w3.org/ns/shacl#")
BIBO = Namespace("http://purl.org/ontology/bibo/")
VANN = Namespace("http://purl.org/vocab/vann/")
ONTOLOGY_IRI = URIRef(_ONTOLOGY_IRI)


def gen(kind: str, out: Path, extra: list[str] | None = None) -> None:
    cmd = ["linkml", "generate", kind, str(SCHEMA)] + (extra or [])
    res = subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True)
    lines = res.stdout.splitlines(keepends=True)
    start = next(i for i, l in enumerate(lines) if l.startswith("@prefix"))
    out.write_text("".join(lines[start:]), encoding="utf-8")
    print(f"generated {out.name}")


def uri_for(sv: SchemaView, curie: str) -> URIRef | None:
    if not curie or ":" not in str(curie):
        return None
    try:
        return URIRef(sv.expand_curie(str(curie)))
    except Exception:
        return None


def humanize_name(name: str) -> str:
    """Mechanically derive a human-readable label from a LinkML element name.

    AgeCriterion -> 'Age Criterion'; assesses_candidate -> 'Assesses candidate';
    PartiallyExtant -> 'Partially Extant'; id -> 'ID'. Purely derived from the
    single-source-of-truth name, so it never drifts from the YAML."""
    import re as _re
    if name == "id":
        return "ID"
    if "_" in name:
        words = name.split("_")
        return " ".join([words[0].capitalize()] + [w.lower() for w in words[1:]])
    return _re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", name)


# Editorial annotation predicates the LinkML schema uses on its own terms.
# Since 1.1.0 their values are published as skos:editorialNote (prefixed with
# EDITORIAL_PREFIX) and the hg: predicates remain only as deprecated stubs.
ANNOTATION_DEFINITIONS = {
    "crminf_pattern": "Editorial note naming the CRMinf pattern that a class instantiates.",
    "design_note": "Editorial note recording a modelling decision about a term.",
    "prov_alignment": "Editorial note naming the PROV-O term that a slot is aligned with.",
    "prov_alignment_note": "Editorial note explaining the status of a class's PROV-O alignment.",
    "provenance_scope": "States whether a class's provenance slots describe the data record or the real-world referent.",
}
EDITORIAL_PREFIX = {
    "crminf_pattern": "CRMinf pattern",
    "design_note": "Design note",
    "prov_alignment": "PROV-O alignment",
    "prov_alignment_note": "PROV-O alignment note",
    "provenance_scope": "Provenance scope",
}


def humanize_and_tag_labels(g: Graph) -> None:
    """Humanize machine-style labels and add @en tags (gen-owl emits element
    names as bare literals). Ontology-node labels (proper names) are tagged
    but never re-worded; literals already carrying a language tag or datatype
    are left untouched."""
    label_preds = (RDFS.label, SKOS.prefLabel, DCTERMS.title)
    text_preds = (SKOS.definition, SKOS.scopeNote, SKOS.altLabel,
                  SKOS.changeNote, DCTERMS.description, SKOS.editorialNote)
    ontology_nodes = set(g.subjects(RDF.type, OWL.Ontology))
    n_hum, n_tag = 0, 0
    for pred in label_preds + text_preds:
        for s, o in list(g.subject_objects(pred)):
            if not isinstance(o, Literal) or o.language is not None:
                continue
            if o.datatype is not None:
                continue
            text = str(o)
            if (pred in label_preds and s not in ontology_nodes
                    and " " not in text and text.replace("_", "").isalnum()):
                new_text = humanize_name(text)
                if new_text != text:
                    n_hum += 1
            else:
                new_text = text
            g.remove((s, pred, o))
            g.add((s, pred, Literal(new_text, lang="en")))
            n_tag += 1
    print(f"labels: humanized {n_hum} machine-style label(s); tagged {n_tag} literal(s) @en")


def apply_attribute_ranges(g: Graph, sv: SchemaView) -> None:
    """LinkML class-scoped attributes (Container/Metadata collections) get no
    global rdfs:range from gen-owl (only per-class restrictions). Each attribute
    property is used by exactly one class, so its declared range is globally
    valid; assert it. Skips datatypes outside the OWL 2 map (handled by SHACL)."""
    XSD_MAP = {"string": XSD.string, "integer": XSD.integer, "float": XSD.float,
               "boolean": XSD.boolean, "datetime": XSD.dateTime,
               "uriorcurie": XSD.anyURI}
    n = 0
    for cn, c in sv.all_classes().items():
        for attr in (c.attributes or {}).values():
            prop = URIRef(f"{HG_NS}{attr.name}")
            if (prop, RDF.type, None) not in g or (prop, RDFS.range, None) in g:
                continue
            rng = attr.range or "string"
            if rng in sv.all_classes():
                rc = sv.get_class(rng)
                target = uri_for(sv, str(rc.class_uri or f"heritageGraph:{rng}"))
            elif rng in XSD_MAP:
                target = XSD_MAP[rng]
            else:
                continue
            if target:
                g.add((prop, RDFS.range, target))
                n += 1
    print(f"asserted rdfs:range on {n} attribute propert(ies)")


def finalize_owl(sv: SchemaView) -> Graph:
    g = Graph()
    g.parse(OWL_OUT, format="turtle")

    # --- re-inject disjointness (gen-owl drops it) ---
    n_disjoint = 0
    for cn, c in sv.all_classes().items():
        for target in c.disjoint_with or []:
            a = uri_for(sv, str(sv.get_class(cn).class_uri or f"heritageGraph:{cn}"))
            b_cls = sv.get_class(target)
            b = uri_for(sv, str(b_cls.class_uri or f"heritageGraph:{target}"))
            if a and b:
                g.add((a, OWL.disjointWith, b))
                n_disjoint += 1
    print(f"injected {n_disjoint} owl:disjointWith axiom(s)")

    # --- re-inject union_of (gen-owl drops the declared class unions) ---
    n_union = 0
    for cn, c in sv.all_classes().items():
        if not c.union_of:
            continue
        cls = uri_for(sv, str(c.class_uri or f"heritageGraph:{cn}"))
        members = []
        for m in c.union_of:
            mc = sv.get_class(m)
            members.append(uri_for(sv, str(mc.class_uri or f"heritageGraph:{m}")))
        # remove any prior (possibly broken) union on this class
        for eq in list(g.objects(cls, OWL.equivalentClass)):
            if (eq, OWL.unionOf, None) in g:
                g.remove((cls, OWL.equivalentClass, eq))
        for sc in list(g.objects(cls, RDFS.subClassOf)):
            if (sc, OWL.unionOf, None) in g:
                g.remove((cls, RDFS.subClassOf, sc))
        expr = BNode()
        head = BNode()
        Collection(g, head, members)
        g.add((expr, RDF.type, OWL.Class))
        g.add((expr, OWL.unionOf, head))
        # A union over HeritageGraph classes is a definition (≡). A union that
        # contains external classes (crm:E21_Person, …) is stated as a covering
        # axiom (⊑) only: ≡ would make every member, i.e. CIDOC-CRM / CRMinf /
        # PROV classes, a subclass of a HeritageGraph class.
        if all(str(m).startswith(HG_NS) for m in members):
            g.add((cls, OWL.equivalentClass, expr))
        else:
            g.add((cls, RDFS.subClassOf, expr))
        n_union += 1
    print(f"injected {n_union} owl:unionOf class definition(s)")

    # --- declare annotation predicates (silences OWLAPI type-guessing:
    #     'annotation property range axiom turned to data property range') ---
    n_ann = 0
    for s, pred, o in list(g.triples((None, None, None))):
        pass
    ANNOTATION_PREDICATES = [
        "http://purl.org/dc/terms/bibliographicCitation",
        "http://purl.org/dc/terms/created",
        "http://purl.org/dc/terms/license",
        "http://purl.org/dc/terms/modified",
        "http://purl.org/dc/terms/issued",
        "http://purl.org/dc/terms/source",
        "http://purl.org/dc/terms/creator",
        "http://purl.org/dc/terms/publisher",
        "http://purl.org/ontology/bibo/status",
        "http://purl.org/ontology/bibo/doi",
        "http://purl.org/pav/version",
        "http://purl.org/vocab/vann/preferredNamespacePrefix",
        "http://purl.org/vocab/vann/preferredNamespaceUri",
    ]
    for ap in ANNOTATION_PREDICATES:
        u = URIRef(ap)
        # never pun: skip predicates already declared object/datatype properties
        if ((u, RDF.type, OWL.ObjectProperty) in g
                or (u, RDF.type, OWL.DatatypeProperty) in g):
            continue
        if (None, u, None) in g and (u, RDF.type, OWL.AnnotationProperty) not in g:
            g.add((u, RDF.type, OWL.AnnotationProperty))
            n_ann += 1
    # Record-level annotation predicates used by the released instance data but
    # not by the schema itself; declared so ontology + data stays inside OWL 2
    # DL (an undeclared predicate is a profile violation).
    for u in (DCTERMS.date,):
        if (u, RDF.type, None) not in g:
            g.add((u, RDF.type, OWL.AnnotationProperty))
            n_ann += 1
    print(f"declared {n_ann} owl:AnnotationProperty(ies)")

    # --- SKOS publication of enumerations (gen-owl emits nothing for them) ---
    # DUAL-REPRESENTATION RATIONALE (alpha.6): each enum is published both as
    # an OWL enumeration class (owl:oneOf over owl:NamedIndividual values, for
    # DL reasoning over enum-ranged properties) and as a SKOS concept scheme
    # (for vocabulary tooling and mapping). To avoid two IRIs (and duplicate
    # labels) per value, the SKOS concept IS the OWL individual: the same IRI
    # is typed owl:NamedIndividual and skos:Concept (DL-legal: skos:Concept is
    # declared owl:Class, so this is just an individual with two types).
    n_scheme, n_concept = 0, 0
    skos_enum_preds = {"exact_mappings": SKOS.exactMatch,
                       "close_mappings": SKOS.closeMatch,
                       "broad_mappings": SKOS.broadMatch,
                       "narrow_mappings": SKOS.narrowMatch,
                       "related_mappings": SKOS.relatedMatch}
    for en, e in sv.all_enums().items():
        enum_cls = URIRef(f"{HG_NS}{en}")
        scheme = URIRef(f"{HG_NS}scheme/{en}")
        g.add((scheme, RDF.type, SKOS.ConceptScheme))
        # rdfs:label alongside prefLabel: generic tools (ROBOT report,
        # Protege) look for rdfs:label and flagged these as missing_label.
        # The '(concept scheme)' suffix keeps the scheme's label distinct from
        # the enum class of the same name (ROBOT duplicate_label); prefLabel
        # carries the same text so the scheme has one label per language.
        scheme_label = Literal(f"{humanize_name(en)} (concept scheme)", lang="en")
        g.add((scheme, SKOS.prefLabel, scheme_label))
        g.add((scheme, RDFS.label, scheme_label))
        if e.description:
            g.add((scheme, SKOS.definition, Literal(str(e.description))))
        # enum-level mappings (e.g. ArchitecturalStyle broadMatch crm:E55_Type)
        for key, pred in skos_enum_preds.items():
            for curie in getattr(e, key, None) or []:
                tgt = uri_for(sv, str(curie))
                if tgt is not None and (enum_cls, RDF.type, None) in g:
                    g.add((enum_cls, pred, tgt))
        n_scheme += 1
        for vn, pv in (e.permissible_values or {}).items():
            # concept IRI: the declared meaning where present (matches data
            # serialization); otherwise the IRI gen-owl minted for the
            # permissible value (<enum-class-IRI>#<value>), so OWL individual
            # and SKOS concept are one resource. scheme/<Enum>/<value> remains
            # only as a fallback if gen-owl emitted nothing for the value.
            if pv.meaning:
                c = uri_for(sv, str(pv.meaning))
            else:
                c = URIRef(f"{HG_NS}{en}#{vn}")
                if (c, None, None) not in g:
                    c = URIRef(f"{HG_NS}scheme/{en}/{vn}")
            g.add((c, RDF.type, SKOS.Concept))
            g.add((c, SKOS.inScheme, scheme))
            # the value's title (e.g. "Stupa style") keeps it distinct from a
            # class of the same name; gen-owl itself labels it with the name
            label = Literal(str(pv.title), lang="en") if pv.title else Literal(vn)
            g.remove((c, SKOS.prefLabel, None))
            g.add((c, SKOS.prefLabel, label))
            if not pv.meaning:
                # label minted concepts only; external meaning IRIs (aat:,
                # wikidata:) keep their owners' labels to avoid duplicate_label
                g.remove((c, RDFS.label, None))
                g.add((c, RDFS.label, label))
            if pv.description:
                g.add((c, SKOS.definition, Literal(str(pv.description))))
            n_concept += 1
    print(f"published {n_scheme} SKOS concept scheme(s) with {n_concept} concept(s)")

    # --- owl:deprecated for slots using the LinkML deprecated metaslot ---
    n_dep = 0
    for sn, s in sv.all_slots().items():
        if s.deprecated and s.slot_uri:
            prop = uri_for(sv, str(s.slot_uri))
            if (prop, RDF.type, None) not in g:
                # slot no longer attached to any class: gen-owl emits nothing,
                # so declare it here to keep it findable (and DL-legal)
                g.add((prop, RDF.type, OWL.DatatypeProperty))
                g.add((prop, RDFS.label, Literal(sn)))
                if s.description:
                    g.add((prop, SKOS.definition, Literal(str(s.description))))
            g.add((prop, OWL.deprecated, Literal(True)))
            # obsolete label (ROBOT convention) and the replacement term
            g.remove((prop, RDFS.label, None))
            g.add((prop, RDFS.label, Literal(f"obsolete {humanize_name(sn).lower()}", lang="en")))
            repl = s.deprecated_element_has_exact_replacement or s.deprecated_element_has_possible_replacement
            if repl and repl in sv.all_slots():
                r = sv.get_slot(repl)
                g.add((prop, DCTERMS.isReplacedBy,
                       uri_for(sv, str(r.slot_uri)) if r.slot_uri else URIRef(f"{HG_NS}{repl}")))
                # declared here: the general annotation declaration ran earlier (OWL 2 DL)
                g.add((DCTERMS.isReplacedBy, RDF.type, OWL.AnnotationProperty))
            n_dep += 1
    print(f"marked {n_dep} property(ies) owl:deprecated")

    # --- slot titles as labels (gen-owl labels a property with its name) ---
    n_title = 0
    titled = {sn: sl for sn, sl in sv.all_slots().items() if sl.title}
    for cn, cl in sv.all_classes().items():
        for an, at in (cl.attributes or {}).items():
            if at.title:
                titled.setdefault(an, at)
    for sn, sl in titled.items():
        prop = uri_for(sv, str(sl.slot_uri)) if sl.slot_uri else URIRef(f"{HG_NS}{sn}")
        if prop is not None and (prop, RDF.type, None) in g:
            g.remove((prop, RDFS.label, None))
            g.add((prop, RDFS.label, Literal(str(sl.title), lang="en")))
            n_title += 1
    print(f"labelled {n_title} property(ies) from their slot title")

    # --- LinkML serialization constructs out of the OWL (1.1.0) ---
    strip_linkml_serialization(g)
    add_deprecated_stubs(g)

    # the LinkML schema IRI, which gen-owl uses as every term's skos:inScheme
    schema_iri = URIRef(HG_NS + "schema")
    if (None, SKOS.inScheme, schema_iri) in g:
        g.add((schema_iri, RDF.type, SKOS.ConceptScheme))
        g.add((schema_iri, RDFS.label, Literal("HeritageGraph LinkML schema", lang="en")))
        g.add((schema_iri, SKOS.definition, Literal(
            "The LinkML schema from which this ontology is generated; every generated term is skos:inScheme it.",
            lang="en")))

    # --- FAIR metadata as typed triples on the ontology node ---
    onts = list(g.subjects(RDF.type, OWL.Ontology))
    ont = onts[0] if onts else ONTOLOGY_IRI
    schema_version = str(sv.schema.version)
    # descriptive metadata comes from the schema header; creators are "; "-separated
    header = {k: str(v.value) for k, v in (sv.schema.annotations or {}).items()}
    citation = header.get("dcterms:bibliographicCitation") or (
        f"CAIR-Nepal (2026). HeritageGraph Ontology ({schema_version}). {ONTOLOGY_IRI}")
    creators = [c.strip() for c in header.get("dcterms:creator", "CAIR-Nepal").split(";") if c.strip()]
    meta = [
        (DCTERMS.created, Literal("2025-11-23", datatype=XSD.date)),
        (DCTERMS.modified, Literal(date.today().isoformat(), datatype=XSD.date)),
        (DCTERMS.source, URIRef("https://github.com/CAIRNepal/heritagegraphontology")),
        (DCTERMS.bibliographicCitation, Literal(citation)),
        (DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")),
        *[(DCTERMS.creator, Literal(c)) for c in creators],
        (DCTERMS.publisher, Literal(header.get("dcterms:publisher", "CAIR-Nepal"))),
        (BIBO.status, Literal(header.get("bibo:status", "Published"))),
        (VANN.preferredNamespacePrefix, Literal("heritageGraph")),
        (VANN.preferredNamespaceUri, Literal(HG_NS)),
    ]
    # release identifiers set in the schema header (dcterms:issued, bibo:doi)
    if header.get("dcterms:issued"):
        meta.append((DCTERMS.issued, Literal(header["dcterms:issued"], datatype=XSD.date)))
    if header.get("bibo:doi"):
        meta.append((BIBO.doi, Literal(header["bibo:doi"])))
    if header.get("owl:priorVersion"):
        meta.append((OWL.priorVersion, URIRef(header["owl:priorVersion"])))
    for p in {p for p, _ in meta}:
        g.remove((ont, p, None))
    for p, o in meta:
        g.add((ont, p, o))
    g.bind("bibo", BIBO); g.bind("vann", VANN)

    apply_attribute_ranges(g, sv)
    repair_dl_profile(g, sv)
    drop_pattern_facets(g)
    add_external_class_domains(g, sv)
    drop_vacuous_min_cardinality(g)
    humanize_and_tag_labels(g)
    # after humanizing: official labels are copied verbatim
    apply_official_external_annotations(g)

    # --- axiom-survival guard ---
    missing: list[str] = []
    for cn, c in sv.all_classes().items():
        a = uri_for(sv, str(c.class_uri or f"heritageGraph:{cn}"))
        for t in c.disjoint_with or []:
            tb = sv.get_class(t)
            b = uri_for(sv, str(tb.class_uri or f"heritageGraph:{t}"))
            if not ((a, OWL.disjointWith, b) in g or (b, OWL.disjointWith, a) in g):
                missing.append(f"disjointWith {cn} <-> {t}")
    mapping_preds = (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
                     SKOS.narrowMatch, SKOS.relatedMatch,
                     RDFS.subClassOf, RDFS.subPropertyOf)
    for section, getter in (("class", sv.all_classes), ("slot", sv.all_slots)):
        for name, el in getter().items():
            if section == "class":
                subj = uri_for(sv, str(el.class_uri or f"heritageGraph:{name}"))
            else:
                subj = uri_for(sv, str(el.slot_uri)) if el.slot_uri else None
            if subj is None:
                continue
            for key in ("exact_mappings", "close_mappings", "broad_mappings",
                        "narrow_mappings", "related_mappings"):
                for curie in getattr(el, key, None) or []:
                    tgt = uri_for(sv, str(curie))
                    if tgt is None:
                        continue
                    if not any((subj, p, tgt) in g for p in mapping_preds):
                        missing.append(f"{key}: {section} {name} -> {curie}")
    for cn, c in sv.all_classes().items():
        if c.union_of:
            cls = uri_for(sv, str(c.class_uri or f"heritageGraph:{cn}"))
            ok = any((eq, OWL.unionOf, None) in g
                     for eq in list(g.objects(cls, OWL.equivalentClass))
                     + list(g.objects(cls, RDFS.subClassOf)))
            if not ok:
                missing.append(f"unionOf: {cn}")
    for sn, s in sv.all_slots().items():
        if s.deprecated and s.slot_uri:
            if (uri_for(sv, str(s.slot_uri)), OWL.deprecated, None) not in g:
                missing.append(f"owl:deprecated: {sn}")
    for en, e in sv.all_enums().items():
        scheme = URIRef(f"{HG_NS}scheme/{en}")
        if (scheme, RDF.type, SKOS.ConceptScheme) not in g:
            missing.append(f"conceptScheme: {en}")
        for vn, pv in (e.permissible_values or {}).items():
            if pv.meaning:
                candidates = [uri_for(sv, str(pv.meaning))]
            else:
                candidates = [
                    URIRef(f"{HG_NS}{en}#{vn}"),
                    URIRef(f"{HG_NS}scheme/{en}/{vn}"),
                ]
            if not any((c, SKOS.inScheme, scheme) in g for c in candidates):
                missing.append(f"enumConcept: {en}.{vn}")
        for key in ("exact_mappings", "close_mappings", "broad_mappings",
                    "narrow_mappings", "related_mappings"):
            for curie in getattr(e, key, None) or []:
                tgt = uri_for(sv, str(curie))
                subj = URIRef(f"{HG_NS}{en}")
                if tgt is not None and not any((subj, p, tgt) in g for p in mapping_preds):
                    missing.append(f"{key}: enum {en} -> {curie}")
    for sn, s in sv.all_slots().items():
        if s.inverse and s.slot_uri:
            a = uri_for(sv, str(s.slot_uri))
            inv = sv.get_slot(s.inverse)
            b = uri_for(sv, str(inv.slot_uri)) if inv and inv.slot_uri else None
            if a and b and not ((a, OWL.inverseOf, b) in g or (b, OWL.inverseOf, a) in g):
                missing.append(f"inverseOf: {sn} <-> {s.inverse}")
    if missing:
        # inverseOf pairs: gen-owl emits owl:inverseOf only sometimes; restore.
        restored = 0
        still = []
        for m in list(missing):
            if m.startswith("inverseOf:"):
                pair = m.split(":", 1)[1].strip().split(" <-> ")
                a = uri_for(sv, str(sv.get_slot(pair[0]).slot_uri))
                b = uri_for(sv, str(sv.get_slot(pair[1]).slot_uri))
                g.add((a, OWL.inverseOf, b)); restored += 1
            else:
                still.append(m)
        print(f"restored {restored} owl:inverseOf axiom(s)")
        if still:
            sys.exit("AXIOM SURVIVAL GUARD FAILED:\n  - " + "\n  - ".join(still[:20]))
    g.serialize(destination=OWL_OUT, format="turtle")
    print(f"finalized {OWL_OUT.name} ({len(g)} triples)")
    return g


GEO = Namespace("http://www.opengis.net/ont/geosparql#")


LINKML_PV = URIRef("https://w3id.org/linkml/permissible_values")
DEPRECATION_NOTE = (
    "Deprecated in HeritageGraph 1.1.0: a LinkML serialization construct for "
    "JSON/YAML data files, not a domain term. It is defined in "
    "HeritageGraph-container.yaml and used only by the JSON Schema; RDF instance "
    "data should not use it.")


def strip_linkml_serialization(g: Graph) -> None:
    """Remove LinkML-internal vocabulary from the OWL release.

    (1) linkml:permissible_values: gen-owl lists each enum value on its enum
        class with this LinkML predicate; the OWL already states the values
        as owl:oneOf over named individuals (and the SKOS scheme lists them),
        so the triples only add a non-OWL annotation property.
    (2) The schema's editorial annotations (design_note, prov_alignment, ...)
        become skos:editorialNote on HeritageGraph's own terms, prefixed with
        the note kind so no information is lost; on external terms (reused
        CIDOC-CRM / CRMinf / PROV-O IRIs) they are dropped, since
        HeritageGraph does not annotate terms it does not own."""
    n_pv = len(list(g.triples((None, LINKML_PV, None))))
    g.remove((None, LINKML_PV, None))
    g.remove((LINKML_PV, None, None))
    n_own, n_ext = 0, 0
    for name, prefix in EDITORIAL_PREFIX.items():
        pred = URIRef(HG_NS + name)
        for s, o in list(g.subject_objects(pred)):
            g.remove((s, pred, o))
            if isinstance(s, URIRef) and str(s).startswith(HG_NS):
                g.add((s, SKOS.editorialNote, Literal(f"{prefix}: {o}", lang="en")))
                n_own += 1
            else:
                n_ext += 1
        g.remove((pred, None, None))
    print(f"removed {n_pv} linkml:permissible_values triple(s); editorial notes: "
          f"{n_own} -> skos:editorialNote, {n_ext} on external terms dropped")


def add_deprecated_stubs(g: Graph) -> None:
    """Keep every IRI that 1.0.x published for a LinkML-only construct as an
    owl:deprecated stub (declaration + obsolete label + definition, no logical
    axioms), so the change is backward compatible: the container classes and
    their collection/header properties (read from the wrapper schema), and the
    editorial annotation predicates (replaced by skos:editorialNote)."""
    cv = SchemaView(str(CONTAINER_SCHEMA))
    core = set(SchemaView(str(SCHEMA)).all_classes())
    n = 0

    def stub(u: URIRef, typ: URIRef, label: str, definition: str | None, note: str) -> None:
        g.add((u, RDF.type, typ))
        g.add((u, OWL.deprecated, Literal(True)))
        g.remove((u, RDFS.label, None))
        g.add((u, RDFS.label, Literal(f"obsolete {label}", lang="en")))
        if definition:
            g.add((u, SKOS.definition, Literal(definition, lang="en")))
        g.add((u, SKOS.editorialNote, Literal(note, lang="en")))
        g.add((u, SKOS.inScheme, URIRef(HG_NS + "schema")))

    for cn, c in cv.all_classes(imports=False).items():
        if cn in core:
            continue
        cls = URIRef(cv.get_uri(c, expand=True))
        stub(cls, OWL.Class, humanize_name(cn), c.description, DEPRECATION_NOTE)
        n += 1
        for an, a in (c.attributes or {}).items():
            if a.annotations and "since" in a.annotations:
                continue  # added after 1.0.x: never published in the OWL, no stub
            prop = URIRef(HG_NS + an)
            rng = a.range or "string"
            typ = OWL.ObjectProperty if (rng in cv.all_classes() or rng in cv.all_enums()) \
                else OWL.DatatypeProperty
            stub(prop, typ, (a.title or humanize_name(an)).lower(), a.description, DEPRECATION_NOTE)
            n += 1
    for name, definition in ANNOTATION_DEFINITIONS.items():
        u = URIRef(HG_NS + name)
        stub(u, OWL.AnnotationProperty, humanize_name(name).lower(), definition,
             "Deprecated in HeritageGraph 1.1.0: the note is published as "
             f"skos:editorialNote with the prefix '{EDITORIAL_PREFIX[name]}: '.")
        g.add((u, DCTERMS.isReplacedBy, SKOS.editorialNote))
        n += 1
    g.add((DCTERMS.isReplacedBy, RDF.type, OWL.AnnotationProperty))
    print(f"kept {n} published LinkML-only IRI(s) as owl:deprecated stubs")


IMPORTS = ROOT / "ontology" / "imports"
PROV_DEFINITION = URIRef("http://www.w3.org/ns/prov#definition")
# annotation predicates HeritageGraph must not write on terms it does not own
OWNER_TEXT_PREDS = (RDFS.label, RDFS.comment, SKOS.definition, SKOS.inScheme,
                    SKOS.prefLabel, SKOS.altLabel, SKOS.scopeNote,
                    SKOS.editorialNote, DCTERMS.description)


def _official_sources() -> list[tuple[str, Graph, URIRef]]:
    """Load the committed official vocabulary snapshots (ontology/imports/),
    verifying each file against the sha256 recorded in sources.json."""
    import hashlib
    import json
    meta = json.loads((IMPORTS / "sources.json").read_text(encoding="utf-8"))
    out = []
    for src in meta["sources"]:
        path = IMPORTS / src["file"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != src["sha256"]:
            sys.exit(f"official vocabulary snapshot changed: {src['file']} (sha256 {digest})")
        vg = Graph()
        vg.parse(path, format=src["format"])
        out.append((src["namespace"], vg, URIRef(src["isDefinedBy"])))
    return out


def _english(literals) -> list[Literal]:
    lits = [l for l in literals if isinstance(l, Literal)]
    en = [l for l in lits if l.language == "en"]
    return en or [l for l in lits if l.language is None]


def apply_official_external_annotations(g: Graph) -> None:
    """Option A' for reused external terms (CIDOC-CRM, CRMinf, PROV-O, ...).

    gen-owl labels and defines every reused IRI with the LinkML element's
    name and description ("Technique" on crm:E29_Design_or_Procedure,
    "Depicts deity" on crm:P62_depicts) and puts it in HeritageGraph's
    scheme. Published that way, HeritageGraph redefines terms it does not
    own. Replace all of HeritageGraph's text on external subjects with the
    owner's own: the official English rdfs:label, the official definition
    (prov:definition for PROV-O, else rdfs:comment, e.g. the CIDOC-CRM scope
    note) as skos:definition, and rdfs:isDefinedBy the source vocabulary.
    HeritageGraph's usage wording moves to the SHACL shapes (finalize_shacl).
    Aborts if any external term would be left without an official label."""
    sources = _official_sources()
    targets = sorted({s for p in OWNER_TEXT_PREDS for s in g.subjects(p, None)
                      if isinstance(s, URIRef) and not str(s).startswith(HG_NS)
                      and s != ONTOLOGY_IRI})
    missing, n_removed = [], 0
    for s in targets:
        for p in OWNER_TEXT_PREDS:
            for o in list(g.objects(s, p)):
                g.remove((s, p, o)); n_removed += 1
        src = next(((vg, idb) for ns, vg, idb in sources
                    if str(s).startswith(ns) and (s, RDFS.label, None) in vg), None)
        if src is None:
            missing.append(str(s)); continue
        vg, idb = src
        labels = _english(vg.objects(s, RDFS.label))
        if not labels:
            missing.append(str(s)); continue
        for l in labels:
            g.add((s, RDFS.label, Literal(str(l).strip(), lang=l.language)))
        defs = (_english(vg.objects(s, PROV_DEFINITION))
                or _english(vg.objects(s, RDFS.comment))
                or _english(vg.objects(s, SKOS.definition)))
        if defs:
            lang = defs[0].language
            text = "\n\n".join(sorted(str(d).strip() for d in defs))
            g.add((s, SKOS.definition, Literal(text, lang=lang)))
        g.add((s, RDFS.isDefinedBy, next(vg.objects(s, RDFS.isDefinedBy), idb)))
    if missing:
        sys.exit("NO OFFICIAL LABEL for reused term(s) (add the vocabulary to "
                 "ontology/imports/):\n  - " + "\n  - ".join(missing))
    print(f"external terms: replaced {n_removed} HeritageGraph-written annotation(s) "
          f"on {len(targets)} term(s) with official labels/definitions")


def drop_pattern_facets(g: Graph) -> None:
    """LinkML `pattern` becomes an OWL datatype restriction xsd:string[pattern
    "..."]. XSD regular expressions are implicitly anchored and treat ^ and $
    as literal characters, while SHACL (SPARQL regex) and JSON Schema need the
    anchors, so one pattern cannot be right in all three: under OWL the value
    "conflicting" fails "^(confirmed|conflicting|unverified)$" and HermiT
    declares valid data inconsistent. As with other checks OWL cannot carry
    faithfully, the pattern stays in SHACL (sh:pattern) and JSON Schema; the
    OWL range falls back to the base datatype."""
    XSD_PATTERN = XSD.pattern
    n = 0
    for dt in list(g.subjects(OWL.onDatatype, None)):
        if not isinstance(dt, BNode):
            continue
        lst = g.value(dt, OWL.withRestrictions)
        facets = list(Collection(g, lst)) if lst is not None else []
        if not facets or not all((f, XSD_PATTERN, None) in g for f in facets):
            continue
        base = g.value(dt, OWL.onDatatype)
        for s, p in list(g.subject_predicates(dt)):
            g.remove((s, p, dt))
            g.add((s, p, base))
        _purge_node(g, dt)
        n += 1
    print(f"DL: replaced {n} xsd:pattern datatype restriction(s) by their base datatype (SHACL keeps the pattern)")


def add_external_class_domains(g: Graph, sv: SchemaView) -> None:
    """HeritageGraph properties used only by classes whose IRI is an external
    term (Assertion = crminf:I2_Belief, Person = crm:E21_Person, TimeSpan =
    crm:E52_Time-Span, ...) end up attached to no class in the OWL: gen-owl
    puts the restrictions on the external class, and repair_dl_profile (i)
    rightly removes axioms on terms HeritageGraph does not own. Restore the
    lost class context as rdfs:domain on the HeritageGraph property (an axiom
    about our own term), derived from the YAML: the class that uses it, or the
    union of the classes when several do (reduced to the most general ones), for
    every property used by at least one external-IRI class. Properties used only
    by HeritageGraph classes keep their restrictions there and get no domain."""
    users: dict[URIRef, set[URIRef]] = {}
    for cn, c in sv.all_classes().items():
        if c.abstract or c.mixin:
            continue
        cls = URIRef(sv.get_uri(c, expand=True))
        for sn in sv.class_slots(cn):
            su = sv.induced_slot(sn, cn).slot_uri
            if su:
                users.setdefault(URIRef(sv.expand_curie(str(su))), set()).add(cls)
    n = 0
    for prop, classes in sorted(users.items()):
        if (not str(prop).startswith(HG_NS) or (prop, RDF.type, None) not in g
                or (prop, OWL.deprecated, None) in g or (prop, RDFS.domain, None) in g):
            continue
        if all(str(c).startswith(HG_NS) for c in classes):
            continue  # restrictions on HeritageGraph classes carry the context
        # A property with an inverse is entailed for every object of the
        # inverse, whatever class declares the slot: its domain is the
        # inverse's range (e.g. hasAssertion, inverse of assertsAbout, has
        # domain AssertionSubject), never the union of declaring classes.
        inverses = set(g.objects(prop, OWL.inverseOf)) | set(g.subjects(OWL.inverseOf, prop))
        if inverses:
            rngs = {r for i in inverses for r in g.objects(i, RDFS.range)}
            if len(rngs) == 1:
                g.add((prop, RDFS.domain, next(iter(rngs))))
                n += 1
            continue
        # minimal covering set: drop a user class whose superclass also uses it
        names = {URIRef(sv.get_uri(sv.get_class(cn), expand=True)): cn
                 for cn in sv.all_classes()}
        classes = {c for c in classes
                   if not any(names.get(o) in sv.class_ancestors(names[c], reflexive=False)
                              for o in classes if o != c)}
        if len(classes) == 1:
            g.add((prop, RDFS.domain, next(iter(classes))))
        else:
            expr, head = BNode(), BNode()
            Collection(g, head, sorted(classes))
            g.add((expr, RDF.type, OWL.Class))
            g.add((expr, OWL.unionOf, head))
            g.add((prop, RDFS.domain, expr))
        n += 1
    print(f"asserted rdfs:domain on {n} propert(ies) used by external-IRI classes")


def drop_vacuous_min_cardinality(g: Graph) -> None:
    """gen-owl emits `C ⊑ ≥0 p` for every optional slot. A minimum of 0 holds
    for every individual, so the axiom constrains nothing; it only inflates
    the axiom count. Remove each restriction whose sole constraint is
    owl:minCardinality 0 (or the qualified form). Non-zero minimums and every
    maximum are left untouched."""
    structural = {RDF.type, OWL.onProperty, OWL.onClass, OWL.onDataRange}
    n = 0
    for pred in (OWL.minCardinality, OWL.minQualifiedCardinality):
        for r, v in list(g.subject_objects(pred)):
            if not isinstance(r, BNode) or int(str(v)) != 0:
                continue
            if any(p not in structural | {pred} for p in g.predicates(r)):
                continue  # restriction carries another constraint: keep it
            _purge_node(g, r)
            n += 1
    print(f"removed {n} vacuous owl:minCardinality 0 restriction(s)")


def _purge_node(g: Graph, node) -> None:
    """Remove every triple whose subject is `node`, recursing into blank-node
    objects (restriction bodies, RDF lists), plus links pointing at it."""
    for s, p in list(g.subject_predicates(node)):
        g.remove((s, p, node))
    for p, o in list(g.predicate_objects(node)):
        g.remove((node, p, o))
        if isinstance(o, BNode):
            _purge_node(g, o)


def repair_dl_profile(g: Graph, sv: SchemaView) -> None:
    """OWL 2 DL compliance repair (alpha.6).

    gen-owl output is OWL Full (robot validate-profile: IllegalPunning,
    reserved-vocabulary property IRIs, undeclared entities, non-OWL2
    datatypes in logical axioms), so strict reasoners reject the file and
    OWLAPI-based ones silently repair it before reasoning. Every step below
    removes or declares an OWL-Full construct; none touches the predicates
    used by instance data or the SHACL layer, which keeps the constraints
    that OWL cannot legally carry (xsd:date/geo:wktLiteral datatypes, the
    conditional current-location rule, name cardinalities on rdfs:label).
    """
    # (a) gen-owl --no-use-native-uris emits skos:exactMatch <class_uri> on
    # every element whose IRI *is* its class_uri/slot_uri -> self-loops that
    # overstate the ontology's external alignment ~3x. Drop them.
    n = 0
    for p in (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
              SKOS.narrowMatch, SKOS.relatedMatch):
        for s, o in list(g.subject_objects(p)):
            if s == o:
                g.remove((s, p, o)); n += 1
    print(f"DL: removed {n} self-referential mapping triple(s)")

    # (a2) for a class whose IRI is an external class_uri (crm:E21_Person, ...),
    # gen-owl additionally emits skos:exactMatch <heritageGraph:{ClassName}>, the
    # "native" IRI it would have minted. Those IRIs are declared nowhere, so the
    # mappings point at nothing. Drop SKOS mappings to undeclared IRIs in the
    # HeritageGraph namespace.
    hg_ns = HG_NS
    n = 0
    for p in (SKOS.exactMatch, SKOS.closeMatch, SKOS.broadMatch,
              SKOS.narrowMatch, SKOS.relatedMatch):
        for s, o in list(g.subject_objects(p)):
            if (isinstance(o, URIRef) and str(o).startswith(hg_ns)
                    and (o, RDF.type, None) not in g):
                g.remove((s, p, o)); n += 1
    print(f"DL: removed {n} mapping triple(s) to undeclared HeritageGraph IRIs")

    # (b) rdfs:label is built-in annotation vocabulary; the `name` slot
    # (slot_uri rdfs:label) makes gen-owl redeclare it as a datatype property,
    # punning every labelled entity into an individual. Remove the
    # redeclaration and the class restrictions on it; instance data keeps
    # rdfs:label and SHACL keeps the name constraints.
    n = 0
    for r in list(g.subjects(OWL.onProperty, RDFS.label)):
        _purge_node(g, r); n += 1
    for p, o in list(g.predicate_objects(RDFS.label)):
        g.remove((RDFS.label, p, o))
    print(f"DL: reverted rdfs:label to built-in annotation ({n} restriction(s) dropped)")

    # (c) xsd:date and geo:wktLiteral are outside the OWL 2 datatype map, so
    # any logical axiom using them is illegal (HermiT CLI:
    # UnsupportedDatatypeException). Drop those axioms - including gen-owl's
    # wrong DatatypeDefinition(geo:wktLiteral := xsd:string) - and leave the
    # exact datatype checks to SHACL (sh:datatype), where they are legal.
    n_rng, n_res = 0, 0
    for dt in (XSD.date, GEO.wktLiteral):
        for prop in list(g.subjects(RDFS.range, dt)):
            g.remove((prop, RDFS.range, dt)); n_rng += 1
        for pred in (OWL.allValuesFrom, OWL.someValuesFrom, OWL.onDataRange):
            for r in list(g.subjects(pred, dt)):
                _purge_node(g, r); n_res += 1
    for p, o in list(g.predicate_objects(GEO.wktLiteral)):
        g.remove((GEO.wktLiteral, p, o))
    print(f"DL: removed {n_rng} range(s) + {n_res} restriction(s) on non-OWL2 "
          f"datatypes (SHACL keeps the checks)")

    # (d) declare used-but-undeclared vocabulary: SKOS classes for the
    # published concept schemes, and every SKOS/DCTERMS predicate used purely
    # as annotation.
    g.add((SKOS.Concept, RDF.type, OWL.Class))
    g.add((SKOS.ConceptScheme, RDF.type, OWL.Class))
    n = 0
    for pred in {p for _, p, _ in g}:
        if (str(pred).startswith(str(SKOS)) or pred in (DCTERMS.title, DCTERMS.description)) \
                and (pred, RDF.type, None) not in g:
            g.add((pred, RDF.type, OWL.AnnotationProperty)); n += 1
    print(f"DL: declared skos:Concept/ConceptScheme + {n} annotation propert(ies)")

    # (e) property axioms referencing undeclared externals (e.g.
    # SubObjectPropertyOf bridges to crm:P2_has_type): declare the undeclared
    # side with the declared side's type (default owl:ObjectProperty).
    n = 0
    prop_types = (OWL.ObjectProperty, OWL.DatatypeProperty)
    for pred in (RDFS.subPropertyOf, OWL.inverseOf):
        for s, o in list(g.subject_objects(pred)):
            if not isinstance(o, URIRef):
                continue
            if (s, RDF.type, OWL.AnnotationProperty) in g \
                    or (o, RDF.type, OWL.AnnotationProperty) in g:
                continue
            stypes = {t for t in g.objects(s, RDF.type) if t in prop_types}
            otypes = {t for t in g.objects(o, RDF.type) if t in prop_types}
            if stypes and not otypes:
                g.add((o, RDF.type, next(iter(stypes)))); n += 1
            elif otypes and not stypes:
                g.add((s, RDF.type, next(iter(otypes)))); n += 1
            elif not stypes and not otypes:
                g.add((s, RDF.type, OWL.ObjectProperty))
                g.add((o, RDF.type, OWL.ObjectProperty)); n += 2
    print(f"DL: declared {n} propert(ies) referenced by property axioms")

    # (e2) LinkML default_range: string declares rangeless slots as datatype
    # properties even when every logical axiom uses them as object properties
    # (has_type -> crm:P2_has_type, which only exists as the parent of the
    # object-property typing slots; was_influenced_by -> prov:wasInfluencedBy,
    # whose range is a PROV class union). Retype them and drop the spurious
    # xsd:string range so the declaration matches the axioms (and CIDOC-CRM/
    # PROV-O, where both are object properties).
    classes = set(g.subjects(RDF.type, OWL.Class))
    n = 0
    for p in list(g.subjects(RDF.type, OWL.DatatypeProperty)):
        obj_evidence = any(
            o in classes or (o, OWL.unionOf, None) in g
            for o in g.objects(p, RDFS.range)
        ) or any(
            (s, RDF.type, OWL.ObjectProperty) in g
            for s in g.subjects(RDFS.subPropertyOf, p)
        )
        data_evidence = any(
            isinstance(o, URIRef) and str(o).startswith(str(XSD))
            for r in g.subjects(OWL.onProperty, p)
            for o in g.objects(r, OWL.allValuesFrom)
        )
        if obj_evidence and not data_evidence:
            g.remove((p, RDF.type, OWL.DatatypeProperty))
            g.add((p, RDF.type, OWL.ObjectProperty))
            for o in list(g.objects(p, RDFS.range)):
                if isinstance(o, URIRef) and str(o).startswith(str(XSD)):
                    g.remove((p, RDFS.range, o))
            n += 1
    print(f"DL: retyped {n} propert(ies) with object-only usage to owl:ObjectProperty")

    # (f) gen-owl translates the ArchitecturalStructure location rule into a
    # GCI over IRIs that exist nowhere else (heritageGraph:has_current_location,
    # heritageGraph:existence_status instead of the slot_uris) AND weakens the
    # precondition from 'status is Extant/PartiallyExtant' to 'any status' -
    # an axiom the schema does not assert. Remove it; the SHACL shapes carry
    # the actual conditional rule.
    n = 0
    for s in list(g.subjects(OWL.intersectionOf, None)):
        if isinstance(s, BNode) and (s, RDFS.subClassOf, None) in g:
            _purge_node(g, s); n += 1
    print(f"DL: removed {n} mistranslated anonymous GCI(s)")

    # (g) one resolvable identity: gen-owl names the ontology node after the
    # file (<.../schema.owl.ttl>) and asserts owl:ontologyIRI/owl:versionIRI
    # as string literals (owl:ontologyIRI is not even OWL vocabulary).
    # Re-seat everything on the canonical IRI with a real owl:versionIRI.
    version = str(sv.schema.version)
    for ont in list(g.subjects(RDF.type, OWL.Ontology)):
        g.remove((ont, URIRef(str(OWL) + "ontologyIRI"), None))
        g.remove((ont, OWL.versionIRI, None))
        if ont != ONTOLOGY_IRI:
            for p, o in list(g.predicate_objects(ont)):
                g.remove((ont, p, o))
                g.add((ONTOLOGY_IRI, p, o))
    g.add((ONTOLOGY_IRI, RDF.type, OWL.Ontology))
    g.add((ONTOLOGY_IRI, OWL.versionIRI,
           URIRef(f"{ONTOLOGY_IRI}/{version}")))
    for pred in (DCTERMS.title, DCTERMS.description):
        if (pred, RDF.type, None) not in g:
            g.add((pred, RDF.type, OWL.AnnotationProperty))
    g.add((ONTOLOGY_IRI, DCTERMS.title, Literal("HeritageGraph Ontology")))
    if sv.schema.description:
        g.add((ONTOLOGY_IRI, DCTERMS.description, Literal(str(sv.schema.description))))
    print(f"DL: ontology IRI -> {ONTOLOGY_IRI} (versionIRI .../{version})")

    # (h) gen-owl renders a numeric range with minimum_value/maximum_value as
    # base ∩ xsd:integer[>= min] ∩ xsd:integer[<= max]. For a non-integer base
    # (confidence_score: decimal) that intersection admits only the integers
    # 0 and 1, and for xsd:float it is empty (float and integer value spaces are
    # disjoint), so every real value made the ABox inconsistent. Rewrite each
    # such intersection into ONE datatype restriction on the base type, with
    # the facet values re-typed to it: base[>= min, <= max].
    n = 0
    for dt in list(g.subjects(OWL.intersectionOf, None)):
        if not isinstance(dt, BNode) or (dt, RDF.type, RDFS.Datatype) not in g:
            continue
        members = list(Collection(g, g.value(dt, OWL.intersectionOf)))
        bases = [m for m in members if isinstance(m, URIRef)]
        faceted = [m for m in members
                   if isinstance(m, BNode) and (m, OWL.onDatatype, None) in g]
        if len(bases) != 1 or len(bases) + len(faceted) != len(members):
            continue
        base = bases[0]
        restrictions = []
        for m in faceted:
            for r in Collection(g, g.value(m, OWL.withRestrictions)):
                for facet, value in g.predicate_objects(r):
                    node = BNode()
                    g.add((node, facet, Literal(str(value), datatype=base)))
                    restrictions.append(node)
        new = BNode()
        head = BNode()
        Collection(g, head, restrictions)
        g.add((new, RDF.type, RDFS.Datatype))
        g.add((new, OWL.onDatatype, base))
        g.add((new, OWL.withRestrictions, head))
        for s, p in list(g.subject_predicates(dt)):
            g.remove((s, p, dt))
            g.add((s, p, new))
        _purge_node(g, dt)
        n += 1
    print(f"DL: collapsed {n} faceted datatype intersection(s) into single-datatype restrictions")

    # (i) No logical axioms about terms HeritageGraph does not own. gen-owl
    # attaches every slot's range and every class's restrictions and parents to
    # the IRI the slot or class reuses, so the core asserted global ranges on
    # CIDOC-CRM properties (crm:P46_is_composed_of rdfs:range
    # ArchitecturalElement), cardinality restrictions on crm:E21_Person, PROV-O
    # classes and crminf:I2_Belief, and crm:E6_Destruction ⊑ HistoricalEvent.
    # Asserted in a reused ontology, those axioms redefine the external terms
    # for every dataset that uses them. Remove every logical axiom whose subject
    # is an external IRI; the constraints stay where they belong: as
    # restrictions on HeritageGraph classes (which gen-owl also emits) and in
    # the SHACL shapes, which target the reused classes. owl:inverseOf between
    # a HeritageGraph and an external property is symmetric and defines the
    # HeritageGraph property, so it is re-stated with the HeritageGraph
    # property as subject. Declarations and annotations are kept.
    #
    # Two justified exceptions. First, owl:inverseOf between two external
    # properties that the owning vocabulary itself declares inverse
    # (prov:generated / prov:wasGeneratedBy, asserted by PROV-O; the YAML
    # declares the pair as slot inverses). Second, rdfs:subClassOf between two
    # named external classes. These are crm:E21_Person ⊑ crm:E39_Actor (CIDOC-CRM's own axiom,
    # restated so the core classifies without importing CRM) and the
    # HeritageGraph CRM→PROV-O alignment of the reused classes (crm:E39_Actor ⊑
    # prov:Agent, crm:E12_Production ⊑ prov:Activity, …, crminf:I2_Belief ⊑
    # prov:Entity). They give no external class a HeritageGraph superclass,
    # classify consistently with CIDOC-CRM, CRMinf, and PROV-O merged
    # (reasoning_extras.py), and the provenance layer's SHACL constraints
    # (e.g. prov:wasAttributedTo values are prov:Agent) depend on them.
    logical = (RDFS.domain, RDFS.range, RDFS.subClassOf, RDFS.subPropertyOf,
               OWL.equivalentClass, OWL.equivalentProperty, OWL.inverseOf,
               OWL.disjointWith, OWL.propertyChainAxiom)
    n = 0
    for pred in logical:
        for s, o in list(g.subject_objects(pred)):
            if not isinstance(s, URIRef) or str(s).startswith(HG_NS):
                continue
            if (pred in (RDFS.subClassOf, OWL.inverseOf) and isinstance(o, URIRef)
                    and not str(o).startswith(HG_NS)):
                continue  # named external → external: the exceptions above
            g.remove((s, pred, o))
            n += 1
            if pred == OWL.inverseOf and isinstance(o, URIRef) and str(o).startswith(HG_NS):
                g.add((o, OWL.inverseOf, s))
            elif isinstance(o, BNode) and not any(g.subjects(None, o)):
                _purge_node(g, o)
    print(f"DL: removed {n} logical axiom(s) whose subject is an external term")


def finalize_shacl(sv: SchemaView) -> None:
    g = Graph()
    g.parse(SHACL_OUT, format="turtle")
    # (1) drop identifier min-count: in RDF the node IRI is the identifier
    n = 0
    for ps in list(g.subjects(SH.path, DCTERMS.identifier)):
        for c in list(g.objects(ps, SH.minCount)):
            g.remove((ps, SH.minCount, c)); n += 1
    print(f"removed {n} identifier minCount constraints")
    # (2) sh:class <union class> -> sh:or over member classes
    unions = {}
    for cn, c in sv.all_classes().items():
        if c.union_of:
            u = uri_for(sv, str(c.class_uri or f"heritageGraph:{cn}"))
            members = []
            for m in c.union_of:
                mc = sv.get_class(m)
                members.append(uri_for(sv, str(mc.class_uri or f"heritageGraph:{m}")))
            unions[u] = members
    n = 0
    for ps, cls in list(g.subject_objects(SH["class"])):
        if cls in unions:
            g.remove((ps, SH["class"], cls))
            alts = []
            for m in unions[cls]:
                node = BNode()
                g.add((node, SH["class"], m))
                alts.append(node)
            head = BNode()
            Collection(g, head, alts)
            g.add((ps, SH["or"], head))
            n += 1
    print(f"rewrote {n} union sh:class constraints as sh:or")
    # (3) open the closed shapes (documented relaxation for polymorphic vocab);
    # sh:ignoredProperties is only legal alongside sh:closed, so remove both.
    n = 0
    for s, o in list(g.subject_objects(SH.closed)):
        g.remove((s, SH.closed, o)); n += 1
    for s, o in list(g.subject_objects(SH.ignoredProperties)):
        g.remove((s, SH.ignoredProperties, o))
    print(f"opened {n} closed shapes (and dropped their ignoredProperties lists)")
    # (4) enum-ranged slots: gen-shacl lists permissible values as string
    # literals in sh:in, while the OWL layer types these slots as object
    # properties ranging over enumeration classes of named individuals, so data
    # satisfying the shapes punned the property (OWL 2 DL violation). Rewrite
    # each sh:in list to the enumeration individuals' IRIs: the declared
    # meaning where present, else the <Enum#Value> IRI gen-owl mints (the same
    # resources finalize_owl publishes as SKOS concepts).
    owl_g = Graph()
    owl_g.parse(OWL_OUT, format="turtle")
    by_emitted = {}
    for en, e in sv.all_enums().items():
        emitted, iri = set(), {}
        for vn, pv in (e.permissible_values or {}).items():
            ind = (uri_for(sv, str(pv.meaning)) if pv.meaning
                   else URIRef(f"{HG_NS}{en}#{vn}"))
            if (ind, RDF.type, OWL.NamedIndividual) not in owl_g:
                sys.exit(f"enum individual missing from OWL: {en}.{vn} -> {ind}")
            key = ind if pv.meaning else Literal(vn)
            emitted.add(key)
            iri[key] = ind
        by_emitted[frozenset(emitted)] = (en, iri)
    n = 0
    in_lists = [(ps, lst, list(Collection(g, lst)))
                for ps, lst in g.subject_objects(SH["in"])]
    for ps, lst, members in in_lists:
        match = by_emitted.get(frozenset(members))
        if match is None:
            if any(isinstance(m, Literal) for m in members):
                sys.exit(f"sh:in over literals matches no enum: {members}")
            continue
        _, iri = match
        g.remove((ps, SH["in"], lst))
        _purge_node(g, lst)
        head = BNode()
        Collection(g, head, [iri[m] for m in members])
        g.add((ps, SH["in"], head))
        n += 1
    print(f"rewrote {n} enum sh:in lists from literals to individual IRIs")
    add_usage_names(g, sv)
    scope_shapes(g, sv)
    g.serialize(destination=SHACL_OUT, format="turtle")
    print(f"finalized {SHACL_OUT.name} ({len(g)} triples)")


def add_usage_names(g: Graph, sv: SchemaView) -> None:
    """HeritageGraph's usage wording for reused external terms lives in the
    shapes, not on the external IRIs (whose OWL labels are the owners'):
    sh:name on each property shape whose path is an external property (the
    slot's title or humanized name, e.g. "Depicts deity" for crm:P62_depicts;
    sh:description already carries the slot description), and on each node
    shape that targets an external class (the LinkML class name, e.g.
    "Technique" for crm:E29_Design_or_Procedure)."""
    by_uri: dict[URIRef, list] = {}
    for sn, sl in sv.all_slots().items():
        if sl.slot_uri:
            u = uri_for(sv, str(sl.slot_uri))
            if u is not None and not str(u).startswith(HG_NS):
                by_uri.setdefault(u, []).append(sl)
    n_prop, unresolved = 0, []
    for ps, path in list(g.subject_objects(SH.path)):
        if path not in by_uri or (ps, SH.name, None) in g:
            continue
        cands = by_uri[path]
        if len(cands) > 1:
            desc = str(g.value(ps, SH.description) or "")
            cands = [c for c in cands if str(c.description or "") == desc] or cands
        if len({c.name for c in cands}) != 1:
            unresolved.append(str(path)); continue
        sl = cands[0]
        g.add((ps, SH.name, Literal(str(sl.title) if sl.title else humanize_name(sl.name), lang="en")))
        n_prop += 1
    n_node = 0
    for cn, c in sv.all_classes().items():
        u = uri_for(sv, str(c.class_uri)) if c.class_uri else None
        if u is None or str(u).startswith(HG_NS):
            continue
        for shape in set(g.subjects(SH.targetClass, u)):
            if (shape, SH.name, None) not in g:
                g.add((shape, SH.name, Literal(humanize_name(cn), lang="en")))
                n_node += 1
    print(f"usage names: sh:name on {n_prop} property shape(s) with an external path "
          f"and {n_node} node shape(s) targeting an external class"
          + (f"; unresolved: {sorted(set(unresolved))}" if unresolved else ""))


def scope_shapes(g: Graph, sv: SchemaView) -> None:
    """gen-shacl names each node shape after its class's IRI, so classes whose IRI
    is an external term (crm:E21_Person, prov:Entity, ...) were typed sh:NodeShape
    in the shapes graph, and the shapes of the abstract PROV/CRM superclasses
    targeted every prov:Entity, prov:Activity, prov:Agent and crm:E74_Group in any
    graph validated with HeritageGraph's shapes, imposing HeritageGraph's rules
    (e.g. one dcterms:identifier of type xsd:anyURI) on third-party data.
    (1) Drop the node shapes of abstract or mixin classes with an external IRI:
        their property shapes are repeated in every concrete subclass's shape.
    (2) Rename the remaining externally named shapes to hg:<ClassName>Shape,
        keeping their explicit sh:targetClass (HeritageGraph uses crm:E21_Person
        etc. as its own Person class, so those targets stay)."""
    # Only the shape node's own triples move or go: the same IRI is also the
    # object of sh:class / sh:targetClass constraints elsewhere, which must stay.
    def rename(old: URIRef, new: URIRef) -> None:
        for p_, o_ in list(g.predicate_objects(old)):
            g.remove((old, p_, o_)); g.add((new, p_, o_))

    def drop(shape: URIRef) -> None:
        def purge_out(node) -> None:
            for p_, o_ in list(g.predicate_objects(node)):
                g.remove((node, p_, o_))
                if isinstance(o_, BNode) and not any(g.subjects(None, o_)):
                    purge_out(o_)
        purge_out(shape)
    n_drop = n_ren = 0
    for cn, c in sv.all_classes().items():
        cls = URIRef(sv.get_uri(c, expand=True))
        if str(cls).startswith(HG_NS) or (cls, RDF.type, SH.NodeShape) not in g:
            continue
        if c.abstract or c.mixin:
            drop(cls)
            n_drop += 1
        else:
            rename(cls, URIRef(f"{HG_NS}{cn}Shape"))
            n_ren += 1
    print(f"shapes: dropped {n_drop} externally named shape(s) of abstract/mixin classes, "
          f"renamed {n_ren} to hg:<Class>Shape")


def run_pyshacl() -> None:
    from pyshacl import validate
    # TOOL WORKAROUND: pyshacl (<=0.31) degrades pathologically (minutes ->
    # hours) when the mixed-in ont_graph contains owl:NamedIndividual
    # declarations. The declarations are correct OWL 2 DL (individuals used in
    # owl:oneOf must be declared) and stay in the release artifact; they are
    # stripped only from this in-memory validation copy. The PV individuals
    # keep their enum-class typing, so validation semantics are unchanged.
    ont = Graph()
    ont.parse(OWL_OUT, format="turtle")
    for s in list(ont.subjects(RDF.type, OWL.NamedIndividual)):
        ont.remove((s, RDF.type, OWL.NamedIndividual))
    conforms, _, text = validate(
        data_graph=str(ABOX), shacl_graph=str(SHACL_OUT),
        ont_graph=ont, inference="none")
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "shacl_alpha5_report.txt").write_text(
        f"pyshacl {date.today().isoformat()}\nconforms: {conforms}\n\n{text}\n",
        encoding="utf-8")
    print(f"SHACL conforms: {conforms}")
    if not conforms:
        head = "\n".join(l for l in text.splitlines() if "Violation" in l or "Path" in l)[:2000]
        sys.exit("SHACL NON-CONFORMANT:\n" + head)


def stamp_provenance() -> None:
    """Prepend a generation header carrying the SHA-256 of the source YAML so
    YAML<->TTL sync is mechanically checkable (scripts/check_yaml_ttl_sync.py)."""
    import hashlib
    digest = hashlib.sha256(SCHEMA.read_bytes()).hexdigest()
    for out in (OWL_OUT, SHACL_OUT):
        body = out.read_text(encoding="utf-8")
        header = (
            f"# GENERATED from {SCHEMA.name} by scripts/finalize_alpha5_artifacts.py"
            f" on {date.today().isoformat()}.\n"
            f"# DO NOT EDIT THIS FILE - edit the YAML and regenerate.\n"
            f"# source-sha256: {digest}\n")
        out.write_text(header + body, encoding="utf-8")
    print(f"stamped source-sha256 {digest[:12]}... into {OWL_OUT.name} and {SHACL_OUT.name}")


def sync_published() -> None:
    g = Graph()
    g.parse(OWL_OUT, format="turtle")
    docs = ROOT / "docs"
    g.serialize(destination=docs / "ontology.ttl", format="turtle")
    g.serialize(destination=docs / "ontology.owl", format="xml")
    g.serialize(destination=docs / "ontology.nt", format="nt", encoding="utf-8")
    g.serialize(destination=docs / "ontology.jsonld", format="json-ld")
    # RDF/XML copy classified by evaluation/run_hermit.py
    g.serialize(destination=ROOT / "ontology" / "review.owl", format="xml")
    print("synced docs/ontology.{ttl,owl,nt,jsonld} and ontology/review.owl")
    # immutable per-release copy served at the version IRI
    subprocess.run([sys.executable, str(ROOT / "scripts" / "publish_release.py"),
                    str(docs)], check=True)
    # per-enumeration pages with value anchors (targets of enum IRIs)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "gen_enum_pages.py"),
                    str(docs)], check=True)


def gen_json_schema() -> None:
    out = ROOT / "ontology" / "HeritageGraph.schema.json"
    # generated from the serialization wrapper (core schema + Container/Metadata);
    # $id and title stay those of the core schema so the published JSON Schema
    # keeps its identity across 1.0.x -> 1.1.0 (its $defs are unchanged).
    import json
    import yaml
    res = subprocess.run(
        ["linkml", "generate", "json-schema", str(CONTAINER_SCHEMA)],
        cwd=ROOT, check=True, capture_output=True, text=True)
    js = json.loads(res.stdout)
    core = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    js["$id"], js["title"] = core["id"], core["name"]
    out.write_text(json.dumps(js, indent=4) + "\n\n", encoding="utf-8")  # gen-json-schema layout
    print(f"generated {out.name}")


def main() -> int:
    sv = SchemaView(str(SCHEMA))
    # PV FIX (alpha.6): without --default-permissible-value-type, gen-owl types
    # every permissible value as owl:Class (values became subclasses of their
    # enum). Enum values are individuals, not classes; owl:NamedIndividual
    # matches the documented modelling (enumeration classes over named
    # individuals) and yields owl:oneOf enumeration classes.
    gen("owl", OWL_OUT, [
        "--no-use-native-uris",
        "--default-permissible-value-type",
        "http://www.w3.org/2002/07/owl#NamedIndividual",
    ])
    gen("shacl", SHACL_OUT)
    gen_json_schema()
    finalize_owl(sv)
    finalize_shacl(sv)
    run_pyshacl()
    stamp_provenance()
    sync_published()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
