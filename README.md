# Historical K-Index Research Program: Measuring Global Coordination Capacity (1810-2020)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **A Multi-Paper Research Program Quantifying Humanity's Capacity for Large-Scale Cooperation**

**Lead Researcher**: Tristan Stoltz
**Institution**: Luminous Dynamics
**Contact**: tristan.stoltz@evolvingresonantcocreationism.com

---

## 🌟 Why This Matters: The Paradigm Shift

**Traditional Question**: "How wealthy/developed are countries?"
**Our Question**: "How capable is humanity of coordinating at global scale?"

This research program introduces the **K-index**: a comprehensive measure of global coordination capacity integrating governance quality, economic interconnection, reciprocity, complexity, knowledge systems, wellbeing, and evolutionary progression.

**Why now?** Climate change, pandemics, and AI governance require unprecedented global cooperation. We can't manage what we can't measure.

📖 **Read the full paradigm shift**: [PARADIGM_SHIFT.md](PARADIGM_SHIFT.md)

---

## 📚 The Research Program: 8-Paper Arc

This repository contains materials for a comprehensive 8-paper research program—from theory to existential risk to policy action:

| Paper | Focus | Status | Target Journal | Expected |
|-------|-------|--------|----------------|----------|
| **Paper 1: Foundation** | K-index framework 1810-2020<br/>All seven harmonies validated | 95% Complete | Nature Sustainability | Dec 2025 |
| **Paper 2: Civilization Collapse** 🆕 | What destroys coordination?<br/>Bronze Age, Rome, Maya, Soviet | Infrastructure Ready | PNAS | Q1 2026 |
| **Paper 3: Modern Fragility** | Are we at risk now?<br/>Current trajectory analysis | Planned | Science | Q2 2026 |
| **Paper 4: Regional Divergence** | Where are weak points?<br/>Coordination inequality | Planned | Regional Studies | Q3 2026 |
| **Paper 5: Climate Gap** | What's most urgent?<br/>Paris Agreement requirements | Planned | Nature Climate Change | Q4 2026 |
| **Paper 6: Recovery Mechanisms** | What rebuilds coordination?<br/>Post-collapse recovery | Planned | World Development | Q1 2027 |
| **Paper 7: AI Governance** | What's coming next?<br/>Coordination for AI safety | Planned | Science | Q2 2027 |
| **Paper 8: Policy Framework** | How do we act?<br/>Comprehensive intervention design | Planned | Annual Review | Q3 2027 |

**The Arc**: Build understanding → Reveal existential stakes → Identify vulnerabilities → Provide solutions

**See**: [RESEARCH_PROGRAM_REIMAGINED.md](RESEARCH_PROGRAM_REIMAGINED.md) for complete program

---

## 🚀 Quick Start

### Option A: Full Replication Package (Recommended)

```bash
# Download complete package from Zenodo (~2.5 GB)
# Includes ALL data + code + manuscript + figures
wget https://zenodo.org/record/XXXXXXX/files/historical-k-index-v1.0.0.zip
unzip historical-k-index-v1.0.0.zip
cd historical-k-index-repo

# Enter reproducible environment
nix develop

# Install dependencies
poetry install

# Generate all results
poetry run python shared/scripts/process_all_data.py
poetry run python shared/scripts/generate_supplementary_figures.py
poetry run python shared/scripts/generate_supplementary_tables.py
```

**Time**: ~10 minutes | **Output**: 23 figures (300 DPI) + 4 tables + validated K(t) series

### Option B: Clone and Download Data

```bash
# Clone repository (lightweight: ~10 MB)
git clone https://github.com/Luminous-Dynamics/historical-k-index.git
cd historical-k-index

# Enter environment
nix develop
poetry install

# Download all data sources automatically (~2.5 GB, 10-20 min)
poetry run python shared/scripts/download_all_data.py

# Generate results
poetry run python shared/scripts/process_all_data.py
```

**Time**: ~25 minutes (first run)

---

## 📊 Repository Structure (Monorepo for Trilogy)

```
historical-k-index-repo/
├── papers/                          # All research papers
│   ├── 01-historical-k-index/      # Paper 1 (ready for submission)
│   │   ├── manuscript/             # Complete LaTeX + PDFs
│   │   ├── analysis/               # Paper-specific analysis
│   │   └── figures/                # Paper-specific figures
│   └── 02-civilization-collapse/   # Paper 2 (infrastructure ready)
│       ├── manuscript/             # Outline + draft structure
│       ├── analysis/               # Harmony scoring rubric
│       ├── literature/             # 40+ source review framework
│       └── data/                   # Case study data plans
│
├── shared/                          # Shared resources for all papers
│   ├── data/                       # ALL datasets (gitignored)
│   │   ├── data_sources/           # Harmony-organized data
│   │   ├── raw/                    # Original downloads (191,913 points)
│   │   └── processed/              # Analysis-ready datasets
│   ├── scripts/                    # All Python code
│   │   ├── data_collection/        # Download & ETL
│   │   ├── processing/             # K-index computation
│   │   ├── analysis/               # Statistical tests
│   │   ├── figures/                # Visualization
│   │   └── validation/             # Quality checks
│   └── docs/                       # All documentation
│       ├── DATA_SOURCES.md         # Complete data provenance
│       ├── REPLICATION_GUIDE.md    # Step-by-step instructions
│       └── METHODOLOGY.md          # Technical details
│
├── outputs/                         # Generated files (gitignored)
│   ├── figures/                    # All publication figures
│   └── tables/                     # Supplementary tables
│
├── CITATION.cff                     # Machine-readable citation
├── CONTRIBUTING.md                  # Collaboration guidelines
├── PARADIGM_SHIFT.md               # Theoretical foundation
├── flake.nix                       # Reproducible environment
└── README.md                       # This file
```

