# HeritageGraph Ontology — Evaluation Suite

Reproducible evaluation of the HeritageGraph ontology, backing the evaluation
section (§7.1–§7.8) of the TGDK paper submission. Every script targets the
released ontology `../ontology/HeritageGraph.ttl` and the demonstrator
`../examples/kathmandu-mini-abox.ttl`; authoritative figures are reported in the
paper and regenerated into `results/`.

## Directory Structure

```
evaluation/
├── README.md                        ← You are here
├── Makefile                         ← One-command reproducibility
├── requirements.txt                 ← Python dependencies
├── setup.sh                         ← Environment setup script
│
│   Core dimensions
├── run_consistency.py               ← §7.1  OWL-RL closure & parse check
├── run_hermit.py                    ← §7.1  OWL 2 DL consistency (HermiT/ROBOT)
├── merged_import_classification.py  ← §7.1  Merged-vocabulary classification
├── inconsistency_injection.py       ← §7.1  Deliberate-inconsistency probes
├── run_oops.py                      ← §7.2  OOPS! pitfall analysis
├── run_abox_cq32.py                 ← §7.3  32 competency questions over the ABox
├── cq_entailment.py                 ← §7.3  CQ answers under OWL-RL entailment
├── run_metrics.py                   ← §7.3  Structural metrics
├── run_alignment.py                 ← §7.6  Alignment counts
├── run_mapping_audit.py             ← §7.6  External mapping audit
├── mapping_audit_negative_control.py← §7.6  Mapping negative control
├── shacl_census.py                  ← §7.4  SHACL constraint-component census
├── supersession_chain.py            ← §7.5  Provenance supersession chain
├── provo_consumer.py                ← §7.5  PROV-O generic-consumer interop
│
│   Pattern ablations (§7.3)
├── ablation_event_vs_static.py      ← Event-mediation vs static attachment
├── tenure_vs_actor_role.py          ← Tenure node vs plain actor-role
├── sameas_vs_reified.py             ← owl:sameAs vs reified syncretism
├── custodianship_depth.py           ← Institutional custodianship depth
├── multicalendar_resolution.py      ← Multi-calendar date resolution
├── artifact_lockstep.py             ← LinkML↔generated-artifact lockstep
│
│   Independent cross-checks
├── independent_eval.py              ← Independent, from-scratch re-evaluation
├── independent_abox.py              ← Independent ABox SHACL conformance + negatives
├── run_tgdk_eval.py                 ← Aggregate TGDK evaluation driver
│
├── setup_protege.sh                 ← §7.1  Protégé download & configuration
├── protege/                         ← Protégé install target
├── lux/                             ← §7.7  Yale LUX interoperability case study
└── results/                         ← All generated reports land here (git-ignored)
```

## Quick Start

### 1. Setup

```bash
cd evaluation/

# Option A: Full automated setup
chmod +x setup.sh
./setup.sh

# Option B: Using Make
make setup
```

### 2. Run All Evaluations

```bash
make all
```

This runs §4.1 through §4.6 in sequence and writes reports to `results/`.

### 3. Run Individual Evaluations

```bash
make consistency    # §4.1  OWL-RL reasoning + parse check
make oops           # §4.2  OOPS! pitfall scan (online + local)
make cq             # §4.3  Competency-question ASK validation
make alignment      # §4.4  CIDOC-CRM / PROV-O alignment count
make metrics        # §4.5 + §4.6  Completeness & metrics
```

### 4. Protégé (Manual DL Reasoning — §4.1)

```bash
make protege        # Downloads Protégé 5.6.4
./protege/launch_protege.sh   # Opens Protégé
```

Then follow `protege/PROTEGE_EVALUATION_CHECKLIST.md`.

---

## Evaluation Dimensions

### §4.1 — Logical Consistency and Reasoning

| Tool | What it checks | Script |
|------|---------------|--------|
| **OWL-RL (Python)** | RDF parse, deductive closure, inferred triple count | `run_consistency.py` |
| **Protégé + HermiT** | Full OWL DL consistency, unsatisfiable classes | `setup_protege.sh` |

**Automated output:**
- `results/consistency_report.txt` — Parse status, OWL-RL inferred triple count, unsatisfiable class heuristic
- `results/consistency_report.csv` — Machine-readable metrics

**Manual step (Protégé):**
1. Load `HeritageGraph.ttl` in Protégé 5.6.4
2. Reasoner → HermiT → Start Reasoner
3. Check for red-highlighted unsatisfiable classes
4. Record results in `protege/PROTEGE_EVALUATION_CHECKLIST.md`

### §4.2 — Modeling Quality (Pitfall Analysis)

| Tool | What it checks | Script |
|------|---------------|--------|
| **OOPS! (online)** | Submits to https://oops.linkeddata.es/ REST API | `run_oops.py` |
| **Local heuristic** | P08, P10, P11, P13, P22, P41 pitfalls | `run_oops.py` |

**Output:**
- `results/oops_report.txt` — Combined online + local pitfall summary
- `results/oops_response.xml` — Raw OOPS! XML (if service available)

**Pitfalls checked locally:**

| ID | Name | Severity |
|----|------|----------|
| P08 | Missing annotations (label/definition) | Minor |
| P10 | Missing disjointness between siblings | Important |
| P11 | Missing domain or range on properties | Important |
| P13 | Missing inverse relationship declarations | Minor |
| P22 | Using non-HTTP URIs | Critical |
| P41 | No license declared | Minor |

### §4.3 — Competency-Question Validation

