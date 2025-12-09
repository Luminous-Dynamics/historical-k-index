#!/usr/bin/env python3
"""
Generate figures for Law 17 (AI Coordination Paradox) and related concepts.

Figures:
- Figure 15: AI Amplification Dynamics
- Figure 16: Three Scenarios Probability Distribution
- Figure 17: Earth Coordination Status Dashboard
- Figure 18: Great Filter Mechanism
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import os

# Set publication quality defaults
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})


def figure_15_ai_amplification(output_dir):
    """
    Figure 15: AI Amplification Dynamics
    Shows how AI amplifies both positive and negative coordination dynamics.
    """
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    t = np.linspace(0, 10, 100)
    theta = 0.375

    # Panel A: Natural dynamics (no AI)
    ax = axes[0]
    H3_natural = 0.50 - 0.015 * t  # Slow decline
    ax.plot(t, H3_natural, 'b-', linewidth=2, label='H₃ (natural)')
    ax.axhline(y=theta, color='r', linestyle='--', linewidth=1.5, label='θ = 0.375')
    ax.fill_between(t, 0, theta, alpha=0.2, color='red')
    ax.fill_between(t, theta, 1, alpha=0.1, color='green')
    ax.set_xlabel('Time (years)')
    ax.set_ylabel('H₃ (Trust Level)')
    ax.set_title('A) Natural Dynamics\n(No AI)')
    ax.set_ylim(0, 0.7)
    ax.set_xlim(0, 10)
    ax.legend(loc='upper right')
    ax.text(5, 0.15, 'Collapse Zone', ha='center', fontsize=9, color='darkred')
    ax.text(5, 0.55, 'Safe Zone', ha='center', fontsize=9, color='darkgreen')

    # Panel B: AI-accelerated collapse
    ax = axes[1]
    A_negative = 0.7  # Current AI impact
    H3_collapse = 0.50 - 0.015 * t * (1 + A_negative)  # Accelerated decline
    ax.plot(t, H3_natural, 'b--', linewidth=1.5, alpha=0.5, label='Natural')
    ax.plot(t, H3_collapse, 'r-', linewidth=2, label='With AI (A⁻ > A⁺)')
    ax.axhline(y=theta, color='r', linestyle='--', linewidth=1.5)
    ax.fill_between(t, 0, theta, alpha=0.2, color='red')
    ax.fill_between(t, theta, 1, alpha=0.1, color='green')

    # Mark threshold crossing
    cross_natural = (0.50 - theta) / 0.015
    cross_ai = (0.50 - theta) / (0.015 * (1 + A_negative))
    ax.axvline(x=cross_ai, color='darkred', linestyle=':', alpha=0.7)
    ax.annotate('Threshold\ncrossed', xy=(cross_ai, theta), xytext=(cross_ai + 1, theta + 0.1),
                fontsize=8, arrowprops=dict(arrowstyle='->', color='darkred'))

    ax.set_xlabel('Time (years)')
    ax.set_ylabel('H₃ (Trust Level)')
    ax.set_title('B) AI-Accelerated Collapse\n(A⁻ = 0.7, A⁺ = 0.3)')
    ax.set_ylim(0, 0.7)
    ax.set_xlim(0, 10)
    ax.legend(loc='upper right')

    # Panel C: AI-enhanced coordination
    ax = axes[2]
    A_positive = 0.8  # Positive AI impact (governance succeeds)
    H3_enhance = 0.50 + 0.01 * t * A_positive  # Growth with AI
    ax.plot(t, H3_natural, 'b--', linewidth=1.5, alpha=0.5, label='Natural')
    ax.plot(t, H3_enhance, 'g-', linewidth=2, label='With AI (A⁺ > A⁻)')
    ax.axhline(y=theta, color='r', linestyle='--', linewidth=1.5)
    ax.fill_between(t, 0, theta, alpha=0.2, color='red')
    ax.fill_between(t, theta, 1, alpha=0.1, color='green')
    ax.set_xlabel('Time (years)')
    ax.set_ylabel('H₃ (Trust Level)')
    ax.set_title('C) AI-Enhanced Coordination\n(Governance Succeeds)')
    ax.set_ylim(0, 0.7)
    ax.set_xlim(0, 10)
    ax.legend(loc='lower right')

    plt.tight_layout()

    for fmt in ['png', 'pdf']:
        plt.savefig(os.path.join(output_dir, f'figure_15_ai_amplification.{fmt}'))
    plt.close()
    print(f"Saved Figure 15 to {output_dir}/figure_15_ai_amplification.[png|pdf]")


def figure_16_three_scenarios(output_dir):
    """
    Figure 16: Three Scenarios for AI-Civilization Interaction
    Shows probability distributions and trajectories for each scenario.
    """
    fig = plt.figure(figsize=(12, 5))
    gs = GridSpec(1, 4, width_ratios=[1, 1, 1, 0.5])

    t = np.linspace(0, 30, 200)
    theta = 0.375

    # Scenario A: Collapse (40%)
    ax1 = fig.add_subplot(gs[0])
    H3_collapse = 0.45 - 0.025 * t + 0.002 * np.random.randn(len(t)).cumsum()
    H3_collapse = np.clip(H3_collapse, 0.1, 0.6)
    ax1.plot(t, H3_collapse, 'r-', linewidth=2)
    ax1.axhline(y=theta, color='gray', linestyle='--', linewidth=1)
    ax1.fill_between(t, 0, theta, alpha=0.15, color='red')
    ax1.set_xlabel('Time (years)')
    ax1.set_ylabel('H₃')
    ax1.set_title('Scenario A: Collapse\nP = 40%', color='darkred', fontweight='bold')
    ax1.set_ylim(0, 0.7)
    ax1.set_xlim(0, 30)
    ax1.text(15, 0.15, 'Fragmentation\n& Cascade', ha='center', fontsize=8, color='darkred')

    # Scenario B: Enhancement (25%)
    ax2 = fig.add_subplot(gs[1])
    H3_enhance = 0.45 + 0.008 * t + 0.001 * np.random.randn(len(t)).cumsum()
    H3_enhance = np.clip(H3_enhance, 0.35, 0.85)
    ax2.plot(t, H3_enhance, 'g-', linewidth=2)
    ax2.axhline(y=theta, color='gray', linestyle='--', linewidth=1)
    ax2.fill_between(t, theta, 1, alpha=0.1, color='green')
    ax2.set_xlabel('Time (years)')
    ax2.set_title('Scenario B: Enhancement\nP = 25%', color='darkgreen', fontweight='bold')
    ax2.set_ylim(0, 0.7)
    ax2.set_xlim(0, 30)
    ax2.text(20, 0.6, 'Transcendence', ha='center', fontsize=8, color='darkgreen')

    # Scenario C: Unstable (35%)
    ax3 = fig.add_subplot(gs[2])
    H3_unstable = 0.45 + 0.08 * np.sin(t/3) + 0.002 * np.random.randn(len(t)).cumsum()
    H3_unstable = np.clip(H3_unstable, 0.25, 0.6)
    ax3.plot(t, H3_unstable, color='orange', linewidth=2)
    ax3.axhline(y=theta, color='gray', linestyle='--', linewidth=1)
    ax3.fill_between(t, 0, theta, alpha=0.1, color='red')
    ax3.fill_between(t, theta, 1, alpha=0.05, color='green')
    ax3.set_xlabel('Time (years)')
    ax3.set_title('Scenario C: Unstable\nP = 35%', color='darkorange', fontweight='bold')
    ax3.set_ylim(0, 0.7)
    ax3.set_xlim(0, 30)
    ax3.text(15, 0.55, 'Repeated\nCrises', ha='center', fontsize=8, color='darkorange')

    # Probability bar chart
    ax4 = fig.add_subplot(gs[3])
    scenarios = ['A\nCollapse', 'B\nEnhance', 'C\nUnstable']
    probs = [0.40, 0.25, 0.35]
    colors = ['#d62728', '#2ca02c', '#ff7f0e']
    bars = ax4.barh(scenarios, probs, color=colors, edgecolor='black')
    ax4.set_xlim(0, 0.5)
    ax4.set_xlabel('Probability')
    ax4.set_title('Scenario\nProbabilities', fontsize=10)
    for bar, prob in zip(bars, probs):
        ax4.text(prob + 0.02, bar.get_y() + bar.get_height()/2,
                f'{int(prob*100)}%', va='center', fontsize=9)

    plt.tight_layout()

    for fmt in ['png', 'pdf']:
        plt.savefig(os.path.join(output_dir, f'figure_16_three_scenarios.{fmt}'))
    plt.close()
    print(f"Saved Figure 16 to {output_dir}/figure_16_three_scenarios.[png|pdf]")


def figure_17_earth_status(output_dir):
    """
    Figure 17: Earth Coordination Status Dashboard
    Shows current H₃, margin to threshold, and key metrics.
    """
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(2, 2, height_ratios=[1.2, 1])

    # Panel A: H₃ Gauge
    ax1 = fig.add_subplot(gs[0, 0], projection='polar')

    # Create gauge
    theta_vals = np.linspace(0, np.pi, 100)
    r = np.ones(100)

    # Color zones
    colors = plt.cm.RdYlGn(np.linspace(0, 1, 100))
    for i in range(len(theta_vals)-1):
        ax1.fill_between([theta_vals[i], theta_vals[i+1]], 0, 1,
                         color=colors[i], alpha=0.6)

    # Current H₃ position
    current_h3 = 0.45
    threshold = 0.375
    h3_angle = np.pi * current_h3
    threshold_angle = np.pi * threshold

    ax1.plot([h3_angle, h3_angle], [0, 1.1], 'k-', linewidth=3)
    ax1.plot([threshold_angle, threshold_angle], [0, 1.15], 'r--', linewidth=2)

    ax1.set_ylim(0, 1.2)
    ax1.set_theta_zero_location('W')
    ax1.set_theta_direction(-1)
    ax1.set_thetamin(0)
    ax1.set_thetamax(180)
    ax1.set_yticklabels([])
    ax1.set_xticklabels([])
    ax1.set_title('A) Global H₃ Status', fontsize=12, fontweight='bold', y=1.1)

    # Add labels
    ax1.text(np.pi * 0.45, 1.35, f'H₃ = {current_h3}', fontsize=14, fontweight='bold', ha='center')
    ax1.text(np.pi * threshold, 1.3, f'θ = {threshold}', fontsize=10, color='red', ha='center')
    ax1.text(0, 0.5, '0', fontsize=9, ha='center')
    ax1.text(np.pi, 0.5, '1', fontsize=9, ha='center')

    # Panel B: Margin Timeline
    ax2 = fig.add_subplot(gs[0, 1])
    years = np.arange(2000, 2030)
    h3_history = 0.55 - 0.005 * (years - 2000) + 0.01 * np.random.randn(len(years)).cumsum() * 0.1
    h3_history = np.clip(h3_history, 0.35, 0.60)

    ax2.fill_between(years, 0, threshold, alpha=0.2, color='red', label='Collapse Zone')
    ax2.fill_between(years, threshold, 1, alpha=0.1, color='green', label='Safe Zone')
    ax2.plot(years, h3_history, 'b-', linewidth=2, label='Global H₃')
    ax2.axhline(y=threshold, color='r', linestyle='--', linewidth=1.5)
    ax2.axvline(x=2025, color='gray', linestyle=':', alpha=0.7)
    ax2.text(2025.5, 0.55, 'NOW', fontsize=9, color='gray')

    # Margin annotation
    current_margin = current_h3 - threshold
    ax2.annotate('', xy=(2025, threshold), xytext=(2025, current_h3),
                arrowprops=dict(arrowstyle='<->', color='purple', lw=2))
    ax2.text(2026, (threshold + current_h3)/2, f'Margin\n= {current_margin:.2f}',
            fontsize=9, color='purple', va='center')

    ax2.set_xlabel('Year')
    ax2.set_ylabel('H₃')
    ax2.set_title('B) Historical Trend & Current Margin', fontsize=12, fontweight='bold')
    ax2.set_ylim(0.3, 0.65)
    ax2.set_xlim(2000, 2030)
    ax2.legend(loc='upper right', fontsize=8)

    # Panel C: Key Metrics
    ax3 = fig.add_subplot(gs[1, 0])
    metrics = ['H₃ (Trust)', 'Margin to θ', 'λ (Modernization)', 'R (Redundancy)', 'AI Net Effect']
    values = [0.45, 0.075, 21, 2.7, -0.4]
    colors = ['#2166ac', '#d73027', '#fdae61', '#4393c3', '#b2182b']

    # Normalize for display
    normalized = [0.45, 0.075/0.2, 21/30, 2.7/5, abs(-0.4)]

    bars = ax3.barh(metrics, normalized, color=colors, edgecolor='black')
    ax3.set_xlim(0, 1.2)
    ax3.set_xlabel('Relative Value')
    ax3.set_title('C) Key Coordination Metrics', fontsize=12, fontweight='bold')

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, values)):
        if i == 4:
            ax3.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{val:+.1f}', va='center', fontsize=9, color='darkred')
        elif i == 2:
            ax3.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{val:.0f}×', va='center', fontsize=9)
        else:
            ax3.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{val:.2f}', va='center', fontsize=9)

    # Panel D: Status Summary
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')

    status_text = """
    EARTH COORDINATION STATUS
    ══════════════════════════

    Status:     ⚠️  DANGER ZONE

    H₃:         0.45 (declining)
    Threshold:  0.375
    Margin:     0.075 (~7.5%)

    λ:          21× pre-industrial
    R:          2.7 (declining)
    AI Effect:  Net Negative

    Window:     1-3 YEARS

    ══════════════════════════
    All early warning signals
    are ELEVATED.

    Action required NOW.
    """

    ax4.text(0.5, 0.5, status_text, transform=ax4.transAxes, fontsize=10,
            verticalalignment='center', horizontalalignment='center',
            fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='orange', alpha=0.8))
    ax4.set_title('D) Status Summary', fontsize=12, fontweight='bold')

    plt.tight_layout()

    for fmt in ['png', 'pdf']:
        plt.savefig(os.path.join(output_dir, f'figure_17_earth_status.{fmt}'))
    plt.close()
    print(f"Saved Figure 17 to {output_dir}/figure_17_earth_status.[png|pdf]")


def figure_18_great_filter(output_dir):
    """
    Figure 18: The Great Filter Mechanism
    Shows how coordination collapse serves as the Great Filter.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Panel A: Filter probability chain
    ax1 = axes[0]

    stages = ['Life', 'Intelligence', 'Technology', 'Coordination\nThreshold', 'Type I', 'Type II']
    x_pos = np.arange(len(stages))

    # Cumulative survival probability
    probs = [1.0, 0.3, 0.15, 0.06, 0.03, 0.014]

    colors = ['#1f77b4', '#1f77b4', '#1f77b4', '#d62728', '#2ca02c', '#2ca02c']

    bars = ax1.bar(x_pos, probs, color=colors, edgecolor='black', alpha=0.8)

    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(stages, fontsize=9)
    ax1.set_ylabel('Cumulative Survival Probability')
    ax1.set_title('A) The Great Filter: Probability Chain', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 1.1)

    # Add probability labels
    for bar, prob in zip(bars, probs):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{prob*100:.1f}%', ha='center', fontsize=9, fontweight='bold')

    # Highlight the filter
    ax1.annotate('THE GREAT\nFILTER', xy=(3, 0.06), xytext=(3, 0.5),
                fontsize=11, color='darkred', fontweight='bold', ha='center',
                arrowprops=dict(arrowstyle='->', color='darkred', lw=2))

    # Add filter percentage
    ax1.text(3, 0.25, '~86%\nfilter\nout', ha='center', fontsize=10,
            color='darkred', style='italic')

    # Panel B: AI as Filter Mechanism
    ax2 = axes[1]

    # Create flow diagram
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')

    # Boxes
    boxes = [
        (1, 8, 'Technological\nCivilization'),
        (1, 5, 'Develops AI'),
        (1, 2, 'Coordination\nPhysics?'),
        (5, 7, 'AI Accelerates\nCollapse'),
        (5, 3, 'AI Enables\nCoordination'),
        (9, 5, 'THE\nFILTER')
    ]

    for x, y, text in boxes:
        color = 'lightblue'
        if 'Filter' in text.upper():
            color = 'lightcoral'
        elif 'Enables' in text:
            color = 'lightgreen'
        elif 'Accelerates' in text:
            color = 'lightyellow'

        bbox = dict(boxstyle='round,pad=0.3', facecolor=color, edgecolor='black')
        ax2.text(x, y, text, fontsize=9, ha='center', va='center', bbox=bbox)

    # Arrows
    arrows = [
        (1, 7.5, 0, -1.5),    # Tech -> AI
        (1, 4.5, 0, -1.5),    # AI -> Coord?
        (1.8, 2, 2.4, 4.5),   # No -> Collapse (diagonal)
        (1.8, 2.3, 2.4, 0.5), # Yes -> Enables (diagonal)
        (6, 7, 2, -1.5),      # Collapse -> Filter
        (6, 3.5, 2, 1),       # Enables -> Filter (bypass)
    ]

    for x, y, dx, dy in arrows:
        ax2.annotate('', xy=(x+dx, y+dy), xytext=(x, y),
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

    # Labels on paths
    ax2.text(2.5, 4.5, 'NO\n(85%)', fontsize=9, color='darkred', ha='center')
    ax2.text(2.5, 1.5, 'YES\n(15%)', fontsize=9, color='darkgreen', ha='center')
    ax2.text(7, 6.5, '40-60%', fontsize=8, color='darkred')
    ax2.text(7, 3.2, '25-40%', fontsize=8, color='darkgreen')

    ax2.set_title('B) AI as Great Filter Mechanism', fontsize=12, fontweight='bold')

    # Add key insight
    ax2.text(5, 0.5, 'τ_AI < τ_coordination → Most civilizations develop AI before understanding coordination physics',
            fontsize=8, ha='center', style='italic', wrap=True)

    plt.tight_layout()

    for fmt in ['png', 'pdf']:
        plt.savefig(os.path.join(output_dir, f'figure_18_great_filter.{fmt}'))
    plt.close()
    print(f"Saved Figure 18 to {output_dir}/figure_18_great_filter.[png|pdf]")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate Law 17 figures')
    parser.add_argument('--output-dir', default='papers/02-civilization-collapse/figures',
                       help='Output directory for figures')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("Generating Law 17 and AI-related figures...")
    print("=" * 60)

    np.random.seed(42)  # For reproducibility

    figure_15_ai_amplification(args.output_dir)
    figure_16_three_scenarios(args.output_dir)
    figure_17_earth_status(args.output_dir)
    figure_18_great_filter(args.output_dir)

    print("=" * 60)
    print(f"All figures saved to {args.output_dir}/")
    print("Formats: PNG (300 dpi) and PDF (vector)")


if __name__ == '__main__':
    main()
