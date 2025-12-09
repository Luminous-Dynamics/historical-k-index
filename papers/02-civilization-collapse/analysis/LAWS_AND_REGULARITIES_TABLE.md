# Laws and Regularities Classification

**Paper 2C: The Coordination Collapse Framework**

*Epistemic Status Classification for Each Relationship*

---

## Overview

This document classifies the coordination collapse relationships into three tiers based on their epistemic status:

1. **Core Laws** - Strong theoretical derivation + solid empirical support
2. **Supporting Regularities** - Empirical patterns with theoretical grounding but more uncertainty
3. **Theoretical Extensions** - Frontier research, speculative but mathematically coherent

This hierarchy is deliberate: it invites empirical and theoretical work to upgrade regularities to laws, rather than presenting all relationships as equally settled.

---

## Classification Summary

| ID | Name | Type | Evidence | Equation |
|----|------|------|----------|----------|
| **1** | Threshold | **Core Law** | Strong | θ = C/(B+C) ≈ 0.375 |
| **2** | Cascade Dynamics | **Core Law** | Strong | dH₃/dt = -λ₁(θ-H₃) - λ₂(θ-H₃)² |
| **5** | Recovery | **Core Law** | Moderate-Strong | P(recovery) ≈ 0.15 × e^(-0.05×years) |
| **9** | Positive Feedback | **Core Law** | Strong | d²H₃/dt² > 0 when H₃ > θ |
| **10** | Percolation | **Core Law** | Strong | θ ≈ p_c(z=4) ≈ 0.388 |
| **3** | Network/Redundancy | Regularity | Moderate | v_cascade ∝ 1/√R |
| **4** | Modernization | Regularity | Moderate | λ = λ_base × F_info × F_econ × F_network |
| **6** | Visibility (Masked Trust) | Regularity | Weak | H₃_apparent = H₃_true + H₃_masked(R) |
| **7** | Intervention ROI | Regularity | Moderate | ROI ≈ 10× above θ vs 1/10 below |
| **8** | Dark Trust | Regularity | Weak | H₃_total = H₃_light + H₃_dark |
| **11** | Learning (μ ≈ 0) | Regularity | Moderate | θ(t) ≈ θ₀ over 5000 years |
| **12** | Glass Ceiling | Regularity | Moderate | K_max ≈ 0.85 |
| **13** | Information Hub | Extension | Theoretical | I(H₃; H₋₃) = max_i I(H_i; H₋ᵢ) |
| **14** | Phase Transition | Extension | Theoretical | F(m,T) = a(T)m² + bm⁴; β=½ |
| **15** | Metacognitive | Extension | Theoretical | M = K × R_model × T_response |
| **16** | Evolutionary Stability | Extension | Theoretical | dp/dt = p(1-p)(-c) < 0 |
| **17** | AI Coordination Paradox | Extension | Theoretical | dH₃/dt_AI = dH₃/dt(1 + A_pos) |

---

## Tier 1: Core Laws (5 Laws)

These have clean mathematical derivations AND solid empirical support. The five Core Laws are: **Threshold (1), Cascade (2), Recovery (5), Feedback (9), and Percolation (10)**.

### Law 1: Coordination Threshold

**Statement**: There exists a critical trust threshold θ ≈ 0.375 below which defection becomes the Nash equilibrium and coordination collapse becomes highly probable.

**Derivation**: Game-theoretic from Prisoner's Dilemma: θ = C/(B+C) where B=benefit, C=cost of cooperation.

**Evidence Status**: **Strong**
- LOOCV validation on 35 historical cases: 94% predictive accuracy
- Independent derivations converge: PD (0.375), half-entropy (0.382), percolation (0.388)
- See MAIN_PAPER Figure 2, SI Table S3

**Note on θ value**: The value θ ≈ 0.375 is model-dependent, not a fundamental constant. Different game payoff structures yield different thresholds. The empirical estimate θ_emp ≈ 0.375 ± 0.025 is consistent with multiple theoretical derivations. The proximity to 1/φ² ≈ 0.382 is noted as a mathematical curiosity, not claimed as evidence.

