# Rewrite plan — three sections to Q1, grounded in the reference papers

Targets (current line numbers in `tgdk-overleaf/main.tex`):
- §3.2 **Ontology Metrics and Standards Compliance** (L317–361)
- §3.3 **Event-Mediated Tangible Heritage** (L362–385)
- §3.4 **Living Goddess Lifecycle** (L387–394)

This is the **plan only** (ARS `/ars-outline` deliverable). Execution path and the
skills for each step are in §5.

---

## 0. What the reference papers actually do (extracted patterns)

Two reusable "section archetypes" recur across the closest peers. I pulled these
from the downloaded PDFs (quotes/loci verified, not from memory).

### Archetype A — *specification / metrics / standards* (ArCo, SeaLiT)
| Convention | Evidence in the peers |
|---|---|
| **A1. Numbers earn their place by backing a claim**, not as a catalogue. | ArCo ties counts to its testing/requirements; SeaLiT reports class/property counts *next to* the competency questions they satisfy. |
| **A2. Explicit conformance to *named* standards/profiles.** | SeaLiT: every class "a direct subclass or descendant of a CIDOC-CRM class"; CRM = ISO 21127. ArCo states OWL profile + SHACL/test artifacts. |
| **A3. Reproducibility block:** tool + version + config + artifact link. | ArCo: GitHub, Docker releases, versioning, test suite (OWL files + SPARQL). |
| **A4. Separate *description* from *evaluation results*.** | ArCo's metrics/specification is descriptive; consistency/inference testing lives in the testing section. |
| **A5. Comparative framing** where possible. | ArCo/EDM position their numbers against the standard they extend. |

### Archetype B — *modeling pattern / lifecycle* (ArCo-pattern, ICON, Recurrent-Situations ODP)
| Convention | Evidence in the peers |
|---|---|
| **B1. Fixed narrative: Problem → Pattern (abstract) → Formalization (axioms) → Implementation → Example.** | Recurrent ODP: *"Section 2 introduces the problem; Section 3 describes the pattern at an abstract level; Section 4 presents implementations; Section 5 usage examples."* |
| **B2. Competency Questions stated up front** (usually a table). | Recurrent ODP "Table 1: Competency questions answered…"; ICON §4 requirements as CQs; ArCo CQs drive design. **This is the single biggest missing element in HeritageGraph.** |
| **B3. Numbered axioms** for the formal core. | Recurrent ODP: "(axiom 1) … (axiom 7)"; HeritageGraph already has one Manchester `Listing` — extend the device. |
| **B4. Explicit reuse statement** (which ODP/CRM construct, direct vs indirect). | ArCo direct/indirect reuse; Recurrent ODP reuses Period ODP, d0:Eventuality. |
| **B5. A worked running example with real instance data** (+ SPARQL answering a CQ). | ICON "Reading…" example; ArCo running examples = NL CQ + SPARQL. |
| **B6. Explicit generalization/reusability claim.** | Recurrent ODP "reusable template"; HeritageGraph's Living-Goddess para already nails this ("reusable template for any temporally bounded sacred status")—keep it. |
| **B7. Ground the design in a named theory/authority.** | ICON grounds everything in Panofsky's three levels (Table 1). HeritageGraph can ground in CIDOC-CRM principles + the cited ethnographic authorities (letizia2013goddess, lewis2016vajrayana). |

---

## 1. §3.2 Ontology Metrics and Standards Compliance

**Diagnosis.** Currently a dense two-paragraph *data dump* (counts in prose) +
Table. Three problems vs Archetype A: (i) numbers are listed, not argued (A1);
(ii) no explicit profile/standard conformance statement — we never say *which* OWL 2
profile, nor claim ISO 21127 / PROV-O conformance (A2); (iii) it mixes **evaluation
results** (HermiT consistency, OWL-RL closure 5,058→25,365) into a description
section (A4). Strengths to keep: it already ties some axioms to invariants
(single-deity embodiment max 1; mandatory provenance min 1) — that is exactly A1;
extend it.

**Target structure (3 short paragraphs + the existing table):**
1. **Framing sentence (A1):** "Table N profiles HeritageGraph along three axes —
   *expressivity*, *standards conformance*, and *logical tightness* — each chosen to
   substantiate a design claim of §3.1." Then walk the table by *theme*, not by row.
2. **Standards conformance (A2):** one paragraph stating, explicitly: OWL 2 DL
   profile (name it); the structural invariant re-quantified (31 external
   `subClassOf` to CRM/PROV; 42 classes / 73 properties aligned; 13 vocabularies);
   ISO 21127 alignment via CRM; PROV-O for provenance; Getty AAT for the 64
   enumeration individuals. Frame as *conformance*, not counts.
3. **Logical tightness + reproducibility (A1+A3), forward-ref evaluation (A4):**
   keep disjointness (70 axioms), cardinality invariants, SHACL (61 shapes) as
   *what they buy* (closed-world validation, domain invariants); **move** the HermiT
   consistency / OWL-RL closure numbers to a single sentence that *forward-references*
   §Evaluation rather than reporting the result here; add the reproducibility pointer
   (artifact: `HeritageGraph.ttl`, LinkML source, generated OWL/SHACL/ShEx/JSON-Schema;
   tool versions). 

**Q1 moves:** name the OWL 2 profile; assert conformance explicitly; one comparative
clause (depth-4, 70 classes vs a peer); every number adjacent to the claim it backs.
**Needs from you:** (a) confirmed OWL 2 profile (DL? RL-safe?); (b) public artifact
URL / DOI (Zenodo/GitHub) for the reproducibility pointer.

---

## 2. §3.3 Event-Mediated Tangible Heritage

