#!/usr/bin/env python3
"""The documentation's Evaluation page, from the repository's own evaluation.

    python3 scripts/gen_eval_page.py      # after `make reproduce`

Writes docs-src/evaluation.md (tracked; ontoreview.toml includes it as a page
of the documentation). Every figure comes from a file `make reproduce` writes:
evaluation/heritagegraph-numbers.tex (the paper macros), results/metrics.json,
results/alignment.json, results/abox_cq32_report.csv, results/cq_mutation.csv,
results/cq_traceability.csv and results/inference_cq_report.txt. OntoReview
builds the documentation only; its generic quality checks are switched off,
because these checks are specific to what HeritageGraph claims.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "evaluation" / "results"
OUT = ROOT / "docs-src" / "evaluation.md"


def macros() -> dict:
    text = (ROOT / "evaluation" / "heritagegraph-numbers.tex").read_text(encoding="utf-8")
    return dict(re.findall(r"\\newcommand\{\\hg(\w+)\}\{([^}]*)\}", text))


def rows(name: str) -> list:
    with open(RES / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    m = macros()
    metrics = json.loads((RES / "metrics.json").read_text())
    align = json.loads((RES / "alignment.json").read_text())
    cq = rows("abox_cq32_report.csv")
    mut = rows("cq_mutation.csv")
    trace = rows("cq_traceability.csv")
    iq = [l for l in (RES / "inference_cq_report.txt").read_text(encoding="utf-8").splitlines()
          if re.match(r"^IQ\d", l)]

    dims = Counter(r["dimension"] for r in cq)
    passed = sum(r["status"] == "PASS" for r in cq)
    swaps = sum(int(r["sibling_swaps"]) for r in mut)
    swaps_killed = sum(int(r["sibling_swaps_killed"]) for r in mut)
    single = sum(r["gold_rows"] == "1" for r in mut)
    need_tbox = sum(int(r["tbox_axioms_needed"]) > 0 for r in mut)
    by_kind: dict = {}
    for r in trace:
        k = by_kind.setdefault(r["kind"], [0, 0, 0])
        k[0] += 1
        k[1] += bool(r["used_in_cqs"].strip())
        k[2] += int(r["demonstrator_uses"] or 0) > 0

    out = []
    w = out.append
    w("All figures on this page are produced by one command from a clean checkout of the repository, "
      "`make reproduce`, which regenerates every artefact from the LinkML source, checks that the "
      "regenerated files equal the released ones, runs every release check, and fails if a figure here "
      "or in the paper is stale. The checks are listed in the repository's `Makefile` (`check` target).")
    w("")
    w("## The ontology")
    w("")
    w("| | |\n|---|---|")
    w(f"| OWL triples | {m['OwlTriples']} |")
    w(f"| Classes (excluding enumerations) | {m['Classes']} |")
    w(f"| Enumerations | {m['Enumerations']} |")
    w(f"| Object / datatype properties | {m['ObjectProperties']} / {m['DatatypeProperties']} |")
    w(f"| Classes stated subclasses of a CIDOC-CRM class | {m['ClassesUnderCRM']} |")
    w(f"| Deprecated terms (kept, never deleted) | {m['Deprecated']} |")
    w(f"| SHACL shapes | {m['NodeShapes']} node shapes, {m['ShaclTriples']} triples |")
    w(f"| Mappings to other vocabularies (SSSOM) | {m['SssomMappings']} |")
    w(f"| CIDOC-CRM terms reused / HeritageGraph terms linked to CIDOC-CRM | "
      f"{align['cidoc_crm_classes_reused']} classes, {align['cidoc_crm_properties_reused']} properties / "
      f"{align['cidoc_crm_hg_classes_linked']} classes, {align['cidoc_crm_hg_properties_linked']} properties |")
    w("")
    w("## Logic")
    w("")
    w("- The ontology is in the OWL 2 DL profile and consistent under HermiT, with no unsatisfiable class.")
    w("- With CIDOC-CRM 7.1.3, CRMinf 1.0, CRMsci 2.0 and PROV-O loaded unmodified (each pinned by "
      "checksum), the merged graph is consistent, has no unsatisfiable class and no unintended class "
      "equivalence, with and without the optional CRM-PROV bridge.")
    w("- The core states no axiom about a term of another vocabulary unless that vocabulary states it "
      "itself, and gives no external class a HeritageGraph superclass (checked with a negative control).")
    w("- Every example data set is consistent with the ontology and with all aligned vocabularies.")
    w("- Inconsistency injection: the axioms bite (two embodied deities, a thing that is both a temple "
      "and a deity, a structure both destroyed and extant are each inconsistent; the controls are not).")
    w("")
    w("## Competency questions")
    w("")
    w(f"- **{passed} of {len(cq)}** competency questions return exactly their expected answers over the "
      f"demonstrator data, both as asserted and under OWL 2 RL entailment; a deliberately broken query "
      f"is detected (negative control).")
    w("- By dimension: " + ", ".join(f"{d} {n}" for d, n in sorted(dims.items())) + ".")
    w(f"- **Inference questions**: {len(iq)} questions whose answers grow only with HeritageGraph's "
      f"axioms: each returns fewer answers over the asserted data and over the external vocabularies alone "
      f"(each frozen set checked) than with HeritageGraph:")
    w("")
    for l in iq:
        mt = re.match(r"^(IQ\d) \[(\w+)\].*with-HG=(\d+)\s+(.*)$", l)
        if mt:
            w(f"  - {mt.group(1)} ({mt.group(3)} answers, {mt.group(2)}): {mt.group(4)}")
    w("")
    w("### How much the questions test (mutation analysis)")
    w("")
    w(f"- {single} of {len(mut)} questions have a single expected answer in the demonstrator (one "
      f"witness); their evidence is thin (see the limitations below).")
    w(f"- Swapping a term for a sibling HeritageGraph term changes the answer in {swaps_killed} of {swaps} "
      f"applicable cases.")
    w(f"- {need_tbox} questions depend on a TBox axiom (their answer changes when the axiom is deleted).")
    w("")
    w("### Coverage of the vocabulary")
    w("")
    w("| | terms | used in a question | used in the demonstrator |\n|---|---|---|---|")
    for kind, (n, in_cq, in_demo) in sorted(by_kind.items()):
        w(f"| {kind} | {n} | {in_cq} | {in_demo} |")
    w("")
    w("## Data validation (SHACL)")
    w("")
    w(f"- {m['Examples']} example data sets each have their expected validation outcome.")
    w(f"- **{m['NegativeTests']} negative tests**, each a single injected error (a missing required value, "
      f"a value of the wrong class or datatype, a value outside a controlled vocabulary, a time-span "
      f"ending before it begins, two labels in one language, a misspelt property, a conflicting belief "
      f"without a rival, ...), are all caught, each by the expected constraint (on the expected property, or on "
      f"the node for the three node-level rules).")
    w("- The shapes are open, so data may use other vocabularies; three SHACL-SPARQL rules check what open "
      "shapes cannot (an undeclared or deprecated HeritageGraph property, a conflicting belief without a "
      "rival).")
    w("")
    w("## Modelling experiments")
    w("")
    w("- **Tenure** against the CIDOC-CRM role idiom (property of property P14.1) and the Wikidata P39 "
      "idiom: the same questions over the same facts, compared on answers and query size.")
    w("- **Custodianship and endowment**: an endowment held by a state heritage body that sustains a "
      "festival, a hereditary office held under that body's mandate, and a custody chain from a Guthi to "
      "the state body, with their questions.")
    w("- **Multiple calendars**: Bikram Sambat and Nepal Sambat dates converted to Gregorian bounds with "
      "full new-year windows, checked against positive and negative controls.")
    w("- **Reuse outside Nepal**: the generic Tenure pattern describes a church office and a museum "
      "custody period with no Nepal-specific term, and one query answers both.")
    w("- **PROV-O consumer**: queries that use only PROV-O terms traverse every recorded belief to its "
      "agent and source, over the data with the HeritageGraph TBox and the optional CRM-PROV bridge (which "
      "makes CRM-typed agents PROV agents).")
    w("")
    w("## Known limitations")
    w("")
    w("- The mappings are curated by the authors; independent rater verdicts are being collected (the "
      "rating sheet and the agreement script are in `evaluation/rater/`).")
    w("- The competency questions were written by the authors; a protocol for held-out questions from "
      "external experts is in `evaluation/expert_cq/`.")
    w("- The demonstrator is a small curated graph; a large populated graph (the DANAM data set) is built "
      "in a separate repository.")
    w(f"- The questions exercise {by_kind.get('class', [0, 0])[1]} of {by_kind.get('class', [0])[0]} classes "
      f"and {by_kind.get('property', [0, 0])[1]} of {by_kind.get('property', [0])[0]} properties; most questions "
      f"retrieve data, and {need_tbox} depend on a TBox axiom (the inference questions test the axioms).")
    w("- Lunar dates are recorded as text; structured lunar dating and recurring-practice modelling are "
      "future work.")
    w("")
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
