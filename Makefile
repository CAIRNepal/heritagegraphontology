# HeritageGraph — top-level build targets.
# The ontology lives in ontology/ ; generated docs live in docs/ (never hand-edit).

.PHONY: help docs preview webvowl artefacts check robot conneg clean

help:                ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

docs:                ## regenerate the WIDOCO docs + WebVOWL for the core ontology into docs/
	scripts/build.sh

preview:             ## same, but into /tmp/hg-preview (leaves docs/ untouched)
	scripts/build.sh /tmp/hg-preview

webvowl: docs        ## regenerate, then serve the visualization at :8000
	@echo "open http://localhost:8000/webvowl/" && cd docs && python3 -m http.server 8000

ROBOT_VERSION ?= 1.9.8
ROBOT_JAR     ?= .tools/robot-$(ROBOT_VERSION).jar

artefacts:           ## regenerate OWL/SHACL/JSON Schema (+ JSON-LD context, CQ TBox doc) from ontology/HeritageGraph.yaml
	python3 scripts/finalize_alpha5_artifacts.py
	python3 scripts/gen_jsonld_context.py
	python3 scripts/gen_cq_tbox_doc.py

robot: $(ROBOT_JAR)  ## download ROBOT $(ROBOT_VERSION) (needs Java) for `make check`

$(ROBOT_JAR):
	mkdir -p $(dir $@)
	curl -fsSL -o $@ https://github.com/ontodev/robot/releases/download/v$(ROBOT_VERSION)/robot.jar

check: $(ROBOT_JAR)  ## release gates: YAML/TTL sync, declared terms, CQ class-property patterns declared, ontology+each example DL/HermiT, no HG superclass on external terms, KumariTenure not an E5_Event
	python3 scripts/check_yaml_ttl_sync.py
	python3 evaluation/check_declared_terms.py
	python3 evaluation/check_cq_class_properties.py
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/check_combined_dl.py
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/reasoning_extras.py no-external-superclass
	ROBOT_JAR=$(abspath $(ROBOT_JAR)) python3 evaluation/reasoning_extras.py tenure-not-event

BASE ?= https://cair-nepal.org/heritagegraph/
conneg:              ## check content negotiation of the deployed IRIs (BASE=<url> for staging)
	python3 deploy/nginx/check_conneg.py $(BASE)

clean:               ## remove build artefacts
	rm -f ontology/HeritageGraph.merged.ttl ontology/HeritageGraph.build.ttl
