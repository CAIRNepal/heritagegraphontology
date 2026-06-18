# Evaluation-Section Benchmark: HeritageGraph (TGDK Resource Paper)

**Scope.** This report benchmarks the *Evaluation* section of the HeritageGraph
resource paper against the evaluation practices of top ontology / resource
papers (ArCo, Polifonia) and against the methodological standards in the
ontology-evaluation literature (Brank/Gangemi/Vrandečić evaluation layers;
Guarino & Welty OntoClean; Grüninger & Fox competency-question entailment; FOCA
user-centered evaluation). It maps the paper's seven current subsections onto
the standard evaluation layers, lists what a top paper would include that this
one lacks or under-does, and gives a ranked, feasibility-aware fix plan keyed to
what is actually achievable from a LinkML-generated schema plus a ~79-triple
demonstrator ABox with local reasoners and no deployed application or users.

No numeric results are invented anywhere in this report. Where a real
computation is required, a `[VERIFY]` placeholder marks the spot.

---

## A. Coverage Map — Current Subsections onto Standard Evaluation Layers

The Brank/Gangemi/Vrandečić synthesis recognizes the following evaluation
layers: **lexical/vocabulary**, **hierarchy/taxonomy**, **semantic
(non-taxonomic relations)**, **context/application**, **syntactic**,
**structural**, and **design-principle**. The seven current subsections map as
follows.

| Layer | Covered? | By which subsection(s) | Strength |
|---|---|---|---|
| Lexical / vocabulary (terms, labels, annotations, naming) | Partial | §2 (OOPS-style scan touches annotation/label pitfalls); §6 (alignment ties terms to external vocabularies) | Weak — no systematic label/definition completeness audit; coverage is incidental |
| Hierarchy / taxonomy (is-a correctness, disjointness) | Partial | §1 (HermiT: +59 inferred subClassOf, 0 unsatisfiable); §2 (disjointness/sibling-group check) | Moderate on *consistency*; **no rigour-based taxonomy cleaning** (OntoClean absent) |
| Semantic — non-taxonomic relations | Partial | §1 (deductive yield via OWL-RL closure); §4 (SHACL property constraints); §3 (CQ SPARQL exercises relations) | Moderate — relations are constrained and exercised, but not evaluated for modelling correctness against a reference |
| Context / application (task-based, in-use, user) | **No** | — | **Absent** — Threats-to-Validity admits no task-based/user study |
| Syntactic (well-formedness, OWL profile, parses) | Partial | §1 (ROBOT/HermiT pipeline implies valid parse); §2 (FAIR/metadata audit) | Weak-implicit — never stated as an explicit syntactic-correctness claim or OWL-profile determination |
| Structural (graph metrics, depth, breadth, modularity) | Yes | §7 (metrics table; positioning vs CIDOC-CRM / ArCo) | Strong on description; **weak on comparison** (no real competitor numbers) |
| Design-principle (FAIR, modelling pitfalls, ODP conformance, provenance pattern) | Yes | §2 (OOPS + FOOPS FAIR); §5 (provenance-under-contradiction, the headline contribution) | Strong — clearest part of the section |

**Layer verdict.** Well-covered: structural, design-principle. Adequately
covered: logical consistency (a syntactic/taxonomic sub-aspect). **Under-covered
or absent: context/application (entirely), rigour-based taxonomy evaluation
(OntoClean), lexical completeness, and explicit syntactic-profile statement.**
The section is strong on *formal/automated* checks and weak on *rigorous
conceptual* and *in-use* evaluation — the exact asymmetry reviewers of a
top-tier resource track look for.

---

## B. Gap List — What a Top Ontology Paper Includes That This One Lacks or Under-Does

For each gap: what it is, why it matters, and a blunt feasibility judgement
given the facts (LinkML schema; ~79-triple demonstrator ABox; local reasoners
HermiT/ELK/Pellet, pySHACL, owlrl, local OOPS heuristic; no app, no users, no
live endpoint, w3id not resolving).

1. **OntoClean meta-property analysis (rigidity, identity, unity, dependence).**
   *Why it matters:* it is *the* standard rigorous taxonomy-cleaning method;
   its absence is conspicuous in any paper that claims modelling quality. It
   surfaces is-a errors that a consistent reasoner will never flag (a consistent
   ontology can still be ontologically wrong). *Feasibility:* **FULLY FEASIBLE
   NOW.** It is a manual conceptual analysis over the top-level taxonomy (depth
   4, 70 classes) — needs no data, no users, no app. Highest value-per-effort
   gap on the list.

