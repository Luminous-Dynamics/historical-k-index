# ⚡ Quick Start Guide

**Get exploring the K-Index in 5 minutes!**

---

## 🎯 What You'll Achieve

By the end of this guide, you'll have:
- ✅ Full repository cloned and environment set up
- ✅ Data downloaded and processed
- ✅ First K-index visualization generated
- ✅ Interactive Jupyter notebook running

**Total time**: ~15 minutes (including downloads)

---

## 📋 Prerequisites

**You need**:
- Git installed
- (Optional but recommended) Nix installed - [Get Nix](https://nixos.org/download.html)
- OR Python 3.11+ and Poetry - [Get Poetry](https://python-poetry.org/docs/#installation)
- 5 GB free disk space
- Stable internet connection

---

## 🚀 Three Paths to Success

Choose the path that matches your system:

### Path A: Nix (Most Reproducible) ⭐ Recommended

```bash
# 1. Clone repository
git clone https://github.com/Luminous-Dynamics/historical-k-index.git
cd historical-k-index

# 2. Enter reproducible environment (downloads dependencies automatically)
nix develop

# 3. Install Python packages
poetry install

# 4. Download data (~2.5 GB, 10-15 min)
poetry run python shared/scripts/download_all_data.py

# 5. Generate your first K-index visualization!
poetry run python shared/scripts/generate_supplementary_figures.py

# Done! Check outputs/figures/ for your plots
```

### Path B: Poetry Only (If No Nix)

```bash
# 1. Clone repository
git clone https://github.com/Luminous-Dynamics/historical-k-index.git
cd historical-k-index

# 2. Install dependencies with Poetry
poetry install

# 3. Download data
poetry run python shared/scripts/download_all_data.py

# 4. Generate visualizations
poetry run python shared/scripts/generate_supplementary_figures.py
```

### Path C: Download Zenodo Package (Fastest)

```bash
# 1. Download complete package from Zenodo (~2.5 GB)
wget https://zenodo.org/record/XXXXXXX/files/historical-k-index-v1.0.0.zip

# 2. Extract
unzip historical-k-index-v1.0.0.zip
cd historical-k-index-repo

# 3. Enter environment
nix develop  # or: poetry install

# 4. Explore! (data already included)
poetry run jupyter notebook notebooks/01_explore_k_index.ipynb
```

---

## 🎓 Your First Analysis

### Generate All Figures (~1 minute)

```bash
poetry run python shared/scripts/generate_supplementary_figures.py
```

**Output**: `outputs/figures/supplementary/`
- `figure_s1_harmony_time_series.png` - All 7 harmonies over time
- `figure_s2_correlation_heatmap.png` - Inter-harmony correlations
- `figure_s3_geographic_distribution.png` - K-index by country
- `figure_s4_robustness_tests.png` - Validation tests

### Launch Interactive Jupyter Notebook

```bash
poetry run jupyter notebook notebooks/01_explore_k_index.ipynb
```

**What's inside**:
- Load and explore K-index data (1810-2020)
- Visualize all seven harmonies
- Analyze structural imbalances (H₃ climate gap)
- Compare countries by coordination capacity
- Identify coordination bottlenecks for policy

**Interactive! Try it yourself:**
- Change countries to analyze
- Modify time periods
- Create your own visualizations
- Propose new research questions

---

## 📊 Understanding the Output

### What is K(t)?

The K-index at time t - global coordination capacity on a 0-1 scale:

```
K(t) = [H₁ × H₂ × H₃ × H₄ × H₅ × H₆ × H₇]^(1/7)
```

Where:
- **H₁**: Governance Coherence (institutions, rule of law)
- **H₂**: Economic Interconnection (trade, finance)
- **H₃**: Cooperative Reciprocity (trust, mutual aid) ⚠️ **Climate bottleneck!**
- **H₄**: Economic Complexity (production sophistication)
- **H₅**: Knowledge Systems (education, innovation)
- **H₆**: Wellbeing Metrics (health, quality of life)
- **H₇**: Evolutionary Progression (infrastructure, development)

### Key Finding: The Structural Imbalance

**Post-1990 growth was unbalanced:**

| Harmony | Growth 1990-2020 | Implication |
|---------|------------------|-------------|
| H₅ (Interconnection) | **35%** | Built digital/trade networks ✅ |
| H₄ (Complexity) | **22%** | Grew economic capacity ✅ |
| H₇ (Evolution) | **18%** | Developed technology ✅ |
| **H₃ (Reciprocity)** | **12%** ⚠️ | **Under-invested in trust** ❌ |

**Why this matters for climate**:
- Climate action requires **trust-intensive cooperation** (H₃)
- We built the wrong infrastructure for the problem we face
- **Policy implication**: Invest in trust, not just technology

---

## 🔬 Common Tasks

### Task 1: Explore Historical Trends

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load K-index time series
df = pd.read_csv('shared/data/processed/K_index_time_series_1810_2020.csv')

# Plot K(t) over time
plt.figure(figsize=(12, 6))
plt.plot(df['year'], df['K_index'], linewidth=2)
plt.title('Global Coordination Capacity 1810-2020')
plt.xlabel('Year')
plt.ylabel('K-Index')
plt.show()
```

### Task 2: Compare Countries

```python
# Load H7 country data
df_h7 = pd.read_csv('shared/data/processed/H7_evolutionary_progression.csv')

# Filter to 2021
df_2021 = df_h7[df_h7['year'] == 2021]

# Top 10 countries
top10 = df_2021.nlargest(10, 'H7')[['country', 'H7']]
print(top10)
```

### Task 3: Identify Bottlenecks

```python
# For a given country, which harmony is lowest?
country_data = {
    'H1': 0.75, 'H2': 0.82, 'H3': 0.58,  # H3 is bottleneck!
    'H4': 0.88, 'H5': 0.81, 'H6': 0.73, 'H7': 0.79
}

bottleneck = min(country_data, key=country_data.get)
print(f"Bottleneck: {bottleneck} = {country_data[bottleneck]:.2f}")
print(f"Policy focus: Strengthen {bottleneck}")
```

---

## 📖 Next Steps: Go Deeper

### Read the Theory

**PARADIGM_SHIFT.md** - Understand the revolutionary framework:
- Why coordination ≠ development
- The climate paradox (tech vs trust)
- Policy implications
- Open research questions

### Explore the Trilogy

**papers/README.md** - The research program:
- Paper 1: K-index foundation (1810-2020) - Ready for submission
- Paper 2: Regional divergence - Planned Q2 2026
- Paper 3: Temporal shocks - Planned Q3 2026

### Contribute

**CONTRIBUTING.md** - Join the research program:
- Report bugs
- Suggest data sources
- Propose Papers 4, 5, 6+
- Improve code/documentation

---

## 🆘 Troubleshooting

### "Data not found" Error

**Problem**: Scripts can't find data files

**Solution**:
```bash
# Download data
poetry run python shared/scripts/download_all_data.py

# Or download from Zenodo (faster)
wget https://zenodo.org/record/XXXXXXX/files/historical-k-index-v1.0.0.zip
```

### "Module not found" Error

**Problem**: Missing Python dependencies

**Solution**:
```bash
# Reinstall dependencies
poetry install

# Or if using Nix
nix develop
poetry install
```

### Slow Downloads

**Problem**: Data downloads taking >30 minutes

**Solution**:
- Use Zenodo package instead (pre-downloaded)
- Or: Run `download_all_data.py --skip-large` to skip biggest files

### Out of Disk Space

**Problem**: Need 5 GB but don't have it

**Solution**:
- Download only processed data (skip raw data)
- Use `--minimal` flag when available
- Or: Use Zenodo's selective download

---

## 💡 Pro Tips

### Tip 1: Use Jupyter for Exploration

Interactive notebooks are the fastest way to explore:
```bash
poetry run jupyter notebook notebooks/01_explore_k_index.ipynb
```

### Tip 2: Start with Processed Data

Don't re-process everything if you don't need to:
- `shared/data/processed/` has analysis-ready datasets
- Skip `download_all_data.py` and `process_all_data.py` if just exploring

### Tip 3: Explore GitHub Issues

See what questions others have asked:
- [Open Issues](https://github.com/Luminous-Dynamics/historical-k-index/issues)
- [Research Proposals](https://github.com/Luminous-Dynamics/historical-k-index/issues?q=label%3Aresearch)

### Tip 4: Join Discussions

Collaborate with other researchers:
- [GitHub Discussions](https://github.com/Luminous-Dynamics/historical-k-index/discussions)
- Share findings, ask questions, propose ideas

---

## 🎉 You're Ready!

**You now have**:
- ✅ Full K-index data (191,913 points)
- ✅ All seven harmonies (1810-2020)
- ✅ Interactive exploration tools
- ✅ Visualization capabilities

**What's possible**:
- 🔬 Analyze historical coordination trends
- 🌍 Compare countries and regions
- 📊 Identify coordination bottlenecks
- 💡 Propose new research questions
- 🤝 Collaborate on Papers 4+

---

## 🌟 Quick Reference

| Task | Command |
|------|---------|
| **Enter environment** | `nix develop` |
| **Install packages** | `poetry install` |
| **Download data** | `poetry run python shared/scripts/download_all_data.py` |
| **Generate figures** | `poetry run python shared/scripts/generate_supplementary_figures.py` |
| **Launch Jupyter** | `poetry run jupyter notebook` |
| **Run tests** | `poetry run pytest tests/` |
| **View docs** | Open `README.md`, `PARADIGM_SHIFT.md`, `FAQ.md` |

---

## 📧 Need Help?

**Got stuck? Have questions?**

- **FAQ**: Check `FAQ.md` for common questions
- **Issues**: [Report bugs or ask questions](https://github.com/Luminous-Dynamics/historical-k-index/issues)
- **Discussions**: [Join research conversations](https://github.com/Luminous-Dynamics/historical-k-index/discussions)
- **Email**: tristan.stoltz@evolvingresonantcocreationism.com

---

**Welcome to the coordination revolution!** 🚀

*"Global coordination is humanity's superpower. By measuring it, we can improve it."*

**Next**: Open `PARADIGM_SHIFT.md` to understand the theoretical breakthrough, or launch `notebooks/01_explore_k_index.ipynb` to start exploring data!
