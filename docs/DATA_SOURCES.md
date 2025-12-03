# Historical K-Index Data Sources

**Complete Data Provenance Documentation**

All data for this project is available through the Zenodo DOI (see README.md) or can be downloaded automatically using the provided scripts.

---

## Quick Start

```bash
# Download ALL data sources automatically
cd /path/to/historical-k-index
nix develop
poetry install
poetry run python scripts/download_all_data.py

# This will download ~2.5 GB of data to:
# - data/data_sources/external/  (raw external datasets)
# - data/raw/                     (processed raw data)
# - data/data_sources/processed/  (analysis-ready datasets)
```

---

## Primary External Data Sources

### 1. World Values Survey (WVS)

**Description**: Comprehensive time-series of cultural values and beliefs across societies

- **Source**: World Values Survey Association
- **URL**: https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp
- **File**: `WVS_Time_Series_1981-2022_csv_v5_0.csv`
- **Size**: 1,316 MB
- **Coverage**: 1981-2022, 120+ countries, 430,000+ respondents
- **Version**: 5.0 (2022)
- **Access Date**: 2024-11-15
- **License**: Free for academic use with citation
- **Download Script**: `scripts/data_collection/download_wvs.py`

**Citation**:
```bibtex
@dataset{wvs2022,
  author = {Haerpfer, C. and Inglehart, R. and Moreno, A. and Welzel, C. and Kizilova, K. and Diez-Medrano, J. and Lagos, M. and Norris, P. and Ponarin, E. and Puranen, B.},
  title = {World Values Survey Time-Series (1981-2022)},
  year = {2022},
  publisher = {World Values Survey Association},
  url = {https://www.worldvaluessurvey.org/}
}
```

**Variables Used**:
- Trust indicators (interpersonal trust, institutional trust)
- Social capital measures
- Democratic values
- Religious beliefs and practices

**SHA256 Checksum**: `[to be computed]`

---

### 2. Varieties of Democracy (V-Dem)

**Description**: Most comprehensive dataset on democracy and governance

- **Source**: V-Dem Institute, University of Gothenburg
- **URL**: https://www.v-dem.net/data/dataset/
- **File**: `V-Dem-CY-Core-v15.csv`
- **Size**: 195 MB
- **Coverage**: 1789-2024, 202 countries, 400+ indicators
- **Version**: v15 (2024)
- **Access Date**: 2024-11-20
- **License**: CC-BY-SA 4.0
- **Download Script**: `scripts/data_collection/download_vdem.py`

**Citation**:
```bibtex
@dataset{vdem2024,
  author = {Coppedge, Michael and Gerring, John and Knutsen, Carl Henrik and Lindberg, Staffan I. and Teorell, Jan and Alizada, Nazifa and Altman, David and Angiolillo, Fabio and Arugha, Juraj and Bernhard, Michael and Edgell, Amanda B. and Gastaldi, Lisa and Grahn, Sofie and Hegre, Håvard and Hindle, Garry and Ilchenko, Nina and Kinzelbach, Katrin and Marquardt, Kyle L. and McMann, Kelly and Mechkova, Valeriya and Medzihorsky, Juraj and Natsika, Natalia and Neundorf, Anja and Paxton, Pamela and Pemstein, Daniel and von Römer, Josefine and Seim, Brigitte and Sigman, Rachel and Skaaning, Svend-Erik and Staton, Jeffrey and Sundström, Aksel and Tzelgov, Eitan and Wang, Yi-ting and Wig, Tore and Wilson, Steven and Ziblatt, Daniel},
  title = {V-Dem Country-Year Dataset v15},
  year = {2024},
  publisher = {Varieties of Democracy Institute},
  url = {https://www.v-dem.net/}
}
```

**Variables Used**:
- Electoral democracy index
- Liberal democracy index
- Participatory democracy index
- Deliberative democracy index
- Egalitarian democracy index
- Rule of law indicators
- Civil society strength

**SHA256 Checksum**: `[to be computed]`

---

### 3. World Bank World Development Indicators (WDI)

**Description**: Primary source for development data and economic indicators

