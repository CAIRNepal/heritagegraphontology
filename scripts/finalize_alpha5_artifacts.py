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

    # --- owl:deprecated for enumeration values using the deprecated metaslot ---
    n_pv = 0
    for en, e in sv.all_enums().items():
        for vn, pv in (e.permissible_values or {}).items():
            if not pv.deprecated:
                continue
            ind = uri_for(sv, str(pv.meaning)) if pv.meaning else URIRef(f"{HG_NS}{en}#{vn}")
            g.add((ind, OWL.deprecated, Literal(True)))
            g.add((ind, SKOS.editorialNote, Literal(f"Deprecated in HeritageGraph 1.1.0: {pv.deprecated}", lang="en")))
            # ROBOT / OBO convention: a deprecated term's label starts with "obsolete"
            for lp in (RDFS.label, SKOS.prefLabel, DCTERMS.title):
                for old in list(g.objects(ind, lp)):
                    if not str(old).startswith("obsolete "):
                        text = str(old)
                        if " " not in text:  # a raw value name (SanGuthi): humanize it first
                            text = humanize_name(text)
                        g.remove((ind, lp, old))
                        g.add((ind, lp, Literal(f"obsolete {text}", lang=getattr(old, "language", None) or "en")))
            repl = pv.deprecated_element_has_exact_replacement
            if repl and repl in sv.all_classes():
                c = sv.get_class(repl)
                g.add((ind, DCTERMS.isReplacedBy, uri_for(sv, str(c.class_uri or f"heritageGraph:{repl}"))))
                g.add((DCTERMS.isReplacedBy, RDF.type, OWL.AnnotationProperty))
            elif repl and repl in (e.permissible_values or {}):
                r = e.permissible_values[repl]  # another value of the same enumeration
                g.add((ind, DCTERMS.isReplacedBy,
                       uri_for(sv, str(r.meaning)) if r.meaning else URIRef(f"{HG_NS}{en}#{repl}")))
                g.add((DCTERMS.isReplacedBy, RDF.type, OWL.AnnotationProperty))
            n_pv += 1
    print(f"marked {n_pv} enumeration value(s) owl:deprecated")

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
    # class titles likewise (e.g. InformationObject, whose name is CRM E73's label)
    n_ctitle = 0
    for cn, cl in sv.all_classes().items():
        if cl.title:
            cls = uri_for(sv, str(cl.class_uri or f"heritageGraph:{cn}"))
            if str(cls).startswith(HG_NS) and (cls, RDF.type, OWL.Class) in g:
                g.remove((cls, RDFS.label, None))
                g.add((cls, RDFS.label, Literal(str(cl.title), lang="en")))
                n_ctitle += 1
    print(f"labelled {n_ctitle} class(es) from their title")

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
        (DCTERMS.modified, Literal(_modified_date(header), datatype=XSD.date)),
        (DCTERMS.source, URIRef("https://github.com/CAIRNepal/heritagegraphontology")),
        (DCTERMS.bibliographicCitation, Literal(citation)),
        (DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")),
        *[(DCTERMS.creator, _creator_node(g, c)) for c in creators],
        (DCTERMS.publisher, Literal(header.get("dcterms:publisher", "CAIR-Nepal"))),
        (BIBO.status, Literal(header.get("bibo:status", "Published"))),
        (VANN.preferredNamespacePrefix, Literal(header.get("vann:preferredNamespacePrefix", "hg"))),
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
    relax_text_ranges(g)
    relax_reused_max_cardinality(g)
    add_property_chains(g, sv)
    add_crm_superclasses(g, sv)
    drop_reused_value_restrictions(g)
    add_disjoint_kinds(g, sv)
    add_enumeration_axioms(g)
    add_official_inverses(g)
    drop_range_unions_and_double_grounding(g)
    # schema build directives, not ontology content
    for d in ("owl_property_chain", "lexical_form", "crm_superclass", "disjoint_kind"):
        g.remove((None, URIRef(HG_NS + d), None))
    add_external_class_domains(g, sv)
    add_domain_includes(g, sv)
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
        # range-naming classes whose union is dropped on purpose (it lives in SHACL)
        if c.union_of and cn not in ("AssertionSubject", "TenureEvent"):
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
    polish_owl(g, sv)
    bind_hg(g)
    g.serialize(destination=OWL_OUT, format="turtle")
    print(f"finalized {OWL_OUT.name} ({len(g)} triples)")
    return g


GEO = Namespace("http://www.opengis.net/ont/geosparql#")


def _modified_date(header: dict) -> str:
    """m27: a deterministic dcterms:modified, so two runs on one commit give the
    same ontology: SOURCE_DATE_EPOCH if set, else the date of the last commit
    of the YAML source, else the schema header's dcterms:modified."""
    import os
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        from datetime import datetime, timezone
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).date().isoformat()
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(SCHEMA)],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        if out:
            return out
    except (OSError, subprocess.CalledProcessError):
        pass
    return header.get("dcterms:modified", "2026-01-01")


def _orcids() -> dict:
    """Author name -> ORCID IRI, from CITATION.cff (the authoritative author list)."""
    import yaml
    path = ROOT / "CITATION.cff"
    if not path.exists():
        return {}
    cff = yaml.safe_load(path.read_text(encoding="utf-8"))
    out = {}
    for a in cff.get("authors", []):
        if a.get("orcid"):
            name = f"{a.get('given-names', '')} {a.get('family-names', '')}".strip()
            out[_ascii(name)] = a["orcid"]
    return out


def _ascii(s: str) -> str:
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c)).lower()


def _creator_node(g: Graph, name: str):
    """m23: a creator with an ORCID is its ORCID IRI, labelled with the name."""
    orcid = _orcids().get(_ascii(name))
    if not orcid:
        return Literal(name)
    node = URIRef(orcid)
    g.add((node, RDFS.label, Literal(name)))
    return node


def polish_owl(g: Graph, sv: SchemaView) -> None:
    """Annotation and serialisation hygiene, after every logical step.

    m22: YAML slot names quoted in HeritageGraph definitions and notes
    (calendar_system, tenure_holder) become the CURIE of the property
    (hg:calendarSystem), and every definition ends with a full stop.
    m23: every HeritageGraph term is rdfs:isDefinedBy the ontology.
    n5: cardinality restrictions carry xsd:nonNegativeInteger literals."""
    import re
    names = {}
    for sn, sl in sv.all_slots().items():
        if "_" in sn and sl.slot_uri:
            curie = sv.expand_curie(str(sl.slot_uri))
            for pfx, ns in g.namespace_manager.namespaces():
                if curie.startswith(str(ns)) and pfx:
                    names[sn] = f"{'hg' if str(ns) == HG_NS else pfx}:{curie[len(str(ns)):]}"
                    break
    word = re.compile(r"\b(" + "|".join(sorted(map(re.escape, names), key=len, reverse=True)) + r")\b") if names else None
    n_name = n_stop = 0
    for p in (SKOS.definition, SKOS.editorialNote, RDFS.comment):
        for s_, o in list(g.subject_objects(p)):
            if not (isinstance(s_, URIRef) and str(s_).startswith(HG_NS) and isinstance(o, Literal)):
                continue
            text = str(o)
            if word:
                new = word.sub(lambda m: names[m.group(1)], text)
                if new != text:
                    n_name += 1
                    text = new
            if p == SKOS.definition and text and not text.rstrip().endswith((".", "!", "?")):
                text = text.rstrip() + "."
                n_stop += 1
            if text != str(o):
                g.remove((s_, p, o))
                g.add((s_, p, Literal(text, lang=o.language, datatype=o.datatype)))
    n_def = 0
    for s_ in set(g.subjects(RDF.type, None)):
        if (isinstance(s_, URIRef) and str(s_).startswith(HG_NS) and s_ != ONTOLOGY_IRI
                and (s_, RDF.type, OWL.Ontology) not in g
                and any((s_, RDF.type, t) in g for t in (OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty,
                                                          OWL.AnnotationProperty, OWL.NamedIndividual))):
            if (s_, RDFS.isDefinedBy, None) not in g:
                g.add((s_, RDFS.isDefinedBy, ONTOLOGY_IRI))
                n_def += 1
    n_card = 0
    for p in (OWL.maxCardinality, OWL.minCardinality, OWL.cardinality,
              OWL.maxQualifiedCardinality, OWL.minQualifiedCardinality, OWL.qualifiedCardinality):
        for r, o in list(g.subject_objects(p)):
            if isinstance(o, Literal) and o.datatype != XSD.nonNegativeInteger:
                g.remove((r, p, o))
                g.add((r, p, Literal(str(o), datatype=XSD.nonNegativeInteger)))
                n_card += 1
    print(f"polish: {n_name} slot name(s) -> CURIEs, {n_stop} definition(s) given a full stop, "
          f"{n_def} rdfs:isDefinedBy, {n_card} cardinality literal(s) typed xsd:nonNegativeInteger")


