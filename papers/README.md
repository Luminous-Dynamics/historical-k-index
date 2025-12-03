# Historical K-Index Research Program: Papers

This directory contains all papers in the K-index research trilogy.

---

## Overview

The Historical K-Index research program explores global coordination capacity through a trilogy of papers:

1. **Foundation** (1810-2020): Establishes K-index framework and validates H₇
2. **Regional Divergence**: Analyzes coordination gaps across regions
3. **Temporal Shocks**: Examines crisis impacts and resilience patterns

---

## Paper Status

| Paper | Status | Journal Target | Expected Submission |
|-------|--------|----------------|---------------------|
| Paper 1: Foundation | 95% ready | Nature Sustainability | Dec 2025 |
| Paper 2: Regional Divergence | Planning | Regional Studies | Q2 2026 |
| Paper 3: Temporal Shocks | Planned | J. Economic History | Q3 2026 |

---

## Shared Resources

All papers use shared resources in `../shared/`:

- **Data**: Complete 1810-2020 dataset (191,913 points)
- **Scripts**: Data collection, processing, analysis
- **Documentation**: Methodology, replication guides

---

## Organization

Each paper has its own directory:

```
papers/
├── 01-historical-k-index/
│   ├── manuscript/           # LaTeX source + PDFs
│   ├── analysis/             # Paper-specific analysis
│   └── figures/              # Paper-specific figures
│
├── 02-regional-divergence/
│   ├── manuscript/
│   ├── analysis/
│   └── figures/
│
└── 03-temporal-shocks/
    ├── manuscript/
    ├── analysis/
    └── figures/
```

---

## Adding a New Paper

1. Create directory: `papers/04-paper-name/`
2. Create subdirectories: `manuscript/`, `analysis/`, `figures/`
3. Add README.md describing research question
4. Update this index

---

## Citation

Each paper has its own DOI. Cite the overall program as:

```bibtex
@misc{stoltz2025kindex_program,
  author = {Stoltz, Tristan},
  title = {Historical K-Index Research Program},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/Luminous-Dynamics/historical-k-index}
}
```

For individual papers, see their respective CITATION.cff files.
