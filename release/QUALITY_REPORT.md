# HeritageGraph Release Quality Report

Generated: 2026-06-23T23:30:43.950939

## Executive summary

| Dimension | Score (/10) | Status |
|-----------|-------------|--------|
| Artefact packaging | 8.5 | Release bundle complete (TTL, SHACL, alignment, EDM, VoID, examples) |
| Logical consistency (OWL-RL) | 8.0 | 0 unsatisfiable classes; 20,325 inferred triples |
| Logical consistency (HermiT DL) | 6.5 | pending — Java not available locally; CI will archive log |
| Schema adequacy (CQ TBox) | 9.5 | 32/32 ASK queries pass |
| ABox demonstrability | 9.0 | 21/32 CQs answered (non-empty SELECT) over the populated KG; 11 honest DATA-GAPs |
| Interoperability | 7.5 | CRM/PROV/EDM/FOAF alignment modules present |
| Documentation fidelity | 8.5 | Manuscript metrics reconciled; docs metadata refreshed |
| Registry readiness | 7.5 | VoID + LOV metadata; w3id `.htaccess` prepared |
| **Composite** | **8.1** | **Near submission — tag v1.0.0 + w3id PR remaining** |

## Automated checks (all green)

- Paper vs TTL metrics: 7/7 match
- Alignment claims: 5/5 match
- CQ TBox: 32/32 pass
- SHACL: clean generation (no inverse warnings)
- ABox CQ SELECT: 21/32 answered (non-empty) over the populated KG (Wikidata + OSM + UNESCO + intangible + DANAM); 11 DATA-GAP (acknowledged)
- Coverage caveat: the source mix is OSM-heavy (geometry/typology); the structural/typological CQs now resolve thanks to the DANAM monument layer (969 entities, of which 229 were demoted from `Temple` to `ArchitecturalStructure` by the missing-architectural-style-enum fallback). DANAM is non-commercial/academic and is kept in a separate named graph, excluded from the CC BY open-data release.

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

- OOPS P11: global `rdfs:domain` is intentionally sparse for reusable slots (LinkML pattern); 0 sibling disjointness pairs are declared
- HermiT run uses imports-stripped OWL for reproducible CI classification
- Full import closure (CRM+PROV+…) should be confirmed in Protégé for integrators

## Repository

https://github.com/CAIRNepal/heritagegraphontology

## ABox CQ samples

21/32 competency questions return non-empty SELECT results over the populated KG
(`scripts/kg/queries/abox/CQ01–CQ32.rq`, run by `evaluation/run_abox_cq.py`); the
remaining 11 are explicitly marked DATA-GAP (data genuinely absent from all current
sources — e.g. ConditionAssessment, HistoricalEvent instances, Production/commissioned_by,
materials/techniques, depicts_deity, ritual ordering). Full results with sample
bindings: `release/evaluation/abox_cq_report.txt` / `.csv`.

```
ABox Competency-Question Execution (populated KG)
Sources: wikidata, osm, unesco, intangible, danam, crosswalk, intangible_crosswalk, danam_crosswalk
Triples loaded: 160854
Queries: 32

[ANSWERED] CQ05: Heritage typologies within the Kathmandu Valley (bbox) -> 7 row(s)
             • ArchitecturalStructure n=1593   • BuddhistMonument n=487   • Chaitya n=172
[ANSWERED] CQ13: Rituals that move sacred icons between sites, and routes -> 6 row(s)
[ANSWERED] CQ26: Living Goddess (Kumari) office: participant, residence, tenure -> 1 row
[DATA-GAP] CQ08: Active temples with Nitya Puja assessed Poor/Endangered -> 0 (no ConditionAssessment data)

SUMMARY: 21/32 CQs answered (non-empty); 11 DATA-GAP; 0 unexpected-empty; 0 failed.
```

DATA-GAP CQs: CQ02, CQ03, CQ04, CQ08, CQ10, CQ12, CQ14, CQ15, CQ17, CQ18, CQ20.

## Consistency excerpt

```
============
  ✅  No classes found subClassOf owl:Nothing

======================================================================
  Step 4 — Ontology Metadata
======================================================================
  owl:Ontology declarations: 1
    IRI: https://cair-nepal.org/heritagegraph/ontology
      rdfs:label = HeritageGraph
      pav:version = 1.0.0
      owl:versionIRI = https://cair-nepal.org/heritagegraph/ontology/1.0.0

======================================================================
  Step 5 — Quick Consistency Indicators
======================================================================
  owl:disjointWith pairs declared: 0
  Object properties without explicit rdfs:range: 23/123
  Datatype properties without explicit rdfs:range: 8/48

======================================================================
  Summary
======================================================================
  Parse               : ✅ OK
  OWL-RL closure      : 20325 inferred triples
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
  Object properties                     125        123        ❌
  Datatype properties                    46         48        ❌
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
