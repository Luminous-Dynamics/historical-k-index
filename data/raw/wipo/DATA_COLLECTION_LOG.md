# WIPO Patent Data Collection Log

**Date:** 2025-12-03 02:03:33
**Component:** H₇ (Evolutionary Progression) - Patents

## Data Source Information

### Primary Source: WIPO IP Statistics
- **URL:** https://www.wipo.int/ipstats/en/
- **Coverage:** 1883-2023 (140 years)
- **Variables:** Patent applications by country of origin
- **Format:** CSV
- **License:** Public use for research (attribution required)

### Alternative Source: World Bank
- **Indicator:** IP.PAT.RESD (Patent applications, residents)
- **URL:** https://data.worldbank.org/indicator/IP.PAT.RESD
- **Coverage:** 1960-2023 (63 years)
- **Format:** CSV
- **License:** CC-BY-4.0

## Collection Status

- [ ] WIPO primary data downloaded
- [ ] World Bank fallback data downloaded
- [ ] Data quality checked
- [ ] Population data integrated
- [ ] Per capita calculation complete
- [ ] Normalization to [0,1] complete
- [ ] Global aggregate calculated

## Notes

WIPO provides the most comprehensive historical coverage going back to 1883.
This is critical for constructing H₇ over the full 1810-2020 period.

For pre-1883 period (1810-1882), we may need to:
1. Extrapolate backwards using proxy indicators
2. Use historical patent office records from major countries
3. Interpolate from earliest available data

## Citation

If using WIPO data:
```
World Intellectual Property Organization (WIPO). 2024.
WIPO IP Statistics Data Center. Geneva: WIPO.
Available at: https://www.wipo.int/ipstats/
Accessed: 2025-12-03
```

## Next Steps

1. Download WIPO patent data manually
2. Integrate with HYDE population data (already available)
3. Calculate patents per capita by country-year
4. Aggregate to global weighted average
5. Normalize to [0, 1] scale using historical min-max
6. Save as `data/processed/H7_components/patents.csv`
