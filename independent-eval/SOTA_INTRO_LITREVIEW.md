# How SOTA Cultural-Heritage Ontology / KG Papers Write Their Introduction and Related Work

**Purpose.** A working blueprint, distilled from real state-of-the-art cultural-heritage (CH) ontology and knowledge-graph papers, for rewriting the *Introduction* and *Related Work* of the **HeritageGraph** paper (a CIDOC-CRM / PROV-O–aligned ontology for the living cultural heritage of Nepal).

**Method note / honesty caveat.** Web fetching was disabled in the environment used to produce this document, so I could not re-pull each paper's HTML at write time. The analysis below is reconstructed from my own knowledge of these specific, well-known papers (all of which predate the knowledge cutoff and all of which appear in this repo's `main/bibliography.bib`). Where I give example sentences they are **paraphrases / reconstructions in the style of the source**, explicitly labelled `[paraphrase]`, **not** verbatim quotations. Treat the verbatim wording as needing a final check against the PDF before it goes in the paper; treat the *structural* claims as reliable. Every paper is cited with a real, resolvable URL.

**Reference set used (all real, all citable):**

- **ArCo** — Carriero et al., *ArCo: The Italian Cultural Heritage Knowledge Graph*, ISWC 2019. https://doi.org/10.1007/978-3-030-30796-7_3 · preprint https://arxiv.org/abs/1905.02840
- **Polifonia Ontology Network (PON)** — Ciroku, de Berardinis, et al., ISWC 2023 (Resources Track). https://doi.org/10.1007/978-3-031-47243-5_16 · project https://polifonia-project.eu
- **DOREMUS** — Achichi et al., *DOREMUS: A Graph of Linked Musical Works*, ISWC 2018. https://doi.org/10.1007/978-3-030-00668-6_1
- **Records in Contexts Ontology (RiC-O)** — Clavaud & Wildi, Linked Archives 2021. https://ceur-ws.org/Vol-3019/ (RiC-O home: https://www.ica.org/standards/RiC/ontology)
- **OntoAndalus** — Almeida & Costa, *OntoAndalus: an ontology of Islamic artefacts for terminological purposes*, Semantic Web Journal 12(2), 2021. https://doi.org/10.3233/SW-200391
- **NAMPI** — Vogeler et al., *Nampi: A model for collaborative…factoid prosopography*, related pubs at https://nampi.gams.uni-graz.at/
- **CRMtex** — Felicetti, Murano, et al., *CRMtex: An extension of CIDOC-CRM for ancient textual entities*, JOCCH 2021. https://doi.org/10.1145/3460249
- **CRMgeo** — Hiebel, Doerr, Eide, *CRMgeo: A spatiotemporal extension of CIDOC-CRM*, IJDL 2017. https://doi.org/10.1007/s00799-016-0192-4
- **CultureSampo** — Mäkelä, Hyvönen, Ruotsalo, Semantic Web Journal 3(1), 2012. https://doi.org/10.3233/SW-2011-0049
- **CHEDO** — Marín-Miranda et al., *An ontology to describe the damage process to built CH triggered by earthquakes*, JOCCH 2025. https://doi.org/10.1016/j.culher.2024.11.014
- **CRMrp** — Carmeliti & Catalano, *CRMrp: …conservation and restoration practice*, JOCCH 2025. https://doi.org/10.1016/j.culher.2025.02.011
- **KCHDM** — Kim et al., *…Korean Cultural Heritage Data Model*, Digital Heritage 2015. https://doi.org/10.1109/DigitalHeritage.2015.7419509

---

## 1. Introduction Blueprint

### 1.1 The recurring "move" structure

SOTA CH-ontology intros are almost never a single flowing essay. They are a **sequence of short, load-bearing moves**, each doing one job. The canonical order:

