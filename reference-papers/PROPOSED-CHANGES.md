# Draft: proposed changes to the *Ontology Description* section

Scope: primarily **§ High-Level Architecture** (`main.tex` lines ~295–311), with
lighter notes on the rest of § Ontology Description. This is a discussion draft —
nothing has been written into `main.tex` yet. Once we agree, the rewrite goes in
via `/ars-revision`.

---

## 1. Diagnosis of the current High-Level Architecture subsection

Current text (lines 297–311) is **one assertion paragraph + a 4-item list + a
figure**. Against the peer models it has four research-grade gaps:

| # | Gap | What peer papers do | Evidence |
|---|-----|---------------------|----------|
| G1 | **No design rationale / no funnel.** It opens by *asserting* "event-centric … performative paradigm" without first stating the representational *problem* that forces that choice. The reader meets the answer before the question. | EDM and ArCo state a paradigm/rationale (and EDM numbered design principles) *before* introducing classes. | EDM Primer; ArCo §"XD … encourages and supports a modular design, where each module addresses a subset of requirements and covers a coherent sub-area of the domain." |
| G2 | **The extension principle is never stated.** It says HeritageGraph "extends CIDOC-CRM … with PROV-O" but not the *invariant* — that every HeritageGraph class is a subclass/descendant of a CRM (or PROV-O) class. That invariant is what makes the alignment credible. | SeaLiT states it explicitly as a one-line contract. | SeaLiT: *"each class of the SeaLiT Ontology is a direct subclass or a descendant of a CIDOC-CRM class."* |
| G3 | **No justification for extending CRM rather than building standalone.** Reviewers expect this defended on concrete grounds. | SeaLiT gives three: it is the standard, it enables integration, it is a sustainable living standard. | SeaLiT: *"we selected to use CIDOC-CRM because it is the standard ontology for cultural heritage documentation … facilitates data integration … enables data sustainability because CIDOC-CRM is a living standard."* |
| G4 | **The "four layers" are listed but not motivated as an architecture.** No upper-ontology backbone is named, and the cross-cutting nature of the provenance layer (called out later in §Ontology-Description intro) is not signalled here. | SeaLiT anchors on CRM's endurant/perdurant top level; ArCo names a top-level module + a generic-relations core + thematic modules. | SeaLiT: *"The highest-level distinction in CIDOC-CRM is … E77 Persistent Item (endurant) [and] E2 Temporal Entity (perdurant)."* ArCo: *"Two modules – arco and core – include top-level concepts and cross-module generic relations respectively."* |

Two **typos** to fix while we're here (line 301, "Event layer" item): the em-dashes
collapsed — `event classes\texttt{Production}` and `\texttt{Enshrinement}mediate`
are missing their surrounding `---` / spaces.

---

## 2. The funnel we propose (broad → narrow)

```
P1  PROBLEM        Why object-centric/static documentation fails for LIVING heritage
                   → motivates the performative, event-centric paradigm.        (broadest)
P2  COMMITMENT     Base standard + extension invariant + why-CRM justification
                   (every HG class ⊑ a CRM/PROV-O class; standard/integration/sustainability).
P3  ARCHITECTURE   The layered organisation, grounded on CRM's endurant/perdurant
                   backbone; provenance layer flagged as cross-cutting; rationale for layering.
P4  CLASSES        The four layers' concrete classes (the existing itemize, tightened). (narrowest)
                   → figure + forward pointer to the four modeling patterns.
```

This is exactly the SeaLiT progression (paradigm → extension principle → backbone →
justification → specifics), adapted to HeritageGraph's living-heritage problem framing.

---

## 3. Proposed rewrite (LaTeX) — drop-in for lines 297–311

> Reuses existing figure label `fig:heritagegraph-overview` and existing cite keys
> `bekiari2021volume`, `carriero2019arco`, `petras2017europeana`, `Doerr_2003`,
> `Suarez-Figueroa2012`. **Two new keys** (`sealit2023`, `guarinowelty2002`) — BibTeX in §5.

