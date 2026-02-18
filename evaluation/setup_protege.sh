#!/usr/bin/env bash
# ==============================================================================
# Protégé 5.6.4 — Automated Download & Setup for HeritageGraph Evaluation
# ==============================================================================
# This script downloads Protégé Desktop 5.6.4 (platform-independent) and
# configures it for reproducible ontology evaluation with HermiT reasoner.
#
# Usage:  chmod +x setup_protege.sh && ./setup_protege.sh
#
# After running:
#   ./protege/Protege-5.6.4/run.sh           (Linux)
#   ./protege/Protege-5.6.4/run.bat           (Windows)
#   ./protege/Protege-5.6.4/Protege.app       (macOS)
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROTEGE_DIR="${SCRIPT_DIR}/protege"
ONTOLOGY_FILE="${SCRIPT_DIR}/../HeritageGraph.ttl"

# Protégé 5.6.4 (latest stable as of 2025)
PROTEGE_VERSION="5.6.4"
PROTEGE_URL="https://github.com/protegeproject/protege-distribution/releases/download/protege-${PROTEGE_VERSION}/Protege-${PROTEGE_VERSION}-linux.tar.gz"
PROTEGE_ARCHIVE="${PROTEGE_DIR}/Protege-${PROTEGE_VERSION}-linux.tar.gz"
PROTEGE_INSTALL="${PROTEGE_DIR}/Protege-${PROTEGE_VERSION}"

echo "=============================================="
echo " Protégé ${PROTEGE_VERSION} Setup"
echo "=============================================="

mkdir -p "${PROTEGE_DIR}"

# --- 1. Download Protégé ---
if [ -d "${PROTEGE_INSTALL}" ]; then
    echo "[1/4] Protégé already installed at ${PROTEGE_INSTALL}"
else
    if [ ! -f "${PROTEGE_ARCHIVE}" ]; then
        echo "[1/4] Downloading Protégé ${PROTEGE_VERSION}..."
        echo "      URL: ${PROTEGE_URL}"

        # Try wget first, fall back to curl
        if command -v wget &> /dev/null; then
            wget -q --show-progress -O "${PROTEGE_ARCHIVE}" "${PROTEGE_URL}" || {
                echo ""
                echo "  ⚠️  Automatic download failed."
                echo "  Please download Protégé manually from:"
                echo "    https://protege.stanford.edu/products.php#desktop-protege"
                echo "  Or from GitHub releases:"
                echo "    https://github.com/protegeproject/protege-distribution/releases"
                echo ""
                echo "  Save the archive to: ${PROTEGE_ARCHIVE}"
                echo "  Then re-run this script."
                exit 1
            }
        elif command -v curl &> /dev/null; then
            curl -L -o "${PROTEGE_ARCHIVE}" "${PROTEGE_URL}" || {
                echo ""
                echo "  ⚠️  Automatic download failed."
                echo "  Please download Protégé manually (see above)."
                exit 1
            }
        else
            echo "  ❌  Neither wget nor curl found. Please install one and retry."
            exit 1
        fi
    else
        echo "[1/4] Archive already downloaded."
    fi

    # --- 2. Extract ---
    echo "[2/4] Extracting Protégé..."
    cd "${PROTEGE_DIR}"
    tar -xzf "${PROTEGE_ARCHIVE}"
    echo "      Extracted to: ${PROTEGE_INSTALL}"
fi

# --- 3. Create launcher script ---
echo "[3/4] Creating launcher script..."

cat > "${PROTEGE_DIR}/launch_protege.sh" << 'LAUNCHER'
#!/usr/bin/env bash
# Launch Protégé and open HeritageGraph.ttl
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PROTEGE_DIR=$(find "${SCRIPT_DIR}" -maxdepth 1 -name "Protege-*" -type d | head -1)
ONTOLOGY="${SCRIPT_DIR}/../HeritageGraph.ttl"

if [ -z "${PROTEGE_DIR}" ]; then
    echo "❌ Protégé installation not found in ${SCRIPT_DIR}"
    echo "   Run setup_protege.sh first."
    exit 1
