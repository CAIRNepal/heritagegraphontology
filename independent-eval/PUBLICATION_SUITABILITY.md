# HeritageGraph — Publication Suitability Assessment
### Target: TGDK (Transactions on Graph Data and Knowledge), Special Issue "Semantic Digital Humanities"
Prepared from an independent evaluation of `HeritageGraph.ttl` + external benchmarking. Date: 2026-06-14.

---

## 1. Executive verdict

**Conditionally suitable — a credible *accept* candidate after a focused, non-structural revision.**

HeritageGraph has the two things that are hardest to manufacture: **genuine conceptual novelty** (an event-centric, provenance-aware model of *living* heritage, with no competing Nepal/Guthi/Newar ontology in the literature) and **sound semantic engineering** (OWL-RL-consistent, richly CIDOC-CRM/PROV-O-aligned, SHACL-validated, fully documented, LinkML-generated). It is a strong conceptual fit for the special issue.

It is **not yet submission-ready**, and the reasons are almost entirely about *resource-paper hygiene*, not the ontology itself: the persistent identifier is not live, there is no archival DOI, the demonstrator ABox is missing from the repository, full DL reasoning is promised rather than shown, and the resource is a *schema* rather than a *populated knowledge graph*. These are the exact dimensions TGDK's resource-article track and a competent reviewer will scrutinise. All are fixable in roughly 2–4 weeks without redesign.

**Recommendation: do Group A (mandatory) and most of Group B (below) before submitting.**

---

## 2. Fit against the TGDK resource-article bar

