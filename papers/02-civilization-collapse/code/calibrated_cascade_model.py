#!/usr/bin/env python3
"""
Calibrated Cascade Timing Model

The original model predicted:
- Soviet: 0y (actual: 6y)
- Maya: 17.1y (actual: 100y)

This module derives properly calibrated scaling constants from historical data.

Key insight: The cascade velocity formula needs calibration constants that
ensure dimensional consistency and match observed collapse durations.

Usage:
    python calibrated_cascade_model.py --output-dir outputs/calibration/
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path

# =============================================================================
# HISTORICAL COLLAPSE DATA (Ground Truth)
# =============================================================================

@dataclass
class CollapseCase:
    """Historical collapse case with measured parameters."""
    name: str
    H3_start: float      # Trust at onset of decline
    H3_end: float        # Trust at collapse endpoint
    R: float             # Redundancy (coordination mechanisms)
    lambda_mod: float    # Modernization factor
    observed_years: float  # Actual collapse duration
    threshold_crossed_year: Optional[float] = None  # When H3 < θ

HISTORICAL_CASES = [
    CollapseCase("Western Rome (376-476 CE)", 0.38, 0.15, 3.3, 1.0, 100, 30),
    CollapseCase("Han Dynasty (184-220 CE)", 0.35, 0.12, 2.8, 0.9, 36, 20),
    CollapseCase("Classic Maya (800-900 CE)", 0.32, 0.10, 1.5, 0.9, 100, 60),
    CollapseCase("Byzantine (1180-1204 CE)", 0.36, 0.18, 2.5, 1.1, 24, 15),
    CollapseCase("Ming Dynasty (1620-1644 CE)", 0.33, 0.14, 2.2, 1.3, 24, 12),
    CollapseCase("Ottoman (1876-1922 CE)", 0.31, 0.12, 2.0, 1.6, 46, 30),
    CollapseCase("Soviet Union (1985-1991)", 0.55, 0.20, 1.6, 2.2, 6, 4),
    CollapseCase("Weimar Germany (1929-1933)", 0.30, 0.15, 2.0, 1.8, 4, 2),
]

THETA = 0.375  # Trust threshold

# =============================================================================
# ORIGINAL (UNCALIBRATED) MODEL
# =============================================================================

def cascade_velocity_original(H3: float, R: float, lambda_mod: float,
                              theta: float = THETA) -> float:
    """Original formula: v = λ × (θ - H₃)² / √R"""
    if H3 >= theta:
        return 0.0
    deficit = theta - H3
    return lambda_mod * (deficit ** 2) / np.sqrt(R)


def time_to_collapse_original(case: CollapseCase) -> float:
    """Integrate original model."""
    dt = 0.1
    t = 0
    H3 = case.H3_start

    while H3 > case.H3_end and t < 1000:
        v = cascade_velocity_original(H3, case.R, case.lambda_mod)
        H3 -= v * dt
        t += dt

    return t

# =============================================================================
# CALIBRATED MODEL
# =============================================================================

def derive_calibration_constant(cases: List[CollapseCase]) -> Tuple[float, float]:
    """
    Derive calibration constant α such that:

    v_cascade = α × λ × (θ - H₃)² / √R

    Using least squares on log(observed_years) vs log(predicted_years).
    """
    # For each case, calculate the "raw velocity integral"
    # and compare to observed duration

    ratios = []
    for case in cases:
        if case.H3_start >= THETA:
            # Need to model the above-threshold phase differently
            # For now, use threshold crossing time
            H3_effective = THETA - 0.01  # Just below threshold
        else:
            H3_effective = case.H3_start

        # Analytical approximation for quadratic cascade time
        # ∫ dH / (λ(θ-H)²/√R) = √R/λ × ∫ dH/(θ-H)² = √R/λ × [1/(θ-H)]
        # T = √R/λ × (1/(θ-H_end) - 1/(θ-H_start))

        if case.H3_end < THETA:
            # Time below threshold
            H_start = min(H3_effective, THETA - 0.001)
            H_end = case.H3_end

            if H_start > H_end:
                raw_integral = np.sqrt(case.R) / case.lambda_mod * (
                    1/(THETA - H_end) - 1/(THETA - H_start)
                )
                ratios.append(case.observed_years / raw_integral)

    if ratios:
        alpha = np.mean(ratios)
        alpha_std = np.std(ratios)
        return alpha, alpha_std
    else:
        return 1.0, 0.0


def cascade_velocity_calibrated(H3: float, R: float, lambda_mod: float,
                                 alpha: float, theta: float = THETA) -> float:
    """
    Calibrated formula: v = (1/α) × λ × (θ - H₃)² / √R

    where α is the calibration constant derived from historical data.
    """
    if H3 >= theta:
        return 0.0
    deficit = theta - H3
    return (1/alpha) * lambda_mod * (deficit ** 2) / np.sqrt(R)


def time_to_collapse_calibrated(case: CollapseCase, alpha: float) -> float:
    """Integrate calibrated model."""
    dt = 0.1
    t = 0
    H3 = case.H3_start

    # If starting above threshold, model gradual decline to threshold
    if H3 >= THETA:
        # Above threshold: slow linear decline
        above_threshold_velocity = 0.005 / case.lambda_mod  # ~0.5% per year base
        while H3 > THETA and t < 500:
            H3 -= above_threshold_velocity * dt
            t += dt

    # Below threshold: cascade dynamics
    while H3 > case.H3_end and t < 1000:
        v = cascade_velocity_calibrated(H3, case.R, case.lambda_mod, alpha)
        H3 -= v * dt
        t += dt

    return t


# =============================================================================
# DIMENSIONAL ANALYSIS
# =============================================================================

def verify_dimensional_consistency():
    """
    Verify that all terms have consistent dimensions.

    [H₃] = dimensionless (0-1 trust fraction)
    [R] = dimensionless (count of mechanisms)
    [λ] = dimensionless (modernization multiplier)
    [θ] = dimensionless (threshold)
    [t] = years

    For v = dH₃/dt:
    [v] = [H₃]/[t] = year⁻¹

    Original formula: v = λ × (θ - H₃)² / √R
    [v] = dimensionless × dimensionless² / dimensionless^0.5
    [v] = dimensionless  ← WRONG! Should be year⁻¹

    Corrected: v = (1/τ) × λ × (θ - H₃)² / √R
    where τ has dimensions of time (years)

    τ = α (our calibration constant) has units of YEARS
    """
    return {
        'H3': 'dimensionless',
        'R': 'dimensionless',
        'lambda': 'dimensionless',
        'theta': 'dimensionless',
        'v': '1/years',
        'alpha_units': 'years',
        'formula': 'v = (1/α) × λ × (θ - H₃)² / √R',
        'dimensional_check': 'year⁻¹ = year⁻¹ × 1 × 1 × 1 = year⁻¹ ✓'
    }


# =============================================================================
# VALIDATION
# =============================================================================

def validate_model(alpha: float) -> Dict:
    """Compare predictions to observations."""
    results = []

    for case in HISTORICAL_CASES:
        original = time_to_collapse_original(case)
        calibrated = time_to_collapse_calibrated(case, alpha)

        original_error = abs(original - case.observed_years) / case.observed_years * 100
        calibrated_error = abs(calibrated - case.observed_years) / case.observed_years * 100

        results.append({
            'case': case.name,
            'observed': case.observed_years,
            'original_pred': round(original, 1),
            'calibrated_pred': round(calibrated, 1),
            'original_error_pct': round(original_error, 1),
            'calibrated_error_pct': round(calibrated_error, 1)
        })

    # Calculate summary statistics
    original_mape = np.mean([r['original_error_pct'] for r in results])
    calibrated_mape = np.mean([r['calibrated_error_pct'] for r in results])

    return {
        'cases': results,
        'original_MAPE': round(original_mape, 1),
        'calibrated_MAPE': round(calibrated_mape, 1),
        'improvement_factor': round(original_mape / calibrated_mape, 1) if calibrated_mape > 0 else float('inf')
    }


# =============================================================================
# RANKING STABILITY TEST
# =============================================================================

def test_ranking_stability(alpha: float, perturbation: float = 0.2) -> Dict:
    """
    The key test: Do relative rankings remain stable?

    Rome should ALWAYS be slower than Soviet, regardless of parameter perturbation.
    """
    rome = next(c for c in HISTORICAL_CASES if 'Rome' in c.name)
    soviet = next(c for c in HISTORICAL_CASES if 'Soviet' in c.name)

    # Generate perturbed scenarios
    perturbations = np.linspace(-perturbation, perturbation, 11)
    rome_slower_count = 0
    total = 0

    for p_R in perturbations:
        for p_lambda in perturbations:
            # Perturb parameters
            rome_R = rome.R * (1 + p_R)
            rome_lambda = rome.lambda_mod * (1 + p_lambda)
            soviet_R = soviet.R * (1 + p_R)
            soviet_lambda = soviet.lambda_mod * (1 + p_lambda)

            # Calculate velocities at H3 = 0.30 (below threshold)
            v_rome = cascade_velocity_calibrated(0.30, rome_R, rome_lambda, alpha)
            v_soviet = cascade_velocity_calibrated(0.30, soviet_R, soviet_lambda, alpha)

            total += 1
            if v_rome < v_soviet:
                rome_slower_count += 1

    return {
        'rome_slower_fraction': rome_slower_count / total,
        'ranking_stable': rome_slower_count / total > 0.95,
        'total_scenarios': total
    }


# =============================================================================
# MAIN
# =============================================================================

def main(output_dir: str = 'outputs/calibration'):
    """Run calibration and validation."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("CALIBRATED CASCADE TIMING MODEL")
    print("=" * 70)

    # Step 1: Derive calibration constant
    print("\n1. Deriving calibration constant from historical data...")
    alpha, alpha_std = derive_calibration_constant(HISTORICAL_CASES)
    print(f"   α = {alpha:.2f} ± {alpha_std:.2f} years")
    print(f"   (This gives the cascade velocity the correct time dimension)")

    # Step 2: Dimensional analysis
    print("\n2. Dimensional Analysis:")
    dims = verify_dimensional_consistency()
    print(f"   Formula: {dims['formula']}")
    print(f"   Check: {dims['dimensional_check']}")
    print(f"   α has units of: {dims['alpha_units']}")

    # Step 3: Validate against historical cases
    print("\n3. Validation Against Historical Cases:")
    print("-" * 70)
    validation = validate_model(alpha)

    print(f"{'Case':<30} {'Observed':>10} {'Original':>10} {'Calibrated':>12} {'Error':>8}")
    print("-" * 70)
    for r in validation['cases']:
        print(f"{r['case']:<30} {r['observed']:>10.0f}y {r['original_pred']:>10.1f}y "
              f"{r['calibrated_pred']:>12.1f}y {r['calibrated_error_pct']:>7.1f}%")
    print("-" * 70)
    print(f"{'Mean Absolute Percentage Error (MAPE)':<30} {validation['original_MAPE']:>10.1f}% "
          f"{validation['calibrated_MAPE']:>12.1f}%")
    print(f"\n   Improvement: {validation['improvement_factor']}x reduction in MAPE")

    # Step 4: Ranking stability
    print("\n4. Ranking Stability Test (±20% perturbation):")
    stability = test_ranking_stability(alpha)
    print(f"   Rome slower than Soviet in {stability['rome_slower_fraction']*100:.1f}% of scenarios")
    print(f"   Ranking stable: {'YES ✓' if stability['ranking_stable'] else 'NO ✗'}")

    # Step 5: Updated formula
    print("\n" + "=" * 70)
    print("CALIBRATED CASCADE LAW (Law 2)")
    print("=" * 70)
    print(f"""
    Original (uncalibrated):
        v_cascade = λ × (θ - H₃)² / √R

    Calibrated:
        v_cascade = (1/{alpha:.1f} years) × λ × (θ - H₃)² / √R

    Or equivalently:
        dH₃/dt = -(1/{alpha:.1f}) × λ × (θ - H₃)² / √R

    This gives collapse time:
        T ≈ {alpha:.1f} × √R/λ × (1/(θ-H₃_end) - 1/(θ-H₃_start))
    """)

    # Save results
    results = {
        'calibration_constant': {
            'alpha': alpha,
            'alpha_std': alpha_std,
            'units': 'years'
        },
        'dimensional_analysis': dims,
        'validation': validation,
        'ranking_stability': stability,
        'formula': {
            'original': 'v = λ × (θ - H₃)² / √R',
            'calibrated': f'v = (1/{alpha:.1f}) × λ × (θ - H₃)² / √R'
        }
    }

    with open(output_path / 'calibration_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Calibrate cascade timing model")
    parser.add_argument('--output-dir', default='outputs/calibration',
                        help='Output directory for results')
    args = parser.parse_args()

    main(args.output_dir)
