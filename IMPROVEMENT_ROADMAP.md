# Historical K(t) Index - Comprehensive Improvement Roadmap

**Version:** 1.0
**Created:** December 2, 2025
**Status:** Active Development Plan
**Timeline:** 18-month phased implementation

---

## Executive Summary

This roadmap transforms the Historical K(t) Index from a publication-ready academic paper into a paradigm-shifting framework for measuring and monitoring civilizational coherence. The plan is organized into five phases, each building on the previous, with clear milestones and success criteria.

**Core Objectives:**
1. **Scientific Rigor** - Replace synthetic proxies with validated measures
2. **Policy Utility** - Make K(t) actionable for decision-makers
3. **Research Infrastructure** - Build ecosystem for collaborative extension
4. **Paradigm Impact** - Establish K(t) as essential civilizational metric

---

## Phase 0: Critical Pre-Publication (Weeks 1-4)

**Goal:** Strengthen manuscript to maximize acceptance probability at Nature/Science

### Priority Tasks

#### Task 0.1: Replace H₇ Synthetic Proxies ⚠️ CRITICAL
**Status:** Must complete before submission
**Effort:** 40 hours
**Dependencies:** None

**Current Problem:**
- H₇ uses HYDE population data as placeholder
- Weakens manuscript ("synthetic" label raises red flags)
- Limits citation potential and credibility

**Solution - Multi-Component H₇:**
```python
H₇(t) = geometric_mean([
    patent_stock_per_capita(t),      # WIPO 1883-2023
    constitutional_complexity(t),     # CCP 1789-2023
    education_capital(t),             # Barro-Lee 1870-2023
    infrastructure_density(t)         # Multiple sources
])
```

**Action Steps:**
1. Download WIPO patent data (World Intellectual Property Indicators)
2. Extract Comparative Constitutions Project complexity measures
3. Calculate cumulative education capital from Barro-Lee dataset
4. Construct infrastructure index (railways, roads, power grid)
5. Recalculate K(t) with validated H₇
6. Update all figures, tables, and text
7. Rerun bootstrap CI and sensitivity analysis

**Success Criteria:**
- ✅ H₇ no longer labeled "synthetic"
- ✅ All seven harmonies use established data sources
- ✅ K₂₀₂₀ estimate remains stable (±5%)
- ✅ Manuscript strengthened for top-tier journals

**Deliverables:**
- `data/processed/H7_validated_1810_2020.csv`
- `manuscript/figures/H7_decomposition.png`
- Updated manuscript and supplementary materials

---

#### Task 0.2: Add Country-Level K(t) for 2020 (Validation)
**Status:** High priority enhancement
**Effort:** 24 hours
**Dependencies:** Task 0.1 complete

**Rationale:**
- Reviewers will ask "does this work at country level?"
- Provides face validity check (expect Nordic countries high, fragile states low)
- Opens door for follow-up comparative paper

**Implementation:**
```python
# For each country c in [top_20_economies + random_sample_30]
K_country(c, 2020) = geometric_mean([H₁(c), H₂(c), ..., H₆(c)])

# Create validation plot
plot_map(K_country, 2020)
correlation(K_country, [GDP, HDI, Fragile_States_Index])
```

**Action Steps:**
1. Extract country-level data for all harmonies (2020)
2. Calculate K(c, 2020) for 50 countries (coverage: 80% global pop)
3. Create world map visualization with K(t) choropleth
4. Validate against GDP, HDI, Fragile States Index
5. Add to supplementary materials as Figure S7

**Success Criteria:**
- ✅ Country-level K(t) correlates strongly with HDI (r > 0.7)
- ✅ Nordic countries rank in top 10
- ✅ Fragile states rank in bottom 20
- ✅ Visual map passes "eye test" for face validity

**Deliverables:**
- `data/processed/K_country_2020.csv`
- `manuscript/supplementary/FIGURE_S7_country_map.png`
- Supplementary text on country-level validation

---

#### Task 0.3: Final Manuscript Polish
**Status:** Continuous
**Effort:** 16 hours
**Dependencies:** Tasks 0.1, 0.2 complete

