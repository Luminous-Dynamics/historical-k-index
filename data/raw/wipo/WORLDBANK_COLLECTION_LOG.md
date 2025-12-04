# World Bank Patent Data Collection Log

**Date**: 2025-12-03 02:26:24
**Component**: H₇ (Evolutionary Progression) - Patents (World Bank fallback)

## Data Source Information

### World Bank Open Data API
- **URL**: https://data.worldbank.org/indicator/IP.PAT.RESD
- **API Endpoint**: https://api.worldbank.org/v2/
- **Coverage**: 1960-2023 (63 years)
- **License**: CC-BY-4.0 (Creative Commons Attribution)
- **Update Frequency**: Annual

### Indicators Downloaded

1. **IP.PAT.RESD**: Patent applications, residents
   - Patent applications filed by residents of a country

2. **IP.PAT.NRES**: Patent applications, non-residents
   - Patent applications filed by foreign applicants

3. **Total**: Sum of resident + non-resident applications

## Collection Status

- [✓] Resident patent applications downloaded
- [✓] Non-resident patent applications downloaded
- [✓] Combined dataset created
- [ ] Data quality validated
- [ ] Population normalization applied
- [ ] Integration with WIPO data (if available)

## Data Statistics

- **Total records**: 4,663
- **Countries**: 179
- **Year range**: 1980 - 2021
- **Years covered**: 42
- **Average years per country**: 26.1

### Top 10 Countries by Patents (latest year: 2021)
```
Country                                  Year   Total          
-----------------------------------------------------------------
World                                    2021         3,401,100
China                                    2021         1,585,663
United States                            2021           591,473
Japan                                    2021           289,200
Korea, Rep.                              2021           237,998
India                                    2021            61,573
Germany                                  2021            58,569
Canada                                   2021            37,155
Australia                                2021            32,409
Russian Federation                       2021            30,977
```


## Comparison: World Bank vs WIPO

| Aspect | World Bank | WIPO |
|--------|-----------|------|
| Coverage | 1960-2023 (63 years) | 1883-2023 (140 years) |
| Download | Automated via API ✓ | Manual selection required |
| License | CC-BY-4.0 (explicit) | Public use (attribution) |
| Update | Annual | Annual |
| Best Use | Quick automated baseline | Comprehensive historical analysis |

## Usage Recommendations

### For 1810-1959
- Use WIPO data if available (extends to 1883)
- Extrapolate backward using historical growth rates
- Consider historical patent office records

### For 1960-2023
- **Primary**: WIPO data (more comprehensive)
- **Fallback**: World Bank data (automated, reliable)
- **Validation**: Cross-check WIPO vs World Bank for overlap period

## Citation

```
The World Bank. 2024. World Development Indicators.
Patent applications, residents (IP.PAT.RESD) and non-residents (IP.PAT.NRES).
Available at: https://data.worldbank.org/indicator/IP.PAT.RESD
Accessed: 2025-12-03
License: CC-BY-4.0
```

## Next Steps

1. Download WIPO data for more comprehensive coverage (1883-2023)
2. Compare World Bank vs WIPO for 1960-2023 overlap
3. Integrate with HYDE population data
4. Calculate patents per capita by country-year
5. Normalize to [0, 1] scale
6. Aggregate to global weighted average

## Technical Notes

- World Bank API accessed via Python `requests` library
- Data returned in JSON format, parsed to CSV
- Null values excluded from analysis
- Both resident and non-resident applications captured
- Total calculated as sum of resident + non-resident

---

*This data was downloaded automatically via the World Bank API.*
*For the most comprehensive historical coverage, also download WIPO data manually.*