| Tool | What it checks | Script |
|------|---------------|--------|
| **rdflib SPARQL 1.1** | 32 instance-level SELECT queries over the demonstrator ABox (`../examples/queries/cq-abox-32.rq`) | `run_abox_cq32.py` |
| **rdflib + OWL-RL** | how CQ answer sets change under deductive closure | `cq_entailment.py` |

**Output:**
- `results/abox_cq32_report.txt` / `.csv` — rows returned per CQ (a CQ passes when it returns ≥1 binding)

**CQ Dimensions:**
- **Structural** (CQ1–CQ6): Architecture, typology, location
- **Ritual/Festival** (CQ7–CQ18): Rituals, festivals, sequences, materials
- **Institutional/Syncretic** (CQ19–CQ25): Guthi, syncretism, multi-tradition
- **Living Goddess** (CQ26–CQ32): Kumari tenure, selection, retirement

### §4.4 — Alignment and Interoperability

| Tool | What it checks | Script |
|------|---------------|--------|
| **rdflib analysis** | CRM/PROV-O class & property URI alignment counts | `run_alignment.py` |

**Output:**
- `results/alignment_report.txt` — Detailed alignment listing
- `results/alignment_report.csv` — Per-element alignment records

**Checked vocabularies:**
CIDOC-CRM, CRMsci, CRMinf, PROV-O, schema.org, AAT, Wikidata, DBpedia, RICO, GeoSPARQL, OWL-Time, DataCite, DCTerms, FOAF

### §4.5 — Structural Completeness

Computed by `run_metrics.py`:
- `rdfs:label` coverage for all classes
- `skos:definition` / `rdfs:comment` coverage
- `rdfs:range` coverage for object and datatype properties
- `rdfs:domain` coverage

### §4.6 — Ontology Metrics

Computed by `run_metrics.py`:
- Class count (HeritageGraph namespace vs external)
- Object property count
- Datatype property count
- Union class count
- Named individual count
- Hierarchy depth
- Comparison against paper claims (70 classes, 123 obj props, 47 datatype props, 64 individuals, etc.)

---

## Prerequisites

- **Python 3.10+** with `venv` support
- **Java 11+** (for Protégé)
- **wget** or **curl** (for Protégé download)
- Internet connection (for OOPS! online scan; local fallback available)

## Cleaning Up

```bash
make clean       # Remove results only
make cleanall    # Remove results + venv + Protégé
```

## Reproducing Paper Results

To fully reproduce the evaluation reported in the paper:

```bash
# 1. Setup everything
make setup
make protege

# 2. Run all automated evaluations
make all

# 3. Manual step: Protégé + HermiT
./protege/launch_protege.sh
# Follow protege/PROTEGE_EVALUATION_CHECKLIST.md

# 4. Check results
ls -la results/
cat results/metrics_report.txt
cat results/abox_cq32_report.txt
cat results/alignment_report.txt
cat results/consistency_report.txt
cat results/oops_report.txt
```

## Ontology File

The evaluation targets `../ontology/HeritageGraph.ttl`, generated from
`../ontology/HeritageGraph.yaml` by `../scripts/finalize_alpha5_artifacts.py`
(which repairs the known gen-owl omissions and guards axiom survival).

The alignment script (`run_alignment.py`) also reads the YAML directly to extract
`slot_uri` / `class_uri` mappings.

If the TTL is out of date, regenerate it:
```bash
python3 scripts/finalize_alpha5_artifacts.py
```

---

## Expected Results Summary

When run against the released ontology (`../ontology/HeritageGraph.ttl`,
v0.1.0-alpha.7), the suite reproduces the figures reported in §7 of the paper.
The paper is the authoritative source; the numbers below are a quick reference.

### §7.1 Consistency
- **5,095** base triples; **26,414** after OWL-RL closure (**21,319** inferred)
- **0** unsatisfiable classes under HermiT (standalone and merged with CRM/CRMinf/PROV-O)
- **1** `owl:disjointWith` axiom (`Stupa`⊓`Chaitya`); separation is otherwise enforced by SHACL

### §7.2 OOPS! Pitfalls
- No critical pitfall; only the deliberate, documented design decisions are reported
  (see `run_oops.py` and the paper §7.2).

### §7.3 Competency Questions
- **32/32** CQs return ≥1 binding over the demonstrator ABox
- Dimensions: Structural 6/6, Ritual/Festival 12/12, Institutional/Syncretic 7/7, Living Goddess 7/7
- Three pattern ablations (`ablation_event_vs_static.py`, `tenure_vs_actor_role.py`,
  `sameas_vs_reified.py`) show each pattern is load-bearing

### §7.4 Constraint Validation
- **75** `sh:NodeShape`s with **1,204** property shapes; released open (closedness relaxed)
- Demonstrator ABox conforms; 8 single-violation negative tests are all caught

### §7.6 Alignment
- **42** classes and **25** minted properties map to **12** external vocabularies via
  **116** mapping triples (48 `skos:broadMatch`, 23 `rdfs:subClassOf`, 23 `rdfs:subPropertyOf`,
  16 `skos:exactMatch`, 6 `skos:closeMatch`)
- Led by CIDOC-CRM (31 classes, 22 properties), PROV-O (28 classes), Getty AAT (6 classes)

### Metrics
| Metric | Value |
|--------|-------|
| Classes (named) | 84 (66 HG-minted + 18 reused) |
| Object properties | 149 |
| Datatype properties | 42 |
| SKOS concepts (enumerations) | 51 |
| SHACL NodeShapes | 75 |
| CQ pass rate (ABox) | 32/32 |

All reports are regenerated against `../ontology/HeritageGraph.ttl`; re-run with
`make all` (from this directory) to refresh `results/`.
