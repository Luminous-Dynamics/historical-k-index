# K-Index Data Sources

## Overview

The K-Index integrates data from multiple authoritative sources. This document provides complete provenance for all indicators used in the 1996-2020 dataset.

## Primary Data Sources

### V-Dem (Varieties of Democracy)
**URL**: https://www.v-dem.net/
**Used for**: H₁ (Governance)
**Indicators**:
- Electoral Democracy Index (v2x_polyarchy)
- Liberal Democracy Index (v2x_libdem)
- Participatory Component Index (v2x_partipdem)
- Deliberative Component Index (v2x_delibdem)
- Egalitarian Component Index (v2x_egaldem)

**Citation**:
```bibtex
@dataset{vdem2024,
  author = {Coppedge, Michael and others},
  title = {V-Dem Dataset v14},
  year = {2024},
  publisher = {Varieties of Democracy Project}
}
```

### World Bank World Development Indicators
**URL**: https://data.worldbank.org/
**Used for**: H₂, H₅, H₆, H₇

**H₂ (Interconnection) Indicators**:
- Trade (% of GDP) - NE.TRD.GNFS.ZS
- Foreign direct investment, net inflows (% of GDP) - BX.KLT.DINV.WD.GD.ZS
- International tourism, arrivals - ST.INT.ARVL
- Air transport, passengers carried - IS.AIR.PSGR

**H₅ (Knowledge) Indicators**:
- School enrollment, tertiary (% gross) - SE.TER.ENRR
- Literacy rate, adult total - SE.ADT.LITR.ZS
- Government expenditure on education - SE.XPD.TOTL.GD.ZS

**H₆ (Wellbeing) Indicators**:
- Life expectancy at birth - SP.DYN.LE00.IN
- Mortality rate, under-5 - SH.DYN.MORT
- Maternal mortality ratio - SH.STA.MMRT
- Access to electricity - EG.ELC.ACCS.ZS
- Access to basic sanitation - SH.STA.BASS.ZS

**H₇ (Technology) Indicators**:
- Internet users (per 100 people) - IT.NET.USER.ZS
- Mobile cellular subscriptions (per 100 people) - IT.CEL.SETS.P2
- Fixed broadband subscriptions (per 100 people) - IT.NET.BBND.P2
- Secure Internet servers (per million) - IT.NET.SECR.P6

**Citation**:
```bibtex
@dataset{worldbank2024,
  author = {{World Bank}},
  title = {World Development Indicators},
  year = {2024},
  publisher = {World Bank Group},
  url = {https://data.worldbank.org/}
}
```

### World Bank Worldwide Governance Indicators
**URL**: https://info.worldbank.org/governance/wgi/
**Used for**: H₁ (Governance)

**Indicators**:
- Government Effectiveness - GE.EST
- Regulatory Quality - RQ.EST
- Rule of Law - RL.EST
- Control of Corruption - CC.EST
- Voice and Accountability - VA.EST
- Political Stability - PV.EST

**Citation**:
```bibtex
@dataset{wgi2024,
  author = {Kaufmann, Daniel and Kraay, Aart and Mastruzzi, Massimo},
  title = {Worldwide Governance Indicators},
  year = {2024},
  publisher = {World Bank}
}
```

### World Values Survey
**URL**: https://www.worldvaluessurvey.org/
**Used for**: H₃ (Trust)

**Indicators**:
- Generalized trust (A165)
- Confidence in government (E069_11)
- Confidence in parliament (E069_07)
- Confidence in the press (E069_04)
- Confidence in major companies (E069_13)

**Waves Used**:
- Wave 3 (1995-1998)
- Wave 4 (1999-2004)
- Wave 5 (2005-2009)
- Wave 6 (2010-2014)
- Wave 7 (2017-2022)

**Citation**:
```bibtex
@dataset{wvs2022,
  author = {Haerpfer, C. and others},
  title = {World Values Survey: Round Seven},
  year = {2022},
  publisher = {JD Systems Institute}
}
```

### Atlas of Economic Complexity
**URL**: https://atlas.cid.harvard.edu/
**Used for**: H₄ (Complexity)

**Indicators**:
- Economic Complexity Index (ECI)
- Product diversity
- Ubiquity measures

**Citation**:
```bibtex
@dataset{atlas2024,
  author = {{Growth Lab at Harvard University}},
  title = {Atlas of Economic Complexity},
  year = {2024},
  publisher = {Harvard University}
}
```

### UNDP Human Development Reports
**URL**: https://hdr.undp.org/
**Used for**: H₅ (Knowledge), H₆ (Wellbeing)

**Indicators**:
- Human Development Index (HDI)
- Mean years of schooling
- Expected years of schooling
- GNI per capita

**Citation**:
```bibtex
@report{undp2024,
  author = {{UNDP}},
  title = {Human Development Report 2023-24},
  year = {2024},
  publisher = {United Nations Development Programme}
}
```

### ITU ICT Development Index
**URL**: https://www.itu.int/
**Used for**: H₇ (Technology)

**Indicators**:
- ICT Development Index (IDI)
- ICT access sub-index
- ICT use sub-index
- ICT skills sub-index

**Citation**:
```bibtex
@report{itu2023,
  author = {{ITU}},
  title = {Measuring Digital Development: ICT Development Index},
  year = {2023},
  publisher = {International Telecommunication Union}
}
```

## Data Processing

### Temporal Alignment
All indicators are aligned to calendar years. For surveys conducted across multiple years (e.g., WVS waves), the midpoint year is used.

### Geographic Aggregation
Global aggregates are computed as population-weighted means:
```
X_global = Σ(X_country × Population_country) / Σ Population_country
```

### Missing Data
- **Interpolation**: Linear interpolation for gaps ≤ 3 years
- **Extrapolation**: Not applied; missing endpoints remain missing
- **Proxy estimation**: Only for pre-1996 historical extensions

## Indicator Availability Matrix

| Indicator | 1996 | 2000 | 2005 | 2010 | 2015 | 2020 |
|-----------|------|------|------|------|------|------|
| V-Dem Democracy | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| WGI Governance | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| WB Trade | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| WVS Trust | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ECI Complexity | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| HDI Components | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Life Expectancy | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Internet Users | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Mobile Subs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Quality Assessment

### High Confidence (1996-2020)
- V-Dem: Rigorous expert coding with uncertainty quantification
- World Bank WDI: Official national statistics
- WGI: Multiple source triangulation
- HDI: UN-validated national data

### Moderate Confidence
- WVS: Survey-based, not annual
- ECI: Trade data quality varies by country
- ITU: Definition changes over time

## Access and Licensing

| Source | Access | License |
|--------|--------|---------|
| V-Dem | Free registration | CC-BY |
| World Bank WDI | Open | CC-BY 4.0 |
| WGI | Open | CC-BY 4.0 |
| WVS | Free registration | Academic use |
| Atlas/ECI | Open | CC-BY |
| UNDP/HDI | Open | CC-BY 3.0 IGO |
| ITU/IDI | Open | ITU terms |

## Replication

To replicate K-Index calculations:

1. Download source data from URLs above
2. Apply normalization per methodology.md
3. Calculate harmony scores (arithmetic mean of components)
4. Calculate K-Index (geometric mean of harmonies)

Scripts for replication available at:
https://github.com/Luminous-Dynamics/historical-k-index

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-10 | Initial source documentation |

## Contact

Data questions: tristan.stoltz@evolvingresonantcocreationism.com
