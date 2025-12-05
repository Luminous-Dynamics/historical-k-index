# The Twelve Laws of Coordination Collapse: Formal Analysis

**Status**: Draft for rigorous review
**Objective**: Prove, refine, or refute each law with evidence and mathematical formalization

---

## Summary Table

| # | Law Name | Statement | Formula | Evidence Level | Status |
|---|----------|-----------|---------|----------------|--------|
| 1 | Trust Threshold | θ ≈ 0.375 is critical boundary | θ = 0.375 ± 0.025 | Strong | ✅ Validated |
| 2 | Cascade | Below θ, decline accelerates | dH₃/dt ∝ -(θ - H₃)² | Moderate | ⚠️ Needs proof |
| 3 | Network | Hub-spoke collapses faster | v_c ∝ centralization | Moderate | ⚠️ Needs data |
| 4 | Modernization | Higher λ = faster collapse | λ ∈ [0.8, 2.2] | Weak | ❌ Needs derivation |
| 5 | Recovery | P(recovery) ≈ 0.15 below θ | Binomial estimate | Moderate | ⚠️ Small N |
| 6 | Visibility | Resources mask H₃ decline | H₃_apparent > H₃_true | Theoretical | ❌ Needs test |
| 7 | Intervention | ROI 10:1 before θ, 1:10 after | ROI = f(distance to θ) | Moderate | ⚠️ Needs cases |
| 8 | Dark Trust | ~40% unmeasured | H₃_dark ≈ 0.4 × H₃_total | Weak | ❌ Key gap |
| 9 | Feedback | Trust generates trust above θ | dH₃/dt > 0 if H₃ > θ | Strong | ✅ Game theory |
| 10 | Percolation | θ ≈ p_c (phase transition) | θ ≈ 0.388 (diamond) | Strong | ✅ Physics |
| 11 | Learning | μ ≈ 0 historically | No civilization learns | Moderate | ⚠️ Observational |
| 12 | Glass Ceiling | K_max ≈ 0.85 | Upper bound on K | Moderate | ⚠️ Needs theory |

---

## Law 1: The Trust Threshold Law

### Statement
> θ ≈ 0.375 is the critical collapse boundary. When H₃ < θ, collapse becomes self-reinforcing.

### Mathematical Formalization
```
Definition: θ* = argmax_θ {Accuracy(θ | collapse_cases)}

Empirical Result: θ* = 0.375 ± 0.025 (95% CI: 0.35-0.40)
```

### Evidence

**Empirical (Strong)**:
- Grid search across 35 cases yields θ = 0.375
- Leave-one-out CV: θ = 0.375 ± 0.004
- 31/35 cases (89%) predicted within ±15 years

**Theoretical (Strong)**:
- Game theory ESS: θ = c/(1+c) ≈ 0.38 for c = 0.6
- Percolation physics: p_c = 0.388 (diamond lattice)
- See Paper 2B for 8 independent derivations converging on 0.381 ± 0.005

### Verdict: ✅ VALIDATED
This is the strongest law with both empirical and theoretical support.

---

## Law 2: The Cascade Law

### Statement
> Below θ, trust decline accelerates quadratically.

### Mathematical Formalization
```
dH₃/dt = -λ(θ - H₃)² for H₃ < θ
       = +μ(H₃ - θ)   for H₃ > θ

where λ > 0 is cascade coefficient, μ > 0 is recovery coefficient
```

### Evidence

**Empirical (Moderate)**:
- Rome: 250-year decline (H₃: 0.50 → 0.20)
- Soviet: 6-year collapse (H₃: 0.35 → 0.15)
- Quadratic fit R² = 0.73 across cases

**Theoretical (Moderate)**:
- Positive feedback loop: low trust → defection → lower trust
- Network percolation: fragmentation accelerates below p_c
- But: Why exactly quadratic? Linear or exponential also plausible.

### Issues
- Quadratic form assumed, not derived
- λ varies by 3x across cases (0.8 - 2.2) without clear explanation
- Need to distinguish cascade rate from measurement noise

