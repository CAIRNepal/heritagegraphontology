# HeritageGraph — top-level build targets.
# The ontology lives in ontology/ ; generated docs live in docs/ (never hand-edit).

.PHONY: help docs preview serve artefacts check robot conneg clean

help:                ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

docs:                ## regenerate the OntoReview documentation (terms, graph, quality report) into docs/
	scripts/build.sh

preview:             ## same, but into /tmp/hg-preview (leaves docs/ untouched)
	scripts/build.sh /tmp/hg-preview

serve: docs          ## regenerate, then serve the documentation at :8000
	@echo "open http://localhost:8000/" && cd docs && python3 -m http.server 8000

ROBOT_VERSION ?= 1.9.8
ROBOT_JAR     ?= .tools/robot-$(ROBOT_VERSION).jar

artefacts:           ## regenerate OWL/SHACL/JSON Schema (+ JSON-LD context, CQ TBox doc) from ontology/HeritageGraph.yaml
	python3 scripts/finalize_alpha5_artifacts.py
	python3 scripts/gen_jsonld_context.py
	python3 scripts/gen_cq_tbox_doc.py
	python3 scripts/gen_sssom.py

robot: $(ROBOT_JAR)  ## download ROBOT $(ROBOT_VERSION) (needs Java) for `make check`

$(ROBOT_JAR):
	mkdir -p $(dir $@)
	curl -fsSL -o $@ https://github.com/ontodev/robot/releases/download/v$(ROBOT_VERSION)/robot.jar

check: $(ROBOT_JAR)  ## release gates: generator unit tests, YAML/TTL sync, artefact lockstep, SHACL conformance and negative tests, the 32 CQs, declared terms, CQ class-property patterns declared, ontology+each example DL/HermiT, no HG superclass on external terms, KumariTenure not an E5_Event, LUX module conservative, core + CRM give no E2/E77 clash, every example ABox consistent with HG + CRM + CRMinf + CRMsci + PROV-O, merged-vocabulary classification (with and without the CRM-PROV bridge), inference CQs answered only under reasoning, multi-calendar resolution and conversion check
	python3 -m pytest -q tests/
	python3 scripts/check_yaml_ttl_sync.py
	python3 evaluation/artifact_lockstep.py
	python3 evaluation/independent_abox.py
	python3 evaluation/check_examples.py
	python3 evaluation/provo_consumer.py
	python3 evaluation/run_abox_cq32.py
	python3 scripts/gen_cq_tbox_doc.py --check
	python3 scripts/gen_sssom.py --check
	python3 evaluation/check_declared_terms.py
	python3 evaluation/check_cq_class_properties.py
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/check_combined_dl.py
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/reasoning_extras.py injection
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/reasoning_extras.py no-external-superclass
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/reasoning_extras.py tenure-not-event
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/reasoning_extras.py lux-conservativity
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/reasoning_extras.py core-crm-disjointness
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/reasoning_extras.py merged-abox
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/reasoning_extras.py merged-import
	python3 evaluation/run_inference_cq.py
	python3 evaluation/pattern_experiments.py multicalendar
	python3 evaluation/pattern_experiments.py reuse
	python3 evaluation/pattern_experiments.py tenure
	python3 evaluation/pattern_experiments.py custodianship

reproduce: $(ROBOT_JAR)  ## (first run fetches CIDOC-CRM, CRMinf, CRMsci, PROV-O and ROBOT) everything the paper reports: regenerate, compare with the committed artefacts, all release gates, mutation analysis, metric reports
	$(MAKE) artefacts
	git checkout -- docs && git clean -fq docs  # docs/ (HTML, JSON-LD context, release copies) is rebuilt at release, not compared here; uncommitted edits under docs/ are discarded
	python3 scripts/check_regenerated.py
	$(MAKE) check
	$(MAKE) coverage
	python3 evaluation/run_metrics.py
	python3 evaluation/run_alignment.py
	python3 evaluation/mapping_audit.py
	python3 evaluation/run_abox_cq32.py --entailment
	python3 evaluation/mapping_audit.py negative-control
	python3 evaluation/pattern_experiments.py ablation
	python3 evaluation/pattern_experiments.py sameas
	python3 evaluation/pattern_experiments.py supersession
	python3 evaluation/run_oops.py --local
	python3 scripts/gen_paper_macros.py

coverage:            ## CQ traceability matrix and mutation analysis (report, ~2 min)
	python3 evaluation/cq_coverage.py

BASE ?= https://cair-nepal.org/heritagegraph/
conneg:              ## check content negotiation of the deployed IRIs (BASE=<url> for staging)
	python3 deploy/nginx/check_conneg.py $(BASE)

clean:               ## remove build artefacts
	rm -f ontology/HeritageGraph.merged.ttl ontology/HeritageGraph.build.ttl