---

### Law 2: Cascade Dynamics

**Statement**: Below threshold, trust decline accelerates quadratically:

```
dH₃/dt = -λ₁(θ - H₃) - λ₂(θ - H₃)²
```

**Derivation**: From contagion dynamics with positive feedback below threshold.

**Evidence Status**: **Strong**
- R² ≈ 0.74 across 35 historical collapse cases
- Calibrated λ₁ ≈ 0.015, λ₂ ≈ 0.08 (per decade)
- See MAIN_PAPER Figure 3, SI Section 4.2

---

### Law 9: Positive Feedback

**Statement**: Above θ, cooperation reinforces itself (virtuous cycle); below θ, defection reinforces itself (vicious cycle).

```
If H₃ > θ: d²H₃/dt² > 0 (recovery accelerates)
If H₃ < θ: d²H₃/dt² < 0 (collapse accelerates)
```

**Derivation**: Game-theoretic from repeated game dynamics and trust reciprocity.

**Evidence Status**: **Strong**
- Supported by Ostrom (1990), Axelrod (1984), social capital literature
- Observed in 28/35 historical cases
- See MAIN_PAPER Section 5.1

---

### Law 10: Percolation

**Statement**: The threshold θ corresponds to the percolation transition of the coordination network.

```
θ ≈ p_c(z=4) = (z-1)^(-1) ≈ 0.333 to 0.388
```

**Derivation**: Network percolation theory; coordination as path connectivity.

**Evidence Status**: **Strong**
- Independent mathematical derivation yields p_c ≈ 0.388 for z=4 networks
- Overlaps with empirical θ_emp ≈ 0.375 within uncertainty
- See SI Section 6.1, Figure S12

---

### Law 5: Recovery

**Statement**: Recovery probability decays exponentially with time below threshold.

```
P(recovery | H₃ < θ) ≈ 0.15 × e^(-0.05 × years_below_θ)
```

**Derivation**: Hazard model fitted to recovery attempts in historical data.

**Evidence Status**: **Moderate-Strong**
- Based on 12 recovery attempts in dataset
- Binomial CI [0.08, 0.22] for base rate
- See MAIN_PAPER Table 2, SI Section 5.3

**Why Core Law**: Recovery dynamics are directly derived from threshold mechanics and validated empirically.

---

## Tier 2: Supporting Regularities (7 Laws)

Empirical patterns with theoretical grounding but more uncertainty.

### Regularity 3: Network/Redundancy

**Statement**: Cascade velocity inversely proportional to network redundancy.

```
v_cascade ∝ λ(θ - H₃)² / √R
```

**Evidence**: Rome (R≈3) vs Soviet Union (R≈1.8) collapse speed comparison.

**Status**: **Moderate** - Fits case studies, needs broader validation.

---

### Regularity 4: Modernization Pressure

**Statement**: Modernization increases cascade speed through multiple channels.

```
λ = λ_base × F_info × F_econ × F_network
```

Where F factors represent information speed, economic integration, and institutional coupling.

**Evidence**: λ ≈ 21× pre-industrial for modern systems.

**Status**: **Moderate** - Predictive but difficult to falsify independently.

---

### Regularity 6: Visibility (Masked Trust)

**Statement**: Observable trust can mask underlying fragility.

```
H₃_apparent = H₃_true + H₃_masked(R)
H₃_masked ≤ 0.25 (bounded)
```

**Evidence**: Pre-collapse optimism observed in multiple cases.

**Status**: **Weak** - Conceptually important but hard to operationalize.

---

### Regularity 7: Intervention ROI Asymmetry

**Statement**: Intervention returns highly asymmetric around threshold.

```
ROI(H₃ > θ) ≈ 10× to 30×
ROI(H₃ < θ) ≈ 0.1× to 0.3×
```

**Evidence**: Comparative effectiveness analysis across interventions.

**Status**: **Moderate** - Policy-relevant, supported by case studies.

---

### Regularity 8: Dark Trust

**Statement**: Total coordination capacity includes hidden reserves.

```
H₃_total = H₃_light + H₃_dark
```

