#!/usr/bin/env python3
"""
Paper 2C Figure Generator: Laws of Civilizational Coordination
===============================================================

Generates all 16 publication-quality figures for Paper 2C.

Figures:
- Fig 1-7: Core Framework (Threshold, Topology, Trust, ROI, Sensitivity, Ranking, Phase)
- Fig 8-16: Extended Framework (Landau, Critical, Entropy, Kardashev, Filter, Meta, ESS, Wisdom, AI)

Usage:
    python generate_figures.py --output-dir ../figures
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path


# Publication-quality settings
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
    'savefig.pad_inches': 0.1,
})


# Key constants from the theory
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio
THETA_THEORETICAL = 1 / PHI**2  # 0.382
THETA_EMPIRICAL = 0.375


def fig1_core_engine(output_dir: Path):
    """Figure 1: The Core Engine - Threshold + Cascade Phase Diagram"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left panel: K threshold dynamics
    ax1 = axes[0]
    K = np.linspace(0, 1, 100)
    cascade_prob = 1 / (1 + np.exp(20 * (K - THETA_EMPIRICAL)))

    ax1.plot(K, cascade_prob, 'b-', linewidth=2)
    ax1.axvline(THETA_EMPIRICAL, color='r', linestyle='--', linewidth=1.5,
                label=f'θ = {THETA_EMPIRICAL:.3f}')
    ax1.fill_between(K, cascade_prob, where=K < THETA_EMPIRICAL, alpha=0.3, color='red',
                     label='Collapse Zone')
    ax1.fill_between(K, cascade_prob, where=K >= THETA_EMPIRICAL, alpha=0.3, color='green',
                     label='Stable Zone')

    ax1.set_xlabel('K (Coordination Index)')
    ax1.set_ylabel('P(Cascade)')
    ax1.set_title('A) Threshold Dynamics')
    ax1.legend()
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3)

    # Right panel: Cascade phase diagram
    ax2 = axes[1]
    decay_rate = np.linspace(0.01, 0.2, 50)
    coupling = np.linspace(0, 2, 50)
    D, C = np.meshgrid(decay_rate, coupling)

    # Phase boundary: cascade occurs when coupling > threshold/decay
    phase = np.where(C > THETA_EMPIRICAL / D, 1, 0)

    ax2.contourf(D, C, phase, levels=[0, 0.5, 1], colors=['green', 'red'], alpha=0.5)
    ax2.contour(D, C, phase, levels=[0.5], colors='black', linewidths=2)
    ax2.set_xlabel('Decay Rate (δ)')
    ax2.set_ylabel('Inter-Harmony Coupling (γ)')
    ax2.set_title('B) Cascade Phase Diagram')

    # Add region labels
    ax2.text(0.15, 0.5, 'Stable\nCoordination', ha='center', fontsize=10, fontweight='bold')
    ax2.text(0.05, 1.5, 'Cascade\nCollapse', ha='center', fontsize=10, fontweight='bold',
             color='white')

    plt.tight_layout()
    save_figure(fig, output_dir, 'figure_1_core_engine')


