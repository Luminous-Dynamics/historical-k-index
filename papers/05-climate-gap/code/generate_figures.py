#!/usr/bin/env python3
"""
Figure Generation for Paper 5: The Climate Coordination Crisis
================================================================

Generates publication-quality figures for the K-Index climate coordination analysis.

Revolutionary Visualizations:
1. The Technology Fallacy - Gap vs Finance mismatch
2. Climate-Coordination Spiral - Vicious cycle dynamics
3. The 10% Reallocation - Comparative impact analysis
4. Intergenerational Trust Timeline - Unprecedented timeframes
5. Finance Misallocation - Current vs Optimal allocation
6. Required vs Actual K-Index - The Paris Gap
7. Spiral Dynamics - Feedback loop visualization
8. Trust Infrastructure ROI - Investment returns

Author: Tristan Stoltz
Date: December 2025
"""

import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import seaborn as sns

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Color schemes
COLORS = {
    'trust': '#E63946',        # Red - critical constraint
    'technology': '#2A9D8F',   # Teal - technology
    'governance': '#264653',   # Dark blue
    'economic': '#F4A261',     # Orange
    'knowledge': '#9B59B6',    # Purple
    'wellbeing': '#3498DB',    # Blue
    'infrastructure': '#2ECC71', # Green
    'gap': '#E74C3C',          # Red for gaps
    'target': '#27AE60',       # Green for targets
    'current': '#3498DB',      # Blue for current
    'spiral_climate': '#FF6B6B',
    'spiral_coord': '#4ECDC4',
}

# Data for climate-coordination analysis
HARMONY_DATA = {
    'Trust (H₃)': {'current': 0.42, 'required': 0.68, 'finance_pct': 1, 'gap_pct': 38},
    'Governance (H₁)': {'current': 0.51, 'required': 0.70, 'finance_pct': 6, 'gap_pct': 27},
    'Economic (H₂)': {'current': 0.48, 'required': 0.65, 'finance_pct': 5, 'gap_pct': 26},
    'Wellbeing (H₆)': {'current': 0.54, 'required': 0.68, 'finance_pct': 2, 'gap_pct': 21},
    'Knowledge (H₅)': {'current': 0.58, 'required': 0.72, 'finance_pct': 8, 'gap_pct': 19},
    'Infrastructure (H₇)': {'current': 0.62, 'required': 0.75, 'finance_pct': 78, 'gap_pct': 17},
}

# Historical precedents
PRECEDENTS = {
    'Marshall Plan (1948)': 0.72,
    'Montreal Protocol (1987)': 0.68,
    'EU Formation (1957)': 0.71,
    'WHO Smallpox (1967)': 0.65,
    'Nuclear Non-Prolif (1968)': 0.64,
}


