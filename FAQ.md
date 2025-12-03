# Frequently Asked Questions (FAQ)

## General Questions

### What is the K-Index?

The K-index is a comprehensive measure of **global coordination capacity** - humanity's ability to cooperate at planetary scale. It integrates seven fundamental dimensions (harmonies) into a single metric ranging from 0 to 1.

**Think of it as**: "GDP measures our ability to produce. K-index measures our ability to coordinate."

### Why do we need a new metric? Isn't GDP enough?

**Short answer**: GDP measures individual prosperity. K-index measures collective capability.

**Long answer**: The 21st century's biggest challenges (climate change, pandemics, AI governance) are fundamentally **coordination problems**, not production problems. We have the wealth, technology, and knowledge to solve them - but we struggle to coordinate action. The K-index helps diagnose where coordination breaks down.

### How is this different from the Human Development Index (HDI)?

| Metric | Focus | Question |
|--------|-------|----------|
| **GDP** | Economic output | How much do we produce? |
| **HDI** | Individual wellbeing | How well do individuals live? |
| **K-Index** | Collective coordination | How capable are we of cooperating? |

**Key difference**: HDI measures individual capabilities. K-index measures the **infrastructure for collective action**.

---

## Methodology Questions

### What are the Seven Harmonies?

1. **H₁: Governance Coherence** - Institutional quality, rule of law
2. **H₂: Economic Interconnection** - Trade, financial integration
3. **H₃: Cooperative Reciprocity** - Trust, mutual aid, social capital
4. **H₄: Economic Complexity** - Production sophistication
5. **H₅: Knowledge Systems** - Education, innovation
6. **H₆: Wellbeing Metrics** - Health, quality of life
7. **H₇: Evolutionary Progression** - Infrastructure, development trajectory

Each harmony represents a critical dimension of coordination capacity.

### Why use geometric mean instead of arithmetic mean?

**Critical design choice!**

Geometric mean: K(t) = [H₁ × H₂ × H₃ × H₄ × H₅ × H₆ × H₇]^(1/7)

**Why?** Because coordination requires **balance**.

- High technology (H₇ = 0.9) cannot compensate for low trust (H₃ = 0.3)
- All seven harmonies must be present for effective coordination
- The geometric mean enforces this: **the weakest link determines capacity**

**Example**:
- Arithmetic mean: [0.9 + 0.9 + 0.3 + 0.9 + 0.9 + 0.9 + 0.9] / 7 = 0.81 ❌ (misleading)
- Geometric mean: [0.9 × 0.9 × 0.3 × 0.9 × 0.9 × 0.9 × 0.9]^(1/7) = 0.75 ✅ (reflects bottleneck)

### How reliable is the K-Index?

**Empirical validation**:
- Correlates r = 0.98 with log(GDP per capita) (p < 10⁻¹⁴⁹)
- Correlates r = 0.82 with life expectancy (p < 10⁻¹¹²)
- Correlates r = 0.70 with HDI (p < 10⁻⁸⁷)

**Historical validity**:
- Correctly identifies coordination crises (WWI, WWII)
- Tracks known coordination improvements (post-war globalization)

**Conservative estimation**:
- Validated H₇ yields **-7.0% lower K(t)** than proxies (demonstrates rigor)

---

## Data Questions

### Where does the data come from?

**All open-access sources**:
- World Values Survey (H₃ reciprocity)
- V-Dem Institute (H₁ governance)
- World Bank WDI/WGI (H₂, H₆, H₇)
- WIPO (H₅ innovation)
- Atlas of Economic Complexity (H₄)

**Complete provenance**: See `shared/docs/DATA_SOURCES.md`

### Can I access the data?

**Three ways**:

1. **Zenodo**: Download complete package (~2.5 GB) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

2. **Download script**:
   ```bash
   poetry run python shared/scripts/download_all_data.py
   ```

3. **Individual sources**: Manual download (see DATA_SOURCES.md)

**Note**: Data excluded from Git due to size (GitHub 100 MB limit).

