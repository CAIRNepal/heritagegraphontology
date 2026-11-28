# HeritageGraph evaluation suite

These scripts evaluate the released ontology (`../ontology/HeritageGraph.ttl`, its SHACL shapes and
the optional modules) and the example data in `../examples/`. The paper's Evaluation section reports
their results. The authoritative way to run them is from the repository root:

```bash
make check       # the release gates (also run by CI on every pull request)
make reproduce   # regenerate everything, run the gates, and recompute every number in the paper
make coverage    # competency-question traceability matrix and mutation analysis (report only)
```

`make check` and `make reproduce` need Java and download ROBOT and the pinned external vocabularies
(CIDOC-CRM, CRMinf, CRMsci, PROV-O) on first use. The Python toolchain is pinned in
`../requirements-build.txt`. Reports are written to `results/`, which is not tracked.

## Release gates (`make check`)

| Script | What it checks |
|---|---|
| `artifact_lockstep.py` | The generated OWL, SHACL and JSON Schema agree with the LinkML source |
| `independent_abox.py` | SHACL conformance of the demonstrator and every negative test (each must fail on the component it targets) |
| `check_examples.py` | Every released example conforms to the shapes |
| `provo_consumer.py` | A client that knows only PROV-O can read the demonstrator's beliefs, also with the `prov` library |
| `run_abox_cq32.py` | The 32 competency questions against their frozen expected answers (`cq_expected.json`), over the asserted data and its OWL 2 RL closure |
| `check_declared_terms.py` | Every `hg:` term used in examples, queries and evaluation files is declared |
| `check_cq_class_properties.py` | Every class/property pattern in a competency query is declared in the shapes |
| `check_combined_dl.py` | The ontology alone and with each example is in OWL 2 DL and HermiT-consistent |
| `reasoning_extras.py` | Inconsistency injection, no HeritageGraph superclass on external terms, no Kumari tenure inferred to be an event, Linked Art module conservativity, CRM disjointness, and classification merged with the external vocabularies |
| `run_inference_cq.py` | The four inference questions, answered only under reasoning (`cq_inference_expected.json`) |
| `pattern_experiments.py` | The pattern experiments: tenure, custodianship, multiple calendars, and reuse outside Nepal (the ablation, `owl:sameAs`, and belief-supersession experiments run under `make reproduce`) |

## Metrics and reports (`make reproduce`)

| Script | Output |
|---|---|
| `run_metrics.py` | Structural metrics of the release |
| `run_alignment.py` | Counts of links to CIDOC-CRM and PROV-O |
| `mapping_audit.py` | Machine audit of every external mapping, with a negative control |
| `run_oops.py` | OOPS! pitfall scan; `--local` runs the local heuristic only |
| `shacl_census.py` | The SHACL constraint census (`shacl-census.tex`) |
| `cq_coverage.py` | Competency-question traceability and mutation analysis |

`../scripts/gen_paper_macros.py` writes the paper's numbers to `heritagegraph-numbers.tex`, and
`make reproduce` fails if that file, `shacl-census.tex` or the documentation's evaluation page is
stale.

## Other folders

- `lux/`: the Yale LUX case study. `generate_lux_eval.py --offline` recomputes class-type coverage
  from the committed instance-count snapshot. Its migration counts come from a pilot run with an
  earlier version of the Linked Art module and are not part of the paper's evaluation.
- `rater/`: the protocol and sheet for an independent rating of the mappings (see its README).
- `expert_cq/`: the protocol for held-out competency questions from external experts (see its README).
- `setup_protege.sh` and `protege/`: an optional local Protégé installation for inspecting the
  ontology with HermiT.

## Running a single script

From the repository root, with the pinned toolchain installed:

```bash
python3 evaluation/run_abox_cq32.py
python3 evaluation/pattern_experiments.py tenure
ROBOT_JAR=.tools/robot-1.9.8.jar python3 evaluation/check_combined_dl.py
```

`make -C evaluation help` lists the convenience targets of `evaluation/Makefile`.
