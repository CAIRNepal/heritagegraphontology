# Q1 rewrite draft — three sections (ready-to-apply LaTeX)

Grounded in the repo (`github.com/CAIRNepal/heritagegraphontology`, branch HeritageGraph).
Resolved inputs: **OWL 2 DL** (HermiT) + OWL-RL closure; persistent IRI
`https://w3id.org/heritagegraph/`, v1.0.0, CAIR-Nepal; **32 existing CQs**
(`cq_sparql.md`, all PASS in `evaluation/results/cq_validation_report.txt`); shared
worked example from `examples/kathmandu-mini-abox.ttl` (Kumari modelled
**anonymously**, matching the repo).

**Apply-time dependencies:**
- Add bib key `recurrentodp2021` (BibTeX already drafted in `PROPOSED-CHANGES.md` §5).
- `guarinowelty2002` already added to `bibliography.bib`.
- **Reconcile numbers:** paper says 5{,}058→25{,}365 (20{,}307); latest
  `run_metrics.py` says 5{,}077→25{,}403 (20{,}326). Decide which release the paper
  pins to and make Table + prose agree. Draft below **keeps the paper's current
  numbers**; do not apply the metrics edit until you confirm the pin.

---

## A. §3.2 Ontology Metrics and Standards Compliance — replace L318–320

> Restructured into three *themed* paragraphs (expressivity / conformance /
> tightness+reproducibility), per the ArCo–SeaLiT archetype: numbers argue a claim,
> standards conformance is stated explicitly, and the HermiT/OWL-RL *results* are
> demoted to a forward-reference so this stays a description, not an evaluation.
> Table unchanged.

```latex
Table~\ref{tab:onto_metrics} profiles HeritageGraph along three axes---\emph{expressivity}, \emph{standards conformance}, and \emph{logical tightness}---each chosen to substantiate a design commitment of Section~\ref{subsec:overview} rather than to enumerate counts for their own sake. In expressivity, the ontology comprises 70 named classes, 125 object properties, and 46 datatype properties over a class hierarchy of maximum depth four; controlled vocabularies are realised as nine enumerations whose 64 permissible values are published as named individuals, each carrying a formal URI (predominantly Getty AAT). Three named union classes (e.g.\ \texttt{PhysicalHeritageThing}) supply range constraints for the event-linking properties of Section~\ref{subsec:event-pattern}.

Standards conformance is explicit and machine-checked. HeritageGraph is an OWL~2~DL ontology: the structural invariant of Section~\ref{subsec:overview}---that every class descends from a CIDOC-CRM or PROV-O class---is realised by 31 external \texttt{rdfs:subClassOf} axioms, with 42 classes and 73 properties aligned to 13 external vocabularies. Through CIDOC-CRM (ISO~21127) it inherits an event-centric backbone; through PROV-O it inherits a W3C-standard provenance vocabulary; and through Getty AAT its enumeration individuals are anchored to a shared authority. The entire artefact is generated from a single LinkML source, from which conformant OWL~2, SHACL, ShEx, JSON~Schema, and Python serialisations are derived, eliminating drift between the logical model and its validation and programming interfaces.

Logical tightness is enforced by both open- and closed-world mechanisms. Seventy \texttt{owl:disjointWith} axioms separate sibling and cross-hierarchy classes across 48 classes (for example \texttt{Temple} from \texttt{BuddhistMonument}, and \texttt{HumanMadeObject} from \texttt{Deity}, \texttt{Place}, \texttt{TimeSpan}, and \texttt{Actor}), and 273 minimum- and 176 maximum-cardinality axioms encode domain invariants such as single-deity embodiment per tenure (\texttt{LivingGoddessTenure.embodied\_deity}, $\mathit{max}=1$) and mandatory provenance sourcing (\texttt{HeritageAssertion.was\_derived\_from\_source}, $\mathit{min}=1$); 61 SHACL \texttt{NodeShape}s add complementary closed-world validation over populated graphs. Domain declarations are deliberately sparse---18 of the 171 properties carry an explicit \texttt{rdfs:domain}---for highly polymorphic relations whose domains span multiple disjoint branches, which avoids unintended entailments. Under the fixed configuration of Section~\ref{subsec:eval-consistency}, HermiT classifies the ontology as consistent with no unsatisfiable classes, the 32 competency questions of Section~\ref{sec:evaluation} are all satisfied, and an OWL-RL closure expands the asserted triples roughly fivefold; we defer these results to the evaluation. All artefacts, the evaluation pipeline, and the released ontology resolve from the persistent namespace \url{https://w3id.org/heritagegraph/} (v1.0.0).
```