### Why isn't the data in the GitHub repo?

**GitHub file size limits**: 100 MB maximum per file.

**Our data**:
- World Values Survey: 1.3 GB
- V-Dem dataset: 195 MB
- Plus 6 other sources

**Solution**:
- Code/docs in Git (~10 MB)
- Data via Zenodo (~2.5 GB complete package)
- Best of both worlds: version control + full replication

### How much data is there?

**191,913 total data points** across:
- 210 years (1810-2020)
- 159 countries (for H₇ component)
- 7 harmonies
- Multiple indicators per harmony

**Key dataset**: 2,352 validated H₇ observations (159 countries, 1996-2021)

---

## Research Questions

### What's the trilogy structure?

**Three interconnected papers**:

| Paper | Focus | Status | Journal Target |
|-------|-------|--------|----------------|
| **Paper 1** | K-index framework 1810-2020 | 95% ready | Nature Sustainability |
| **Paper 2** | Regional divergence | Planning | Regional Studies |
| **Paper 3** | Temporal shocks & resilience | Planned | J. Economic History |

**Shared infrastructure**: All papers use same data + code base.

### Can I propose Paper 4?

**Absolutely!** We welcome research extensions.

**Process**:
1. Open a GitHub Issue using "Research Proposal" template
2. Describe your research question and methodology
3. Discuss collaboration and resources
4. If approved, add to research roadmap

**Criteria**: Novel question, sound methodology, builds on K-index framework.

### How do I cite this work?

**For the research program**:
```bibtex
@misc{stoltz2025k_index_program,
  author = {Stoltz, Tristan},
  title = {Historical K-Index Research Program},
  year = {2025},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.XXXXXXX}
}
```

**Automated**: See `CITATION.cff` (GitHub renders automatically)

---

## Technical Questions

### What are the computational requirements?

**Minimal** (reproduce results):
- RAM: 4 GB
- Storage: 2 GB
- Time: ~6 minutes

**Full pipeline** (download + process):
- RAM: 8 GB recommended
- Storage: 5 GB
- Time: ~15 minutes (first run)

**Environment**: Nix flake ensures exact reproducibility across systems.

### Why use Nix + Poetry?

**Reproducibility**!

- **Nix**: Manages system dependencies (Python, libraries, compilers)
- **Poetry**: Manages Python packages
- **Result**: Exact same versions on any machine (Linux, macOS, NixOS)

**Alternative**: Can use Poetry alone if Nix unavailable (less reproducible).

### I found a bug. What should I do?

**Please report it!**

1. Open GitHub Issue using "Bug Report" template
2. Include:
   - Steps to reproduce
   - Error message
   - Your environment (OS, Python version)
3. We'll investigate and fix

**Or**: Submit a Pull Request with fix (see CONTRIBUTING.md)

---

## Policy & Impact Questions

### What are the policy implications?

**Key insight**: Climate crisis is a **coordination crisis**, not a technology crisis.

**Evidence**:
- Technology (H₇) grew 18% (1990-2020)
- Cooperation (H₃) grew only 12%
- **Climate action requires high H₃** (trust-intensive cooperation)

**Policy shift**:
From "invest $100B in green tech R&D"
To "invest $50B in green tech + $50B in trust infrastructure"

**Why?** Technology without trust = stalled coordination.

### How can this inform climate policy?

**Diagnostic framework**:
1. Measure K(t) by country/region
2. Identify bottleneck harmony (often H₃)
3. Design interventions targeting bottleneck
4. Monitor K(t) improvement

**Example**:
- Country X: H₃ (trust) = 0.55 (low)
- Intervention: Community-level climate forums, shared benefit mechanisms
- Outcome: H₃ ↑ → K(t) ↑ → Better climate coordination

### Could this be used for other global challenges?

**Yes!** The K-index framework applies to:

- **Pandemic preparedness**: Requires high H₃ (international cooperation)
- **AI governance**: Requires high H₁ (institutional quality) and H₃ (trust)
- **Nuclear nonproliferation**: Requires high H₃ (reciprocity)
- **Financial stability**: Requires high H₂ (interconnection) and H₁ (governance)

**Principle**: Any challenge requiring global coordination can be analyzed through K-index lens.

---

## Contribution Questions

### How can I contribute?

**Five ways**:

1. **Report bugs**: Use GitHub Issues
2. **Suggest data sources**: Use "Data Contribution" template
3. **Propose research**: Use "Research Proposal" template
4. **Improve code**: Submit Pull Requests
5. **Spread the word**: Share with colleagues

**See**: `CONTRIBUTING.md` for complete guidelines

### I'm not a coder. Can I still contribute?

**Absolutely!** Many valuable contributions don't require coding:

- **Data expertise**: Identify new data sources
- **Domain knowledge**: Suggest research directions
- **Communication**: Write tutorials, create visualizations
- **Translation**: Translate documentation
- **Feedback**: Report clarity issues in documentation

**All contributions welcome!**

### What's the collaboration philosophy?

**Open science principles**:
- Full transparency and reproducibility
- Collaborative over competitive
- Credit generously shared
- Community-driven research program

**Co-authorship criteria** (see CONTRIBUTING.md):
- Substantial intellectual contribution
- Active participation in analysis/writing
- Approval of final manuscript

---

## Philosophical Questions

### Is this just rebranding existing development metrics?

**No - fundamentally different paradigm.**

**Old paradigm**: Progress = individual capabilities (GDP, HDI)
**New paradigm**: Progress = collective coordination capacity (K-index)

**Example of the difference**:
- High GDP, low trust = Fragile coordination (climate inaction)
- Moderate GDP, high trust = Effective coordination (Nordic climate leadership)

**K-index reveals what GDP misses**: The infrastructure for cooperation.

### Isn't "coordination capacity" too abstract?

**It's actually very concrete:**

**Low coordination capacity** = Can't coordinate on:
- International climate treaties
- Pandemic response protocols
- Shared technology governance
- Equitable resource distribution

**High coordination capacity** = Can effectively:
- Implement Paris Agreement
- Respond to global health threats
- Govern AI development
- Manage shared resources (oceans, atmosphere)

**K-index quantifies this**: From abstract concept to measurable variable.

### What's the vision for this research program?

**Short-term (2025-2026)**: Complete trilogy (Papers 1-3)

**Medium-term (2027-2029)**:
- Community-driven extensions (Papers 4+)
- Interactive K-index dashboard
- Policy pilot programs

**Long-term (2030+)**:
- K-index as standard metric (like GDP, HDI)
- Used by UN, World Bank, policymakers
- Quarterly updates tracking global coordination

**Ultimate vision**: Build the knowledge infrastructure for planetary coordination.

---

## Getting Started

### I'm new to this. Where should I start?

**5-minute quickstart**:
1. Read `README.md` (overview)
2. Explore `notebooks/01_explore_k_index.ipynb` (interactive)
3. Check `PARADIGM_SHIFT.md` (theory)

**Going deeper**:
4. Read Paper 1 manuscript
5. Run replication scripts
6. Propose research extension

### I want to use this for my research. How do I get started?

**Step 1**: Download data
```bash
git clone https://github.com/Luminous-Dynamics/historical-k-index.git
cd historical-k-index
nix develop  # or: poetry install
poetry run python shared/scripts/download_all_data.py
```

**Step 2**: Explore interactively
```bash
poetry run jupyter notebook notebooks/01_explore_k_index.ipynb
```

**Step 3**: Develop your research question

**Step 4**: Open "Research Proposal" issue to discuss

### I have more questions!

**Ask away!**

- **GitHub Discussions**: For research ideas and general questions
- **GitHub Issues**: For specific bugs or feature requests
- **Email**: tristan.stoltz@evolvingresonantcocreationism.com

---

**Welcome to the coordination revolution!** 🌊

*"By measuring global coordination capacity, we can improve it."*
