# Reference papers — closest peers to HeritageGraph

Downloaded 2026-06-27 to ground a research-grade rewrite of the **High-Level
Architecture** subsection of the HeritageGraph paper (`tgdk-overleaf/main.tex`,
§ Ontology Description). The **closest 10 papers** to HeritageGraph — CIDOC-CRM
extensions, cultural-heritage ontologies, provenance/iconography/event design
patterns, and the methodology authorities its architecture should answer to.
Selected from the `/deep-research` source set plus targeted follow-up search.

## Core architecture-description peers (the funnel models)

| File | Paper | Why it matters here |
|------|-------|---------------------|
| `SeaLiT_Ontology_CIDOC-CRM_2023.pdf` | The SeaLiT Ontology – An Extension of CIDOC-CRM for Maritime History (arXiv 2301.04493 = JOCCH 10.1145/3586080) | **Closest peer.** A CIDOC-CRM extension that uses the exact funnel we want: (1) characterise CRM's paradigm → (2) state the extension principle (every class is a subclass/descendant of a CRM class) → (3) name the endurant/perdurant backbone → (4) justify *why* CRM (standard, integration, sustainability). |
| `ArCo_KnowledgeGraph_Carriero2019.pdf` | ArCo: the Italian Cultural Heritage Knowledge Graph (arXiv 1905.02840) | Modular **network of 7 ontology modules** connected by `owl:imports`; names a top-level module, a generic-relations core, and thematic modules; distinguishes **direct vs indirect reuse**; justifies modularity (readability/reusability/maintainability). Model for how to *name and rationalise* layers. |
| `ArCo_PatternBasedDesign_2019.pdf` | Pattern-based design applied to CH knowledge graphs (arXiv 1911.07585) | ArCo's ODP/eXtreme-Design treatment; the "root–thematic–foundations" layering pattern. |
| `EDM_Primer_Europeana.pdf` | Europeana Data Model (EDM) Primer | Funnel via explicit **design principles + requirements** before classes; explicitly contrasts object-centric vs event-centric description (the contrast HeritageGraph asserts). |

## Methodology / foundational authorities

| File | Paper | Why it matters here |
|------|-------|---------------------|
| `OntoClean_Overview_GuarinoWelty.pdf` | An Overview of OntoClean (Guarino & Welty) | Metaproperties (rigidity, identity, unity) for *justifying* subsumption choices — directly relevant to defending `RitualEvent ⊑ E7_Activity` and the anti-rigid **role/tenure** modelling (LivingGoddessTenure). |
| `Modularization_CIDOC-CRM_FOIS2020.pdf` | Ontological Analysis and Modularization of CIDOC-CRM (FOIS 2020, LOA-ISTC) | Authority for describing CRM's endurant/perdurant top level and principled modularisation. |

## Domain peers — extension/sub-domain ontologies HeritageGraph touches

| File | Paper | Why it matters here |
|------|-------|---------------------|
| `CRMdig_DigitalProvenance_Doerr2011.pdf` | CRMdig: A Generic Digital Provenance Model for Scientific Observation (Doerr & Theodoridou, TaPP 2011) | The canonical CRM provenance extension — peer model for HeritageGraph's **provenance layer** (`HeritageAssertion`, `DataSource`, `Verification`). |
| `IntangibleCH_OntologyDesign_CIDOC.pdf` | The Ontology Design of Intangible Cultural Heritage Based on CIDOC-CRM (IJUNESST 2014) | A prior CIDOC-CRM model of *intangible* heritage — the nearest direct precedent for HeritageGraph's living/performative scope; useful as contrast in related work. |
| `ICON_Ontology_ArtisticInterpretation_Sartini2023.pdf` | ICON: An Ontology for Comprehensive Artistic Interpretations (Sartini et al., JOCCH 2023) | Panofsky-based iconography/iconology + symbolism — peer for HeritageGraph's `IconographicObject` (`Murti`, `Paubha`), `depicts_deity`, and syncretic/symbolic modelling. |
| `ODP_RecurrentSituations_2021.pdf` | An Ontology Design Pattern for Representing Recurrent Situations (arXiv 2101.00286) | ODP for recurrence — peer for HeritageGraph's `recurrence_pattern` / `lunar_date_tithi` festival modelling. |

**Not retrieved (blocked, fetch manually in a browser if wanted):**
- LACRIMALit (MDPI *Information* 13(8):398) — Cloudflare/JS challenge. Open-access
  (CC-BY): <https://www.mdpi.com/2078-2489/13/8/398>. Most tangential of the set.
- Doerr (2003), *The CIDOC CRM* (AI Magazine 24(3)) — the foundational paper
  HeritageGraph extends (cited as `Doerr_2003`); AAAI OJS is erroring and no clean
  open PDF resolved. <https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/1720>
- Theodoridou et al. (2010), *Modeling and querying provenance by extending
  CIDOC CRM* (Springer DPDB) — paywalled.

**Caveat on the deep-research run:** the verification pass aborted on a session
limit, so its claims came back "0–0 / refuted" — that means *unverified*, not
*false*. The architecture facts above were re-confirmed directly from the
downloaded PDFs (see quotes in `PROPOSED-CHANGES.md`).
