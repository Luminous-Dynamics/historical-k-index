#!/usr/bin/env python3
"""
Figure Generation for Paper 6: Coordination Recovery Mechanisms
================================================================

Generates publication-quality figures illustrating recovery dynamics,
the Recovery Trap, Sequential Harmony Theorem, and historical recoveries.

Author: Tristan Stoltz
Date: December 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import seaborn as sns
import os
import argparse

# Set publication-quality defaults
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 300

# Color schemes
RECOVERY_COLORS = {
    'phoenix': '#2ecc71',      # Green - rapid recovery
    'gradual': '#3498db',      # Blue - steady ascent
    'partial': '#f39c12',      # Orange - incomplete
    'trapped': '#e74c3c',      # Red - stuck
    'collapse': '#c0392b',     # Dark red
    'threshold': '#9b59b6',    # Purple - Phoenix threshold
    'optimal': '#27ae60',      # Bright green
    'trust': '#1abc9c',        # Teal
    'governance': '#3498db',   # Blue
    'infrastructure': '#95a5a6' # Gray
}


def fig1_recovery_asymmetry(output_dir):
    """
    Figure 1: The Recovery Asymmetry Principle
    Shows collapse happening faster than recovery (3-7x)
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Time axis
    years = np.linspace(0, 100, 1000)

    # Collapse trajectory (fast)
    collapse_start = 20
    collapse_duration = 8
    collapse_years = years[(years >= collapse_start) & (years <= collapse_start + collapse_duration)]
    collapse_k = 0.65 - 0.40 * ((collapse_years - collapse_start) / collapse_duration) ** 0.7

    # Pre-collapse stable
    pre_collapse = np.ones_like(years[years < collapse_start]) * 0.65

    # Post-collapse low point
    low_point = 0.25

    # Recovery trajectory (slow)
    recovery_start = collapse_start + collapse_duration
    recovery_scenarios = {
        'Phoenix (1x)': {'multiplier': 1, 'color': RECOVERY_COLORS['phoenix'], 'linestyle': '--', 'alpha': 0.3},
        'Optimal (3x)': {'multiplier': 3, 'color': RECOVERY_COLORS['gradual'], 'linestyle': '-', 'alpha': 0.7},
        'Typical (5x)': {'multiplier': 5, 'color': RECOVERY_COLORS['partial'], 'linestyle': '-', 'alpha': 1.0},
        'Suboptimal (7x)': {'multiplier': 7, 'color': RECOVERY_COLORS['trapped'], 'linestyle': ':', 'alpha': 0.7},
    }

    # Plot collapse
    ax.plot(years[years < collapse_start], pre_collapse, 'k-', linewidth=2, label='Pre-collapse')
    ax.plot(collapse_years, collapse_k, color=RECOVERY_COLORS['collapse'], linewidth=3, label='Collapse (8 years)')

    # Plot recovery scenarios
    for name, params in recovery_scenarios.items():
        recovery_duration = collapse_duration * params['multiplier']
        recovery_years = years[(years >= recovery_start) & (years <= recovery_start + recovery_duration)]
        if len(recovery_years) > 0:
            recovery_k = low_point + 0.40 * ((recovery_years - recovery_start) / recovery_duration) ** 1.3
            ax.plot(recovery_years, recovery_k, color=params['color'],
                   linewidth=2.5, linestyle=params['linestyle'],
                   alpha=params['alpha'], label=f'{name}: {int(recovery_duration)} years')

    # Add horizontal lines for thresholds
    ax.axhline(y=0.65, color='gray', linestyle=':', alpha=0.5, label='Pre-collapse level')
    ax.axhline(y=0.25, color=RECOVERY_COLORS['threshold'], linestyle='--',
               alpha=0.7, label='Phoenix Threshold (K=0.25)')

    # Annotations
    ax.annotate('Collapse\n(Fast)', xy=(24, 0.45), fontsize=11, ha='center', color=RECOVERY_COLORS['collapse'])
    ax.annotate('Recovery\n(3-7x Slower)', xy=(60, 0.45), fontsize=11, ha='center', color=RECOVERY_COLORS['partial'])

    ax.set_xlabel('Years')
    ax.set_ylabel('K-Index (Coordination Capacity)')
    ax.set_title("THE RECOVERY ASYMMETRY PRINCIPLE\n\"Recovery takes 3-7× longer than collapse\"", fontweight='bold')
    ax.legend(loc='lower right', framealpha=0.9)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 0.8)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig1_recovery_asymmetry.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig1_recovery_asymmetry.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig1_recovery_asymmetry")


