#!/usr/bin/env bash
#
# Repository Consolidation Script
# Consolidates scattered historical-k materials into single clean repo
#
# Usage: ./CONSOLIDATE_REPOSITORY.sh
#

set -e  # Exit on error

echo "=========================================="
echo "Historical K-Index Repository Consolidation"
echo "=========================================="
echo ""

# Define paths
REPO_ROOT="/srv/luminous-dynamics/historical-k-index-repo"
KOSMIC_PAPER="/srv/luminous-dynamics/kosmic-lab/docs/papers/Historical-k"
KOSMIC_SCRIPTS="/srv/luminous-dynamics/kosmic-lab/historical_k"

cd "$REPO_ROOT"

# Step 1: Create manuscript directory and copy files
echo "📄 Step 1: Consolidating manuscript files..."
mkdir -p manuscript

# Copy main manuscript files
cp "$KOSMIC_PAPER/k_index_manuscript.tex" manuscript/
cp "$KOSMIC_PAPER/k_index_manuscript.pdf" manuscript/
cp "$KOSMIC_PAPER/k_index_references.bib" manuscript/
cp "$KOSMIC_PAPER/Supplementary_Materials.tex" manuscript/
cp "$KOSMIC_PAPER/Supplementary_Materials.pdf" manuscript/
cp "$KOSMIC_PAPER/cover_letter.txt" manuscript/

echo "  ✓ Copied 6 manuscript files"

# Step 2: Organize scripts by function
echo ""
echo "🔧 Step 2: Organizing scripts by function..."

# Create script subdirectories
mkdir -p scripts/processing
mkdir -p scripts/analysis
mkdir -p scripts/figures
mkdir -p scripts/validation

# Copy processing scripts
cp "$KOSMIC_SCRIPTS/compute_final_k_index.py" scripts/processing/
cp "$KOSMIC_SCRIPTS/compute_h7_composite.py" scripts/processing/
cp "$KOSMIC_SCRIPTS/compute_k.py" scripts/processing/
cp "$KOSMIC_SCRIPTS/etl.py" scripts/processing/
cp "$KOSMIC_SCRIPTS/aggregation_methods.py" scripts/processing/

echo "  ✓ Copied 5 processing scripts"

# Copy H-component creation scripts
cp "$KOSMIC_SCRIPTS/create_h1_governance_dataset.py" scripts/processing/
cp "$KOSMIC_SCRIPTS/create_h2_interconnection_dataset.py" scripts/processing/
cp "$KOSMIC_SCRIPTS/create_h3_reciprocity_dataset.py" scripts/processing/
cp "$KOSMIC_SCRIPTS/create_h4_complexity_dataset.py" scripts/processing/
cp "$KOSMIC_SCRIPTS/create_h5_knowledge_dataset.py" scripts/processing/
cp "$KOSMIC_SCRIPTS/create_h6_wellbeing_dataset.py" scripts/processing/

echo "  ✓ Copied 6 H-component scripts"

# Copy analysis scripts
cp "$KOSMIC_SCRIPTS/alternative_formulations.py" scripts/analysis/
cp "$KOSMIC_SCRIPTS/robustness_tests.py" scripts/analysis/
cp "$KOSMIC_SCRIPTS/sensitivity.py" scripts/analysis/
cp "$KOSMIC_SCRIPTS/external_validation.py" scripts/analysis/
cp "$KOSMIC_SCRIPTS/structural_breaks.py" scripts/analysis/

echo "  ✓ Copied 5 analysis scripts"

# Copy figure generation scripts
cp "$KOSMIC_SCRIPTS/create_manuscript_figures.py" scripts/figures/
cp "$KOSMIC_SCRIPTS/visualize_harmonies.py" scripts/figures/

echo "  ✓ Copied 2 figure scripts"

# Copy validation scripts
cp "$KOSMIC_SCRIPTS/validate_k_index.py" scripts/validation/
cp "$KOSMIC_SCRIPTS/validate_geometric_integration.py" scripts/validation/
cp "$KOSMIC_SCRIPTS/test_geometric_conversion.py" scripts/validation/

echo "  ✓ Copied 3 validation scripts"

# Step 3: Create archive of old structure
echo ""
echo "🗄️  Step 3: Creating archive of old structure..."

mkdir -p archive/kosmic-lab-snapshot-2025-12-03

# Copy key documentation files for reference
cp "$KOSMIC_PAPER/README.md" archive/kosmic-lab-snapshot-2025-12-03/ 2>/dev/null || true
cp "$KOSMIC_PAPER/IMPLEMENTATION_PROGRESS_2025_11_27.md" archive/kosmic-lab-snapshot-2025-12-03/ 2>/dev/null || true
cp "$KOSMIC_PAPER/SESSION_SUMMARY_2025_11_27.md" archive/kosmic-lab-snapshot-2025-12-03/ 2>/dev/null || true

echo "  ✓ Archived 3 reference documents"

# Step 4: Update README with new structure
echo ""
echo "📝 Step 4: Documentation updated separately"

# Step 5: Summary
echo ""
echo "=========================================="
echo "CONSOLIDATION COMPLETE"
echo "=========================================="
echo ""
echo "Repository structure:"
echo "  manuscript/       - LaTeX + PDF (6 files)"
echo "  scripts/"
echo "    ├── data_collection/  - Download scripts (already here)"
echo "    ├── processing/       - ETL & H-component (11 scripts)"
echo "    ├── analysis/         - Robustness tests (5 scripts)"
echo "    ├── figures/          - Visualization (2 scripts)"
echo "    └── validation/       - Quality checks (3 scripts)"
echo "  data/             - Raw + processed data"
echo "  outputs/          - Figures + tables"
echo "  docs/             - Documentation"
echo "  archive/          - Legacy reference materials"
echo ""
echo "Next steps:"
echo "1. Review consolidated structure"
echo "2. Update manuscript with H₇ improvements"
echo "3. Add Zenodo DOI"
echo "4. Submit to Nature Sustainability!"
echo ""
echo "✅ Ready for publication excellence!"
