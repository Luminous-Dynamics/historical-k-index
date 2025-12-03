# Data Availability Statement

## Primary Data Sources

All data used in this study are from publicly accessible sources with open licenses.

### World Bank World Development Indicators (WDI)
- **URL**: https://databank.worldbank.org/source/world-development-indicators
- **License**: CC-BY-4.0
- **Accessed**: November 2024
- **Variables**: Education, infrastructure, economic indicators
- **Coverage**: 266 countries, 1960-2023

### World Bank Worldwide Governance Indicators (WGI)
- **URL**: https://www.worldbank.org/governance/wgi
- **License**: CC-BY-4.0
- **Accessed**: November 2024
- **Variables**: 6 governance dimensions
- **Coverage**: 215 countries, 1996-2023

### World Intellectual Property Organization (WIPO)
- **URL**: https://www.wipo.int/ipstats/en/
- **License**: Open access
- **Accessed**: November 2024
- **Variables**: Patent applications (resident + non-resident)
- **Coverage**: 195 countries, 1980-2021

### Barro-Lee Educational Attainment Dataset
- **URL**: http://www.barrolee.com/
- **License**: Open access
- **Accessed**: November 2024
- **Variables**: Years of schooling by level
- **Coverage**: 146 countries, 1950-2015

### Varieties of Democracy (V-Dem) Dataset v14
- **URL**: https://www.v-dem.net
- **License**: CC-BY-SA-4.0
- **Accessed**: November 2024
- **Variables**: Democracy indicators
- **Coverage**: 202 countries, 1789-2023

### KOF Globalisation Index
- **URL**: https://kof.ethz.ch/en/forecasts-and-indicators/indicators/kof-globalisation-index.html
- **License**: Open access
- **Accessed**: November 2024
- **Variables**: Economic, social, political globalization
- **Coverage**: 203 countries, 1970-2021

### HYDE 3.2.1 (History Database of the Global Environment)
- **URL**: https://dataportaal.pbl.nl/downloads/HYDE/
- **License**: CC-BY-4.0
- **Accessed**: November 2024
- **Variables**: Population, land use
- **Coverage**: Global gridded, 10000 BCE-2020 CE

### Seshat: Global History Databank
- **URL**: http://seshatdatabank.info/
- **License**: CC-BY-SA-4.0
- **Accessed**: November 2024
- **Variables**: Historical polity characteristics
- **Coverage**: 414 polities, 10000 BCE-1900 CE

---

## Processed Data Files

All processed data files are available in this repository:

### Main Dataset
- **File**: `data/processed/H7_evolutionary_progression.csv`
- **Size**: 247 KB
- **Observations**: 2,352 (159 countries × 26 years, 1996-2021)
- **Variables**: Country, year, education, patents, infrastructure, governance, H7 (integrated)

### K-Index Integration
- **File**: `data/processed/K_index_validated_h7_integration_1996_2020.csv`
- **Size**: 4.1 KB
- **Observations**: 25 years (1996-2020)
- **Variables**: Year, K_6harmony, K_7harmony_validated, K_7harmony_synthetic

### Country Rankings
- **File**: `data/processed/H7_country_rankings_2021.csv`
- **Size**: 32 KB
- **Observations**: 159 countries
- **Variables**: Country, H7_2021, rank, education, patents, infrastructure, governance

---

## Persistent Identifier

**Zenodo DOI**: [10.5281/zenodo.XXXXXXX](https://doi.org/10.5281/zenodo.XXXXXXX)

This ensures long-term preservation and citable access to all data and code.

---

## Replication Package

Complete replication package available at:
- **GitHub**: https://github.com/Luminous-Dynamics/historical-k-index
- **Zenodo**: https://doi.org/10.5281/zenodo.XXXXXXX

Includes:
- All data collection scripts (7 scripts)
- All processing scripts
- All analysis scripts
- Reproducible environment (Nix flake)
- Complete documentation

**Replication time**: 6 minutes (automated pipeline)

---

## License

- **Code**: MIT License
- **Data**: CC-BY-4.0

When using this data, please cite both the manuscript and this repository (see CITATION.cff).

---

## Contact

Questions about data or replication: [Your Email]

Issues with replication: https://github.com/Luminous-Dynamics/historical-k-index/issues