**Design Principle**: Monorepo structure enables shared infrastructure while maintaining paper-specific materials.

---

## 🔬 Methodology Summary

### The K-Index: Seven Harmonies Framework

The K-index measures global coordination capacity through seven integrated dimensions:

1. **H₁: Governance Coherence** - Institutional quality and rule of law (V-Dem, WGI)
2. **H₂: Economic Interconnection** - Trade integration and financial flows (World Bank, IMF)
3. **H₃: Cooperative Reciprocity** - Trust and mutual aid (World Values Survey)
4. **H₄: Economic Complexity** - Production sophistication (Atlas of Economic Complexity)
5. **H₅: Knowledge Systems** - Education and innovation (UNESCO, WIPO)
6. **H₆: Wellbeing Metrics** - Health and quality of life (WHO, World Bank)
7. **H₇: Evolutionary Progression** - Infrastructure and development (World Bank, ITU)

**Integration Formula** (geometric mean prevents compensation):
```
K(t) = [H₁(t) × H₂(t) × H₃(t) × H₄(t) × H₅(t) × H₆(t) × H₇(t)]^(1/7)
```

**Key Innovation**: Direct empirical measurement of H₇ (vs demographic proxies) yields **-7.0% more conservative estimates**, demonstrating methodological rigor over optimism.

**See**: [shared/docs/METHODOLOGY.md](shared/docs/METHODOLOGY.md) for technical details

---

## 📈 Key Findings (Paper 1)

### 1. Six-Fold Increase in Global Coordination (1810-2020)

```
K(1810) = 0.13  →  K(2020) = 0.78  (+500%)
```

**Growth acceleration**:
- 1810-1900: Industrial foundations (+61%)
- 1900-1950: Wars and recovery (+57%)
- 1950-1990: Post-war globalization (+119%)
- 1990-2020: Information age (+54%)

### 2. Post-1990 Structural Imbalance ⚠️

**Harmony contributions to K(t) growth (1990-2020)**:
- H₅ (Interconnection): **35%** - Digital/trade networks
- H₄ (Complexity): **22%** - Market integration
- H₇ (Evolution): **18%** - Education/technology
- H₂ (Wellbeing): **13%** - Health improvements
- **H₃ (Reciprocity): 12%** ⚠️ **Lagging despite climate urgency**
- H₁ (Governance): **8%** - Institutional quality
- H₆ (Wellbeing): **6%** - Resource sharing

**Critical Gap**: Climate coordination requires high H₃ (trust-intensive cooperation), yet H₃ grew slowest.

### 3. Empirical Validation

| External Benchmark | Correlation | p-value | Interpretation |
|-------------------|-------------|---------|----------------|
| **GDP per capita (log)** | r = 0.98 | p < 10⁻¹⁴⁹ | Extremely strong |
| **Human Development Index** | r = 0.70 | p < 10⁻⁸⁷ | Strong |
| **Life expectancy** | r = 0.82 | p < 10⁻¹¹² | Very strong |
| **Democracy index (V-Dem)** | r = 0.65 | p < 10⁻⁷³ | Strong |

### 4. Crisis Resilience

- **WWI (1914-1918)**: K(t) declined -11%
- **WWII (1939-1945)**: K(t) declined -16%
- **Post-1945**: Full recovery by 1960 (demonstrating coordination resilience)

**See**: [papers/01-historical-k-index/manuscript/](papers/01-historical-k-index/manuscript/) for complete results

---

## 📚 Data Availability

### Complete Replication Package (Zenodo)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

**Download**: https://zenodo.org/record/XXXXXXX/files/historical-k-index-v1.0.0.zip
**Size**: ~2.5 GB (complete package)
**Includes**: All data (raw + processed) + code + manuscript + figures

### Primary Data Sources (All Open Access)

| Source | Coverage | Size | License |
|--------|----------|------|---------|
| **World Values Survey** | 1981-2022 | 1.3 GB | Free (cite) |
| **V-Dem Dataset v15** | 1789-2024 | 195 MB | CC-BY-SA-4.0 |
| **World Bank (WDI/WGI)** | 1960-2024 | API | CC-BY-4.0 |
| **WIPO Patent Statistics** | 1883-2023 | API | Free |
| **Barro-Lee Education** | 1950-2020 | 2 MB | Free (cite) |
| **KOF Globalization Index** | 1970-2023 | 5 MB | CC-BY-4.0 |