- **Source**: World Bank Group
- **URL**: https://datacatalog.worldbank.org/search/dataset/0037712
- **API Access**: `wbdata` Python package
- **Coverage**: 1960-2024, 217 economies, 1400+ indicators
- **Version**: Updated quarterly
- **Access Date**: 2024-11-25
- **License**: CC-BY 4.0
- **Download Script**: `scripts/data_collection/00_download_worldbank_patents.py`

**Citation**:
```bibtex
@dataset{worldbank2024,
  author = {{World Bank}},
  title = {World Development Indicators},
  year = {2024},
  publisher = {World Bank Group},
  url = {https://datacatalog.worldbank.org/search/dataset/0037712}
}
```

**Indicators Used**:
- GDP per capita (constant 2015 USD)
- Population totals
- Education expenditure (% of GDP)
- Health expenditure per capita
- Infrastructure investment
- Trade volumes
- Energy consumption
- CO2 emissions

**SHA256 Checksum**: N/A (API access, checksums per indicator)

---

### 4. World Intellectual Property Organization (WIPO)

**Description**: Global intellectual property statistics

- **Source**: WIPO Statistics Database
- **URL**: https://www.wipo.int/ipstats/en/
- **File**: Downloaded via API and web scraping
- **Coverage**: 1883-2023, 150+ countries
- **Version**: 2024 edition
- **Access Date**: 2024-11-10
- **License**: Free for non-commercial use
- **Download Script**: `scripts/data_collection/01_download_wipo_patents.py`

**Citation**:
```bibtex
@dataset{wipo2024,
  author = {{World Intellectual Property Organization}},
  title = {WIPO IP Statistics Data Center},
  year = {2024},
  publisher = {WIPO},
  url = {https://www.wipo.int/ipstats/}
}
```

**Variables Used**:
- Patent applications (resident and non-resident)
- Patent grants
- Trademark applications
- Industrial design applications

**SHA256 Checksum**: `[to be computed]`

---

### 5. Barro-Lee Educational Attainment Dataset

**Description**: Educational attainment for population aged 15 and over

- **Source**: Barro & Lee (2013), updated 2018
- **URL**: http://www.barrolee.com/
- **File**: `BL_v3.0.xlsx`
- **Coverage**: 1950-2020, 146 countries
- **Version**: 3.0 (2018)
- **Access Date**: 2024-10-05
- **License**: Free for academic use with citation
- **Download Script**: `scripts/data_collection/03_download_barro_lee_education.py`

**Citation**:
```bibtex
@article{barrolee2013,
  author = {Barro, Robert J. and Lee, Jong-Wha},
  title = {A New Data Set of Educational Attainment in the World, 1950-2010},
  journal = {Journal of Development Economics},
  volume = {104},
  pages = {184-198},
  year = {2013},
  doi = {10.1016/j.jdeveco.2012.10.001}
}
```

**Variables Used**:
- Average years of schooling (total population 15+)
- Average years of schooling by gender
- Percentage of population by educational level
- School enrollment ratios

**SHA256 Checksum**: `[to be computed]`

---

### 6. KOF Globalization Index

**Description**: Comprehensive measure of economic, social, and political globalization

- **Source**: KOF Swiss Economic Institute, ETH Zurich
- **URL**: https://kof.ethz.ch/en/forecasts-and-indicators/indicators/kof-globalisation-index.html
- **File**: `KOFGI_2024_public.xlsx`
- **Coverage**: 1970-2023, 203 countries
- **Version**: 2024
- **Access Date**: 2024-11-01
- **License**: CC-BY 4.0
- **Download Script**: `scripts/data_collection/download_kof.py`

**Citation**:
```bibtex
@article{gygli2019,
  author = {Gygli, Savina and Haelg, Florian and Potrafke, Niklas and Sturm, Jan-Egbert},
  title = {The KOF Globalisation Index - Revisited},
  journal = {Review of International Organizations},
  volume = {14},
  pages = {543-574},
  year = {2019},
  doi = {10.1007/s11558-019-09344-2}
}
```

**Variables Used**:
- Economic globalization (trade, FDI)
- Social globalization (information flows, cultural proximity)
- Political globalization (embassies, treaties, IGO membership)

**SHA256 Checksum**: `[to be computed]`

---

### 7. IMF Financial Soundness Indicators

**Description**: Financial system health and stability metrics

