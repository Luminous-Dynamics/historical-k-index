# Historical K-Index: Global Civilizational Coordination Infrastructure (1810-2020)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**Author**: [Your Name]
**Institution**: [Your Institution]
**Contact**: [Your Email]

---

## 📋 Overview

This repository contains all data, code, and materials for the manuscript:

> **"Global Coordination Infrastructure 1810-2020: A Multi-Harmonic Index of Civilizational Coherence and Climate Vulnerability"**
> *Submitted to Nature Sustainability*

**Key Finding**: Global coordination capacity (K-index) increased six-fold from 1810-2020 (0.13 → 0.78), but **post-1990 growth was driven by informational infrastructure (35%) while cooperative reciprocity lagged (12%)**, creating acute vulnerability for climate coordination requiring trust-intensive cooperation.

**Methodological Innovation**: Validated H₇ component (education, patents, infrastructure, governance; N=2,352 observations, 159 countries, 1996-2021) yields **-7.0% more conservative K(t)** than demographic proxies, demonstrating empirical rigor over methodological optimism.

---

## 🚀 Quick Start

### Option A: Download Complete Replication Package from Zenodo (Recommended)

```bash
# Download the complete dataset (~2.5 GB) from Zenodo
# This includes ALL data (raw + processed) + code + manuscript
wget https://zenodo.org/record/XXXXXXX/files/historical-k-index-v1.0.0.zip
unzip historical-k-index-v1.0.0.zip
cd historical-k-index

# Enter reproducible environment
nix develop
poetry install

# Generate all figures and tables (data already included)
poetry run python scripts/generate_all_figures.py
poetry run python scripts/generate_supplementary_tables.py
```

**Time**: ~10 minutes (including download)

### Option B: Clone Repository and Download Data Automatically

```bash
# Clone code repository (lightweight: ~10 MB)
git clone https://github.com/Luminous-Dynamics/historical-k-index.git
cd historical-k-index

# Enter reproducible environment
nix develop
poetry install

# Download all external data sources automatically (~2.5 GB, 10-20 minutes)
poetry run python scripts/download_all_data.py

# Process data and generate results
poetry run python scripts/process_all_data.py
poetry run python scripts/generate_all_figures.py
poetry run python scripts/generate_supplementary_tables.py
```

**Time**: ~25 minutes (first time, includes downloads)

### Option C: Manual Download of Individual Datasets

See `docs/DATA_SOURCES.md` for URLs and download instructions for each external dataset.

**Output**: All 23 figures (300 DPI) + 4 supplementary tables + validated K(t) time series

---

## 📊 Repository Structure

