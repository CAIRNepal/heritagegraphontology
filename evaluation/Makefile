# ==============================================================================
# HeritageGraph Ontology — Evaluation Makefile
# ==============================================================================
# Usage:
#   make setup       — Create venv, install deps
#   make all         — Run all automated evaluations
#   make consistency — §4.1 OWL-RL reasoning
#   make oops        — §4.2 Pitfall analysis
#   make cq          — §7.3 Competency-question execution over the ABox
#   make alignment   — §4.4 Interoperability
#   make metrics     — §4.5 + §4.6 Completeness & metrics
#   make protege     — Download & configure Protégé
#   make clean       — Remove results (keep venv)
#   make cleanall    — Remove results + venv + Protégé
# ==============================================================================

SHELL := /bin/bash
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
RESULTS := results

.PHONY: all setup consistency oops cq alignment metrics independent quality protege clean cleanall help

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

independent: setup ## Independent from-scratch re-evaluation + SHACL negative tests
	@echo "Running independent cross-check..."
	$(PYTHON) independent_eval.py
	$(PYTHON) independent_abox.py
	@echo ""

quality: all ## Run evaluations + copy to release/
	@echo "Building release quality report..."
	cd .. && $(CURDIR)/$(PYTHON) scripts/run_release_quality.py
	@echo ""

all: setup consistency oops cq alignment metrics ## Run ALL automated evaluations
	@echo ""
	@echo "=============================================="
	@echo " ✅ All evaluations complete!"
	@echo " Results in: $(RESULTS)/"
	@echo "=============================================="
	@ls -la $(RESULTS)/

consistency: setup ## §4.1 — Logical consistency & OWL-RL reasoning
	@echo "Running §4.1 — Consistency & Reasoning..."
	$(PYTHON) run_consistency.py
	@echo ""

oops: setup ## §4.2 — OOPS! pitfall analysis
	@echo "Running §4.2 — OOPS! Pitfall Analysis..."
	$(PYTHON) run_oops.py
	@echo ""

cq: setup ## §7.3 — Competency-question execution over the demonstrator ABox
	@echo "Running §7.3 — Competency-Question Execution..."
	$(PYTHON) run_abox_cq32.py
	@echo ""

alignment: setup ## §4.4 — Alignment & interoperability
	@echo "Running §4.4 — Alignment & Interoperability..."
	$(PYTHON) run_alignment.py
	@echo ""

metrics: setup ## §4.5 + §4.6 — Structural completeness & metrics
	@echo "Running §4.5/§4.6 — Metrics & Completeness..."
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
