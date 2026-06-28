# How to structure the "Ontology Description" section — expanded analysis

Section-level analysis grounded in (a) the **authoritative venue checklist** for
ontology-description papers, and (b) a **16-paper corpus** spanning cultural heritage
*and* other domains. Method: web-sourced the venue spec + `pdftotext` heading-mining of
each paper's *describe-the-ontology* section. PDFs are in `reference-papers/` and
`reference-papers/desc-section-corpus/`. Loci cited so claims are checkable.

---

## 0. The normative target — Semantic Web Journal "Ontology Description" checklist

The SWJ defines a dedicated *Descriptions of Ontologies* paper type. Its author
guidance is the closest thing to a standard for this exact section. Verbatim-distilled,
a description must report:

- **Design principles & methodology** of creation/maintenance.
- **Identity & availability:** name, URL/namespace, version date & number, **licensing**, availability (open/accessible preferred).
- **Scope & provenance:** topic coverage, source of the data, purpose, **reported usage**.
- **Metrics & statistics:** internal/external connectivity, **use of established vocabularies** (RDF/OWL/SKOS/FOAF…), **language expressivity** (OWL profile), growth.
- **Modeling patterns:** examples + **critical discussion of typical knowledge-modeling patterns** used.
- **Known shortcomings / limitations.**
- **Comparison** with other ontologies on the same topic.
- **Pointers to applications / use-case experiments.**

Review dimensions: (1) *quality & relevance* with convincing evidence; (2) *illustration,
clarity & readability* that conveys the key aspects; (3) *openness/accessibility*.
Source: <https://www.semantic-web-journal.net/authors>.

> This checklist becomes the scoring rubric in §3.

---

## 1. Corpus — how 16 papers organise the description (CH + beyond)

### Cultural-heritage / CIDOC-CRM cluster
| Paper | Description-section structure (locus) | Organising principle |
|-------|----------------------------------------|----------------------|
| **SeaLiT** | §4 roadmap → 4.1 Overview (counts+scope+figures) → 4.2 *single evolving example* → 4.3 specification + RDFS/OWL | overview → example → specification |
| **ArCo (KG)** | network of **7 modules**, each = namespace+scope+reused ODPs → FAIR → CQ evaluation | module-by-module + reuse + CQ |
| **ArCo (patterns)** | **pattern-by-pattern**: requirement → pattern → numbered axioms → direct/indirect reuse | uniform per-pattern template |
| **ICON** | §5 **construct-by-construct** (Recognitions/Interpretations/Subjects/Symbols/Style/Sources), each = requirement + theory + reuse; one example across ICON/VIR/Wikidata = comparison | construct-by-construct + single example=comparison |
| **EDM Primer** | design principles (D1–D3) + requirements (R1–R7) → core → contextual classes | principles/requirements → classes |
| **Intangible-CH/CIDOC** | construction method → faceted classes → CRM mapping | method → facets → mapping |
| **Recurrent-Situations ODP** | problem → abstract pattern → implementations → examples + **CQ table** | problem→pattern→impl→example+CQ |
| **CRMdig** | motivation → model (provenance classes) → examples | motivation→model→example |
| **CH-LOD Ontologies Review (ISPRS 2023)** | *survey*: compares CIDOC-CRM/EDM/ArCo/… along coverage axes | comparison framing (useful for our §3.8) |
| **HERITRACE (2025)** | data model → **provenance management & change-tracking** → discussion | provenance-centric |
| **POI Cultural Heritage (Nature HS)** | requirements → data model → application at a CH site | requirements→model→application |
| **Aldrovandi FAIR 3D (2024)** | FAIR principles → metadata model/crosswalks → methodology → records | FAIR-led |

### Beyond cultural heritage (cross-domain check)
| Paper | Structure (locus) | Organising principle |
|-------|-------------------|----------------------|
| **PWO — Publishing Workflow Ontology (SWJ)** | Intro → background → §3 **sub-pattern-by-sub-pattern** (Participation/Sequence/Control-flow/Time-indexed-situation/Error) → §5 **applied worked cases** (Submission→Reviewing→Decision→Revision; legislative case) → Conclusion | construct-by-construct + applied examples |
| **InBiodiv-O — Biodiversity (2021)** | related work → **methodology** → **evaluation of the ontology** (CQs/metrics) | method + evaluation-forward |
| **ODP for Annotation (SWJ)** | motivation → **patterns** → applying the patterns → **lessons learned** | pattern + lessons/shortcomings |
| **FIBO (finance)** | two tiers: **core domains** + operational **modules** (11 + 49) | layered modular |
| **FaBiO (SPAR, bibliographic)** | classes structured by a backbone schema (FRBR Work/Expression/Manifestation/Item) | backbone-driven taxonomy |

---

## 2. Distilled template (holds across CH *and* cross-domain, and matches §0)

1. **Roadmap sentence** opening the section. *(SeaLiT, EDM, Recurrent, PWO)*
2. **Overview first:** scope + size counts + a structural figure. *(SeaLiT, ArCo, EDM, InBiodiv-O)*
3. **Requirements / competency questions surfaced up front.** *(ICON, ArCo, EDM, Recurrent, PWO)*
4. Content **module/pattern/construct-by-construct under ONE uniform mini-template**: motivation → standard reuse/mapping → formal axioms → CQ → example. *(ArCo×2, ICON, PWO, Recurrent)*
5. **One running worked example threaded through** (often reused for comparison). *(SeaLiT 4.2, ICON Figs 6–9, PWO §5)*
6. **Identity, availability & specification** (name/IRI/version/license/serialisations/FAIR). *(SWJ checklist, SeaLiT 4.3, ArCo, Aldrovandi)*
7. **Known shortcomings/limitations** stated as part of the description. *(SWJ checklist, ODP-Annotation "lessons learned")*
8. **Comparison with existing ontologies** + **pointers to applications/usage**. *(SWJ checklist, ICON, ArCo, CH-LOD review)*