| # | Move | What it does | Typical length |
|---|------|--------------|----------------|
| M1 | **Domain hook, made concrete** | Anchors the paper in a *specific* dataset/institution/phenomenon, not "culture is important". | 2–4 sentences |
| M2 | **What the established standards already do well** | Credits CIDOC-CRM / EDM / Getty / PROV-O honestly, so the gap is not a strawman. | 2–4 sentences |
| M3 | **The specific, named gap** | One crisp limitation that the rest of the paper is organised around. Stated as a *capability the field lacks*, not as "no one has done exactly my thing". | 2–5 sentences |
| M4 | **"We present X"** | One sentence naming the resource and its one-line identity (what it is aligned to, what it covers). | 1–2 sentences |
| M5 | **Enumerated contributions** | A literal numbered/bulleted list ("Our contributions are: (1)… (2)…"). Usually 3–5 items, each a *capability*, not an activity. | a short list |
| M6 | **Approach + validation preview** | How it was built (methodology name) and how it was checked (CQs, reasoner, SPARQL, real data, uptake). | 2–4 sentences |
| M7 | **Roadmap** | "The remainder of this paper is organised as follows…" | 1 short paragraph |

**Length.** ISWC/SWJ intros run ~0.75–1.5 pages (≈ 5–8 paragraphs). They are dense but never padded.

**Citation density.** Moderate and *targeted*: M2 and M3 carry most citations (the standards being credited and the closest competitors being positioned), often 1 citation per claim rather than a `[3,7,11,15]` dump. M1 cites the data source / domain authority; M4–M6 are largely citation-free because they describe the authors' own work. Net effect: ~8–15 citations in a typical intro, clustered where they do argumentative work.

**How they state novelty without overclaiming.** The strong papers claim novelty about a **capability or a resource**, and *scope* it:
- ArCo claims to be *"the"* Italian CH KG and grounds the claim in a concrete, verifiable artifact (a 7-ontology network + 169M triples from the official MiBAC catalogue) rather than in adjectives. The novelty is "this exists, at this scale, from the national catalogue," which is unfalsifiable-by-puffery and easy to verify.
- OntoAndalus scopes novelty *terminologically and regionally* ("an ontology of Islamic artefacts **for terminological purposes**" in al-Andalus), so the claim is bounded and defensible.
- CRMtex / CRMgeo / CRMrp claim novelty as **a named extension of a known standard** for a named sub-domain — the most defensible novelty form in this field, because the contribution is precisely "the missing module," not "a better ontology."

The rhetorical trick: **bound the claim** (national / regional / sub-domain / capability), and **anchor it in an artifact** (triples, endpoint, reasoner runs, uptake). A scoped, anchored claim cannot be read as overclaiming.

**How they motivate a NATIONAL / domain-specific ontology** (this is the move HeritageGraph most needs to nail). The successful pattern is a three-step argument, *not* "Nepal is unique and deserves its own ontology":
1. **State the general standard's deliberate generality as a feature** (CIDOC-CRM is domain-neutral by design — that is *why* it interoperates).
2. **Show that a specific real phenomenon falls outside what the generic primitives express cleanly** — and show it with a concrete example, not an abstraction.
3. **Conclude that an *extension/profile aligned to* the standard is the right response** — i.e. you are not competing with CIDOC-CRM, you are completing it for this domain.

ArCo, KCHDM, and OntoAndalus all use exactly this "specialise-don't-replace" framing; it is what makes a national ontology read as a *contribution to* the LOD ecosystem rather than a parochial silo.

### 1.2 Two concrete examples (paraphrased, labelled)

**Example A — ArCo (ISWC 2019).** `[paraphrase of the rhetorical structure]`
> *M1:* The Italian General Catalogue, maintained by the national heritage ministry, records (ideally) every Italian cultural property and is the authoritative source for the country's heritage data. *M2:* Linked-data standards such as CIDOC-CRM and the Getty vocabularies make it possible to publish such records interoperably. *M3:* Yet the catalogue's records were locked in tabular/relational form and not available as a queryable, reusable knowledge graph. *M4:* We present ArCo, the Italian Cultural Heritage Knowledge Graph — a network of seven CIDOC-CRM–aligned ontologies plus a populated LOD dataset. *M5:* Contributions: the ontology network; the converter from catalogue records to RDF; the published triples and SPARQL endpoint; the documentation/test suite; the evaluation. *M6:* Built with ontology-design-pattern methodology and eXtreme Design, validated with competency questions and tests, released with a community process.

