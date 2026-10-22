# HermiT DL consistency check

Automated OWL-RL reports 0 unsatisfiable classes. For OWL 2 DL classification:

```bash
python3 evaluation/run_hermit.py   # requires Java 17+; runs in CI on push
```

Log archive: `release/evaluation/hermit_consistency_log.txt`

## Manual Protégé check (optional, with imports)

1. Open Protégé 5.6.x
2. Load `HeritageGraph.ttl`
3. Enable imports: **File → Preferences → Imports → Allow imports**
4. Ensure remote imports resolve (CRM, CRMinf, PROV, EDM, GeoSPARQL, OWL-Time)
5. **Reasoner → HermiT → Start reasoner**
6. **Reasoner → Explain unsatisfiable classes** (expect: none)
7. Save screenshot or log to `release/evaluation/hermit_consistency_log.txt`

Archive the log with your release tag.
