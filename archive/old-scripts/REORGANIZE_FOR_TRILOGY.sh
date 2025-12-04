#!/usr/bin/env bash
#
# Reorganize repository for multi-paper trilogy structure
# Implements Option A from FUTURE_ORGANIZATION_PROPOSAL.md
#

set -e

echo "=========================================="
echo "Reorganizing for Trilogy Structure"
echo "=========================================="
echo ""

# Create new structure
echo "📁 Step 1: Create trilogy directory structure"
echo ""

mkdir -p papers/01-historical-k-index/{manuscript,analysis,figures}
mkdir -p papers/02-regional-divergence/{manuscript,analysis,figures}
mkdir -p papers/03-temporal-shocks/{manuscript,analysis,figures}
mkdir -p shared/{data,scripts,docs}

echo "  ✓ Created papers/ structure"
echo "  ✓ Created shared/ structure"

echo ""
echo "📦 Step 2: Move Paper 1 materials"
echo ""

# Move manuscript
mv manuscript/* papers/01-historical-k-index/manuscript/
rmdir manuscript
echo "  ✓ Moved manuscript/ → papers/01-historical-k-index/manuscript/"

# Move paper 1 specific analysis (if any)
if [ -d "analysis" ]; then
    mv analysis/* papers/01-historical-k-index/analysis/ 2>/dev/null || true
    rmdir analysis 2>/dev/null || true
    echo "  ✓ Moved analysis/"
fi

# Note: outputs/figures stays where it is (generated files, gitignored)

echo ""
echo "📂 Step 3: Move shared resources"
echo ""

# Move data to shared (it's already there, just document)
mv data shared/ 2>/dev/null || true
echo "  ✓ Moved data/ → shared/data/"

# Move scripts to shared
mv scripts shared/ 2>/dev/null || true
echo "  ✓ Moved scripts/ → shared/scripts/"

# Move docs to shared
mv docs shared/ 2>/dev/null || true
echo "  ✓ Moved docs/ → shared/docs/"

echo ""
echo "📝 Step 4: Create paper placeholders"
echo ""

# Paper 2 README
cat > papers/02-regional-divergence/README.md << 'PAPER2'
# Paper 2: Regional Divergence in Coordination Capacity

**Status**: Planned for Q2 2026
**Journal Target**: Regional Studies or similar

## Research Question

How do regional coordination capacities diverge, and what explains persistent gaps between developed and developing regions?

## Key Hypotheses

1. **Path Dependency**: Early industrialization creates lock-in effects
2. **Network Effects**: Regional clusters amplify coordination capacity
3. **Colonial Legacy**: Historical extraction patterns predict modern deficits

## Data Requirements

- Same H₁-H₇ framework as Paper 1
- Sub-national data where available
- Regional trade network analysis
- Historical institutional quality measures

## Preliminary Findings

*To be developed after Paper 1 publication*

---

**Dependencies**: 
- Builds on Paper 1 K-index framework
- Uses same shared data sources
- Extends to regional/sub-national analysis
PAPER2

# Paper 3 README
cat > papers/03-temporal-shocks/README.md << 'PAPER3'
# Paper 3: Temporal Shocks and Resilience

**Status**: Planned for Q3 2026
**Journal Target**: Journal of Economic History or similar

## Research Question

How do global shocks (wars, pandemics, financial crises) impact coordination capacity, and which harmonies are most vulnerable?

## Key Hypotheses

1. **Differential Vulnerability**: H₃ (reciprocity) most fragile during crises
2. **Recovery Patterns**: H₅ (knowledge) recovers fastest
3. **Structural Breaks**: Some shocks create permanent shifts

## Data Requirements

- Event study methodology
- High-frequency K(t) estimates
- Shock dating (wars, pandemics, financial crises)
- Country-level resilience metrics

## Preliminary Findings

*To be developed after Paper 1 publication*

---

**Dependencies**:
- Builds on Papers 1-2
- Requires validated K(t) time series
- Uses same shared methodological framework
PAPER3

echo "  ✓ Created papers/02-regional-divergence/README.md"
echo "  ✓ Created papers/03-temporal-shocks/README.md"

echo ""
echo "📋 Step 5: Create papers index"
echo ""

cat > papers/README.md << 'PAPERS_INDEX'
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
PAPERS_INDEX

echo "  ✓ Created papers/README.md"

echo ""
echo "🔧 Step 6: Update repository README"
echo ""

# Update main README to reflect new structure
sed -i 's|├── manuscript/|├── papers/                           # All research papers\n│   ├── 01-historical-k-index/      # Paper 1 (main manuscript)\n│   ├── 02-regional-divergence/     # Paper 2 (planned)\n│   └── 03-temporal-shocks/         # Paper 3 (planned)\n│\n├── shared/                          # Shared resources|g' README.md

echo "  ✓ Updated README.md structure"

echo ""
echo "=========================================="
echo "REORGANIZATION COMPLETE"
echo "=========================================="
echo ""
echo "New structure:"
echo "  papers/"
echo "    ├── 01-historical-k-index/   (Paper 1 - ready for submission)"
echo "    ├── 02-regional-divergence/  (Paper 2 - planned)"
echo "    ├── 03-temporal-shocks/      (Paper 3 - planned)"
echo "    └── README.md"
echo ""
echo "  shared/"
echo "    ├── data/                    (All datasets)"
echo "    ├── scripts/                 (All code)"
echo "    └── docs/                    (All documentation)"
echo ""
echo "Next steps:"
echo "1. Review new structure"
echo "2. Update any hardcoded paths in scripts"
echo "3. Commit reorganization"
echo "4. Create GitHub release for Paper 1"
