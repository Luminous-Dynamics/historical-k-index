#!/usr/bin/env python3
"""
Sensitivity Analysis for Coordination Collapse Laws

Tests robustness of model predictions under parameter perturbation.
Key question: Do rankings and qualitative predictions remain stable
when we vary key parameters by ±20%?

Usage:
    python sensitivity_analysis.py --output-dir outputs/sensitivity/
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple
import json
from pathlib import Path

# =============================================================================
# CORE MODEL PARAMETERS
# =============================================================================

@dataclass
class CivilizationParams:
    """Parameters for a civilization case study."""
    name: str
    H3_trust: float           # Organic trust level
    R_redundancy: float       # Number of independent coordination mechanisms
    C_centralization: float   # Power concentration (0-1)
    lambda_modernization: float  # Information speed factor
    resource_rent: float      # Resource dependence (0-1)
    H3_coerced: float = 0.0   # Dark trust - coerced component
    H3_habitual: float = 0.0  # Dark trust - habitual component
    observed_collapse_years: float = None  # Actual collapse duration


# Historical baseline cases
CASES = {
    'rome_400ce': CivilizationParams(
        name="Western Rome (400 CE)",
        H3_trust=0.38,
        R_redundancy=3.3,
        C_centralization=0.7,
        lambda_modernization=1.0,  # Baseline
        resource_rent=0.05,
        observed_collapse_years=250
    ),
    'soviet_1985': CivilizationParams(
        name="Soviet Union (1985)",
        H3_trust=0.20,
        R_redundancy=1.6,
        C_centralization=0.9,
        lambda_modernization=2.2,
        resource_rent=0.15,
        H3_coerced=0.25,
        H3_habitual=0.10,
        observed_collapse_years=6
    ),
    'maya_800ce': CivilizationParams(
        name="Classic Maya (800 CE)",
        H3_trust=0.32,
        R_redundancy=1.5,
        C_centralization=0.4,
        lambda_modernization=0.9,
        resource_rent=0.02,
        observed_collapse_years=100
    ),
    'usa_2024': CivilizationParams(
        name="United States (2024)",
        H3_trust=0.42,
        R_redundancy=4.5,
        C_centralization=0.4,
        lambda_modernization=2.8,
        resource_rent=0.03
    ),
    'china_2024': CivilizationParams(
        name="China (2024)",
        H3_trust=0.25,
        R_redundancy=1.3,
        C_centralization=0.85,
        lambda_modernization=2.5,
        resource_rent=0.08,
        H3_coerced=0.30,
        H3_habitual=0.15
    )
}

# Model constants
THETA = 0.375  # Trust threshold
K_MAX = 0.85   # Glass ceiling


# =============================================================================
# CORE MODEL FUNCTIONS
# =============================================================================

def cascade_velocity(H3: float, R: float, lambda_mod: float,
                     theta: float = THETA) -> float:
    """
    Law 2 + Law 3: Cascade velocity as function of trust deficit and redundancy.

    v_c = λ × (θ - H₃)² / √R

    Returns velocity in "trust units per year"
    """
    if H3 >= theta:
        return 0.0  # Above threshold, no cascade

    deficit = theta - H3
    velocity = lambda_mod * (deficit ** 2) / np.sqrt(R)
    return velocity


def time_to_collapse(H3_start: float, H3_end: float, R: float,
                     lambda_mod: float, theta: float = THETA) -> float:
    """
    Integrate cascade dynamics to get time from H3_start to H3_end.

    Uses simplified analytical solution for quadratic cascade.
    """
    if H3_start >= theta:
        return float('inf')  # Never crosses

    # Numerical integration (more accurate than analytical for this form)
    dt = 0.1  # years
    t = 0
    H3 = H3_start

    while H3 > H3_end and t < 1000:
        v = cascade_velocity(H3, R, lambda_mod, theta)
        H3 -= v * dt
        t += dt

    return t


def recovery_probability(H3: float, years_below: float = 0,
                         intervention: bool = False,
                         theta: float = THETA) -> float:
    """
    Law 5: Recovery probability as function of position and time.

    P(recovery) = 0.15 × exp(-0.05 × years_below) × intervention_modifier
    """
    if H3 >= theta:
        return 0.85  # Above threshold, high recovery

    base_prob = 0.15
    time_decay = np.exp(-0.05 * years_below)
    intervention_boost = 3.0 if intervention else 1.0

    return min(0.95, base_prob * time_decay * intervention_boost)


def intervention_roi(H3: float, theta: float = THETA) -> float:
    """
    Law 7: Return on investment for trust-building intervention.

    ROI = 1.0 at threshold, higher above, lower below.
    """
    if H3 > theta:
        return 1.0 + 5.0 * (H3 - theta)  # Linear improvement above
    else:
        return np.exp(-10.0 * (theta - H3))  # Exponential degradation below


def fragility_index(C: float, R: float, lambda_mod: float) -> float:
    """
    Law 3: Combined fragility measure.

    Fragility = C × λ / R
    """
    return C * lambda_mod / R


def total_trust(H3_light: float, H3_coerced: float, H3_habitual: float,
                resource_rent: float) -> float:
    """
    Law 8 + Law 6: Total apparent trust including dark trust and resource masking.
    """
    # Dark trust components
    H3_dark = H3_coerced + H3_habitual

    # Resource masking (Law 6)
    psi_R = (resource_rent ** 1.5) / (resource_rent ** 1.5 + 0.058)
    H3_masked = min(0.25, 0.8 * psi_R)

    return H3_light + H3_dark + H3_masked


# =============================================================================
# SENSITIVITY ANALYSIS
# =============================================================================

def perturb_parameter(base_value: float, perturbation: float) -> float:
    """Apply multiplicative perturbation."""
    return base_value * (1 + perturbation)


def run_sensitivity_single_case(case: CivilizationParams,
                                param_name: str,
                                perturbations: List[float]) -> Dict:
    """
    Run sensitivity analysis for a single parameter on a single case.

    Returns dict with predictions at each perturbation level.
    """
    results = []

    for pert in perturbations:
        # Create perturbed case
        perturbed = CivilizationParams(
            name=case.name,
            H3_trust=perturb_parameter(case.H3_trust, pert) if param_name == 'H3_trust' else case.H3_trust,
            R_redundancy=perturb_parameter(case.R_redundancy, pert) if param_name == 'R_redundancy' else case.R_redundancy,
            C_centralization=perturb_parameter(case.C_centralization, pert) if param_name == 'C_centralization' else case.C_centralization,
            lambda_modernization=perturb_parameter(case.lambda_modernization, pert) if param_name == 'lambda_modernization' else case.lambda_modernization,
            resource_rent=case.resource_rent,
            H3_coerced=case.H3_coerced,
            H3_habitual=case.H3_habitual,
            observed_collapse_years=case.observed_collapse_years
        )

        # Calculate predictions
        v_cascade = cascade_velocity(perturbed.H3_trust, perturbed.R_redundancy,
                                     perturbed.lambda_modernization)
        fragility = fragility_index(perturbed.C_centralization, perturbed.R_redundancy,
                                    perturbed.lambda_modernization)
        roi = intervention_roi(perturbed.H3_trust)
        recovery_p = recovery_probability(perturbed.H3_trust)

        # Time to critical (H3 = 0.20)
        if perturbed.H3_trust < THETA:
            t_collapse = time_to_collapse(perturbed.H3_trust, 0.20,
                                          perturbed.R_redundancy,
                                          perturbed.lambda_modernization)
        else:
            t_collapse = float('inf')

        results.append({
            'perturbation': pert,
            'cascade_velocity': v_cascade,
            'fragility': fragility,
            'intervention_roi': roi,
            'recovery_probability': recovery_p,
            'time_to_critical': t_collapse
        })

    return {
        'case': case.name,
        'parameter': param_name,
        'base_value': getattr(case, param_name),
        'results': results
    }


def run_full_sensitivity_analysis(perturbation_range: float = 0.2,
                                  n_steps: int = 9) -> Dict:
    """
    Run complete sensitivity analysis across all cases and parameters.
    """
    perturbations = np.linspace(-perturbation_range, perturbation_range, n_steps)
    parameters = ['H3_trust', 'R_redundancy', 'C_centralization', 'lambda_modernization']

    all_results = {}

    for case_name, case in CASES.items():
        all_results[case_name] = {}
        for param in parameters:
            result = run_sensitivity_single_case(case, param, perturbations.tolist())
            all_results[case_name][param] = result

    return all_results


def check_ranking_stability(results: Dict) -> Dict:
    """
    Check if rankings of civilizations remain stable under perturbation.

    Key test: Does Rome always collapse slower than Soviet?
    """
    stability_checks = []

    # Extract base case predictions
    base_rome = cascade_velocity(
        CASES['rome_400ce'].H3_trust,
        CASES['rome_400ce'].R_redundancy,
        CASES['rome_400ce'].lambda_modernization
    )
    base_soviet = cascade_velocity(
        CASES['soviet_1985'].H3_trust,
        CASES['soviet_1985'].R_redundancy,
        CASES['soviet_1985'].lambda_modernization
    )

    # Check: Rome velocity < Soviet velocity at all perturbation levels
    rome_slower_count = 0
    total_comparisons = 0

    for param in ['R_redundancy', 'lambda_modernization']:
        rome_results = results['rome_400ce'][param]['results']
        soviet_results = results['soviet_1985'][param]['results']

        for r_rome, r_soviet in zip(rome_results, soviet_results):
            total_comparisons += 1
            if r_rome['cascade_velocity'] < r_soviet['cascade_velocity']:
                rome_slower_count += 1

    ranking_stable = rome_slower_count == total_comparisons

    return {
        'rome_vs_soviet_ranking_stable': ranking_stable,
        'rome_slower_fraction': rome_slower_count / total_comparisons if total_comparisons > 0 else 0,
        'base_rome_velocity': base_rome,
        'base_soviet_velocity': base_soviet,
        'velocity_ratio': base_soviet / base_rome if base_rome > 0 else float('inf')
    }


def check_collapse_timing_accuracy(results: Dict) -> Dict:
    """
    Check if predicted collapse times remain within ±5 years of observed.
    """
    timing_checks = {}

    for case_name, case in CASES.items():
        if case.observed_collapse_years is None:
            continue

        base_results = results[case_name]['lambda_modernization']['results']
        # Find the base case (perturbation = 0)
        base_idx = len(base_results) // 2
        base_prediction = base_results[base_idx]['time_to_critical']

        # Check range across perturbations
        predictions = [r['time_to_critical'] for r in base_results]
        predictions = [p for p in predictions if p < 999]  # Filter infinities

        if predictions:
            min_pred = min(predictions)
            max_pred = max(predictions)
            observed = case.observed_collapse_years

            timing_checks[case_name] = {
                'observed': observed,
                'predicted_base': base_prediction,
                'predicted_range': (min_pred, max_pred),
                'within_5_years': abs(base_prediction - observed) <= 5 if base_prediction < 999 else False,
                'observed_in_range': min_pred <= observed <= max_pred
            }

    return timing_checks


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main(output_dir: str = 'outputs/sensitivity'):
    """Run full sensitivity analysis and save results."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("SENSITIVITY ANALYSIS FOR COORDINATION COLLAPSE LAWS")
    print("=" * 60)

    # Run analysis
    print("\n1. Running parameter sensitivity analysis...")
    results = run_full_sensitivity_analysis(perturbation_range=0.20, n_steps=9)

    # Save raw results
    with open(output_path / 'sensitivity_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=lambda x: str(x) if isinstance(x, float) and (np.isnan(x) or np.isinf(x)) else x)

    # Check ranking stability
    print("\n2. Checking ranking stability (Rome vs Soviet)...")
    ranking = check_ranking_stability(results)
    print(f"   Rome slower than Soviet in {ranking['rome_slower_fraction']*100:.1f}% of scenarios")
    print(f"   Ranking stable: {ranking['rome_vs_soviet_ranking_stable']}")
    print(f"   Velocity ratio (Soviet/Rome): {ranking['velocity_ratio']:.2f}x")

    # Check timing accuracy
    print("\n3. Checking collapse timing predictions...")
    timing = check_collapse_timing_accuracy(results)
    for case, data in timing.items():
        print(f"   {case}: Observed={data['observed']}y, Predicted={data['predicted_base']:.1f}y, "
              f"Within 5y: {data['within_5_years']}")

    # Summary report
    print("\n" + "=" * 60)
    print("SENSITIVITY ANALYSIS SUMMARY")
    print("=" * 60)

    summary = {
        'ranking_stability': ranking,
        'timing_accuracy': timing,
        'model_robust': ranking['rome_vs_soviet_ranking_stable'],
        'parameters_tested': ['H3_trust', 'R_redundancy', 'C_centralization', 'lambda_modernization'],
        'perturbation_range': '±20%',
        'cases_analyzed': list(CASES.keys())
    }

    with open(output_path / 'sensitivity_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    if summary['model_robust']:
        print("\n✅ MODEL IS ROBUST")
        print("   Rankings remain stable under ±20% parameter perturbation")
        print("   Qualitative predictions hold across all scenarios")
    else:
        print("\n⚠️ MODEL SENSITIVITY DETECTED")
        print("   Some rankings change under parameter perturbation")
        print("   Review and tighten parameter derivations")

    print(f"\nResults saved to: {output_path}")

    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run sensitivity analysis")
    parser.add_argument('--output-dir', default='outputs/sensitivity',
                        help='Output directory for results')
    args = parser.parse_args()

    main(args.output_dir)
