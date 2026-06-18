# HeritageGraph at Q1 Standard? A Comparative Gap Analysis Against ArCo, Polifonia, and Venue Criteria

*Synthesis Report — Phase 3 (Analysis). Evidence-grounded comparison of the HeritageGraph ontology against the success factors of Q1-published cultural-heritage (CH) ontologies (Semantic Web journal, ISWC resources, TGDK), with a prioritised improvement roadmap. All claims trace to the supplied evidence and the independent-evaluation facts; no figures or sources are invented.*

---

## A. Executive Summary

On **interoperability breadth**, HeritageGraph is genuinely strong and near Q1: it carries external alignment axioms on 42 distinct classes + 73 distinct properties across ~13–14 vocabularies, with deep CIDOC-CRM coverage (32 classes / 62 properties incl. a subproperty chain), plus PROV-O, Getty AAT, EDM, Wikidata, Schema.org, CRMinf/CRMsci, and OWL-Time. But on **interoperability as the exemplars practise it** — and on the resource's overall publication readiness — it is **not yet at Q1 standard**. The two Q1 exemplars succeeded not on alignment counts but on a bundle HeritageGraph lacks: ArCo shipped a *populated* knowledge graph (~169M triples / ~820k entities) with a live SPARQL endpoint and third-party consumer requirements (ISWC 2019); Polifonia shipped a *modular* network of 15 ODP-based modules with four foundational interoperability modules (ISWC 2023). HeritageGraph is a **schema, not a populated KG** (~79-triple demonstrator ABox), is **not modular**, is **not grounded in a foundational ontology** (no DOLCE/BFO, no OntoClean), has **no third-party use** (the Semantic Web journal makes evidenced third-party usefulness a *required* criterion), and its **persistent IRI is not live** (w3id.org A1 dereferenceability unmet) — alongside fixable defects (disjointness dropped in OWL generation, 33 self-referential SKOS mappings). Its distinctive novelty (no competing Nepal/Guthi/Newar living-heritage ontology) and its demonstrated conflict-aware provenance layer are real Q1-grade assets; the gap is execution of the resource bundle, not the modelling.

---

## B. The Q1 Success-Factor Framework

Derived from the supplied evidence — ArCo (ISWC 2019), Polifonia/PON (ISWC 2023), foundational-grounding literature, Ferrario & Grüninger (2020) publishing guidelines, Semantic Web journal author criteria, and TGDK resource-article criteria. Ten named factors; for each, what the exemplars did and the crisp Q1 bar.

### F1. Populated knowledge graph + scale
- **Exemplars:** ArCo is a *populated* KG of **~169 million triples over ~820,000 cultural entities** — not just a schema. Semantic Web journal requires that datasets used in applications be **deposited in repositories**.
- **Q1 bar:** A substantive, queryable instance graph at real scale exists and is deposited — the ontology is demonstrated *in use over data*, not only in the abstract.

### F2. Demonstrated third-party use / usefulness
- **Exemplars:** ArCo elicited requirements from **both** the data provider (ICCD) **and** a community of independent **consumer** organisations. Semantic Web journal makes **usefulness shown by third-party uses an evidence-REQUIRED criterion**. TGDK requires a resource that **adds value over existing ones**.
- **Q1 bar:** Independent (non-author) adoption or use is documented with evidence.

### F3. Modularity + ontology design patterns (ODPs)
- **Exemplars:** ArCo is a **network of 7 modular ontologies**; Polifonia is **strongly modular (15 thematic modules with explicit dependencies)** built on reusable **ODPs** plus a Core pattern module.
- **Q1 bar:** The resource is decomposed into versioned, dependency-explicit modules and/or packaged design patterns enabling partial reuse.

### F4. Foundational grounding + OntoClean
- **Exemplars:** Foundational ontologies (**DOLCE, BFO**) and **OntoClean** are standard for maximising interoperability; DOLCE has grounded/improved CIDOC-CRM and CH ontologies (e.g., OntoAndalus grounds specialization in DOLCE+DnS Ultralite). Polifonia ships **four abstract "foundational" modules** providing network-wide interoperability.
- **Q1 bar:** Top-level categories are aligned to a foundational ontology and/or cleaned with OntoClean, justifying category choices.

### F5. Alignment to upper/standard domain ontologies
- **Exemplars:** ArCo aligned to **CIDOC-CRM and EDM**. Semantic Web journal notes **alignment to upper ontologies enhances interoperability**.
- **Q1 bar:** Systematic, axiom-level alignment to the recognised standard ontologies of the domain.