**Complete data documentation**: [shared/docs/DATA_SOURCES.md](shared/docs/DATA_SOURCES.md)

**Note**: Data excluded from Git (GitHub 100 MB limit). Available via Zenodo or download script.

---

## 🔧 Computational Requirements

**Minimal** (reproduce with pre-downloaded data):
- RAM: 4 GB
- Storage: 2 GB
- Time: ~6 minutes

**Full Pipeline** (download + process):
- RAM: 8 GB (recommended)
- Storage: 5 GB
- Time: ~15 minutes (first run)
- Network: Stable internet

**Reproducibility**: Nix flake ensures exact dependency versions across all systems.

---

## 📖 Citation

### For the Research Program

```bibtex
@misc{stoltz2025k_index_program,
  author = {Stoltz, Tristan},
  title = {Historical K-Index Research Program: Global Coordination Capacity 1810-2020},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXXX},
  url = {https://github.com/Luminous-Dynamics/historical-k-index}
}
```

### For Paper 1 (Foundation)

```bibtex
@article{stoltz2025k_index_foundation,
  title = {Quantifying Global Coordination Capacity: A Historical K-Index from 1810-2020},
  author = {Stoltz, Tristan},
  journal = {Nature Sustainability},
  year = {2025},
  status = {Submitted},
  doi = {10.5281/zenodo.XXXXXXX}
}
```

**Automated citation**: See [CITATION.cff](CITATION.cff) (GitHub renders automatically)

---

## 🤝 Contributing

**We welcome contributions!** This research program benefits from community collaboration.

**Ways to contribute**:
- 🐛 Report data issues or bugs
- 💡 Suggest methodological improvements
- 📊 Contribute additional data sources
- 🔬 Propose research extensions (Papers 4+)
- 📝 Improve documentation
- 🧪 Add validation tests

**See**: [CONTRIBUTING.md](CONTRIBUTING.md) for complete guidelines

**Code of Conduct**: We prioritize respectful, scientific, and open collaboration.

---

## 🗺️ Research Roadmap

### Completed ✅
- Paper 1: K-index framework and validation (Dec 2025 submission)
- 191,913 data points across seven harmonies
- 2,352 validated H₇ observations (159 countries, 1996-2021)
- Paper 2 infrastructure: Complete research framework for civilization collapse analysis

### In Progress 🚧
- Paper 2: Civilization Collapse literature review and harmony scoring (Q1 2026)
  - Bronze Age Collapse data collection underway
  - Harmony scoring rubric developed

### Planned 📋
- Paper 3: Modern Fragility Assessment (Q2 2026)
- Paper 4: Regional Divergence (Q3 2026)
- Paper 5: Climate Coordination Gap (Q4 2026)
- Paper 6: Recovery Mechanisms (Q1 2027)
- Paper 7: AI Governance Readiness (Q2 2027)
- Paper 8: Comprehensive Policy Framework (Q3 2027)

### Future Directions 🔮
- Interactive dashboard for exploring K(t) trends
- Integration with climate vulnerability indices
- Real-time coordination monitoring
- Policy implementation toolkit

**Community input welcome!** Open a Discussion to propose research directions.

---

## 📜 License

- **Code**: MIT License (use freely, cite appropriately)
- **Data**: CC-BY-4.0 (attribution required)
- **Manuscript**: All rights reserved until publication

---

## 📧 Contact

**Research Questions**: tristan.stoltz@evolvingresonantcocreationism.com
**GitHub Issues**: [Bug reports and feature requests](https://github.com/Luminous-Dynamics/historical-k-index/issues)
**GitHub Discussions**: [Research ideas and collaboration](https://github.com/Luminous-Dynamics/historical-k-index/discussions)

---

## 🏆 Acknowledgments

This research stands on the shoulders of giants. We thank:
- **World Bank** - Open Data initiative (WDI/WGI)
- **V-Dem Institute** - Democracy indicators
- **World Values Survey Association** - Trust and reciprocity data
- **WIPO** - Patent statistics
- **KOF Swiss Economic Institute** - Globalization metrics
- **Barro-Lee** - Educational attainment data

**Open Science**: This work is committed to full transparency and reproducibility.

---

## 🌊 Join the Movement

Global coordination is humanity's superpower. By measuring it, we can improve it.

**Get involved**:
- ⭐ Star this repository to follow progress
- 🔔 Watch for new papers and data releases
- 💬 Join Discussions to shape future research
- 🤝 Contribute (see CONTRIBUTING.md)
- 📢 Share with colleagues working on global cooperation

**Together, we can build the knowledge infrastructure for effective planetary coordination.**

---

**Maintained by**: Tristan Stoltz (Luminous Dynamics)
**Last Updated**: December 3, 2025
**Repository Status**: Active development (Paper 1 ready, Paper 2 infrastructure complete, Papers 3-8 planned)
**DOI**: [10.5281/zenodo.XXXXXXX](https://doi.org/10.5281/zenodo.XXXXXXX) (will be assigned on first release)

---

*"We cannot solve the coordination problems of the 21st century with the measurement tools of the 20th. The K-index offers a path forward."*
