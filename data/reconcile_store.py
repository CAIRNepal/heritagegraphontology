#!/usr/bin/env python3
"""Reconcile the initial DANAM pipeline vocabulary to the current released
HeritageGraph ontology.

Reads the N-Quads export of the Fuseki/TDB2 `heritagegraph` store
(data/reconciled/store_export.nq) and rewrites every ontology term from the
initial pipeline namespace (https://cair-nepal.org/heritagegraph/, snake_case)
to the current released ontology (https://w3id.org/heritagegraph/, camelCase),
using data/reconcile_crosswalk.json. Specifically it:

  * drops the old cair-nepal ontology T-Box graph (we use the real ontology);
  * drops predicates removed from the current ontology (epistemic_stance);
  * rewrites class and property IRIs per the crosswalk (incl. two CRM targets
    for the syncretic-assignment predicates);
  * converts remaining cair-nepal enumeration-value IRIs (e.g. .../NityaPuja)
    to string literals ("NityaPuja"), matching how the released ontology's
    demonstrator and the competency-question queries represent enum slots.

Instance IRIs (https://data.cair-nepal.org/...) are a data namespace, not
ontology terms, and are left unchanged. Output is written as N-Quads to
data/reconciled/danam-heritagegraph.nq (named graphs preserved). The input
store is never modified."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CROSSWALK = ROOT / "reconcile_crosswalk.json"
SRC = ROOT / "reconciled" / "store_export.nq"
OUT = ROOT / "reconciled" / "danam-heritagegraph.nq"

OLD_NS = "https://cair-nepal.org/heritagegraph/"
VOCAB_IRI = re.compile(r"<https://cair-nepal\.org/heritagegraph/([^>]+)>")


def build_iri_map(cw: dict) -> dict[str, str]:
    m: dict[str, str] = {}
    for local, target in cw["class_map"].items():
        m[f"<{OLD_NS}{local}>"] = f"<{target}>"
    for local, target in cw["predicate_map"].items():
        m[f"<{OLD_NS}{local}>"] = f"<{target}>"
    return m


def escape_literal(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main() -> int:
    cw = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    iri_map = build_iri_map(cw)
    drop_preds = {f"<{p}>" for p in cw["drop_predicates"]}
    exclude_graph_suffixes = tuple(f"<{g}> ." for g in cw["exclude_graphs"])

    mapped_locals = set(cw["class_map"]) | set(cw["predicate_map"])
    dropped_locals = {p.rsplit("/", 1)[-1] for p in cw["drop_predicates"]}

    stats = {
        "in": 0, "kept": 0, "dropped_graph": 0, "dropped_pred": 0,
        "enum_literalised": 0, "iri_rewrites": 0,
    }

    with SRC.open(encoding="utf-8") as fin, OUT.open("w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip() or line.startswith("#"):
                continue
            stats["in"] += 1

            # 1. drop the old ontology T-Box graph
            if line.rstrip().endswith(exclude_graph_suffixes):
                stats["dropped_graph"] += 1
                continue
            # 2. drop predicates removed from the current ontology
            if any(f" {p} " in line for p in drop_preds):
                stats["dropped_pred"] += 1
                continue

            # 3. rewrite mapped class/property IRIs (exact <iri> tokens)
            def repl_vocab(mobj: re.Match) -> str:
                token = mobj.group(0)
                local = mobj.group(1)
                if token in iri_map:
                    stats["iri_rewrites"] += 1
                    return iri_map[token]
                if local in mapped_locals or local in dropped_locals:
                    return token  # shouldn't reach here
                # 4. otherwise it's an enum-value individual -> string literal
                stats["enum_literalised"] += 1
                return f'"{escape_literal(local)}"'

            new_line = VOCAB_IRI.sub(repl_vocab, line)
            fout.write(new_line)
            stats["kept"] += 1

    print("Reconciliation complete:")
    for k in ["in", "kept", "dropped_graph", "dropped_pred", "iri_rewrites", "enum_literalised"]:
        print(f"  {k:16} {stats[k]}")
    print(f"\nOutput: {OUT.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
