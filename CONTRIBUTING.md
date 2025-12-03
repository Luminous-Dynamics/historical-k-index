# Contributing to the Historical K-Index Research Program

Thank you for your interest in contributing to the Historical K-Index Research Program! This document provides guidelines for contributing to this academic research repository.

---

## 🎯 Ways to Contribute

### 1. **Data Improvements**
- Suggest additional data sources for harmonies
- Identify data quality issues
- Contribute temporal extensions (pre-1810 or post-2020)
- Add regional/sub-national data

### 2. **Code Contributions**
- Improve data processing scripts
- Optimize computational performance
- Add visualization tools
- Enhance reproducibility infrastructure

### 3. **Documentation**
- Fix typos or unclear explanations
- Translate documentation
- Add tutorials or examples
- Improve replication guides

### 4. **Research Extensions**
- Propose new research questions (Paper 4+)
- Suggest alternative methodologies
- Contribute validation analyses
- Add robustness tests

### 5. **Bug Reports**
- Report data inconsistencies
- Identify computational errors
- Flag reproducibility issues

---

## 📋 Before You Start

### Read the Documentation
- `README.md` - Project overview
- `shared/docs/REPLICATION_GUIDE.md` - How to replicate results
- `papers/README.md` - Trilogy structure
- `CITATION.cff` - How to cite this work

### Understand the Structure
```
historical-k-index-repo/
├── papers/               # Three papers (trilogy)
│   ├── 01-historical-k-index/
│   ├── 02-regional-divergence/
│   └── 03-temporal-shocks/
├── shared/              # Shared resources
│   ├── data/           # Datasets (gitignored)
│   ├── scripts/        # All Python code
│   └── docs/           # Documentation
└── outputs/            # Generated files
```

### Set Up Your Environment
```bash
# Clone the repository
git clone https://github.com/Luminous-Dynamics/historical-k-index.git
cd historical-k-index

# Enter Nix development environment (recommended)
nix develop

# OR use Poetry directly
poetry install

# Download data
poetry run python shared/scripts/download_all_data.py
```

---

## 🔄 Contribution Workflow

### 1. **Fork and Branch**
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/historical-k-index.git
cd historical-k-index

# Create a feature branch
git checkout -b feature/your-feature-name
```

### 2. **Make Changes**
- Follow existing code style
- Add tests for new functionality
- Update documentation
- Keep commits focused and atomic

### 3. **Test Your Changes**
```bash
# Run data processing
poetry run python shared/scripts/process_all_data.py

# Run validation
poetry run python shared/scripts/validation/validate_k_index.py

# Generate figures (if applicable)
poetry run python shared/scripts/generate_supplementary_figures.py
```

### 4. **Commit with Clear Messages**
```bash
git add .
git commit -m "feat: Add regional breakdown for H₃ reciprocity

- Add sub-national data from XYZ source
- Update processing pipeline
- Add validation tests
- Update documentation"
```

### 5. **Push and Create Pull Request**
```bash
git push origin feature/your-feature-name

# Then create PR on GitHub
```

---

## 📝 Commit Message Guidelines

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring (no behavior change)
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Build process, dependencies

**Examples**:
```bash
feat(h7): Add infrastructure component for evolutionary progression
fix(data): Correct WVS temporal coverage for 2022
docs(readme): Update installation instructions for NixOS
refactor(processing): Optimize K-index computation (30% faster)
```

---

## 🎨 Code Style Guidelines

### Python
- **Style**: Follow PEP 8
- **Formatting**: Use `black` with line length 88
- **Linting**: Use `ruff`
- **Type hints**: Encouraged for public functions
- **Docstrings**: Google style for functions/classes

```python
def compute_harmony_score(
    data: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None
) -> pd.Series:
    """Compute harmony score from component data.
    
    Args:
        data: DataFrame with component columns
        weights: Optional weights dict (defaults to equal weighting)
        
    Returns:
        Series with harmony scores by year
        
    Raises:
        ValueError: If required columns missing
    """
    pass