def bind_hg(g: Graph) -> None:
    """Serialize HeritageGraph IRIs with the short prefix hg: (the LinkML
    source keeps heritageGraph: internally; IRIs are unchanged)."""
    g.namespace_manager.bind("hg", HG_NS, override=True, replace=True)
    # n6: schema.org as schema:, not rdflib's generated schema1:
    g.namespace_manager.bind("schema", "http://schema.org/", override=True, replace=True)


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
            # a standard term now carries the field (e.g. license -> dcterms:license)
            if a.slot_uri:
                repl = URIRef(cv.expand_curie(str(a.slot_uri)))
                if not str(repl).startswith(HG_NS):
                    g.add((prop, DCTERMS.isReplacedBy, repl))
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
                      and s != ONTOLOGY_IRI and not str(s).startswith("https://orcid.org/")})  # creators, not terms
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


SCHEMA_INLANGUAGE = URIRef("http://schema.org/inLanguage")
# Lexical form of string slots, declared in the schema (annotation
# lexical_form): "code" for codes and identifiers, where a language tag would
# be meaningless (they stay xsd:string); "any_literal" for a slot whose value
# may be any literal (e.g. a proposition's object "1564"^^xsd:gYear). Every
# other string slot is human-language text. Filled by load_lexical_forms.
CODE_VALUED: set[URIRef] = set()
ANY_LITERAL: set[URIRef] = set()


def load_lexical_forms(sv: SchemaView) -> None:
    CODE_VALUED.clear(); ANY_LITERAL.clear()
    for name, sl in sv.all_slots().items():
        ann = sl.annotations.get("lexical_form") if sl.annotations else None
        form = getattr(ann, "value", None)
        if sl.pattern and form != "code":
            sys.exit(f"slot {name} has a pattern but no 'lexical_form: code' annotation")
        if form is None:
            continue
        if form not in ("code", "any_literal") or not sl.slot_uri:
            sys.exit(f"slot {name}: bad lexical_form {form!r}")
        (CODE_VALUED if form == "code" else ANY_LITERAL).add(uri_for(sv, str(sl.slot_uri)))


RDF_LANGSTRING = RDF.langString


def text_valued_properties(g: Graph) -> set[URIRef]:
    """Properties whose values are human-language text: every property with
    an xsd:string range or xsd:string value restriction in the OWL, minus the
    code/identifier slots (CODE_VALUED)."""
    props = {p for p in g.subjects(RDFS.range, XSD.string)}
    props |= {g.value(r, OWL.onProperty) for r in g.subjects(OWL.allValuesFrom, XSD.string)}
    return {p for p in props if isinstance(p, URIRef) and p not in CODE_VALUED}


def relax_text_ranges(g: Graph) -> set[URIRef]:
    """B1: text in Nepali, Newari and Sanskrit is recorded with language tags
    ("Taleju"@en, "तलेजु"@ne). RDF 1.1 gives "x"@ne the datatype rdf:langString,
    which is disjoint from xsd:string, so an xsd:string range or ∀p.xsd:string
    restriction makes every tagged value an OWL inconsistency. For the
    free-text properties the OWL range becomes rdf:PlainLiteral, the OWL 2
    datatype whose values are exactly the plain strings and the
    language-tagged strings (so HermiT still rejects a note of 42); the
    SHACL shapes say the same as xsd:string or rdf:langString. Code and
    identifier properties keep xsd:string; ANY_LITERAL slots take rdfs:Literal."""
    props = text_valued_properties(g)
    n = 0
    for p in props:
        dt = RDFS.Literal if p in ANY_LITERAL else RDF.PlainLiteral
        if (p, RDFS.range, XSD.string) in g:
            g.remove((p, RDFS.range, XSD.string)); g.add((p, RDFS.range, dt)); n += 1
    for r in list(g.subjects(OWL.allValuesFrom, XSD.string)):
        p = g.value(r, OWL.onProperty)
        if p in props:
            dt = RDFS.Literal if p in ANY_LITERAL else RDF.PlainLiteral
            g.remove((r, OWL.allValuesFrom, XSD.string)); g.add((r, OWL.allValuesFrom, dt)); n += 1
    # "at most one" on a text property would forbid giving the same text in
    # a second language ("Around the city"@en, "शहर परिक्रमा"@ne): the limit
    # becomes one value per language tag, which only SHACL can state
    n_max = 0
    for r in list(g.subjects(OWL.maxCardinality, None)):
        p = g.value(r, OWL.onProperty)
        if p in props and p not in ANY_LITERAL:
            for c in list(g.subjects(RDFS.subClassOf, r)):
                g.remove((c, RDFS.subClassOf, r))
            g.remove((r, None, None)); n_max += 1
    print(f"B1: {n} xsd:string range/value restriction(s) on {len(props)} text propert(ies) "
          f"-> rdf:PlainLiteral ({len(ANY_LITERAL & props)} -> rdfs:Literal); "
          f"{n_max} max-1 on text properties -> one value per language (SHACL)")
    return props


CRM_NS = "http://www.cidoc-crm.org/cidoc-crm/"
CRM_UNQUANTIFIED = {URIRef(CRM_NS + n) for n in (
    "P81a_end_of_the_begin", "P81b_begin_of_the_end",
    "P82a_begin_of_the_begin", "P82b_end_of_the_end")}


def crm_max_one() -> dict[URIRef, bool]:
    """For every CIDOC CRM property (and its inverse), whether the official
    quantification allows at most one value per subject. CRM writes
    "(a,b:c,d)": b is the maximum number of range instances per domain
    instance (the forward property), d the maximum for the inverse.
    Properties without a quantification (P82a, P82b) are absent."""
    import re
    crm = next(vg for ns, vg, _ in _official_sources() if ns == CRM_NS)
    out: dict[URIRef, bool] = {}
    for p in set(crm.subjects(RDF.type, RDF.Property)):
        text = " ".join(str(c) for c in crm.objects(p, RDFS.comment))
        m = re.search(r"\((\d),(\d|n):(\d),(\d|n)\)", text)
        if not m:
            continue
        # an inverse property's comment quotes the forward quantification
        mirrored = "Quantification of the inverse property" in text
        out[p] = m.group(4 if mirrored else 2) == "1"
    return out