def fig2_sequential_harmony(output_dir):
    """
    Figure 2: Sequential Harmony Theorem
    Shows the required order of harmony restoration
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    harmonies = [
        ('H₃\nTrust', 0, '#1abc9c', 'Years 1-3'),
        ('H₁\nGovernance', 1, '#3498db', 'Years 2-7'),
        ('H₇\nInfrastructure', 2, '#95a5a6', 'Years 5-15'),
        ('H₂/H₄\nEcon/Social', 3, '#f39c12', 'Years 8-20'),
        ('H₅\nInnovation', 4, '#9b59b6', 'Years 12-25'),
        ('H₆\nCultural', 5, '#e74c3c', 'Years 15-30+'),
    ]

    # Create staggered bars showing overlap
    bar_height = 0.6

    for i, (name, idx, color, timeframe) in enumerate(harmonies):
        # Main bar
        ax.barh(idx, 1, height=bar_height, color=color, alpha=0.8, edgecolor='black')
        # Label inside bar
        ax.text(0.5, idx, name, ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        # Timeframe on right
        ax.text(1.1, idx, timeframe, ha='left', va='center', fontsize=10)

    # Add arrows showing dependencies
    arrow_style = dict(arrowstyle='->', color='black', lw=2)
    for i in range(len(harmonies) - 1):
        ax.annotate('', xy=(0.05, i + 0.35), xytext=(0.05, i + 0.65),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

    # Add violation penalty text
    ax.text(1.5, 2.5, 'SEQUENCE VIOLATION\nPENALTY:', fontsize=10, fontweight='bold', va='center')
    ax.text(1.5, 1.5, '• Skip H₃ → 50% efficiency loss\n• Skip H₁ → 35% efficiency loss\n• Skip H₇ → 20% efficiency loss',
           fontsize=9, va='center', family='monospace')

    ax.set_xlim(-0.1, 2.5)
    ax.set_ylim(-0.5, 5.5)
    ax.set_title("THE SEQUENTIAL HARMONY THEOREM\n\"Harmonies must be restored in order, or recovery fails\"",
                 fontweight='bold', fontsize=13)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig2_sequential_harmony.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig2_sequential_harmony.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig2_sequential_harmony")


def fig3_phoenix_threshold(output_dir):
    """
    Figure 3: The Phoenix Threshold
    Shows the minimum coordination floor for self-sustaining recovery
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    k_values = np.linspace(0.1, 0.7, 100)

    # Recovery rate as function of K
    # Below phoenix threshold: negative or zero
    # Above threshold: positive and increasing
    phoenix = 0.25

    recovery_rate = np.where(k_values < phoenix,
                             -0.02 * (phoenix - k_values),  # Below: negative
                             0.03 * (k_values - phoenix) ** 0.8)  # Above: positive

    # Plot
    ax.fill_between(k_values[k_values < phoenix], 0, recovery_rate[k_values < phoenix],
                   color=RECOVERY_COLORS['trapped'], alpha=0.3, label='Below Phoenix: Decay')
    ax.fill_between(k_values[k_values >= phoenix], 0, recovery_rate[k_values >= phoenix],
                   color=RECOVERY_COLORS['phoenix'], alpha=0.3, label='Above Phoenix: Recovery')
    ax.plot(k_values, recovery_rate, 'k-', linewidth=2)

    # Threshold line
    ax.axvline(x=phoenix, color=RECOVERY_COLORS['threshold'], linewidth=3,
               linestyle='--', label=f'Phoenix Threshold (K={phoenix})')
    ax.axhline(y=0, color='gray', linewidth=1)

    # Annotate regions
    ax.annotate('RECOVERY TRAP\nCannot self-recover\nRequires external help',
               xy=(0.17, -0.012), ha='center', fontsize=10,
               bbox=dict(boxstyle='round', facecolor=RECOVERY_COLORS['trapped'], alpha=0.3))
    ax.annotate('SELF-SUSTAINING\nRECOVERY ZONE',
               xy=(0.5, 0.02), ha='center', fontsize=10,
               bbox=dict(boxstyle='round', facecolor=RECOVERY_COLORS['phoenix'], alpha=0.3))

    ax.set_xlabel('K-Index (Current Coordination Level)')
    ax.set_ylabel('Recovery Rate (dK/dt)')
    ax.set_title("THE PHOENIX THRESHOLD\n\"Below K≈0.25, recovery requires external coordination injection\"", fontweight='bold')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.1, 0.7)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig3_phoenix_threshold.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig3_phoenix_threshold.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig3_phoenix_threshold")


