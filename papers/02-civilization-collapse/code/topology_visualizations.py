#!/usr/bin/env python3
"""
Network Topology Visualizations for Law 3 (Network Law)

Generates visual diagrams showing:
- Panel A: Soviet "Star" topology (C=High, R=1)
- Panel B: Market "Mesh" topology (C=Low, R=High)
- Panel C: Rome "Clustered" topology (C=High, R=Medium)

Also generates the "Coercion Cliff" visualization for Law 8 (Dark Trust)

Usage:
    python topology_visualizations.py --output-dir outputs/figures/
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
from pathlib import Path


# =============================================================================
# COLOR SCHEMES
# =============================================================================

COLORS = {
    'hub': '#e74c3c',          # Red for central hub
    'node': '#3498db',         # Blue for regular nodes
    'edge': '#7f8c8d',         # Gray for edges
    'cluster': '#2ecc71',      # Green for cluster boundaries
    'cascade': '#e74c3c',      # Red for cascade
    'trust_light': '#27ae60',  # Green for light trust
    'trust_coerced': '#e74c3c', # Red for coerced trust
    'trust_habitual': '#f39c12', # Orange for habitual trust
    'background': '#ecf0f1'    # Light gray background
}


# =============================================================================
# TOPOLOGY DIAGRAMS (FIGURE 2)
# =============================================================================

def draw_star_topology(ax, title="Soviet Model", show_failure=False):
    """
    Panel A: Star topology (Hub-and-Spoke)
    Central node connects to all peripheral nodes.
    Removing center kills 100% of edges.
    """
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)

    # Hub node at center
    hub_color = COLORS['cascade'] if show_failure else COLORS['hub']
    hub = Circle((0, 0), 0.15, color=hub_color, zorder=5)
    ax.add_patch(hub)
    ax.text(0, 0, 'CPSU', ha='center', va='center', fontsize=8,
            color='white', fontweight='bold', zorder=6)

    # Peripheral nodes
    n_nodes = 8
    angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
    radius = 1.0

    for i, angle in enumerate(angles):
        x, y = radius * np.cos(angle), radius * np.sin(angle)

        # Draw edge to hub
        edge_style = '--' if show_failure else '-'
        edge_alpha = 0.3 if show_failure else 0.6
        ax.plot([0, x], [0, y], edge_style, color=COLORS['edge'],
                linewidth=2, alpha=edge_alpha, zorder=1)

        # Draw node
        node_color = COLORS['edge'] if show_failure else COLORS['node']
        node = Circle((x, y), 0.12, color=node_color, zorder=4)
        ax.add_patch(node)

        labels = ['Army', 'KGB', 'Mins.', 'Oblasts', 'Komsomol', 'Unions', 'Media', 'Industry']
        ax.text(x*1.25, y*1.25, labels[i], ha='center', va='center', fontsize=7)

    # Stats
    stats_text = f"C = 0.9 (High)\nR = 1.6 (Low)\nFragility = 1.24"
    if show_failure:
        stats_text += "\n\n❌ Hub fails →\n100% edges lost"
    ax.text(0, -1.4, stats_text, ha='center', va='top', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))


def draw_mesh_topology(ax, title="Market Model"):
    """
    Panel B: Mesh topology (Distributed)
    Many interconnected nodes, no single point of failure.
    """
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)

    # Generate grid of nodes
    n_rows, n_cols = 4, 4
    positions = []
    for i in range(n_rows):
        for j in range(n_cols):
            x = -0.9 + j * 0.6
            y = -0.9 + i * 0.6
            positions.append((x, y))

    # Draw edges (connect nearby nodes)
    for i, (x1, y1) in enumerate(positions):
        for j, (x2, y2) in enumerate(positions):
            if i < j:
                dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
                if dist < 0.7:  # Only connect nearby nodes
                    ax.plot([x1, x2], [y1, y2], '-', color=COLORS['edge'],
                            linewidth=1.5, alpha=0.4, zorder=1)

    # Draw nodes (all equal)
    for x, y in positions:
        node = Circle((x, y), 0.08, color=COLORS['node'], zorder=4)
        ax.add_patch(node)

    # Stats
    stats_text = f"C = 0.2 (Low)\nR = 6.0+ (High)\nFragility = 0.08"
    ax.text(0, -1.4, stats_text, ha='center', va='top', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))


def draw_clustered_topology(ax, title="Roman Model"):
    """
    Panel C: Clustered/Small-World topology (Rome)
    Central hub exists, but clusters are semi-independent.
    Removing center only kills ~30% of edges.
    """
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)

    # Central hub (Emperor)
    hub = Circle((0, 0), 0.12, color=COLORS['hub'], zorder=5)
    ax.add_patch(hub)
    ax.text(0, 0, 'Emperor', ha='center', va='center', fontsize=6,
            color='white', fontweight='bold', zorder=6)

    # Define clusters
    clusters = [
        {'center': (0.8, 0.6), 'name': 'Army', 'n_nodes': 4, 'radius': 0.35},
        {'center': (-0.8, 0.6), 'name': 'Church', 'n_nodes': 4, 'radius': 0.35},
        {'center': (0.8, -0.6), 'name': 'Senate', 'n_nodes': 3, 'radius': 0.30},
        {'center': (-0.8, -0.6), 'name': 'Local', 'n_nodes': 4, 'radius': 0.35},
    ]

    for cluster in clusters:
        cx, cy = cluster['center']
        n = cluster['n_nodes']
        r = cluster['radius']

        # Draw cluster boundary (dashed circle)
        circle = plt.Circle((cx, cy), r + 0.1, fill=False,
                            linestyle='--', color=COLORS['cluster'],
                            linewidth=2, alpha=0.5, zorder=1)
        ax.add_patch(circle)

        # Cluster label
        ax.text(cx, cy + r + 0.18, cluster['name'], ha='center', va='bottom',
                fontsize=8, fontweight='bold', color=COLORS['cluster'])

        # Draw edge from hub to cluster center
        ax.plot([0, cx], [0, cy], '-', color=COLORS['edge'],
                linewidth=2, alpha=0.5, zorder=2)

        # Draw nodes within cluster
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        node_positions = []
        for angle in angles:
            nx, ny = cx + r * 0.6 * np.cos(angle), cy + r * 0.6 * np.sin(angle)
            node_positions.append((nx, ny))
            node = Circle((nx, ny), 0.06, color=COLORS['node'], zorder=4)
            ax.add_patch(node)

        # Connect nodes within cluster (internal redundancy)
        for i, (x1, y1) in enumerate(node_positions):
            for j, (x2, y2) in enumerate(node_positions):
                if i < j:
                    ax.plot([x1, x2], [y1, y2], '-', color=COLORS['node'],
                            linewidth=1, alpha=0.4, zorder=3)

    # Stats
    stats_text = f"C = 0.7 (High)\nR = 3.3 (Medium)\nFragility = 0.17"
    ax.text(0, -1.4, stats_text, ha='center', va='top', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))


def generate_topology_figure(output_path: Path):
    """Generate the complete topology comparison figure."""
    fig = plt.figure(figsize=(14, 5))
    gs = gridspec.GridSpec(1, 4, width_ratios=[1, 1, 1, 0.8])

    # Panel A: Soviet (Star)
    ax1 = fig.add_subplot(gs[0])
    draw_star_topology(ax1, "A. Soviet Model\n(Hub-and-Spoke)")

    # Panel B: Market (Mesh)
    ax2 = fig.add_subplot(gs[1])
    draw_mesh_topology(ax2, "B. Market Model\n(Distributed Mesh)")

    # Panel C: Rome (Clustered)
    ax3 = fig.add_subplot(gs[2])
    draw_clustered_topology(ax3, "C. Roman Model\n(Clustered Small-World)")

    # Panel D: Legend / Key Insight
    ax4 = fig.add_subplot(gs[3])
    ax4.axis('off')

    key_text = """KEY INSIGHT