### Verdict: ⚠️ PARTIALLY VALIDATED
The cascade exists, but the quadratic form needs theoretical derivation.

---

## Law 3: The Network Law

### Statement
> Hub-and-spoke networks collapse faster than distributed networks.

### Mathematical Formalization
```
v_c = base_rate × f(topology)

where:
f(hierarchical)  ≈ 0.8  (Rome)
f(polycentric)   ≈ 1.1  (Maya)
f(trade_network) ≈ 1.5  (Bronze Age)
f(centralized)   ≈ 2.2  (Soviet)
```

### Evidence

**Empirical (Moderate)**:
- Soviet (centralized): 6 years
- Bronze Age (trade): 50 years
- Maya (polycentric): 100 years
- Rome (hierarchical): 250 years

**Theoretical (Strong)**:
- Network science: centralized networks have single point of failure
- Percolation: removal of hub fragments network immediately
- BUT: Contradicts data! Rome was hierarchical but slowest.

### Issues
- **Major inconsistency**: Rome was hub-and-spoke centered on emperor, yet collapsed slowest
- Need to separate "collapse speed" from "total duration"
- Centralization may affect cascade onset, not rate

### Proposed Refinement
```
v_c = λ × (θ - H₃)² × redundancy⁻¹

where redundancy = # of independent coordination paths
Soviet: redundancy = 1 (CPSU monopoly)
Rome: redundancy = 3 (Senate, Army, Church)
```

### Verdict: ⚠️ NEEDS REFINEMENT
The core insight is valid but formalization conflicts with data.

---

## Law 4: The Modernization Law

### Statement
> Higher λ (modernization coefficient) leads to faster collapse.

### Mathematical Formalization
```
λ = f(communication_speed, economic_integration, institutional_complexity)

Proposed: λ ≈ log(network_connectivity × information_speed)
```

### Evidence

**Empirical (Weak)**:
- Values assigned post-hoc: λ_Rome = 0.8, λ_Soviet = 2.2
- No independent derivation of λ

**Theoretical (Moderate)**:
- Information cascades: faster communication → faster panic
- Bank runs analogy: modern systems more vulnerable to coordination failure

### Issues
- λ is currently a free parameter fit to each case
- No predictive test (what is λ for USA 2024?)
- Circularity: we define λ by how fast collapse happened

### Proposed Fix
```
λ_predicted = α × log(GDP_per_capita) + β × urbanization_rate + γ × media_penetration

Then validate: does predicted λ match observed collapse speed?
```

### Verdict: ❌ NEEDS DERIVATION
Currently unfalsifiable - λ is fit rather than predicted.

---

## Law 5: The Recovery Law

### Statement
> P(recovery | H₃ < θ) ≈ 0.15

### Mathematical Formalization
```
P(recovery | H₃ < θ) = k / n

where k = # civilizations that recovered after crossing θ
      n = # civilizations that crossed θ

Estimate: k ≈ 5, n ≈ 35, P ≈ 0.14 ± 0.06
```

### Evidence

**Empirical (Moderate)**:
- 4 "survivor" cases studied
- ~5/35 historical cases show some recovery
- Binomial 95% CI: [0.05, 0.28]

**Theoretical (Moderate)**:
- Below θ, defection is Nash equilibrium
- Recovery requires coordination on new equilibrium
- Schelling focal points: hard to coordinate without trust

### Issues
- Small N (n=35) gives wide confidence intervals
- "Recovery" not operationally defined
- Selection bias: we only study cases with documentation

### Verdict: ⚠️ PLAUSIBLE BUT UNCERTAIN
Point estimate reasonable but uncertainty is high.

---

## Law 6: The Visibility Law

### Statement
> Resource wealth masks declining H₃.

### Mathematical Formalization
```
H₃_apparent = H₃_true + ε_resources

where ε = f(GDP_per_capita, natural_resources)

"Dutch Disease of Trust": Resource wealth substitutes for cooperation
```

### Evidence