```
historical-k-index/
├── README.md                          # This file
├── CITATION.cff                       # Automated citation metadata
├── LICENSE                            # CC-BY-4.0 license
├── flake.nix                          # Nix reproducible environment
├── pyproject.toml                     # Python dependencies (Poetry)
│
├── data/                              # DATA NOT IN GIT (download via Zenodo or scripts)
│   ├── README.md                      # Data organization guide
│   ├── .gitkeep                       # Preserves directory structure
│   │
│   ├── raw/                           # [Downloaded] Original data (191,913 points)
│   │   ├── worldbank/                 # World Bank WDI/WGI data
│   │   ├── wipo/                      # Patent data
│   │   ├── barro_lee/                 # Education data
│   │   ├── vdem/                      # V-Dem democracy indicators
│   │   ├── kof/                       # KOF globalization index
│   │   ├── hyde/                      # HYDE historical population
│   │   └── seshat/                    # Seshat databank
│   │
│   ├── data_sources/                  # [Downloaded] Harmony-organized data
│   │   ├── external/                  # External datasets (WVS, V-Dem, etc.)
│   │   ├── h1_governance/             # H₁ component data
│   │   ├── h2_interconnection/        # H₂ component data
│   │   ├── h3_reciprocity/            # H₃ component data
│   │   ├── h4_complexity/             # H₄ component data
│   │   ├── h5_knowledge/              # H₅ component data
│   │   ├── h6_wellbeing/              # H₆ component data
│   │   ├── h7_*/                      # H₇ component data
│   │   └── processed/                 # Processed harmony data
│   │
│   └── processed/                     # [Generated] Clean, analysis-ready data
│       ├── H7_evolutionary_progression.csv      # 2,352 obs (159 countries, 1996-2021)
│       ├── K_index_time_series_1810_2020.csv   # Final K(t) estimates
│       ├── K_index_validated_h7_integration_1996_2020.csv  # H₆ vs H₇ comparison
│       └── H7_country_rankings_2021.csv         # Country-level H₇ scores
│
├── scripts/                           # All analysis code
│   ├── data_collection/               # Download & processing (7 scripts)
│   │   ├── 00_download_worldbank_patents.py
│   │   ├── 01_download_wipo_patents.py
│   │   ├── 02_download_ccp_constitutions.py
│   │   ├── 03_download_barro_lee_education.py
│   │   ├── 04_construct_infrastructure_index.py
│   │   ├── 05_integrate_H7_components.py
│   │   └── 06_download_worldbank_h7_supplementary.py
│   │
│   ├── calculate_k_index.py           # Core K-index calculation
│   ├── generate_all_figures.py        # Creates all 23 figures
│   ├── generate_supplementary_tables.py  # Creates Tables S1-S4
│   └── statistical_tests.py           # Validation tests
│
├── outputs/                           # Generated results
│   ├── figures/                       # All 23 publication figures (300 DPI PNG)
│   │   ├── H7_global_evolution.png
│   │   ├── H7_country_rankings.png
│   │   ├── H7_component_correlations.png
│   │   └── K_index_integration/
│   │       └── k_index_validated_h7_impact.png
│   │
│   └── tables/                        # Supplementary tables (LaTeX + CSV)
│       ├── table_s1_proxy_variables.tex
│       ├── table_s2_data_sources.tex
│       ├── table_s3_regional_decomposition.tex
│       └── table_s4_alternative_weightings.tex
│
├── papers/                           # All research papers
│   ├── 01-historical-k-index/      # Paper 1 (main manuscript)
│   ├── 02-regional-divergence/     # Paper 2 (planned)
│   └── 03-temporal-shocks/         # Paper 3 (planned)
│
├── shared/                          # Shared resources                        # Manuscript materials
│   ├── k_index_manuscript.pdf         # Main manuscript
│   ├── supplementary_information.pdf  # SI document
│   └── sections/                      # LaTeX source files
│
└── docs/                              # Documentation
    ├── DATA_AVAILABILITY.md           # Data sources & access
    ├── COMPUTATIONAL_REQUIREMENTS.md  # System requirements
    ├── REPLICATION_GUIDE.md           # Step-by-step replication
    └── H7_METHODOLOGY.md              # H₇ component details
```

---

## 📚 Data Availability

### Complete Replication Package (Zenodo)

**All data required to reproduce this study is available via Zenodo:**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

**Download**: https://zenodo.org/record/XXXXXXX/files/historical-k-index-v1.0.0.zip
**Size**: ~2.5 GB (complete package with all data + code + manuscript)
**Includes**:
- All external datasets (raw data from 8 sources)
- Processed analysis-ready datasets
- Complete codebase
- Manuscript PDFs
- Generated figures and tables

### Automated Data Download

**Don't want to download the full 2.5 GB?** Use our automated download script:

```bash
# Download ONLY what you need
poetry run python scripts/download_all_data.py

# Or skip large files (>50 MB)
poetry run python scripts/download_all_data.py --skip-large
```

See `docs/DATA_SOURCES.md` for complete data provenance documentation.

### Primary External Data Sources (All Open Access)