def fig2_topology_comparison(output_dir: Path):
    """Figure 2: Topology Comparison - Star vs Mesh vs Clustered"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    topologies = [
        ('Star (Soviet)', 'hub-spoke', 0.85, 'red'),
        ('Mesh (Market)', 'distributed', 0.45, 'green'),
        ('Clustered (Rome)', 'hierarchical', 0.65, 'orange')
    ]

    for ax, (name, topo_type, fragility, color) in zip(axes, topologies):
        # Draw network topology
        n_nodes = 12
        angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
        x = np.cos(angles)
        y = np.sin(angles)

        ax.scatter(x, y, s=100, c='lightblue', edgecolors='black', zorder=3)

        if topo_type == 'hub-spoke':
            # Central hub
            ax.scatter([0], [0], s=200, c='red', edgecolors='black', zorder=4)
            for i in range(n_nodes):
                ax.plot([0, x[i]], [0, y[i]], 'k-', alpha=0.5, linewidth=1)
        elif topo_type == 'distributed':
            # Many connections
            for i in range(n_nodes):
                for j in range(i+1, n_nodes):
                    if np.random.random() > 0.4:
                        ax.plot([x[i], x[j]], [y[i], y[j]], 'k-', alpha=0.3, linewidth=0.5)
        else:  # hierarchical
            # Cluster heads + inter-cluster
            ax.scatter([0], [0], s=150, c='orange', edgecolors='black', zorder=4)
            for i in range(0, n_nodes, 4):
                ax.scatter([x[i]], [y[i]], s=120, c='yellow', edgecolors='black', zorder=3.5)
                ax.plot([0, x[i]], [0, y[i]], 'k-', alpha=0.7, linewidth=1.5)
                for j in range(1, 4):
                    if i+j < n_nodes:
                        ax.plot([x[i], x[i+j]], [y[i], y[i+j]], 'k-', alpha=0.3, linewidth=0.5)

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(f'{name}\nFragility: {fragility:.2f}', fontsize=11)

        # Add fragility bar
        ax.barh([-1.3], [fragility], height=0.1, color=color, alpha=0.7)
        ax.set_xlim(-1.5, 1.5)

    plt.suptitle('Network Topology and Systemic Fragility', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_figure(fig, output_dir, 'figure_2_topology_comparison')


def fig3_dark_trust_iceberg(output_dir: Path):
    """Figure 3: The Dark Trust Iceberg / Coercion Cliff"""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create iceberg shape
    trust = np.linspace(0, 1, 100)

    # Visible (above water) - formal institutions
    visible = np.minimum(trust, 0.3) * 2

    # Hidden (below water) - dark trust
    hidden = (trust - 0.3).clip(0) * 3

    # Coercion cliff
    coercion = np.where(trust < THETA_EMPIRICAL,
                        1 - trust/THETA_EMPIRICAL,
                        0.1)

    ax.fill_between(trust, 0, visible, alpha=0.5, color='skyblue', label='Visible Trust (Formal)')
    ax.fill_between(trust, -hidden, 0, alpha=0.7, color='darkblue', label='Dark Trust (Informal)')
    ax.plot(trust, coercion, 'r-', linewidth=2, label='Coercion Level')
    ax.axhline(0, color='black', linewidth=2)  # Waterline
    ax.axvline(THETA_EMPIRICAL, color='orange', linestyle='--', linewidth=2,
               label=f'Threshold θ={THETA_EMPIRICAL:.3f}')

    # Add "waterline" label
    ax.text(0.8, 0.05, 'Waterline', fontsize=10, ha='center')

    # Add zone labels
    ax.text(0.15, 0.8, 'Coercion\nDominates', fontsize=10, ha='center', color='red')
    ax.text(0.7, 0.8, 'Trust\nDominates', fontsize=10, ha='center', color='green')

    ax.set_xlabel('Trust Level (H₃)')
    ax.set_ylabel('Social Structure')
    ax.set_title('The Dark Trust Iceberg: Visible vs Hidden Coordination')
    ax.legend(loc='upper right')
    ax.set_xlim(0, 1)
    ax.set_ylim(-1.5, 1.5)
    ax.grid(True, alpha=0.3)

    save_figure(fig, output_dir, 'figure_3_dark_trust_iceberg')


def fig4_intervention_roi(output_dir: Path):
    """Figure 4: Intervention ROI Curve"""
    fig, ax = plt.subplots(figsize=(10, 6))

    K = np.linspace(0.1, 0.9, 100)

    # ROI is highest near threshold, drops off at extremes
    # Based on Law 12: dK/d(investment) = k_i(θ - K)
    roi = np.exp(-((K - THETA_EMPIRICAL)**2) / 0.02) * 10

    ax.plot(K, roi, 'b-', linewidth=2.5)
    ax.fill_between(K, roi, alpha=0.3, color='blue')
    ax.axvline(THETA_EMPIRICAL, color='red', linestyle='--', linewidth=2,
               label=f'θ = {THETA_EMPIRICAL:.3f}')

    # Mark zones
    ax.annotate('Maximum ROI\nIntervention Window',
                xy=(THETA_EMPIRICAL, roi.max()),
                xytext=(THETA_EMPIRICAL + 0.2, roi.max() * 0.8),
                fontsize=10, ha='center',
                arrowprops=dict(arrowstyle='->', color='black'))

    ax.text(0.2, 2, 'Low ROI:\nSystem too\ndegraded', fontsize=9, ha='center', color='gray')
    ax.text(0.75, 2, 'Low ROI:\nSystem already\nstable', fontsize=9, ha='center', color='gray')

    ax.set_xlabel('K (Coordination Index)')
    ax.set_ylabel('Intervention ROI')
    ax.set_title('Intervention Return on Investment: The Threshold Sweet Spot')
    ax.legend()
    ax.set_xlim(0.1, 0.9)
    ax.set_ylim(0, 12)
    ax.grid(True, alpha=0.3)

    save_figure(fig, output_dir, 'figure_4_intervention_roi')


def fig5_cascade_tornado(output_dir: Path):
    """Figure 5: Cascade Velocity Tornado (Sensitivity Analysis)"""
    fig, ax = plt.subplots(figsize=(10, 7))

    parameters = [
        'Trust decay rate (δ₃)',
        'Inter-harmony coupling (γ)',
        'Initial K value (K₀)',
        'Recovery capacity (ρ)',
        'External shock (σ)',
        'Network density (ν)',
        'Information lag (τ)'
    ]

    # Sensitivity values (normalized)
    low_sensitivity = [-0.8, -0.6, -0.5, -0.3, -0.4, -0.2, -0.1]
    high_sensitivity = [0.9, 0.7, 0.5, 0.4, 0.5, 0.3, 0.2]

    y_pos = np.arange(len(parameters))

    ax.barh(y_pos, low_sensitivity, align='center', color='blue', alpha=0.7, label='Low value')
    ax.barh(y_pos, high_sensitivity, align='center', color='red', alpha=0.7, label='High value')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(parameters)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_xlabel('Impact on Cascade Velocity')
    ax.set_title('Cascade Velocity Sensitivity Analysis')
    ax.legend(loc='lower right')
    ax.set_xlim(-1, 1)
    ax.grid(True, axis='x', alpha=0.3)

    save_figure(fig, output_dir, 'figure_5_cascade_tornado')


def fig6_ranking_stability(output_dir: Path):
    """Figure 6: Ranking Stability Heatmap (Rome vs Soviet)"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    harmonies = ['H₁', 'H₂', 'H₃', 'H₄', 'H₅', 'H₆', 'H₇']
    n = len(harmonies)

    # Rome: gradual cascade, rankings shift slowly
    rome_matrix = np.array([
        [1.0, 0.9, 0.8, 0.6, 0.4, 0.3, 0.2],  # H1
        [0.9, 1.0, 0.85, 0.7, 0.5, 0.4, 0.3],  # H2
        [0.8, 0.85, 1.0, 0.75, 0.55, 0.45, 0.35],  # H3
        [0.6, 0.7, 0.75, 1.0, 0.7, 0.55, 0.4],  # H4
        [0.4, 0.5, 0.55, 0.7, 1.0, 0.75, 0.55],  # H5
        [0.3, 0.4, 0.45, 0.55, 0.75, 1.0, 0.7],  # H6
        [0.2, 0.3, 0.35, 0.4, 0.55, 0.7, 1.0],  # H7
    ])

    # Soviet: rapid cascade, rankings shift abruptly
    soviet_matrix = np.array([
        [1.0, 0.95, 0.3, 0.2, 0.15, 0.1, 0.05],  # H1
        [0.95, 1.0, 0.35, 0.25, 0.2, 0.15, 0.1],  # H2
        [0.3, 0.35, 1.0, 0.4, 0.3, 0.2, 0.15],  # H3
        [0.2, 0.25, 0.4, 1.0, 0.5, 0.3, 0.2],  # H4
        [0.15, 0.2, 0.3, 0.5, 1.0, 0.6, 0.4],  # H5
        [0.1, 0.15, 0.2, 0.3, 0.6, 1.0, 0.7],  # H6
        [0.05, 0.1, 0.15, 0.2, 0.4, 0.7, 1.0],  # H7
    ])

    for ax, matrix, title in [(axes[0], rome_matrix, 'Rome (Gradual)'),
                               (axes[1], soviet_matrix, 'Soviet (Rapid)')]:
        im = ax.imshow(matrix, cmap='RdYlGn', vmin=0, vmax=1)
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels(harmonies)
        ax.set_yticklabels(harmonies)
        ax.set_xlabel('Time Period t₂')
        ax.set_ylabel('Time Period t₁')
        ax.set_title(title)

        # Add values
        for i in range(n):
            for j in range(n):
                color = 'white' if matrix[i,j] < 0.5 else 'black'
                ax.text(j, i, f'{matrix[i,j]:.2f}', ha='center', va='center',
                       fontsize=7, color=color)

    plt.colorbar(im, ax=axes, label='Rank Correlation', shrink=0.8)
    plt.suptitle('Harmony Ranking Stability Over Time', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_figure(fig, output_dir, 'figure_6_ranking_stability')


def fig7_cascade_phase_diagram(output_dir: Path):
    """Figure 7: Cascade Velocity Phase Diagram"""
    fig, ax = plt.subplots(figsize=(10, 8))

    K = np.linspace(0.1, 0.9, 100)
    dK = np.linspace(-0.1, 0.05, 100)
    K_grid, dK_grid = np.meshgrid(K, dK)

    # Phase: collapse if K < theta AND dK < 0
    # Recovery if K > theta OR dK > 0
    phase = np.where((K_grid < THETA_EMPIRICAL) & (dK_grid < 0), -1,
                     np.where((K_grid > THETA_EMPIRICAL) | (dK_grid > 0.02), 1, 0))

    cmap = LinearSegmentedColormap.from_list('phase', ['red', 'yellow', 'green'])
    im = ax.contourf(K_grid, dK_grid, phase, levels=[-1.5, -0.5, 0.5, 1.5],
                     cmap=cmap, alpha=0.6)

    ax.axvline(THETA_EMPIRICAL, color='black', linestyle='--', linewidth=2)
    ax.axhline(0, color='black', linestyle='-', linewidth=1)

    # Add trajectories
    t = np.linspace(0, 10, 100)

    # Collapse trajectory
    K_collapse = 0.6 * np.exp(-0.3 * t) + 0.15
    dK_collapse = -0.18 * np.exp(-0.3 * t)
    ax.plot(K_collapse, dK_collapse, 'r-', linewidth=2, label='Collapse (Rome)')
    ax.annotate('', xy=(K_collapse[-1], dK_collapse[-1]),
                xytext=(K_collapse[-20], dK_collapse[-20]),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))

    # Recovery trajectory
    K_recover = 0.3 + 0.4 * (1 - np.exp(-0.2 * t))
    dK_recover = 0.08 * np.exp(-0.2 * t)
    ax.plot(K_recover, dK_recover, 'g-', linewidth=2, label='Recovery')
    ax.annotate('', xy=(K_recover[-1], dK_recover[-1]),
                xytext=(K_recover[-20], dK_recover[-20]),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))

    ax.set_xlabel('K (Coordination Index)')
    ax.set_ylabel('dK/dt (Rate of Change)')
    ax.set_title('Cascade Velocity Phase Diagram')
    ax.legend(loc='upper left')
    ax.text(THETA_EMPIRICAL + 0.02, -0.08, f'θ = {THETA_EMPIRICAL:.3f}', fontsize=10)
    ax.set_xlim(0.1, 0.9)
    ax.set_ylim(-0.1, 0.05)
    ax.grid(True, alpha=0.3)

    save_figure(fig, output_dir, 'figure_7_cascade_phase_diagram')