### F6. FAIR + persistent identifier + DOI
- **Exemplars:** Polifonia is **FAIR + open source**. Semantic Web journal requires **provenance + appropriate license** and **repository deposit**.
- **Q1 bar:** FAIR-compliant, with a **live dereferenceable persistent IRI** and an archival DOI (e.g., Zenodo).

### F7. Tooling, endpoint, and documentation suite
- **Exemplars:** ArCo shipped a **live SPARQL endpoint**, **catalogue-record-to-RDF conversion software**, and a **rich documentation suite** (testing, evaluation, how-to, examples). Polifonia shipped an **NLP toolkit** for CQs. TGDK mandates a **Resource Availability Statement**.
- **Q1 bar:** Live endpoint and/or hosted HTML docs, supporting tooling, and a complete, navigable documentation suite.

### F8. Stakeholder-driven competency-question rigour
- **Exemplars:** Polifonia placed **heavy emphasis on stakeholder CQs** plus an **NLP toolkit to generate/validate CQs**, developed via the agile **eXtreme Design (XD)** methodology; ArCo elicited requirements from provider + consumers.
- **Q1 bar:** CQs sourced from diverse stakeholders (incl. consumers) and validated **against populated data (ABox-level)**, not only the schema.

### F9. Provenance + license (reuse readiness)
- **Exemplars:** Semantic Web journal **requires provenance + an appropriate license** for reuse.
- **Q1 bar:** Explicit provenance modelling and an open, reuse-permitting license are present and demonstrated.

### F10. Quality, stability, and reproducibility (per Ferrario & Grüninger 2020)
- **Exemplars / standard:** Semantic Web journal requires **quality and stability of the resource (evidence required)** and **clarity/completeness**; **Ferrario & Grüninger (2020)** is the reference standard for what an ontology paper must contain; TGDK requires **relevance, scope, completeness, clarity**.
- **Q1 bar:** Logically consistent, stable, completely documented and reproducibly evaluated, with no generation defects between source and published artifacts.

---

## C. Factor-by-Factor Scorecard

| # | Factor | Rating | One-line justification (grounded in the facts) |
|---|--------|--------|------------------------------------------------|
| F1 | Populated KG + scale | **Missing** | Schema only; ~79-triple demonstrator ABox, no large dataset — vs ArCo's ~169M triples / ~820k entities. |
| F2 | Third-party use / usefulness | **Missing** | No third-party adoption/use case; requirements from community/Guthi experts but NOT an independent data-consumer org — the SWJ-required evidence is absent. |
| F3 | Modularity + ODPs | **Missing** | Single LinkML schema; not modular, no packaged ODPs — vs ArCo (7 modules) / Polifonia (15 modules + ODPs). |
| F4 | Foundational grounding + OntoClean | **Missing** | No DOLCE/BFO grounding, no OntoClean — the standard interoperability-maximising step is unperformed. |
| F5 | Alignment to upper/standard ontologies | **Strong** | 42 classes + 73 properties carry alignment axioms over ~13–14 vocabularies; CIDOC-CRM 32 classes/62 props incl. subproperty chain; PROV-O, AAT, EDM, Wikidata, Schema.org, CRMinf/sci, OWL-Time. |
| F6 | FAIR + persistent ID + DOI | **Partial** | CC-BY-4.0, owl:versionIRI, FOOPS-style 12/12 metadata — BUT w3id.org IRI not live (A1 unmet), no Zenodo DOI, no LOV registration. |
| F7 | Tooling / endpoint / docs | **Partial** | LinkML multi-format generation (OWL/SHACL/ShEx/JSON-Schema/Python) is strong tooling; but no live SPARQL endpoint, no hosted WIDOCO HTML docs. |
| F8 | Stakeholder-driven CQ rigour | **Partial** | 32 CQs via NeOn methodology from Guthi/community experts; BUT CQ validation largely TBox-level and no consumer-org stakeholder. |
| F9 | Provenance + license | **Strong** | HeritageAssertion dual-aligned crminf:I2_Belief + prov:Entity, demonstrated by a real query returning two conflicting, source-attributed claims; CC-BY-4.0 present. |
| F10 | Quality / stability / reproducibility | **Partial** | HermiT consistent, 0 unsatisfiable classes (~1.3s); 61 SHACL shapes / 722 constraints; 4/4 negative tests pass — BUT disjointness (45 classes) DROPPED by the OWL generator (0 owl:disjointWith), 33 self-referential SKOS mappings, multilingual labels absent. |