def reused_max_one_allowed(p: URIRef, crm: dict[URIRef, bool]) -> bool:
    """B2: may HeritageGraph state "at most one value" for property p?
    Its own properties: yes (a design decision). A CIDOC CRM property: only
    where CRM's own quantification is at most one. Any other external
    property (PROV-O, schema.org): no, the owner sets none."""
    if str(p).startswith(HG_NS):
        return True
    if str(p).startswith(CRM_NS):
        # P82a/P82b (the RDFS encoding of time-span bounds) have no
        # quantification; each names a single instant, so the limit stays
        if p not in crm and p not in CRM_UNQUANTIFIED:
            print(f"WARNING: no CRM quantification for {p}; keeping its limit")
        return crm.get(p, True)
    return False


def relax_reused_max_cardinality(g: Graph) -> None:
    """B2: OWL has no unique-name assumption, so a max-1 restriction on a
    property CRM declares many-valued does not reject a second value: it
    merges the two values (owl:sameAs), or makes the data inconsistent when
    they are known to differ. A note plus a citation (sourceCitation ⊑ P3),
    a procession over two places (routePlaces ⊑ P7) and any third-party CRM
    graph that uses the property as CRM allows were affected. Drop the max-1
    restrictions on reused properties that CRM (or the owner) does not
    limit; keep the ones CRM itself states, e.g. P4 has time-span (1,1)."""
    crm = crm_max_one()
    dropped, kept = {}, {}
    for r in list(g.subjects(OWL.maxCardinality, None)):
        p = g.value(r, OWL.onProperty)
        if str(p).startswith(HG_NS):
            continue
        name = str(p).rsplit("/", 1)[-1].rsplit("#", 1)[-1]
        if reused_max_one_allowed(p, crm):
            kept[name] = kept.get(name, 0) + 1
            continue
        for s in list(g.subjects(RDFS.subClassOf, r)):
            g.remove((s, RDFS.subClassOf, r))
        g.remove((r, None, None))
        dropped[name] = dropped.get(name, 0) + 1
    print(f"B2: dropped max-1 on reused properties {dict(sorted(dropped.items()))}; "
          f"kept (CRM quantification max 1) {dict(sorted(kept.items()))}")


def add_crm_superclasses(g: Graph, sv: SchemaView) -> None:
    """A class annotated crm_superclass X is stated rdfs:subClassOf X. The
    criterion (written in the paper): subClassOf whenever every instance of
    the HeritageGraph class is an instance of X (a ritual is an E7 Activity,
    a tenure an E4 Period); where that is not so for every instance (Deity),
    the class keeps only its skos:broadMatch. The subject is the
    HeritageGraph class, so the core says nothing new about the CRM class.
    Aborts if X is not a class of the official CIDOC-CRM/CRMinf snapshot."""
    official = Graph()
    for _, vg, _ in _official_sources():
        official += vg
    n, bad = 0, []
    for cn, c in sv.all_classes().items():
        ann = c.annotations.get("crm_superclass") if c.annotations else None
        if ann is None:
            continue
        sub = uri_for(sv, str(c.class_uri or f"heritageGraph:{cn}"))
        sup = uri_for(sv, str(ann.value))
        if not ((sup, RDF.type, RDFS.Class) in official or (sup, RDF.type, OWL.Class) in official):
            bad.append(f"{cn} -> {ann.value}")
            continue
        if (sup, RDF.type, OWL.Class) not in g:
            g.add((sup, RDF.type, OWL.Class))
            g.add((sup, RDFS.label, Literal(str(sup))))  # replaced by the official label
        g.add((sub, RDFS.subClassOf, sup))
        n += 1
    if bad:
        sys.exit("crm_superclass is not an official CRM/CRMinf class: " + ", ".join(bad))
    print(f"CRM grounding: {n} HeritageGraph class(es) stated rdfs:subClassOf their CRM class")


def drop_reused_value_restrictions(g: Graph) -> None:
    """M5: an owl:allValuesFrom restriction from a HeritageGraph class over a
    reused CIDOC-CRM property to a HeritageGraph class (Guthi ⊑
    ∀crm:P50i_is_current_keeper_of.ArchitecturalStructure) does not check
    data, it reclassifies it: a Guthi that keeps a murti makes the murti an
    ArchitecturalStructure, an iconographic object that depicts a person
    makes the person a Deity. Such value ranges are checks, so they stay in
    the SHACL shapes (sh:class) and leave the OWL. Restrictions over
    HeritageGraph's own properties, and datatype restrictions, are kept."""
    n, dropped = 0, []
    for r in list(g.subjects(OWL.allValuesFrom, None)):
        p, v = g.value(r, OWL.onProperty), g.value(r, OWL.allValuesFrom)
        # also a datatype range on a reused property (schema:inLanguage only
        # xsd:string): the property belongs to another vocabulary, so the
        # value check stays in the SHACL shapes
        # every value restriction on a reused property (to a HeritageGraph class, a
        # CRM class narrower than CRM's own range such as P105 only E74, or a datatype
        # such as P3 only rdf:PlainLiteral): the property belongs to another
        # vocabulary, so its value check stays in the SHACL shapes (Rule 3)
        if isinstance(p, URIRef) and not str(p).startswith(HG_NS) and isinstance(v, URIRef):
            for c in list(g.subjects(RDFS.subClassOf, r)):
                g.remove((c, RDFS.subClassOf, r))
                dropped.append(f"{str(c).rsplit('/', 1)[-1]} ∀{str(p).rsplit('/', 1)[-1]}")
            g.remove((r, None, None))
            n += 1
    print(f"M5: moved {n} value restriction(s) over reused properties to SHACL only")


# kinds whose classes are also pairwise disjoint (a deity is not a role,
# a tradition, a selection criterion, a calendar or a proposition)
PAIRWISE_KINDS = {"concept"}


def add_disjoint_kinds(g: Graph, sv: SchemaView) -> None:
    """M5: classes annotated disjoint_kind (physical, event, period, concept,
    group, information) are grouped, and the groups are stated disjoint
    (owl:AllDisjointClasses over each group, a union where it has several
    classes); the classes of a PAIRWISE_KINDS group are also pairwise
    disjoint. Subclasses inherit. Only HeritageGraph classes take part."""
    kinds: dict[str, list[URIRef]] = {}
    for cn, c in sv.all_classes().items():
        ann = c.annotations.get("disjoint_kind") if c.annotations else None
        if ann is None:
            continue
        iri = uri_for(sv, str(c.class_uri or f"heritageGraph:{cn}"))
        if not str(iri).startswith(HG_NS):
            sys.exit(f"disjoint_kind on {cn}, whose IRI is not a HeritageGraph class")
        kinds.setdefault(str(ann.value), []).append(iri)

    def all_disjoint(members: list) -> None:
        node, head = BNode(), BNode()
        Collection(g, head, members)
        g.add((node, RDF.type, OWL.AllDisjointClasses))
        g.add((node, OWL.members, head))

    groups = []
    for kind in sorted(kinds):
        cls = sorted(kinds[kind])
        if len(cls) == 1:
            groups.append(cls[0])
        else:
            u, head = BNode(), BNode()
            Collection(g, head, cls)
            g.add((u, RDF.type, OWL.Class))
            g.add((u, OWL.unionOf, head))
            groups.append(u)
        if kind in PAIRWISE_KINDS and len(cls) > 1:
            all_disjoint(cls)
    if len(groups) > 1:
        all_disjoint(groups)
    print(f"M5: {len(groups)} disjoint kinds ({', '.join(f'{k} {len(v)}' for k, v in sorted(kinds.items()))}); "
          f"pairwise within {', '.join(sorted(PAIRWISE_KINDS))}")


CRM_E55 = URIRef("http://www.cidoc-crm.org/cidoc-crm/E55_Type")
SCHEMA_DOMAIN_INCLUDES = URIRef("http://schema.org/domainIncludes")