- **Source**: International Monetary Fund
- **URL**: https://data.imf.org/FSI
- **File**: `imf_fsi_raw.csv`
- **Size**: 85 MB
- **Coverage**: 2005-2024, 120+ countries
- **Version**: Latest available
- **Access Date**: 2024-11-18
- **License**: Public domain
- **Download Script**: `scripts/data_collection/download_imf_fsi.py`

**Citation**:
```bibtex
@dataset{imf2024fsi,
  author = {{International Monetary Fund}},
  title = {Financial Soundness Indicators},
  year = {2024},
  publisher = {IMF Data},
  url = {https://data.imf.org/FSI}
}
```

**Variables Used**:
- Capital adequacy
- Asset quality
- Earnings and profitability
- Liquidity
- Sensitivity to market risk

**SHA256 Checksum**: `[to be computed]`

---

### 8. Pew Research Center Global Attitudes Survey

**Description**: Public opinion on global issues, values, and institutions

- **Source**: Pew Research Center
- **URL**: https://www.pewresearch.org/global/datasets/
- **File**: `Pew Research Center Global Attitudes Spring 2024 Dataset CSV.csv`
- **Size**: 54 MB
- **Coverage**: Spring 2024, 34 countries
- **Version**: Spring 2024
- **Access Date**: 2024-11-22
- **License**: Free for non-commercial use with citation
- **Download Script**: `scripts/data_collection/download_pew.py`

**Citation**:
```bibtex
@dataset{pew2024,
  author = {{Pew Research Center}},
  title = {Global Attitudes Survey Spring 2024},
  year = {2024},
  publisher = {Pew Research Center},
  url = {https://www.pewresearch.org/global/}
}
```

**Variables Used**:
- Trust in institutions
- Views on democracy
- Economic satisfaction
- Social values

**SHA256 Checksum**: `[to be computed]`

---

## Processed Datasets (Generated by This Project)

These are the analysis-ready datasets created by our processing pipeline:

### H₇ Evolutionary Progression Dataset
- **File**: `data/processed/H7_evolutionary_progression.csv`
- **Size**: 247 KB
- **Observations**: 2,352 (159 countries, 1996-2021)
- **Generated by**: `scripts/data_collection/05_integrate_H7_components.py`
- **Description**: Complete H₇ (Evolutionary Progression) harmony component with all sub-indicators

**Variables**:
- `country_code`: ISO 3-letter country code
- `year`: Year of observation
- `h7_education`: Educational attainment index (Barro-Lee)
- `h7_patents`: Patent applications per capita (WIPO)
- `h7_infrastructure`: Infrastructure quality index (World Bank)
- `h7_governance`: Governance effectiveness (V-Dem)
- `h7_composite`: Final H₇ score (0-1 scale)

### K-Index Time Series
- **File**: `data/processed/K_index_time_series_1810_2020.csv`
- **Size**: 89 KB
- **Coverage**: 211 years (1810-2020)
- **Generated by**: `scripts/processing/compute_k_index.py`
- **Description**: Complete historical K-index trajectory with all seven harmony components

**Variables**:
- `year`: Year of observation
- `k_index`: Composite K(t) value (0-1 scale)
- `h1_governance`: H₁ governance component
- `h2_interconnection`: H₂ financial integration
- `h3_reciprocity`: H₃ reciprocity/altruism
- `h4_complexity`: H₄ economic complexity
- `h5_knowledge`: H₅ knowledge/education
- `h6_wellbeing`: H₆ health/wellbeing
- `h7_progression`: H₇ evolutionary progression

### K-Index with H₇ Integration (Validated)
- **File**: `data/processed/K_index_validated_h7_integration_1996_2020.csv`
- **Size**: 12 KB
- **Coverage**: 1996-2020 (validation period)
- **Generated by**: `scripts/analysis/validate_h7_integration.py`
- **Description**: Comparison of 6-harmony vs 7-harmony K-index formulations

**Variables**:
- `year`: Year of observation
- `k_6harmony`: Original K(t) with 6 harmonies
- `k_7harmony`: Updated K(t) with 7 harmonies
- `k_7harmony_weighted`: Alternative weighted formulation
- `difference_pct`: Percentage difference between formulations

---

## Data Processing Pipeline

