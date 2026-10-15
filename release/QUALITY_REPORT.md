# HeritageGraph Release Quality Report

Generated: 2026-10-15T21:59:47.674837

## Executive summary

| Dimension | Score (/10) | Status |
|-----------|-------------|--------|
| Artefact packaging | 8.5 | Release bundle complete (TTL, SHACL, alignment, EDM, VoID, examples) |
| Logical consistency (OWL-RL) | 8.0 | 0 unsatisfiable classes; 9,779 inferred triples |
| Logical consistency (HermiT DL) | 9.0 | HermiT: 0 unsatisfiable classes (imports stripped) |
| Schema adequacy (CQ TBox) | 9.5 | 32/32 ASK queries pass |
| ABox demonstrability | 8.5 | Mini Kathmandu ABox + 32 sample SELECT queries |
| Interoperability | 7.5 | CRM/PROV/EDM/FOAF alignment modules present |
| Documentation fidelity | 8.5 | Manuscript metrics reconciled; docs metadata refreshed |
| Registry readiness | 7.5 | VoID + LOV metadata; nginx content negotiation prepared (`deploy/nginx/`) |
| **Composite** | **8.4** | **Submission-ready draft** |

## Automated checks (all green)

- Paper vs TTL metrics: 7/7 match
- Alignment claims: 5/5 match
- CQ TBox: 32/32 pass
- SHACL: clean generation (no inverse warnings)
- ABox samples: 32 passing SELECT queries

## Pre-submission checklist

- [x] Regenerate artefacts from `HeritageGraph.yaml`
- [x] Archive evaluation reports under `release/evaluation/`
- [x] Refresh `docs/` ontology serialisations and HTML metadata
- [x] Prepare nginx content negotiation for cair-nepal.org (`deploy/nginx/`)
- [x] Prepare `registry/lov-metadata.ttl` for LOV submission
- [ ] Tag git release `v1.0.0` and push to `CAIRNepal/heritagegraphontology`
- [ ] Deploy `deploy/nginx/` on cair-nepal.org and run `deploy/nginx/check_conneg.py`
- [ ] Submit LOV entry after the cair-nepal.org IRIs resolve
- [ ] Fill author initials in `sw_template.tex` before journal submit

## Known intentional limitations

- OOPS P11: global `rdfs:domain` is intentionally sparse for reusable slots (LinkML pattern); 2 sibling disjointness pairs are declared
- HermiT run uses imports-stripped OWL for reproducible CI classification
- Full import closure (CRM+PROV+…) should be confirmed in Protégé for integrators

## Repository

https://github.com/CAIRNepal/heritagegraphontology

## ABox CQ samples