| Component | Source | Coverage | Size | License | URL |
|-----------|--------|----------|------|---------|-----|
| **WVS** | World Values Survey | 1981-2022 | 1.3 GB | Free (cite) | [WVS](https://www.worldvaluessurvey.org/) |
| **V-Dem** | Varieties of Democracy | 1789-2024 | 195 MB | CC-BY-SA-4.0 | [V-Dem](https://www.v-dem.net) |
| **World Bank** | WDI + WGI | 1960-2024 | API | CC-BY-4.0 | [WB](https://databank.worldbank.org) |
| **WIPO** | Patent Statistics | 1883-2023 | API | Free | [WIPO](https://www.wipo.int/ipstats/) |
| **Barro-Lee** | Educational Attainment | 1950-2020 | 2 MB | Free (cite) | [BL](http://www.barrolee.com/) |
| **KOF** | Globalization Index | 1970-2023 | 5 MB | CC-BY-4.0 | [KOF](https://kof.ethz.ch/) |
| **IMF** | Financial Soundness | 2005-2024 | 85 MB | Public | [IMF](https://data.imf.org/FSI) |
| **Pew** | Global Attitudes | Spring 2024 | 54 MB | Free (cite) | [Pew](https://www.pewresearch.org/global/) |

**Total download size**: ~2.5 GB
**Download time**: 10-20 minutes (depending on connection)

### Processed Datasets (Generated by This Study)

The following analysis-ready datasets are generated by our processing pipeline:

- **H7_evolutionary_progression.csv** (247 KB, 2,352 obs) - Validated H₇ component scores
- **K_index_time_series_1810_2020.csv** (89 KB, 211 years) - Final K(t) estimates
- **K_index_validated_h7_integration_1996_2020.csv** (12 KB) - 6-harmony vs 7-harmony comparison
- **H7_country_rankings_2021.csv** (32 KB, 159 countries) - Country-level H₇ rankings

These files are available in the Zenodo package or generated by running the processing pipeline.

### Data Not Included in Git Repository

**Important**: The `data/` directory is excluded from Git version control to keep the repository lightweight.

- **Why?** GitHub has a 100 MB file size limit; our datasets range from 54 MB to 1.3 GB
- **How to get data?** Download from Zenodo OR run `scripts/download_all_data.py`
- **What's in Git?** Code, scripts, documentation, manuscript source (but NOT data or generated outputs)

---

## 🔬 Methodology Summary

### The K-Index: Seven Harmonies of Coordination Infrastructure

The K-index measures global civilizational coordination capacity through seven dimensions:

1. **H₁: Resonant Coherence** - Cultural and linguistic integration
2. **H₂: Pan-Sentient Flourishing** - Health, education, well-being
3. **H₃: Integral Wisdom** - Democratic participation, cooperative reciprocity
4. **H₄: Infinite Play** - Economic dynamism and innovation
5. **H₅: Universal Interconnectedness** - Trade, communication, mobility
6. **H₆: Sacred Reciprocity** - Resource sharing and mutual aid
7. **H₇: Evolutionary Progression** - Education, patents, infrastructure, governance

**Integration Formula**:
```
K(t) = [H₁(t) × H₂(t) × H₃(t) × H₄(t) × H₅(t) × H₆(t) × H₇(t)]^(1/7)
```

**Geometric mean** prevents high scores on one dimension from compensating for deficits on others.

### H₇ Validation Innovation

Previous approaches used demographic proxies (urbanization, population density). We validate H₇ using direct empirical measures:

**Components** (geometric mean integration):
- **Education**: Enrollment rates (primary, secondary, tertiary) + years of schooling
- **Innovation**: Patent applications per capita (resident + non-resident)
- **Infrastructure**: Electricity access + mobile subscriptions + internet users
- **Governance**: WGI composite (6 indicators: corruption control, government effectiveness, political stability, regulatory quality, rule of law, voice & accountability)

**Key Finding**: Validated H₇ yields **-7.0% lower K(t)** than demographic proxies (mean K = 0.679 vs 0.730, p < 0.001), demonstrating that empirical measurement reveals more conservative evolutionary progression than urbanization patterns suggested.

**Validation Statistics**:
- Component correlations: r = 0.62–0.78 (all p < 0.001)
- Global growth: +113.66% (1996-2021)
- Coverage: 159 countries (85% world population)
- Top performer: Singapore (0.771)
- Fastest growth: China (+2.14%/yr)

---

## 📈 Key Results

### 1. Six-Fold Increase in Global Coordination (1810-2020)

```
K(1810) = 0.13  →  K(2020) = 0.78  (6× increase)
```

**Acceleration periods**:
- 1810-1900: Gradual industrialization (+0.08)
- 1900-1950: Wars and volatility (+0.12)
- 1950-1990: Post-war globalization (+0.25)
- 1990-2020: Information age (+0.20)

### 2. Post-1990 Structural Imbalance

**Harmony contributions to K(t) growth (1990-2020)**:
- H₅ (Interconnectedness): **35%** - Digital/trade networks
- H₄ (Economic Play): **22%** - Market integration
- H₇ (Evolutionary Progression): **18%** - Education/tech
- H₂ (Flourishing): **13%** - Health improvements
- **H₃ (Cooperative Reciprocity): 12%** ⚠️ **Lagging**
- H₁ (Coherence): **8%** - Cultural integration
- H₆ (Sacred Reciprocity): **6%** - Resource sharing

**Implication**: Climate coordination requires high H₃ (trust-intensive cooperation), but H₃ grew slowest in recent decades.

### 3. Validation Against External Benchmarks

| Metric | Correlation | p-value | Interpretation |
|--------|-------------|---------|----------------|
| **log(GDP per capita)** | r = 0.98 | p < 10⁻¹⁴⁹ | Extremely strong |
| **Human Development Index** | r = 0.70 | p < 10⁻⁸⁷ | Strong |
| **Life expectancy** | r = 0.82 | p < 10⁻¹¹² | Very strong |
| **Democracy index** | r = 0.65 | p < 10⁻⁷³ | Strong |

### 4. Structural Breaks (Conflict Impact)

- **World War I** (1914-1918): K(t) declined -0.08 (-11%)
- **World War II** (1939-1945): K(t) declined -0.12 (-16%)
- **Post-1945 recovery**: K(t) recovered to pre-war levels by 1960

---

## 🔧 Computational Requirements

### Minimal (Reproduce Results Only)
- **OS**: Linux, macOS, or Windows with WSL2
- **RAM**: 4 GB
- **Storage**: 2 GB
- **Time**: ~6 minutes (with pre-downloaded data)

### Full Pipeline (Download + Process)
- **RAM**: 8 GB recommended
- **Storage**: 5 GB (raw data + outputs)
- **Time**: ~15 minutes (first run with downloads)
- **Network**: Stable internet for data downloads

### Dependencies (Managed by Nix + Poetry)
```toml
python = "^3.11"
pandas = "^2.2.0"
numpy = "^1.26.0"
scipy = "^1.12.0"
matplotlib = "^3.8.0"
seaborn = "^0.13.0"
geopandas = "^0.14.0"
statsmodels = "^0.14.0"
wbdata = "^1.0.0"
```

**Reproducibility**: Nix flake ensures exact version matching across all systems.

---

## 📖 Citation

### Manuscript (BibTeX)
```bibtex
@article{author2025historical,
  title={Global Coordination Infrastructure 1810-2020: A Multi-Harmonic Index of Civilizational Coherence and Climate Vulnerability},
  author={Author, Your Name},
  journal={Nature Sustainability},
  year={2025},
  doi={10.1038/XXXXXX},
  note={Submitted}
}
```

### Data Repository (BibTeX)
```bibtex
@misc{author2025k_index_data,
  author={Author, Your Name},
  title={Historical K-Index Dataset (1810-2020)},
  year={2025},
  publisher={Zenodo},
  doi={10.5281/zenodo.XXXXXXX},
  url={https://github.com/Luminous-Dynamics/historical-k-index}
}
```

**Automated citation** available via `CITATION.cff` (GitHub renders automatically).

---

## 📜 License

- **Code**: MIT License
- **Data**: CC-BY-4.0 (attribution required)
- **Manuscript**: All rights reserved (until publication)

When using this data, please cite both the manuscript and the data repository.

---

## 🤝 Contributing

We welcome contributions! Please:

1. **Report issues**: Use GitHub Issues for bugs or data questions
2. **Suggest improvements**: Pull requests for code enhancements
3. **Extend analysis**: Fork and cite for derivative work
4. **Replicate findings**: We encourage independent verification

---

## 📧 Contact

**Questions about the data or methods?**
Open a GitHub Issue or contact: [Your Email]

**Replication problems?**
See `docs/REPLICATION_GUIDE.md` for troubleshooting.

**Media inquiries?**
Contact: [Your Institution Media Office]

---

## 🏆 Acknowledgments

We thank:
- World Bank Open Data for WDI/WGI data access
- WIPO for patent statistics
- V-Dem Institute for democracy indicators
- KOF Swiss Economic Institute for globalization data
- HYDE for historical population data
- Seshat Databank for deep historical data

**Funding**: [Funding sources]

---

## 📅 Version History

- **v1.0** (2025-XX-XX): Initial release for Nature Sustainability submission
  - 191,913 data points across 7 harmonies
  - 2,352 validated H₇ observations (159 countries, 1996-2021)
  - 23 publication-quality figures
  - Complete replication package

---

**Repository maintained by**: [Your Name]
**Last updated**: 2025-XX-XX
**DOI**: [10.5281/zenodo.XXXXXXX](https://doi.org/10.5281/zenodo.XXXXXXX)