### Complete Replication Workflow

```bash
# 1. Download all external data sources
poetry run python scripts/data_collection/00_download_worldbank_patents.py
poetry run python scripts/data_collection/01_download_wipo_patents.py
poetry run python scripts/data_collection/02_download_ccp_constitutions.py
poetry run python scripts/data_collection/03_download_barro_lee_education.py
poetry run python scripts/data_collection/04_construct_infrastructure_index.py
poetry run python scripts/data_collection/05_integrate_H7_components.py
poetry run python scripts/data_collection/06_download_worldbank_h7_supplementary.py

# 2. Process and clean data
poetry run python scripts/processing/clean_wvs_data.py
poetry run python scripts/processing/clean_vdem_data.py
poetry run python scripts/processing/clean_worldbank_data.py

# 3. Compute harmony components
poetry run python scripts/processing/compute_h1_governance.py
poetry run python scripts/processing/compute_h2_interconnection.py
poetry run python scripts/processing/compute_h3_reciprocity.py
poetry run python scripts/processing/compute_h4_complexity.py
poetry run python scripts/processing/compute_h5_knowledge.py
poetry run python scripts/processing/compute_h6_wellbeing.py
poetry run python scripts/processing/compute_h7_progression.py

# 4. Compute final K-index
poetry run python scripts/processing/compute_k_index.py

# 5. Validate and analyze
poetry run python scripts/analysis/validate_h7_integration.py
poetry run python scripts/analysis/compute_robustness_tests.py
poetry run python scripts/analysis/external_validation.py

# 6. Generate figures and tables
poetry run python scripts/generate_supplementary_figures.py
poetry run python scripts/generate_supplementary_tables.py
```

**Total Runtime**: ~6 minutes on modern hardware

---

## Data Quality and Validation

### Missing Data Handling

- **Interpolation**: Linear interpolation for gaps < 5 years
- **Extrapolation**: None (missing data remains missing)
- **Imputation**: Multiple imputation for structural missing data (documented in methodology)
- **Documentation**: All missing data patterns documented in `data/processed/missing_data_report.csv`

### Data Validation

- **Cross-source validation**: Compare overlapping indicators across sources
- **Temporal consistency**: Check for implausible year-to-year changes
- **Geographic consistency**: Check for outliers within regions
- **Statistical validation**: Outlier detection using robust methods
- **External validation**: Compare with external benchmarks (log-GDP, HDI)

**Validation Report**: `docs/DATA_VALIDATION_REPORT.md`

---

## Data Availability Statement

**For Manuscript Submission**:

> All data and code required to reproduce the findings of this study are publicly available. The complete replication package, including all external datasets (2.5 GB), processed datasets, analysis code, and manuscript materials, is permanently archived on Zenodo with DOI: [10.5281/zenodo.XXXXXXX]. The code repository is available on GitHub at https://github.com/Luminous-Dynamics/historical-k-index under an MIT license. External data sources are used under their respective licenses (all permit academic use with citation). Processed datasets generated by this study are released under CC-BY 4.0.

---

## Computing SHA256 Checksums

After downloading data, verify integrity:

```bash
# Compute checksums for all downloaded files
cd data/data_sources/external
find . -type f -exec sha256sum {} \; > checksums.txt

# Verify checksums
sha256sum -c checksums.txt
```

Expected checksums will be provided in the Zenodo release.

---

## License Information

### External Data Sources
- **WVS**: Free for academic use (cite properly)
- **V-Dem**: CC-BY-SA 4.0
- **World Bank WDI**: CC-BY 4.0
- **WIPO**: Free for non-commercial use
- **Barro-Lee**: Free for academic use (cite properly)
- **KOF**: CC-BY 4.0
- **IMF**: Public domain
- **Pew**: Free for non-commercial use (cite properly)

### Our Processed Data
- **License**: CC-BY 4.0
- **Citation**: See CITATION.cff in repository root

---

## Questions or Issues?

- **GitHub Issues**: https://github.com/Luminous-Dynamics/historical-k-index/issues
- **Email**: tristan.stoltz@luminousdynamics.org

---

**Last Updated**: 2025-12-03
**Document Version**: 1.0
**Zenodo DOI**: [To be assigned upon first release]
