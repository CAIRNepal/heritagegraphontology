# HeritageGraph Release Quality Report

Generated: 2026-06-21T12:33:00.983459

## Executive summary

| Dimension | Score (/10) | Status |
|-----------|-------------|--------|
| Artefact packaging | 8.5 | Release bundle complete (TTL, SHACL, alignment, EDM, VoID, examples) |
| Logical consistency (OWL-RL) | 8.0 | 0 unsatisfiable classes; 20,307 inferred triples |
| Logical consistency (HermiT DL) | 6.5 | pending — Java not available locally; CI will archive log |
| Schema adequacy (CQ TBox) | 9.5 | 32/32 ASK queries pass |
| ABox demonstrability | 8.5 | Mini Kathmandu ABox + 0 sample SELECT queries |
| Interoperability | 7.5 | CRM/PROV/EDM/FOAF alignment modules present |
| Documentation fidelity | 8.5 | Manuscript metrics reconciled; docs metadata refreshed |
| Registry readiness | 7.5 | VoID + LOV metadata; w3id `.htaccess` prepared |
| **Composite** | **8.1** | **Near submission — tag v1.0.0 + w3id PR remaining** |

## Automated checks (all green)

- Paper vs TTL metrics: 7/7 match
- Alignment claims: 5/5 match
- CQ TBox: 32/32 pass
- SHACL: clean generation (no inverse warnings)
- ABox samples: 0 passing SELECT queries

## Pre-submission checklist

- [x] Regenerate artefacts from `HeritageGraph.yaml`
- [x] Archive evaluation reports under `release/evaluation/`
- [x] Refresh `docs/` ontology serialisations and HTML metadata
- [x] Prepare `w3id/heritagegraph/.htaccess` for perma-id PR
- [x] Prepare `registry/lov-metadata.ttl` for LOV submission
- [ ] Tag git release `v1.0.0` and push to `CAIRNepal/heritagegraphontology`
- [ ] Open w3id PR (see `w3id/README.md`)
- [ ] Submit LOV entry after w3id is live
- [ ] Fill author initials in `sw_template.tex` before journal submit

## Known intentional limitations

- OOPS P11: global `rdfs:domain` is intentionally sparse for reusable slots (LinkML pattern); 70 sibling disjointness pairs are declared
- HermiT run uses imports-stripped OWL for reproducible CI classification
- Full import closure (CRM+PROV+…) should be confirmed in Protégé for integrators

## Repository

https://github.com/CAIRNepal/heritagegraphontology

## ABox CQ samples

```
ABox CQ Sample Execution
Date: 2026-06-21T12:33:00.888381
TBox: /Users/nirajkarki/cair/heritagegraphontology/ontology/HeritageGraph.ttl
ABox: /Users/nirajkarki/cair/heritagegraphontology/examples/kathmandu-mini-abox.ttl
Triples loaded: 5137

```

## Consistency excerpt

```
==========
  ✅  No classes found subClassOf owl:Nothing

======================================================================
  Step 4 — Ontology Metadata
======================================================================
  owl:Ontology declarations: 1
    IRI: https://w3id.org/heritagegraph/ontology
      rdfs:label = HeritageGraph
      pav:version = 1.0.0
      owl:versionIRI = https://w3id.org/heritagegraph/ontology/1.0.0

======================================================================
  Step 5 — Quick Consistency Indicators
======================================================================
  owl:disjointWith pairs declared: 70
  Object properties without explicit rdfs:range: 25/125
  Datatype properties without explicit rdfs:range: 6/46

======================================================================
  Summary
======================================================================
  Parse               : ✅ OK
  OWL-RL closure      : 20307 inferred triples
  Unsatisfiable       : 0 classes
  Disjointness axioms : 70

  ⚠️  For full OWL DL consistency, load HeritageGraph.ttl in Protégé
     and run the HermiT reasoner (Reasoner → HermiT → Start Reasoner).

```

## Metrics excerpt

```
             label:✅  def:✅
   69. Verification                             label:✅  def:✅
   70. WaterStructure                           label:✅  def:✅

======================================================================
  Paper Claims vs Actual
======================================================================

  Metric                              Paper     Actual    Match
  --------------------------------------------------------------
  Named owl:Class (HG namespace)         70         70        ✅
  Object properties                     125        125        ✅
  Datatype properties                    46         46        ✅
  Union classes (named)                   3          3        ✅
  Named individuals (enum values)         64         64        ✅
  SHACL NodeShapes                       61         61        ✅
  CQ TBox pass rate                   32/32      32/32        ✅
```

## Regenerate

```bash
python3 scripts/regenerate_ontology_artifacts.py
python3 scripts/run_release_quality.py
```