def fig8_landau_free_energy(output_dir: Path):
    """Figure 8: Landau Free Energy Landscape (Phase Transition)"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    K = np.linspace(-0.5, 1.5, 200)

    # Three scenarios: pre-critical, critical, post-critical
    scenarios = [
        ('Pre-Critical (K > θ)', 0.1, 'green'),
        ('Critical Point (K = θ)', 0.0, 'orange'),
        ('Post-Critical (K < θ)', -0.1, 'red')
    ]

    for ax, (title, a, color) in zip(axes, scenarios):
        # Landau free energy: F = a*K^2 + b*K^4
        b = 0.5
        F = a * (K - THETA_EMPIRICAL)**2 + b * (K - THETA_EMPIRICAL)**4

        ax.plot(K, F, color=color, linewidth=2.5)
        ax.fill_between(K, F, F.min(), alpha=0.2, color=color)

        # Find and mark minima
        idx_min = np.argmin(F)
        ax.scatter([K[idx_min]], [F[idx_min]], s=100, c=color, zorder=5,
                   edgecolors='black', linewidth=2)

        ax.axvline(THETA_EMPIRICAL, color='gray', linestyle='--', alpha=0.5)
        ax.set_xlabel('K (Order Parameter)')
        ax.set_ylabel('Free Energy F(K)')
        ax.set_title(title)
        ax.set_xlim(0, 1)
        ax.grid(True, alpha=0.3)

    plt.suptitle('Landau Free Energy: Phase Transition Formalism', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_figure(fig, output_dir, 'figure_8_landau_free_energy')


def fig9_critical_exponents(output_dir: Path):
    """Figure 9: Critical Exponent Scaling (Universal Behavior)"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Order parameter scaling
    ax1 = axes[0]
    epsilon = np.linspace(0.001, 0.3, 100)  # Distance from critical point

    # Mean-field exponent β = 1/2
    beta = 0.5
    order_param = epsilon**beta

    ax1.loglog(epsilon, order_param, 'b-', linewidth=2, label=f'β = {beta:.1f}')
    ax1.set_xlabel('|K - θ| (Distance from critical point)')
    ax1.set_ylabel('Order Parameter ψ')
    ax1.set_title('A) Order Parameter Scaling')
    ax1.legend()
    ax1.grid(True, alpha=0.3, which='both')

    # Right: Susceptibility scaling
    ax2 = axes[1]

    # Mean-field exponent γ = 1
    gamma = 1.0
    susceptibility = epsilon**(-gamma)

    ax2.loglog(epsilon, susceptibility, 'r-', linewidth=2, label=f'γ = {gamma:.1f}')
    ax2.set_xlabel('|K - θ| (Distance from critical point)')
    ax2.set_ylabel('Susceptibility χ')
    ax2.set_title('B) Susceptibility Divergence')
    ax2.legend()
    ax2.grid(True, alpha=0.3, which='both')

    # Add theoretical prediction lines
    ax2.axhline(100, color='gray', linestyle='--', alpha=0.5)
    ax2.text(0.1, 120, 'Early Warning Signal Threshold', fontsize=9, color='gray')

    plt.suptitle('Critical Exponents: Universal Scaling Near Threshold', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_figure(fig, output_dir, 'figure_9_critical_exponents')


def fig10_information_entropy(output_dir: Path):
    """Figure 10: Information Entropy Landscape (Law 13)"""
    fig, ax = plt.subplots(figsize=(10, 7))

    # Trust level determines information entropy
    trust = np.linspace(0.01, 0.99, 100)

    # Binary entropy: H(p) = -p*log(p) - (1-p)*log(1-p)
    entropy = -trust * np.log2(trust) - (1-trust) * np.log2(1-trust)

    ax.plot(trust, entropy, 'b-', linewidth=2.5)
    ax.fill_between(trust, entropy, alpha=0.3, color='blue')

    # Mark key points
    ax.axvline(0.5, color='red', linestyle='--', linewidth=2, label='Maximum Entropy (H₃=0.5)')
    ax.axvline(THETA_EMPIRICAL, color='orange', linestyle='--', linewidth=2,
               label=f'Threshold θ={THETA_EMPIRICAL:.3f}')

    # Calculate entropy at threshold
    entropy_at_theta = -THETA_EMPIRICAL * np.log2(THETA_EMPIRICAL) - (1-THETA_EMPIRICAL) * np.log2(1-THETA_EMPIRICAL)
    ax.scatter([THETA_EMPIRICAL], [entropy_at_theta], s=100, c='orange', zorder=5,
               edgecolors='black', linewidth=2)
    ax.text(THETA_EMPIRICAL + 0.05, entropy_at_theta, f'H(θ) = {entropy_at_theta:.3f}', fontsize=10)

    # Add zone labels
    ax.text(0.15, 0.5, 'Low Trust\nHigh Uncertainty', fontsize=10, ha='center', color='gray')
    ax.text(0.85, 0.5, 'High Trust\nLow Uncertainty', fontsize=10, ha='center', color='gray')

    ax.set_xlabel('Trust Level (H₃)')
    ax.set_ylabel('Information Entropy (bits)')
    ax.set_title('Information Entropy as Function of Trust\n(Law 13: H₃ as Information Hub)')
    ax.legend(loc='upper right')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3)

    save_figure(fig, output_dir, 'figure_10_information_entropy')


