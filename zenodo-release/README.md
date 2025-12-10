# Historical K-Index Dataset v1.0.0

## Overview

The K-Index measures humanity's collective capacity for coordination on a 0-1 scale.

**Time Period**: 1996-2020 (25 years)
**Geographic Scope**: Global aggregate
**Update Frequency**: Annual

## The Seven Harmonies

| Harmony | Name | Description |
|---------|------|-------------|
| H1 | Governance | Institutional quality, democracy, rule of law |
| H2 | Interconnection | Trade openness, communication networks |
| H3 | Trust | Social trust, interpersonal cooperation |
| H4 | Complexity | Economic complexity, innovation capacity |
| H5 | Knowledge | Education, human capital development |
| H6 | Wellbeing | Health, life expectancy, quality of life |
| H7 | Technology | Digital infrastructure, tech adoption |

## K-Index Formula

```
K = [H1 × H2 × H3 × H4 × H5 × H6 × H7]^(1/7)
```

The geometric mean ensures that weakness in any single harmony drags down the overall index - coordination requires balance.

## Golden Threshold

**θ = 0.382 = 1/φ²**

Below this threshold, coordination collapse risk increases significantly. Derived from the golden ratio, this represents a critical boundary in complex systems.

## Files Included

- `k_index_1996_2020.csv` - Main K-Index time series with all seven harmonies
- `methodology.md` - Detailed methodology documentation
- `data_sources.md` - Complete list of source datasets
- `.zenodo.json` - Zenodo metadata

## Data Format

```csv
year,k,h1,h2,h3,h4,h5,h6,h7
1996,0.554,0.631,0.735,0.592,0.714,0.482,0.684,0.249
...
2020,0.727,0.825,0.871,0.720,0.796,0.645,0.778,0.517
```

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{stoltz_k_index_2025,
  author = {Stoltz, Tristan},
  title = {Historical K-Index Dataset: Global Coordination Capacity (1996-2020)},
  year = {2025},
  publisher = {Zenodo},
  version = {1.0.0},
  doi = {10.5281/zenodo.XXXXXXX}
}
```

## License

CC-BY-4.0 - You are free to share and adapt this dataset with attribution.

## Interactive Dashboard

Explore the data: https://luminous-dynamics.github.io/historical-k-index/

## Source Code

https://github.com/Luminous-Dynamics/historical-k-index

## Contact

Questions or collaborations: tristan.stoltz@evolvingresonantcocreationism.com
