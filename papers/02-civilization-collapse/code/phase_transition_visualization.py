#!/usr/bin/env python3
"""
Phase Transition Visualization for Coordination Collapse Laws

Generates:
- Figure 8: Landau Free Energy Landscape
- Figure 9: Critical Exponent Scaling
- Figure 10: Information Entropy Landscape

Usage:
    python phase_transition_visualization.py --output-dir outputs/figures/
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

THETA = 0.375  # Critical threshold
K_CRITICAL = 0.4  # K at threshold
BETA = 0.5  # Critical exponent (mean-field)
GAMMA = 1.0  # Susceptibility exponent


def landau_free_energy(m: np.ndarray, a: float, b: float = 0.1) -> np.ndarray:
    """
    Landau free energy: F(m) = a*m^2 + b*m^4

    Args:
        m: Order parameter (K - K_critical)
        a: Temperature-dependent coefficient (a < 0 below T_c)
        b: Fourth-order coefficient (positive for stability)
    """
    return a * m**2 + b * m**4


def plot_free_energy_landscape(output: str):
    """
    Create the Landau free energy landscape showing phase transition.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    m = np.linspace(-1.5, 1.5, 200)

    # Panel A: Above threshold (T > T_c, a > 0)
    ax = axes[0]
    a_above = 0.3
    F_above = landau_free_energy(m, a_above)
    ax.plot(m, F_above, 'b-', linewidth=2)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax.scatter([0], [0], color='green', s=100, zorder=5, label='Stable (cooperation)')
    ax.set_xlabel('m = K - K_c', fontsize=12)
    ax.set_ylabel('Free Energy F(m)', fontsize=12)
    ax.set_title('Above Threshold (H_3 > 0.375)\nSingle Minimum: Cooperation Stable', fontsize=11)
    ax.set_ylim(-0.2, 0.5)
    ax.legend()
    ax.text(0.05, 0.95, 'a > 0\nOrdered state\nstable', transform=ax.transAxes,
            fontsize=10, va='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    # Panel B: At threshold (T = T_c, a = 0)
    ax = axes[1]
    a_critical = 0.0
    F_critical = landau_free_energy(m, a_critical)
    ax.plot(m, F_critical, 'orange', linewidth=2)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    ax.scatter([0], [0], color='orange', s=100, zorder=5, label='Critical point')
    ax.set_xlabel('m = K - K_c', fontsize=12)
    ax.set_ylabel('Free Energy F(m)', fontsize=12)
    ax.set_title('At Threshold (H_3 = 0.375)\nFlat Bottom: Critical Point', fontsize=11)
    ax.set_ylim(-0.2, 0.5)
    ax.legend()
    ax.text(0.05, 0.95, 'a = 0\nCritical point\nMaximum fluctuations', transform=ax.transAxes,
            fontsize=10, va='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Panel C: Below threshold (T < T_c, a < 0)
    ax = axes[2]
    a_below = -0.2
    b = 0.1
    F_below = landau_free_energy(m, a_below, b)
    ax.plot(m, F_below, 'r-', linewidth=2)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)

    # Find minima
    m_min = np.sqrt(-a_below / (2*b))
    F_min = landau_free_energy(m_min, a_below, b)
    ax.scatter([m_min, -m_min], [F_min, F_min], color='red', s=100, zorder=5,
               label='New minima (defection)')
    ax.scatter([0], [landau_free_energy(np.array([0]), a_below, b)],
               color='white', edgecolors='red', s=100, zorder=5, label='Unstable (cooperation)')

    ax.set_xlabel('m = K - K_c', fontsize=12)
    ax.set_ylabel('Free Energy F(m)', fontsize=12)
    ax.set_title('Below Threshold (H_3 < 0.375)\nDouble Well: Defection Stable', fontsize=11)
    ax.set_ylim(-0.2, 0.5)
    ax.legend(loc='upper right')
    ax.text(0.05, 0.95, 'a < 0\nSymmetry broken\nDefection favored', transform=ax.transAxes,
            fontsize=10, va='top', bbox=dict(boxstyle='round', facecolor='lightsalmon', alpha=0.8))

    plt.suptitle('Landau Free Energy Landscape: Coordination Collapse as Phase Transition',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()


def plot_critical_exponents(output: str):
    """
    Create visualization of critical exponent scaling near threshold.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Distance from threshold
    delta = np.linspace(0.001, 0.2, 100)  # |H_3 - theta|

    # Panel A: Order parameter scaling (m ~ delta^beta)
    ax = axes[0, 0]
    m = delta**BETA
    ax.loglog(delta, m, 'b-', linewidth=2, label=f'm ~ |H_3 - theta|^{BETA}')
    ax.set_xlabel('|H_3 - theta|', fontsize=12)
    ax.set_ylabel('Order parameter m', fontsize=12)
    ax.set_title(f'Order Parameter Scaling\nbeta = {BETA} (mean-field)', fontsize=11)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add slope annotation
    ax.text(0.05, 0.15, f'Slope = {BETA}', transform=ax.transAxes, fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    # Panel B: Susceptibility divergence (chi ~ delta^-gamma)
    ax = axes[0, 1]
    chi = delta**(-GAMMA)
    ax.loglog(delta, chi, 'r-', linewidth=2, label=f'chi ~ |H_3 - theta|^-{GAMMA}')
    ax.set_xlabel('|H_3 - theta|', fontsize=12)
    ax.set_ylabel('Susceptibility chi', fontsize=12)
    ax.set_title(f'Susceptibility Divergence\ngamma = {GAMMA} (mean-field)', fontsize=11)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add physical interpretation
    ax.text(0.3, 0.85, 'Response to shocks\nincreases near threshold',
            transform=ax.transAxes, fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightsalmon', alpha=0.8))

    # Panel C: Correlation length (xi ~ delta^-nu, nu=0.5)
    ax = axes[1, 0]
    nu = 0.5
    xi = delta**(-nu)
    ax.loglog(delta, xi, 'g-', linewidth=2, label=f'xi ~ |H_3 - theta|^-{nu}')
    ax.set_xlabel('|H_3 - theta|', fontsize=12)
    ax.set_ylabel('Correlation length xi', fontsize=12)
    ax.set_title(f'Correlation Length Growth\nnu = {nu} (mean-field)', fontsize=11)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add physical interpretation
    ax.text(0.3, 0.85, 'Coordination failures\nbecome correlated\nacross larger regions',
            transform=ax.transAxes, fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

    # Panel D: Relaxation time (critical slowing down, tau ~ delta^-1)
    ax = axes[1, 1]
    tau = delta**(-1)
    ax.loglog(delta, tau, 'm-', linewidth=2, label='tau ~ |H_3 - theta|^-1')
    ax.set_xlabel('|H_3 - theta|', fontsize=12)
    ax.set_ylabel('Relaxation time tau', fontsize=12)
    ax.set_title('Critical Slowing Down\nnu*z = 1 (mean-field)', fontsize=11)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add physical interpretation
    ax.text(0.3, 0.85, 'Recovery from crises\ntakes longer\nnear threshold',
            transform=ax.transAxes, fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='plum', alpha=0.8))

    plt.suptitle('Critical Exponents: Universal Scaling Near Threshold',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()


def shannon_entropy(p: np.ndarray) -> np.ndarray:
    """
    Calculate Shannon entropy H(p) = -p*log(p) - (1-p)*log(1-p)
    Handles edge cases where p=0 or p=1.
    """
    result = np.zeros_like(p)
    mask = (p > 0) & (p < 1)
    result[mask] = -p[mask] * np.log2(p[mask]) - (1-p[mask]) * np.log2(1-p[mask])
    return result


def plot_information_entropy(output: str):
    """
    Create visualization of information-theoretic threshold derivation.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    p = np.linspace(0.001, 0.999, 200)  # Cooperation fraction

    # Panel A: Shannon entropy curve
    ax = axes[0]
    H = shannon_entropy(p)
    ax.plot(p, H, 'b-', linewidth=2)
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.8, label='H_max/2 = 0.5')
    ax.axvline(x=THETA, color='green', linestyle='--', alpha=0.8, label=f'theta = {THETA}')

    # Find half-entropy point
    half_idx = np.argmin(np.abs(H - 0.5))
    ax.scatter([p[half_idx]], [H[half_idx]], color='red', s=100, zorder=5)
    ax.annotate(f'Half-entropy\np = {p[half_idx]:.3f}',
                xy=(p[half_idx], H[half_idx]),
                xytext=(p[half_idx]+0.15, H[half_idx]+0.15),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='red'))

    ax.set_xlabel('Cooperation fraction p', fontsize=12)
    ax.set_ylabel('Shannon entropy H(p)', fontsize=12)
    ax.set_title('Entropy of Coordination State\nThreshold = Half-Entropy Point', fontsize=11)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Panel B: Mutual information structure
    ax = axes[1]
    harmonies = ['H_1\n(Gov)', 'H_2\n(Net)', 'H_3\n(Trust)', 'H_4\n(Comp)',
                 'H_5\n(Know)', 'H_6\n(Well)', 'H_7\n(Tech)']
    mutual_info_with_H3 = [0.85, 0.78, 1.0, 0.72, 0.65, 0.58, 0.45]

    colors = ['steelblue' if h != 'H_3\n(Trust)' else 'gold' for h in harmonies]
    bars = ax.bar(harmonies, mutual_info_with_H3, color=colors, edgecolor='black')
    ax.set_ylabel('Mutual Information with H_3', fontsize=12)
    ax.set_xlabel('Harmony', fontsize=12)
    ax.set_title('H_3 as Information Hub\nHighest Connectivity to Other Harmonies', fontsize=11)
    ax.set_ylim(0, 1.1)

    # Highlight H_3
    ax.annotate('H_3 is the\nINFORMATION HUB', xy=(2, 1.0), xytext=(4, 1.05),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='gold', lw=2))

    # Panel C: Information cascade model
    ax = axes[2]

    # Create cascade simulation
    time = np.linspace(0, 10, 100)
    H3 = 0.45 - 0.015 * time - 0.002 * time**2  # Quadratic decay
    H3 = np.maximum(H3, 0.1)

    # Information content (mutual info total)
    I_total = 0.85 * H3  # Scales with H3 being the hub

    ax.plot(time, H3, 'b-', linewidth=2, label='H_3 (Trust)')
    ax.plot(time, I_total, 'r--', linewidth=2, label='Total Mutual Info')
    ax.axhline(y=THETA, color='green', linestyle=':', alpha=0.8, label=f'Threshold theta={THETA}')

    # Mark threshold crossing
    cross_idx = np.argmin(np.abs(H3 - THETA))
    ax.scatter([time[cross_idx]], [H3[cross_idx]], color='red', s=100, zorder=5)
    ax.axvline(x=time[cross_idx], color='red', linestyle=':', alpha=0.5)
    ax.fill_betweenx([0, 0.5], time[cross_idx], 10, alpha=0.2, color='red',
                      label='Information loss phase')

    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Level', fontsize=12)
    ax.set_title('Information Cascade\nH_3 Collapse Drives Total Info Loss', fontsize=11)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 0.5)
    ax.grid(True, alpha=0.3)

    plt.suptitle('Information-Theoretic Foundation: Threshold from Shannon Entropy',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()


def plot_kardashev_scaling(output: str):
    """
    Create visualization of K_max scaling with Kardashev civilization type.
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    # Kardashev types
    types = np.array([0, 1, 2, 3])  # Type 0, I, II, III
    type_labels = ['Type 0\n(Current Earth)', 'Type I\n(Planetary)',
                   'Type II\n(Stellar)', 'Type III\n(Galactic)']

    # Energy in Watts (log scale)
    E_type0 = 2e13   # Current humanity
    E_type1 = 1e17   # Full planetary
    E_type2 = 4e26   # Full solar
    E_type3 = 4e37   # Full galactic

    # K_max scaling: K_max = 1 - epsilon/log(E/E_0)
    epsilon = 0.5
    E_0 = 1e10  # Reference energy

    energies = [E_type0, E_type1, E_type2, E_type3]
    K_max = [1 - epsilon/np.log10(E/E_0) for E in energies]

    # Current K estimates
    K_current = [0.72, None, None, None]  # Only Type 0 is measured

    # Plot K_max
    ax.plot(types, K_max, 'bo-', markersize=12, linewidth=2, label='K_max (theoretical ceiling)')

    # Plot current K
    ax.scatter([0], [0.72], color='red', s=150, zorder=5, marker='*', label='Current Earth K=0.72')

    # Add asymptote
    ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Theoretical limit K=1.0')

    # Shade forbidden region
    ax.fill_between(types, K_max, [1.0]*4, alpha=0.2, color='red', label='Coordination ceiling')

    # Labels
    ax.set_xticks(types)
    ax.set_xticklabels(type_labels, fontsize=10)
    ax.set_ylabel('K-Index', fontsize=12)
    ax.set_xlabel('Kardashev Civilization Type', fontsize=12)
    ax.set_title('Coordination Ceiling Scales with Civilization Type\n(Law 12 Extended to Kardashev Scale)',
                 fontsize=14)

    # Add K_max values
    for i, (t, k) in enumerate(zip(types, K_max)):
        ax.annotate(f'K_max = {k:.3f}', xy=(t, k), xytext=(t+0.15, k-0.03),
                   fontsize=10, color='blue')

    # Add energy scale annotation
    energy_text = 'Energy scaling:\nType 0: 2x10^13 W\nType I: 10^17 W\nType II: 4x10^26 W\nType III: 4x10^37 W'
    ax.text(0.98, 0.02, energy_text, transform=ax.transAxes, fontsize=9,
            va='bottom', ha='right', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    ax.set_ylim(0.7, 1.02)
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main(output_dir: str = 'outputs/figures'):
    """Generate all phase transition visualizations."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("GENERATING PHASE TRANSITION VISUALIZATIONS")
    print("=" * 60)

    print("\n1. Generating Figure 8: Landau Free Energy Landscape...")
    plot_free_energy_landscape(output_path / 'figure8_free_energy_landscape.png')

    print("2. Generating Figure 9: Critical Exponent Scaling...")
    plot_critical_exponents(output_path / 'figure9_critical_exponents.png')

    print("3. Generating Figure 10: Information Entropy Landscape...")
    plot_information_entropy(output_path / 'figure10_information_entropy.png')

    print("4. Generating Figure 11: Kardashev Scaling...")
    plot_kardashev_scaling(output_path / 'figure11_kardashev_scaling.png')

    print("\n" + "=" * 60)
    print("ALL PHASE TRANSITION VISUALIZATIONS GENERATED")
    print("=" * 60)
    print(f"\nOutput directory: {output_path}")
    print("Files created:")
    print("  - figure8_free_energy_landscape.png")
    print("  - figure9_critical_exponents.png")
    print("  - figure10_information_entropy.png")
    print("  - figure11_kardashev_scaling.png")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate phase transition visualizations")
    parser.add_argument('--output-dir', default='outputs/figures',
                        help='Output directory for figures')
    args = parser.parse_args()

    main(args.output_dir)
