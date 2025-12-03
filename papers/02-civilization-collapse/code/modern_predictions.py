#!/usr/bin/env python3
"""
Modern Predictions: K-Index Projections for Contemporary Societies

This module applies the collapse dynamics framework to current data,
generating testable predictions for modern democracies.

Usage:
    python modern_predictions.py
    python modern_predictions.py --country USA --years 20
    python modern_predictions.py --scenario intervention
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
import matplotlib.pyplot as plt

# Import from collapse_models
from collapse_models import (
    CascadeParameters,
    simulate_cascade,
    K_INDEX_THRESHOLD,
    TRUST_EQUILIBRIUM,
    TRUST_RESTORATION_RATE,
    MANUFACTURED_DISTRUST_SUSCEPTIBILITY
)


class InterventionType(Enum):
    """Types of interventions based on the Four Laws"""
    NONE = "none"
    TRUST_BUILDING = "trust_building"          # Address systemic failures
    COUNTER_PROPAGANDA = "counter_propaganda"  # Reduce manufactured distrust
    COMPLEXITY_REDUCTION = "complexity"         # Proactive simplification
    NETWORK_RESILIENCE = "network"             # Distribute dependencies
    FULL_PORTFOLIO = "full"                    # All interventions combined


@dataclass
class ModernSociety:
    """Current state of a modern society with K-Index indicators"""
    name: str

    # Current harmony values (0-1 scale)
    H1_governance: float      # Government effectiveness
    H2_economic: float        # Economic coordination
    H3_trust: float          # Social cohesion (measured from surveys)
    H4_complexity: float     # Institutional complexity
    H5_knowledge: float      # Knowledge preservation
    H6_wellbeing: float      # Population wellbeing
    H7_infrastructure: float # Technological infrastructure

    # Additional modern indicators
    polarization_index: float = 0.5      # 0=consensus, 1=total fragmentation
    elite_public_gap: float = 0.15       # Difference in trust levels
    manufactured_distrust: float = 0.02  # External trust erosion rate
    digital_exposure: float = 0.5        # Social media penetration

    # Trend data
    trust_trend: float = 0.0  # Annual change in H3

    def calculate_K(self) -> float:
        """Calculate current K-Index (geometric mean of harmonies)"""
        harmonies = [
            self.H1_governance,
            self.H2_economic,
            self.H3_trust,
            self.H4_complexity,
            self.H5_knowledge,
            self.H6_wellbeing,
            self.H7_infrastructure
        ]
        return np.prod(harmonies) ** (1/7)

    def effective_H3(self) -> float:
        """H3 adjusted for polarization"""
        return self.H3_trust * (1 - self.polarization_index)

    def coordination_stress_index(self) -> float:
        """Calculate CSI based on multiple indicators"""
        # Distance from threshold
        threshold_distance = max(0, K_INDEX_THRESHOLD - self.calculate_K())

        # Polarization contribution
        polarization_stress = self.polarization_index * 0.3

        # Elite-public gap contribution
        gap_stress = min(self.elite_public_gap / 0.30, 1.0) * 0.2

        # Trend contribution
        trend_stress = max(0, -self.trust_trend * 10) * 0.3

        return min(1.0, threshold_distance + polarization_stress + gap_stress + trend_stress)

    def to_parameters(self) -> CascadeParameters:
        """Convert to CascadeParameters for simulation"""
        return CascadeParameters(
            initial_harmonies={
                'H1': self.H1_governance,
                'H2': self.H2_economic,
                'H3': self.H3_trust,
                'H4': self.H4_complexity,
                'H5': self.H5_knowledge,
                'H6': self.H6_wellbeing,
                'H7': self.H7_infrastructure
            },
            manufactured_distrust=self.manufactured_distrust,
            trust_equilibrium=TRUST_EQUILIBRIUM,
            trust_restoration=TRUST_RESTORATION_RATE
        )


# Current estimates for major societies (as of 2024-2025)
CURRENT_SOCIETIES = {
    'USA': ModernSociety(
        name="United States",
        H1_governance=0.55,      # Functional but stressed institutions
        H2_economic=0.65,        # Strong economy, rising inequality
        H3_trust=0.30,           # Edelman/Gallup: historic lows
        H4_complexity=0.75,      # High complexity, federalism
        H5_knowledge=0.70,       # Strong universities, politicized media
        H6_wellbeing=0.55,       # Good for some, declining for many
        H7_infrastructure=0.60,  # Aging infrastructure
        polarization_index=0.78,
        elite_public_gap=0.32,
        manufactured_distrust=0.04,
        digital_exposure=0.85,
        trust_trend=-0.012
    ),

    'UK': ModernSociety(
        name="United Kingdom",
        H1_governance=0.58,
        H2_economic=0.55,        # Post-Brexit stress
        H3_trust=0.32,
        H4_complexity=0.65,
        H5_knowledge=0.68,
        H6_wellbeing=0.58,
        H7_infrastructure=0.55,
        polarization_index=0.62,
        elite_public_gap=0.23,
        manufactured_distrust=0.03,
        digital_exposure=0.82,
        trust_trend=-0.008
    ),

    'France': ModernSociety(
        name="France",
        H1_governance=0.52,      # Yellow vests, pension protests
        H2_economic=0.55,
        H3_trust=0.28,           # Among lowest in EU
        H4_complexity=0.70,
        H5_knowledge=0.65,
        H6_wellbeing=0.60,
        H7_infrastructure=0.65,
        polarization_index=0.58,
        elite_public_gap=0.20,
        manufactured_distrust=0.02,
        digital_exposure=0.75,
        trust_trend=-0.006
    ),

    'Germany': ModernSociety(
        name="Germany",
        H1_governance=0.68,
        H2_economic=0.62,
        H3_trust=0.40,
        H4_complexity=0.72,
        H5_knowledge=0.70,
        H6_wellbeing=0.65,
        H7_infrastructure=0.65,
        polarization_index=0.45,
        elite_public_gap=0.12,
        manufactured_distrust=0.02,
        digital_exposure=0.78,
        trust_trend=-0.004
    ),

    'Brazil': ModernSociety(
        name="Brazil",
        H1_governance=0.42,
        H2_economic=0.48,
        H3_trust=0.20,
        H4_complexity=0.55,
        H5_knowledge=0.50,
        H6_wellbeing=0.45,
        H7_infrastructure=0.50,
        polarization_index=0.75,
        elite_public_gap=0.28,
        manufactured_distrust=0.05,
        digital_exposure=0.70,
        trust_trend=-0.010
    ),

    'Nordic': ModernSociety(
        name="Nordic Countries (avg)",
        H1_governance=0.82,
        H2_economic=0.72,
        H3_trust=0.65,
        H4_complexity=0.70,
        H5_knowledge=0.78,
        H6_wellbeing=0.80,
        H7_infrastructure=0.75,
        polarization_index=0.25,
        elite_public_gap=0.05,
        manufactured_distrust=0.01,
        digital_exposure=0.88,
        trust_trend=-0.003
    ),

    'Hungary': ModernSociety(
        name="Hungary",
        H1_governance=0.45,      # Democratic backsliding
        H2_economic=0.52,
        H3_trust=0.25,
        H4_complexity=0.55,
        H5_knowledge=0.55,
        H6_wellbeing=0.52,
        H7_infrastructure=0.55,
        polarization_index=0.72,
        elite_public_gap=0.25,
        manufactured_distrust=0.06,  # State media control
        digital_exposure=0.65,
        trust_trend=-0.005
    )
}


def apply_intervention(
    society: ModernSociety,
    intervention: InterventionType,
    strength: float = 0.5
) -> ModernSociety:
    """
    Apply an intervention to a society's parameters.

    Args:
        society: Current state
        intervention: Type of intervention
        strength: Intervention intensity (0-1)

    Returns:
        Modified society parameters
    """
    # Create a copy
    modified = ModernSociety(
        name=f"{society.name} + {intervention.value}",
        H1_governance=society.H1_governance,
        H2_economic=society.H2_economic,
        H3_trust=society.H3_trust,
        H4_complexity=society.H4_complexity,
        H5_knowledge=society.H5_knowledge,
        H6_wellbeing=society.H6_wellbeing,
        H7_infrastructure=society.H7_infrastructure,
        polarization_index=society.polarization_index,
        elite_public_gap=society.elite_public_gap,
        manufactured_distrust=society.manufactured_distrust,
        digital_exposure=society.digital_exposure,
        trust_trend=society.trust_trend
    )

    if intervention == InterventionType.NONE:
        return modified

    if intervention == InterventionType.TRUST_BUILDING:
        # Address systemic failures, build bridging institutions
        modified.trust_trend += 0.01 * strength
        modified.elite_public_gap *= (1 - 0.3 * strength)
        modified.polarization_index *= (1 - 0.2 * strength)

    elif intervention == InterventionType.COUNTER_PROPAGANDA:
        # Media literacy, platform regulation, counter-messaging
        modified.manufactured_distrust *= (1 - 0.5 * strength)
        modified.polarization_index *= (1 - 0.15 * strength)

    elif intervention == InterventionType.COMPLEXITY_REDUCTION:
        # Proactive simplification of institutions
        modified.H4_complexity *= (1 - 0.2 * strength)
        modified.H1_governance *= (1 + 0.1 * strength)  # Simpler = more effective

    elif intervention == InterventionType.NETWORK_RESILIENCE:
        # Distribute trust dependencies
        modified.digital_exposure *= (1 - 0.2 * strength)
        modified.polarization_index *= (1 - 0.1 * strength)

    elif intervention == InterventionType.FULL_PORTFOLIO:
        # All interventions at reduced strength
        for int_type in [InterventionType.TRUST_BUILDING,
                        InterventionType.COUNTER_PROPAGANDA,
                        InterventionType.COMPLEXITY_REDUCTION,
                        InterventionType.NETWORK_RESILIENCE]:
            modified = apply_intervention(modified, int_type, strength * 0.5)

    return modified


def project_society(
    society: ModernSociety,
    years: int = 20,
    intervention: InterventionType = InterventionType.NONE,
    intervention_strength: float = 0.5,
    external_shocks: Optional[List[Tuple[int, float]]] = None
) -> Dict:
    """
    Project a society's trajectory over time.

    Args:
        society: Starting state
        years: Projection horizon
        intervention: Type of intervention to apply
        intervention_strength: Intensity of intervention
        external_shocks: List of (year, magnitude) tuples for shocks

    Returns:
        Dictionary with projection results
    """
    # Apply intervention to parameters
    if intervention != InterventionType.NONE:
        society = apply_intervention(society, intervention, intervention_strength)

    # Convert to simulation parameters
    params = society.to_parameters()

    # Set manufactured distrust
    params.manufactured_distrust = society.manufactured_distrust

    # Add external shocks
    if external_shocks:
        # Convert to simulation format
        shock_times = [s[0] for s in external_shocks]
        shock_magnitudes = [s[1] for s in external_shocks]
        # Note: Full shock integration would require modifying simulate_cascade

    # Run simulation
    n_steps = years * 12  # Monthly resolution
    dt = 1/12  # One month

    results = simulate_cascade(params, n_steps=n_steps, dt=dt)

    # Calculate key metrics
    K_trajectory = results['K']
    H3_trajectory = results['H3']

    # Find threshold crossing
    threshold_year = None
    for i, K in enumerate(K_trajectory):
        if K < K_INDEX_THRESHOLD:
            threshold_year = i / 12  # Convert to years
            break

    # Calculate risks
    final_K = K_trajectory[-1]
    min_K = np.min(K_trajectory)

    return {
        'society': society.name,
        'intervention': intervention.value,
        'years': years,
        'K_initial': K_trajectory[0],
        'K_final': final_K,
        'K_minimum': min_K,
        'K_trajectory': K_trajectory,
        'H3_trajectory': H3_trajectory,
        'threshold_crossed': threshold_year is not None,
        'threshold_year': threshold_year,
        'cascade_risk': 'high' if threshold_year and threshold_year < 10 else
                       'moderate' if threshold_year else 'low',
        'effective_H3_final': final_K  # Approximation
    }


def compare_scenarios(
    society: ModernSociety,
    years: int = 20
) -> Dict[str, Dict]:
    """
    Compare multiple intervention scenarios for a society.

    Args:
        society: Starting state
        years: Projection horizon

    Returns:
        Dictionary mapping intervention type to projection results
    """
    scenarios = {}

    for intervention in InterventionType:
        scenarios[intervention.value] = project_society(
            society, years, intervention
        )

    return scenarios


def generate_prediction_report(country: str = 'USA', years: int = 20) -> str:
    """
    Generate a detailed prediction report for a country.

    Args:
        country: Country code from CURRENT_SOCIETIES
        years: Projection horizon

    Returns:
        Formatted report string
    """
    if country not in CURRENT_SOCIETIES:
        return f"Unknown country: {country}. Available: {list(CURRENT_SOCIETIES.keys())}"

    society = CURRENT_SOCIETIES[country]
    scenarios = compare_scenarios(society, years)

    report = []
    report.append(f"\n{'='*70}")
    report.append(f"K-INDEX PROJECTION REPORT: {society.name}")
    report.append(f"{'='*70}\n")

    # Current state
    report.append("CURRENT STATE (2024-2025)")
    report.append("-" * 40)
    report.append(f"K-Index:            {society.calculate_K():.3f}")
    report.append(f"H3 (Trust):         {society.H3_trust:.3f}")
    report.append(f"Effective H3:       {society.effective_H3():.3f}")
    report.append(f"Polarization:       {society.polarization_index:.2f}")
    report.append(f"Elite-Public Gap:   {society.elite_public_gap:.2f}")
    report.append(f"Trust Trend:        {society.trust_trend:+.3f}/year")
    report.append(f"CSI:                {society.coordination_stress_index():.3f}")
    report.append(f"\nThreshold:          {K_INDEX_THRESHOLD:.3f}")
    report.append(f"Distance to θ:      {society.calculate_K() - K_INDEX_THRESHOLD:+.3f}")

    # Scenario comparisons
    report.append(f"\n\n{years}-YEAR PROJECTIONS BY SCENARIO")
    report.append("-" * 40)

    for scenario_name, results in scenarios.items():
        report.append(f"\n{scenario_name.upper()}")
        report.append(f"  K-Index: {results['K_initial']:.3f} → {results['K_final']:.3f}")
        report.append(f"  Minimum K: {results['K_minimum']:.3f}")
        if results['threshold_crossed']:
            report.append(f"  ⚠️  THRESHOLD CROSSED at year {results['threshold_year']:.1f}")
        else:
            report.append(f"  ✓ Threshold NOT crossed")
        report.append(f"  Cascade Risk: {results['cascade_risk']}")

    # Key insights
    report.append(f"\n\nKEY INSIGHTS")
    report.append("-" * 40)

    baseline = scenarios['none']
    best = scenarios['full']

    if baseline['threshold_crossed'] and not best['threshold_crossed']:
        report.append("• Full intervention portfolio PREVENTS threshold crossing")
        report.append(f"• Without intervention: cascade begins ~year {baseline['threshold_year']:.1f}")
        report.append(f"• With intervention: K-Index maintained at {best['K_final']:.3f}")
    elif not baseline['threshold_crossed']:
        report.append("• Society remains above threshold without intervention")
        report.append("• Intervention improves trajectory but not critical")
    else:
        report.append("• Even full intervention may not prevent threshold crossing")
        report.append("• Situation requires extraordinary measures")

    # Recommendations
    report.append(f"\n\nRECOMMENDATIONS")
    report.append("-" * 40)

    if society.manufactured_distrust > 0.03:
        report.append("• URGENT: Counter manufactured distrust (platform regulation, media literacy)")
    if society.polarization_index > 0.6:
        report.append("• HIGH PRIORITY: Depolarization initiatives (bridging programs)")
    if society.elite_public_gap > 0.20:
        report.append("• Address elite-public disconnect (democratic reforms, responsiveness)")
    if society.trust_trend < -0.005:
        report.append("• Arrest trust decline (address root causes of distrust)")

    report.append(f"\n{'='*70}\n")

    return "\n".join(report)


def plot_scenarios(country: str = 'USA', years: int = 20):
    """
    Create visualization of scenarios for a country.

    Args:
        country: Country code
        years: Projection horizon
    """
    if country not in CURRENT_SOCIETIES:
        print(f"Unknown country: {country}")
        return

    society = CURRENT_SOCIETIES[country]
    scenarios = compare_scenarios(society, years)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # K-Index trajectories
    time = np.linspace(0, years, len(scenarios['none']['K_trajectory']))

    colors = {
        'none': 'red',
        'trust_building': 'blue',
        'counter_propaganda': 'green',
        'complexity': 'purple',
        'network': 'orange',
        'full': 'black'
    }

    for scenario_name, results in scenarios.items():
        ax1.plot(time, results['K_trajectory'],
                label=scenario_name, color=colors.get(scenario_name, 'gray'),
                linewidth=2 if scenario_name in ['none', 'full'] else 1)

    ax1.axhline(y=K_INDEX_THRESHOLD, color='red', linestyle='--',
                label=f'Threshold (θ={K_INDEX_THRESHOLD})')
    ax1.set_xlabel('Years from Present')
    ax1.set_ylabel('K-Index')
    ax1.set_title(f'{society.name}: K-Index Projections by Intervention')
    ax1.legend(loc='lower left')
    ax1.grid(True, alpha=0.3)

    # Final K comparison
    final_Ks = {name: results['K_final'] for name, results in scenarios.items()}
    names = list(final_Ks.keys())
    values = list(final_Ks.values())
    colors_list = [colors.get(n, 'gray') for n in names]

    bars = ax2.bar(names, values, color=colors_list, alpha=0.7)
    ax2.axhline(y=K_INDEX_THRESHOLD, color='red', linestyle='--',
                label=f'Threshold (θ={K_INDEX_THRESHOLD})')
    ax2.set_ylabel('Final K-Index')
    ax2.set_title(f'{society.name}: Final K-Index by Intervention ({years} years)')
    ax2.set_xticklabels(names, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(f'outputs/figures/{country.lower()}_scenarios.png', dpi=150)
    plt.show()


def global_risk_assessment() -> str:
    """
    Generate global risk assessment across all tracked societies.

    Returns:
        Formatted risk assessment report
    """
    report = []
    report.append("\n" + "=" * 70)
    report.append("GLOBAL COORDINATION RISK ASSESSMENT")
    report.append("K-Index Framework Analysis")
    report.append("=" * 70 + "\n")

    # Calculate metrics for all societies
    assessments = []
    for code, society in CURRENT_SOCIETIES.items():
        K = society.calculate_K()
        CSI = society.coordination_stress_index()
        effective_H3 = society.effective_H3()

        # Determine risk level
        if K < K_INDEX_THRESHOLD or CSI > 0.4:
            risk = "CRITICAL"
        elif K < 0.50 or CSI > 0.3:
            risk = "HIGH"
        elif K < 0.55 or CSI > 0.2:
            risk = "MODERATE"
        else:
            risk = "LOW"

        assessments.append({
            'code': code,
            'name': society.name,
            'K': K,
            'H3': society.H3_trust,
            'effective_H3': effective_H3,
            'CSI': CSI,
            'risk': risk
        })

    # Sort by risk
    risk_order = {'CRITICAL': 0, 'HIGH': 1, 'MODERATE': 2, 'LOW': 3}
    assessments.sort(key=lambda x: (risk_order[x['risk']], -x['CSI']))

    # Report by risk level
    for risk_level in ['CRITICAL', 'HIGH', 'MODERATE', 'LOW']:
        matching = [a for a in assessments if a['risk'] == risk_level]
        if matching:
            report.append(f"\n{risk_level} RISK")
            report.append("-" * 40)
            for a in matching:
                report.append(
                    f"  {a['name']:25s} K={a['K']:.3f}  H3={a['H3']:.2f}  "
                    f"CSI={a['CSI']:.2f}"
                )

    # Global summary
    report.append("\n\nGLOBAL SUMMARY")
    report.append("-" * 40)

    critical_count = sum(1 for a in assessments if a['risk'] == 'CRITICAL')
    high_count = sum(1 for a in assessments if a['risk'] == 'HIGH')

    report.append(f"Societies at CRITICAL risk: {critical_count}")
    report.append(f"Societies at HIGH risk: {high_count}")

    # Global cascade risk
    global_risk = (critical_count * 3 + high_count * 2) / (len(assessments) * 3)
    report.append(f"\nGlobal Cascade Risk Index: {global_risk:.2f}")

    if global_risk > 0.5:
        report.append("\n⚠️  WARNING: Global cascade risk is ELEVATED")
        report.append("   Multiple major societies at or near threshold")
        report.append("   Cascade in one could trigger cascade in others")

    report.append("\n" + "=" * 70 + "\n")

    return "\n".join(report)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="K-Index Modern Predictions")
    parser.add_argument('--country', type=str, default='USA',
                       help='Country code (USA, UK, France, Germany, Brazil, Nordic, Hungary)')
    parser.add_argument('--years', type=int, default=20,
                       help='Projection horizon in years')
    parser.add_argument('--global-risk', action='store_true',
                       help='Generate global risk assessment')
    parser.add_argument('--plot', action='store_true',
                       help='Generate scenario plots')

    args = parser.parse_args()

    if args.global_risk:
        print(global_risk_assessment())
    else:
        print(generate_prediction_report(args.country, args.years))

        if args.plot:
            plot_scenarios(args.country, args.years)