Why it works: every move is tied to an artifact you can click. Novelty = "this national resource now exists, at scale, openly." Source: https://doi.org/10.1007/978-3-030-30796-7_3 · https://arxiv.org/abs/1905.02840

**Example B — OntoAndalus (SWJ 2021).** `[paraphrase]`
> *M1:* Islamic material culture in al-Andalus is documented in dispersed, multilingual catalogues with inconsistent terminology. *M2:* CIDOC-CRM and foundational ontologies (DOLCE+DnS Ultralite) provide the upper-level scaffolding for principled artefact modelling. *M3:* But there is no shared, formally grounded terminological resource for Islamic artefacts, so the same object type is named and classified inconsistently across collections. *M4:* We present OntoAndalus, a DUL-grounded ontology of Islamic artefacts for terminological purposes. *M5/M6:* It is built on an explicit foundational alignment and validated against domain terminology and expert review.

Why it works: the gap is *terminological inconsistency in a specific corpus* — concrete and checkable — and the novelty is explicitly scoped to "terminological purposes." Source: https://doi.org/10.3233/SW-200391

---

## 2. Related Work Blueprint

### 2.1 How SOTA papers ORGANISE related work

The strong papers do **not** organise by paper ("X did A. Y did B."). They organise by **a frame that makes the gap inevitable.** Three dominant patterns:

1. **Funnel by abstraction level (most common, and the right fit for HeritageGraph).**
   General foundational/standard layer (CIDOC-CRM, EDM, PROV-O, DOLCE) → domain/national specialisations and CRM extensions (CRMgeo, CRMtex, CRMrp, KCHDM, OntoAndalus, ArCo) → the *specific* capability nobody covers → "hence our work." Each tier inherits the previous tier's vocabulary, so the prose has forward momentum instead of being a list.

2. **By requirement / capability (thematic).** PON and DOREMUS-style: organise the review around the *requirements* the new resource must meet (e.g. "modelling agents and roles," "modelling time," "modelling provenance of claims"), and under each requirement discuss who addresses it and how far. This is the cleanest way to set up a comparison table, because the table columns = the requirements you just walked through.

3. **By heritage modality, then collapse.** Walk tangible → intangible/ritual → textual → institutional, showing each is handled *in isolation*, then make the killer move: "these are treated separately; living heritage requires them integrated." (This is essentially what HeritageGraph already attempts — see §4.)

### 2.2 How they move from general standards to the gap

The transition is the heart of the section. SOTA pattern:

- **Credit the standard fully first** (expressivity, ISO status, adoption). Never open by attacking CIDOC-CRM.
- **Then reframe its generality as the source of the gap** — "domain-neutral by design, therefore under-specified for phenomenon Z." This is a *judo* move: the standard's greatest strength becomes the reason your extension is legitimate. CRMtex, CRMgeo and CRMrp all do this explicitly ("CIDOC-CRM provides the event-centric backbone but does not natively express [textual / spatiotemporal / restoration] phenomena, motivating an extension").
- **Position competitors as partial coverage, not as wrong.** Each competitor gets credited for what it *does* cover and is then shown to stop short of the specific capability — fairly, with a citation, in one or two sentences.

### 2.3 How they use the comparison table

The comparison table is a near-universal device in CH-ontology resource papers. Best practice observed:

- **Columns = capabilities/requirements**, derived from the gap argument (not from features the authors happen to have). The reader should be able to predict the columns from the Related Work prose.
- **Rows = representative comparator ontologies**, with the new ontology as the **last row**, visually distinguished.
- **Graded cells, not just ✓/✗.** "Strong / Partial / Limited / —" (as ArCo-adjacent and survey papers do) is far more credible than a wall of ticks, because it shows you read the competitors and concedes where they are strong.
- **Every row must be defended in prose** somewhere — a table cell that contradicts the text, or a competitor that appears only in the table, reads as cherry-picking.
- **The "all ticks in the last row" trap.** A table where only your row is all-✓ is the single most AI-/junior-looking artifact in CH papers. SOTA papers avoid it by (a) grading, (b) conceding at least one column where a competitor beats them or matches them, and (c) keeping columns to the genuinely differentiating capabilities (5–7), not 12 columns engineered so only you win.