fi

echo "=============================================="
echo " Launching Protégé"
echo "=============================================="
echo " Ontology: ${ONTOLOGY}"
echo ""
echo " After Protégé opens:"
echo "   1. File → Open → select HeritageGraph.ttl"
echo "      (or use the path above)"
echo "   2. Reasoner → HermiT"
echo "   3. Reasoner → Start Reasoner"
echo "   4. Check for red classes in the Class Hierarchy"
echo "   5. Window → Views → Class Views → Classification Results"
echo "=============================================="

cd "${PROTEGE_DIR}"

# Set memory for large ontologies
export PROTEGE_MAX_MEMORY=4G

if [ -f "${PROTEGE_DIR}/run.sh" ]; then
    chmod +x "${PROTEGE_DIR}/run.sh"
    "${PROTEGE_DIR}/run.sh" &
elif [ -f "${PROTEGE_DIR}/Protege" ]; then
    chmod +x "${PROTEGE_DIR}/Protege"
    "${PROTEGE_DIR}/Protege" &
else
    echo "❌ Cannot find Protégé executable in ${PROTEGE_DIR}"
    ls -la "${PROTEGE_DIR}"
    exit 1
fi

echo ""
echo "Protégé is starting in the background..."
echo "Load: ${ONTOLOGY}"
LAUNCHER

chmod +x "${PROTEGE_DIR}/launch_protege.sh"

# --- 4. Create evaluation checklist ---
echo "[4/4] Creating Protégé evaluation checklist..."

cat > "${PROTEGE_DIR}/PROTEGE_EVALUATION_CHECKLIST.md" << 'CHECKLIST'
# Protégé Evaluation Checklist for HeritageGraph Ontology

## Environment
- **Protégé version**: 5.6.4
- **Reasoner**: HermiT 1.4.3 (bundled)
- **Ontology file**: `../HeritageGraph.ttl`
- **Date evaluated**: _______________

## Step-by-Step Instructions

### 1. Load the Ontology
1. Launch Protégé: `./launch_protege.sh`
2. File → Open → navigate to `../HeritageGraph.ttl`
3. Verify it loads without errors in the log panel (bottom)

### 2. Run HermiT Reasoner
1. Go to **Reasoner → HermiT**
2. Click **Reasoner → Start Reasoner**
3. Wait for classification to complete

### 3. Check Consistency
- [ ] **Consistent?** (no "Inconsistent ontology" error)
- [ ] **Unsatisfiable classes?** (check for red/orange highlighting in class hierarchy)
  - If found, list them: _______________

### 4. Record Classification Results
- [ ] Open: Window → Views → Class Views → Classification Results
- [ ] **Inferred subclass relationships**: _____ new inferences
- [ ] **Inferred equivalent classes**: _____ 

### 5. Check for Warnings
- [ ] Open the Protégé log: Window → Show Log
- [ ] Note any warnings: _______________

### 6. Export Results
1. File → Save As → save classified version as `HeritageGraph_classified.owl`
2. Screenshot the class hierarchy
3. Copy log contents

## Results Summary

| Check | Result | Notes |
|-------|--------|-------|
| Parses without error | ☐ Yes / ☐ No | |
| HermiT: Consistent | ☐ Yes / ☐ No | |
| Unsatisfiable classes | ☐ None / ☐ Found | Count: ___ |
| Inferred subclasses | | Count: ___ |
| Warnings | ☐ None / ☐ Found | |

## Signature
- Evaluator: _______________
- Date: _______________
- Protégé version confirmed: _______________
CHECKLIST

echo ""
echo "=============================================="
echo " Protégé Setup Complete!"
echo "=============================================="
echo ""
echo " To launch Protégé:"
echo "   ${PROTEGE_DIR}/launch_protege.sh"
echo ""
echo " Evaluation checklist:"
echo "   ${PROTEGE_DIR}/PROTEGE_EVALUATION_CHECKLIST.md"
echo ""
echo " Manual download (if auto-download failed):"
echo "   https://protege.stanford.edu/products.php#desktop-protege"
echo "=============================================="
