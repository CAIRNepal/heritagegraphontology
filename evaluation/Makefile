# ==============================================================================
# HeritageGraph Ontology — Evaluation Makefile
# ==============================================================================
# Usage:
#   make setup       — Create venv, install deps
#   make all         — Run all release gates (the root `make reproduce`)
#   make oops        — OOPS! pitfall scan (needs its web service or local image)
#   make cq          — Competency-question execution over the demonstrator
#   make alignment   — Alignment counts
#   make metrics     — Structural metrics
#   make terms       — Every hg: term used is declared in the ontology
#   make combined    — Ontology + each example in OWL 2 DL and HermiT-consistent
#   make independent — SHACL conformance of the demonstrator + negative tests
#   make protege     — Download & configure Protégé
#   make clean       — Remove results (keep venv)
#   make cleanall    — Remove results + venv + Protégé
# ==============================================================================

SHELL := /bin/bash
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
RESULTS := results

.PHONY: all setup oops cq alignment metrics terms combined independent protege clean cleanall help

help: ## Show this help
	@echo ""
	@echo "HeritageGraph Ontology Evaluation"
	@echo "================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-15s %s\n", $$1, $$2}'
	@echo ""

setup: $(VENV)/bin/activate ## Create venv and install dependencies

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip -q
	$(PIP) install -r requirements.txt -q
	touch $(VENV)/bin/activate
	@echo "✅ Virtual environment ready. Run: source $(VENV)/bin/activate"

independent: setup ## SHACL conformance of the demonstrator + negative tests
	@echo "Running independent cross-check..."
	$(PYTHON) independent_abox.py
	@echo ""

all: ## Run ALL automated evaluations: the root `make reproduce` (one source of truth for the gates)
	$(MAKE) -C .. reproduce

oops: setup ## OOPS! pitfall analysis
	@echo "Running OOPS! Pitfall Analysis..."
	$(PYTHON) run_oops.py
	@echo ""

cq: setup ## Competency-question execution over the demonstrator ABox
	@echo "Running Competency-Question Execution..."
	$(PYTHON) run_abox_cq32.py
	@echo ""

terms: setup ## Every hg: term in examples/queries/evaluation is declared in the ontology
	@echo "Checking HeritageGraph term declarations..."
	$(PYTHON) check_declared_terms.py
	@echo ""

combined: setup ## Ontology + each example ABox in OWL 2 DL and HermiT-consistent (needs Java + ROBOT_JAR)
	@echo "Checking ontology + example ABoxes (single graph) with ROBOT..."
	$(PYTHON) check_combined_dl.py
	@echo ""

alignment: setup ## Alignment & interoperability
	@echo "Running Alignment & Interoperability..."
	$(PYTHON) run_alignment.py
	@echo ""

metrics: setup ## Structural completeness & metrics
	@echo "Running Metrics & Completeness..."
	$(PYTHON) run_metrics.py
	@echo ""

protege: ## Download and configure Protégé 5.6.4
	@echo "Setting up Protégé..."
	chmod +x setup_protege.sh
	./setup_protege.sh

clean: ## Remove results (keep venv)
	rm -rf $(RESULTS)/*.txt $(RESULTS)/*.csv $(RESULTS)/*.xml
	@echo "✅ Results cleaned."

cleanall: clean ## Remove results + venv + Protégé
	rm -rf $(VENV) protege/Protege-* protege/*.tar.gz
	@echo "✅ Full clean done."
