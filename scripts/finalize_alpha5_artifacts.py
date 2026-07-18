#!/usr/bin/env python3
"""Finalize HeritageGraph 0.1.0-alpha.5 artifacts.

Addresses the committee-review validation blockers for the alpha.5 lineage:
  1. OWL: gen-owl (--no-use-native-uris) drops `disjoint_with`; this script
     re-injects owl:disjointWith, asserts FAIR metadata as typed triples, and
     ABORTS if any declared axiom (disjointness, inverses, mappings,
     subproperty bridges) is missing from the final graph (axiom-survival
     guard, mirroring scripts/regenerate_ontology_artifacts.py).
  2. SHACL: gen-shacl output fails its own demonstrator (identifier MinCount
     on every node although the node IRI is the identifier; sh:class on
     union_of classes that no generator can satisfy; closed shapes). This
     script repairs the shapes: drops identifier min-counts, rewrites
     sh:class <union class> as sh:or over the union members, and opens the
     closed shapes (documented relaxation).
  3. Runs pyshacl over examples/kathmandu-mini-abox-alpha5.ttl and aborts
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
OWL_OUT = ROOT / "ontology" / "HeritageGraph.ttl"
SHACL_OUT = ROOT / "ontology" / "HeritageGraph.shacl.ttl"
ABOX = ROOT / "examples" / "kathmandu-mini-abox-alpha5.ttl"
RESULTS = ROOT / "evaluation" / "results"

HG = Namespace("https://w3id.org/heritagegraph/")
SH = Namespace("http://www.w3.org/ns/shacl#")
BIBO = Namespace("http://purl.org/ontology/bibo/")
VANN = Namespace("http://purl.org/vocab/vann/")
ONTOLOGY_IRI = URIRef("https://w3id.org/heritagegraph/ontology")


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
        expr = BNode()
        head = BNode()
        Collection(g, head, members)
        g.add((expr, RDF.type, OWL.Class))
        g.add((expr, OWL.unionOf, head))
        g.add((cls, OWL.equivalentClass, expr))
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
        "http://purl.org/dc/terms/source",
        "http://purl.org/dc/terms/creator",
        "http://purl.org/dc/terms/publisher",
        "http://purl.org/ontology/bibo/status",
        "http://purl.org/pav/version",
        "http://purl.org/vocab/vann/preferredNamespacePrefix",
        "http://purl.org/vocab/vann/preferredNamespaceUri",
        "https://w3id.org/heritagegraph/crminf_pattern",
        "https://w3id.org/heritagegraph/design_note",
        "https://w3id.org/heritagegraph/prov_alignment",
        "https://w3id.org/heritagegraph/prov_alignment_note",
        "https://w3id.org/heritagegraph/provenance_scope",
        "https://w3id.org/linkml/permissible_values",
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
    print(f"declared {n_ann} owl:AnnotationProperty(ies)")

    # --- SKOS publication of enumerations (gen-owl emits nothing for them) ---
    n_scheme, n_concept = 0, 0
    for en, e in sv.all_enums().items():
        scheme = URIRef(f"https://w3id.org/heritagegraph/scheme/{en}")
        g.add((scheme, RDF.type, SKOS.ConceptScheme))
        g.add((scheme, SKOS.prefLabel, Literal(en)))
        # rdfs:label alongside prefLabel: generic tools (ROBOT report,
        # Protege) look for rdfs:label and flagged these as missing_label
        g.add((scheme, RDFS.label, Literal(en)))
        if e.description:
            g.add((scheme, SKOS.definition, Literal(str(e.description))))
        n_scheme += 1
        for vn, pv in (e.permissible_values or {}).items():
            # concept IRI: the declared meaning where present (matches data
            # serialization); otherwise minted under scheme/<Enum>/<value> so it
            # cannot collide with class IRIs (data serializes these as literals)
            if pv.meaning:
                c = uri_for(sv, str(pv.meaning))
            else:
                c = URIRef(f"https://w3id.org/heritagegraph/scheme/{en}/{vn}")
            g.add((c, RDF.type, SKOS.Concept))
            g.add((c, SKOS.inScheme, scheme))
            g.add((c, SKOS.prefLabel, Literal(vn)))
            if not pv.meaning:
                # label minted concepts only; external meaning IRIs (aat:,
                # wikidata:) keep their owners' labels to avoid duplicate_label
                g.add((c, RDFS.label, Literal(vn)))
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
            n_dep += 1
    print(f"marked {n_dep} property(ies) owl:deprecated")

    # --- FAIR metadata as typed triples on the ontology node ---
    onts = list(g.subjects(RDF.type, OWL.Ontology))
    ont = onts[0] if onts else ONTOLOGY_IRI
    meta = [
        (DCTERMS.created, Literal("2025-11-23", datatype=XSD.date)),
        (DCTERMS.modified, Literal(date.today().isoformat(), datatype=XSD.date)),
        (DCTERMS.source, URIRef("https://github.com/CAIRNepal/heritagegraphontology")),
        (DCTERMS.bibliographicCitation, Literal(
            "CAIR-Nepal (2026). HeritageGraph Ontology (0.1.0-alpha.5). "
            "https://w3id.org/heritagegraph/ontology")),
        (DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")),
        (DCTERMS.creator, Literal("CAIR-Nepal")),
        (DCTERMS.publisher, Literal("CAIR-Nepal")),
        (BIBO.status, Literal("Pre-release specification draft (alpha)")),
        (VANN.preferredNamespacePrefix, Literal("heritageGraph")),
        (VANN.preferredNamespaceUri, Literal("https://w3id.org/heritagegraph/")),
    ]
    for p, o in meta:
        for old in list(g.objects(ont, p)):
            g.remove((ont, p, old))
        g.add((ont, p, o))
    g.bind("bibo", BIBO); g.bind("vann", VANN)

    repair_dl_profile(g, sv)

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
            ok = any((eq, OWL.unionOf, None) in g for eq in g.objects(cls, OWL.equivalentClass))
            if not ok:
                missing.append(f"unionOf: {cn}")
    for sn, s in sv.all_slots().items():
        if s.deprecated and s.slot_uri:
            if (uri_for(sv, str(s.slot_uri)), OWL.deprecated, None) not in g:
                missing.append(f"owl:deprecated: {sn}")
    for en, e in sv.all_enums().items():
        scheme = URIRef(f"https://w3id.org/heritagegraph/scheme/{en}")
        if (scheme, RDF.type, SKOS.ConceptScheme) not in g:
            missing.append(f"conceptScheme: {en}")
        for vn, pv in (e.permissible_values or {}).items():
            c = uri_for(sv, str(pv.meaning)) if pv.meaning else URIRef(
                f"https://w3id.org/heritagegraph/scheme/{en}/{vn}")
            if (c, SKOS.inScheme, scheme) not in g:
                missing.append(f"enumConcept: {en}.{vn}")
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
           URIRef(f"https://w3id.org/heritagegraph/ontology/{version}")))
    for pred in (DCTERMS.title, DCTERMS.description):
        if (pred, RDF.type, None) not in g:
            g.add((pred, RDF.type, OWL.AnnotationProperty))
    g.add((ONTOLOGY_IRI, DCTERMS.title, Literal("HeritageGraph Ontology")))
    if sv.schema.description:
        g.add((ONTOLOGY_IRI, DCTERMS.description, Literal(str(sv.schema.description))))
    print(f"DL: ontology IRI -> {ONTOLOGY_IRI} (versionIRI .../{version})")


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
    g.serialize(destination=SHACL_OUT, format="turtle")
    print(f"finalized {SHACL_OUT.name} ({len(g)} triples)")


def run_pyshacl() -> None:
    from pyshacl import validate
    conforms, _, text = validate(
        data_graph=str(ABOX), shacl_graph=str(SHACL_OUT),
        ont_graph=str(OWL_OUT), inference="none")
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
    print("synced docs/ontology.{ttl,owl,nt,jsonld}")


def main() -> int:
    sv = SchemaView(str(SCHEMA))
    gen("owl", OWL_OUT, ["--no-use-native-uris"])
    gen("shacl", SHACL_OUT)
    finalize_owl(sv)
    finalize_shacl(sv)
    run_pyshacl()
    stamp_provenance()
    sync_published()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
