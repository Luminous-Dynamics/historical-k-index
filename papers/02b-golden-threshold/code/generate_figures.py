#!/usr/bin/env python3
"""
Generate publication-quality figures for Paper 2B: The Golden Threshold.

Creates:
1. Figure 1: Convergence of 9 derivations on θ ≈ 0.382
2. Figure 2: Rigor classification matrix
3. Figure 3: Monte Carlo parameter robustness

Usage:
    python generate_figures.py --output-dir ../figures
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import argparse
from pathlib import Path

# Set publication style
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

# Constants
PHI = (1 + np.sqrt(5)) / 2
THETA_GOLDEN = 1 / PHI**2  # 0.3820

# Derivation data
DERIVATIONS = {
    'Game Theory': {'theta': 0.375, 'rigor': 'B+', 'field': 'Social Science'},
    'Diamond Percolation': {'theta': 0.388, 'rigor': 'A+', 'field': 'Physics'},
    'Bifurcation': {'theta': 0.382, 'rigor': 'A', 'field': 'Mathematics'},
    'Channel Capacity': {'theta': 0.380, 'rigor': 'B', 'field': 'Information'},
    'Landau Theory': {'theta': 0.382, 'rigor': 'B+', 'field': 'Thermodynamics'},
    'ESS Stability': {'theta': 0.378, 'rigor': 'B+', 'field': 'Biology'},
    'Spectral Gap': {'theta': 0.385, 'rigor': 'B', 'field': 'Networks'},
    'Maximum Entropy': {'theta': 0.382, 'rigor': 'A', 'field': 'Information'},
    'Renormalization Group': {'theta': 0.385, 'rigor': 'B+', 'field': 'Physics'},
}

RIGOR_COLORS = {
    'A+': '#1a9850',  # Dark green
    'A': '#66bd63',   # Light green
    'B+': '#fdae61',  # Orange
    'B': '#f46d43',   # Red-orange
}

FIELD_MARKERS = {
    'Social Science': 'o',
    'Physics': 's',
    'Mathematics': '^',
    'Information': 'D',
    'Thermodynamics': 'v',
    'Biology': 'p',
    'Networks': 'h',
}


def figure1_convergence(output_dir: Path):
    """
    Figure 1: Convergence of 9 derivations on θ ≈ 0.382

    Shows all derivations as points with error bars, golden ratio line,
    and statistical summary.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    names = list(DERIVATIONS.keys())
    thetas = [DERIVATIONS[n]['theta'] for n in names]
    rigors = [DERIVATIONS[n]['rigor'] for n in names]
    fields = [DERIVATIONS[n]['field'] for n in names]

    # Sort by theta value for visual clarity
    sorted_idx = np.argsort(thetas)
    names = [names[i] for i in sorted_idx]
    thetas = [thetas[i] for i in sorted_idx]
    rigors = [rigors[i] for i in sorted_idx]
    fields = [fields[i] for i in sorted_idx]

    y_positions = np.arange(len(names))

    # Plot derivation points with colors by rigor
    for i, (name, theta, rigor, field) in enumerate(zip(names, thetas, rigors, fields)):
        color = RIGOR_COLORS[rigor]
        marker = FIELD_MARKERS[field]
        ax.scatter(theta, i, c=color, marker=marker, s=120, zorder=5,
                   edgecolors='black', linewidths=0.5)

    # Golden ratio line
    ax.axvline(THETA_GOLDEN, color='gold', linestyle='-', linewidth=2.5,
               label=f'1/φ² = {THETA_GOLDEN:.4f}', zorder=3)

    # Mean line
    mean_theta = np.mean(thetas)
    std_theta = np.std(thetas)
    ax.axvline(mean_theta, color='blue', linestyle='--', linewidth=1.5,
               label=f'Mean = {mean_theta:.4f}', zorder=3)

    # Shaded region for ±1σ
    ax.axvspan(mean_theta - std_theta, mean_theta + std_theta,
               alpha=0.2, color='blue', label=f'±1σ = {std_theta:.4f}')

    # Empirical value
    ax.axvline(0.375, color='red', linestyle=':', linewidth=1.5,
               label='Empirical = 0.375', zorder=3)

    # Labels
    ax.set_yticks(y_positions)
    ax.set_yticklabels(names)
    ax.set_xlabel('Trust Threshold θ')
    ax.set_title('Convergence of Nine Independent Derivations\non the Coordination Collapse Threshold')

    # Set x limits
    ax.set_xlim(0.365, 0.395)

    # Add rigor legend
    rigor_patches = [mpatches.Patch(color=RIGOR_COLORS[r], label=f'{r}')
                     for r in ['A+', 'A', 'B+', 'B']]
    legend1 = ax.legend(handles=rigor_patches, title='Rigor',
                        loc='upper left', framealpha=0.9)
    ax.add_artist(legend1)

    # Add main legend
    ax.legend(loc='lower right', framealpha=0.9)

    # Add statistics annotation
    stats_text = (
        f'N = 9 derivations\n'
        f'Mean = {mean_theta:.4f}\n'
        f'Std = {std_theta:.4f}\n'
        f'95% CI = [{mean_theta-1.96*std_theta/3:.4f}, {mean_theta+1.96*std_theta/3:.4f}]\n'
        f'|Mean - 1/φ²| = {abs(mean_theta - THETA_GOLDEN):.5f}'
    )
    ax.text(0.392, 7.5, stats_text, fontsize=8, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()

    # Save
    for fmt in ['png', 'pdf']:
        fig.savefig(output_dir / f'figure_1_convergence.{fmt}')
    plt.close()
    print(f"Saved Figure 1 to {output_dir}/figure_1_convergence.[png|pdf]")


def figure2_rigor_matrix(output_dir: Path):
    """
    Figure 2: Rigor classification matrix

    Shows rigor grades by derivation with color coding.
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    # Rigor grade to numeric
    rigor_to_num = {'A+': 4, 'A': 3, 'B+': 2, 'B': 1}

    names = list(DERIVATIONS.keys())
    rigors = [DERIVATIONS[n]['rigor'] for n in names]
    rigor_nums = [rigor_to_num[r] for r in rigors]

    # Sort by rigor
    sorted_idx = np.argsort(rigor_nums)[::-1]
    names = [names[i] for i in sorted_idx]
    rigors = [rigors[i] for i in sorted_idx]
    rigor_nums = [rigor_nums[i] for i in sorted_idx]

    y_positions = np.arange(len(names))
    colors = [RIGOR_COLORS[r] for r in rigors]

    bars = ax.barh(y_positions, rigor_nums, color=colors, edgecolor='black', linewidth=0.5)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(names)
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(['B', 'B+', 'A', 'A+'])
    ax.set_xlabel('Rigor Grade')
    ax.set_title('Rigor Classification of Threshold Derivations')

    # Add rigor labels on bars
    for bar, rigor in zip(bars, rigors):
        ax.text(bar.get_width() - 0.3, bar.get_y() + bar.get_height()/2,
                rigor, va='center', ha='center', fontsize=10, fontweight='bold')

    ax.set_xlim(0, 4.5)

    # Add legend explaining grades
    grade_text = (
        'A+ : Exact (Monte Carlo verified)\n'
        'A  : Analytic closed-form\n'
        'B+ : Robust with validation\n'
        'B  : Established with approximations'
    )
    ax.text(4.4, 8, grade_text, fontsize=8, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    plt.tight_layout()

    for fmt in ['png', 'pdf']:
        fig.savefig(output_dir / f'figure_2_rigor_matrix.{fmt}')
    plt.close()
    print(f"Saved Figure 2 to {output_dir}/figure_2_rigor_matrix.[png|pdf]")


def figure3_parameter_robustness(output_dir: Path):
    """
    Figure 3: Monte Carlo parameter robustness for game theory derivation.

    Shows distribution of θ across parameter space.
    """
    np.random.seed(42)
    n_samples = 100000

    # Parameter ranges
    alpha = np.random.uniform(0.4, 0.8, n_samples)
    beta = np.random.uniform(0.2, 0.6, n_samples)
    gamma = np.random.uniform(0.6, 0.9, n_samples)

    # Compute threshold: θ = γ × α / (1 + α - β)
    theta = gamma * alpha / (1 + alpha - beta)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Left: Histogram
    ax1 = axes[0]
    n, bins, patches = ax1.hist(theta, bins=100, density=True, alpha=0.7,
                                 color='steelblue', edgecolor='black', linewidth=0.3)

    # Highlight target range
    target_mask = (theta > 0.35) & (theta < 0.42)
    target_frac = np.mean(target_mask)

    ax1.axvline(0.35, color='green', linestyle='--', linewidth=1.5, label='Target range')
    ax1.axvline(0.42, color='green', linestyle='--', linewidth=1.5)
    ax1.axvspan(0.35, 0.42, alpha=0.2, color='green')

    ax1.axvline(THETA_GOLDEN, color='gold', linestyle='-', linewidth=2,
                label=f'1/φ² = {THETA_GOLDEN:.3f}')
    ax1.axvline(np.mean(theta), color='red', linestyle=':', linewidth=1.5,
                label=f'Mean = {np.mean(theta):.3f}')

    ax1.set_xlabel('Trust Threshold θ')
    ax1.set_ylabel('Probability Density')
    ax1.set_title(f'Game Theory θ Distribution\n(n = {n_samples:,} samples)')
    ax1.legend(loc='upper right')

    stats_text = (
        f'Mean = {np.mean(theta):.3f}\n'
        f'Std = {np.std(theta):.3f}\n'
        f'Target [0.35, 0.42]: {target_frac:.1%}'
    )
    ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, fontsize=9,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Right: 2D scatter showing α vs β colored by θ
    ax2 = axes[1]
    sample_idx = np.random.choice(n_samples, 5000, replace=False)
    scatter = ax2.scatter(alpha[sample_idx], beta[sample_idx],
                          c=theta[sample_idx], cmap='RdYlGn_r',
                          s=5, alpha=0.6, vmin=0.2, vmax=0.6)

    cbar = plt.colorbar(scatter, ax=ax2)
    cbar.set_label('θ value')

    ax2.set_xlabel('α (betrayal cost)')
    ax2.set_ylabel('β (exploitation gain)')
    ax2.set_title('Parameter Space Exploration')

    # Add contour for θ = 0.382
    alpha_grid = np.linspace(0.4, 0.8, 100)
    beta_grid = np.linspace(0.2, 0.6, 100)
    A, B = np.meshgrid(alpha_grid, beta_grid)
    gamma_mid = 0.75  # Middle of range
    T = gamma_mid * A / (1 + A - B)
    ax2.contour(A, B, T, levels=[THETA_GOLDEN], colors='gold', linewidths=2)

    plt.tight_layout()

    for fmt in ['png', 'pdf']:
        fig.savefig(output_dir / f'figure_3_robustness.{fmt}')
    plt.close()
    print(f"Saved Figure 3 to {output_dir}/figure_3_robustness.[png|pdf]")


def figure4_convergence_probability(output_dir: Path):
    """
    Figure 4: Statistical significance of convergence.

    Shows the probability calculation for random convergence.
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    # Derivation range
    thetas = [DERIVATIONS[n]['theta'] for n in DERIVATIONS]
    range_width = max(thetas) - min(thetas)  # 0.013

    # If N derivations fall within range R by chance from uniform [0,1]
    # P(all in range) = R^N

    N_derivations = np.arange(2, 15)
    p_random = range_width ** N_derivations

    ax.semilogy(N_derivations, p_random, 'b-o', linewidth=2, markersize=8)

    # Mark our case (N=9)
    ax.axvline(9, color='red', linestyle='--', linewidth=1.5)
    ax.axhline(range_width**9, color='red', linestyle='--', linewidth=1.5)
    ax.scatter([9], [range_width**9], color='red', s=150, zorder=5,
               marker='*', label=f'N=9: p = {range_width**9:.1e}')

    # Significance thresholds
    ax.axhline(0.05, color='orange', linestyle=':', label='p = 0.05')
    ax.axhline(0.01, color='orange', linestyle='-.', label='p = 0.01')
    ax.axhline(1e-10, color='green', linestyle=':', label='p = 10⁻¹⁰')

    ax.set_xlabel('Number of Independent Derivations')
    ax.set_ylabel('Probability of Random Convergence')
    ax.set_title(f'Statistical Significance of Convergence\n(Range width = {range_width:.3f})')
    ax.legend(loc='upper right')
    ax.set_xlim(1.5, 14.5)
    ax.set_ylim(1e-25, 1)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    for fmt in ['png', 'pdf']:
        fig.savefig(output_dir / f'figure_4_significance.{fmt}')
    plt.close()
    print(f"Saved Figure 4 to {output_dir}/figure_4_significance.[png|pdf]")


def main():
    parser = argparse.ArgumentParser(description='Generate Paper 2B figures')
    parser.add_argument('--output-dir', type=str, default='../figures',
                        help='Output directory for figures')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating publication-quality figures for Paper 2B...")
    print("=" * 60)

    figure1_convergence(output_dir)
    figure2_rigor_matrix(output_dir)
    figure3_parameter_robustness(output_dir)
    figure4_convergence_probability(output_dir)

    print("=" * 60)
    print(f"All figures saved to {output_dir}/")
    print("Formats: PNG (300 dpi) and PDF (vector)")


if __name__ == '__main__':
    main()
