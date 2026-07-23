# Evaluation Section Revision Roadmap

**STATUS: TGDK RE-STRUCTURE PIPELINE EXECUTED 2026-07-23 (second pass).**
Applied the five-stage TGDK-calibrated pipeline on top of the trim passes below:
(1) **Restructure** — kept the title "Evaluation" (0/11 TGDK papers use
"Validation"; ~half use "Evaluation"); added a headline one-paragraph results
summary as the section's first paragraph; **reordered subsections by evidential
weight** so the contribution-bearing experiments lead (Competency Questions →
Constraint Validation → Provenance under Contradiction → Alignment Quality →
LUX Case Study) and the confirmatory formal-hygiene checks (Logical
Consistency, Modelling Quality & FAIR Readiness) now sit just before Threats.
Cross-references are label-based and all 20 in-section `\ref`s resolve.
(2) **Register** — converted the SHACL constraint-component census from prose
into `tab:wc-census`; the "beyond venue norm" experiments (merged
classification, injection, negative control, PROV-O consumer, SHACL census)
are now explicitly framed as rigor beyond the TGDK norm in the preamble and
kept concise. (3) **Ablation table** — the three plain-CRM baselines collapsed
into `tab:wc-ablation` (Pattern / baseline / what is lost) with a one-sentence
lead; added an explicit **adoption-absence** caveat to Threats (first public
release, no external uptake yet). (4) **Limitations** — the labelled Threats
subsection is confirmed last in the section; lead de-brittled ("Several
limitations" rather than a hard count). (5) **Re-measure** — §7 prose now
≈3,950 words, **37.3%** of the Intro–Conclusion body; slightly above the ~33%
TGDK centre but justified by the above-norm formal battery, which is now
framed as such. No experiment or number removed.

---

**STATUS: EXECUTED 2026-07-23.** All trim passes (T1–T7) and removals (R1–R3)
applied to `tgdk-overleaf/main.tex`. §7 reduced from 5,175 to 3,786 words
(−27%). Per-subsection outcomes: §7.1 694→484 (incl. merged classification
~140w and three-arm injection ~60w), §7.2 623→469, §7.3 1,622→928 (two worked
CQs — CQ11, CQ25 — retained; the CQ1 and CQ27/31 walkthroughs deleted, their
per-CQ outcomes remaining in the appendix table and the released runner;
three baselines collapsed into one "Pattern ablations" block; custodianship,
multi-calendar, and entailment paragraphs compressed to verdict level),
§7.4 327→274, §7.5 669→497, §7.6 334→305, §7.7 264 (untouched, K3),
§7.8 449→372. §4.2's duplicate closure numbers now defer to Table 1 /
the evaluation (R2). No experiment removed from the released suite; every
finding and number retained. A1 (terminological coverage experiment) NOT
executed — deliberately deferred per §5/§6 of this roadmap.

## TGDK calibration (added 2026-07-23, 11 TGDK papers surveyed)

Surveyed the evaluation sections of 11 TGDK papers — the 8 "Resources for
Graph Data and Knowledge" special-issue papers (Vol 2 Issue 2: NEOntometrics,
dblp KG, FAIR Jupyter, OTTR, TØIRoads, Whelk, MELArt, Horned-OWL), the closest
peer set, plus KG2Tables, CoaKG, and GraphRAG-schema from Vol 3. PDFs in
`reference-papers/tgdk/`. Findings that revise the target above:

1. **Length: 33% is IN-BAND, not an outlier.** TGDK evaluation blocks span 5%
   (dblp performance subsection) to 55% (MELArt), central tendency ~25–35%.
   The Vol 3 research/resource papers cluster higher (33–45%). HeritageGraph's
   §7 at 33% sits in the middle. **The earlier ~25% target was set from
   non-TGDK peers and is too aggressive for this venue — heavy further cutting
   is NOT required and would weaken the MAJOR_REVIEW.md defenses.**