2. **Competency-question *entailment* (Grüninger & Fox), not just coverage +
   SELECTs.** *Why it matters:* the CQ method's evidentiary standard is that a
   CQ is *answerable/entailed* by the ontology, ideally formalised; the current
   "coverage at schema level + 6 SELECTs over a tiny ABox" is the weaker form.
   *Feasibility:* **PARTIALLY FEASIBLE NOW.** You can (a) classify each of the
   32 CQs as schema-answerable vs requiring instance data, (b) formalise the
   answer pattern (the classes/properties/path that entail an answer) for each,
   and (c) keep the 6 SELECTs as worked demonstrations. Full entailment proof
   over a populated KG needs data → future work.

3. **CQ-to-ontology-element traceability matrix (ArCo includes this).** *Why it
   matters:* it is the requirements-engineering backbone of a CQ-driven
   ontology and makes coverage *auditable* rather than asserted. ArCo's
   inclusion of it is part of why its evaluation reads as rigorous.
   *Feasibility:* **FULLY FEASIBLE NOW.** A table mapping each of the 32 CQs to
   the exact classes/properties/SHACL shapes that satisfy it. Pure
   documentation of existing artefacts.

4. **Cross-reasoner confirmation + reasoning-time reporting.** *Why it matters:*
   a single-reasoner result (HermiT only) is a single point of failure; top
   papers confirm consistency/classification across reasoners. *Feasibility:*
   **FULLY FEASIBLE NOW.** ELK and Pellet are available via ROBOT locally. Re-run
   classification under each, report agreement on consistency / unsatisfiable
   classes / inferred subClassOf count, and tabulate times. Caveat: ELK is
   EL-profile only, so report what each reasoner can and cannot see.

5. **Explicit OWL-profile / syntactic-correctness statement.** *Why it matters:*
   reviewers expect to know the OWL profile (and whether ELK's EL coverage is
   complete or partial for your axioms). Currently only implied. *Feasibility:*
   **FULLY FEASIBLE NOW** — ROBOT can report the profile; pairs naturally with
   gap 4.

6. **Gold-standard comparison.** *Why it matters:* comparing extracted/modelled
   terms against a reference vocabulary is a classic lexical/semantic evaluation.
   *Feasibility:* **PARTIAL / HONEST-FRAMING NOW.** There is no curated gold
   standard for living-heritage Kathmandu Valley concepts, and inventing
   precision/recall numbers is forbidden. Feasible *now*: frame §6 alignment as
   a *proxy* gold-standard exercise (mapping to 13 established vocabularies) and
   state explicitly that no domain gold standard exists. A real gold-standard
   study is future work.

7. **Task-based / application-based evaluation.** *Why it matters:* the
   context/application layer is entirely empty; top resource papers show the
   ontology doing real work in a system. *Feasibility:* **NOT FEASIBLE NOW** —
   no deployed application. Future work; the demonstrator ABox queries are the
   closest current proxy and should be framed as such, not as task-based eval.

8. **User-centered evaluation (FOCA / expert review).** *Why it matters:*
   domain-expert judgement is the credible check on whether
   Hindu-Buddhist-Newar syncretism, Guthi trusts, and the Kumari are modelled
   *correctly*, not just consistently. *Feasibility:* **NOT FEASIBLE NOW** (no
   users recruited). Future work — and worth flagging as the single most
   important domain-validity step, given the cultural sensitivity of the domain.

9. **Structural metrics *vs competitors with real numbers*.** *Why it matters:*
   §7 positions HeritageGraph against CIDOC-CRM / ArCo but the comparison is
   qualitative; a metrics table with the competitors' actual figures is what
   makes positioning credible. *Feasibility:* **FEASIBLE NOW with caveats** —
   CIDOC-CRM and ArCo are public; their class/property counts and depth can be
   computed locally with the same script used for HeritageGraph (or cited from
   their papers). Do not invent; compute or cite, mark `[VERIFY]` until done.

10. **Single-rater alignment audit → inter-rater reliability.** *Why it matters:*
    §6's single-rater audit of 20/112 mappings has no reliability estimate; the
    Threats section already concedes this. *Feasibility:* **PARTIAL NOW** — a
    second rater on the same 20 mappings + a Cohen's κ is feasible if a second
    annotator is available locally; if not, expand the sample and keep the
    honest single-rater caveat. Full feasibility depends on a second person.

11. **Lexical completeness audit (labels/definitions/multilingual coverage).**
    *Why it matters:* completeness of `rdfs:label`/definitions/annotations is a
    basic lexical-layer check; partially the domain (Newar/Nepali terms) demands
    multilingual labelling. *Feasibility:* **FULLY FEASIBLE NOW** — a SPARQL/
    script count of classes & properties with/without labels, definitions, and
    language-tagged labels over the schema.

---

## C. Ranked Fix Plan

### (i) DO NOW — feasible without new data, users, or an application

Ranked by impact-per-effort. Each item states exactly what to write/compute and
where it goes in the section.