def fig11_kardashev_scaling(output_dir: Path):
    """Figure 11: Kardashev Scaling of K_max"""
    fig, ax = plt.subplots(figsize=(10, 7))

    # Kardashev types
    K_type = np.array([0.7, 1.0, 2.0, 3.0])
    K_max_theory = THETA_THEORETICAL * K_type  # Theoretical maximum K scales with Kardashev

    # Add Earth's current position
    earth_kardashev = 0.73
    earth_K = 0.45  # Current estimate

    ax.plot(K_type, K_max_theory, 'b-o', linewidth=2, markersize=10, label='K_max Scaling')
    ax.scatter([earth_kardashev], [earth_K], s=200, c='green', marker='*',
               zorder=5, label='Earth (2024)')

    # Add labels for each type
    labels = ['Type 0.7\n(Earth)', 'Type I\n(Planetary)', 'Type II\n(Stellar)', 'Type III\n(Galactic)']
    for i, (kt, km, label) in enumerate(zip(K_type, K_max_theory, labels)):
        ax.annotate(label, (kt, km), textcoords='offset points', xytext=(0, 15),
                   ha='center', fontsize=9)

    # Add threshold line
    ax.axhline(THETA_EMPIRICAL, color='red', linestyle='--', linewidth=1.5,
               label=f'Collapse Threshold θ={THETA_EMPIRICAL:.3f}')

    # Shade danger zone
    ax.fill_between([0.5, 3.5], 0, THETA_EMPIRICAL, alpha=0.2, color='red',
                    label='Collapse Zone')

    ax.set_xlabel('Kardashev Type')
    ax.set_ylabel('Maximum Sustainable K')
    ax.set_title('Kardashev Scaling: Coordination Capacity vs Energy Scale')
    ax.legend(loc='upper left')
    ax.set_xlim(0.5, 3.5)
    ax.set_ylim(0, 1.5)
    ax.grid(True, alpha=0.3)

    save_figure(fig, output_dir, 'figure_11_kardashev_scaling')


