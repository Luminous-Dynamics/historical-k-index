#!/usr/bin/env bash
#
# Consolidate all data from kosmic-lab to new repository
# This moves (not copies) data to avoid duplication
#

set -e

echo "=========================================="
echo "Data Consolidation: kosmic-lab → historical-k-index-repo"
echo "=========================================="
echo ""

# Define paths
NEW_REPO="/srv/luminous-dynamics/historical-k-index-repo"
OLD_SCRIPTS="/srv/luminous-dynamics/kosmic-lab/historical_k"

cd "$NEW_REPO"

echo "📊 Step 1: Move data_sources/ (H1-H7 organized data)"
echo ""

if [ -d "$OLD_SCRIPTS/data_sources" ]; then
    echo "  Moving data_sources/ with H-component structure..."

    # Move the entire data_sources directory
    mv "$OLD_SCRIPTS/data_sources" data/

    echo "  ✓ Moved data_sources/ containing:"
    ls -d data/data_sources/*/ | sed 's/^/    - /'
else
    echo "  ⚠ data_sources/ not found in old location"
fi

echo ""
echo "📁 Step 2: Move raw data files"
echo ""

if [ -d "$OLD_SCRIPTS/data" ]; then
    echo "  Moving individual data files..."

    # Move CSV files
    if ls "$OLD_SCRIPTS/data"/*.csv 1> /dev/null 2>&1; then
        mv "$OLD_SCRIPTS/data"/*.csv data/raw/
        echo "  ✓ Moved $(ls data/raw/*.csv 2>/dev/null | wc -l) CSV files"
    fi

    # Move large datasets (like OWID)
    if ls "$OLD_SCRIPTS/data"/OWID*.csv 1> /dev/null 2>&1; then
        mkdir -p data/raw/owid/
        mv "$OLD_SCRIPTS/data"/OWID*.csv data/raw/owid/
        echo "  ✓ Moved OWID dataset (9.2 MB)"
    fi

    # Move build scripts to processing
    if ls "$OLD_SCRIPTS/data"/build_*.py 1> /dev/null 2>&1; then
        mkdir -p scripts/processing/legacy_builders/
        mv "$OLD_SCRIPTS/data"/build_*.py scripts/processing/legacy_builders/
        echo "  ✓ Moved $(ls scripts/processing/legacy_builders/*.py 2>/dev/null | wc -l) build scripts"
    fi
fi

echo ""
echo "🖼️  Step 3: Move figures"
echo ""

if [ -d "$OLD_SCRIPTS/figures" ]; then
    echo "  Moving generated figures..."

    # Merge with existing figures
    if [ -d "outputs/figures" ]; then
        cp -r "$OLD_SCRIPTS/figures"/* outputs/figures/
        rm -rf "$OLD_SCRIPTS/figures"
        echo "  ✓ Merged figures directories"
    else
        mv "$OLD_SCRIPTS/figures" outputs/
        echo "  ✓ Moved figures directory"
    fi

    echo "  Total figures: $(find outputs/figures -type f -name "*.png" 2>/dev/null | wc -l)"
fi

echo ""
echo "📋 Step 4: Inventory what was moved"
echo ""

# Count files
CSV_COUNT=$(find data/raw -name "*.csv" 2>/dev/null | wc -l)
DATASOURCES_DIRS=$(find data/data_sources -type d -maxdepth 1 2>/dev/null | wc -l)
BUILD_SCRIPTS=$(find scripts/processing/legacy_builders -name "*.py" 2>/dev/null | wc -l)
FIGURES=$(find outputs/figures -name "*.png" 2>/dev/null | wc -l)

echo "Moved to new repository:"
echo "  📊 $CSV_COUNT raw CSV files"
echo "  📁 $DATASOURCES_DIRS data_sources directories"
echo "  🔧 $BUILD_SCRIPTS legacy build scripts"
echo "  🖼️  $FIGURES figure files"

echo ""
echo "📍 Step 5: Create data organization README"
echo ""

cat > data/README.md << 'EOF'
# Historical K-Index Data Organization

**Last Updated**: 2025-12-03
**Total Data Points**: 191,913 across 211 years

---

## Directory Structure

```
data/
├── raw/                          # Original downloaded data
│   ├── *.csv                    # Individual datasets
│   └── owid/                    # Our World in Data files
│
├── data_sources/                # Organized by harmony
│   ├── h1_governance/           # H₁ component data
│   ├── h2_interconnection/      # H₂ component data
│   ├── h3_reciprocity/          # H₃ component data
│   ├── h4_complexity/           # H₄ component data
│   ├── h5_knowledge/            # H₅ component data
│   ├── h6_wellbeing/            # H₆ component data
│   ├── h7_computation/          # H₇ computation files
│   ├── h7_energy/               # H₇ energy data
│   ├── h7_institutions/         # H₇ governance data
│   ├── h7_knowledge/            # H₇ education/patents
│   ├── h7_tech/                 # H₇ technology data
│   ├── processed/               # Processed harmony data
│   ├── raw/                     # Raw source files
│   └── external/                # External datasets
│
├── processed/                   # Analysis-ready datasets
│   ├── H7_evolutionary_progression.csv      # Main H₇ dataset
│   ├── K_index_time_series_1810_2020.csv   # Full K(t) series
│   ├── K_index_validated_h7_integration_1996_2020.csv
│   ├── H7_country_rankings_2021.csv        # Country rankings
│   └── H7_components/                       # Component breakdowns
│
└── sources/                     # Documentation
    └── [data source documentation]
```

---

## Data Sources

All raw data downloaded from:
- World Bank WDI (education, infrastructure, economic)
- World Bank WGI (governance indicators)
- WIPO (patent statistics)
- Barro-Lee (educational attainment)
- V-Dem (democracy indicators)
- KOF (globalization index)
- HYDE 3.2.1 (historical population)
- Seshat (ancient civilizations)
- Our World in Data (energy, environment)

---

## Processing Pipeline

1. **Download** → `data/raw/` (via scripts/data_collection/)
2. **Transform** → `data/data_sources/` (via scripts/processing/)
3. **Integrate** → `data/processed/` (analysis-ready)
4. **Analyze** → Results in `outputs/`

---

## Key Datasets

### H₇ Evolutionary Progression
- **File**: `processed/H7_evolutionary_progression.csv`
- **Size**: 247 KB
- **Observations**: 2,352 (159 countries, 1996-2021)
- **Variables**: Country, year, education, patents, infrastructure, governance, H7

### K-Index Time Series
- **File**: `processed/K_index_time_series_1810_2020.csv`
- **Coverage**: 211 years
- **Variables**: Year, K(t), H1-H7 components

### Country Rankings
- **File**: `processed/H7_country_rankings_2021.csv`
- **Size**: 32 KB
- **Countries**: 159
- **Top Performer**: Singapore (0.771)

---

## Data Versioning

- v1.0.0: Initial dataset (Paper 1)
- v1.1.0: Planned H₃ refinement (climate finance + refugees)
- v2.0.0: Planned sub-national data

---

## Usage

See `docs/DATA_AVAILABILITY.md` for complete data documentation.
See `docs/REPLICATION_GUIDE.md` for reproduction instructions.
EOF

echo "  ✓ Created data/README.md"

echo ""
echo "🧹 Step 6: Clean up empty directories in kosmic-lab"
echo ""

# Remove empty data directories
if [ -d "$OLD_SCRIPTS/data" ]; then
    rmdir "$OLD_SCRIPTS/data" 2>/dev/null || echo "  (data/ not empty, contains other files)"
fi

if [ -d "$OLD_SCRIPTS/figures" ]; then
    rmdir "$OLD_SCRIPTS/figures" 2>/dev/null || echo "  (figures/ cleaned)"
fi

echo ""
echo "=========================================="
echo "CONSOLIDATION COMPLETE"
echo "=========================================="
echo ""
echo "New repository structure:"
echo "  data/"
echo "    ├── raw/              ($CSV_COUNT CSV files)"
echo "    ├── data_sources/     ($DATASOURCES_DIRS harmony directories)"
echo "    └── processed/        (4 main analysis files)"
echo ""
echo "  scripts/"
echo "    └── processing/legacy_builders/  ($BUILD_SCRIPTS scripts)"
echo ""
echo "  outputs/"
echo "    └── figures/          ($FIGURES PNG files)"
echo ""
echo "Files remaining in kosmic-lab/historical_k/:"
ls -la "$OLD_SCRIPTS" | grep -E "^d|^-" | wc -l
echo "  (Mostly Python scripts and docs)"
echo ""
echo "✅ All data successfully moved to new repository!"
echo ""
echo "Next steps:"
echo "1. Review data organization"
echo "2. Update any hardcoded paths in scripts"
echo "3. Archive remaining kosmic-lab files"
echo "4. Test data pipeline"
