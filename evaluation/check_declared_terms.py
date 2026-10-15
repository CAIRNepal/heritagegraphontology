#!/usr/bin/env python3
"""Every HeritageGraph term used by the examples, queries, and evaluation code
must be declared in the released ontology.

Scans examples/ (ABoxes and examples/queries/), evaluation/ (scripts, fixtures,
expected answers), and the generated cq_sparql.md for HeritageGraph IRIs, in any
of the spellings the repository uses: CURIEs (hg:x, heritageGraph:x), full IRIs
(<http://cair-nepal.org/heritagegraph/x>, including enumeration individuals such as
.../ConditionType#Damaged), and the Python constructions HG + "x" and U("x").
Each term must be the subject of an rdf:type triple in
ontology/HeritageGraph.ttl. A stale term (e.g. a snake_case name from an older
schema lineage, or hg:Person instead of crm:E21_Person) fails the check.

Instance IRIs (demo/, example/ namespaces) and the ontology's own document IRIs
are not terms and are ignored. Two exemptions are explicit and printed:
  * NEGATIVE_CONTROLS: terms that are undeclared on purpose (a test that must
    see a missing predicate);
  * SKIPPED: files out of scope (none at present).

The LUX bridge module (ontology/lux/) mints its own interoperability terms;
files that belong to it (LUX_SCOPED) may use those terms as well as the core's.
Every other file may use core terms only.

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
HG = "http://cair-nepal.org/heritagegraph/"

SCAN = [ROOT / "examples", ROOT / "evaluation", ROOT / "ontology" / "lux",
        ROOT / "cq_sparql.md"]
LUX_MODULE_FILES = sorted((ROOT / "ontology" / "lux").glob("*.ttl"))
LUX_SCOPED = ("ontology/lux", "evaluation/lux", "examples/lux-")
SUFFIXES = {".ttl", ".rq", ".py", ".json", ".md", ".csv"}
IGNORED_DIRS = {".venv", "venv", "results", "__pycache__", "protege"}

# Instance / document namespaces under the HeritageGraph base that are not terms.
NON_TERMS = ("demo/", "example/", "ontology", "schema", "scheme/", "dataset", "imported/",
             "alignment", "edm-profile")

# Pre-1.0.0 types that external data (the LUX endpoint's migrated graph) still
# carries; only the script that maps them onto v1.0.0 classes may name them.
LEGACY_DATA_TYPES = {
    "evaluation/lux/generate_lux_eval.py": {"Person", "Place", "HumanMadeObject"},
}

NEGATIVE_CONTROLS = {
    "doesNotExistPattern": "run_abox_cq32.py self-test: a predicate no triple uses",
}
SKIPPED: dict[str, str] = {}

PATTERNS = [
    re.compile(r"\b(?:hg|heritageGraph):([A-Za-z_][\w\-]*(?:\\?#\w+)?)"),
    re.compile(r"cair-nepal\.org/heritagegraph/([A-Za-z_][\w\-/]*(?:#\w+)?)"),
    re.compile(r"\bHG\s*\+\s*[\"']([A-Za-z_][\w\-]*)[\"']"),
    re.compile(r"\bU\(\s*[\"']([A-Za-z_][\w\-]*)[\"']\s*\)"),
]


def declared_terms(*paths: Path) -> set[str]:
    g = Graph()
    for path in paths:
        g.parse(path, format="turtle")
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
    declared = declared_terms(TTL)
    lux_declared = declared | declared_terms(*LUX_MODULE_FILES)
    undeclared: dict[str, set[str]] = {}
    checked, skips = 0, {}
    for path in files():
        rel = path.relative_to(ROOT).as_posix()
        reason = skipped(rel)
        if reason:
            skips[rel] = reason
            continue
        checked += 1
        allowed = lux_declared if rel.startswith(LUX_SCOPED) else declared
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pat in PATTERNS:
            for m in pat.finditer(text):
                local = m.group(1).replace("\\#", "#")
                if local.startswith(NON_TERMS) or local in NEGATIVE_CONTROLS:
                    continue
                if local in LEGACY_DATA_TYPES.get(rel, ()):
                    continue
                if HG + local not in allowed:
                    undeclared.setdefault(rel, set()).add(local)

    print(f"Declared HeritageGraph terms in {TTL.name}: {len(declared)}; "
          f"+ LUX module/shapes: {len(lux_declared) - len(declared)}")
    print(f"Files checked: {checked}")
    for term, why in NEGATIVE_CONTROLS.items():
        print(f"  exempt (negative control): hg:{term} -- {why}")
    for rel, terms in LEGACY_DATA_TYPES.items():
        print(f"  exempt (maps legacy data types to v1.0.0): {rel}: {', '.join(sorted(terms))}")
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
