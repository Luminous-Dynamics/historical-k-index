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