**Tally:** Strong = 2 (F5, F9); Partial = 4 (F6, F7, F8, F10); Missing = 4 (F1, F2, F3, F4).

---

## D. The Interoperability Deep-Dive

Interoperability is HeritageGraph's headline strength *and* its clearest structural gap — depending on which dimension is measured.

**Where HeritageGraph is genuinely strong (alignment breadth — F5, F9):**
- **Axiom-level alignment density:** 42 distinct classes + 73 distinct properties carry external alignment axioms — this is real, machine-actionable interoperability, not a mapping spreadsheet.
- **Deep CIDOC-CRM commitment:** 32 classes / 62 properties incl. a subproperty chain — matching the *standard-ontology alignment* that ArCo built on (CIDOC-CRM + EDM). HeritageGraph aligns to EDM (7) as well, so on the specific axis ArCo used, HeritageGraph is comparable.
- **Breadth across the LOD ecosystem:** PROV-O, Getty AAT (11), Wikidata (6), Schema.org (5), DBpedia, CRMinf, CRMsci, FOAF, OWL-Time, RICO, DCTerms — wide reuse-surface.
- **Provenance interoperability (F9):** the crminf:I2_Belief + prov:Entity dual-alignment, *demonstrated* by a live query returning two conflicting source-attributed claims, is a Q1-grade interoperability feature ArCo's description does not emphasise.

**Where HeritageGraph lags the exemplars on interoperability:**
1. **No foundational grounding (F4).** ArCo and Polifonia treat top-level coherence as load-bearing; DOLCE/BFO + OntoClean are the documented route to *maximising* interoperability, and Polifonia ships four foundational modules precisely for cross-network interoperability. HeritageGraph aligns *outward* to many vocabularies but is not anchored *upward* to a foundational backbone — so its interoperability is breadth without depth-of-category-justification.
2. **Not modular (F3).** Interoperability in ArCo (7 modules) and Polifonia (15 modules + ODPs, explicit dependencies) is partly *delivered through modular reuse*: a consumer can adopt one module. HeritageGraph's single schema cannot be partially reused; there are no packaged ODPs to import.
3. **No populated KG to interoperate WITH (F1).** Alignment axioms are necessary but the *value* of interoperability is realised over instance data. ArCo's ~169M triples / ~820k entities make its alignments exploitable at scale; HeritageGraph's ~79-triple ABox cannot demonstrate cross-vocabulary querying in practice.
4. **Persistent ID not live (F6).** Interoperability presupposes dereferenceability. The w3id.org IRI is not live (A1 unmet) — external agents cannot resolve HeritageGraph terms, undercutting the alignment work that is otherwise its strength.
5. **Generation defect undermining the TBox (F10).** Disjointness for 45 classes was authored in YAML but **dropped by the LinkML OWL generator** (0 owl:disjointWith in OWL). Disjointness axioms are part of what makes a CIDOC-CRM-aligned ontology safely interoperable under reasoning; losing them weakens the logical guarantees a reuser relies on. The 33 self-referential SKOS mappings are a related interoperability defect.

**Net:** HeritageGraph wins the *alignment-breadth* sub-dimension and the *provenance-interoperability* sub-dimension, but loses the *foundational-grounding*, *modular-reuse*, *interoperate-at-scale*, and *dereferenceability* sub-dimensions that distinguish ArCo/Polifonia. Interoperability counts are Q1-grade; interoperability *as deliverable practice* is not yet.

---

## E. Prioritised Improvement Roadmap to Reach Q1

### Tier 1 — Mandatory (cross the Q1 threshold; without these, desk-reject risk on stated venue criteria)