def fig12_great_filter(output_dir: Path):
    """Figure 12: The Great Filter as Coordination Threshold"""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create a funnel showing civilization progression
    stages = ['Microbial', 'Multicellular', 'Intelligence', 'Technology',
              'Coordination\nThreshold', 'Interstellar', 'Type III']
    n = len(stages)

    # Number of civilizations at each stage (log scale, hypothetical)
    n_civs = [1e12, 1e9, 1e6, 1e4, 1e2, 1e1, 1e0]  # Exponential filter

    # Filter intensity (bigger drop = stronger filter)
    filter_strength = [0.999, 0.999, 0.99, 0.99, 0.99, 0.9]

    y_pos = np.arange(n)
    colors = ['green']*4 + ['red'] + ['blue']*2

    bars = ax.barh(y_pos, np.log10(n_civs), color=colors, alpha=0.7)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages)
    ax.set_xlabel('log₁₀(Number of Civilizations)')
    ax.set_title('The Great Filter as Coordination Threshold\n(Modified Drake Equation)')

    # Highlight the threshold
    ax.axhspan(3.5, 4.5, alpha=0.3, color='red', label='Coordination Threshold Filter')
    ax.text(6, 4, f'θ = {THETA_EMPIRICAL:.3f}\n~99% fail', fontsize=10, ha='center',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.legend(loc='upper right')
    ax.set_xlim(0, 14)
    ax.grid(True, axis='x', alpha=0.3)

    save_figure(fig, output_dir, 'figure_12_great_filter')


def fig13_metacognitive_levels(output_dir: Path):
    """Figure 13: Metacognitive Levels and Collapse Trajectory (Law 15)"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Metacognitive levels
    ax1 = axes[0]
    levels = ['Level 0:\nUnaware', 'Level 1:\nAware of K',
              'Level 2:\nAware of\nAwareness', 'Level 3:\nCan Change\nAwareness']
    colors = ['red', 'orange', 'yellow', 'green']
    heights = [1, 2, 3, 4]

    bars = ax1.bar(range(4), heights, color=colors, alpha=0.7, edgecolor='black')
    ax1.set_xticks(range(4))
    ax1.set_xticklabels(levels, fontsize=8)
    ax1.set_ylabel('Metacognitive Capacity')
    ax1.set_title('A) Metacognitive Levels')

    # Add threshold line
    ax1.axhline(1.5, color='red', linestyle='--', linewidth=2,
                label=f'Minimum for Recovery')
    ax1.legend(loc='upper left')

    # Right: Collapse trajectory by metacognitive level
    ax2 = axes[1]
    t = np.linspace(0, 20, 100)

    # Different trajectories based on metacognitive level
    K_level0 = 0.6 * np.exp(-0.2 * t) + 0.15  # Collapse
    K_level1 = 0.5 * np.exp(-0.1 * t) + 0.25  # Slower collapse
    K_level2 = 0.4 + 0.1 * np.sin(0.5 * t) * np.exp(-0.05 * t)  # Oscillates near threshold
    K_level3 = 0.4 + 0.15 * (1 - np.exp(-0.1 * t))  # Recovery

    ax2.plot(t, K_level0, 'r-', linewidth=2, label='Level 0 (Collapse)')
    ax2.plot(t, K_level1, color='orange', linewidth=2, label='Level 1 (Slow Collapse)')
    ax2.plot(t, K_level2, 'y-', linewidth=2, label='Level 2 (Oscillation)')
    ax2.plot(t, K_level3, 'g-', linewidth=2, label='Level 3 (Recovery)')

    ax2.axhline(THETA_EMPIRICAL, color='gray', linestyle='--', linewidth=1.5,
                label=f'θ = {THETA_EMPIRICAL:.3f}')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('K (Coordination Index)')
    ax2.set_title('B) K Trajectory by Metacognitive Level')
    ax2.legend(loc='upper right', fontsize=8)
    ax2.set_xlim(0, 20)
    ax2.set_ylim(0.1, 0.7)
    ax2.grid(True, alpha=0.3)

    plt.suptitle('Metacognitive Collapse Theory (Law 15)', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_figure(fig, output_dir, 'figure_13_metacognitive_levels')


def fig14_evolutionary_stability(output_dir: Path):
    """Figure 14: Evolutionary Stability Landscape (Law 16)"""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Create fitness landscape
    cooperation = np.linspace(0, 1, 100)
    trust = np.linspace(0, 1, 100)
    C, T = np.meshgrid(cooperation, trust)

    # Fitness: high when both are high, but defection temptation creates ridge
    # ESS analysis shows cooperation is NOT stable below threshold
    fitness = C * T - 0.3 * (1-C) * (T > THETA_EMPIRICAL).astype(float)

    # Add defection basin
    defection_basin = np.where(T < THETA_EMPIRICAL, -0.5 * (1-C), 0)
    fitness = fitness + defection_basin

    im = ax.contourf(C, T, fitness, levels=20, cmap='RdYlGn')
    ax.contour(C, T, fitness, levels=10, colors='black', alpha=0.3, linewidths=0.5)

    # Mark threshold
    ax.axhline(THETA_EMPIRICAL, color='white', linestyle='--', linewidth=2,
               label=f'θ = {THETA_EMPIRICAL:.3f}')

    # Mark ESS point
    ax.scatter([1], [0.8], s=200, c='white', marker='*', edgecolors='black',
               linewidth=2, label='Cooperation ESS', zorder=5)

    # Mark defection attractor
    ax.scatter([0], [0.2], s=150, c='black', marker='x', linewidth=3,
               label='Defection Attractor', zorder=5)

    ax.set_xlabel('Cooperation Level')
    ax.set_ylabel('Trust Level (H₃)')
    ax.set_title('Evolutionary Stability Landscape\n(Law 16: Cooperation is NOT an ESS below θ)')
    ax.legend(loc='upper left', fontsize=9)

    plt.colorbar(im, ax=ax, label='Fitness')

    save_figure(fig, output_dir, 'figure_14_evolutionary_stability')


def fig15_wisdom_silence(output_dir: Path):
    """Figure 15: The Wisdom Silence - Contact Safety Boundary"""
    fig, ax = plt.subplots(figsize=(10, 7))

    # Create safety boundary visualization
    K_civilization = np.linspace(0.2, 1.0, 100)

    # Safety factor increases with K
    safety = (K_civilization / THETA_EMPIRICAL) ** 2

    # Contact probability increases with K (but plateaus)
    contact_prob = 1 - np.exp(-2 * (K_civilization - THETA_EMPIRICAL).clip(0))

    ax.plot(K_civilization, safety, 'b-', linewidth=2.5, label='Safety Factor')
    ax.plot(K_civilization, contact_prob, 'g--', linewidth=2.5, label='Contact Probability')

    # Shade unsafe zone
    ax.fill_between(K_civilization, 0, safety, where=K_civilization < THETA_EMPIRICAL,
                    alpha=0.3, color='red', label='Unsafe for Contact')
    ax.fill_between(K_civilization, 0, safety, where=K_civilization >= THETA_EMPIRICAL,
                    alpha=0.3, color='green', label='Safe for Contact')

    ax.axvline(THETA_EMPIRICAL, color='orange', linestyle='--', linewidth=2,
               label=f'θ = {THETA_EMPIRICAL:.3f}')

    # Add wisdom silence region
    ax.axhspan(0.8, 1.2, xmin=0, xmax=0.3, alpha=0.4, color='purple')
    ax.text(0.25, 0.95, 'The Wisdom\nSilence', fontsize=10, ha='center', color='purple')

    ax.set_xlabel('K (Coordination Index)')
    ax.set_ylabel('Safety / Probability')
    ax.set_title('The Wisdom Silence: Why Advanced Civilizations May Avoid Contact')
    ax.legend(loc='center right', fontsize=9)
    ax.set_xlim(0.2, 1.0)
    ax.set_ylim(0, 1.2)
    ax.grid(True, alpha=0.3)

    save_figure(fig, output_dir, 'figure_15_wisdom_silence')


def fig16_ai_coordination_paradox(output_dir: Path):
    """Figure 16: The AI Coordination Paradox - Amplification Dynamics (Law 17)"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: AI amplification scenarios
    ax1 = axes[0]
    t = np.linspace(0, 30, 100)
    K_initial = 0.45

    # Three scenarios
    # Scenario A: AI accelerates coordination (positive)
    K_positive = K_initial + 0.4 * (1 - np.exp(-0.1 * t))

    # Scenario B: AI accelerates collapse (negative)
    K_negative = K_initial * np.exp(-0.15 * t) + 0.1

    # Scenario C: AI creates oscillations (unstable)
    K_oscillate = K_initial + 0.15 * np.sin(0.5 * t) * np.exp(-0.02 * t)

    ax1.plot(t, K_positive, 'g-', linewidth=2.5, label='AI-Assisted Coordination (35%)')
    ax1.plot(t, K_oscillate, 'orange', linewidth=2.5, label='Unstable Amplification (45%)')
    ax1.plot(t, K_negative, 'r-', linewidth=2.5, label='AI-Accelerated Collapse (20%)')

    ax1.axhline(THETA_EMPIRICAL, color='black', linestyle='--', linewidth=1.5,
                label=f'θ = {THETA_EMPIRICAL:.3f}')
    ax1.fill_between(t, 0, THETA_EMPIRICAL, alpha=0.1, color='red')

    ax1.set_xlabel('Time (years from AI deployment)')
    ax1.set_ylabel('K (Coordination Index)')
    ax1.set_title('A) AI Coordination Scenarios')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.set_xlim(0, 30)
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3)

    # Right: Critical window analysis
    ax2 = axes[1]

    # The window of AI influence on coordination
    ai_capability = np.linspace(0, 2, 100)  # AI capability index

    # Positive potential: peaks at moderate capability
    positive = 0.8 * ai_capability * np.exp(-0.5 * ai_capability)

    # Negative potential: increases with capability
    negative = 0.3 * ai_capability ** 1.5

    # Net effect
    net = positive - negative

    ax2.plot(ai_capability, positive, 'g-', linewidth=2, label='Coordination Enhancement')
    ax2.plot(ai_capability, negative, 'r-', linewidth=2, label='Fragmentation Risk')
    ax2.plot(ai_capability, net, 'b-', linewidth=2.5, label='Net Effect')
    ax2.fill_between(ai_capability, net, 0, where=net > 0, alpha=0.3, color='green')
    ax2.fill_between(ai_capability, net, 0, where=net < 0, alpha=0.3, color='red')

    ax2.axhline(0, color='black', linewidth=1)
    ax2.axvline(0.8, color='orange', linestyle='--', linewidth=1.5,
                label='Critical Window')

    ax2.set_xlabel('AI Capability Index')
    ax2.set_ylabel('Effect on Coordination')
    ax2.set_title('B) Critical Window Analysis')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlim(0, 2)
    ax2.grid(True, alpha=0.3)

    # Add annotation
    ax2.annotate('Optimal\nIntervention\nPoint', xy=(0.8, 0.15),
                 xytext=(1.2, 0.3), fontsize=9,
                 arrowprops=dict(arrowstyle='->', color='orange'))

    plt.suptitle('The AI Coordination Paradox (Law 17)', fontsize=13, fontweight='bold')
    plt.tight_layout()
    save_figure(fig, output_dir, 'figure_16_ai_coordination_paradox')