**Empirical (Weak)**:
- Oil states (Saudi, Venezuela) show high apparent function despite low trust surveys
- No systematic test across historical cases

**Theoretical (Moderate)**:
- Resource curse literature (Sachs, Ross)
- Rentier state theory: no need for social contract
- But: indirect evidence, not direct H₃ measurement

### Issues
- Needs operational definition of "masking"
- How to measure H₃_true vs H₃_apparent?
- May confuse cause and effect

### Verdict: ❌ THEORETICAL - NEEDS TESTING
Plausible mechanism but no rigorous test.

---

## Law 7: The Intervention Law

### Statement
> ROI of intervention = 10:1 before θ, 1:10 after.

### Mathematical Formalization
```
ROI(intervention) = ΔH₃ / Cost

Claim:
ROI_before = 10 × ROI_after
```

### Evidence

**Empirical (Moderate)**:
- Marshall Plan: $13B → prevented collapse (ROI high)
- Late Roman reforms: high cost, little effect (ROI low)
- No systematic comparison

**Theoretical (Strong)**:
- Hysteresis: crossing threshold changes system dynamics
- Prevention vs cure: medical analogy
- Network repair is harder than maintenance

### Issues
- 10:1 ratio is an assertion, not derived
- Need cases with comparable interventions before/after θ
- Confounding: different interventions, different contexts

### Proposed Test
```
Compare:
- Interventions in [θ+0.05, θ+0.15] range
- Interventions in [θ-0.15, θ-0.05] range
- Measure ΔH₃ per $1B invested
```

### Verdict: ⚠️ PLAUSIBLE BUT UNQUANTIFIED
Directionally correct, ratio unproven.

---

## Law 8: The Dark Trust Law

### Statement
> ~40% of coordination capacity is unmeasured ("dark trust").

### Mathematical Formalization
```
H₃_total = H₃_measured + H₃_dark

H₃_dark = H₃_coerced + H₃_habitual + H₃_implicit

Claim: H₃_dark / H₃_total ≈ 0.40
```

### Evidence

**Empirical (Weak)**:
- Survey trust ≠ behavioral trust
- Dictator game: 40% give despite anonymous setting
- Institutional trust not captured by interpersonal surveys

**Theoretical (Moderate)**:
- Multiple trust mechanisms: calculated, identity-based, habit
- Only interpersonal trust typically measured
- Dark matter analogy from physics

### Issues
- **Critical gap**: No method to measure dark trust
- 40% is an assertion, could be 20% or 60%
- Different types of "dark" trust may behave differently

### Proposed Operationalization
```
H₃_dark = H₃_behavioral - H₃_survey

where:
H₃_behavioral = observed cooperation rate in field experiments
H₃_survey = reported trust in surveys
```

### Verdict: ❌ KEY CONCEPTUAL GAP
Important insight but completely unoperationalized.

---

## Law 9: The Feedback Law

### Statement
> Trust generates trust (positive feedback above θ).

### Mathematical Formalization
```
dH₃/dt = μ(H₃ - θ) for H₃ > θ  [positive feedback]
dH₃/dt = -λ(θ - H₃)² for H₃ < θ [negative feedback]
```

### Evidence

**Empirical (Moderate)**:
- High-trust societies (Nordics) maintain/increase trust
- Low-trust societies (many developing) stay low
- But: some low-trust societies have improved (South Korea)

**Theoretical (Strong)**:
- Repeated games: tit-for-tat stabilizes cooperation
- Reputation mechanisms: cooperation signals cooperativeness
- Social capital literature (Putnam)

### Verdict: ✅ VALIDATED
Well-established in game theory and empirical literature.

---

## Law 10: The Percolation Law

### Statement
> θ ≈ p_c (trust threshold equals network percolation threshold).

### Mathematical Formalization
```
θ_coordination ≈ p_c^network

For diamond lattice (z=4): p_c = 0.388
Empirical: θ = 0.375

Difference: 3.5% (within measurement error)
```

### Evidence