def fig4_recovery_trap(output_dir):
    """
    Figure 4: The Recovery Trap Visualization
    Shows the chicken-and-egg paradox
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis('off')

    # Central circle - The Trap
    trap_circle = Circle((5, 4), 2.5, fill=True, facecolor='#e74c3c', alpha=0.2, edgecolor='#c0392b', linewidth=3)
    ax.add_patch(trap_circle)
    ax.text(5, 4, 'THE RECOVERY\nTRAP', ha='center', va='center', fontsize=14, fontweight='bold')

    # Four elements of the trap in a cycle
    elements = [
        (5, 7.5, 'Need coordination\nto coordinate', '#3498db'),
        (8.5, 4, 'Meta-coordination\nrequires coordination', '#27ae60'),
        (5, 0.5, 'External help needs\ncoordination to receive', '#f39c12'),
        (1.5, 4, 'Recovery nuclei\ncannot aggregate', '#9b59b6'),
    ]

    for x, y, text, color in elements:
        box = FancyBboxPatch((x-1.5, y-0.5), 3, 1, boxstyle="round,pad=0.1",
                            facecolor=color, alpha=0.7, edgecolor='black')
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    # Arrows connecting elements (circular)
    for i in range(4):
        x1, y1, _, _ = elements[i]
        x2, y2, _, _ = elements[(i+1) % 4]
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=2,
                                  connectionstyle='arc3,rad=0.3'))

    # Title
    ax.text(5, 8.5, "THE RECOVERY TRAP PARADOX\n\"You cannot pull yourself up by your bootstraps if you don't have boots\"",
           ha='center', fontsize=12, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig4_recovery_trap.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig4_recovery_trap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig4_recovery_trap")


def fig5_escape_mechanisms(output_dir):
    """
    Figure 5: Five Mechanisms to Escape the Recovery Trap
    """
    fig, axes = plt.subplots(1, 5, figsize=(15, 5))

    mechanisms = [
        ('External\nInjection', 'Marshall Plan\nModel', '#2ecc71'),
        ('Nuclei\nAggregation', 'Bottom-Up\nPath', '#3498db'),
        ('Diaspora\nNetworks', 'External-Internal\nBridge', '#9b59b6'),
        ('Symbolic\nReset', 'Clean Slate\nMechanism', '#f39c12'),
        ('Tech-Mediated\nCoordination', 'Digital\nBootstrap', '#1abc9c'),
    ]

    for ax, (title, subtitle, color) in zip(axes, mechanisms):
        # Draw upward arrow
        ax.arrow(0.5, 0.2, 0, 0.5, head_width=0.15, head_length=0.08,
                fc=color, ec='black', linewidth=2)

        # Labels
        ax.text(0.5, 0.85, title, ha='center', va='center', fontsize=11, fontweight='bold')
        ax.text(0.5, 0.1, subtitle, ha='center', va='top', fontsize=9, style='italic')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    fig.suptitle("FIVE MECHANISMS TO ESCAPE THE RECOVERY TRAP", fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig5_escape_mechanisms.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig5_escape_mechanisms.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig5_escape_mechanisms")


def fig6_sixty_forty_rule(output_dir):
    """
    Figure 6: The 60:40 Investment Rule
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Current vs Optimal allocation
    categories = ['Trust\nInfrastructure', 'Governance\nSupport', 'Physical\nInfrastructure',
                 'Economic\nDevelopment', 'Security']
    current = [8, 12, 55, 20, 5]
    optimal = [35, 25, 25, 12, 3]

    x = np.arange(len(categories))
    width = 0.35

    bars1 = ax1.bar(x - width/2, current, width, label='Current Practice', color=RECOVERY_COLORS['trapped'], alpha=0.7)
    bars2 = ax1.bar(x + width/2, optimal, width, label='Optimal (60:40)', color=RECOVERY_COLORS['phoenix'], alpha=0.7)

    ax1.set_ylabel('Percentage of Recovery Budget')
    ax1.set_title('Current vs. Optimal Investment Allocation', fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=9)
    ax1.legend()
    ax1.axhline(y=35, color='gray', linestyle=':', alpha=0.5)

    # Right: 60:40 pie chart
    sizes = [60, 40]
    labels = ['Trust Infrastructure\n(60%)', 'Institutional Support\n(40%)']
    colors = [RECOVERY_COLORS['trust'], RECOVERY_COLORS['governance']]
    explode = (0.05, 0)

    ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='',
           shadow=True, startangle=90)
    ax2.set_title('THE 60:40 RULE\nOptimal Recovery Allocation', fontweight='bold')

    fig.suptitle("RECOVERY INVESTMENT PORTFOLIO", fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig6_sixty_forty_rule.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig6_sixty_forty_rule.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig6_sixty_forty_rule")


def fig7_recovery_taxonomy(output_dir):
    """
    Figure 7: The Four Recovery Types
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    years = np.linspace(0, 50, 500)

    # Different recovery trajectories
    trajectories = {
        'Type I: Phoenix (17%)': {
            'k': lambda t: 0.25 + 0.40 * (1 - np.exp(-t/10)),
            'color': RECOVERY_COLORS['phoenix'],
            'final': 0.65
        },
        'Type II: Gradual (35%)': {
            'k': lambda t: 0.25 + 0.35 * (1 - np.exp(-t/20)),
            'color': RECOVERY_COLORS['gradual'],
            'final': 0.58
        },
        'Type III: Partial (31%)': {
            'k': lambda t: 0.25 + 0.20 * (1 - np.exp(-t/15)),
            'color': RECOVERY_COLORS['partial'],
            'final': 0.45
        },
        'Type IV: Trapped (17%)': {
            'k': lambda t: 0.25 + 0.05 * np.sin(t/5) + 0.02 * t / 50,
            'color': RECOVERY_COLORS['trapped'],
            'final': 0.28
        },
    }

    for name, params in trajectories.items():
        k_values = params['k'](years)
        ax.plot(years, k_values, color=params['color'], linewidth=2.5, label=name)

    # Thresholds
    ax.axhline(y=0.65, color='green', linestyle=':', alpha=0.5, label='Pre-collapse level')
    ax.axhline(y=0.25, color=RECOVERY_COLORS['threshold'], linestyle='--',
               alpha=0.7, label='Phoenix Threshold')

    ax.set_xlabel('Years Since Collapse')
    ax.set_ylabel('K-Index')
    ax.set_title("THE RECOVERY TAXONOMY\nFour Distinct Patterns of Coordination Regeneration", fontweight='bold')
    ax.legend(loc='right', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 50)
    ax.set_ylim(0.15, 0.75)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig7_recovery_taxonomy.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig7_recovery_taxonomy.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig7_recovery_taxonomy")


def fig8_historical_recoveries(output_dir):
    """
    Figure 8: Historical Recovery Case Studies
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # Historical recovery data
    cases = {
        'Germany (1945-1970)': {'type': 'Phoenix', 'duration': 25, 'k_start': 0.22, 'k_end': 0.68, 'color': RECOVERY_COLORS['phoenix']},
        'Japan (1945-1970)': {'type': 'Phoenix', 'duration': 25, 'k_start': 0.20, 'k_end': 0.70, 'color': RECOVERY_COLORS['phoenix']},
        'Spain (1975-2005)': {'type': 'Gradual', 'duration': 30, 'k_start': 0.38, 'k_end': 0.62, 'color': RECOVERY_COLORS['gradual']},
        'S. Korea (1953-1990)': {'type': 'Gradual', 'duration': 37, 'k_start': 0.28, 'k_end': 0.65, 'color': RECOVERY_COLORS['gradual']},
        'Rwanda (1994-2024)': {'type': 'Phoenix', 'duration': 30, 'k_start': 0.15, 'k_end': 0.52, 'color': RECOVERY_COLORS['phoenix']},
        'Colombia (ongoing)': {'type': 'Partial', 'duration': 35, 'k_start': 0.35, 'k_end': 0.48, 'color': RECOVERY_COLORS['partial']},
        'S. Africa (1994-)': {'type': 'Partial', 'duration': 30, 'k_start': 0.32, 'k_end': 0.46, 'color': RECOVERY_COLORS['partial']},
        'Haiti (ongoing)': {'type': 'Trapped', 'duration': 40, 'k_start': 0.22, 'k_end': 0.24, 'color': RECOVERY_COLORS['trapped']},
    }

    y_positions = np.arange(len(cases))

    for i, (name, data) in enumerate(cases.items()):
        # Arrow from start to end
        ax.arrow(data['k_start'], i, data['k_end'] - data['k_start'] - 0.02, 0,
                head_width=0.25, head_length=0.02, fc=data['color'], ec='black', linewidth=1.5)

        # Labels
        ax.text(data['k_start'] - 0.02, i, f"{data['k_start']:.2f}", ha='right', va='center', fontsize=9)
        ax.text(data['k_end'] + 0.02, i, f"{data['k_end']:.2f}", ha='left', va='center', fontsize=9)
        ax.text(0.02, i, name, ha='left', va='center', fontsize=10)
        ax.text(0.78, i, f"{data['type']}\n({data['duration']} yrs)", ha='left', va='center', fontsize=8)

    # Phoenix threshold
    ax.axvline(x=0.25, color=RECOVERY_COLORS['threshold'], linestyle='--', linewidth=2, alpha=0.7)
    ax.text(0.25, -0.8, 'Phoenix\nThreshold', ha='center', va='top', fontsize=9, color=RECOVERY_COLORS['threshold'])

    ax.set_xlim(0, 0.95)
    ax.set_ylim(-1.5, len(cases) - 0.5)
    ax.set_xlabel('K-Index')
    ax.set_title("HISTORICAL RECOVERY TRAJECTORIES\n23 Case Studies of Coordination Regeneration", fontweight='bold')
    ax.set_yticks([])
    ax.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig8_historical_recoveries.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig8_historical_recoveries.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig8_historical_recoveries")


def main():
    parser = argparse.ArgumentParser(description='Generate Paper 6 figures')
    parser.add_argument('--output-dir', default='figures', help='Output directory')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 60)
    print("GENERATING PAPER 6 FIGURES: Coordination Recovery Mechanisms")
    print("=" * 60)

    fig1_recovery_asymmetry(args.output_dir)
    fig2_sequential_harmony(args.output_dir)
    fig3_phoenix_threshold(args.output_dir)
    fig4_recovery_trap(args.output_dir)
    fig5_escape_mechanisms(args.output_dir)
    fig6_sixty_forty_rule(args.output_dir)
    fig7_recovery_taxonomy(args.output_dir)
    fig8_historical_recoveries(args.output_dir)

    print("=" * 60)
    print(f"All figures generated in: {args.output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