| Action | Motivated by |
|--------|-------------|
| **Make the w3id.org persistent IRI live and dereferenceable** (resolve A1); register so terms resolve to docs/RDF. | Semantic Web journal reuse requirements; FAIR (F6). Cheapest fix with the highest reuse impact. |
| **Fix the disjointness generation defect** — ensure the 45 authored disjoint classes emit owl:disjointWith in OWL; re-run HermiT to confirm consistency holds. | Ferrario & Grüninger (2020) quality/completeness; SWJ stability "evidence required" (F10). |
| **Remove the 33 self-referential SKOS mappings.** | SWJ clarity/quality; FOOPS/FAIR mapping correctness (F10). |
| **Mint an archival DOI (Zenodo) and add a Resource Availability Statement; deposit artifacts in a repository.** | TGDK mandatory Resource Availability Statement; SWJ repository-deposit requirement (F6). |
| **Populate a substantive ABox** beyond the ~79-triple demonstrator — even a curated Kathmandu Valley subset (temples, Guthi, festival cycles) at meaningful scale, deposited. | ArCo's ~169M-triple populated KG; SWJ dataset-deposit (F1). |

### Tier 2 — Strongly recommended (move from "acceptable" to "competitive")

| Action | Motivated by |
|--------|-------------|
| **Modularise** the single schema into dependency-explicit modules (e.g., core / heritage-object / ritual-festival / Guthi-institution / belief-provenance) and/or package reusable ODPs. | ArCo (7 modules); Polifonia (15 modules + ODPs) (F3). |
| **Host HTML documentation** (WIDOCO) and stand up a **live SPARQL endpoint** over the populated ABox. | ArCo's endpoint + documentation suite; TGDK availability (F7). |
| **Elevate CQ validation to the ABox level** — run the 32 CQs as SPARQL over the populated data, not just TBox checks. | Polifonia stakeholder-CQ + NLP toolkit rigour; XD methodology (F8). |
| **Register in LOV.** | LOD discoverability / FAIR findability (F6/F7). |
| **Secure and document at least one independent third-party use** (e.g., a museum, archive, or Guthi-data org consuming the ontology). | SWJ usefulness "evidence required"; ArCo provider+consumer model (F2). |

### Tier 3 — Excellence (distinguish for the top venues)

| Action | Motivated by |
|--------|-------------|
| **Ground the top-level categories in a foundational ontology (DOLCE or BFO) and apply OntoClean.** | Foundational-grounding literature; OntoAndalus/DOLCE precedent; Polifonia foundational modules (F4). |
| **Add multilingual (Nepali/Newari) labels.** | Completeness/clarity + accessibility for the living-heritage community; novelty positioning (F10). |
| **Add an independent data-consumer organisation to requirements elicitation** for the next iteration. | ArCo's dual provider+consumer requirements model (F2/F8). |
| **Publish a conversion/ingestion tool** (record → RDF) to lower adoption cost. | ArCo's catalogue-record-to-RDF conversion software (F7). |

---

## F. The Single Highest-Leverage Change

**Populate the ontology into a real, deposited knowledge graph and expose it via a live SPARQL endpoint behind a live persistent IRI (combining F1 + F6 + F7).**

Rationale grounded in the evidence: the single sharpest discriminator between HeritageGraph and the two Q1 exemplars is that **ArCo and Polifonia are resources-in-use, while HeritageGraph is a schema**. HeritageGraph already has the hardest parts done — consistent reasoning, dense standard-ontology alignment (42 classes + 73 properties), a demonstrated conflict-aware provenance layer, and a novelty no competitor holds (no Nepal/Guthi/Newar living-heritage ontology exists). What it cannot currently show is its alignments and CQs *working over data at scale*. A populated, queryable, dereferenceable KG simultaneously: (i) satisfies the SWJ dataset-deposit and stability criteria, (ii) makes the third-party-usefulness requirement (F2) achievable because there is finally something usable to adopt, (iii) lets the 32 CQs be validated at the ABox level (F8), and (iv) turns the strong-but-currently-latent alignment breadth (F5) into demonstrable interoperability (D). It converts a strong schema into a publishable resource — which is precisely the transition ArCo and Polifonia made.

---

## Synthesis Limitations

- This analysis uses ONLY the supplied evidence and the single independent-evaluation fact set; no external figures or sources were introduced, and exemplar details are limited to what the provided sources state (e.g., ArCo/Polifonia internals beyond the cited success factors are out of scope).
- Venue criteria are taken at the level the supplied sources describe; specific reviewer thresholds for each venue may vary beyond the stated public criteria.
- HeritageGraph's profile is a snapshot from one independent evaluation; defects flagged (e.g., the LinkML OWL-generation drop of disjointness) are reported as found and may be resolved by configuration changes not captured here.
- "Q1 standard" is operationalised here through the ten derived success factors; it is a structured rubric, not a guarantee of acceptance, which depends on review.
