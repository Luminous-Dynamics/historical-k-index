# Replication Guide

## Quick Start (6 minutes)

### Prerequisites
- Nix package manager installed
- 8 GB RAM
- 5 GB disk space
- Stable internet connection

### Step 1: Clone Repository
```bash
git clone https://github.com/Luminous-Dynamics/historical-k-index.git
cd historical-k-index
```

### Step 2: Enter Reproducible Environment
```bash
nix develop
```

This will automatically download and configure all dependencies with exact version matching.

### Step 3: Install Python Dependencies
```bash
poetry install
```

### Step 4: Run Data Collection Pipeline
```bash
# Download all data sources (automatically)
poetry run python scripts/data_collection/00_download_worldbank_patents.py
poetry run python scripts/data_collection/01_download_wipo_patents.py
poetry run python scripts/data_collection/02_download_ccp_constitutions.py
poetry run python scripts/data_collection/03_download_barro_lee_education.py
poetry run python scripts/data_collection/04_construct_infrastructure_index.py
poetry run python scripts/data_collection/05_integrate_H7_components.py
poetry run python scripts/data_collection/06_download_worldbank_h7_supplementary.py
```

**Expected runtime**: ~6 minutes

### Step 5: Generate Figures and Tables
```bash
# Generate all supplementary tables
poetry run python scripts/generate_supplementary_tables.py

# Generate all supplementary figures
poetry run python scripts/generate_supplementary_figures.py
```

**Output**:
- `outputs/tables/` - Tables S1-S4 (CSV + LaTeX)
- `outputs/figures/supplementary/` - Figures S1-S4 (300 DPI PNG)

---

## Detailed Replication

### Data Sources
All data is downloaded automatically from public sources:
- **World Bank WDI**: Education, infrastructure, economic data
- **World Bank WGI**: Governance indicators
- **WIPO**: Patent statistics
- **Barro-Lee**: Educational attainment
- **V-Dem**: Democracy indicators
- **KOF**: Globalization index

### Reproducibility
- **Nix flake** ensures exact version matching across all systems
- **Poetry** locks Python dependencies
- **All scripts** are idempotent (safe to re-run)
- **No manual steps** required

### Verification
After running the pipeline, verify:
```bash
# Check H7 data file
ls -lh data/processed/H7_evolutionary_progression.csv
# Should be ~247 KB with 2,352 observations

# Check K-index integration
ls -lh data/processed/K_index_validated_h7_integration_1996_2020.csv
# Should show 3 formulations compared

# Check figures
ls outputs/figures/ | wc -l
# Should show 23 figures
```

---

## Troubleshooting

### Issue: Nix not found
**Solution**: Install Nix from https://nixos.org/download.html

### Issue: Poetry not found
**Solution**: Run `nix develop` first - Poetry is included in the environment

### Issue: Data download fails
**Solution**: Check internet connection, retry script (idempotent)

### Issue: Missing dependencies
**Solution**: Exit and re-enter `nix develop` to refresh environment

---

## Expected Results

### H7 Component (1996-2021)
- **Observations**: 2,352 (159 countries, 26 years)
- **Coverage**: 85% world population
- **Top performer**: Singapore (0.771)
- **Fastest growth**: China (+2.14%/yr)
- **Global growth**: +113.66%

### K-Index Impact
- **6-harmony (1810-2020)**: K₂₀₂₀ = 0.78
- **7-harmony validated (1996-2020)**: K₂₀₂₀ = 0.68
- **Difference**: -7.0% (validated more conservative)

### Validation Statistics
- Component correlations: r = 0.62-0.78 (all p < 0.001)
- Bootstrap 95% CI: All results robust
- External validation: log-GDP r = 0.98, HDI r = 0.70

---

## Questions?

Open an issue on GitHub: https://github.com/Luminous-Dynamics/historical-k-index/issues
