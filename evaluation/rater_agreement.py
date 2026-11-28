#!/usr/bin/env python3
"""Agreement between two independent raters of HeritageGraph's mappings.

    python3 evaluation/rater_agreement.py RATER1.csv RATER2.csv

Each file is a completed copy of evaluation/rater/mapping_rater_sheet.csv
(scripts/gen_rater_sheet.py). The mappings both raters judged are compared on
their verdict (accept / reject / revise): the script prints the number
compared, the observed agreement, Cohen's kappa with its interpretation
(Landis & Koch), the confusion matrix, and every disagreement, which the
raters then discuss; the resolved verdicts go to
evaluation/mapping_rater_verdicts.csv. Writes results/rater_agreement.json.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

LABELS = ("accept", "reject", "revise")


def load(path: str) -> dict:
    with open(path, newline="", encoding="utf-8") as f:
        return {(r["subject_id"], r["predicate_id"], r["object_id"]): r["verdict"].strip().lower()
                for r in csv.DictReader(f) if r.get("verdict", "").strip()}


def cohen_kappa(pairs: list) -> tuple[float, float]:
    """(observed agreement, kappa) for a list of (verdict1, verdict2)."""
    n = len(pairs)
    if n == 0:
        raise ValueError("no mapping was judged by both raters")
    po = sum(a == b for a, b in pairs) / n
    c1, c2 = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(c1[k] * c2[k] for k in set(c1) | set(c2)) / (n * n)
    kappa = 1.0 if pe == 1 else (po - pe) / (1 - pe)
    return po, kappa


def interpret(k: float) -> str:
    if k < 0:
        return "poor"
    for bound, word in ((0.20, "slight"), (0.40, "fair"), (0.60, "moderate"),
                        (0.80, "substantial"), (1.01, "almost perfect")):
        if k <= bound:
            return word
    return "almost perfect"


def main(argv: list) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    r1, r2 = load(argv[1]), load(argv[2])
    bad = {v for v in list(r1.values()) + list(r2.values()) if v not in LABELS}
    if bad:
        print(f"unknown verdict(s) {sorted(bad)}: use accept, reject or revise", file=sys.stderr)
        return 1
    both = sorted(set(r1) & set(r2))
    pairs = [(r1[k], r2[k]) for k in both]
    if not pairs:
        print("The two sheets share no judged mapping: rater 2 judges the rows marked second_rater = yes.",
              file=sys.stderr)
        return 1
    po, kappa = cohen_kappa(pairs)
    print(f"Mappings judged by both raters: {len(both)}")
    print(f"Observed agreement: {po:.3f}")
    print(f"Cohen's kappa: {kappa:.3f} ({interpret(kappa)})")
    print("\nConfusion (rows rater 1, columns rater 2):")
    print(f"{'':<10}" + "".join(f"{l:>9}" for l in LABELS))
    for a in LABELS:
        print(f"{a:<10}" + "".join(f"{sum(1 for x, y in pairs if x == a and y == b):>9}" for b in LABELS))
    dis = [(k, r1[k], r2[k]) for k in both if r1[k] != r2[k]]
    if dis:
        print(f"\nDisagreements to resolve ({len(dis)}):")
        for (s, p, o), a, b in dis:
            print(f"  {s} {p} {o}: {a} vs {b}")
    out = Path(__file__).resolve().parent / "results" / "rater_agreement.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"n": len(both), "observed_agreement": po, "kappa": kappa,
                               "interpretation": interpret(kappa), "disagreements": len(dis)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