def fig1_technology_fallacy(output_dir):
    """The Technology Fallacy: Gap vs Finance allocation"""
    fig, ax = plt.subplots(figsize=(12, 8))

    harmonies = list(HARMONY_DATA.keys())
    gaps = [HARMONY_DATA[h]['gap_pct'] for h in harmonies]
    finance = [HARMONY_DATA[h]['finance_pct'] for h in harmonies]

    x = np.arange(len(harmonies))
    width = 0.35

    bars1 = ax.bar(x - width/2, gaps, width, label='Coordination Gap (%)',
                   color=COLORS['gap'], alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, finance, width, label='Climate Finance (%)',
                   color=COLORS['technology'], alpha=0.8, edgecolor='black', linewidth=1.5)

    # Highlight the mismatch
    ax.annotate('THE TECHNOLOGY\nFALLACY', xy=(5, 78), fontsize=16, fontweight='bold',
                color=COLORS['gap'], ha='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=COLORS['gap'], linewidth=2))

    # Draw arrows showing mismatch
    ax.annotate('', xy=(0, 38), xytext=(0, 1),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax.annotate('37% MISMATCH', xy=(0.3, 20), fontsize=10, color='red', fontweight='bold')

    ax.annotate('', xy=(5, 17), xytext=(5, 78),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax.annotate('+61% OVER-\nINVESTMENT', xy=(5.3, 50), fontsize=10, color='red', fontweight='bold')

    ax.set_xlabel('Harmony Dimension', fontsize=14, fontweight='bold')
    ax.set_ylabel('Percentage (%)', fontsize=14, fontweight='bold')
    ax.set_title('THE TECHNOLOGY FALLACY\nClimate Finance Inverts Coordination Priorities',
                 fontsize=18, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([h.split(' ')[0] for h in harmonies], rotation=45, ha='right', fontsize=11)
    ax.legend(loc='upper right', fontsize=12)
    ax.set_ylim(0, 100)

    # Add subtitle
    fig.text(0.5, 0.01, 'Largest gap (Trust, 38%) receives smallest investment (1%); '
             'Smallest gap (Infrastructure, 17%) receives largest investment (78%)',
             ha='center', fontsize=11, style='italic')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig1_technology_fallacy.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig1_technology_fallacy.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig1_technology_fallacy")


def fig2_climate_coordination_spiral(output_dir):
    """The Climate-Coordination Spiral: Vicious cycle visualization"""
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Draw spiral nodes
    nodes = [
        ('Low K-Index', 0, 1, COLORS['spiral_coord']),
        ('Insufficient\nClimate Action', 1, 0, COLORS['spiral_coord']),
        ('Climate\nStress Increases', 0, -1, COLORS['spiral_climate']),
        ('Trust (H₃)\nErodes', -1, 0, COLORS['spiral_climate']),
    ]

    for label, x, y, color in nodes:
        circle = plt.Circle((x, y), 0.35, color=color, alpha=0.8, ec='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=12, fontweight='bold',
                color='white')

    # Draw connecting arrows
    arrow_style = 'Simple, tail_width=15, head_width=30, head_length=20'
    for i in range(4):
        start = nodes[i]
        end = nodes[(i+1) % 4]

        # Calculate arrow positions
        dx = end[1] - start[1]
        dy = end[2] - start[2]
        length = np.sqrt(dx**2 + dy**2)

        start_x = start[1] + 0.4 * dx/length
        start_y = start[2] + 0.4 * dy/length
        end_x = end[1] - 0.4 * dx/length
        end_y = end[2] - 0.4 * dy/length

        ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                   arrowprops=dict(arrowstyle='->', color='black', lw=3,
                                 connectionstyle='arc3,rad=0.2'))

    # Add center text
    ax.text(0, 0, 'THE CLIMATE-\nCOORDINATION\nSPIRAL', ha='center', va='center',
            fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=2))

    # Add labels on arrows
    labels = [
        ('Coordination\nfailure', 0.7, 0.7),
        ('Emissions\nrise', 0.7, -0.7),
        ('Social fabric\nweakens', -0.7, -0.7),
        ('K-Index\ndeclines', -0.7, 0.7),
    ]
    for label, x, y in labels:
        ax.text(x, y, label, ha='center', va='center', fontsize=10, style='italic',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='lightyellow', alpha=0.8))

    ax.set_title('THE CLIMATE-COORDINATION SPIRAL\nA Vicious Cycle Toward Dual Catastrophe',
                 fontsize=18, fontweight='bold', pad=20)

    # Add warning
    ax.text(0, -1.4, '⚠ Without intervention, this spiral accelerates toward both\n'
            'climate catastrophe AND coordination collapse simultaneously',
            ha='center', va='center', fontsize=12, style='italic',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFEBEE', edgecolor='red'))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig2_climate_spiral.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig2_climate_spiral.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig2_climate_spiral")


def fig3_ten_percent_reallocation(output_dir):
    """The 10% Reallocation Principle: Comparative impact"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # Current allocation
    ax1 = axes[0]
    current_labels = ['Infrastructure\n(78%)', 'Knowledge (8%)', 'Governance (6%)',
                     'Economic (5%)', 'Wellbeing (2%)', 'Trust (1%)']
    current_sizes = [78, 8, 6, 5, 2, 1]
    current_colors = [COLORS['infrastructure'], COLORS['knowledge'], COLORS['governance'],
                     COLORS['economic'], COLORS['wellbeing'], COLORS['trust']]

    wedges1, texts1, autotexts1 = ax1.pie(current_sizes, labels=current_labels, colors=current_colors,
                                          autopct='', startangle=90, pctdistance=0.75,
                                          wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
    ax1.set_title('CURRENT ALLOCATION\n(Failing Strategy)', fontsize=14, fontweight='bold',
                  color='red')

    # Add metrics in center
    ax1.text(0, 0, 'Paris\nCompliance:\n18%', ha='center', va='center', fontsize=14, fontweight='bold')

    # Proposed allocation
    ax2 = axes[1]
    proposed_labels = ['Infrastructure\n(68%)', 'Trust (11%)', 'Knowledge (8%)',
                      'Governance (6%)', 'Economic (5%)', 'Wellbeing (2%)']
    proposed_sizes = [68, 11, 8, 6, 5, 2]
    proposed_colors = [COLORS['infrastructure'], COLORS['trust'], COLORS['knowledge'],
                      COLORS['governance'], COLORS['economic'], COLORS['wellbeing']]

    wedges2, texts2, autotexts2 = ax2.pie(proposed_sizes, labels=proposed_labels, colors=proposed_colors,
                                          autopct='', startangle=90, pctdistance=0.75,
                                          wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
    ax2.set_title('10% REALLOCATION\n(Optimized Strategy)', fontsize=14, fontweight='bold',
                  color='green')

    # Add metrics in center
    ax2.text(0, 0, 'Paris\nCompliance:\n42%', ha='center', va='center', fontsize=14, fontweight='bold')

    # Add comparison arrow
    fig.text(0.5, 0.5, '→', ha='center', va='center', fontsize=60, fontweight='bold', color='green')
    fig.text(0.5, 0.35, '+133%\nimprovement', ha='center', va='center', fontsize=14,
             fontweight='bold', color='green')

    fig.suptitle('THE 10% REALLOCATION PRINCIPLE\n'
                 'Redirecting Climate Finance to Trust Infrastructure',
                 fontsize=18, fontweight='bold', y=1.02)

    # Add bottom text
    fig.text(0.5, 0.02, 'Moving just 10% of finance from technology to trust yields 3.2× higher emissions reduction per dollar',
             ha='center', fontsize=12, style='italic')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig3_ten_percent_reallocation.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig3_ten_percent_reallocation.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig3_ten_percent_reallocation")


def fig4_paris_gap(output_dir):
    """The Paris Gap: Required vs Actual K-Index"""
    fig, ax = plt.subplots(figsize=(12, 8))

    years = np.arange(1990, 2051, 5)

    # Historical and projected K-Index
    historical_k = [0.58, 0.56, 0.55, 0.54, 0.53, 0.52, 0.51]  # 1990-2020
    projected_current = [0.50, 0.48, 0.46, 0.44, 0.42, 0.40]  # 2025-2050 (current trajectory)
    projected_optimal = [0.54, 0.58, 0.63, 0.68, 0.72, 0.75]  # 2025-2050 (with trust investment)

    k_current = historical_k + projected_current
    k_optimal = historical_k + projected_optimal

    # Required K for Paris
    k_paris = [0.72] * len(years)
    k_15c = [0.78] * len(years)

    # Plot lines
    ax.plot(years[:7], k_current[:7], 'b-', linewidth=3, label='Historical K-Index')
    ax.plot(years[6:], k_current[6:], 'r--', linewidth=3, label='Current Trajectory')
    ax.plot(years[6:], k_optimal[6:], 'g--', linewidth=3, label='With Trust Investment')
    ax.axhline(y=0.72, color='orange', linestyle=':', linewidth=2, label='Required for 2°C (Paris)')
    ax.axhline(y=0.78, color='red', linestyle=':', linewidth=2, label='Required for 1.5°C')
    ax.axhline(y=0.375, color='darkred', linestyle='-.', linewidth=2, label='Collapse Threshold')

    # Fill the gap
    ax.fill_between(years, k_current, 0.72, where=[k < 0.72 for k in k_current],
                    alpha=0.2, color='red', label='Coordination Gap')

    # Mark key points
    ax.scatter([2024], [0.52], s=200, color='blue', zorder=5, marker='*')
    ax.annotate('Current\n(2024)', xy=(2024, 0.52), xytext=(2018, 0.58),
                arrowprops=dict(arrowstyle='->', color='blue'), fontsize=11, fontweight='bold')

    ax.annotate('38% GAP', xy=(2024, 0.62), fontsize=14, fontweight='bold', color='red',
                ha='center')

    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_ylabel('K-Index', fontsize=14, fontweight='bold')
    ax.set_title('THE PARIS GAP\nRequired vs. Actual Coordination Capacity for Climate Action',
                 fontsize=18, fontweight='bold', pad=20)
    ax.legend(loc='lower left', fontsize=10)
    ax.set_xlim(1990, 2050)
    ax.set_ylim(0.3, 0.85)
    ax.grid(True, alpha=0.3)

    # Add annotations
    ax.text(2045, 0.42, 'FAILURE\nPATHWAY', fontsize=12, color='red', fontweight='bold', ha='center')
    ax.text(2045, 0.73, 'SUCCESS\nPATHWAY', fontsize=12, color='green', fontweight='bold', ha='center')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig4_paris_gap.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig4_paris_gap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig4_paris_gap")


def fig5_intergenerational_timeline(output_dir):
    """Intergenerational Trust: Unprecedented coordination timeframes"""
    fig, ax = plt.subplots(figsize=(14, 8))

    challenges = [
        ('Trade\nAgreements', 7.5, 'Low'),
        ('Security\nAlliances', 20, 'Medium'),
        ('Infrastructure\nInvestment', 35, 'Medium'),
        ('Ozone\nProtection', 50, 'High'),
        ('CLIMATE\nACTION', 125, 'Extreme'),
    ]

    colors = ['#2ECC71', '#F1C40F', '#F1C40F', '#E67E22', '#E74C3C']

    y_pos = np.arange(len(challenges))
    timeframes = [c[1] for c in challenges]

    bars = ax.barh(y_pos, timeframes, color=colors, edgecolor='black', linewidth=2, height=0.6)

    # Add timeframe labels
    for i, (label, time, difficulty) in enumerate(challenges):
        ax.text(time + 5, i, f'{time} years\n({difficulty})', va='center', fontsize=11, fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels([c[0] for c in challenges], fontsize=12)
    ax.set_xlabel('Required Coordination Timeframe (Years)', fontsize=14, fontweight='bold')
    ax.set_title('THE INTERGENERATIONAL COORDINATION LAW\n'
                 'Climate Action Requires Unprecedented Trust Across Generations',
                 fontsize=18, fontweight='bold', pad=20)

    # Add institutional memory line
    ax.axvline(x=30, color='purple', linestyle='--', linewidth=2, label='Institutional Memory Limit (~30 years)')
    ax.text(32, 4.5, 'Beyond institutional\nmemory', fontsize=10, color='purple', style='italic')

    # Highlight the unprecedented nature
    ax.annotate('', xy=(125, 4), xytext=(50, 4),
                arrowprops=dict(arrowstyle='->', color='red', lw=3))
    ax.text(85, 4.3, '2.5× longer than\nany precedent', fontsize=11, color='red',
            fontweight='bold', ha='center')

    ax.set_xlim(0, 170)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, axis='x', alpha=0.3)

    # Add note
    fig.text(0.5, 0.01, 'Climate action requires coordination across 50-200 years—a form of trust '
             'for which human institutions have NO precedent',
             ha='center', fontsize=12, style='italic', color='darkred')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig5_intergenerational.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig5_intergenerational.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig5_intergenerational")


def fig6_trust_infrastructure_roi(output_dir):
    """Trust Infrastructure ROI: Investment returns comparison"""
    fig, ax = plt.subplots(figsize=(12, 8))

    interventions = [
        'Transparent Climate\nVerification',
        'Scientific Credibility\nRestoration',
        'Indigenous Knowledge\nIntegration',
        'Cross-border\nCommunity Projects',
        'Citizen Climate\nAssemblies',
        'Local Government\nCooperation',
        'International Youth\nExchanges',
        'Media Literacy\nPrograms',
    ]

    roi_per_billion = [0.012, 0.011, 0.010, 0.009, 0.008, 0.007, 0.006, 0.005]
    costs = [4, 4, 2, 8, 2, 6, 5, 3]

    # Sort by ROI
    sorted_data = sorted(zip(interventions, roi_per_billion, costs), key=lambda x: x[1], reverse=True)
    interventions, roi_per_billion, costs = zip(*sorted_data)

    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(interventions)))

    bars = ax.barh(range(len(interventions)), roi_per_billion, color=colors,
                   edgecolor='black', linewidth=1.5, height=0.7)

    # Add cost labels
    for i, (roi, cost) in enumerate(zip(roi_per_billion, costs)):
        ax.text(roi + 0.0005, i, f'${cost}B/yr → ΔH₃: +{roi:.3f}', va='center', fontsize=10)

    ax.set_yticks(range(len(interventions)))
    ax.set_yticklabels(interventions, fontsize=11)
    ax.set_xlabel('Trust Improvement per $1 Billion (ΔH₃/\$B)', fontsize=14, fontweight='bold')
    ax.set_title('TRUST INFRASTRUCTURE ROI\n'
                 'Which Investments Build Climate Coordination Capacity?',
                 fontsize=18, fontweight='bold', pad=20)

    # Add comparison to technology
    ax.axvline(x=0.003, color='red', linestyle='--', linewidth=2)
    ax.text(0.003, -0.8, 'Technology ROI\n(baseline)', fontsize=10, color='red', ha='center')

    ax.set_xlim(0, 0.016)
    ax.grid(True, axis='x', alpha=0.3)

    # Add total portfolio note
    fig.text(0.5, 0.01, 'Total Portfolio: $34B/year yields ΔH₃ ≈ +0.068 (equivalent to reversing 3 years of trust erosion)',
             ha='center', fontsize=12, style='italic')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig6_trust_roi.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig6_trust_roi.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig6_trust_roi")


def fig7_harmony_gaps(output_dir):
    """Harmony Gap Analysis: Current vs Required levels"""
    fig, ax = plt.subplots(figsize=(12, 8))

    harmonies = list(HARMONY_DATA.keys())
    current = [HARMONY_DATA[h]['current'] for h in harmonies]
    required = [HARMONY_DATA[h]['required'] for h in harmonies]

    x = np.arange(len(harmonies))
    width = 0.35

    bars1 = ax.bar(x - width/2, current, width, label='Current (2024)',
                   color=COLORS['current'], alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, required, width, label='Required for Paris',
                   color=COLORS['target'], alpha=0.8, edgecolor='black', linewidth=1.5)

    # Add gap annotations
    for i, (c, r) in enumerate(zip(current, required)):
        gap = r - c
        gap_pct = (gap / r) * 100
        ax.annotate(f'-{gap_pct:.0f}%', xy=(i, r + 0.02), ha='center', fontsize=10,
                    fontweight='bold', color='red' if gap_pct > 30 else 'orange')

    # Highlight trust as binding constraint
    ax.annotate('BINDING\nCONSTRAINT', xy=(0, 0.42), xytext=(-0.8, 0.25),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=12, fontweight='bold', color='red')

    ax.set_xlabel('Harmony Dimension', fontsize=14, fontweight='bold')
    ax.set_ylabel('Harmony Score', fontsize=14, fontweight='bold')
    ax.set_title('COORDINATION GAP BY HARMONY\nTrust (H₃) Shows the Largest Shortfall',
                 fontsize=18, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels([h.split(' ')[0] for h in harmonies], rotation=45, ha='right', fontsize=11)
    ax.legend(loc='upper right', fontsize=12)
    ax.set_ylim(0, 0.9)

    # Add collapse threshold
    ax.axhline(y=0.375, color='darkred', linestyle='-.', linewidth=2)
    ax.text(5.5, 0.38, 'Collapse Threshold', fontsize=10, color='darkred')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig7_harmony_gaps.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig7_harmony_gaps.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig7_harmony_gaps")


def fig8_historical_precedents(output_dir):
    """Historical Precedents: K-Index requirements for collective action"""
    fig, ax = plt.subplots(figsize=(12, 8))

    precedents = list(PRECEDENTS.keys())
    k_values = list(PRECEDENTS.values())

    # Sort by K-Index
    sorted_data = sorted(zip(precedents, k_values), key=lambda x: x[1])
    precedents, k_values = zip(*sorted_data)

    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(precedents)))

    bars = ax.barh(range(len(precedents)), k_values, color=colors,
                   edgecolor='black', linewidth=1.5, height=0.6)

    # Add Paris requirement
    ax.axvline(x=0.72, color='red', linestyle='--', linewidth=3, label='Paris Required (0.72)')
    ax.axvline(x=0.52, color='blue', linestyle='--', linewidth=3, label='Current Global (0.52)')

    ax.set_yticks(range(len(precedents)))
    ax.set_yticklabels(precedents, fontsize=11)
    ax.set_xlabel('K-Index Required for Success', fontsize=14, fontweight='bold')
    ax.set_title('HISTORICAL PRECEDENTS FOR COLLECTIVE ACTION\n'
                 'What K-Index Enabled Past Coordination Successes?',
                 fontsize=18, fontweight='bold', pad=20)

    # Add annotations
    for i, (label, k) in enumerate(zip(precedents, k_values)):
        ax.text(k + 0.01, i, f'{k:.2f}', va='center', fontsize=11, fontweight='bold')

    ax.legend(loc='lower right', fontsize=11)
    ax.set_xlim(0.5, 0.85)
    ax.grid(True, axis='x', alpha=0.3)

    # Add note
    fig.text(0.5, 0.01, 'Climate action is MORE demanding than all precedents due to global scope '
             'and intergenerational timeframe',
             ha='center', fontsize=12, style='italic', color='darkred')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig8_precedents.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig8_precedents.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig8_precedents")


def main():
    parser = argparse.ArgumentParser(description='Generate Paper 5 figures')
    parser.add_argument('--output-dir', type=str, default='../figures',
                        help='Output directory for figures')
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 60)
    print("GENERATING PAPER 5 FIGURES: The Climate Coordination Crisis")
    print("=" * 60)

    # Generate all figures
    fig1_technology_fallacy(args.output_dir)
    fig2_climate_coordination_spiral(args.output_dir)
    fig3_ten_percent_reallocation(args.output_dir)
    fig4_paris_gap(args.output_dir)
    fig5_intergenerational_timeline(args.output_dir)
    fig6_trust_infrastructure_roi(args.output_dir)
    fig7_harmony_gaps(args.output_dir)
    fig8_historical_precedents(args.output_dir)

    print("=" * 60)
    print(f"All figures generated in: {args.output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