def add_enumeration_axioms(g: Graph) -> None:
    """m1: an enumeration class (owl:oneOf over named individuals) is a set of
    types in the CIDOC-CRM sense, so it is stated rdfs:subClassOf crm:E55_Type
    (every value is a type: a condition, a style, a status), and its values are
    stated pairwise different (owl:AllDifferent): without it, no unique-name
    assumption means a structure given two values of a single-valued status
    (Destroyed and Extant) would merely make the two values the same
    individual, instead of being inconsistent."""
    official = Graph()
    for _, vg, _ in _official_sources():
        official += vg
    if (CRM_E55, RDF.type, RDFS.Class) not in official and (CRM_E55, RDF.type, OWL.Class) not in official:
        sys.exit("crm:E55_Type is not in the official CRM snapshot")
    n = 0
    for c in sorted(set(g.subjects(OWL.oneOf, None))):
        if not (isinstance(c, URIRef) and str(c).startswith(HG_NS)):
            continue
        members = list(Collection(g, g.value(c, OWL.oneOf)))
        if (CRM_E55, RDF.type, OWL.Class) not in g:
            g.add((CRM_E55, RDF.type, OWL.Class))
            g.add((CRM_E55, RDFS.label, Literal(str(CRM_E55))))  # replaced by the official label
        g.add((c, RDFS.subClassOf, CRM_E55))
        if len(members) > 1:
            node, head = BNode(), BNode()
            Collection(g, head, sorted(members))
            g.add((node, RDF.type, OWL.AllDifferent))
            g.add((node, OWL.distinctMembers, head))
        n += 1
    print(f"m1: {n} enumeration(s) stated rdfs:subClassOf crm:E55_Type, values owl:AllDifferent")


def add_official_inverses(g: Graph) -> None:
    """m2: where the core reuses both properties of a CIDOC-CRM/CRMinf inverse
    pair (P14 / P14i, P50 / P50i, ...), copy the owl:inverseOf the official
    snapshot states. The axiom is the owner's own, so the core still states
    nothing about an external term that its owner does not state."""
    official = Graph()
    for _, vg, _ in _official_sources():
        official += vg
    n = 0
    for p, q in sorted(official.subject_objects(OWL.inverseOf)):
        if ((p, RDF.type, OWL.ObjectProperty) in g and (q, RDF.type, OWL.ObjectProperty) in g
                and (p, OWL.inverseOf, q) not in g and (q, OWL.inverseOf, p) not in g):
            g.add((p, OWL.inverseOf, q))
            n += 1
    print(f"m2: copied {n} official owl:inverseOf axiom(s) between reused CRM properties")


def drop_range_unions_and_double_grounding(g: Graph) -> None:
    """(1) A class that only names the range of a property and is declared a
    subclass of a union (AssertionSubject for assertsAbout, TenureEvent for the
    tenure-bounding properties) constrains the wrong way: every subject of such a
    property is forced into one of the union's members, so an assertion about a
    class the union omits reclassifies its subject. The union stays in the SHACL
    shapes (sh:or); the OWL keeps the named class without the union axiom.
    (2) A class stated rdfs:subClassOf a CRM class does not also skos:broadMatch
    the same class (the grounding rule: subclass, or broadMatch, not both)."""
    n_u = 0
    for name in ("AssertionSubject", "TenureEvent"):
        c = URIRef(HG_NS + name)
        for o in list(g.objects(c, RDFS.subClassOf)):
            if isinstance(o, BNode) and (o, OWL.unionOf, None) in g:
                g.remove((c, RDFS.subClassOf, o))
                lst = g.value(o, OWL.unionOf)
                Collection(g, lst).clear()
                g.remove((lst, RDF.first, None)); g.remove((lst, RDF.rest, None))
                g.remove((o, None, None))
                n_u += 1
    n_b = 0
    for c, o in list(g.subject_objects(RDFS.subClassOf)):
        if isinstance(o, URIRef) and (c, SKOS.broadMatch, o) in g:
            g.remove((c, SKOS.broadMatch, o))
            n_b += 1
    print(f"dropped {n_u} range-union axiom(s) and {n_b} broadMatch(es) duplicating a subclass axiom")


def add_domain_includes(g: Graph, sv: SchemaView) -> None:
    """m3: HeritageGraph gives a property's class context as restrictions on
    the classes that use it and as SHACL shapes, not as rdfs:domain (a domain
    would retype every subject the property is used on, so reusing a property
    on another class would make the data inconsistent under the disjoint
    kinds). So that the context is still stated on the property itself, each
    HeritageGraph property without an rdfs:domain gets schema:domainIncludes
    (an annotation, no inference) for the most general classes that use it."""
    users: dict[URIRef, set[str]] = {}
    for cn, c in sv.all_classes().items():
        if c.mixin:
            continue
        for sn in sv.class_slots(cn):
            su = sv.induced_slot(sn, cn).slot_uri
            if su:
                users.setdefault(URIRef(sv.expand_curie(str(su))), set()).add(cn)
    n = 0
    for prop, names in sorted(users.items()):
        if (not str(prop).startswith(HG_NS) or (prop, RDF.type, None) not in g
                or (prop, OWL.deprecated, None) in g or (prop, RDFS.domain, None) in g):
            continue
        top = {cn for cn in names
               if not (set(sv.class_ancestors(cn, reflexive=False)) & names)}
        for cn in sorted(top):
            g.add((prop, SCHEMA_DOMAIN_INCLUDES, URIRef(sv.get_uri(sv.get_class(cn), expand=True))))
            n += 1
    if n:
        g.add((SCHEMA_DOMAIN_INCLUDES, RDF.type, OWL.AnnotationProperty))
    g.bind("schema", "http://schema.org/")
    print(f"m3: {n} schema:domainIncludes annotation(s) on properties without rdfs:domain")


