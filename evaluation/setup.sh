#!/usr/bin/env bash
# ==============================================================================
# HeritageGraph Ontology — Evaluation Environment Setup
# ==============================================================================
# Usage:  chmod +x setup.sh && ./setup.sh
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"
RESULTS_DIR="${SCRIPT_DIR}/results"
PROTEGE_DIR="${SCRIPT_DIR}/protege"

echo "=============================================="
echo " HeritageGraph Evaluation Setup"
echo "=============================================="

# --- 1. Create Python virtual environment ---
if [ ! -d "$VENV_DIR" ]; then
    echo "[1/4] Creating Python virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "[1/4] Virtual environment already exists."
fi

source "${VENV_DIR}/bin/activate"

# --- 2. Install Python dependencies ---
echo "[2/4] Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r "${SCRIPT_DIR}/requirements.txt" -q
echo "       Installed: rdflib, owlrl, requests, tabulate, pandas"

# --- 3. Ensure output directories ---
echo "[3/4] Creating output directories..."
mkdir -p "${RESULTS_DIR}"
mkdir -p "${PROTEGE_DIR}"
mkdir -p "${SCRIPT_DIR}/queries"

# --- 4. Verify ontology file ---
ONTOLOGY_FILE="${SCRIPT_DIR}/../HeritageGraph.ttl"
if [ -f "$ONTOLOGY_FILE" ]; then
    echo "[4/4] Ontology file found: HeritageGraph.ttl"
    LINES=$(wc -l < "$ONTOLOGY_FILE")
    echo "       Lines: ${LINES}"
else
    echo "[4/4] WARNING: HeritageGraph.ttl not found at ${ONTOLOGY_FILE}"
    echo "       Make sure the ontology is generated from HeritageGraph.yaml"
fi

echo ""
echo "=============================================="
echo " Setup Complete!"
echo "=============================================="
echo ""
echo " To activate the environment:"
echo "   source ${VENV_DIR}/bin/activate"
echo ""
echo " To run all evaluations:"
echo "   make all"
echo " Or individually:"
echo "   python run_consistency.py"
echo "   python run_abox_cq32.py"
echo "   python run_alignment.py"
echo "   python run_metrics.py"
echo "   python run_oops.py"
echo "=============================================="
