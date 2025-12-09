#!/usr/bin/env python3
"""
Sensitivity Visualization for Coordination Collapse Laws

Generates:
- Figure 5: Tornado diagram showing parameter sensitivity
- Figure 6: Ranking stability heatmap

Usage:
    python sensitivity_visualization.py --output-dir outputs/figures/
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================================================
# MODEL PARAMETERS
# =============================================================================

THETA = 0.375

# Baseline case (Soviet-like)
BASELINE = {
    'H3': 0.30,
    'R': 1.6,
    'lambda': 2.2,
    'C': 0.9
}

def cascade_velocity(H3: float, R: float, lam: float, theta: float = THETA) -> float:
    """Cascade velocity (relative, not absolute time)."""
    if H3 >= theta:
        return 0.0
    return lam * (theta - H3)**2 / np.sqrt(R)

def intervention_roi(H3: float, theta: float = THETA) -> float:
    """Intervention ROI."""
    if H3 > theta:
        return 1.0 + 5.0 * (H3 - theta)
    else:
        return np.exp(-10.0 * (theta - H3))

def fragility_index(C: float, R: float, lam: float) -> float:
    """Fragility = C × λ / R"""
    return C * lam / R


# =============================================================================
# SENSITIVITY ANALYSIS
# =============================================================================

def one_at_a_time_sensitivity(perturbation: float = 0.2) -> dict:
    """
    Calculate sensitivity of outputs to each input parameter.

    Returns the % change in output for +/- perturbation of each input.
    """
    results = {}

    # Baseline outputs
    base_v = cascade_velocity(BASELINE['H3'], BASELINE['R'], BASELINE['lambda'])
    base_roi = intervention_roi(BASELINE['H3'])
    base_frag = fragility_index(BASELINE['C'], BASELINE['R'], BASELINE['lambda'])

    # Parameters to test
    params = {
        'H₃ (Trust)': ('H3', BASELINE['H3']),
        'R (Redundancy)': ('R', BASELINE['R']),
        'λ (Modernization)': ('lambda', BASELINE['lambda']),
        'C (Centralization)': ('C', BASELINE['C'])
    }

    for name, (key, base_val) in params.items():
        # Perturb up
        params_up = BASELINE.copy()
        params_up[key] = base_val * (1 + perturbation)

        # Perturb down
        params_down = BASELINE.copy()
        params_down[key] = base_val * (1 - perturbation)

        # Calculate cascade velocity sensitivity
        v_up = cascade_velocity(params_up['H3'], params_up['R'], params_up['lambda'])
        v_down = cascade_velocity(params_down['H3'], params_down['R'], params_down['lambda'])

        # Calculate ROI sensitivity
        roi_up = intervention_roi(params_up['H3'])
        roi_down = intervention_roi(params_down['H3'])

        # Calculate fragility sensitivity
        frag_up = fragility_index(params_up['C'], params_up['R'], params_up['lambda'])
        frag_down = fragility_index(params_down['C'], params_down['R'], params_down['lambda'])

        # Store relative changes
        results[name] = {
            'velocity': {
                'up': (v_up - base_v) / base_v * 100 if base_v != 0 else 0,
                'down': (v_down - base_v) / base_v * 100 if base_v != 0 else 0
            },
            'roi': {
                'up': (roi_up - base_roi) / base_roi * 100 if base_roi != 0 else 0,
                'down': (roi_down - base_roi) / base_roi * 100 if base_roi != 0 else 0
            },
            'fragility': {
                'up': (frag_up - base_frag) / base_frag * 100 if base_frag != 0 else 0,
                'down': (frag_down - base_frag) / base_frag * 100 if base_frag != 0 else 0
            }
        }

    return results


def plot_tornado(results: dict, output: str, title: str, key: str):
    """Create tornado diagram."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Extract data
    params = list(results.keys())
    ups = [results[p][key]['up'] for p in params]
    downs = [results[p][key]['down'] for p in params]

    # Sort by total range
    ranges = [abs(u) + abs(d) for u, d in zip(ups, downs)]
    sorted_idx = np.argsort(ranges)[::-1]

    params = [params[i] for i in sorted_idx]
    ups = [ups[i] for i in sorted_idx]
    downs = [downs[i] for i in sorted_idx]

    y_pos = np.arange(len(params))

    # Plot bars
    ax.barh(y_pos, ups, align='center', color='#e74c3c', label='+20% change', alpha=0.8)
    ax.barh(y_pos, downs, align='center', color='#3498db', label='-20% change', alpha=0.8)

    # Labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(params, fontsize=12)
    ax.set_xlabel(f'% Change in {title}', fontsize=12)
    ax.set_title(f'Sensitivity Analysis: {title}\n(±20% Parameter Perturbation)', fontsize=14)

    # Add zero line
    ax.axvline(x=0, color='black', linewidth=0.5)

    # Add values on bars
    for i, (u, d) in enumerate(zip(ups, downs)):
        if abs(u) > 5:
            ax.text(u + 2 if u > 0 else u - 2, i, f'{u:.0f}%',
                   va='center', ha='left' if u > 0 else 'right', fontsize=10)
        if abs(d) > 5:
            ax.text(d + 2 if d > 0 else d - 2, i, f'{d:.0f}%',
                   va='center', ha='left' if d > 0 else 'right', fontsize=10)

    ax.legend(loc='lower right')
    ax.set_xlim(-100, 100)

    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()


