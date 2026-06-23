# HeritageGraph — top-level build targets.
# The ontology lives in ontology/ ; generated docs live in docs/ (never hand-edit).

.PHONY: help docs preview webvowl artefacts clean

help:                ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

docs:                ## regenerate the WIDOCO docs + WebVOWL for the core ontology into docs/
	scripts/build.sh

preview:             ## same, but into /tmp/hg-preview (leaves docs/ untouched)
	scripts/build.sh /tmp/hg-preview

webvowl: docs        ## regenerate, then serve the visualization at :8000
	@echo "open http://localhost:8000/webvowl/" && cd docs && python3 -m http.server 8000

artefacts:           ## regenerate RDF artefacts from the LinkML source (ontology/HeritageGraph.yaml)
	python3 scripts/regenerate_ontology_artifacts.py

clean:               ## remove build artefacts
	rm -f ontology/HeritageGraph.merged.ttl ontology/HeritageGraph.build.ttl