**FIX-1 (highest impact). Add an OntoClean meta-property analysis of the
top-level taxonomy.** *Where:* new subsection, ideally §2 (Modelling Quality) or
a new §2b. *What to do:* select the top-level / backbone classes (aim for the
~15–25 that carry the taxonomy — e.g., the roots and their immediate children
under the depth-4 hierarchy). For each, assign the four OntoClean meta-properties
— **Rigidity** (+R rigid / ~R anti-rigid / ¬R non-rigid), **Identity** (+I
supplies own identity criterion / -I does not), **Unity** (+U / -U / ~U), and
**external Dependence** (+D / -D). Then apply the OntoClean subsumption
constraints and report any violations (e.g., an anti-rigid class subsuming a
rigid class; a class with an identity criterion under one with an incompatible
one). Present as a table: `Class | Rigidity | Identity | Unity | Dependence |
Notes`, followed by a short prose paragraph on violations found and how they were
resolved or justified. *Honesty note:* this is conceptual analysis — there are no
numbers to fabricate; the output is the meta-property assignments and the
violation verdict.

**FIX-2. Restore/add the CQ-to-ontology-element traceability matrix.** *Where:*
§3 (Competency Questions). *What to do:* one row per CQ (all 32). Columns: `CQ ID
| CQ text (short) | Satisfying classes | Satisfying properties | Satisfying SHACL
shape(s) | Answerable at schema level? (Y/N) | Demonstrated by SPARQL? (Y/N, which
of the 6)`. This converts the current "coverage of all 32 CQs" claim into an
auditable artefact and simultaneously documents which CQs need instance data
(setting up the future-work framing for entailment over a populated KG).

**FIX-3. Add cross-reasoner confirmation + an OWL-profile statement.** *Where:*
§1 (Logical Consistency). *What to do:* re-run classification via ROBOT under
**HermiT, ELK, and Pellet** over the same import-stripped axioms. Report a small
table: `Reasoner | Consistent? | Unsatisfiable classes | Inferred subClassOf |
Time(s) | Profile coverage note`. Fill measured cells with `[VERIFY]` until the
runs are done; do not carry over HermiT's existing numbers to the other
reasoners. Add one sentence stating the OWL profile (ROBOT report) and noting
ELK's EL-only coverage means it confirms a subset of axioms — keep HermiT/Pellet
as the full-expressivity check. This directly retires the "single reasoner on
import-stripped axioms" threat.

**FIX-4. Add an explicit evaluation-layers framing paragraph.** *Where:* opening
of the Evaluation section (a 4–6 sentence preamble). *What to do:* name the
Brank/Gangemi/Vrandečić layers, state which the section covers (structural,
design-principle, taxonomy-consistency, semantic-constraint) and which it does
not (context/application, user-centered), and forward-reference the OntoClean
addition (FIX-1) as the rigour-based taxonomy layer. This single paragraph makes
the section legible to reviewers and pre-empts the "no evaluation framework"
criticism. Use the Coverage Map table in Part A as the backing structure.

**FIX-5. Add a lexical completeness audit.** *Where:* §2. *What to do:* compute
counts (via SPARQL/script over the schema): classes/properties with vs without
`rdfs:label`, with vs without a definition annotation, and with language-tagged
labels (flagging Newar/Nepali/English coverage given the syncretic domain).
Report as a small table with `[VERIFY]` cells until computed. Cheap, and closes
the lexical layer.

**FIX-6. Reframe §6 (alignment) and §7 (competitors) honestly.** *Where:* §6 and
§7. *What to do:* (a) In §6, explicitly state that no curated gold standard
exists for this domain and that alignment to 13 established vocabularies serves
as a *proxy* external-grounding check, not a precision/recall gold-standard
study; keep the single-rater 20/112 audit but label it a pilot and add a second
rater + Cohen's κ if a second annotator is available (`[VERIFY]`), else state the
sample-size/precision limitation plainly. (b) In §7, replace qualitative
positioning with a metrics table that includes **real** CIDOC-CRM and ArCo
figures (computed locally with the same script, or cited from their papers with
citation); mark every competitor cell `[VERIFY]` until sourced. No invented
numbers.

**FIX-7. Promote CQ answers from coverage toward entailment (schema-level
portion).** *Where:* §3, alongside FIX-2. *What to do:* for each schema-answerable
CQ, state the entailment pattern — the specific class hierarchy + property path
that *entails* an answer — rather than only asserting coverage. The 6 existing
SELECTs become worked demonstrations of these patterns. Full entailment over a
populated KG is deferred (see (ii)).

### (ii) NEEDS DATA / USERS / APPLICATION — state as future work

These cannot be done honestly from a ~79-triple demonstrator with no app/users;
present them explicitly in a Future Work / Threats subsection so reviewers see
they are recognized, not overlooked.

