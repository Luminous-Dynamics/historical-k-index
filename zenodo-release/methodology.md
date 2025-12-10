# K-Index Methodology

## Overview

The K-Index measures humanity's collective capacity for coordination on a 0-1 scale. It synthesizes seven domain-specific indicators ("harmonies") into a single composite measure using the geometric mean.

## Theoretical Foundation

### Why Geometric Mean?

The K-Index uses geometric mean rather than arithmetic mean:

```
K = [H₁ × H₂ × H₃ × H₄ × H₅ × H₆ × H₇]^(1/7)
```

**Rationale**: Coordination requires balance across all domains. A civilization with excellent technology (H₇ = 0.9) but collapsed trust (H₃ = 0.1) cannot coordinate effectively. The geometric mean ensures that:

1. **Weakness penalizes**: Low values drag down the overall index
2. **Balance rewards**: Even improvement across domains yields higher K
3. **Collapse visible**: If any harmony approaches zero, K approaches zero

### The Golden Threshold

**θ = 0.382 = 1/φ² ≈ 0.382**

This threshold derives from the golden ratio (φ ≈ 1.618) and appears in:
- Complex systems theory (bifurcation points)
- Network science (percolation thresholds)
- Ecological resilience (critical transitions)

Below θ, systems exhibit:
- Increased fragility
- Reduced adaptive capacity
- Higher collapse probability

## Harmony Definitions

### H₁: Governance (0-1)
**Measures**: Institutional quality, democratic participation, rule of law

**Components**:
- Electoral democracy index (V-Dem)
- Liberal democracy index (V-Dem)
- Government effectiveness (World Bank WGI)
- Rule of law (World Bank WGI)
- Control of corruption (World Bank WGI)

**Normalization**: Min-max scaling against theoretical maximum, then averaged

### H₂: Interconnection (0-1)
**Measures**: Trade openness, communication networks, mobility

**Components**:
- Trade (% of GDP) - World Bank
- Foreign direct investment flows
- International tourism arrivals
- Fixed broadband subscriptions (post-1998)
- Mobile cellular subscriptions
- Air transport passengers

**Normalization**: Log-transformed where needed, min-max scaled to 0-1

### H₃: Trust (0-1)
**Measures**: Social trust, interpersonal cooperation, institutional confidence

**Components**:
- Generalized trust (World Values Survey)
- Confidence in institutions (WVS)
- Social cohesion indicators
- Interpersonal safety (homicide rates, inverted)

**Normalization**: Survey data rescaled from typical 0-100 or categorical responses

**Note**: Trust data is sparse before 1981 (first WVS wave). Pre-1981 values are estimated from proxy indicators.

### H₄: Complexity (0-1)
**Measures**: Economic complexity, innovation capacity, productive knowledge

**Components**:
- Economic Complexity Index (Atlas of Economic Complexity)
- Patent applications per capita
- R&D expenditure (% GDP)
- High-technology exports (% manufactured exports)

**Normalization**: ECI rescaled from typical -2 to +2 range

### H₅: Knowledge (0-1)
**Measures**: Education, human capital, information access

**Components**:
- Mean years of schooling (UNDP)
- Expected years of schooling (UNDP)
- Literacy rate
- Tertiary enrollment ratio
- Human Development Index (education component)

**Normalization**: Against theoretical maximum (e.g., 15 years schooling = 1.0)

### H₆: Wellbeing (0-1)
**Measures**: Health, life expectancy, quality of life

**Components**:
- Life expectancy at birth
- Under-5 mortality rate (inverted)
- Maternal mortality ratio (inverted)
- Access to basic sanitation
- Access to electricity

**Normalization**: Life expectancy scaled against 85-year benchmark

### H₇: Technology (0-1)
**Measures**: Technological adoption, digital infrastructure, innovation diffusion

**Components**:
- ICT Development Index (ITU)
- Internet users per 100 people
- Mobile subscriptions per 100 people
- Secure internet servers per million
- Technology Achievement Index (where available)

**Normalization**: Against observed maximum in high-income countries

## Aggregation Method

### Step 1: Component Normalization
Each raw indicator is normalized to 0-1:
```
x_norm = (x - x_min) / (x_max - x_min)
```

For inverted indicators (mortality, etc.):
```
x_norm = 1 - (x - x_min) / (x_max - x_min)
```

### Step 2: Harmony Calculation
Each harmony is the arithmetic mean of its components:
```
H_i = (1/n) × Σ component_j
```

### Step 3: K-Index Calculation
```
K = (H₁ × H₂ × H₃ × H₄ × H₅ × H₆ × H₇)^(1/7)
```

## Data Quality Notes

### Temporal Coverage
- **1996-2020**: High confidence (primary data period)
- **1980-1995**: Moderate confidence (some interpolation)
- **Pre-1980**: Lower confidence (significant estimation)

### Geographic Scope
This dataset provides **global aggregates** weighted by population. Country-level data is available in extended datasets.

### Missing Data Treatment
- Linear interpolation for gaps ≤ 3 years
- Proxy estimation for structural gaps
- Explicit notation in data files

## Validation

### Internal Consistency
- All harmonies positively correlated (expected)
- No harmony dominates (by construction)
- Temporal trends align with historical events

### External Validation
- K dips during known crises (2008, 2020)
- Regional patterns match development literature
- Trends consistent with UN/World Bank assessments

## Limitations

1. **Data availability**: Pre-1980 estimates have higher uncertainty
2. **Survey timing**: Trust data (WVS) collected in waves, not annually
3. **Concept drift**: What "technology" means changes over time
4. **Aggregation loss**: Global aggregates mask regional variation
5. **Normalization choices**: Different scalings yield different K values

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-10 | Initial release (1996-2020) |

## Citation

```bibtex
@dataset{stoltz_k_index_2025,
  author = {Stoltz, Tristan},
  title = {Historical K-Index Dataset: Global Coordination Capacity (1996-2020)},
  year = {2025},
  publisher = {Zenodo},
  version = {1.0.0}
}
```

## Contact

Questions about methodology: tristan.stoltz@evolvingresonantcocreationism.com
