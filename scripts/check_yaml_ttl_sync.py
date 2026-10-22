#!/usr/bin/env python3
"""Verify ontology/HeritageGraph.ttl (+ .shacl.ttl) were generated from the
CURRENT ontology/HeritageGraph.yaml. Fails (exit 1) if the YAML changed after
the TTLs were generated — i.e., someone edited the YAML without regenerating,
or edited a TTL by hand. Run scripts/finalize_alpha5_artifacts.py to re-sync."""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "ontology" / "HeritageGraph.yaml"
digest = hashlib.sha256(SCHEMA.read_bytes()).hexdigest()
ok = True
for name in ("HeritageGraph.ttl", "HeritageGraph.shacl.ttl"):
    f = ROOT / "ontology" / name
    head = f.read_text(encoding="utf-8")[:400]
    m = re.search(r"source-sha256: ([0-9a-f]{64})", head)
    if not m:
        print(f"FAIL {name}: no source-sha256 stamp (regenerate)")
        ok = False
    elif m.group(1) != digest:
        print(f"FAIL {name}: generated from a DIFFERENT YAML "
              f"(stamp {m.group(1)[:12]}..., current YAML {digest[:12]}...)")
        ok = False
    else:
        print(f"OK   {name}: in sync with {SCHEMA.name} ({digest[:12]}...)")
sys.exit(0 if ok else 1)