TGDK resource articles are judged on **Relevance, Scope, Completeness, Clarity**, must describe a **novel resource that adds value over existing ones**, and must carry a **Resource Availability Statement** (sources: [TGDK CfP](https://tgdk.org/cfp.html), [TGDK submit](https://tgdk.org/submit.html), [Dagstuhl TGDK](https://www.dagstuhl.de/en/publishing/series/details/TGDK)).

| Criterion | Status | Notes |
|---|---|---|
| Relevance (SI scope) | ✅ Strong | Ontology engineering for humanities, CIDOC-CRM extension, FAIR+CARE, provenance, KG construction — all explicit SI topics. |
| Novelty / adds value | ✅ Strong | No existing Nepal/Guthi/Newar/living-heritage ontology found; four patterns are new combinations over CRM. |
| Scope clearly defined | ✅ Good | Living heritage of the Kathmandu Valley; well-bounded. |
| Completeness | ⚠️ Partial | Related work omits actor/social-role ontologies (Nampi, CRMsoc); comparison is feature-checkmarks only. |
| Clarity | ✅ Good | Writing is clear (sections 1–3 at Q1 standard after revision). |
| Resource Availability Statement | ⚠️ Present but **partly untrue** | Statement exists, but the w3id IRI is not live and the cited ABox is absent (see Group A). |

---

## 3. The bar set by published cultural-heritage ontologies

What strong CH ontology/resource papers (ArCo, Polifonia, OntoAndalus, CRMrp, Nampi) typically deliver, and where HeritageGraph stands:

| Expectation of a published CH resource | Typical exemplars | HeritageGraph |
|---|---|---|
| Persistent, **dereferenceable** IRI w/ content negotiation | ArCo, Polifonia (w3id live) | ⚠️ w3id namespace chosen but **not live** |
| **Archival DOI** (Zenodo/figshare), versioned | ArCo, Polifonia | ❌ none |
| **Human-readable HTML docs** (WIDOCO/LODE) | ArCo, Polifonia, OntoAndalus | ⚠️ docs/ exists; not WIDOCO-grade / not hosted |
| **Populated knowledge graph** (not just schema) | ArCo (~M triples), Polifonia | ❌ schema + 64 enum individuals + tiny demo |
| Reasoning **consistency (HermiT/Pellet)** | all | ⚠️ OWL-RL shown; HermiT promised via CI |
| **OOPS!** pitfall scan | most | ✅ done (independently reproduced) |
| **FOOPS!** FAIR score | increasingly expected | ❌ not reported |
| **Competency questions** + SPARQL | all | ✅ schema-level; ⚠️ instance answers thin |
| **Alignment** to CRM/standards | all | ✅ strong (CRM, PROV, AAT, EDM, …) |
| **Adoption / use case / uptake** | ArCo (MiBACT), Polifonia | ❌ none yet |
| **License** (data + code) | all | ⚠️ CC-BY on ontology; code license unstated |

**Reading:** HeritageGraph matches the bar on *design, alignment, documentation-completeness, OOPS, and reasoning-coherence*, but trails on the **"is it a real, citable, persistent, populated, independently-usable resource"** axis — which is precisely what a *resource* paper is graded on.

---

## 4. Verified strengths (from my independent run)

- **Coherent and inferential**: OWL-RL closure 5,049 → 25,353 triples (20,304 inferred); **0 unsatisfiable classes**.
- **Well-formed**: 70 classes, 123 object + 47 datatype properties, depth-4 hierarchy, 9 enumerations/64 values, 18 inverse assertions, 273/176 cardinality restrictions.
- **Fully documented**: 70/70 classes have label + definition; 100/123 obj-prop and 41/47 dat-prop ranges.
- **Interoperable**: alignments to CIDOC-CRM (32 cls / 62 props incl. subproperty chain), PROV-O (3/9), AAT (11), EDM (7), Wikidata (6), Schema.org (5), +more.
- **Validated**: 61 SHACL node shapes / 722 property constraints; pySHACL confirms they actively enforce required fields.
- **FAIR metadata header present**: `dct:title`, `dct:creator`, `dct:publisher`, `dct:license` (CC-BY-4.0), `pav:version` 1.0.0, `owl:versionIRI`, 6 `owl:imports`.
- **Reproducible engineering**: LinkML single source → OWL/SHACL/ShEx/JSON-Schema/Python.

---

## 5. Detailed gap analysis (prioritised)

### Group A — Mandatory before submission (these will sink the paper if left)

| # | Gap | Why it blocks | Fix |
|---|---|---|---|
| A1 | **Persistent IRI not live** (`w3id.org/heritagegraph/` does not resolve; PR not opened) | FAIR Findability/Accessibility fail; the Resource Availability Statement is currently false | Open the w3id PR with content negotiation; verify it resolves to TTL/HTML |
| A2 | **No archival DOI** | Resource papers require a citable, versioned, immutable archive; GitHub ≠ archive | Mint a **Zenodo DOI** for a tagged `v1.0.0` release; cite it in the paper |
| A3 | **Demonstrator ABox missing** (`examples/kathmandu-mini-abox.ttl` + queries absent from repo/zip/git) | Instance-level evaluation is irreproducible; "ABox available" claim untrue | Restore the files **or** ship the in-script synthetic ABox (`eval_hg.py`) and cite it |
| A4 | **HermiT DL consistency only promised** | OWL-RL ≠ full DL; headline "consistent" claim under-evidenced | Run HermiT (Docker has Java) over the import closure; archive + cite the log |

### Group B — Strongly recommended (a serious reviewer will expect these)

| # | Gap | Fix |
|---|---|---|
| B1 | **No FOOPS! FAIR score** | Run [FOOPS!](https://foops.linkeddata.es/) once the IRI is live; report the score; fix flagged items (missing `vann:preferredNamespacePrefix`, `dct:description`, etc.) |
| B2 | **Schema, not a populated KG** | Publish a real exemplar dataset (e.g., 1–2 fully modelled sites: Kasthamandap + Kumari Ghar with rituals, Guthi, provenance) — even a few hundred curated triples materially raises a *resource* paper |
| B3 | **HTML documentation not WIDOCO-grade/hosted** | Generate WIDOCO docs; host at the w3id HTML endpoint |
| B4 | **Alignment counting ambiguous** (paper 68/59/14 vs my 42/73/13) | State methodology; report *distinct* counts + note direct-reuse vocabularies (GeoSPARQL, DataCite) |
| B5 | **Code license unstated** | Add an OSI license (e.g., Apache-2.0/MIT) to scripts; keep CC-BY for the ontology |
| B6 | **No registry presence** | Submit to **LOV**; mention BioPortal/`prefix.cc` status |

### Group C — Scholarly strengthening (raises from "accept-with-revisions" toward "strong accept")

| # | Gap | Fix |
|---|---|---|
| C1 | Related work omits **actor/social-role + provenance ontologies** (Nampi, CRMsoc, PROV extensions) | Add them; sharpen why Guthi/role modeling is novel beyond them |
| C2 | Comparison is **feature checkmarks only** | Add at least one qualitative or quantitative axis (expressivity, axiom counts, or a worked modelling example competitors cannot capture) |
| C3 | **No multilingual labels** (Nepali/Newari) | Add `skos:prefLabel`@ne / @new for key terms — expected for CARE + DH |
| C4 | **No adoption / use case** | One realistic integration narrative (e.g., mapping a DANAM record, or an Europeana-via-EDM exposure demo) |
| C5 | **Disjointness entirely SHACL-side** | Defensible, but consider adding `owl:disjointWith` for at least the five core event classes to strengthen the DL story (you already argue it's future work) |

---

## 6. Likely reviewer objections — and current readiness

1. **"This is a schema, not a knowledge graph."** ← highest risk for a *resource* paper. Mitigate with B2 (populated exemplar) + A3.
2. **"The resource isn't actually available/persistent."** ← A1 + A2.
3. **"Evaluation is schema self-validation."** ← add populated-CQ answers, FOOPS (B1), HermiT (A4).
4. **"Novelty over existing CRM extensions?"** ← C1 + C2; your novelty is real but currently under-defended against actor/social ontologies.
5. **"CARE is aspirational."** ← honest in the paper; strengthen with C3 + a governance sentence.

---

## 7. Bottom line + effort

- **Conceptually and technically, HeritageGraph is publishable** in this venue.
- **As a *resource*, it is not yet ready**: it must become *live, citable, populated, and independently reproducible*.
- **Effort to submission-ready**: Group A ≈ a few days (DOI, w3id PR, restore/ship ABox, run HermiT); Group B ≈ 1–2 weeks (populated exemplar, FOOPS, WIDOCO, alignment note); Group C optional but high-value.

**If you do Group A + B1–B4, this is a defensible submission with a realistic shot at "accept with minor/major revisions."** Group C is what would push reviewers toward enthusiasm.