**Net:** 3 themed paragraphs replacing 3 list-like ones; +~90 words; adds the explicit
OWL 2 DL / ISO 21127 / PROV-O conformance statement, the LinkML single-source claim,
the persistent-artefact pointer, and a forward-ref to the 32-CQ result.

---

## B. §3.3 Event-Mediated Tangible Heritage — additions (keep existing prose)

Three Q1 additions; the existing paragraphs and the `Production` listing stay.

### B1. After the opening problem paragraph, add a CQ anchor:
```latex
This pattern is what lets the ontology answer competency questions that cross object and time, such as ``what was the condition of a temple at successive assessments?'' (CQ8), ``which historical events---earthquakes, restorations, political transitions---affected a structure, and over what time-spans?'' (CQ4), and ``who produced an object, when, and by what technique?'' (CQ1, CQ20). None is expressible by direct property attachment.
```

### B2. Replace the dense five-event prose block (the `\textbf{Construction}...` paragraph) with a table + the two subtle cases as prose:
```latex
\begin{table}[htbp]
\centering
\caption{Event classes that mediate historically contingent properties of tangible heritage, with their CIDOC-CRM mapping and the contingency each captures.}
\label{tab:event-mediation}
\small
\begin{tabular}{@{}llp{4.6cm}@{}}
\toprule
\textbf{Event class} & \textbf{CRM} & \textbf{Contingency captured} \\
\midrule
\texttt{Production} & \texttt{E12} & creator, commissioner, technique, and date of construction \\
\texttt{TransferOfCustody} & \texttt{E10} & custodial change between actors / \texttt{Guthi} institutions \\
\texttt{ConditionAssessment} & \texttt{E14} & material state (\textit{Good}/\textit{Damaged}/\textit{Ruined}/\textit{Restored}) at a point in time \\
\texttt{Consecration} & \texttt{E7} & ritual activation: a \texttt{Murti} becomes a locus of divine presence \\
\texttt{Enshrinement} & \texttt{E7} & installation of a deity's representation within a sanctum \\
\bottomrule
\end{tabular}
\end{table}

Each contingent assertion thus becomes a typed event in which the entity participates: \texttt{Production} links the produced object (\texttt{crm:P108}) to creator (\texttt{crm:P14}), commissioner, time-span (\texttt{crm:P4}), and technique (\texttt{crm:P32}); \texttt{TransferOfCustody} records surrendering and receiving actors (\texttt{crm:P28}/\texttt{crm:P29}) and, via \texttt{transferred\_to\_guthi}, the receiving \texttt{Guthi}; and \texttt{ConditionAssessment} relates an assessed object (\texttt{crm:P34}) to a \texttt{ConditionState} (\texttt{crm:P35}), tracking condition across successive assessments. The two ritual events are deliberately distinguished: \texttt{Consecration} makes a deity ritually present in a \texttt{Murti} (\texttt{makes\_deity\_present})---before it an ordinary sculpture, after it a locus of divine presence---whereas \texttt{Enshrinement} places a deity's representation within a temple sanctum, modelled separately because in Newar practice a deity may be consecrated independently of its installation.
```