**Diagnosis.** Content is strong and already follows half of Archetype B: it opens
with the Problem (B1 ✓), reuses CRM constructs explicitly (B4 ✓), has one Manchester
listing (B3 partial). **Missing:** competency questions (B2), a worked instance
example + SPARQL (B5), and the per-event mapping is a long dense prose block that a
**CRM-alignment table** would carry far better.

**Target structure:**
1. Problem paragraph — keep (tighten; it overlaps slightly with §3.1 P1 now, so
   trim the museum-cataloguing restatement to one clause and cross-ref §3.1).
2. **Add a Competency-Questions paragraph or mini-table (B2):** 3–4 CQs the pattern
   answers, e.g. *"What was the condition of temple T at successive assessments?"*,
   *"Who produced object O, when, and by what technique?"*, *"Which custody transfers
   moved O between Guthis?"*.
3. Class hierarchy itemize — keep.
4. **Convert the five-event prose block into a table (A1/B-readability):** columns
   = Event class | CRM mapping | key participants/properties | what contingency it
   captures. Keep one or two sentences of prose for the subtle cases (Consecration
   vs Enshrinement) that a table can't carry.
5. Keep the `Production` Manchester listing; optionally add **numbered axioms** for
   the Consecration "before/after divine presence" claim (B3) — its strongest point.
6. **Add a worked example (B5):** one real object (e.g., a named temple/Murti) shown
   as a few RDF/Turtle triples instantiating Production + ConditionAssessment, and
   **one SPARQL query** answering a CQ from step 2. This is the highest-value Q1 add.
7. Recurrence paragraph — keep; **cite the Recurrent-Situations ODP** (`recurrentodp2021`)
   as the design precedent for `recurrence_pattern` (B4/B7).

**Needs from you:** a real instance to use as the running example (temple + its
production/condition facts), and whether a SPARQL endpoint/dataset exists to cite.

---

## 3. §3.4 Living Goddess Lifecycle

**Diagnosis.** A single, well-argued paragraph — the rationale (period vs event;
anti-identity; OntoClean-style reasoning) is genuinely Q1-grade prose (B6 ✓, B7
partial). **Missing:** CQs (B2), a worked example with the *actual* institution
(B5), numbered axioms for the Selection→Tenure→Retirement core (B3), and an explicit
OntoClean citation now that we introduced it in §3.1.

**Target structure:**
1. Problem sentence — keep (Kumari poses a role-modeling problem).
2. **Theory/authority grounding (B7):** add the one-clause OntoClean tie
   (`guarinowelty2002`): tenure is anti-rigid → period, not identity; this now
   echoes §3.1 deliberately.
3. Core modeling paragraph — keep, but pull the dense property list into a small
   **axiom listing (B3)** (Manchester) mirroring the `Production` listing: 
   `LivingGoddessTenure ⊑ E4_Period`, `embodied_deity max 1`, `had_participant min 1`,
   `has_timespan min 1`.
4. **CQs (B2):** e.g. *"Who embodied deity D during period P?"*, *"Which selection
   established tenure T and on what lakshana criteria?"*, *"What is the temporal
   extent of a given tenure?"*.
5. **Worked example (B5):** instantiate one real tenure (a named Kumari, residence,
   Guthi, timespan) as Turtle + one SPARQL answering a CQ.
6. Generalization claim — keep verbatim (it's already the B6 model sentence).

**Needs from you:** permission/accuracy check to name a real Kumari tenure as the
worked example (sensitivity — a living sacred institution); if not, use an
explicitly anonymized/illustrative instance.

---

## 4. Cross-cutting Q1 levers (apply to all three)

1. **Competency Questions** — the field-standard device the paper currently lacks
   entirely. Adding them is the biggest single jump toward Q1 (B2).
2. **One worked running example + SPARQL** shared across the sections (use the same
   temple/Kumari instance) — mirrors ArCo/SeaLiT application sections (B5).
3. **Tables over dense prose** for CRM mappings and metrics (A1, readability).
4. **Explicit standards-conformance + reproducibility** statements (A2, A3).
5. **Numbered axioms** as the formal anchor per pattern (B3).
6. Tighten the now-slight overlap between §3.3's problem paragraph and the new §3.1 P1.

---

## 5. Execution path + skills (your "which skills" question)

| Step | Skill | Why |
|---|---|---|
| Assess peer section craft | *(done here — local PDF analysis; no skill needed)* | Cheaper/higher-signal than a subagent re-deriving context. |
| **Plan the rewrite** | **`/ars-outline`** | "Detailed outline + evidence map, no draft" = exactly this document; rerun it to formalize per-section outlines if you want the ARS template. |
| **Draft the Q1 rewrite** | **`/ars-revision`** | Produces the revised section text; I feed it this plan + the target sections. |
| **Set/verify the Q1 bar** | **`/ars-reviewer`** | Simulated peer panel (EIC + reviewers + devil's advocate) → tells us if it clears a Q1 venue and what's still weak. |
| Address review, iterate | **`/ars-revision`** (round 2) | Close the panel's points. |
| Citation hygiene | **`/ars-citation-check`** | Verify the new `recurrentodp2021` / OntoClean / SeaLiT cites + any added refs. |
| (Optional one-shot loop) | **`/ars-full`** | Runs research→write→review→revise→finalize end-to-end if you'd rather not drive each step. |

**Recommended order:** approve this plan → `/ars-revision` on the three sections →
`/ars-reviewer` to confirm Q1 → `/ars-revision` round 2 → `/ars-citation-check`.

**Blocking inputs before drafting** (collected from §§1–3):
- OWL 2 profile name + public artifact URL/DOI (for §3.2).
- A real instance (temple/Murti + facts) for the shared worked example, and whether
  a SPARQL endpoint exists to cite (for §3.3 + §3.4).
- Go/no-go on naming a real Kumari tenure as the §3.4 example (sensitivity).