```

### Documentation
- **Markdown**: Use standard markdown
- **Line length**: 80-100 characters
- **Links**: Use relative paths when possible
- **Code blocks**: Always specify language

---

## 🧪 Testing Guidelines

### Data Validation
All data processing should include:
1. **Input validation**: Check data sources exist and are current
2. **Range checks**: Verify values are reasonable (e.g., indices 0-1)
3. **Temporal coverage**: Confirm years match expectations
4. **Geographic coverage**: Verify country lists

### Example Test
```python
def test_h7_component_ranges():
    """Test H₇ components are in valid ranges."""
    h7_data = pd.read_csv("shared/data/processed/H7_evolutionary_progression.csv")
    
    assert h7_data['h7_score'].between(0, 1).all(), "H₇ scores must be 0-1"
    assert h7_data['year'].min() >= 1996, "H₇ data starts 1996"
    assert h7_data['year'].max() <= 2021, "H₇ data ends 2021"
```

---

## 📊 Data Contribution Guidelines

### Adding New Data Sources
1. **Document provenance**: Add to `shared/docs/DATA_SOURCES.md`
2. **Create download script**: Add to `shared/scripts/data_collection/`
3. **Include validation**: Add checks in processing script
4. **Update replication guide**: Document in `shared/docs/REPLICATION_GUIDE.md`

### Data Quality Standards
- **Completeness**: Document missing data explicitly
- **Accuracy**: Verify against original sources
- **Temporal alignment**: Ensure consistent time periods
- **Geographic consistency**: Use standard country codes (ISO 3166)

### File Naming Conventions
```
raw data: {source}_{indicator}_{temporal_coverage}.csv
processed: {harmony}_component_{start}_{end}.csv
final: k_index_final_{start}_{end}.csv
```

---

## 🔬 Research Contribution Guidelines

### Proposing New Papers (Paper 4+)
1. **Open an issue** describing the research question
2. **Reference existing work**: How does it build on Papers 1-3?
3. **Data requirements**: What new data is needed?
4. **Methodological approach**: Brief overview
5. **Expected contribution**: What's novel?

### Suggesting Methodological Improvements
- Explain the limitation of current approach
- Propose specific alternative
- Provide references if applicable
- Consider backward compatibility

---

## 🚀 Release Process (For Maintainers)

### Creating a New Release
1. **Update version** in relevant files
2. **Update CHANGELOG.md**
3. **Run full validation suite**
4. **Create git tag**: `git tag -a v1.0.0 -m "Release v1.0.0"`
5. **Push tag**: `git push origin v1.0.0`
6. **GitHub Release**: Creates Zenodo DOI automatically

---

## 📄 Licensing

By contributing, you agree that your contributions will be licensed under CC-BY-4.0, the same license as the project.

---

## 🤝 Code of Conduct

### Our Standards
- **Respectful**: Treat all contributors with respect
- **Collaborative**: Work together constructively
- **Scientific**: Prioritize empirical accuracy and honesty
- **Open**: Share knowledge and credit generously

### Unacceptable Behavior
- Harassment or discrimination
- Personal attacks
- Data fabrication or manipulation
- Plagiarism

### Reporting
Email conduct issues to: tristan.stoltz@evolvingresonantcocreationism.com

---

## ❓ Questions?

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Open a GitHub Issue
- **Security concerns**: Email tristan.stoltz@evolvingresonantcocreationism.com
- **Research collaboration**: Email for direct discussion

---

## 🙏 Acknowledgments

Contributors will be acknowledged in:
1. Repository CONTRIBUTORS.md file
2. Paper acknowledgments (for significant contributions)
3. Co-authorship (for major research contributions)

**Contribution criteria for co-authorship**:
- Substantial intellectual contribution
- Active participation in analysis/writing
- Approval of final manuscript

---

Thank you for contributing to advancing our understanding of global coordination capacity! Every contribution, no matter how small, helps make this research more robust and accessible.

**Happy contributing! 🎉**
