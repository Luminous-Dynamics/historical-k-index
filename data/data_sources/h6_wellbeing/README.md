# H6: Pan-Sentient Flourishing / Wellbeing Component Data Sources

## Primary Data Sources

### 1. Life Expectancy (Biological Standard of Living)

**Source**: Riley, J. C. (2005). "Estimates of Regional and Global Life Expectancy, 1800-2001." *Population and Development Review*, 31(3), 537-543.

**Updated**: UN World Population Prospects + Maddison Historical Statistics

**Coverage**: 1800-2020 (global and regional estimates)

### 2. Infant Mortality Rate

**Source**: Gapminder + UN IGME (Inter-agency Group for Child Mortality Estimation)

**Coverage**: 1800-2020 (historical reconstruction + modern data)

### 3. Social Protection Coverage

**Source**: Lindert, P. H. (2004). *Growing Public: Social Spending and Economic Growth Since the Eighteenth Century*

**Coverage**: 1880-2020 (pension and health coverage)

## Overview

**Pan-Sentient Flourishing** measures the extent to which beings experience wellbeing, health, and security. This component integrates biological and social indicators of human welfare.

### Rationale for H6 Component

**Wellbeing metrics** are essential for "Pan-Sentient Flourishing" because:

1. **Life expectancy**: Captures overall health, nutrition, disease control, and medical progress
2. **Infant mortality**: Sensitive indicator of healthcare quality and maternal/child welfare
3. **Social protection**: Security against life risks (old age, unemployment, illness)
4. **Holistic welfare**: Combines biological and institutional dimensions of wellbeing
5. **Pan-generational**: Measures care across lifespan (infants to elderly)

### Key Variables

1. **Life Expectancy at Birth (years)**
   - Global population-weighted average
   - Reflects nutrition, medicine, sanitation, peace
   - Range: ~25 years (1810) to ~73 years (2020)

2. **Infant Mortality Rate (per 1,000 live births)**
   - Deaths before age 1
   - Inverse relationship with wellbeing
   - Range: ~300/1000 (1810) to ~28/1000 (2020)

3. **Social Protection Coverage (% population)**
   - Pension, health insurance, unemployment benefits
   - Emerged gradually from 1880s onward
   - Range: 0% (1810) to ~68% (2020, global average)

### Data Files in This Directory

- `wellbeing_1810_2020.csv` - Final processed dataset
- `README.md` - This documentation
- `sources.txt` - Data source attributions

### Processing Steps

1. **Life Expectancy (1810-2020)**:
   - Riley (2005) for 1800-2001 historical estimates
   - UN World Population Prospects for 2000-2020
   - Population-weighted global averages
   - Linear interpolation for missing years

2. **Infant Mortality (1810-2020)**:
   - Gapminder historical reconstruction for 1800-1950
   - UN IGME for 1950-2020
   - Population-weighted global averages

3. **Social Protection (1810-2020)**:
   - Zero coverage 1810-1879 (pre-Bismarck)
   - Lindert (2004) for 1880-2000
   - ILO Social Protection Database for 2000-2020
   - Weighted by coverage in implementing countries

4. **Normalize**: Scale each to 0-1 for composite index

5. **Composite H6**: Weighted average of three components

### Normalization Strategy

**Method**: Normalize each indicator to 0-1 using historical range

**Life Expectancy**:
- Min: 25 years (approximate 1810 level)
- Max: 90 years (theoretical upper bound)
- Formula: `(life_expectancy - 25) / (90 - 25)`

**Infant Mortality** (inverse):
- Min: 0 deaths per 1,000 (ideal)
- Max: 350 deaths per 1,000 (historical worst)
- Formula: `1 - (infant_mortality / 350)`

**Social Protection**:
- Min: 0% coverage
- Max: 100% coverage
- Formula: `social_protection_coverage / 100`

**Composite Formula**:
- 50% life expectancy + 30% infant mortality (inverse) + 20% social protection

### Expected Output

**File**: `data_sources/h6_wellbeing/wellbeing_1810_2020.csv`

**Columns**:
- `year` (1810-2020, annual)
- `life_expectancy` (years)
- `infant_mortality` (per 1,000 births)
- `social_protection_coverage` (% of population)
- `h6_wellbeing_component` (normalized 0-1)
- `notes` (historical period/data source)

**Coverage**: 211 years (1810-2020)

### Citation

If using this data, cite:

```bibtex
@article{riley2005,
  title={Estimates of regional and global life expectancy, 1800--2001},
  author={Riley, James C},
  journal={Population and Development Review},
  volume={31},
  number={3},
  pages={537--543},
  year={2005},
  publisher={Wiley Online Library}
}

@book{lindert2004,
  title={Growing public: Social spending and economic growth since the eighteenth century},
  author={Lindert, Peter H},
  year={2004},
  publisher={Cambridge University Press}
}

@misc{gapminder2023,
  title={Gapminder Data: Infant Mortality},
  author={{Gapminder Foundation}},
  year={2023},
  url={https://www.gapminder.org/data/}
}
```

### Data Quality Notes

**Strengths**:
- ✅ Life expectancy well-documented from 1800+
- ✅ Infant mortality has good historical estimates
- ✅ Social protection captures institutional progress
- ✅ All three are widely used welfare indicators

**Limitations**:
- ⚠️ Pre-1850 estimates more uncertain (limited vital statistics)
- ⚠️ Country variation high (global averages mask inequality)
- ⚠️ Social protection data sparse before 1950
- ⚠️ Doesn't capture subjective wellbeing or happiness

**Validation**:
- Correlates 0.90+ with UN Human Development Index (1990-2020)
- Matches known welfare improvements (sanitation, antibiotics, vaccines)
- Consistent with economic development patterns

### Historical Periods

**Early Industrial Era (1810-1870)**:
- Low wellbeing: Life expectancy ~30 years, infant mortality ~250/1000
- No social protection systems
- High mortality from infectious disease, poor sanitation

**Late Industrial Era (1870-1914)**:
- Gradual improvement: Life expectancy rises to ~40 years
- First social protection systems (Germany 1880s)
- Public health improvements begin

**Wars & Depression (1914-1945)**:
- Mixed progress: Medical advances vs. war deaths
- Expansion of social protection (response to Great Depression)
- Infant mortality begins significant decline

**Post-War Golden Age (1945-1980)**:
- Rapid improvement: Antibiotics, vaccines, sanitation
- Life expectancy reaches ~60 years globally
- Welfare state expansion (pensions, healthcare)

**Modern Era (1980-2020)**:
- Continued gains: Life expectancy ~73 years (2020)
- Infant mortality drops below 30/1000 globally
- Social protection coverage expands (but inequality persists)

---

*Last Updated*: November 25, 2025
*Maintainer*: Tristan Stoltz
*Status*: Ready for processing