2. **Naming: 0/11 use "Validation"; ~half use "Evaluation."** The rest carry
   the burden under descriptive titles ("Proof of Concept", "Results and
   Discussion", "Uses", "Performance", "Benchmark Generation"). Retitling §7 or
   its subsections descriptively is optional polish, not required.
3. **The formal battery EXCEEDS the norm.** SHACL, OOPS!, FAIR/FOOPS scoring,
   CQ-entailment, and reasoner consistency appear in ~0/11 TGDK papers. Keep
   them — they are a differentiator — but present concisely, not as centerpiece.
4. **The real TGDK gap HeritageGraph cannot fill now:** every TGDK resource
   paper leads with adoption/usage statistics and/or performance-scale figures.
   HeritageGraph is pre-adoption, so it honestly has neither; the LUX case
   study is the nearest substitute. This is a limitation to state, not a
   fixable trim.
5. **Register: state the result; drop the meta-commentary.** TGDK papers report
   "31 of 32 return identical answers" — they do not write "both sides of the
   reading hold" or "we state plainly what the verdict is worth." This is the
   highest-value quality lever and the one applied in the register pass below.

**Revised verdict:** the section is already at a TGDK-appropriate length and
above the venue's methodological bar. To reach publishable level it needs
plainer register and (optionally) descriptive subsection titles, NOT another
big cut. A register pass was applied 2026-07-23 (see status line), trimming
meta-commentary to 32.9% with zero evidence loss. Going below ~28% is
discretionary and trades review-defense coverage for brevity.

Produced 2026-07-23 (revision-coach mode). Basis: a survey of the evaluation
sections of all 13 published papers in `reference-papers/` (SeaLiT, ArCo ISWC
2019, ArCo SWJ 2021, ICON JOCCH 2023, PWO SWJ, ODP-Annotation SWJ, InBiodiv-O,
HERITRACE 2025, ODP-RecurrentSituations, CRMdig, Aldrovandi 2024, POI Heritage
Science 2022, CulturalGems 2024), compared against `tgdk-overleaf/main.tex` §7.

## 1. Calibration: where the paper stands against the corpus

Current state of main.tex:
- §7 ≈ 5,200 words across 9 subsections ≈ **40% of the paper body** (~12,900
  words), plus the per-CQ appendix. §7.3 alone (~1,600 words) is the largest
  subsection in the paper — larger than Related Work.

Corpus norms:
- **7 of 13 peers have no measured evaluation section at all** (SeaLiT, PWO,
  ODP-Annotation, HERITRACE, CRMdig, CulturalGems, ODP-RecurrentSituations).
  They substitute worked examples, feature comparisons, or deployment
  narratives.
- The two heaviest peers — **ArCo SWJ (~21% of paper)** and **ICON JOCCH
  (~26%)** — are the ceiling. Both report aggregate pass/fail counts with 1–6
  worked examples, never per-experiment multi-paragraph narratives.
- The common core toolkit is: CQ unit tests (count + aggregate verdict + a few
  worked examples), reasoner consistency (one sentence to one paragraph),
  error provocation (ArCo: counts only), OOPS!/FOOPS! (ICON only, ~2
  paragraphs), and one baseline comparison (terminological coverage or
  granularity vs CIDOC-CRM/EDM/Wikidata).
- **No peer has**: SHACL constraint census, threats-to-validity subsection,
  merged-import classification, negative controls, supersession experiments,
  PROV-O consumer tests, multi-calendar experiments, or LUX-scale migration.
- Register: peers assert results in one sentence ("All issues have been
  fixed"; "All the CQs confirmed the expected results") and put mechanics in
  the methodology section or the repository.

**Diagnosis.** HeritageGraph's evaluation exceeds the strongest published peer
on both instrument count and per-experiment narrative depth. The problem is
not the experiments — it is that the *paper* carries the full narrative of
each experiment, where peers carry the verdict + one worked example and leave
the mechanics to released artifacts. Target: **compress §7 from ~40% to
~25% of the body (≈ 3,000–3,300 words)** without deleting a single
experiment from the released evaluation suite. Every cut below moves prose to
the repository (scripts + `HeritageGraph_TGDK_EVALUATION.md`), never deletes
evidence — so all MAJOR_REVIEW.md responses remain defensible.

## 2. KEEP (as-is or near-as-is)

| ID | Item | Why |
|----|------|-----|
| K1 | §7 preamble: pre-registered, scripted protocol framing (~190w) | No peer has it; it is the paper's reproducibility differentiator. Keep. |
| K2 | §7.5 core contradiction experiment (claim–query–data walkthrough) | The reviewer called it "the paper's best experiment". ICON-style single worked example done right. Keep in full. |
| K3 | §7.7 LUX case study (~260w, just rewritten) | Already right-sized; no peer has third-party migration at all. Keep. |
| K4 | §7.8 Threats to Validity (~450w) | No peer has one; for TGDK this is a strength, and it absorbed multiple review responses. Keep (light trim OK). |
| K5 | §7.4 SHACL negative tests + census verdicts (~330w) | Unique instrument; already compact. Keep, keep the census as numbers not prose. |
| K6 | One-sentence consistency verdict + timing in §7.1 | Matches ArCo/ICON register exactly. |
| K7 | Per-CQ appendix | Appendix pages are cheap; ICON externalizes CQ notebooks, you inline them — either is acceptable. Keep unless page budget forces it out. |

## 3. TRIM / COMPRESS (the ~2,000-word reduction lives here)

| ID | Item | Current | Target | How |
|----|------|--------:|-------:|-----|
| T1 | §7.3 Competency Questions | ~1,620w | ~850w | The single biggest win. (a) Cut the four worked CQ walkthroughs to **two** (ICON shows 6 of 24 but in a 38-page paper; ArCo shows 1); point to the appendix for the rest. (b) Collapse the three baseline comparisons (event-vs-static ablation, sameAs-vs-reified, tenure-vs-actor-role) into one "pattern ablations" block: one 3–4-sentence verdict paragraph each, sharing a single summary table. The full protocols stay in the scripts. (c) Entailment re-run: keep the numbers and the property-hierarchy witness, cut to 3–4 sentences. |
| T2 | §7.1 merged-vocabulary classification paragraph | ~250w | ~100w | Keep the discovery (AssertionSubject ⊑ prov:Entity caught and repaired — this is a genuine selling point; ArCo reports "3 issues raised, all fixed" in one sentence). Cut the PROV-O property-chain repair mechanics to one sentence + pointer to the script; drop the process narrative ("this audit did its job before the results could be reported"). |
| T3 | §7.1 injection tests | ~150w | ~60w | ArCo register: counts + one clause per arm. "Two injection arms (double-deity tenure; Stupa∧Chaitya individual) are reported inconsistent; the control arm classifies consistent, with HermiT inferring co-denotation as open-world semantics prescribe." |
| T4 | §7.2 design-decision defense prose | ~620w | ~420w | Keep the OOPS!/FAIR reporting (ICON does both in ~2 paragraphs — match that); compress the per-decision defenses into the existing table and one linking paragraph. |
| T5 | §7.5 supersession + Proposition paragraph, PROV-O consumer | ~300w of §7.5's 670w | ~120w | Verdict sentences only: what the chain query returns, what the Proposition query returns, what the generic PROV consumer sees (36 entities). Mechanics → script. |
| T6 | §7.6 negative control | ~120w | ~60w | Two sentences: what was seeded, what was caught, what by design was not. |
| T7 | Repeated reproducibility framing | scattered | — | The "released with the evaluation scripts / re-runnable / versioned" clause appears in nearly every subsection. State it once in the preamble; delete the repetitions. |

Estimated outcome: §7 ≈ 3,100–3,300 words ≈ 24–26% of body — exactly the
ArCo-SWJ/ICON band.

## 4. REMOVE (from the paper; keep in the repository)

| ID | Item | Rationale |
|----|------|-----------|
| R1 | Process/history narration inside results (how an experiment came to be run, what an earlier release did wrong beyond the one-sentence repair note) | No peer narrates process; reviewers read it as padding. The full history lives in MAJOR_REVIEW.md and the changelog. |
| R2 | Duplicated numbers (closure sizes, constraint counts appearing in §4.2 *and* §7 prose *and* Table 1) | State each number once in the table, reference it. |
| R3 | Sub-experiment details of the SHACL census (per-component occurrence counts in prose) | Keep one summary sentence + the coverage claim; full census → repository report. |

## 5. ADD (at most one; guard against scope creep)

| ID | Item | Cost | Rationale |
|----|------|-----:|-----------|
| A1 | **Terminological / structural coverage comparison vs CIDOC-CRM and EDM** (ArCo-style: extracted domain vocabulary, matcher, coverage scores — ArCo reports 0.72 vs 0.29 vs 0.12) | Medium (one script + one paragraph) | This is the one instrument the two strongest peers have that you lack, and it directly supports the abstract's gap claim with a *number* rather than pattern-level ablations. Addresses MAJOR_REVIEW threat 7 (comparative baseline) at the level reviewers actually expect. Optional — the paper survives without it. |

Explicitly **not** recommended to add: user/curator study (declared future
work, corpus norm accepts this — HERITRACE defers it too), ArCo-at-reasoning-
level comparison (the reviewer advised against it), adoption statistics
(nothing truthful to report yet; SeaLiT-style sustainability statement already
exists in the availability section).

## 6. Suggested execution order

1. T1 (§7.3) — largest single reduction, no information loss.
2. T2+T3 (§7.1) — second largest; preserves both discoveries.
3. T4–T6, R1–R3 — mechanical passes.
4. K4 light trim of §7.8 if still over budget.
5. A1 only if you want the numeric gap-claim support; run it before any
   camera-ready deadline, not during the compression pass.

## 7. Traceability guard

Before cutting any paragraph, check MAJOR_REVIEW.md for the review item it
answers. The compression rule that keeps every response defensible:
**the finding and the number stay in the paper; the protocol and the process
move to the released scripts and evaluation report.** No review response is
weakened by moving mechanics to artifacts the paper already cites.