def plot_ranking_heatmap(output: str):
    """
    Create heatmap showing Rome vs Soviet velocity ratio across parameter space.

    This visualizes the robustness of the ranking prediction.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Rome and Soviet baseline parameters
    rome = {'R': 3.3, 'lambda': 1.0}
    soviet = {'R': 1.6, 'lambda': 2.2}

    # Create perturbation grid
    perturbations = np.linspace(-0.3, 0.3, 21)
    n = len(perturbations)

    # Calculate velocity ratio for each combination
    ratio_grid = np.zeros((n, n))

    for i, p_R in enumerate(perturbations):
        for j, p_lambda in enumerate(perturbations):
            rome_R = rome['R'] * (1 + p_R)
            rome_lam = rome['lambda'] * (1 + p_lambda)
            soviet_R = soviet['R'] * (1 + p_R)
            soviet_lam = soviet['lambda'] * (1 + p_lambda)

            v_rome = cascade_velocity(0.30, rome_R, rome_lam)
            v_soviet = cascade_velocity(0.30, soviet_R, soviet_lam)

            if v_soviet > 0:
                ratio_grid[i, j] = v_rome / v_soviet
            else:
                ratio_grid[i, j] = 0

    # Plot heatmap
    im = ax.imshow(ratio_grid, cmap='RdYlGn_r', aspect='auto',
                   extent=[-30, 30, -30, 30], origin='lower',
                   vmin=0, vmax=1)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Velocity Ratio (Rome / Soviet)', fontsize=12)

    # Add contour at ratio = 1 (if it exists in range)
    if ratio_grid.min() < 1 < ratio_grid.max():
        ax.contour(perturbations * 100, perturbations * 100, ratio_grid.T,
                  levels=[1.0], colors='white', linewidths=2)

    # Labels
    ax.set_xlabel('R (Redundancy) Perturbation (%)', fontsize=12)
    ax.set_ylabel('λ (Modernization) Perturbation (%)', fontsize=12)
    ax.set_title('Ranking Stability: Rome vs Soviet\n(Rome slower = ratio < 1 = green)', fontsize=14)

    # Add annotation
    ax.text(0.02, 0.98, 'Green region: Rome slower (prediction holds)\nRed region: Soviet slower (prediction fails)',
           transform=ax.transAxes, fontsize=10, va='top',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Check what fraction is green (ratio < 1)
    green_fraction = (ratio_grid < 1).sum() / ratio_grid.size * 100
    ax.text(0.98, 0.02, f'Rome slower in {green_fraction:.0f}% of scenarios',
           transform=ax.transAxes, fontsize=11, ha='right',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()


def plot_cascade_phase_diagram(output: str):
    """
    Phase diagram showing cascade velocity as function of H3 and R.
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create grid
    H3_vals = np.linspace(0.15, 0.45, 100)
    R_vals = np.linspace(1.0, 5.0, 100)
    H3_grid, R_grid = np.meshgrid(H3_vals, R_vals)

    # Calculate velocity (using λ = 2.0 as mid-range)
    lam = 2.0
    V_grid = np.zeros_like(H3_grid)
    for i in range(len(R_vals)):
        for j in range(len(H3_vals)):
            V_grid[i, j] = cascade_velocity(H3_vals[j], R_vals[i], lam)

    # Plot
    im = ax.contourf(H3_grid, R_grid, V_grid, levels=20, cmap='YlOrRd')
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Cascade Velocity (relative)', fontsize=12)

    # Add threshold line
    ax.axvline(x=THETA, color='black', linestyle='--', linewidth=2, label=f'Threshold θ = {THETA}')

    # Add isovelocity contours
    cs = ax.contour(H3_grid, R_grid, V_grid, levels=[0.01, 0.05, 0.10, 0.20],
                   colors='white', linewidths=1)
    ax.clabel(cs, inline=True, fontsize=9, fmt='%.2f')

    # Mark Rome and Soviet positions
    ax.plot(0.30, 3.3, 'o', markersize=15, color='blue', label='Rome (R=3.3)')
    ax.plot(0.30, 1.6, 's', markersize=15, color='red', label='Soviet (R=1.6)')

    # Labels
    ax.set_xlabel('H₃ (Interpersonal Trust)', fontsize=12)
    ax.set_ylabel('R (Network Redundancy)', fontsize=12)
    ax.set_title('Cascade Velocity Phase Diagram\n(λ = 2.0 fixed)', fontsize=14)

    # Add region labels
    ax.text(0.41, 4.5, 'STABLE\n(H₃ > θ)', fontsize=12, ha='center',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    ax.text(0.25, 4.5, 'CASCADE\n(H₃ < θ)', fontsize=12, ha='center',
           bbox=dict(boxstyle='round', facecolor='lightsalmon', alpha=0.8))

    ax.legend(loc='lower left')

    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main(output_dir: str = 'outputs/figures'):
    """Generate all sensitivity visualizations."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("GENERATING SENSITIVITY VISUALIZATIONS")
    print("=" * 60)

    # Calculate sensitivities
    print("\n1. Calculating one-at-a-time sensitivities...")
    sensitivities = one_at_a_time_sensitivity(perturbation=0.2)

    for param, data in sensitivities.items():
        print(f"\n   {param}:")
        print(f"     Velocity: {data['velocity']['down']:.0f}% to {data['velocity']['up']:.0f}%")
        print(f"     ROI: {data['roi']['down']:.0f}% to {data['roi']['up']:.0f}%")
        print(f"     Fragility: {data['fragility']['down']:.0f}% to {data['fragility']['up']:.0f}%")

    # Generate figures
    print("\n2. Generating Figure 5: Cascade Velocity Tornado...")
    plot_tornado(sensitivities,
                output_path / 'figure5_velocity_tornado.png',
                'Cascade Velocity',
                'velocity')

    print("3. Generating Figure 6: Ranking Stability Heatmap...")
    plot_ranking_heatmap(output_path / 'figure6_ranking_heatmap.png')

    print("4. Generating Figure 7: Cascade Phase Diagram...")
    plot_cascade_phase_diagram(output_path / 'figure7_phase_diagram.png')

    print("\n" + "=" * 60)
    print("ALL VISUALIZATIONS GENERATED")
    print("=" * 60)
    print(f"\nOutput directory: {output_path}")
    print("Files created:")
    print("  - figure5_velocity_tornado.png")
    print("  - figure6_ranking_heatmap.png")
    print("  - figure7_phase_diagram.png")

    return sensitivities


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate sensitivity visualizations")
    parser.add_argument('--output-dir', default='outputs/figures',
                        help='Output directory for figures')
    args = parser.parse_args()

    main(args.output_dir)