Where H₃_dark represents informal networks, shadow institutions, underground cooperation.

**Evidence**: Post-collapse resilience variations.

**Status**: **Weak** - Conceptually crucial but still being operationalized.

---

### Regularity 11: Threshold Stability (μ ≈ 0)

**Statement**: Civilizations do not learn to lower θ over time.

```
dθ/dt ≈ μ ≈ 0 over historical record
```

**Evidence**: θ stable across 5000 years of civilization.

**Status**: **Moderate** - Observational; absence of evidence vs evidence of absence.

---

### Regularity 12: Glass Ceiling

**Statement**: Maximum sustainable K bounded below 1.

```
K_max ≈ 0.85 ± 0.05
```

**Evidence**: No civilization sustained K > 0.9 for extended periods.

**Status**: **Moderate** - Strong empirical bound, theoretical derivation in progress.

---

## Tier 3: Theoretical Extensions

Frontier research—mathematically coherent but speculative.

### Extension 13: Information Hub

**Statement**: H₃ (trust) has highest mutual information with other harmonies.

```
I(H₃; H₋₃) = max_i I(H_i; H₋ᵢ)
```

And θ corresponds to half-maximum coordination entropy: S_coord(θ) = S_max/2.

**Status**: **Theoretical** - Plausible framework, needs explicit derivation and data validation.

---

### Extension 14: Phase Transition

**Statement**: Coordination collapse follows mean-field second-order transition.

```
F(m,T) = a(T)m² + bm⁴
β = 1/2, γ = 1, ν = 1/2 (mean-field exponents)
```

**Status**: **Theoretical** - Elegant mapping but historical data too sparse to estimate exponents rigorously.

---

### Extension 15: Metacognitive Collapse

**Statement**: Civilizations lose self-awareness before collapse.

```
M = K × R_model × T_response
Collapse when M < C_env
```

**Status**: **Theoretical** - Interesting framework for "why they can't see it coming"; needs operationalization.

---

### Extension 16: Evolutionary Stability

**Statement**: Under baseline replicator dynamics, cooperation is not ESS.

```
dp/dt = p(1-p)(-c) < 0
```

**Scope limitation**: This applies to one-shot, well-mixed populations without institutions. Does NOT contradict network reciprocity, repeated games, or group selection mechanisms.

**Status**: **Theoretical** - Clean math but claim must be scoped carefully.

---

### Extension 17: AI Coordination Paradox

**Statement**: AI amplifies coordination dynamics in both directions.

```
dH₃/dt_AI = dH₃/dt_nat × (1 + A_pos(t))
dλ/dt_AI = dλ/dt_nat × (1 + A_neg(t))
```

**Status**: **Theoretical** - Framework for analyzing AI impact; connects to Technology Evaluation Matrix.

---

## How to Read This Classification

### For Academic Reviewers

We distinguish between a small set of **Core Laws** (threshold, cascade, feedback, percolation) that we claim have strong support, and a larger set of **Supporting Regularities** that capture observed patterns but remain open to refinement.

This hierarchy:
- Shows epistemic humility
- Identifies which claims are grounded vs speculative
- Invites empirical work to upgrade regularities to laws

### For Practitioners

**Core Laws** provide hard constraints on what trajectories are sustainable.

**Regularities** provide guidance on mechanisms and interventions, with appropriate uncertainty.

**Extensions** provide conceptual frameworks for frontier issues (AI, cosmic implications).

---

## Evidence Summary

| Tier | Count | Average Evidence | Use |
|------|-------|------------------|-----|
| Core Laws | 5 | Strong | Hard constraints |
| Regularities | 7 | Moderate-Weak | Guidance with uncertainty |
| Extensions | 5 | Theoretical | Frontier frameworks |
| **Total** | **17** | | |

---

## Citation

When referencing this classification:

```
Coordination Physics Framework. (2025). Laws and Regularities Classification
for Paper 2C: The Coordination Collapse Framework. [Working document].
```

---

**Status**: Living document
**Last Updated**: December 2025
**Purpose**: Distinguish epistemic status of framework components