def add_property_chains(g: Graph, sv: SchemaView) -> None:
    """A slot annotated owl_property_chain "p1 p2" is a shortcut for that
    path: emit SubObjectPropertyOf(ObjectPropertyChain(p1 p2) slot), so data
    written the long way (person -P98i-> Birth -P4-> time-span) also has the
    shortcut. A property with a chain axiom is non-simple and may not appear
    in a cardinality restriction (OWL 2 DL), so any such restriction on it is
    dropped; SHACL keeps the at-most-one check."""
    n = 0
    for name, sl in sv.all_slots().items():
        ann = sl.annotations.get("owl_property_chain") if sl.annotations else None
        if ann is None:
            continue
        prop = uri_for(sv, str(sl.slot_uri))
        steps = [uri_for(sv, c) for c in str(ann.value).split()]
        for st in steps:
            if (st, RDF.type, OWL.ObjectProperty) not in g:
                g.add((st, RDF.type, OWL.ObjectProperty))
                g.add((st, RDFS.label, Literal(str(st))))  # replaced by the official label
        head = BNode(); Collection(g, head, steps)
        g.add((prop, OWL.propertyChainAxiom, head))
        for r in list(g.subjects(OWL.onProperty, prop)):
            if any((r, k, None) in g for k in (OWL.maxCardinality, OWL.minCardinality,
                                                OWL.cardinality)):
                for c in list(g.subjects(RDFS.subClassOf, r)):
                    g.remove((c, RDFS.subClassOf, r))
                g.remove((r, None, None))
        n += 1
    print(f"property chains: {n} shortcut propert(ies) stated as chains of CRM paths")


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
    """HeritageGraph properties used by classes whose IRI is an external term
    (Assertion = crminf:I2_Belief, Person = crm:E21_Person, TimeSpan =
    crm:E52_Time-Span, ...) lose that class context in the OWL: gen-owl
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
        rngs = {r for i in inverses for r in g.objects(i, RDFS.range)}
        if len(rngs) == 1:
            g.add((prop, RDFS.domain, next(iter(rngs))))
            n += 1
            continue
        # minimal covering set: drop a user class whose superclass also uses it,
        # but only through subclass links that exist in the OWL (crm:E6_Destruction
        # is a HistoricalEvent in the YAML, but the OWL keeps no axiom on it)
        classes = {c for c in classes
                   if not any(o in set(g.transitive_objects(c, RDFS.subClassOf)) - {c}
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


_OFFICIAL: Graph | None = None


def _owner_states(s: URIRef, pred: URIRef, o: URIRef) -> bool:
    """Does an official vocabulary snapshot (ontology/imports/) state this
    axiom (for owl:inverseOf, in either direction)?"""
    global _OFFICIAL
    if _OFFICIAL is None:
        _OFFICIAL = Graph()
        for _, vg, _ in _official_sources():
            _OFFICIAL += vg
    return (s, pred, o) in _OFFICIAL or (pred == OWL.inverseOf and (o, pred, s) in _OFFICIAL)


PROV_NS = "http://www.w3.org/ns/prov#"
BRIDGE_OUT = ROOT / "ontology" / "HeritageGraph-crm-prov-bridge.ttl"
BRIDGE_IRI = URIRef(HG_NS + "crm-prov-bridge")
# PROV class -> the reused (external) classes the bridge places under it
BRIDGE: dict[URIRef, set[URIRef]] = {}


def write_crm_prov_bridge(sv: SchemaView) -> None:
    """The optional CRM→PROV-O alignment module. One rule, read from the
    schema: a LinkML class whose IRI is an external class (Production =
    crm:E12_Production, TimeSpan = crm:E52_Time-Span, ...) and that has the
    PROV mixin Activity, Entity or Agent (directly or inherited) gives
    <its IRI> rdfs:subClassOf prov:Activity / prov:Entity / prov:Agent. These
    are HeritageGraph's statements about other vocabularies' classes, so they
    are kept out of the core; load the module with the core when PROV-O-only
    clients should see CRM-typed data as PROV."""
    BRIDGE.clear()
    # one written rule over the CIDOC-CRM hierarchy (not over HeritageGraph usage):
    # activities are PROV activities, actors are PROV agents, and information
    # objects and beliefs (records and claims) are PROV entities. Physical
    # things, places and time-spans are not mapped: PROV describes the record,
    # not the heritage thing itself.
    crm = "http://www.cidoc-crm.org/cidoc-crm/"
    BRIDGE[URIRef(PROV_NS + "Activity")] = {URIRef(crm + "E7_Activity")}
    BRIDGE[URIRef(PROV_NS + "Agent")] = {URIRef(crm + "E39_Actor")}
    BRIDGE[URIRef(PROV_NS + "Entity")] = {URIRef(crm + "E73_Information_Object"),
                                          URIRef("http://www.cidoc-crm.org/extensions/crminf/I2_Belief")}
    b = Graph()
    b.bind("owl", OWL); b.bind("rdfs", RDFS); b.bind("prov", PROV_NS)
    b.bind("crm", "http://www.cidoc-crm.org/cidoc-crm/")
    b.bind("crminf", "http://www.cidoc-crm.org/extensions/crminf/")
    b.bind("dcterms", DCTERMS)
    b.add((BRIDGE_IRI, RDF.type, OWL.Ontology))
    b.add((BRIDGE_IRI, RDFS.label, Literal("HeritageGraph CIDOC-CRM to PROV-O bridge", lang="en")))
    b.add((BRIDGE_IRI, RDFS.comment, Literal(
        "Optional module. HeritageGraph's alignment of CIDOC-CRM and CRMinf to PROV-O by one rule: "
        "E7 Activity is a subclass of prov:Activity, E39 Actor of prov:Agent, and E73 Information "
        "Object and CRMinf I2 Belief of prov:Entity (records and claims, not heritage things). These axioms are about classes HeritageGraph does not own, so "
        "they are not in the core ontology; load this module together with the core, CIDOC-CRM, "
        "CRMinf and PROV-O when PROV-O-only clients should see CRM-typed data as PROV.", lang="en")))
    b.add((BRIDGE_IRI, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")))
    b.add((BRIDGE_IRI, DCTERMS.source, URIRef("https://github.com/CAIRNepal/heritagegraphontology")))
    for pc, members in sorted(BRIDGE.items()):
        b.add((pc, RDF.type, OWL.Class))
        for m in sorted(members):
            b.add((m, RDF.type, OWL.Class))
            b.add((m, RDFS.subClassOf, pc))
    # declarations, so the module is OWL 2 DL on its own (not only when merged)
    for ap in (DCTERMS.license, DCTERMS.source):
        b.add((ap, RDF.type, OWL.AnnotationProperty))
    b.serialize(BRIDGE_OUT, format="turtle")
    print(f"wrote {BRIDGE_OUT.name}: " + ", ".join(
        f"{len(v)} -> prov:{k.split('#')[1]}" for k, v in sorted(BRIDGE.items())))


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
    # the actual conditional rule (add_location_rule).
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
    # One exception: an axiom between two external terms that the owning
    # vocabulary itself states, checked against the official snapshot
    # (crm:E21_Person ⊑ crm:E39_Actor, restated so the core classifies
    # without importing CRM; prov:generated owl:inverseOf prov:wasGeneratedBy).
    # 1.1.0: HeritageGraph's own CRM→PROV-O alignment of the reused classes
    # (crm:E12_Production ⊑ prov:Activity, crm:E39_Actor ⊑ prov:Agent, …) is
    # not in the core: asserted there it redefined CIDOC-CRM classes for every
    # dataset loading HeritageGraph. It is published as the optional module
    # HeritageGraph-crm-prov-bridge.ttl (write_crm_prov_bridge), and the SHACL
    # provenance constraints name the CRM classes explicitly
    # (bridge_shacl_classes).
    logical = (RDFS.domain, RDFS.range, RDFS.subClassOf, RDFS.subPropertyOf,
               OWL.equivalentClass, OWL.equivalentProperty, OWL.inverseOf,
               OWL.disjointWith, OWL.propertyChainAxiom)
    n = 0
    for pred in logical:
        for s, o in list(g.subject_objects(pred)):
            if not isinstance(s, URIRef) or str(s).startswith(HG_NS):
                continue
            if (pred in (RDFS.subClassOf, OWL.inverseOf) and isinstance(o, URIRef)
                    and not str(o).startswith(HG_NS) and _owner_states(s, pred, o)):
                continue  # stated by the owning vocabulary: the exception above
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
        Collection(g, o).clear()  # and the list cells, or they stay as orphan triples
        g.remove((o, RDF.first, None)); g.remove((o, RDF.rest, None))
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
    relax_shacl_text_and_cardinality(g)
    bridge_shacl_classes(g)
    add_usage_names(g, sv)
    scope_shapes(g, sv)
    add_timespan_rules(g)
    add_location_rule(g, sv)
    harden_shacl(g, sv)
    bind_hg(g)
    g.serialize(destination=SHACL_OUT, format="turtle")
    print(f"finalized {SHACL_OUT.name} ({len(g)} triples)")


CRM_NS = "http://www.cidoc-crm.org/cidoc-crm/"
# nodes that only exist as part of another description (Linked Art writes them
# as blank nodes): their value may be a blank node as well as an IRI
DEPENDENT_CLASSES = {URIRef(CRM_NS + "E52_Time-Span"), URIRef(CRM_NS + "E12_Production"),
                     URIRef(CRM_NS + "E3_Condition_State"), URIRef(CRM_NS + "E14_Condition_Assessment"),
                     URIRef(HG_NS + "Proposition")}


def harden_shacl(g: Graph, sv: SchemaView) -> None:
    """Shape rules beyond what gen-shacl derives from the schema.

    m14: a value of a dependent class (time-span, production, condition
         state or assessment, proposition) may be a blank node.
    m15: the confidence score accepts xsd:integer as well as xsd:decimal (1
         and 0 are scores); xsd:double is not accepted, since its value space
         is disjoint from the OWL range xsd:decimal.
    m16: no text value is the empty string (sh:minLength 1).
    m12: the shapes are open (data may use other vocabularies), so three
         SHACL-SPARQL rules check what open shapes cannot:
         an undeclared hg: property (a typo such as hg:hasArchitecturalStyel)
         is a violation, a deprecated one a warning, and a belief marked
         "conflicting" needs a rival belief about the same subject.
    m23: the shapes graph states its licence and version."""
    owl = Graph().parse(OWL_OUT, format="turtle")
    # the LUX alignment module mints terms in the hg: namespace too
    lux = ROOT / "heritagegraph-lux-migration" / "alignment" / "heritagegraph-lux-alignment.ttl"
    if lux.exists():
        owl += Graph().parse(lux, format="turtle")
    n_bn = 0
    for ps in list(g.subjects(SH.nodeKind, SH.IRI)):
        if any(c in DEPENDENT_CLASSES for c in g.objects(ps, SH["class"])):
            g.remove((ps, SH.nodeKind, SH.IRI))
            g.add((ps, SH.nodeKind, SH.BlankNodeOrIRI))
            n_bn += 1
    n_cs = 0
    for ps in list(g.subjects(SH.path, URIRef(HG_NS + "confidenceScore"))):
        if (ps, SH.datatype, XSD.decimal) in g:
            g.remove((ps, SH.datatype, XSD.decimal))
            alts = []
            for dt in (XSD.decimal, XSD.integer):
                b = BNode(); g.add((b, SH.datatype, dt)); alts.append(b)
            head = BNode(); Collection(g, head, alts)
            g.add((ps, SH["or"], head))
            n_cs += 1
    n_len = 0
    text_types = {XSD.string, RDF.langString}
    for ps in set(g.subjects(SH.path, None)):
        if (ps, RDF.type, SH.NodeShape) in g or (ps, SH.minLength, None) in g:
            continue
        dts = set(g.objects(ps, SH.datatype))
        for lst in g.objects(ps, SH["or"]):
            for alt in Collection(g, lst):
                dts |= set(g.objects(alt, SH.datatype))
        if dts and dts <= text_types:
            g.add((ps, SH.minLength, Literal(1)))
            n_len += 1

    declared = sorted({str(s_) for s_ in owl.subjects(RDF.type, None)
                       if str(s_).startswith(HG_NS) and "#" not in str(s_)
                       and any((s_, RDF.type, t) in owl for t in (OWL.ObjectProperty, OWL.DatatypeProperty,
                                                                  OWL.AnnotationProperty))})
    deprecated = sorted(p for p in declared if (URIRef(p), OWL.deprecated, None) in owl)
    import re as _re
    # one anchored regular expression: rdflib evaluates it far faster than a
    # NOT IN over some two hundred IRIs, once per triple of every focus node
    allowed_re = "^" + _re.escape(HG_NS) + "(" + "|".join(_re.escape(p[len(HG_NS):]) for p in declared) + ")$"
    allowed_re = allowed_re.replace("\\", "\\\\")
    dep = ", ".join(f"<{p}>" for p in deprecated) or "<urn:none>"

    # the shapes target instances of the classes that have a node shape (not
    # every typed node: validation mixes the ontology into the data graph, and
    # its terms are typed too)
    class_shapes = sorted(sh_ for sh_ in g.subjects(RDF.type, SH.NodeShape)
                          if (sh_, SH.targetClass, None) in g)

    def sparql_shape(name: str, select: str, message: str, severity=SH.Violation, target=None):
        c = URIRef(HG_NS + "shapes/" + name)
        g.add((c, RDF.type, SH.SPARQLConstraint))
        g.add((c, SH.message, Literal(message, lang="en")))
        g.add((c, SH.select, Literal(select)))
        g.add((c, RDFS.comment, Literal(message, lang="en")))
        if target is not None:
            shape = URIRef(HG_NS + "shapes/" + name + "Shape")
            g.add((shape, RDF.type, SH.NodeShape))
            g.add((shape, SH.targetSubjectsOf, target))
            g.add((shape, SH.severity, severity))
            g.add((shape, SH.sparql, c))
            return
        if severity == SH.Violation:
            for sh_ in class_shapes:
                g.add((sh_, SH.sparql, c))
        else:  # a warning needs its own shape (severity is per shape)
            shape = URIRef(HG_NS + "shapes/" + name + "Shape")
            g.add((shape, RDF.type, SH.NodeShape))
            g.add((shape, SH.severity, severity))
            g.add((shape, SH.sparql, c))
            for sh_ in class_shapes:
                for tc in g.objects(sh_, SH.targetClass):
                    g.add((shape, SH.targetClass, tc))

    sparql_shape("UndeclaredProperty",
                 "SELECT $this ?path WHERE { $this ?path ?o . "
                 f"FILTER(STRSTARTS(STR(?path), \"{HG_NS}\") && !REGEX(STR(?path), \"{allowed_re}\")) }}",
                 "Uses a property in the HeritageGraph namespace that the ontology does not declare "
                 "(a misspelt or invented term).")
    sparql_shape("DeprecatedProperty",
                 f"SELECT $this ?path WHERE {{ $this ?path ?o . FILTER(?path IN ({dep})) }}",
                 "Uses a deprecated HeritageGraph property; see its dcterms:isReplacedBy.",
                 severity=SH.Warning)
    sparql_shape("ConflictingBeliefHasRival",
                 "SELECT $this WHERE { $this <" + HG_NS + "reconciliationStatus> ?st . "
                 "FILTER(LCASE(STR(?st)) = \"conflicting\") "
                 "OPTIONAL { $this <" + HG_NS + "assertsAbout> ?subj . "
                 "?other <" + HG_NS + "assertsAbout> ?s2 . FILTER(?other != $this) "
                 "FILTER(?s2 = ?subj || EXISTS { ?subj ?p1 ?s2 } || EXISTS { ?s2 ?p2 ?subj }) } "
                 "FILTER(!BOUND(?other)) }",
                 "A belief marked conflicting needs at least one other belief about the same subject or a subject "
                 "directly linked to it (e.g. a belief about a syncretic relationship and one about its deity).",
                 target=URIRef(HG_NS + "reconciliationStatus"))

    shapes = URIRef(HG_NS + "shapes")
    g.add((shapes, RDF.type, OWL.Ontology))
    g.add((shapes, DCTERMS.title, Literal("HeritageGraph SHACL shapes", lang="en")))
    g.add((shapes, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")))
    g.add((shapes, OWL.versionInfo, Literal(str(sv.schema.version))))
    g.add((shapes, DCTERMS.source, ONTOLOGY_IRI))
    print(f"SHACL hardening: {n_bn} blank-node-or-IRI value(s), {n_cs} confidence score shape(s), "
          f"{n_len} minLength 1, 3 SHACL-SPARQL rules ({len(declared)} declared hg: properties)")


def bridge_shacl_classes(g: Graph) -> None:
    """Without the CRM→PROV axioms in the core, a crm:E21_Person value of
    prov:wasAttributedTo is not (in the shapes' class closure) a prov:Agent.
    Each sh:class prov:Activity / prov:Entity / prov:Agent constraint becomes
    "that PROV class or one of the reused classes the bridge places under it",
    so validation accepts what it accepted with the axioms in the core, plus
    crm:E6_Destruction (which the core never placed under prov:Activity and the
    bridge's single rule does). Violations are reported as sh:or results."""
    n = 0
    for pc, members in BRIDGE.items():
        for node in list(g.subjects(SH["class"], pc)):
            g.remove((node, SH["class"], pc))
            alts = []
            for c in [pc] + sorted(members):
                a = BNode(); g.add((a, SH["class"], c)); alts.append(a)
            head = BNode(); Collection(g, head, alts)
            g.add((node, SH["or"], head))
            n += 1
    print(f"SHACL: {n} sh:class prov:* constraint(s) also accept the reused CRM classes "
          f"(the core no longer states CRM ⊑ PROV)")


def relax_shacl_text_and_cardinality(g: Graph) -> None:
    """The SHACL counterpart of relax_text_ranges and
    relax_reused_max_cardinality (B1, B2).
    B1: a free-text property shape (sh:datatype xsd:string, no sh:pattern,
    not a code/identifier slot) accepts xsd:string or rdf:langString.
    Labels, and HeritageGraph's single-valued text properties: at most one
    value per language tag (sh:uniqueLang) and at most one untagged, so
    "Taleju Bhawani"@en and "तलेजु भवानी"@ne may both be given but two
    English names may not.
    B2: sh:maxCount on a CIDOC CRM path is kept only where CRM's own
    quantification allows at most one value (as in the OWL), so CRM data
    with two notes, places or custodians validates. Limits on other
    vocabularies' properties (one prov:generatedAtTime per record) stay: a
    closed-world shape is HeritageGraph's application profile, not an axiom
    about the property, and those owners state no cardinality to follow."""
    crm = crm_max_one()
    n_text = n_label = n_max = 0
    for ps in list(g.subjects(SH.path, None)):
        p = g.value(ps, SH.path)
        if not isinstance(p, URIRef):
            continue
        if ((ps, SH.datatype, XSD.string) in g and (ps, SH.pattern, None) not in g
                and p not in CODE_VALUED):
            g.remove((ps, SH.datatype, XSD.string))
            if p in ANY_LITERAL:      # sh:nodeKind sh:Literal remains
                continue
            alts = []
            for dt in (XSD.string, RDF_LANGSTRING):
                b = BNode(); g.add((b, SH.datatype, dt)); alts.append(b)
            head = BNode(); Collection(g, head, alts)
            g.add((ps, SH["or"], head))
            n_text += 1
            if p == RDFS.label or (ps, SH.maxCount, None) in g:
                g.remove((ps, SH.maxCount, None))
                g.add((ps, SH.uniqueLang, Literal(True)))
                q = BNode(); g.add((q, SH.datatype, XSD.string))
                g.add((ps, SH.qualifiedValueShape, q))
                g.add((ps, SH.qualifiedMaxCount, Literal(1)))
                n_label += 1
                continue
        if (ps, SH.maxCount, None) in g and (
                p == SCHEMA_INLANGUAGE   # one recording in Nepali and Newari
                or (str(p).startswith(CRM_NS) and not reused_max_one_allowed(p, crm))):
            g.remove((ps, SH.maxCount, None))
            n_max += 1
    print(f"B1: {n_text} text shape(s) accept xsd:string or rdf:langString "
          f"({n_label} label/single-valued text shape(s): uniqueLang, one untagged); "
          f"B2: dropped {n_max} sh:maxCount on reused many-valued paths (CRM per its quantification; schema:inLanguage)")


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
        keeping their explicit sh:targetClass.
    Limit: HeritageGraph uses crm:E21_Person, crm:E39_Actor, ... as its own
    classes, so those shapes still apply to any instance of them (and, with the
    ontology mixed in, of their subclasses, e.g. crm:E74_Group via E74 ⊑ E39) in
    a graph validated with these shapes; only the PROV mixins stop applying."""
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


def add_timespan_rules(g: Graph) -> None:
    """Two time-span rules LinkML cannot express, added to the TimeSpan shape:
    the earliest date is not after the latest (crm:P82a sh:lessThanOrEquals
    crm:P82b), and a date recorded in a source calendar (hg:recordedDate)
    names that calendar (hg:calendarSystem)."""
    E52 = URIRef("http://www.cidoc-crm.org/cidoc-crm/E52_Time-Span")
    P82A = URIRef("http://www.cidoc-crm.org/cidoc-crm/P82a_begin_of_the_begin")
    P82B = URIRef("http://www.cidoc-crm.org/cidoc-crm/P82b_end_of_the_end")
    shape = next(iter(g.subjects(SH.targetClass, E52)), None)
    if shape is None:
        sys.exit("TimeSpan shape not found")
    ps = BNode()
    g.add((shape, SH.property, ps))
    g.add((ps, SH.path, P82A))
    g.add((ps, SH.lessThanOrEquals, P82B))
    g.add((ps, SH.description, Literal("The earliest date is not after the latest date.")))
    no_rec, has_cal = BNode(), BNode()
    g.add((no_rec, SH.path, URIRef(HG_NS + "recordedDate")))
    g.add((no_rec, SH.maxCount, Literal(0)))
    g.add((has_cal, SH.path, URIRef(HG_NS + "calendarSystem")))
    g.add((has_cal, SH.minCount, Literal(1)))
    head = BNode()
    Collection(g, head, [no_rec, has_cal])
    g.add((shape, SH["or"], head))
    print("time-span rules: P82a <= P82b; recordedDate requires calendarSystem")


def add_location_rule(g: Graph, sv: SchemaView) -> None:
    """The ArchitecturalStructure rule "a structure whose existence status is
    one of S must record a current location" (a LinkML rule, which gen-shacl
    does not translate) as SHACL on the ArchitecturalStructure shape: either
    no existence status in S, or at least one crm:P55_has_current_location.
    S is read from the rule's precondition, so the YAML stays the source."""
    cls = sv.get_class("ArchitecturalStructure")
    statuses = []
    for rule in cls.rules or []:
        conds = (rule.preconditions.slot_conditions or {}) if rule.preconditions else {}
        es = conds.get("existence_status")
        post = (rule.postconditions.slot_conditions or {}) if rule.postconditions else {}
        if es is not None and "has_current_location" in post:
            statuses = [c.equals_string for c in (es.any_of or [])]
    if not statuses:
        sys.exit("ArchitecturalStructure location rule not found in the schema")
    # on the shape of the class and of every descendant (gen-shacl repeats
    # inherited constraints in each subclass shape, so validation without the
    # ontology graph, where Temple is not known to be an ArchitecturalStructure,
    # still applies the rule)
    names = ["ArchitecturalStructure"] + sorted(sv.class_descendants("ArchitecturalStructure", reflexive=False))
    n = 0
    for name in names:
        c = sv.get_class(name)
        target = uri_for(sv, str(c.class_uri or f"heritageGraph:{name}"))
        shape = next(iter(g.subjects(SH.targetClass, target)), None)
        if shape is None:
            sys.exit(f"{name} shape not found")
        not_in, inner, has_loc = BNode(), BNode(), BNode()
        lst = BNode()
        Collection(g, lst, [URIRef(f"{HG_NS}ExistenceStatus#{v}") for v in statuses])
        g.add((inner, SH["in"], lst))
        g.add((not_in, SH.path, URIRef(HG_NS + "existenceStatus")))
        g.add((not_in, SH["not"], inner))
        g.add((has_loc, SH.path, URIRef("http://www.cidoc-crm.org/cidoc-crm/P55_has_current_location")))
        g.add((has_loc, SH.minCount, Literal(1)))
        head = BNode()
        Collection(g, head, [not_in, has_loc])
        g.add((shape, SH["or"], head))
        n += 1
    print(f"location rule: structures with status {', '.join(statuses)} record a current location "
          f"({n} shapes)")


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


def resolve_abstract_refs(js: dict, sv: SchemaView) -> None:
    """gen-json-schema writes "$ref": "#/$defs/X" for a slot whose range X is
    an abstract or union class without an identifier (AssertionSubject,
    RitualAssessment, KumariLifecycleEvent), but writes no $defs entry for X:
    the reference cannot be resolved and validation of any document using
    the field fails. In a data object such a field holds a reference, as
    every other object-valued field does: it becomes the referenced
    instance's id (a string). In a Container collection, which holds the
    instances themselves, it becomes any of X's concrete descendants."""
    defs = js.get("$defs", {})

    def concrete(x: str) -> list[str]:
        c = sv.get_class(x)
        names = set(sv.class_descendants(x)) | set(c.union_of or [])
        for u in list(c.union_of or []):
            names |= set(sv.class_descendants(u))
        return sorted(n for n in names if n in defs and not sv.get_class(n).abstract)

    fixed = []

    def repair(holder, key, inlined: bool, where: str) -> None:
        node = holder[key]
        target = node.get("$ref", "").removeprefix("#/$defs/")
        if not target or target in defs:
            return
        desc = node.get("description")
        if inlined:
            new = {"anyOf": [{"$ref": f"#/$defs/{n}"} for n in concrete(target)]}
        else:
            new = {"type": "string"}
        if desc:
            new = {"description": desc, **new}
        holder[key] = new
        fixed.append(f"{where} ({target})")

    for owner, props, inlined in ([("Container", js.get("properties", {}), True)] +
                                  [(c, d.get("properties", {}), c == "Container")
                                   for c, d in defs.items()]):
        for pname, pdef in props.items():
            if "$ref" in pdef:
                repair(props, pname, inlined, f"{owner}.{pname}")
            if isinstance(pdef.get("items"), dict) and "$ref" in pdef["items"]:
                repair(pdef, "items", inlined, f"{owner}.{pname}")
            for i, alt in enumerate(pdef.get("anyOf", [])):   # nullable form
                if isinstance(alt, dict) and "$ref" in alt:
                    repair(pdef["anyOf"], i, inlined, f"{owner}.{pname}")
    # de-duplicate anyOf alternatives (two members resolved to the same id string)
    def dedupe(node):
        if isinstance(node, dict):
            if isinstance(node.get("anyOf"), list):
                seen, out = set(), []
                for alt in node["anyOf"]:
                    key = json.dumps(alt, sort_keys=True)
                    if key not in seen:
                        seen.add(key); out.append(alt)
                node["anyOf"] = out
            for v in node.values():
                dedupe(v)
        elif isinstance(node, list):
            for v in node:
                dedupe(v)
    import json
    dedupe(js)
    print(f"JSON Schema: resolved {len(fixed)} reference(s) to classes with no $defs entry")

    # A Container collection holds the instances themselves, and the generated
    # schema allows only its declared class there ($ref, additionalProperties
    # false): a destruction (with destroyed) could not go into
    # historical_events, nor a Temple's own fields into structures. Each
    # collection accepts its class or any concrete descendant.
    widened = set()
    for props in (js.get("properties", {}), defs.get("Container", {}).get("properties", {})):
        for pname, pdef in props.items():
            items = pdef.get("items")
            if not isinstance(items, dict) or "$ref" not in items:
                continue
            cname = items["$ref"].removeprefix("#/$defs/")
            if cname not in sv.all_classes():
                continue
            subs = sorted(d for d in sv.class_descendants(cname, reflexive=False)
                          if d in defs and not sv.get_class(d).abstract)
            if subs:
                pdef["items"] = {"anyOf": [{"$ref": f"#/$defs/{x}"} for x in [cname] + subs]}
                widened.add(pname)
    print(f"JSON Schema: {len(widened)} Container collection(s) (root and Container def) also accept "
          f"the concrete subclasses")


def allow_single_string(js: dict, sv: SchemaView) -> None:
    """A text field made multivalued in 1.1.0 (note, and source_citation
    through is_a note) is an array in the generated JSON Schema; 1.0.x data
    gave it as one string. Accept a single string as well, so every 1.0.x
    instance still validates. JSON values are plain strings: language-tagged
    text is an RDF-level feature (tagged literals, checked by the SHACL
    shapes), with no JSON form in this schema."""
    classes = sv.all_classes()
    n = 0
    for cname, cdef in js.get("$defs", {}).items():
        if cname not in classes:
            continue
        for pname, pdef in cdef.get("properties", {}).items():
            try:
                sl = sv.induced_slot(pname, cname)
            except ValueError:
                continue
            if (not sl.multivalued or sl.range != "string" or sl.any_of
                    or sl.exactly_one_of or not sl.slot_uri):
                continue
            if uri_for(sv, str(sl.slot_uri)) in CODE_VALUED | ANY_LITERAL:
                continue
            alts = [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]
            new = {"anyOf": alts if sl.required else alts + [{"type": "null"}]}
            if pdef.get("description"):
                new = {"description": pdef["description"], **new}
            cdef["properties"][pname] = new
            n += 1
    print(f"JSON Schema: {n} multivalued text field(s) also accept a single string")


XSD_DATETIME = (r"^-?[0-9]{4,}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?"
                r"(Z|[+-][0-9]{2}:[0-9]{2})?$")


def relax_datetime(js: dict) -> None:
    """JSON Schema's "format": "date-time" is RFC 3339, which requires a time
    zone offset; the RDF values are xsd:dateTime, where the offset is optional
    (the demonstrator's dates have none), so valid data was refused. Each
    date-time field takes the xsd:dateTime lexical form instead."""
    n = 0
    def walk(node):
        nonlocal n
        if isinstance(node, dict):
            if node.get("format") == "date-time":
                del node["format"]
                node["pattern"] = XSD_DATETIME
                n += 1
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(js)
    print(f"JSON Schema: {n} date-time field(s) take the xsd:dateTime form (offset optional)")


def gen_json_schema() -> None:
    out = ROOT / "ontology" / "HeritageGraph.schema.json"
    # generated from the serialization wrapper (core schema + Container/Metadata);
    # $id and title stay those of the core schema so the published JSON Schema
    # keeps its identity across 1.0.x -> 1.1.0. Its $defs change only
    # additively (note also accepts an array; references that could not be
    # resolved are repaired), so every 1.0.x instance still validates.
    import json
    import yaml
    res = subprocess.run(
        ["linkml", "generate", "json-schema", str(CONTAINER_SCHEMA)],
        cwd=ROOT, check=True, capture_output=True, text=True)
    js = json.loads(res.stdout)
    core = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    js["$id"], js["title"] = core["id"], core["name"]
    csv = SchemaView(str(CONTAINER_SCHEMA))
    resolve_abstract_refs(js, csv)
    relax_datetime(js)
    allow_single_string(js, csv)
    # m23: licence and provenance of the schema itself (an annotation keyword, no validation effect)
    js["$comment"] = (f"HeritageGraph JSON Schema, version {js.get('version', '')}, generated from "
                      "ontology/HeritageGraph.yaml (HeritageGraph-container.yaml). Licence: CC BY 4.0 "
                      "(https://creativecommons.org/licenses/by/4.0/). Ontology: https://cair-nepal.org/heritagegraph/ontology")
    out.write_text(json.dumps(js, indent=4) + "\n\n", encoding="utf-8")  # gen-json-schema layout
    print(f"generated {out.name}")


def main() -> int:
    sv = SchemaView(str(SCHEMA))
    load_lexical_forms(SchemaView(str(CONTAINER_SCHEMA)))
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
    write_crm_prov_bridge(sv)
    finalize_shacl(sv)
    run_pyshacl()
    stamp_provenance()
    sync_published()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