### 2.4 How they avoid the flat "X did A. Y did B." list

- **Group, don't enumerate**: 3–5 thematic paragraphs, each with a topic sentence stating the *theme*, then 2–4 works as evidence for that theme.
- **End each paragraph with a "so-what" sentence** that advances toward the gap ("…thus these models excel at cataloguing fixed objects but treat custodianship as static metadata").
- **Synthesise across works** ("a recurring limitation across CRM extensions is…") rather than describing each in turn.
- **Cite in support of a claim**, not as the subject of the sentence. Prefer "Provenance of scholarly claims remains under-modelled in CH ontologies [a,b,c]" over "Author A built ontology A. Author B built ontology B."

---

## 3. Common WEAKNESSES that make an Intro / Related Work read as junior or AI-generated — and how SOTA avoids them

| Weakness | What it looks like | How SOTA avoids it |
|---|---|---|
| **Generic hook** | "Cultural heritage is important for identity and must be preserved." / "In recent years…" / "With the rapid development of…" | Open on a *specific* artifact, dataset, institution, or phenomenon (ArCo opens on the national catalogue; OntoAndalus on multilingual al-Andalus catalogues). Delete every "In recent years" and "plays a vital role." |
| **Throat-clearing / definitional padding** | A paragraph defining ontology vs. metadata vs. KG with textbook citations before any argument. | Define a term only if the *argument* turns on the distinction, and keep it to one sentence. (HeritageGraph's current Related Work opens with exactly this padding — see §4.) |
| **Listy citations** | "Many ontologies exist [3,5,7,9,12,15]." | One citation per claim, placed where it does argumentative work; group works by theme with a synthesising topic sentence. |
| **Unmotivated novelty / overclaiming** | "We propose the first ontology to fully capture living heritage." / "a comprehensive solution." | Scope the claim (national / sub-domain / capability) and anchor it in an artifact and a concrete failing example. Use "to our knowledge" sparingly and only when you actually checked. |
| **Hedging stacks** | "may potentially be able to possibly help…" | One modal max. State what the ontology *does*. |
| **Uniform paragraphs** | Every paragraph same length, same "Ontology X is a model that does Y and was proposed by Z" template. | Vary paragraph length by importance; lead with the *theme*, demote the citation to support. |
| **Strawman gap** | "No existing ontology handles X" with no evidence the authors looked. | Credit the closest competitors first, concede their strengths, *then* locate the precise residual gap (the funnel). |
| **All-ticks comparison table** | Last row is all ✓, competitors all ✗. | Graded cells; concede at least one column; columns = differentiating capabilities only. |
| **Contribution list = activity list** | "(1) we reviewed literature, (2) we built an ontology, (3) we evaluated it." | Contributions = *capabilities/artifacts* the reader gains ("(1) an event-mediated pattern for temporally-scoped custodianship; …"). HeritageGraph's current list is already in good shape here. |
| **Roadmap as filler / missing** | No roadmap, or a roadmap that just lists section titles. | One tight paragraph; optionally tie each section to what the reader gets from it. |
| **"Bag of named systems" Related Work** | A parade of acronyms with no through-line. | Organise by frame (abstraction funnel / requirements / modality-then-collapse) so the gap is the section's destination. |

---

## 4. Grading checklist for HeritageGraph's Intro + Related Work

Apply to `main/sw_template.tex` lines ~175–283. Grade each item Pass / Partial / Fail.

**Introduction**
1. **Concrete hook (M1).** Does sentence 1 anchor on a specific phenomenon/dataset/institution rather than "ontologies for CH have achieved maturity…"? — *Current draft opens with a domain-maturity generalisation; consider opening on a concrete Nepali living-heritage scene (e.g. the Kumari, a Guthi-maintained temple) to earn the gap.* 
2. **Standards credited before critique (M2).** Are CIDOC-CRM / EDM / PROV-O credited honestly before the gap? — *Current draft does this (CRM "dominant event-centric upper ontology", ArCo/Europeana "effectiveness at scale"). Pass.*
3. **Single, crisp, named gap (M3).** Is there one organising gap, stated as a missing capability, not "no one did my thing"? — *Current draft states it well: objects-as-static vs. living-heritage-as-constituted-through-events. Good; keep but tighten the four-challenge block so it doesn't become a second list before M4.*
4. **"We present X" is one clean line (M4).** Is there a single sentence that names HeritageGraph and its identity (CRM+PROV-O aligned, living heritage of Nepal)? — *Present. Pass.*
5. **Enumerated contributions = capabilities (M5).** Are the contributions a numbered list of capabilities/artifacts, not activities? — *Yes, five numbered modelling innovations. Strong. Pass.* (Minor: "five key principal" is redundant — pick one word.)
6. **Validation preview (M6).** Are CQ-driven design, alignment testing, and SPARQL reasoning previewed? — *Present. Pass.*
7. **Roadmap (M7).** One tight paragraph mapping sections? — *Present. Pass.* (Note: it promises "four novel modelling patterns" but the intro lists five contributions — reconcile the count.)
8. **No generic-hook / throat-clearing phrases.** Search and kill "In recent years", "plays a vital role", "with the rapid development", "has achieved considerable maturity". — *"have achieved considerable maturity" in sentence 1 is borderline; rephrase.*
9. **Novelty scoped + anchored, not overclaimed.** Are claims bounded (Nepal / living heritage / specific capability) and tied to artifacts? — *Mostly yes; ensure nothing reads as "first to fully…".*
10. **Citation density targeted, not dumped.** No `[a,b,c,d]` bundles standing in for argument. — *Intro is fine; watch Related Work.*

**Related Work**
11. **Organised by a frame, not a list.** Is it a funnel / requirements / modality structure, not "X did A, Y did B"? — *Current draft uses a reasonable funnel (standards → national/domain extensions → modalities → deployments → gap). Pass, but the ontology-vs-metadata-vs-KG opening paragraph is throat-clearing — cut or compress to one sentence.*
12. **Standard's generality reframed as the gap.** Is CIDOC-CRM's domain-neutrality turned into the justification for an extension (judo move)? — *Yes, explicitly (lines ~229). Strong.*
13. **Competitors credited fairly, then bounded.** Does each comparator get a "does well… but stops short" treatment with a citation? — *Yes for ArCo, EDM, OntoAndalus, KCHDM, RiC-O, CRMrp, CHEDO. Pass.*
14. **Comparison table: graded cells, columns = capabilities, last row distinguished, no all-tick trap.** — *Table uses Strong/Partial/Limited/— grading (good) and a distinguished HeritageGraph row, but the HeritageGraph row is effectively all-✓ — add at least one honest concession (e.g. ArCo beats you on dataset scale / deployment maturity; CRMrp is "Very Strong" on tangible and you are only "Integrated"). Also: every row in the table must be discussed in prose ("24 Solar Terms" appears in the table but not the text — fix).* 
15. **Synthesis over enumeration; each paragraph ends in a "so-what."** Are there cross-work synthesis sentences and theme-first topic sentences? — *Partially; lines ~239 and ~241 do this well ("treated in isolation", "persistent semantic fragmentation"). Ensure earlier paragraphs also end on a gap-advancing sentence rather than trailing off after the last citation.*

**Quick wins for HeritageGraph (highest leverage):**
- Replace the M1 opening generalisation with a concrete living-heritage vignette.
- Compress the ontology/metadata/KG definitional paragraph to one sentence (or move to background).
- Add one honest concession to the comparison table so the last row isn't all-✓.
- Reconcile the "four patterns" vs "five contributions" count.
- Ensure every table row is named in the prose (the "24 Solar Terms" / ClaOnto / MedinaOnto entries).
