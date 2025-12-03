#!/usr/bin/env bash
#
# Update hardcoded paths in scripts after trilogy reorganization
# Updates absolute paths and relative data/docs references
#

set -e

echo "=========================================="
echo "Updating Script Paths for Trilogy Structure"
echo "=========================================="
echo ""

# Track changes
CHANGES=0

echo "📝 Step 1: Update absolute BASE_DIR paths"
echo ""

# Update generate_supplementary_figures.py
if grep -q 'BASE_DIR = Path("/srv/luminous-dynamics/historical-k-index")' shared/scripts/generate_supplementary_figures.py; then
    sed -i 's|BASE_DIR = Path("/srv/luminous-dynamics/historical-k-index")|BASE_DIR = Path("/srv/luminous-dynamics/historical-k-index-repo")|g' shared/scripts/generate_supplementary_figures.py
    echo "  ✓ Updated shared/scripts/generate_supplementary_figures.py"
    ((CHANGES++))
fi

# Update generate_supplementary_tables.py
if grep -q 'BASE_DIR = Path("/srv/luminous-dynamics/historical-k-index")' shared/scripts/generate_supplementary_tables.py; then
    sed -i 's|BASE_DIR = Path("/srv/luminous-dynamics/historical-k-index")|BASE_DIR = Path("/srv/luminous-dynamics/historical-k-index-repo")|g' shared/scripts/generate_supplementary_tables.py
    echo "  ✓ Updated shared/scripts/generate_supplementary_tables.py"
    ((CHANGES++))
fi

echo ""
echo "📂 Step 2: Update relative data/ paths to shared/data/"
echo ""

# Update all Python files with "data/" references
# Only update paths that should point to shared/data/
FILES_WITH_DATA_PATHS=(
    "shared/scripts/data_collection/02_download_ccp_constitutions.py"
    "shared/scripts/data_collection/06_download_worldbank_h7_supplementary.py"
    "shared/scripts/data_collection/05_integrate_H7_components.py"
    "shared/scripts/data_collection/explore_worldbank_indicators.py"
    "shared/scripts/data_collection/04_construct_infrastructure_index.py"
    "shared/scripts/data_collection/01_download_wipo_patents.py"
    "shared/scripts/data_collection/00_download_worldbank_patents.py"
    "shared/scripts/data_collection/03_download_barro_lee_education.py"
    "shared/scripts/analysis/external_validation.py"
)

for file in "${FILES_WITH_DATA_PATHS[@]}"; do
    if [ -f "$file" ]; then
        # Update OUTPUT_DIR and PROCESSED_DIR paths
        if grep -q 'OUTPUT_DIR = Path("data/' "$file"; then
            sed -i 's|OUTPUT_DIR = Path("data/|OUTPUT_DIR = Path("shared/data/|g' "$file"
            echo "  ✓ Updated OUTPUT_DIR in $file"
            ((CHANGES++))
        fi
        if grep -q 'PROCESSED_DIR = Path("data/' "$file"; then
            sed -i 's|PROCESSED_DIR = Path("data/|PROCESSED_DIR = Path("shared/data/|g' "$file"
            echo "  ✓ Updated PROCESSED_DIR in $file"
            ((CHANGES++))
        fi
        if grep -q 'COMPONENTS_DIR = Path("data/' "$file"; then
            sed -i 's|COMPONENTS_DIR = Path("data/|COMPONENTS_DIR = Path("shared/data/|g' "$file"
            echo "  ✓ Updated COMPONENTS_DIR in $file"
            ((CHANGES++))
        fi
        # Update string literals
        if grep -q '"data/raw/' "$file"; then
            sed -i 's|"data/raw/|"shared/data/raw/|g' "$file"
            echo "  ✓ Updated string paths in $file"
            ((CHANGES++))
        fi
        if grep -q 'data_dir: str = "data/' "$file"; then
            sed -i 's|data_dir: str = "data/|data_dir: str = "shared/data/|g' "$file"
            echo "  ✓ Updated data_dir in $file"
            ((CHANGES++))
        fi
    fi
done

echo ""
echo "📊 Step 3: Update figure output paths"
echo ""

# Update figure directory references
if grep -q 'FIGURES_DIR = Path("figures")' shared/scripts/data_collection/05_integrate_H7_components.py; then
    sed -i 's|FIGURES_DIR = Path("figures")|FIGURES_DIR = Path("outputs/figures")|g' shared/scripts/data_collection/05_integrate_H7_components.py
    echo "  ✓ Updated FIGURES_DIR in 05_integrate_H7_components.py"
    ((CHANGES++))
fi

echo ""
echo "📋 Step 4: Update script execution references"
echo ""

# The script references in download_all_data.py are correct as-is
# because they're meant to be run from project root
# where scripts/ resolves to shared/scripts/ correctly

echo "  ℹ️  Script execution paths are correct (run from project root)"

echo ""
echo "=========================================="
echo "PATH UPDATE COMPLETE"
echo "=========================================="
echo ""
echo "Summary:"
echo "  Total changes: $CHANGES"
echo ""
echo "Changes made:"
echo "  1. Updated absolute paths to historical-k-index-repo"
echo "  2. Updated data/ → shared/data/ in data collection scripts"
echo "  3. Updated figure output paths"
echo ""
echo "Note: Script execution paths remain as 'scripts/' because"
echo "      they are executed from project root where scripts/"
echo "      correctly resolves to shared/scripts/"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Test a script: poetry run python shared/scripts/download_all_data.py --verify-only"
echo "  3. Commit changes: git commit -m 'Fix script paths for trilogy structure'"
echo ""
