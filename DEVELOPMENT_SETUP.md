# Development Environment Setup

**Project:** Historical K(t) Index
**Approach:** Nix Flakes + Poetry (Hybrid Best-of-Both-Worlds)
**Status:** Production-Ready Reproducible Environment

---

## 🎯 Why Flake + Poetry?

This project uses a **pragmatic hybrid approach** combining the best of both ecosystems:

- **Nix Flakes:** System-level dependencies (GDAL, GEOS, compilers, etc.)
- **Poetry:** Python package management (pandas, numpy, scipy, etc.)

### Advantages

✅ **Reproducibility:** Nix ensures identical system dependencies everywhere
✅ **Simplicity:** Poetry handles Python packages without poetry2nix complexity
✅ **Speed:** Faster iteration on Python deps (no Nix rebuild)
✅ **Reliability:** Always works (no poetry2nix evaluation errors)
✅ **Familiar:** Use standard Poetry workflow

---

## 🚀 Quick Start

### First Time Setup
```bash
cd /srv/luminous-dynamics/historical-k-index

# Enter Nix development environment
nix develop

# Install Python dependencies
poetry install

# Verify installation
poetry run python --version
poetry run python -c "import pandas; print('pandas:', pandas.__version__)"
```

### Daily Workflow
```bash
# Enter environment
nix develop

# Run scripts directly
poetry run python scripts/data_collection/01_download_wipo_patents.py

# Or enter Poetry shell for interactive work
poetry shell
python scripts/data_collection/01_download_wipo_patents.py
```

---

## 📦 What's Included

### System Dependencies (via Nix)
- Python 3.11
- Poetry 2.2+
- GCC compiler
- Geospatial libraries (GDAL, GEOS, PROJ)
- Scientific computing (HDF5, NetCDF)

### Python Packages (via Poetry)
**Core Data Processing:**
- pandas ^2.0
- numpy ^1.24
- scipy ^1.11

**Statistical Analysis:**
- statsmodels ^0.14

**Visualization:**
- matplotlib ^3.7
- seaborn ^0.12

**Geospatial:**
- geopandas ^0.13
- shapely ^2.0

**Development Tools:**
- pytest ^7.4
- black ^23.7
- ruff ^0.0.285
- mypy ^1.5

---

## 🔧 Common Commands

### Environment Management
```bash
# Enter development environment
nix develop

# Enter CI environment (minimal, fast)
nix develop .#ci

# Update flake inputs
nix flake update

# Check flake structure
nix flake show
```

### Poetry Operations
```bash
# Install dependencies
poetry install

# Add new package
poetry add requests

# Add development dependency
poetry add --group dev pytest

# Update dependencies
poetry update

# Show installed packages
poetry show

# Run a script
poetry run python script.py

# Enter virtual environment
poetry shell
```

### Data Collection Scripts
```bash
# Option 1: Using poetry run
poetry run python scripts/data_collection/01_download_wipo_patents.py

# Option 2: Using Poetry shell
poetry shell
python scripts/data_collection/01_download_wipo_patents.py

# Option 3: Using Poetry scripts (if configured)
poetry run download-wipo
```

---

## 📁 File Structure

```
historical-k-index/
├── flake.nix                   # Nix flake for system dependencies
├── flake.lock                  # Locked Nix dependencies
├── pyproject.toml              # Poetry configuration
├── poetry.lock                 # Locked Python dependencies
├── .venv/                      # Poetry virtual environment (created on install)
├── scripts/
│   └── data_collection/        # Data collection scripts
├── data/
│   ├── raw/                    # Raw downloaded data
│   └── processed/              # Processed data
└── tests/                      # Test suite
```

---

## 🔍 Troubleshooting

### "Command not found: poetry"
**Solution:** You're not in the Nix environment. Run `nix develop` first.

### "Module not found" errors
**Solution:** Install Python dependencies:
```bash
nix develop
poetry install
```