---

## 3. HeritageGraph §3 scored against the SWJ checklist (the actionable gap map)

Current order: intro → 3.1 Architecture → 3.2 Metrics & Standards → 3.3–3.6 patterns → 3.7 Epistemic Provenance → 3.8 Comparison.

| SWJ checklist item | HeritageGraph status | Action |
|---|---|---|
| Design principles & methodology | ✅ (Methodology §, 3.1 paradigm) | — |
| Name / IRI / version | ⚠️ IRI+v1.0.0 only in 3.2 prose | R4 |
| **Licensing** | ❌ not stated in §3 | **R4** (repo has LICENSE: CC-BY-style) |
| Availability (open) | ⚠️ implicit (w3id) | R4 |
| Topic coverage / source | ✅ (3.1, Methodology) | — |
| **Reported usage / applications** | ⚠️ only in Evaluation (LUX case) | R8 pointer from §3 |
| Metrics & statistics | ✅ 3.2 (strong) | R6 (placement) |
| Use of established vocabularies | ✅ 3.2 (13 aligned) | — |
| Language expressivity (OWL profile) | ✅ 3.2 (OWL 2 DL) | — |
| **Modeling patterns + critical discussion** | ⚠️ present but **not uniform** across 3.3–3.6 | **R2** |
| Examples | ⚠️ present but **scattered**, not one running example | **R3** |
| **Known shortcomings** | ❌ only "Threats to Validity" in Evaluation, none in §3 | **R7** |
| Comparison | ✅ 3.8 | reuse running example (R3) |
| Roadmap clarity/readability | ⚠️ "four patterns" vs five layers | **R5** |
| **CQs surfaced up front** | ❌ CQs live only in Evaluation | **R1** |

---

## 4. Recommended section-level changes (priority-ordered, now checklist-anchored)

- **R1 — CQ frame in the §3 intro** *(High/Low).* Name the four CQ themes + point to the 32 CQs in Evaluation. Closes "CQs up front" (template #3) and grounds the CQ-IDs the subsections now cite.
- **R2 — Uniform per-pattern template across 3.3–3.6** *(High/Med).* Same five beats, same order: motivation → CRM reuse → axiom Listing → CQ → example. Closes "critical discussion of patterns" (template #4). Syncretic still needs an axiom Listing.
- **R3 — One running example threaded through** *(High/Med).* Introduce the Kathmandu demonstrator once (3.1), reuse the *same* instances in every ABox listing and in §3.8. Mirrors SeaLiT 4.2 / ICON / PWO §5.
- **R4 — "Availability & Specification" close** *(High/Low — now checklist-mandated).* IRI `w3id.org/heritagegraph` v1.0.0, **license**, repository, LinkML-generated OWL/SHACL/ShEx/JSON-Schema/Python, FAIR statement.
- **R5 — Fix roadmap wording** *(Low/Low).* Enumerate the actual subsections in order.
- **R6 — Reposition the heavy metrics table** *(Med/Med, judgement).* Keep headline counts in 3.1; defer the full table to the R4 availability close or to Evaluation (SeaLiT/ArCo do this).
- **R7 — A "Known limitations" sentence(s) in §3** *(Med/Low — now checklist-mandated).* A 2–3 sentence pointer to scope boundaries (e.g., Kathmandu-Valley focus, sparse domains by design), cross-ref Threats to Validity. The SWJ rubric expects shortcomings *in the description*, not only buried in evaluation.
- **R8 — Usage pointer** *(Low/Low).* One clause in §3 pointing to the LUX interoperability case study as reported usage.

---

## 5. Suggested target structure for §3

```
3  Ontology Description
   ├─ intro: roadmap (R5) + CQ-theme frame (R1) + running-example + usage pointer (R3,R8)
   ├─ 3.1 High-Level Architecture          (overview + figure + running-example intro)
   ├─ 3.2 Modeling Patterns                 (uniform template R2)
   │     3.2.1 Event-Mediated · 3.2.2 Living Goddess · 3.2.3 Syncretic · 3.2.4 Institutional
   ├─ 3.3 Epistemic Provenance              (cross-cutting layer)
   ├─ 3.4 Metrics, Availability & Specification   (R4 + R6 + R7 limitations)
   └─ 3.5 Comparison with Existing Ontologies     (reuse running example; cf. CH-LOD review framing)
```
Lighter alternative: keep the flat ordering, apply only R1+R2+R3+R4+R5+R7.

---

## 6. Corpus manifest

- **`reference-papers/`** — closest-10 set (SeaLiT, ArCo×2, ICON, EDM, CRMdig, Intangible-CH, Recurrent ODP, OntoClean, CIDOC modularization).
- **`reference-papers/desc-section-corpus/`** — PWO (SWJ), ODP-Annotation (SWJ), InBiodiv-O, HERITRACE, Cultural-Gems LOD, Aldrovandi FAIR-3D, CH-LOD review (ISPRS), POI-CH (Nature HS).
- **Venue spec:** SWJ ontology-description author guidance (web; quoted in §0).
- **Cited but not downloaded** (blocked/known): SAREF (ETSI), FaBiO/CiTO (SPAR, HTML at sparontologies.net), FIBO (EDM Council), Music Ontology — used here for the cross-domain organising-principle check only.

**Bottom line:** the expanded, cross-domain corpus *and* the SWJ venue checklist agree on
the same template, so the §1 recommendations are not CH-specific taste — they are what the
target venue's rubric asks for. R1–R5 + R7 are the high-value, low-risk first pass.