Centralization (C)
→ Affects cascade ONSET
→ Single shock can trigger

Redundancy (R)
→ Affects cascade VELOCITY
→ More paths = slower spread

Rome Paradox Resolved:
Rome was centralized (C=0.7)
BUT had high redundancy (R=3.3)

When Emperor failed,
clusters continued functioning,
slowing the cascade.

Soviet had C=0.9, R=1.6
→ Fast collapse (6 years)

Rome had C=0.7, R=3.3
→ Slow collapse (250 years)

Formula:
v_cascade ∝ 1/√R
"""
    ax4.text(0.05, 0.95, key_text, transform=ax4.transAxes,
             fontsize=9, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    fig.savefig(output_path / 'figure2_topology_comparison.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    fig.savefig(output_path / 'figure2_topology_comparison.pdf',
                bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_path / 'figure2_topology_comparison.png'}")


# =============================================================================
# DARK TRUST VISUALIZATION (FIGURE 3)
# =============================================================================

def generate_dark_trust_figure(output_path: Path):
    """
    Generate the "Iceberg" / "Coercion Cliff" visualization for Law 8.

    Shows:
    - H3_light (organic trust) - low, stable baseline
    - H3_coerced (forced compliance) - high, fragile block
    - H3_habitual (behavioral inertia) - medium, slowly decaying
    - Shock event showing discontinuous collapse
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # =========================================================================
    # Panel A: The "Iceberg" - Trust Decomposition
    # =========================================================================
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 0.7)
    ax1.set_xlabel('', fontsize=12)
    ax1.set_ylabel('Trust Level (H₃)', fontsize=12)
    ax1.set_title('A. Trust Decomposition: The "Iceberg"', fontsize=14, fontweight='bold')

    # Light trust (organic) - always visible
    light_trust = 0.18
    ax1.fill_between([1, 9], 0, light_trust, color=COLORS['trust_light'],
                     alpha=0.8, label='H₃_light (Organic)')

    # Habitual trust - medium layer
    habitual_trust = 0.12
    ax1.fill_between([1, 9], light_trust, light_trust + habitual_trust,
                     color=COLORS['trust_habitual'], alpha=0.8,
                     label='H₃_habitual (Behavioral)')

    # Coerced trust - top layer (fragile)
    coerced_trust = 0.25
    total_trust = light_trust + habitual_trust + coerced_trust
    ax1.fill_between([1, 9], light_trust + habitual_trust, total_trust,
                     color=COLORS['trust_coerced'], alpha=0.8,
                     label='H₃_coerced (Forced)')

    # Threshold line
    ax1.axhline(y=0.375, color='black', linestyle='--', linewidth=2,
                label='Threshold (θ = 0.375)')
    ax1.text(9.2, 0.375, 'θ', fontsize=12, fontweight='bold', va='center')

    # Annotations
    ax1.annotate('Apparent function\n(surveys see this)', xy=(5, 0.50),
                xytext=(7.5, 0.60), fontsize=10,
                arrowprops=dict(arrowstyle='->', color='gray'),
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax1.annotate('True organic trust\n(would remain if\ncoercion ends)', xy=(5, 0.09),
                xytext=(7.5, 0.08), fontsize=10,
                arrowprops=dict(arrowstyle='->', color='gray'),
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # "Waterline" metaphor
    ax1.axhline(y=light_trust + habitual_trust, color='blue', linestyle=':',
                linewidth=1.5, alpha=0.7)
    ax1.text(0.5, light_trust + habitual_trust + 0.02, '← "Waterline"\n    (visible vs. hidden)',
             fontsize=8, color='blue', va='bottom')

    ax1.set_xticks([])
    ax1.legend(loc='upper left', fontsize=9)
    ax1.set_xlim(0, 10)

    # =========================================================================
    # Panel B: The "Coercion Cliff" - Discontinuous Collapse
    # =========================================================================
    ax2 = axes[1]

    # Time series
    t = np.linspace(0, 30, 300)

    # Phase 1: Stable authoritarian (0-15 years)
    # Phase 2: Shock event (year 15) - coercion fails
    # Phase 3: Rapid cascade (15-25 years)

    H3_light = np.ones_like(t) * 0.18  # Constant low organic trust

    H3_coerced = np.piecewise(t,
        [t < 15, (t >= 15) & (t < 16), t >= 16],
        [0.25, lambda x: 0.25 * (16 - x), 0])  # Sudden drop

    H3_habitual = np.piecewise(t,
        [t < 15, t >= 15],
        [0.12, lambda x: 0.12 * np.exp(-0.15 * (x - 15))])  # Gradual decay

    H3_total = H3_light + H3_coerced + H3_habitual

    # Plot stacked areas
    ax2.fill_between(t, 0, H3_light, color=COLORS['trust_light'], alpha=0.8,
                     label='H₃_light (Organic)')
    ax2.fill_between(t, H3_light, H3_light + H3_habitual,
                     color=COLORS['trust_habitual'], alpha=0.8,
                     label='H₃_habitual')
    ax2.fill_between(t, H3_light + H3_habitual, H3_total,
                     color=COLORS['trust_coerced'], alpha=0.8,
                     label='H₃_coerced')

    # Total trust line
    ax2.plot(t, H3_total, 'k-', linewidth=2, label='H₃_total')

    # Threshold
    ax2.axhline(y=0.375, color='black', linestyle='--', linewidth=2)
    ax2.text(31, 0.375, 'θ', fontsize=12, fontweight='bold', va='center')

    # Shock event marker
    ax2.axvline(x=15, color='red', linestyle=':', linewidth=2, alpha=0.7)
    ax2.text(15.5, 0.58, 'SHOCK\n(enforcement\nbudget cut)',
             fontsize=9, color='red', va='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Annotations for phases
    ax2.annotate('Apparent\nstability', xy=(7, 0.50), fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    ax2.annotate('Discontinuous\ncollapse', xy=(17, 0.25), fontsize=10, ha='center',
                bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.8))

    ax2.annotate('Below θ →\nCascade begins', xy=(20, 0.28), xytext=(24, 0.40),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='red'),
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax2.set_xlabel('Time (years)', fontsize=12)
    ax2.set_ylabel('Trust Level (H₃)', fontsize=12)
    ax2.set_title('B. The "Coercion Cliff": Discontinuous Collapse', fontsize=14, fontweight='bold')
    ax2.set_xlim(0, 30)
    ax2.set_ylim(0, 0.65)
    ax2.legend(loc='upper right', fontsize=9)

    plt.tight_layout()
    fig.savefig(output_path / 'figure3_dark_trust_iceberg.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    fig.savefig(output_path / 'figure3_dark_trust_iceberg.pdf',
                bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_path / 'figure3_dark_trust_iceberg.png'}")


# =============================================================================
# INTERVENTION ROI CURVE (FIGURE 4)
# =============================================================================

def generate_intervention_roi_figure(output_path: Path):
    """
    Generate the Intervention ROI asymmetry visualization for Law 7.

    Shows the 10:1 vs 1:10 asymmetry across the threshold.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # H3 range
    H3 = np.linspace(0.15, 0.60, 200)
    theta = 0.375

    # ROI function
    def roi(h3, theta=0.375):
        if isinstance(h3, np.ndarray):
            result = np.zeros_like(h3)
            above = h3 > theta
            below = ~above
            result[above] = 1.0 + 5.0 * (h3[above] - theta)
            result[below] = np.exp(-10.0 * (theta - h3[below]))
            return result
        else:
            if h3 > theta:
                return 1.0 + 5.0 * (h3 - theta)
            else:
                return np.exp(-10.0 * (theta - h3))

    ROI = roi(H3)

    # Plot
    ax.fill_between(H3[H3 <= theta], 0, ROI[H3 <= theta], color='mistyrose', alpha=0.5)
    ax.fill_between(H3[H3 >= theta], 0, ROI[H3 >= theta], color='honeydew', alpha=0.5)

    ax.plot(H3, ROI, 'b-', linewidth=3)

    # Threshold line
    ax.axvline(x=theta, color='black', linestyle='--', linewidth=2)
    ax.axhline(y=1.0, color='gray', linestyle=':', linewidth=1, alpha=0.5)

    # Annotations
    ax.annotate('ROI ≈ 10:1\n(Healthy society)', xy=(0.55, 1.9), fontsize=12,
                ha='center', color='darkgreen',
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.8))

    ax.annotate('ROI ≈ 1:10\n(Failed state)', xy=(0.22, 0.25), fontsize=12,
                ha='center', color='darkred',
                bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.8))

    ax.annotate('Threshold\n(θ = 0.375)', xy=(theta, 1.0), xytext=(theta + 0.08, 1.8),
                fontsize=11, arrowprops=dict(arrowstyle='->', color='black'),
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Key examples
    examples = [
        (0.45, 'Marshall Plan\n(ROI ≈ 11:1)', 'darkgreen'),
        (0.20, 'Afghanistan\n(ROI ≈ -0.9:1)', 'darkred'),
        (0.42, 'USA 2024\n(ROI ≈ 1.5:1)', 'orange'),
    ]

    for h3, label, color in examples:
        r = roi(h3)
        ax.plot(h3, r, 'o', markersize=10, color=color, zorder=5)
        offset = (0.04, 0.3) if h3 > theta else (-0.04, -0.2)
        ax.annotate(label, xy=(h3, r), xytext=(h3 + offset[0], r + offset[1]),
                   fontsize=9, ha='center', color=color,
                   arrowprops=dict(arrowstyle='->', color=color, alpha=0.7))

    ax.set_xlabel('Trust Level (H₃)', fontsize=12)
    ax.set_ylabel('Intervention ROI', fontsize=12)
    ax.set_title('Law 7: The Intervention Window\n(10:1 ROI above threshold, 1:10 below)',
                fontsize=14, fontweight='bold')
    ax.set_xlim(0.15, 0.60)
    ax.set_ylim(0, 2.5)
    ax.grid(True, alpha=0.3)

    # Add formula
    formula_text = r"$ROI = \begin{cases} 1 + 5(H_3 - \theta) & H_3 > \theta \\ e^{-10(\theta - H_3)} & H_3 < \theta \end{cases}$"
    ax.text(0.95, 0.05, formula_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    fig.savefig(output_path / 'figure4_intervention_roi.png', dpi=300,
                bbox_inches='tight', facecolor='white')
    fig.savefig(output_path / 'figure4_intervention_roi.pdf',
                bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_path / 'figure4_intervention_roi.png'}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main(output_dir: str = 'outputs/figures'):
    """Generate all visualization figures."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("GENERATING COORDINATION COLLAPSE LAW VISUALIZATIONS")
    print("=" * 60)

    print("\n1. Generating Figure 2: Network Topology Comparison...")
    generate_topology_figure(output_path)

    print("\n2. Generating Figure 3: Dark Trust Iceberg...")
    generate_dark_trust_figure(output_path)

    print("\n3. Generating Figure 4: Intervention ROI Curve...")
    generate_intervention_roi_figure(output_path)

    print("\n" + "=" * 60)
    print("ALL FIGURES GENERATED")
    print("=" * 60)
    print(f"\nOutput directory: {output_path}")
    print("Files created:")
    for f in sorted(output_path.glob('figure*.png')):
        print(f"  - {f.name}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate topology visualizations")
    parser.add_argument('--output-dir', default='outputs/figures',
                        help='Output directory for figures')
    args = parser.parse_args()

    main(args.output_dir)