**Focus Areas:**
1. **Abstract:** Strengthen Great Filter connection
2. **Introduction:** Add policy relevance framing
3. **Discussion:** Expand on existential risk implications
4. **Limitations:** Honest about remaining uncertainties
5. **Data Availability:** Commit to open data release schedule

**Submission Strategy:**
- **First Choice:** Nature (high impact, broad readership)
- **Second Choice:** Science (similar tier, faster turnaround)
- **Third Choice:** PNAS (excellent reputation, higher acceptance rate)

**Timeline:**
- Week 1-2: Tasks 0.1, 0.2
- Week 3: Manuscript updates
- Week 4: Internal review, final checks, submit

---

## Phase 1: Foundation (Months 1-3 Post-Publication)

**Goal:** Build infrastructure for K(t) as living, evolving framework

### Priority Tasks

#### Task 1.1: Full Country-Level K(t) Time Series (1810-2020)
**Status:** Foundation for comparative research
**Effort:** 80 hours
**Dependencies:** Phase 0 complete

**Scope:**
- Calculate K(c, t) for all countries with sufficient data
- Handle missing data gracefully (mark as NA, don't impute across countries)
- Create regional aggregates (continents, OECD, Global South, etc.)

**Technical Approach:**
```python
countries = get_countries_with_coverage(min_years=50, min_harmonies=4)

for c in countries:
    for year in range(1810, 2021):
        if data_available(c, year) >= 4:  # At least 4/6 harmonies
            K[c, year] = geometric_mean([H_d(c, year) for d in available])
        else:
            K[c, year] = NA
```

**Analysis Outputs:**
1. **Convergence/Divergence:** Are countries becoming more similar (convergence) or diverse (divergence)?
2. **Leaders & Laggards:** Which countries show fastest coherence growth?
3. **Shocks & Resilience:** How do countries respond to global crises?
4. **Predictive Power:** Does K(c, t) predict future outcomes?

**Deliverables:**
- `data/processed/K_country_timeseries_1810_2020.csv` (200 countries × 210 years)
- `analysis/convergence_divergence_analysis.py`
- `visualizations/country_trajectories_animated.gif`
- Research brief: "Mapping Global Coherence: 200 Years of Country-Level Analysis"

---

#### Task 1.2: Dynamic Weighting by Data Quality
**Status:** Methodological improvement
**Effort:** 60 hours
**Dependencies:** None (can run in parallel)

**Problem:**
- Equal weights assume all harmonies equally reliable across all time
- Pre-1900 governance data sparse → should be downweighted
- Post-1990 globalization data excellent → can be trusted more

**Solution - Quality-Adjusted Weights:**
```python
def quality_score(harmony, year):
    coverage = country_coverage(harmony, year) / total_countries
    resolution = temporal_resolution(harmony, year)  # annual vs decadal
    source_quality = established_data_source(harmony)  # V-Dem=5, HYDE=3

    return coverage * resolution * source_quality

# Apply to K(t) calculation
w_d(t) = quality_score(d, t) / sum(quality_score(i, t) for i in harmonies)
K(t) = sum(w_d(t) * H_d(t) for d in harmonies)
```

**Impact:**
- More honest uncertainty quantification
- Confidence intervals reflect actual data quality
- Pre-1900 K(t) appropriately uncertain
- Post-1990 K(t) highly confident

**Validation:**
- Compare static vs dynamic weighting
- Show that dynamic weights don't change main conclusions
- Demonstrate improved calibration (CI coverage)

**Deliverables:**
- `src/weighting/dynamic_quality_weights.py`
- `docs/DYNAMIC_WEIGHTING_METHODOLOGY.md`
- Updated K(t) time series with quality-adjusted weights

---

#### Task 1.3: Automated Data Pipeline & Version Control
**Status:** Infrastructure
**Effort:** 100 hours
**Dependencies:** None (high priority parallel track)

**Goal:** Make K(t) reproducible, updatable, and transparent

**Architecture:**
```
k-index-pipeline/
├── data/
│   ├── raw/              # Source data (versioned)
│   ├── interim/          # Intermediate processing
│   └── processed/        # Final K(t) outputs
├── src/
│   ├── download/         # Automated data fetching
│   ├── harmonize/        # Data cleaning & alignment
│   ├── calculate/        # K(t) computation
│   └── validate/         # Quality checks
├── tests/                # Unit & integration tests
├── config/
│   └── sources.yaml      # Data source definitions
└── dvc.yaml              # Data version control (DVC)
```

**Key Features:**
1. **Automated Downloads:**
   - V-Dem: API-based fetch
   - KOF: Web scraping + caching
   - World Bank: WDI API
   - All sources: Check for updates weekly

2. **Version Control:**
   - Git for code
   - DVC for data (data version control)
   - Semantic versioning (v1.0.0, v1.1.0, etc.)
   - Changelog for methodology changes

3. **Continuous Integration:**
   - Run full pipeline on every commit
   - Compare outputs to previous version
   - Flag significant changes (>1% in K₂₀₂₀)
   - Automated testing (unit + integration)

4. **Reproducibility:**
   - Docker container with fixed environment
   - `make reproduce` runs entire pipeline
   - Verification script checks outputs match manuscript

**Deliverables:**
- Complete pipeline codebase on GitHub
- Docker image: `k-index:v1.0`
- Documentation: `docs/REPLICATION_GUIDE.md`
- CI/CD setup (GitHub Actions)

---

#### Task 1.4: K(t) Dashboard MVP (Minimum Viable Product)
**Status:** High impact deliverable
**Effort:** 120 hours
**Dependencies:** Tasks 1.1, 1.2 complete

**Vision:** Interactive web dashboard for exploring K(t) data

**Technology Stack:**
- **Backend:** Python (Flask/FastAPI)
- **Frontend:** React + D3.js for visualizations
- **Database:** PostgreSQL for time series
- **Hosting:** Vercel (frontend) + Railway (backend)

**Features - Phase 1 (MVP):**
1. **Global K(t) Time Series:** Interactive line chart (1810-2020)
2. **Harmony Decomposition:** Stacked area chart showing H₁-H₇ contributions
3. **Country Comparison:** Select 2-5 countries, overlay trajectories
4. **World Map:** Choropleth for any year (slider to animate)
5. **Data Export:** Download CSV for selected countries/years

**User Experience:**
```
[Landing Page]
├─ Current K(t): 0.914 (2020) ↑ 76% since 1810
├─ Interactive Chart: 200-year trajectory
├─ [Explore by Country] → Country selector
├─ [Explore by Harmony] → Harmony deep-dive
└─ [Download Data] → CSV export

[Country Page]
├─ K(t) trajectory for selected country
├─ Comparison to global average
├─ Harmony radar chart (spider plot)
└─ Historical context (major events)
```

**Success Criteria:**
- ✅ Dashboard loads in <2 seconds
- ✅ Visualizations responsive and intuitive
- ✅ Mobile-friendly design
- ✅ 1000+ unique visitors in first month

**Deliverables:**
- Live dashboard at `atlas.luminousdynamics.io/k-index`
- Source code on GitHub
- User guide and API documentation

---

## Phase 2: Expansion (Months 4-9)

**Goal:** Advanced features and research applications

### Priority Tasks

#### Task 2.1: Sub-Annual K(t) (Monthly/Quarterly)
**Status:** Innovation - high-frequency monitoring
**Effort:** 150 hours
**Dependencies:** Phase 1 complete

**Motivation:**
- Annual K(t) misses rapid changes (COVID-19 shock, 2008 crisis)
- Policy-makers need real-time monitoring
- Test whether K(t) has predictive power for crises

**Approach:**
```python
# High-frequency proxies for each harmony
H₁_monthly: Stock market volatility, social media political sentiment
H₂_monthly: Trade volumes (customs data), flight data
H₃_monthly: Aid disbursements, diplomatic exchanges
H₄_monthly: Patent filings, cultural production
H₅_monthly: R&D spending, scientific preprints
H₆_monthly: Life satisfaction surveys, environmental indicators
```

**Coverage:**
- 2000-2025 (25 years × 12 months = 300 observations)
- Focus on G20 countries first, then expand

**Research Questions:**
1. Did K(t) drop sharply during COVID-19 (Q1 2020)?
2. Can monthly K(t) predict stock market crashes?
3. Does K(t) show leading indicators for conflicts?

**Deliverables:**
- `data/processed/K_monthly_2000_2025.csv`
- Real-time dashboard update (monthly refresh)
- Research paper: "High-Frequency Civilizational Coherence"

---

#### Task 2.2: Causal Structure Learning
**Status:** Advanced analytics
**Effort:** 100 hours
**Dependencies:** Task 1.1 complete

**Question:** What are the causal relationships between harmonies?

**Methods:**
1. **Granger Causality:** Test lead-lag relationships
   - Does H₁ (governance) Granger-cause H₆ (flourishing)?
   - Does H₅ (interconnection) Granger-cause H₃ (reciprocity)?

2. **Bayesian Network Learning:** Discover causal DAG
   - Use PC algorithm or GES search
   - Validate with domain knowledge
   - Test interventional predictions

3. **Vector Autoregression (VAR):** Joint dynamics
   - Estimate VAR(p) model for all harmonies
   - Impulse response functions (IRFs)
   - Variance decomposition

**Example Hypotheses:**
- H₁ → H₆: Better governance → higher wellbeing (direct)
- H₅ → H₃: More interconnection → more reciprocity (mediated)
- H₆ → H₁: Higher wellbeing → better governance (feedback)

**Impact:**
- Identifies policy leverage points
- Reveals which harmonies are "drivers" vs "outcomes"
- Guides intervention priorities

**Deliverables:**
- Causal diagram (DAG) for seven harmonies
- Technical report: "Causal Dynamics of Civilizational Coherence"
- Policy brief: "Which Dimensions Drive Coherence?"

---

#### Task 2.3: K(t) and Existential Risk
**Status:** High-impact application
**Effort:** 80 hours
**Dependencies:** Phase 1 complete

**Thesis:** K(t) acts as a "risk buffer" for existential threats

**Analysis:**
```python
# Test correlation between K(t) and risk proxies
risks = {
    'nuclear_near_misses': load_near_miss_database(),  # 1950-2020
    'pandemic_preparedness': load_ghs_index(),          # 2019-2023
    'ai_safety_governance': load_ai_readiness(),        # 2020-2023
    'climate_policy_strength': load_climate_action()    # 1990-2023
}

for risk in risks:
    correlation(K(t), risk(t))
    regression(risk ~ K + controls)
    threshold_analysis(K_min_for_safe_navigation)
```

**Research Questions:**
1. Did nuclear near-misses occur during low-K periods?
2. Do high-K countries have better pandemic preparedness?
3. Is there a K(t) threshold below which existential risks unmanageable?

**Deliverable:**
- Research paper: "Civilizational Coherence and Existential Risk"
- Submission target: *Nature Human Behaviour* or *Global Policy*
- Policy recommendations for UN, Long-Term Institutions

---

#### Task 2.4: Integration with Earth System Models
**Status:** Cross-disciplinary collaboration
**Effort:** 200 hours
**Dependencies:** Phase 1 complete, external partnerships

**Goal:** Integrate K(t) with climate and planetary boundaries research

**Partnerships:**
- Stockholm Resilience Centre (Planetary Boundaries)
- PIK Potsdam (DICE model)
- IIASA (MESSAGE, SSP scenarios)

**Research Questions:**
1. Does K(t) predict better climate policy outcomes?
2. How do planetary boundary transgressions affect K(t)?
3. Can K(t) improve Shared Socioeconomic Pathways (SSPs)?

**Implementation:**
```python
# Add K(t) as exogenous variable to IAMs
DICE_with_K:
    emissions(t) = f(GDP(t), carbon_tax(t), K(t))
    # Hypothesis: Higher K → lower emissions at same GDP

# Test feedback loops
planetary_boundaries → H₆ (flourishing) → K(t) → policy_quality → boundaries
```

**Deliverable:**
- Joint paper with climate modeling community
- K(t) integrated into SSP scenarios for IPCC AR7
- Policy brief: "Coherence and Climate: Why Social Factors Matter"

---

## Phase 3: Innovation (Months 10-18)

**Goal:** Breakthrough extensions and theoretical advances

### Priority Tasks

#### Task 3.1: Machine Learning for Harmony Discovery
**Status:** Ambitious - test foundational assumptions
**Effort:** 150 hours
**Dependencies:** Phase 1 complete

**Question:** Are the seven harmonies the "right" structure?

**Approach:**
```python
# Load all 30+ proxy variables (no theory, just data)
X = load_all_proxies()  # 30 variables × 210 years

# Unsupervised learning
pca = PCA(n_components=10)
factors = pca.fit_transform(X)

# How many latent dimensions?
plot_scree(pca.explained_variance_ratio_)

# What do discovered factors represent?
for i, factor in enumerate(factors):
    top_loadings = X.columns[argsort(pca.components_[i])]
    interpret_factor(top_loadings)

# Compare to seven harmonies
discovered_K = geometric_mean(factors[:n_optimal])
correlation(discovered_K, K_seven_harmonies)
```

**Possible Outcomes:**
1. **Confirmation:** PCA discovers ~7 factors matching our harmonies
2. **Refinement:** Suggests 5-6 core factors, others are subcomponents
3. **Surprise:** Data suggests different structure entirely

**Radical Honesty:**
- If data suggests different structure, seriously consider revising framework
- Science over aesthetics (even if seven harmonies are elegant)

**Deliverable:**
- Technical report: "Data-Driven Discovery of Coherence Dimensions"
- Potential framework revision if strongly warranted

---

#### Task 3.2: Historical Deep Dive - Ancient Civilizations
**Status:** Ambitious archeo-historical extension
**Effort:** 300 hours
**Dependencies:** Phase 2 complete, historian partnerships

**Goal:** Apply K(t) framework to pre-1810 civilizations

**Case Studies:**
1. **Roman Empire** (500 BCE - 500 CE)
2. **Han Dynasty** (206 BCE - 220 CE)
3. **Islamic Golden Age** (750-1258 CE)
4. **Mongol Empire** (1206-1368 CE)

**Data Sources:**
- ORBIS (Roman transportation networks) → H₅
- Seshat Global History Databank → H₁, H₇
- Historical climate proxies → H₆
- Archaeological surveys → urbanization, trade

**Research Questions:**
1. Did collapse civilizations show coherence decline patterns?
2. Is there a coherence threshold below which collapse inevitable?
3. Can K(t) predict resilience vs fragility?

**Challenges:**
- Data sparse and uncertain
- Comparability across cultures difficult
- Need historian collaboration for interpretation

**Deliverable:**
- Book chapter or edited volume
- "Coherence and Collapse: Lessons from Ancient Civilizations"

---

#### Task 3.3: K(t) for Sub-Global Systems
**Status:** Exploratory - test scale-invariance
**Effort:** 200 hours
**Dependencies:** Phase 1 complete

**Hypothesis:** Coherence dynamics are scale-invariant

**Applications:**
1. **Cities:** K(t) for 50 global megacities
   - Data: Urban Observatory, city-level stats
   - Question: Do coherent cities grow faster?

2. **Firms:** Corporate coherence index
   - Data: ESG ratings, employee satisfaction, innovation metrics
   - Question: Does firm coherence predict performance?

3. **Online Communities:** Reddit, GitHub, Wikipedia
   - Data: Contribution patterns, conflict resolution, diversity
   - Question: What makes online communities coherent?

4. **Ecosystems:** Ecological coherence
   - Data: Biodiversity, trophic balance, resilience
   - Question: Parallels between social and ecological coherence?

**Deliverable:**
- Comparative study: "Coherence Across Scales"
- Test whether K(t) framework generalizes beyond civilizations

---

## Phase 4: Maturity & Ecosystem (Year 2+)

**Goal:** Establish K(t) as paradigm and build community

### Priority Tasks

#### Task 4.1: K(t) Data Commons & API
**Status:** Infrastructure for collaborative research
**Effort:** 250 hours
**Dependencies:** Phase 1, 2 complete

**Vision:** Open infrastructure for coherence research

**Components:**
1. **Data Repository:**
   - Zenodo DOI for all datasets
   - Version control (v1.0, v1.1, etc.)
   - Metadata and documentation

2. **REST API:**
```python
GET /api/v1/k-index/global?start_year=1810&end_year=2020
GET /api/v1/k-index/country/{iso_code}?year=2020
GET /api/v1/harmonies/{harmony_id}?country={iso_code}
```

3. **Computation Platform:**
   - Jupyter Hub for reproducible analysis
   - Pre-loaded data and compute resources
   - Shareable notebooks

4. **Collaboration Hub:**
   - GitHub Discussions for research community
   - Quarterly virtual workshops
   - Annual K(t) conference

**Deliverable:**
- Public API at `api.k-index.org`
- Data commons at `data.k-index.org`
- Community hub at `community.k-index.org`

---

#### Task 4.2: K(t) in Policy & Practice
**Status:** Real-world adoption
**Effort:** Ongoing
**Dependencies:** Strong publication record

**Engagement Strategy:**

1. **UN System:**
   - Present to UN Development Programme
   - Propose as SDG complement (Goal 16+)
   - Integrate into Human Development Reports

2. **G7/G20:**
   - Policy brief for finance ministers
   - Propose as monitoring framework
   - Quarterly coherence updates

3. **Academic Adoption:**
   - Textbook chapters on K(t)
   - Course curricula (global governance, sustainability)
   - Citation tracking (target: 100+ cites/year)

4. **Public Communication:**
   - TED Talk: "Measuring Civilizational Coherence"
   - Op-eds in NYT, Guardian, FT
   - Documentary or podcast series

**Success Metrics:**
- 5+ organizations using K(t) in policy documents
- 500+ citations in peer-reviewed literature
- 100,000+ dashboard unique visitors

---

## Implementation Strategy

### Resource Requirements

**Personnel:**
- Lead Researcher (Tristan): 20 hrs/week
- AI Assistant (Claude): Continuous collaboration
- Local AI (Mistral): Domain-specific queries
- External Consultants: Historians, climate scientists, policy experts (as needed)

**Infrastructure:**
- Cloud Compute: $200-500/month (AWS/GCP)
- Dashboard Hosting: $100/month (Vercel + Railway)
- Data Storage: $50/month (PostgreSQL)
- AI Tools: $200/month (Claude, local models)

**Total Budget:** ~$12,000-15,000/year

### Timeline Summary

| Phase | Duration | Key Milestones |
|-------|----------|----------------|
| Phase 0 | Weeks 1-4 | H₇ fixed, country K(t), submission |
| Phase 1 | Months 1-3 | Pipeline, dashboard, dynamic weighting |
| Phase 2 | Months 4-9 | Sub-annual K(t), causal analysis, risk paper |
| Phase 3 | Months 10-18 | ML discovery, ancient civilizations, multi-scale |
| Phase 4 | Year 2+ | API, community, policy adoption |

### Success Criteria by Phase

**Phase 0:**
- ✅ Manuscript accepted at Nature/Science/PNAS
- ✅ H₇ validated with real data
- ✅ Country-level K(t) demonstrated

**Phase 1:**
- ✅ Dashboard live with 1000+ users
- ✅ Automated pipeline operational
- ✅ Country time series complete

**Phase 2:**
- ✅ 2+ follow-up papers published
- ✅ K(t) integrated into 1+ climate model
- ✅ Monthly K(t) tracking live

**Phase 3:**
- ✅ Framework validated across scales
- ✅ Theoretical advances published
- ✅ Historical case studies complete

**Phase 4:**
- ✅ API serving 10+ research groups
- ✅ Policy adoption by major organizations
- ✅ 100+ citations/year achieved

---

## Risk Mitigation

### Scientific Risks

**Risk:** H₇ replacement doesn't work
- **Mitigation:** Test multiple proxy combinations, fallback to 6-harmony

**Risk:** Country-level K(t) doesn't correlate with expected outcomes
- **Mitigation:** Investigate mismatches, may reveal interesting anomalies

**Risk:** ML discovers very different structure than seven harmonies
- **Mitigation:** Embrace revision if data strongly supports, frame as refinement

### Technical Risks

**Risk:** Data pipeline too complex to maintain
- **Mitigation:** Prioritize simplicity, extensive documentation, modular design

**Risk:** Dashboard performance issues
- **Mitigation:** Database optimization, caching, CDN for static assets

**Risk:** API abuse or overuse
- **Mitigation:** Rate limiting, authentication for heavy users

### Adoption Risks

**Risk:** Policy-makers don't find K(t) useful
- **Mitigation:** User research, iterate on communication, focus groups

**Risk:** Academic community ignores K(t)
- **Mitigation:** Publish in top journals, present at conferences, build coalition

**Risk:** Public misinterprets K(t) (e.g., "coherence = conformity")
- **Mitigation:** Clear communication, emphasize diversity (H₄) component

---

## Measurement & Accountability

### Key Performance Indicators (KPIs)

**Academic Impact:**
- Publications in top journals (target: 5 in Year 1-2)
- Citation count (target: 100+ by end of Year 2)
- Conference presentations (target: 10+ in Year 1-2)

**Policy Impact:**
- Organizations using K(t) (target: 5 by end of Year 2)
- Policy briefs downloaded (target: 1000+ downloads)
- Mentions in policy documents (target: 20+ by end of Year 2)

**Public Engagement:**
- Dashboard visitors (target: 100,000+ by end of Year 2)
- Media coverage (target: 10+ major outlets)
- Social media reach (target: 50,000+ impressions)

**Technical:**
- API requests/month (target: 10,000+ by end of Year 2)
- Data downloads (target: 1,000+ unique users)
- GitHub stars (target: 500+ on main repo)

### Quarterly Reviews

**Q1 (Months 1-3):** Phase 0 + Phase 1 start
- Manuscript submitted? ✓/✗
- Pipeline operational? ✓/✗
- Dashboard launched? ✓/✗

**Q2 (Months 4-6):** Phase 1 complete, Phase 2 start
- Country time series complete? ✓/✗
- First follow-up paper submitted? ✓/✗
- 1000+ dashboard users? ✓/✗

**Q3 (Months 7-9):** Phase 2 midpoint
- Causal analysis complete? ✓/✗
- Monthly K(t) operational? ✓/✗
- Climate modeling integration started? ✓/✗

**Q4 (Months 10-12):** Phase 2 complete, Phase 3 start
- Risk paper submitted? ✓/✗
- ML discovery analysis complete? ✓/✗
- Ancient civilizations data collected? ✓/✗

---

## Adaptive Planning

**This roadmap is a living document.** Adjust based on:

1. **Manuscript Feedback:** Reviewer suggestions may prompt new directions
2. **Community Interest:** If certain features gain traction, prioritize them
3. **Resource Availability:** Scale ambition to match funding and personnel
4. **Breakthrough Opportunities:** If unexpected insights emerge, follow them
5. **Strategic Partnerships:** Collaborations may accelerate certain tracks

**Review Cadence:**
- Monthly: Progress check on active phase
- Quarterly: Phase completion review
- Annually: Full roadmap revision

---

## Conclusion

The Historical K(t) Index has the potential to transform how humanity understands and navigates its collective development. This roadmap provides a clear path from academic publication to paradigm-shifting framework.

**Core Philosophy:**
- **Rigor First:** Scientific validity over speed
- **Utility Matters:** Build what policy-makers and researchers need
- **Open by Default:** Transparent methods, open data, collaborative community
- **Adaptive Evolution:** Let evidence guide the framework's development

**Vision:**
By the end of this roadmap, K(t) should be as essential to global governance as GDP, HDI, or the Planetary Boundaries framework. It should be the "coherence dashboard" that helps civilization navigate the 21st century's existential challenges.

**Next Step:** Begin Phase 0, Task 0.1 - Replace H₇ synthetic proxies.

---

**Document Status:** v1.0 - Comprehensive Plan
**Next Update:** After Phase 0 completion
**Contact:** tristan.stoltz@luminousdynamics.org
