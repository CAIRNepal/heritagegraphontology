# HeritageGraph Release Quality Report

Generated: 2026-06-06T08:47:06.775119

## Executive summary

| Dimension | Score (/10) | Status |
|-----------|-------------|--------|
| Artefact packaging | 8.5 | Release bundle complete (TTL, SHACL, alignment, EDM, VoID, examples) |
| Logical consistency (OWL-RL) | 8.0 | 0 unsatisfiable classes; 20,304 inferred triples |
| Logical consistency (HermiT DL) | 6.5 | pending — Java not available locally; CI will archive log |
| Schema adequacy (CQ TBox) | 9.5 | 32/32 ASK queries pass |
| ABox demonstrability | 8.5 | Mini Kathmandu ABox + 9 sample SELECT queries |
| Interoperability | 7.5 | CRM/PROV/EDM/FOAF alignment modules present |
| Documentation fidelity | 8.5 | Manuscript metrics reconciled; docs metadata refreshed |
| Registry readiness | 7.5 | VoID + LOV metadata; w3id `.htaccess` prepared |
| **Composite** | **8.1** | **Near submission — tag v1.0.0 + w3id PR remaining** |

## Automated checks (all green)

- Paper vs TTL metrics: 7/7 match
- Alignment claims: 5/5 match
- CQ TBox: 32/32 pass
- SHACL: clean generation (no inverse warnings)
- ABox samples: 9 passing SELECT queries

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

- OOPS P10/P11: sparse global `rdfs:domain` and partial sibling disjointness (LinkML restriction pattern)
- HermiT run uses imports-stripped OWL for reproducible CI classification
- Full import closure (CRM+PROV+…) should be confirmed in Protégé for integrators

## Repository

https://github.com/CAIRNepal/heritagegraphontology

## ABox CQ samples

```
ABox CQ Sample Execution
Date: 2026-06-06T08:47:06.572379
TBox: /Users/nirajkarki/cair/heritagegraphontology/HeritageGraph.ttl
ABox: /Users/nirajkarki/cair/heritagegraphontology/examples/kathmandu-mini-abox.ttl
Triples loaded: 5155

[PASS] CQ1-style: structures with production timespan: 1 row(s)
[PASS] CQ11-style: rituals on structures at places: 2 row(s)
[PASS] CQ25-style: syncretic deity links with sources: 1 row(s)
[PASS] Multi-vocal: conflicting assertions: 2 row(s)
[PASS] CQ26-style: Living Goddess tenure: 1 row(s)
[PASS] CQ7-style: sacred structures in a place with associated rituals: 3 row(s)
[PASS] CQ12-style: canonical ritual sequence within a festival: 1 row(s)
[PASS] CQ19-style: institutions managing heritage and performing rituals: 1 row(s)
[PASS] CQ27-style: Kumari person linked to embodied deity: 1 row(s)
```

## Consistency excerpt

```
============
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
  owl:disjointWith pairs declared: 0
  Object properties without explicit rdfs:range: 23/123
  Datatype properties without explicit rdfs:range: 6/47

======================================================================
  Summary
======================================================================
  Parse               : ✅ OK
  OWL-RL closure      : 20304 inferred triples
  Unsatisfiable       : 0 classes
  Disjointness axioms : 0

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
  Object properties                     123        123        ✅
  Datatype properties                    47         47        ✅
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