### Poetry virtual environment issues
**Solution:** Remove and recreate:
```bash
rm -rf .venv
poetry install
```

### System library issues (GDAL, GEOS, etc.)
**Solution:** These are managed by Nix. Make sure you're in `nix develop`.

### Slow Poetry install
**Solution:** This is normal on first run (compiling geospatial packages). Subsequent runs are fast.

---

## 🎓 Advanced Usage

### Adding a New Python Dependency

```bash
# Enter environment
nix develop

# Add package
poetry add scikit-learn

# Verify
poetry show scikit-learn

# Use in scripts
poetry run python -c "import sklearn; print(sklearn.__version__)"
```

### Adding a New System Dependency

Edit `flake.nix`:
```nix
buildInputs = with pkgs; [
  pythonEnv
  poetry

  # Add your new system package here
  postgresql
];
```

Then:
```bash
# Rebuild environment
nix develop
```

### Running Tests

```bash
nix develop
poetry run pytest tests/
```

### Code Formatting

```bash
# Auto-format with Black
poetry run black scripts/

# Lint with Ruff
poetry run ruff check scripts/

# Type check with MyPy
poetry run mypy scripts/
```

---

## 📊 CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: cachix/install-nix-action@v22
        with:
          extra_nix_config: |
            experimental-features = nix-command flakes
      - run: nix develop .#ci --command poetry install
      - run: nix develop .#ci --command poetry run pytest
```

---

## 🌊 Best Practices

### For Development
1. Always start with `nix develop`
2. Use `poetry install` after pulling changes
3. Add new Python deps via `poetry add`, not pip
4. Test in clean environment occasionally: `rm -rf .venv && poetry install`

### For Collaboration
1. Commit `flake.lock` and `poetry.lock` to git
2. Update lockfiles with `nix flake update` and `poetry update`
3. Document any new system dependencies in README

### For Reproducibility
1. Don't modify system Python packages outside Nix
2. Don't use pip install globally
3. Keep all Python deps in `pyproject.toml`
4. Keep all system deps in `flake.nix`

---

## 🎯 Comparison: Traditional vs Hybrid Approach

| Aspect | Traditional (venv) | poetry2nix | **Hybrid (This Project)** |
|--------|-------------------|------------|---------------------------|
| System deps | Manual install | Nix managed | ✅ Nix managed |
| Python deps | pip/poetry | Nix | ✅ Poetry |
| Reproducibility | Poor | Excellent | ✅ Excellent |
| Iteration speed | Fast | Slow (rebuild) | ✅ Fast |
| Complexity | Low | High | ✅ Medium |
| Reliability | Medium | Flaky | ✅ High |

---

## 📚 Learn More

**Nix Flakes:**
- https://nixos.wiki/wiki/Flakes
- https://zero-to-nix.com/concepts/flakes

**Poetry:**
- https://python-poetry.org/docs/
- https://python-poetry.org/docs/basic-usage/

**Hybrid Approach:**
- See `/srv/luminous-dynamics/11-meta-consciousness/luminous-nix/POETRY2NIX_INTEGRATION.md`
- Example from Luminous Nix project (successfully using this approach)

---

## ✅ Verification

### Check System Dependencies (Nix)
```bash
nix develop --command bash -c "which python && which poetry && which gcc"
```

### Check Python Environment (Poetry)
```bash
nix develop --command poetry run python -c "
import pandas
import numpy
import geopandas
print('All imports successful!')
print(f'pandas: {pandas.__version__}')
print(f'numpy: {numpy.__version__}')
print(f'geopandas: {geopandas.__version__}')
"
```

### Run Test Script
```bash
nix develop --command poetry run python scripts/data_collection/01_download_wipo_patents.py
```

---

**Environment Status:** ✅ Production Ready
**Reproducibility:** ✅ Fully Reproducible
**Performance:** ✅ Fast Iteration
**Maintenance:** ✅ Easy to Update

🌊 **Ready to collect H₇ component data!**
