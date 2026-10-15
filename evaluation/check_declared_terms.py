#!/usr/bin/env python3
"""Every HeritageGraph term used by the examples, queries, and evaluation code
must be declared in the released ontology.

Scans examples/ (ABoxes and examples/queries/), evaluation/ (scripts, fixtures,
expected answers), and the generated cq_sparql.md for HeritageGraph IRIs, in any
of the spellings the repository uses: CURIEs (hg:x, heritageGraph:x), full IRIs
(<https://w3id.org/heritagegraph/x>, including enumeration individuals such as
.../ConditionType#Damaged), and the Python constructions HG + "x" and U("x").
Each term must be the subject of an rdf:type triple in
ontology/HeritageGraph.ttl. A stale term (e.g. a snake_case name from an older
schema lineage, or hg:Person instead of crm:E21_Person) fails the check.

Instance IRIs (demo/, example/ namespaces) and the ontology's own document IRIs
are not terms and are ignored. Two exemptions are explicit and printed:
  * NEGATIVE_CONTROLS: terms that are undeclared on purpose (a test that must
    see a missing predicate);
  * SKIPPED: the LUX bridge module and its consumers, which are built on the
    pre-1.0.0 schema lineage and are out of scope until that module is migrated.

Exit status is non-zero if any undeclared term is found.

Run:  python3 evaluation/check_declared_terms.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from rdflib import Graph, RDF, URIRef

ROOT = Path(__file__).resolve().parents[1]
TTL = ROOT / "ontology" / "HeritageGraph.ttl"
HG = "https://w3id.org/heritagegraph/"

SCAN = [ROOT / "examples", ROOT / "evaluation", ROOT / "cq_sparql.md"]
SUFFIXES = {".ttl", ".rq", ".py", ".json", ".md", ".csv"}
IGNORED_DIRS = {".venv", "venv", "results", "__pycache__", "protege"}

# Instance / document namespaces under the HeritageGraph base that are not terms.
NON_TERMS = ("demo/", "example/", "ontology", "schema", "scheme/", "dataset",
             "alignment", "edm-profile")

NEGATIVE_CONTROLS = {
    "doesNotExistPattern": "run_abox_cq32.py self-test: a predicate no triple uses",
}
SKIPPED = {
    "examples/lux-murti-merged.ttl": "LUX bridge module (pre-1.0.0 schema lineage)",
    "evaluation/lux": "LUX bridge module evaluation (pre-1.0.0 schema lineage)",
}

PATTERNS = [
    re.compile(r"\b(?:hg|heritageGraph):([A-Za-z_][\w\-]*(?:\\?#\w+)?)"),
    re.compile(r"w3id\.org/heritagegraph/([A-Za-z_][\w\-/]*(?:#\w+)?)"),
    re.compile(r"\bHG\s*\+\s*[\"']([A-Za-z_][\w\-]*)[\"']"),
    re.compile(r"\bU\(\s*[\"']([A-Za-z_][\w\-]*)[\"']\s*\)"),
]


def declared_terms() -> set[str]:
    g = Graph()
    g.parse(TTL, format="turtle")
    return {str(s) for s in g.subjects(RDF.type, None)
            if isinstance(s, URIRef) and str(s).startswith(HG)}


def files() -> list[Path]:
    out = []
    for root in SCAN:
        paths = [root] if root.is_file() else sorted(root.rglob("*"))
        for p in paths:
            if not p.is_file() or p.suffix not in SUFFIXES:
                continue
            if IGNORED_DIRS & set(p.relative_to(ROOT).parts):
                continue
            if p.resolve() == Path(__file__).resolve():
                continue  # this file's docstring quotes stale terms as examples
            out.append(p)
    return out


def skipped(rel: str) -> str | None:
    for prefix, reason in SKIPPED.items():
        if rel == prefix or rel.startswith(prefix + "/"):
            return reason
    return None


def main() -> int:
    declared = declared_terms()
    undeclared: dict[str, set[str]] = {}
    checked, skips = 0, {}
    for path in files():
        rel = path.relative_to(ROOT).as_posix()
        reason = skipped(rel)
        if reason:
            skips[rel] = reason
            continue
        checked += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in PATTERNS:
            for m in pat.finditer(text):
                local = m.group(1).replace("\\#", "#")
                if local.startswith(NON_TERMS) or local in NEGATIVE_CONTROLS:
                    continue
                if HG + local not in declared:
                    undeclared.setdefault(rel, set()).add(local)

    print(f"Declared HeritageGraph terms in {TTL.name}: {len(declared)}")
    print(f"Files checked: {checked}")
    for term, why in NEGATIVE_CONTROLS.items():
        print(f"  exempt (negative control): hg:{term} -- {why}")
    for rel, why in sorted(skips.items()):
        print(f"  SKIPPED {rel} -- {why}")
    if undeclared:
        print("\nUNDECLARED HeritageGraph terms:")
        for rel, terms in sorted(undeclared.items()):
            print(f"  {rel}: {', '.join(sorted(terms))}")
        return 1
    print("\nPASS: every HeritageGraph term used is declared in the ontology.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
