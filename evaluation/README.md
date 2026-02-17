# HeritageGraph Ontology — Evaluation Suite

Reproducible evaluation of the HeritageGraph ontology across the seven dimensions described in the SWJ paper submission (§4.1–§4.7).

## Directory Structure

```
evaluation/
├── README.md                    ← You are here
├── Makefile                     ← One-command reproducibility
├── requirements.txt             ← Python dependencies
├── setup.sh                     ← Environment setup script
│
├── run_consistency.py           ← §4.1  Logical consistency & OWL-RL reasoning
├── run_oops.py                  ← §4.2  OOPS! pitfall analysis
├── run_cq_validation.py         ← §4.3 + §4.7  CQ validation & traceability
├── run_alignment.py             ← §4.4  Alignment & interoperability
├── run_metrics.py               ← §4.5 + §4.6  Structural completeness & metrics
│
├── setup_protege.sh             ← §4.1  Protégé download & configuration
├── protege/
│   ├── launch_protege.sh        ← One-click Protégé launcher
│   └── PROTEGE_EVALUATION_CHECKLIST.md
│
├── queries/                     ← (Optional) Individual .rq SPARQL files
│
└── results/                     ← All generated reports land here
    ├── consistency_report.txt
    ├── consistency_report.csv
    ├── oops_report.txt
    ├── oops_response.xml
    ├── cq_validation_report.txt
    ├── cq_traceability_matrix.csv
    ├── alignment_report.txt
    ├── alignment_report.csv
    ├── metrics_report.txt
    └── metrics_report.csv
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
| **rdflib SPARQL** | 32 TBox-only ASK queries against schema | `run_cq_validation.py` |

**Output:**
- `results/cq_validation_report.txt` — Pass/fail for each CQ
- `results/cq_traceability_matrix.csv` — Full CQ → ontology element mapping

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
- Comparison against paper claims (111 classes, 118 obj props, etc.)

### §4.7 — CQ Traceability

Generated by `run_cq_validation.py` as `results/cq_traceability_matrix.csv`:

| Column | Description |
|--------|-------------|
| `cq_id` | CQ identifier (CQ1–CQ32) |
| `dimension` | Thematic dimension |
| `question` | Full competency question text |
| `ontology_elements` | Classes and properties needed |
| `ask_result` | Boolean pass/fail |
| `time_ms` | Query execution time |

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
cat results/cq_validation_report.txt
cat results/alignment_report.txt
cat results/consistency_report.txt
cat results/oops_report.txt
```

## Ontology File

The evaluation targets `../HeritageGraph.ttl` (generated from `../HeritageGraph.yaml` via LinkML).

The alignment script (`run_alignment.py`) also reads `../HeritageGraph.yaml` directly to extract `slot_uri` / `class_uri` mappings that are not emitted as OWL triples in the generated TTL.

If the TTL is out of date, regenerate it:
```bash
pip install linkml
cd ..
gen-owl HeritageGraph.yaml -o HeritageGraph.ttl
```

---

## Expected Results Summary

When run against the current HeritageGraph ontology, the evaluation suite produces:

### §4.1 Consistency
- **4,312** base triples parsed
- **17,894** inferred triples via OWL-RL closure (22,206 total)
- **0** unsatisfiable classes detected

### §4.2 OOPS! Pitfalls
- **P08** (Minor): 6 classes missing annotations (enum parent classes)
- **P10** (Important): 17 sibling class pairs missing `owl:disjointWith`
- **P11** (Important): 147 missing domain/range declarations
- **P13** (Minor): 5 likely inverse pairs missing `owl:inverseOf`
- **P22** (Critical): 2 non-HTTP URIs (ontology IRI uses `file://` scheme)

### §4.3 Competency Questions
- **32/32** CQs pass (100%)
- All 4 dimensions: Structural 6/6, Ritual/Festival 12/12, Institutional/Syncretic 7/7, Living Goddess 7/7

### §4.4 Alignment
| Namespace | Classes | Properties |
|-----------|---------|------------|
| CIDOC-CRM | 42 | 71 ✅ |
| PROV-O | 3 | 11 ✅ |
| AAT | 25 | 0 |
| Wikidata | 6 | 0 |
| DBpedia | 3 | 0 |
| DataCite | 0 | 5 |
| Others | 5 | 3 |

### §4.5/§4.6 Metrics — Paper vs Actual
| Metric | Paper | Actual | Match |
|--------|-------|--------|-------|
| Classes (HG namespace) | 111 | 111 | ✅ |
| Object properties | 118 | 118 | ✅ |
| Datatype properties | 44 | 44 | ✅ |
| Union classes (named) | 2 | 2 | ✅ |
| Named individuals | 0 | 0 | ✅ |

### Known Notes
- **CRM class count** (42 vs paper's 35): The script finds 42 CRM-aligned classes because it also counts AAT concepts that have `rdfs:subClassOf crm:E55_Type`. The paper's 35 counts only direct `class_uri` mappings from the YAML.
- **P22 non-HTTP URI**: The ontology IRI resolves to a `file://` path (`CulturalHeritageOntology.owl.ttl`). This should be fixed before publication to use the canonical `https://w3id.org/heritagegraph/` URI.
- **Property alignment source**: Property alignments (71 CRM, 11 PROV-O) are extracted from `HeritageGraph.yaml` `slot_uri` values since LinkML does not emit these as OWL triples in the generated TTL.