**Theoretical (Strong)**:
- Dunbar's support clique: ~4-5 critical trust relationships
- Diamond lattice: z=4 coordination
- Bond percolation threshold: 0.3886 (exact)
- See SOCIAL_DIAMOND_MODEL.tex for full derivation

**Empirical (Strong)**:
- θ = 0.375 ± 0.025 overlaps with p_c = 0.388

### Verdict: ✅ VALIDATED
Strongest theoretical connection to physics. Core of Paper 2B.

---

## Law 11: The Learning Law

### Statement
> μ (learning coefficient) ≈ 0 historically. Civilizations don't learn from predecessors' collapses.

### Mathematical Formalization
```
θ_t+1 = θ_t + μ × ε_t

where ε_t = learning signal from collapse at time t

Observation: μ ≈ 0 (no trend in θ over 5000 years)
```

### Evidence

**Empirical (Moderate)**:
- θ stable at ~0.375 across all eras
- Modern collapses (Soviet, Yugoslavia) not obviously avoided
- But: we only have ~35 data points

**Theoretical (Weak)**:
- Collapse knowledge is tacit, not transmissible
- Each society believes "we're different"
- Generational memory loss (~80 years)

### Issues
- Selection bias: we only study collapses
- Some societies may have learned (Japan post-1945?)
- "Learning" hard to define operationally

### Verdict: ⚠️ OBSERVATIONAL
True historically but may not be fundamental.

---

## Law 12: The Glass Ceiling Law

### Statement
> K_max ≈ 0.85 is the coordination limit. No civilization exceeds this.

### Mathematical Formalization
```
max{K(t)} ≤ K_max ≈ 0.85

across all civilizations and time periods
```

### Evidence

**Empirical (Moderate)**:
- Highest observed: Nordic countries ~0.82
- Ancient peaks: Rome, Han, Achaemenid ~0.75
- No case exceeds 0.85

**Theoretical (Weak)**:
- Why 0.85 specifically?
- Dunbar's number: cognitive limits on trust networks?
- Diminishing returns on coordination?

### Issues
- Observation without theory
- Sample may not include peak cases
- Different harmonies may have different ceilings

### Proposed Derivation
```
K_max = f(Dunbar_number, network_density, information_capacity)

Hypothesis: K_max ≈ 1 - (1/Dunbar) ≈ 1 - 1/150 ≈ 0.993

This doesn't match 0.85 - needs work.
```

### Verdict: ⚠️ EMPIRICAL OBSERVATION
True in data but lacks theoretical foundation.

---

## Priority Ranking for Paper 2

### Must Include (Strong Evidence)
1. **Law 1 (Threshold)**: Core empirical finding
2. **Law 9 (Feedback)**: Well-established theory
3. **Law 10 (Percolation)**: Physics connection (defer details to Paper 2B)

### Should Include (Moderate Evidence)
4. **Law 2 (Cascade)**: Central to velocity equation
5. **Law 5 (Recovery)**: Important policy implication
6. **Law 7 (Intervention)**: Key practical takeaway

### Include with Caveats
7. **Law 3 (Network)**: Needs refinement
8. **Law 11 (Learning)**: Interesting observation
9. **Law 12 (Glass Ceiling)**: Empirical bound

### Defer or Remove
10. **Law 4 (Modernization)**: Unfalsifiable as stated
11. **Law 6 (Visibility)**: Untested
12. **Law 8 (Dark Trust)**: Needs operationalization

---

## Recommended Action

For Paper 2, present as **"Four Core Laws + Eight Supporting Regularities"**:

**Four Core Laws** (high confidence):
1. Threshold Law (θ ≈ 0.375)
2. Cascade Law (quadratic acceleration)
3. Feedback Law (trust begets trust)
4. Recovery Law (P ≈ 0.15)

**Eight Supporting Regularities** (lower confidence, in SI):
5-12: Network, Modernization, Visibility, Dark Trust, Percolation, Learning, Glass Ceiling, Intervention

This acknowledges the evidence hierarchy while retaining the full framework.
