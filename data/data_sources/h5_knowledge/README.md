# H5: Integral Wisdom / Knowledge Component Data Sources

## Primary Data Source: Barro-Lee Educational Attainment Dataset

### Overview
**Source**: Barro, Robert J. and Jong-Wha Lee (2013), "A New Data Set of Educational Attainment in the World, 1950-2010." *Journal of Development Economics*, vol 104, pp. 184-198.

**Updated**: Lee & Lee (2016) extends coverage to 1870-2010

**Website**: http://www.barrolee.com/

### Dataset Details

**Temporal Coverage**:
- Original: 1950-2010 (5-year intervals)
- Extended: 1870-2010 (5-year intervals for some countries)
- Our target: 1870-2010 for H5 component construction

**Geographic Coverage**:
- 146 countries
- Global aggregates available

**Key Variables**:
1. **Average years of schooling** (age 15+, 25+)
   - Primary schooling years
   - Secondary schooling years
   - Tertiary schooling years
2. **Educational attainment rates** (% of population)
   - No schooling
   - Primary completed
   - Secondary completed
   - Tertiary completed
3. **Literacy rates** (historical estimates)
4. **School enrollment ratios**

### Rationale for H5 Component

**Educational attainment** is a superior proxy for "Integral Wisdom" because:

1. **Wisdom Infrastructure**: Education creates the foundational capacity for knowledge acquisition and synthesis
2. **Cumulative Measure**: Years of schooling reflects accumulated human capital
3. **Broad Coverage**: Available for most countries over long time periods
4. **Strongly Correlated** with:
   - Scientific output
   - Innovation capacity
   - Forecast accuracy
   - Information processing ability

### Data Files in This Directory

- `BLv3.0.dta` - Barro-Lee 3.0 dataset (Stata format)
- `BLv3.0.csv` - Converted to CSV
- `BLv2.2.xls` - Legacy version 2.2 (Excel)
- `README.pdf` - Official documentation from barrolee.com

### Processing Steps

1. **Download**: Get latest version from barrolee.com
2. **Aggregate**: Compute global/regional averages weighted by population
3. **Interpolate**: Fill 5-year gaps to annual data
4. **Normalize**: Scale to 0-1 range relative to theoretical maximum
5. **Extend**: Use literacy estimates for pre-1870 extension to 1810

### Normalization Strategy

**Method**: Normalize years of schooling relative to theoretical maximum

- **Min**: 0 years (1810 baseline)
- **Max**: 15 years (approximate upper limit for average population)
- **Formula**: `H5_normalized = years_of_schooling / 15`

**Alternative** (if using education index):
- Use composite of years of schooling + literacy rate
- Weighted average: 70% schooling years + 30% literacy

### Expected Output

**File**: `data_sources/processed/h5_knowledge_1810_2020.csv`

**Columns**:
- `year` (1810-2020, annual)
- `avg_years_schooling` (raw value)
- `literacy_rate` (0-100%)
- `h5_knowledge_component` (normalized 0-1)
- `notes` (data source/interpolation notes)

**Coverage**: 211 years (1810-2020)

### Citation

If using this data, cite:

```bibtex
@article{barro2013,
  title={A new data set of educational attainment in the world, 1950--2010},
  author={Barro, Robert J and Lee, Jong-Wha},
  journal={Journal of Development Economics},
  volume={104},
  pages={184--198},
  year={2013},
  publisher={Elsevier}
}

@article{lee2016,
  title={Educational attainment for the world population, 1870-2010},
  author={Lee, Jong-Wha and Lee, Hanol},
  journal={mimeo, Korea University},
  year={2016}
}
```

### Data Quality Notes

**Strengths**:
- ✅ Peer-reviewed and widely cited (17,000+ citations)
- ✅ Consistent methodology across countries and time
- ✅ Regular updates (version 3.0 released 2018)
- ✅ Publicly available and reproducible

**Limitations**:
- ⚠️ 5-year intervals (requires interpolation for annual)
- ⚠️ Pre-1870 data sparse (requires literacy estimates)
- ⚠️ Quality varies by country/region
- ⚠️ Doesn't capture education *quality*, only *quantity*

**Validation**:
- Correlates 0.85+ with UNESCO education statistics
- Matches independent literacy estimates from Buringh & Van Zanden (2009)
- Consistent with van Zanden et al. (2014) *How Was Life?*

---

*Last Updated*: November 25, 2025
*Maintainer*: Tristan Stoltz
*Status*: Ready for processing
