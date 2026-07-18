# evaluation-independent/

Independent, reviewer-style evaluation of `ontology/HeritageGraph.ttl`, produced 2026-07-16 without reading or reusing anything in `evaluation/`.

- **`POSTFIX.md`** — audit of the DL-compliance fixes applied after the evaluation (what changed, proof of no degradation, before→after scorecard); post-fix raw evidence in `raw-postfix/`. `REPORT.md` describes the **pre-fix** artifact (SHA `ae26535c…`); the post-fix artifact is SHA `f443622c…`.
- **`REPORT.md`** — the evaluation report. Measured facts and reviewer opinion are separated and labeled; every number cites the raw file and command that produced it.
- **`raw/`** — unedited tool outputs (ROBOT measure/validate-profile/reason/report, HermiT/JFact/Pellet logs, OOPS! REST responses, pySHACL output, curl transcripts, grep counts). Appendix A of the report indexes them.
- **`scripts/`** — the Python scripts used for measurements; each has a run command in its docstring. Java-based steps used ROBOT 1.9.8 and Temurin JREs downloaded into a session scratchpad (not committed; commands recorded in the report §1).

To re-verify any claim: find it in `REPORT.md`, follow the citation to `raw/`, and re-run the command listed in Appendix A against the file with SHA-256 `ae26535c20f0bffea6b2acadaf39d8f5cdcc7fa5a8f45b4447ec331deab61721`.