def save_figure(fig, output_dir: Path, name: str):
    """Save figure in both PDF and PNG formats."""
    for ext in ['pdf', 'png']:
        filepath = output_dir / f'{name}.{ext}'
        fig.savefig(filepath, format=ext, dpi=300 if ext == 'png' else None)
        print(f'  Saved: {filepath}')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description='Generate Paper 2C figures')
    parser.add_argument('--output-dir', type=str, default='../figures',
                        help='Output directory for figures')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f'Generating Paper 2C figures in: {output_dir}')
    print(f'Golden threshold θ = {THETA_EMPIRICAL:.3f} (empirical)')
    print(f'                θ = {THETA_THEORETICAL:.3f} (theoretical = 1/φ²)')
    print()

    # Generate all figures
    figures = [
        ('Figure 1: Core Engine', fig1_core_engine),
        ('Figure 2: Topology Comparison', fig2_topology_comparison),
        ('Figure 3: Dark Trust Iceberg', fig3_dark_trust_iceberg),
        ('Figure 4: Intervention ROI', fig4_intervention_roi),
        ('Figure 5: Cascade Tornado', fig5_cascade_tornado),
        ('Figure 6: Ranking Stability', fig6_ranking_stability),
        ('Figure 7: Cascade Phase Diagram', fig7_cascade_phase_diagram),
        ('Figure 8: Landau Free Energy', fig8_landau_free_energy),
        ('Figure 9: Critical Exponents', fig9_critical_exponents),
        ('Figure 10: Information Entropy', fig10_information_entropy),
        ('Figure 11: Kardashev Scaling', fig11_kardashev_scaling),
        ('Figure 12: Great Filter', fig12_great_filter),
        ('Figure 13: Metacognitive Levels', fig13_metacognitive_levels),
        ('Figure 14: Evolutionary Stability', fig14_evolutionary_stability),
        ('Figure 15: Wisdom Silence', fig15_wisdom_silence),
        ('Figure 16: AI Coordination Paradox', fig16_ai_coordination_paradox),
    ]

    for name, func in figures:
        print(f'Generating {name}...')
        func(output_dir)

    print()
    print(f'Successfully generated {len(figures)} figures!')


if __name__ == '__main__':
    main()
