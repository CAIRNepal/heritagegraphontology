#!/usr/bin/env python3
"""Convert the hand-authored HeritageGraph figure SVGs to PDF/PNG for the TGDK manuscript.

Each SVG is the editable source (TTL-correct pattern figure); the PDF is what
main.tex includes and the PNG is a convenience preview. Requires: rsvg-convert
(librsvg).

  python3 scripts/generate_event_centric_figure.py            # all known figures
  python3 scripts/generate_event_centric_figure.py <stem> ... # only these stems

A "stem" is the filename without extension, e.g. HeritageGraph-Event-Centric.
Any *.svg in the figures directory is eligible; STEMS lists the ones we ship.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "tgdk-overleaf" / "figures"

# Editable SVG sources kept TTL-correct and regenerated into the manuscript.
STEMS = (
    "HeritageGraph-Event-Centric",
    "HeritageGraph-Institutional_Infrastructure",
    "HeritageGraph-Epistemic_Provenance",
    "HeritageGraph-Module-Alignment",
    "HeritageGraph-Vocabulary-Reuse",
)

def convert(stem: str) -> bool:
    svg = FIG / f"{stem}.svg"
    if not svg.exists():
        print(f"Missing {svg}", file=sys.stderr)
        return False
    for fmt in ("pdf", "png"):
        out = FIG / f"{stem}.{fmt}"
        subprocess.check_call(["rsvg-convert", "-f", fmt, "-o", str(out), str(svg)])
        print("Wrote", out)
    return True

def main(argv: list[str]) -> int:
    stems = argv[1:] or list(STEMS)
    ok = all(convert(s) for s in stems)
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