- **Task-based / application-based evaluation.** Requires a deployed application
  exercising the ontology on a real task. Future work; the demonstrator ABox
  queries are a proxy, not a substitute.
- **User-centered / FOCA expert evaluation.** Requires recruiting domain experts
  (heritage scholars, Guthi/Newar community knowledge-holders). *Flag this as the
  most important domain-validity step* given cultural sensitivity — consistency
  does not establish cultural correctness.
- **CQ entailment over a populated KG.** Requires building/ingesting a real
  populated knowledge graph (the current ABox is a demonstrator, ~79 triples).
  Future work; pairs with FIX-7's schema-level entailment as the bridge.
- **True gold-standard precision/recall.** Requires constructing or obtaining a
  curated reference vocabulary for living-heritage Kathmandu Valley concepts —
  none exists. Future work.
- **Live deployment artefacts.** w3id dereferenceability (the failing FOOPS A1
  check) and a live SPARQL endpoint require deployment; note as a deployment
  task, not an evaluation gap to be papered over.

---

## D. Drop-In Template for the Single Most Impactful DO-NOW Addition (FIX-1: OntoClean)

The following is honest, contains no fabricated numbers, and leaves `[VERIFY]`
placeholders wherever a real assignment/verdict must be filled in by the authors
after performing the analysis. It is written to be dropped into §2 / a new §2b.

> **Ontological Rigour: OntoClean Meta-Property Analysis.**
> To complement the reasoner-based consistency check (§1) — which establishes
> that the taxonomy is *logically* satisfiable but not that it is
> *ontologically* well-founded — we applied the OntoClean methodology (Guarino &
> Welty) to the backbone of the HeritageGraph class hierarchy. For the
> [VERIFY: N] top-level and backbone classes (the roots of the depth-4 hierarchy
> and their immediate subclasses), each class was tagged with the four OntoClean
> meta-properties: rigidity (±R / ~R), identity (±I), unity (±U / ~U), and
> external dependence (±D). For example, a class such as *[VERIFY: e.g.,
> PhysicalTemple]* carries its own identity criterion and is rigid (+I, +R),
> whereas a role-like class such as *[VERIFY: e.g., Kumari / GuthiTrustee]* is
> anti-rigid and externally dependent (~R, +D), since an individual is a
> goddess-incarnation or a trustee only contingently and in virtue of an external
> relation. We then checked the OntoClean subsumption constraints — notably that
> an anti-rigid class cannot subsume a rigid class, that classes with
> incompatible identity criteria cannot stand in subsumption, and that
> carriers of unity are not subsumed by non-carriers. Of the constraints
> evaluated, we found [VERIFY: number] violations: [VERIFY: list each, or "none"].
> [VERIFY: For each violation, describe the resolution — e.g., re-modelled the
> offending is-a as a non-taxonomic relation, introduced a role pattern, or
> justified the retention.] This analysis addresses the rigour-based taxonomy
> evaluation layer (Brank/Gangemi/Vrandečić) that reasoner consistency alone does
> not cover, and is particularly salient for a domain where role-like and
> phase-like concepts (living-goddess incarnation, trusteeship, festival
> participation) sit alongside rigid physical and conceptual entities.

Accompanying table to insert directly beneath the paragraph:

> | Class | Rigidity | Identity | Unity | Dependence | Constraint check |
> |---|---|---|---|---|---|
> | [VERIFY] | [VERIFY ±R/~R] | [VERIFY ±I] | [VERIFY ±U/~U] | [VERIFY ±D] | [VERIFY pass/violation] |

Why this is the highest-impact DO-NOW item: it is the most prominent *missing*
standard method in the section, it requires no data/users/application, it speaks
directly to the modelling-correctness question that a consistent-but-possibly-
wrong taxonomy leaves open, and it is uniquely well-motivated by this ontology's
domain (role and phase concepts like the Kumari and Guthi trusteeship are exactly
what OntoClean is designed to discipline).

---

## Summary

The current evaluation is strong on automated/formal checks (consistency, SHACL,
FAIR/pitfalls, deductive yield) and on its headline provenance-under-contradiction
contribution, but under-covers the **rigour-based taxonomy** and
**context/application** layers and relies on a **single reasoner** and a
**single rater**. The five fully-feasible DO-NOW additions — **OntoClean
(FIX-1)**, **CQ traceability matrix (FIX-2)**, **cross-reasoner confirmation
(FIX-3)**, **evaluation-layers framing (FIX-4)**, and **lexical completeness
(FIX-5)** — plus the honest reframings of alignment/competitors (FIX-6) and the
schema-level CQ entailment (FIX-7), can all be implemented from the existing
schema and local toolchain with no fabricated numbers. Task-based, user-centered,
gold-standard, and populated-KG evaluations are genuine future work and should be
stated as such rather than glossed.