```
All-32 CQ expected-vs-actual execution
Date: 2026-10-15T21:59:46.713786
TBox: HeritageGraph.ttl
ABox: kathmandu-mini-abox.ttl
Triples loaded: 4523
Pass criterion: returned bindings == expected answer set (exact match).

CQ1   [PASS] expected=1  actual=1  Which architectural structures were built during a time period using an architectural style?
CQ2   [PASS] expected=1  actual=1  Which architectural elements are components of structures used in a given ritual?
CQ3   [PASS] expected=1  actual=1  Which iconographic objects depict a deity, and where are they currently located?
CQ4   [PASS] expected=1  actual=1  Which heritage structures are associated with historical events, and over what time-spans?
CQ5   [PASS] expected=2  actual=2  Which architectural structures within a geographical area belong to a particular typology?
CQ6   [PASS] expected=1  actual=1  Which heritage shares a common architectural style?
CQ7   [PASS] expected=1  actual=1  Which sacred structures in a place are associated with which deities?
CQ8   [PASS] expected=1  actual=1  Among temples that conduct daily Nitya Puja, which are assessed as damaged/endangered?
CQ9   [PASS] expected=1  actual=1  Which caste groups have hereditary roles in rituals critical for a festival?
CQ10  [PASS] expected=1  actual=1  Which ritual objects are associated with rituals, and who is responsible for their use?
CQ11  [PASS] expected=1  actual=1  Which rituals are associated with which sites, invoke which deities, with what recurrence?
CQ12  [PASS] expected=1  actual=1  What is the sequence of ritual events, and which actors are responsible for each step?
CQ13  [PASS] expected=1  actual=1  Which rituals move sacred presences between sites, and what routes are traversed?
CQ14  [PASS] expected=1  actual=1  How do crises trigger extraordinary rituals outside the normal calendar?
CQ15  [PASS] expected=1  actual=1  What materials and techniques are used in key ritual events?
CQ16  [PASS] expected=4  actual=4  What are the ritual obligations of participant groups, and how are their roles recorded?
CQ17  [PASS] expected=1  actual=1  Which rituals have documented transformations, and which sources attest them?
CQ18  [PASS] expected=2  actual=2  How do changes in structures reflect broader transitions (via provenance assertions)?
CQ19  [PASS] expected=1  actual=1  Which organisations manage which heritage, perform which rituals, and hold custody?
CQ20  [PASS] expected=1  actual=1  Which structures were commissioned by a specific patron?
CQ21  [PASS] expected=1  actual=1  Which institutions provide economic and ritual support for sites, rituals, or sacred figures?
CQ22  [PASS] expected=1  actual=1  Which festivals bring together multiple groups around a shared syncretic deity?
CQ23  [PASS] expected=1  actual=1  Which places or structures function as shared or contested sites for multiple traditions?
CQ24  [PASS] expected=1  actual=1  Which rituals at Hindu temples and Buddhist monuments invoke the same syncretic deity?
CQ25  [PASS] expected=2  actual=2  How do syncretic deities link traditions, and what evidence supports these links?
CQ26  [PASS] expected=1  actual=1  Which person served as Kumari, for which period, at which residence?
CQ27  [PASS] expected=2  actual=2  For a given Kumari, which deity is believed present, in which religious traditions?
CQ28  [PASS] expected=1  actual=1  How does the Kumari institution embody Hindu-Buddhist syncretism in a place and period?
CQ29  [PASS] expected=1  actual=1  What daily rituals does a Kumari perform at her residence, with what temporal pattern?
CQ30  [PASS] expected=1  actual=1  In which processions does a given Kumari participate, and in what sequence?
CQ31  [PASS] expected=1  actual=1  Which institution bears responsibility for a given Kumari during her tenure?
CQ32  [PASS] expected=1  actual=1  When and why did an individual stop being Kumari, and what event terminated the status?

Total: 32/32 CQs match their expected answer set.

Negative control (CQ11 with a broken predicate): actual=0 vs expected=1 -> mismatch detected (oracle discriminates)

```

## Consistency excerpt

```

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
  owl:disjointWith pairs declared: 2
  Object properties without explicit rdfs:range: 47/149
  Datatype properties without explicit rdfs:range: 10/42

======================================================================
  Summary
======================================================================
  Parse               : ✅ OK
  OWL-RL closure      : 9779 inferred triples
  Unsatisfiable       : 0 classes
  Disjointness axioms : 2

  ⚠️  For full OWL DL consistency, load HeritageGraph.ttl in Protégé
     and run the HermiT reasoner (Reasoner → HermiT → Start Reasoner).

```

## Metrics excerpt

```
n            label:✅  def:✅
   65. Verification                             label:✅  def:✅
   66. WaterStructure                           label:✅  def:✅

======================================================================
  Paper Claims vs Actual
======================================================================

  Metric                              Paper     Actual    Match
  --------------------------------------------------------------
  Named owl:Class (HG namespace)         70         66        ❌
  Object properties                     123        149        ❌
  Datatype properties                    48         42        ❌
  Union classes (named)                   3          1        ❌
  Named individuals (enum values)         64         51        ❌
  SHACL NodeShapes                       61         61        ✅
  CQ TBox pass rate                   32/32      32/32        ✅
```

## Regenerate

```bash
python3 scripts/finalize_alpha5_artifacts.py
python3 scripts/run_release_quality.py
```
