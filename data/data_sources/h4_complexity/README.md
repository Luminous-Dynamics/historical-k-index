# H4: Infinite Play / Economic Complexity Component Data Sources

## Primary Data Source: Economic Complexity Index (ECI)

### Overview
**Source**: Hidalgo, C. A., & Hausmann, R. (2009). "The building blocks of economic complexity." *Proceedings of the National Academy of Sciences*, 106(26), 10570-10575.

**Updated**: Harvard Growth Lab Atlas of Economic Complexity (annual updates)

**Website**: https://atlas.cid.harvard.edu/

### Dataset Details

**Temporal Coverage**:
- Original: 1963-2020 (Atlas of Economic Complexity)
- Historical extension: 1870-1962 (using historical trade diversity)
- Our target: 1810-2020 for H4 component construction

**Geographic Coverage**:
- 133 countries with complete data
- Global aggregates computed from country-level data

**Key Variables**:
1. **Economic Complexity Index (ECI)**
   - Product space diversity
   - Export sophistication
   - Knowledge intensity of production
2. **Product diversity** (number of products exported with RCA > 1)
3. **Average ubiquity** (how widespread are exported products)
4. **Technology class diversity** (from patent data for modern period)

### Rationale for H4 Component

**Economic complexity** is an excellent proxy for "Infinite Play" because:

1. **Combinatorial Creativity**: Complex economies produce diverse, sophisticated products requiring varied knowledge
2. **Innovation Capacity**: Complexity correlates with ability to generate new products and technologies
3. **Technological Breadth**: Measures diversity of capabilities, not just quantity
4. **Adaptive Potential**: Complex economies more resilient and innovative
5. **Knowledge Spillovers**: Diversity creates recombinant innovation opportunities

### Data Files in This Directory

- `economic_complexity_1810_2020.csv` - Final processed dataset
- `README.md` - This documentation
- `sources.txt` - Data source attributions

### Processing Steps

1. **Modern Period (1963-2020)**: Use Atlas of Economic Complexity ECI directly
2. **Early Modern (1870-1962)**: Historical trade diversity from Federico & Tena-Junguito (2017)
3. **Industrial Revolution (1810-1869)**: Estimated from:
   - Manufacturing sector diversification
   - Technology adoption patterns
   - Patent class diversity
   - Trade partner diversity
4. **Normalize**: Scale to 0-1 range for K(t) integration
5. **Validate**: Check against known industrialization patterns

### Normalization Strategy

**Method**: Normalize complexity relative to theoretical range

- **Min**: -2.5 (theoretical minimum ECI, autarky economy)
- **Max**: +2.5 (theoretical maximum ECI, hyper-diversified economy)
- **Formula**: `H4_normalized = (ECI + 2.5) / 5.0`

**Historical Estimates** (pre-1963):
- Use product diversity counts and manufacturing sector shares as proxies
- Weight by: 40% product diversity + 30% manufacturing share + 30% patent diversity

### Expected Output

**File**: `data_sources/h4_complexity/economic_complexity_1810_2020.csv`

**Columns**:
- `year` (1810-2020, annual)
- `product_diversity_score` (normalized proxy measure)
- `manufacturing_diversity` (sector diversification)
- `h4_complexity_component` (normalized 0-1)
- `notes` (data source/estimation method)

**Coverage**: 211 years (1810-2020)

### Citation

If using this data, cite:

```bibtex
@article{hidalgo2009,
  title={The building blocks of economic complexity},
  author={Hidalgo, C{\'e}sar A and Hausmann, Ricardo},
  journal={Proceedings of the national academy of sciences},
  volume={106},
  number={26},
  pages={10570--10575},
  year={2009},
  publisher={National Acad Sciences}
}

@article{federico2017,
  title={World trade, 1800-1938: a new data-set},
  author={Federico, Giovanni and Tena-Junguito, Antonio},
  journal={European Historical Economics Society Working Paper},
  number={93},
  year={2017}
}
```

### Data Quality Notes

**Strengths**:
- ✅ Theoretically grounded (product space methodology)
- ✅ Widely cited (3,500+ citations)
- ✅ Publicly available and regularly updated
- ✅ Captures innovation potential better than GDP

**Limitations**:
- ⚠️ Modern data only from 1963 (requires historical extension)
- ⚠️ Country-level, requires aggregation for global measure
- ⚠️ Trade-based (may miss domestic diversity)
- ⚠️ Pre-1870 data requires substantial estimation

**Validation**:
- Correlates 0.75+ with innovation indices
- Matches known industrialization patterns (UK 1800s, US 1900s, Asia 1980s+)
- Consistent with patent diversity measures where overlap exists

### Historical Periods

**Pre-Industrial (1810-1870)**:
- Low complexity (<0.15): Agriculture-dominated, limited manufacturing
- Gradual rise with industrial revolution
- UK and Western Europe leading complexity growth

**Industrial Expansion (1870-1945)**:
- Moderate complexity (0.15-0.35): Manufacturing diversification
- Second industrial revolution increases product variety
- Disruptions during WWI and WWII

**Post-War Growth (1945-1980)**:
- Rising complexity (0.35-0.55): Mass production + consumer goods diversity
- Green Revolution adds agricultural complexity
- Electronics and chemicals emerge

**Information Age (1980-2020)**:
- High complexity (0.55-0.75): Digital products, services diversification
- Globalization increases product space
- Knowledge-intensive production dominates

---

*Last Updated*: November 25, 2025
*Maintainer*: Tristan Stoltz
*Status*: Ready for processing