```latex
\subsection{High-Level Architecture}\label{subsec:overview}

% P1 — PROBLEM / PARADIGM (broadest)
Cultural-heritage ontologies have largely inherited the object-centric stance of
museum cataloguing, attaching properties such as date, style, or condition directly
to physical things as timeless facts~\cite{Doerr_2003,petras2017europeana}. For
\emph{living} heritage this stance is inadequate: a temple's significance is not a
fixed attribute but is continually re-constituted through ritual enactment,
institutional custody, and time-bounded sacred roles, and it is routinely
renegotiated by reconsecration, damage, repair, and functional change. HeritageGraph
therefore adopts a \emph{performative, event-centric} paradigm, in which cultural
meaning is documented through the events in which it is observed rather than asserted
as a standing property of an object.

% P2 — COMMITMENT: base standard, extension invariant, justification
We realise this paradigm as an extension of CIDOC-CRM v7.2.1~\cite{bekiari2021volume},
a high-level, event-centric ontology of human activity, things, and events that is the
ISO standard for cultural-heritage documentation, augmented with PROV-O for
provenance. As in comparable CRM extensions~\cite{sealit2023}, the extension obeys a
single structural invariant: \emph{every HeritageGraph class is a subclass or
descendant of a CIDOC-CRM class} (or, in the provenance layer, of a PROV-O class), so
that HeritageGraph instances inherit the standard's properties (e.g.\ \texttt{P14
carried\_out\_by}, \texttt{P4 has\_timespan}) and remain interoperable with the wider
CRM ecosystem. We extend the standard rather than build a stand-alone model on three
grounds: CIDOC-CRM is the established reference for the domain; alignment to it
enables integration with existing and future CRM-based datasets; and, as an actively
maintained living standard, it offers long-term sustainability~\cite{sealit2023}.

% P3 — ARCHITECTURE: layering grounded on the CRM backbone
HeritageGraph is organised as four layers anchored on CIDOC-CRM's top-level
endurant/perdurant distinction---persistent items (\texttt{crm:E77}) versus temporal
entities (\texttt{crm:E2}). A \emph{tangible} layer of persistent physical things and
an \emph{event} layer of temporal occurrences form the endurant/perdurant core; a
\emph{syncretic and religious} layer supplies the conceptual entities (deities,
traditions) those events and things refer to; and a \emph{provenance} layer cuts
across all three, attributing every substantive assertion to its evidential source.
Figure~\ref{fig:heritagegraph-overview} gives the structural overview; the four layers
are detailed below and elaborated as reusable modeling patterns in
Sections~\ref{subsec:event-pattern}--\ref{subsec:institutional-layer}.

% P4 — CLASSES (existing itemize, tightened; typos fixed)
\begin{itemize}
    \item \textbf{Tangible entities:} rooted in \texttt{crm:E22\_Human-Made\_Object},
    encompassing \texttt{ArchitecturalStructure} and its specialisations
    (\texttt{Temple}, \texttt{BuddhistMonument}, \texttt{Stupa}, \texttt{Chaitya},
    \texttt{RestHouse}, \texttt{Pati}, \texttt{Sattal}, \texttt{Dharmashala},
    \texttt{WaterStructure}, \texttt{DhungeDhara}, \texttt{Pokhari}),
    \texttt{IconographicObject} (\texttt{Murti}, \texttt{Paubha}), and
    \texttt{ArchitecturalElement} (\texttt{crm:E25\_Architectural\_Element}). The union
    class \texttt{PhysicalHeritageThing} aggregates these for range constraints.
    \item \textbf{Event layer:} centred on \texttt{RitualEvent} (extending
    \texttt{crm:E7\_Activity}), with subclasses \texttt{Festival},
    \texttt{ChariotFestival}, \texttt{MaskedDance}, and lifecycle events
    \texttt{LivingGoddessSelection} and \texttt{LivingGoddessRetirement}. Further event
    classes---\texttt{Production} (\texttt{crm:E12}), \texttt{TransferOfCustody}
    (\texttt{crm:E10}), \texttt{ConditionAssessment} (\texttt{crm:E14}),
    \texttt{Consecration}, and \texttt{Enshrinement}---mediate historically contingent
    properties.
    \item \textbf{Provenance layer:} realised through \texttt{HeritageAssertion}
    (aligned with both \texttt{crminf:I2\_Belief} and \texttt{prov:Entity}),
    \texttt{DataSource} (subclasses \texttt{FieldSurveyDataset},
    \texttt{OralHistoryRecording}, \texttt{ArchivalRecord}),
    \texttt{DocumentationActivity}, and \texttt{Verification}.
    \item \textbf{Syncretic and religious concepts:} modelled contextually via
    \texttt{SyncreticRelationship} (\texttt{crm:E13\_Attribute\_Assignment}),
    \texttt{Deity} (\texttt{crm:E28\_Conceptual\_Object}), and
    \texttt{ReligiousTradition} (\texttt{crm:E55\_Type}).
\end{itemize}

% figure block unchanged (lines 306-311)
```

**Net effect:** the subsection grows from 1 paragraph + list to 3 short paragraphs +
the (same) list, and now moves problem → commitment → architecture → classes. Roughly
+150 words.

---

## 4. Optional, higher-value additions (flag for decision)

- **A1 (recommended).** One sentence in P2 invoking OntoClean to justify the most
  load-bearing subsumption choices — that `LivingGoddessTenure` is modelled as a
  *period* (`crm:E4`) and the goddess *role* is anti-rigid, not identity
  (`owl:sameAs`). This pre-empts the obvious reviewer question and is already
  half-argued in §\ref{subsec:living-goddess}. Needs cite `guarinowelty2002`.