### B3. After the `Production` listing, add a shared worked example + SPARQL:
```latex
Figure~\ref{fig:event-pattern} and Listing~\ref{lst:abox-event} make this concrete with the Kasthamandap pavilion in Kathmandu Durbar Square. Its construction, custody, and post-2015-earthquake damage are three separate events sharing one object, so condition is read from the assessment timeline rather than from a static attribute.
\begin{lstlisting}[caption={Event-mediated ABox excerpt (Turtle) for the Kasthamandap pavilion, from the HeritageGraph demonstrator dataset.},label={lst:abox-event}]
ex:Kasthamandap a hg:Temple ; hg:has_architectural_style hg:Pagoda .
ex:Prod_Kasthamandap a hg:Production ;
    hg:produced_object ex:Kasthamandap ; hg:carried_out_by ex:LicchaviBuilders .
ex:CA_2015 a hg:ConditionAssessment ;
    hg:assessed_object ex:Kasthamandap ; hg:assessed_condition_state ex:CS_Damaged .
ex:CS_Damaged a hg:ConditionState ; hg:has_condition_type hg:Damaged .
\end{lstlisting}
The condition history is then a query, not a fact (CQ8):
\begin{lstlisting}[caption={SPARQL answering CQ8 over the demonstrator ABox.},label={lst:sparql-cq8}]
SELECT ?structure ?type WHERE {
  ?a a hg:ConditionAssessment ;
     hg:assessed_object ?structure ;
     hg:assessed_condition_state/hg:has_condition_type ?type . }
\end{lstlisting}
```

### B4. In the recurrence paragraph, add the ODP citation:
> change "Recurrence is encoded via \texttt{recurrence\_pattern}..." to cite the design
> precedent: `...for calendar-independent reasoning, following the recurrent-situations design pattern~\cite{recurrentodp2021}.`

---

## C. §3.4 Living Goddess Lifecycle — additions (keep the existing paragraph)

The existing paragraph is already Q1-grade reasoning; keep it and add four things.

### C1. OntoClean tie (insert after the first sentence):
```latex
In OntoClean terms~\cite{guarinowelty2002}, ``Kumari'' is an anti-rigid role rather than a rigid kind: an individual is Kumari only contingently and temporarily, so the status cannot be modelled as class membership without violating rigidity, and must instead be reified as a bounded temporal entity.
```

### C2. Axiom listing (after the property-bearing sentence), mirroring `Production`:
```latex
\begin{lstlisting}[caption={Manchester-syntax core of the \texttt{LivingGoddessTenure} period, derived from the LinkML schema.},label={lst:tenure-owl}]
Class: LivingGoddessTenure
  SubClassOf: crm:E4_Period
  SubClassOf: embodied_deity   max 1 Deity
  SubClassOf: had_participant  min 1 Person
  SubClassOf: has_timespan     min 1 TimeSpan
\end{lstlisting}
```

### C3. CQ + worked example (before the generalization sentence):
```latex
The pattern answers competency questions over the institution's history---which person embodied which deity, for which period, at which residence (CQ26, CQ27); which institution bore responsibility (CQ31); and what event terminated the status and when (CQ32)---without ever equating the person with the deity. Listing~\ref{lst:abox-tenure} shows one (anonymised) tenure from the demonstrator dataset.
\begin{lstlisting}[caption={Living Goddess tenure ABox excerpt (Turtle); the incumbent is represented anonymously.},label={lst:abox-tenure}]
ex:Tenure a hg:LivingGoddessTenure ;
    hg:had_participant ex:KumariPerson ;   # anonymous incumbent
    hg:embodied_deity ex:Taleju ;
    hg:supported_by_institution ex:KumariGuthi ;
    crm:P4_has_time-span ex:TS_Tenure .
ex:Sel a hg:LivingGoddessSelection ; hg:initiated_tenure ex:Tenure .
ex:Ret a hg:LivingGoddessRetirement ; hg:ended_tenure_of ex:Tenure .
\end{lstlisting}
```

### C4. Keep the final generalization sentence verbatim (it is already the model
"reusable template for any temporally bounded sacred or ceremonial status").

**Net for §3.4:** +OntoClean rigor, +axiom listing, +CQ anchor, +anonymised worked
example; ~+110 words.

---

## D. Suggested apply order
1. `bibliography.bib`: add `recurrentodp2021`.
2. §3.4 (smallest, self-contained) → §3.3 → §3.2 (only after you pin the triple counts).
3. Run `/ars-reviewer` on the revised §3.2–3.4 to confirm the Q1 bar, then
   `/ars-revision` to close any panel points, then `/ars-citation-check`.