- **A2.** Name the four layers as a stated *separation-of-concerns* design principle
  (à la EDM's numbered principles) rather than leaving it implicit. Low effort, raises
  rigor.
- **A3.** Cross-reference the metrics table (Table~\ref{tab:onto_metrics}) from P3 so
  the "70 classes / 4 layers / depth 4" claims are grounded where the architecture is
  introduced, not only later.

### Newly-added domain peers (from the closest-10 set) — where they land

These three strengthen *related work* and the *pattern subsections* more than the
high-level architecture itself, but each gives a citable peer that pre-empts a
"why didn't you reuse X?" reviewer question:

- **A4 — CRMdig** (`crmdig2011`). In the **Provenance layer** bullet (P4) and in
  §\ref{subsec:provenance}, cite CRMdig as the canonical CRM provenance model and
  note that `HeritageGraph` aligns to PROV-O + `crminf:I2_Belief` rather than CRMdig
  because it needs *belief/assertion*-level attribution, not digital-process
  provenance. One clause in P4; one sentence in the provenance subsection.
- **A5 — ICON** (`icon2023`). In §\ref{subsec:syncretic} (and optionally the
  Syncretic/religious bullet in P4), cite ICON as the Panofsky-based peer for
  iconographic/symbolic interpretation, positioning `SyncreticRelationship` +
  `depicts_deity` as a *reified, attributed* alternative for cross-tradition identity.
- **A6 — Recurrent Situations ODP** (`recurrentodp2021`). In
  §\ref{subsec:event-pattern} where `recurrence_pattern` / `lunar_date_tithi` are
  introduced, cite it as the design-pattern precedent for recurrence modelling.

> Net: A4–A6 add 0 words to the High-Level Architecture funnel itself (besides one
> optional clause in the provenance bullet); they mainly enrich the later subsections
> and related work. Keep them out of P1–P3 to preserve the funnel's tightness.

---

## 5. New BibTeX needed (paste into `bibliography.bib`)

```bibtex
@article{sealit2023,
  author  = {Fafalios, Pavlos and Kritsotaki, Athina and Doerr, Martin},
  title   = {The {SeaLiT} Ontology -- An Extension of {CIDOC-CRM} for the Modeling
             and Integration of Maritime History Information},
  journal = {ACM Journal on Computing and Cultural Heritage},
  volume  = {16}, number = {3}, pages = {1--20}, year = {2023},
  doi     = {10.1145/3586080}
}

@incollection{guarinowelty2002,
  author    = {Guarino, Nicola and Welty, Christopher A.},
  title     = {Evaluating Ontological Decisions with {OntoClean}},
  booktitle = {Communications of the ACM},
  volume    = {45}, number = {2}, pages = {61--65}, year = {2002},
  publisher = {ACM}, doi = {10.1145/503124.503150}
}

% --- domain peers (A4–A6), used in the pattern subsections / related work ---
@inproceedings{crmdig2011,
  author    = {Doerr, Martin and Theodoridou, Maria},
  title     = {{CRMdig}: A Generic Digital Provenance Model for Scientific Observation},
  booktitle = {Proc. 3rd USENIX Workshop on the Theory and Practice of Provenance (TaPP)},
  year      = {2011}, address = {Heraklion, Crete}
}

@article{icon2023,
  author  = {Sartini, Bruno and Baroncini, Sofia and van Erp, Marieke and
             Tomasi, Francesca and Gangemi, Aldo},
  title   = {{ICON}: An Ontology for Comprehensive Artistic Interpretations},
  journal = {ACM Journal on Computing and Cultural Heritage},
  volume  = {16}, number = {3}, pages = {1--38}, year = {2023},
  doi     = {10.1145/3594724}
}

@misc{recurrentodp2021,
  author = {Porello, Daniele and others},
  title  = {An Ontology Design Pattern for Representing Recurrent Situations},
  year   = {2021}, eprint = {2101.00286}, archivePrefix = {arXiv}, primaryClass = {cs.AI}
}
```
> Verify author lists / volumes for `sealit2023`, `icon2023`, and `recurrentodp2021`
> against the PDFs before final submission (placeholders filled from search metadata).

---

## 6. Open questions before I apply this

1. **Depth of the OntoClean move (A1):** one-sentence nod, or a fuller
   rigidity/identity argument? (More rigor vs more length.)
2. **Length budget:** the rewrite adds ~150 words. Is the subsection's length capped?
3. **Scope of this pass:** High-Level Architecture only, or shall I also tighten the
   §Ontology-Description intro (line 293) to preview the funnel and the cross-cutting
   provenance layer consistently?
```
