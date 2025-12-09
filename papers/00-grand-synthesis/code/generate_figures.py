#!/usr/bin/env python3
"""
Grand Unified Synthesis - Figure Generation

Creates paradigm-shifting visualizations that integrate all K-Index concepts:
1. The Seven Harmonies Mandala
2. The Threshold Landscape
3. The 35 Laws Network
4. The Twelve Paradoxes Wheel
5. The Eight Escape Mechanisms
6. The Master Equation Visualization
7. The Coordination Singularity
8. The Two Paths of Humanity
9. The Unified Theory Map
10. The Birth of Coordination Science
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Rectangle, Polygon
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
import seaborn as sns
import argparse
import os

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['figure.figsize'] = (12, 10)

# Color schemes
COLORS = {
    'h1': '#1a5276',  # Blue - Institutions
    'h2': '#27ae60',  # Green - Economics
    'h3': '#e74c3c',  # Red - Social
    'h4': '#f39c12',  # Orange - Communication
    'h5': '#9b59b6',  # Purple - Cultural
    'h6': '#1abc9c',  # Teal - Environmental
    'h7': '#34495e',  # Dark - Technology
    'gold': '#d4ac0d',
    'danger': '#c0392b',
    'safe': '#27ae60',
    'neutral': '#7f8c8d'
}


def fig1_seven_harmonies_mandala(output_dir):
    """Create the Seven Harmonies Mandala - the core of the K-Index."""
    fig, ax = plt.subplots(figsize=(14, 14))

    center_x, center_y = 0.5, 0.5
    outer_radius = 0.38
    inner_radius = 0.12

    harmonies = [
        ('H1: Institutions', 'Governance\nQuality', COLORS['h1']),
        ('H2: Economics', 'Market\nCoordination', COLORS['h2']),
        ('H3: Social', 'Interpersonal\nTrust', COLORS['h3']),
        ('H4: Communication', 'Information\nFlow', COLORS['h4']),
        ('H5: Culture', 'Shared\nValues', COLORS['h5']),
        ('H6: Environment', 'Resource\nCoordination', COLORS['h6']),
        ('H7: Technology', 'Technical\nCapability', COLORS['h7'])
    ]

    # Draw outer petals
    for i, (name, desc, color) in enumerate(harmonies):
        angle = np.pi/2 - (2 * np.pi * i / 7)
        x = center_x + outer_radius * np.cos(angle)
        y = center_y + outer_radius * np.sin(angle)

        # Petal shape
        petal = Circle((x, y), 0.1, facecolor=color, edgecolor='white',
                       linewidth=2, alpha=0.85, transform=ax.transAxes)
        ax.add_patch(petal)

        # Harmony label
        ax.text(x, y + 0.02, name, ha='center', va='center',
               fontsize=10, fontweight='bold', color='white',
               transform=ax.transAxes)
        ax.text(x, y - 0.03, desc, ha='center', va='center',
               fontsize=7, color='white', transform=ax.transAxes)

        # Connection lines to all other harmonies
        for j in range(i+1, 7):
            angle2 = np.pi/2 - (2 * np.pi * j / 7)
            x2 = center_x + outer_radius * np.cos(angle2)
            y2 = center_y + outer_radius * np.sin(angle2)
            ax.plot([x, x2], [y, y2], '-', color='gray', alpha=0.2, lw=1,
                   transform=ax.transAxes)

    # Central K
    center = Circle((center_x, center_y), inner_radius, facecolor='#2c3e50',
                   edgecolor=COLORS['gold'], linewidth=4, transform=ax.transAxes)
    ax.add_patch(center)
    ax.text(center_x, center_y + 0.02, 'K', ha='center', va='center',
           fontsize=32, fontweight='bold', color=COLORS['gold'],
           transform=ax.transAxes)
    ax.text(center_x, center_y - 0.04, 'Index', ha='center', va='center',
           fontsize=12, color='white', transform=ax.transAxes)

    # Equation below
    ax.text(0.5, 0.08, r'$K = \left(\prod_{i=1}^{7} H_i^{w_i}\right)^{1/\sum w_i}$',
           ha='center', va='center', fontsize=14, transform=ax.transAxes)

    ax.text(0.5, 0.96, 'THE SEVEN HARMONIES MANDALA',
           ha='center', va='top', fontsize=18, fontweight='bold',
           transform=ax.transAxes)
    ax.text(0.5, 0.92, 'The Complete Space of Civilizational Coordination',
           ha='center', va='top', fontsize=12, style='italic',
           transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig1_seven_harmonies_mandala.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig1_seven_harmonies_mandala.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig1_seven_harmonies_mandala")


def fig2_threshold_landscape(output_dir):
    """Create the Threshold Landscape visualization."""
    fig, ax = plt.subplots(figsize=(14, 8))

    # Create landscape
    k_values = np.linspace(0, 1, 1000)

    # Define zones with different colors
    zones = [
        (0, 0.25, '#8e0000', 'Zone I:\nCivilizational Death'),
        (0.25, 0.35, '#c0392b', 'Zone II:\nCritical Danger'),
        (0.35, 0.45, '#e74c3c', 'Zone III:\nInstability'),
        (0.45, 0.62, '#f39c12', 'Zone IV:\nSuboptimal'),
        (0.62, 0.72, '#27ae60', 'Zone V:\nOptimal'),
        (0.72, 0.78, '#1e8449', 'Zone VI:\nHigh Capacity'),
        (0.78, 1.0, '#145a32', 'Zone VII:\nFull Capacity')
    ]

    # Draw zones
    for k_min, k_max, color, label in zones:
        ax.axvspan(k_min, k_max, alpha=0.6, color=color)
        ax.text((k_min + k_max) / 2, 0.85, label, ha='center', va='center',
               fontsize=8, fontweight='bold', transform=ax.transData,
               rotation=90 if k_max - k_min < 0.15 else 0)

    # Threshold markers
    thresholds = [
        (0.25, 'Phoenix\n(0.25)', 'k'),
        (0.35, 'Critical\n(0.35)', 'darkred'),
        (0.45, 'Stability\n(0.45)', 'red'),
        (0.52, 'Current\nK (0.52)', 'orange'),
        (0.62, 'Golden\n(0.62)', 'gold'),
        (0.72, 'Paris\n(0.72)', 'blue'),
        (0.78, 'AI\n(0.78)', 'purple')
    ]

    for k, label, color in thresholds:
        ax.axvline(x=k, color=color, linestyle='--', linewidth=2, alpha=0.8)
        ax.annotate(label, xy=(k, 0.95), fontsize=9, ha='center',
                   fontweight='bold', color=color)

    # Potential curve
    y_potential = 1 - np.exp(-3 * k_values) * (1 + 3 * k_values)
    ax.plot(k_values, y_potential * 0.7 + 0.1, 'k-', linewidth=3, alpha=0.7,
           label='Coordination Potential')

    ax.set_xlabel('K-Index Value', fontsize=12)
    ax.set_ylabel('Civilizational Potential', fontsize=12)
    ax.set_title('THE THRESHOLD LANDSCAPE\nSeven Zones of Civilizational Possibility',
                fontsize=14, fontweight='bold')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc='lower right')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig2_threshold_landscape.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig2_threshold_landscape.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig2_threshold_landscape")


def fig3_paradoxes_wheel(output_dir):
    """Create the Twelve Paradoxes Wheel."""
    fig, ax = plt.subplots(figsize=(14, 14))

    paradoxes = [
        'Emergence\nParadox',
        'Trust\nParadox',
        'Institution\nParadox',
        'Scale\nParadox',
        'Recovery\nTrap',
        'Success\nParadox',
        'Technology\nParadox',
        'AI-Coordination\nParadox',
        'Race-Cooperation\nTrap',
        'Short-Long\nTension',
        'Visibility\nParadox',
        'Measurement\nParadox'
    ]

    center_x, center_y = 0.5, 0.5
    radius = 0.35

    # Draw paradoxes in a wheel
    for i, paradox in enumerate(paradoxes):
        angle = np.pi/2 - (2 * np.pi * i / 12)
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)

        # Alternating colors for visual interest
        color = '#e74c3c' if i % 2 == 0 else '#c0392b'

        # Paradox box
        rect = FancyBboxPatch((x - 0.08, y - 0.05), 0.16, 0.1,
                             boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='white',
                             linewidth=2, alpha=0.9, transform=ax.transAxes)
        ax.add_patch(rect)

        ax.text(x, y, paradox, ha='center', va='center',
               fontsize=8, fontweight='bold', color='white',
               transform=ax.transAxes)

        # Connect to center
        ax.plot([center_x, x], [center_y, y], '-', color=color, alpha=0.3, lw=2,
               transform=ax.transAxes)

    # Center
    center = Circle((center_x, center_y), 0.12, facecolor='#2c3e50',
                   edgecolor='#e74c3c', linewidth=4, transform=ax.transAxes)
    ax.add_patch(center)
    ax.text(center_x, center_y + 0.02, 'THE 12', ha='center', va='center',
           fontsize=14, fontweight='bold', color='white',
           transform=ax.transAxes)
    ax.text(center_x, center_y - 0.03, 'PARADOXES', ha='center', va='center',
           fontsize=11, color='#e74c3c', transform=ax.transAxes)

    ax.text(0.5, 0.96, 'THE TWELVE PARADOXES OF COORDINATION',
           ha='center', va='top', fontsize=16, fontweight='bold',
           transform=ax.transAxes)
    ax.text(0.5, 0.92, 'Why Coordination is Simultaneously Necessary and Difficult',
           ha='center', va='top', fontsize=11, style='italic',
           transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig3_paradoxes_wheel.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig3_paradoxes_wheel.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig3_paradoxes_wheel")


def fig4_escape_mechanisms(output_dir):
    """Create the Eight Escape Mechanisms visualization."""
    fig, ax = plt.subplots(figsize=(14, 10))

    mechanisms = [
        ('1. SEEDING', 'Small wins build trust', 'Trust Paradox', '#27ae60'),
        ('2. SCAFFOLDING', 'Temporary structures enable permanent', 'Institution Paradox', '#3498db'),
        ('3. NESTING', 'Local to regional to global', 'Scale Paradox', '#9b59b6'),
        ('4. CATALYSIS', 'External capacity injection', 'Recovery Trap', '#e74c3c'),
        ('5. MEMORY', 'Institutionalize importance', 'Success Paradox', '#f39c12'),
        ('6. SEQUENCING', 'Trust before technology', 'Technology Paradox', '#1abc9c'),
        ('7. REFRAMING', 'Competition within cooperation', 'Race-Cooperation', '#e67e22'),
        ('8. MEASUREMENT', 'Make invisible visible', 'Visibility Paradox', '#34495e')
    ]

    # Create grid layout
    for i, (name, desc, paradox, color) in enumerate(mechanisms):
        row = i // 4
        col = i % 4

        x = 0.12 + col * 0.22
        y = 0.65 - row * 0.45

        # Mechanism box
        rect = FancyBboxPatch((x - 0.09, y - 0.15), 0.18, 0.3,
                             boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='white',
                             linewidth=2, alpha=0.9, transform=ax.transAxes)
        ax.add_patch(rect)

        ax.text(x, y + 0.08, name, ha='center', va='center',
               fontsize=9, fontweight='bold', color='white',
               transform=ax.transAxes)
        ax.text(x, y - 0.02, desc, ha='center', va='center',
               fontsize=7, color='white', transform=ax.transAxes,
               wrap=True)
        ax.text(x, y - 0.1, f'Escapes:\n{paradox}', ha='center', va='center',
               fontsize=6, style='italic', color='white', alpha=0.8,
               transform=ax.transAxes)

    ax.text(0.5, 0.96, 'THE EIGHT ESCAPE MECHANISMS',
           ha='center', va='top', fontsize=16, fontweight='bold',
           transform=ax.transAxes)
    ax.text(0.5, 0.91, 'How to Transcend the Paradoxes of Coordination',
           ha='center', va='top', fontsize=11, style='italic',
           transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig4_escape_mechanisms.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig4_escape_mechanisms.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig4_escape_mechanisms")


def fig5_coordination_singularity(output_dir):
    """Create the Coordination Singularity visualization."""
    fig, ax = plt.subplots(figsize=(12, 8))

    years = np.arange(2000, 2051)

    # Challenge complexity (exponential growth)
    challenge = 0.5 * np.exp(0.03 * (years - 2000))

    # Coordination capacity (status quo - declining)
    k_status_quo = np.zeros_like(years, dtype=float)
    k_status_quo[years <= 2008] = 0.62 - 0.005 * (years[years <= 2008] - 2000)
    k_status_quo[years > 2008] = 0.62 - 0.005 * 8 - 0.008 * (years[years > 2008] - 2008)

    # Coordination capacity (with intervention)
    k_intervention = k_status_quo.copy()
    intervention_start = 2025
    for i, year in enumerate(years):
        if year >= intervention_start:
            target = 0.78
            k_intervention[i] = k_status_quo[years == intervention_start][0] + \
                               (target - k_status_quo[years == intervention_start][0]) * \
                               (1 - np.exp(-0.1 * (year - intervention_start)))

    # Find singularity point
    singularity_idx = np.argmax(challenge > k_status_quo)
    singularity_year = years[singularity_idx]

    ax.fill_between(years, challenge, k_status_quo,
                    where=(challenge > k_status_quo),
                    alpha=0.3, color='red', label='Permanent Gap')

    ax.plot(years, challenge, 'r-', linewidth=3, label='Challenge Complexity')
    ax.plot(years, k_status_quo, 'b--', linewidth=2, label='K (Status Quo)')
    ax.plot(years, k_intervention, 'g-', linewidth=3, label='K (With Intervention)')

    # Singularity marker
    ax.axvline(x=singularity_year, color='red', linestyle=':', linewidth=2, alpha=0.8)
    ax.annotate(f'COORDINATION\nSINGULARITY\n~{singularity_year}',
               xy=(singularity_year, challenge[singularity_idx]),
               xytext=(singularity_year + 5, challenge[singularity_idx] + 0.1),
               fontsize=10, fontweight='bold', color='red',
               arrowprops=dict(arrowstyle='->', color='red'))

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Level', fontsize=12)
    ax.set_title('THE COORDINATION SINGULARITY\nWhen Challenges Permanently Exceed Capacity',
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10)
    ax.set_xlim(2000, 2050)
    ax.set_ylim(0.3, 1.2)
    ax.grid(True, alpha=0.3)

    # Warning box
    ax.text(0.98, 0.02, 'After the singularity,\nthe gap grows forever.\nHumanity can never catch up.',
           transform=ax.transAxes, fontsize=9, style='italic',
           ha='right', va='bottom', color='red',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig5_coordination_singularity.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig5_coordination_singularity.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig5_coordination_singularity")


def fig6_two_paths(output_dir):
    """Create the Two Paths of Humanity visualization."""
    fig, axes = plt.subplots(1, 2, figsize=(16, 10))

    # Path A: Decline
    ax1 = axes[0]
    years = np.arange(2025, 2051)
    k_decline = 0.52 - 0.008 * (years - 2025)

    ax1.fill_between(years, k_decline, 0.2, alpha=0.3, color='red')
    ax1.plot(years, k_decline, 'r-', linewidth=3)

    milestones_a = [
        (2031, 'Coordination Singularity'),
        (2040, 'Below Stability (0.45)'),
        (2050, 'Near Critical (0.35)')
    ]

    for year, label in milestones_a:
        k_val = 0.52 - 0.008 * (year - 2025)
        ax1.scatter([year], [k_val], color='red', s=100, zorder=5)
        ax1.annotate(label, xy=(year, k_val), xytext=(year, k_val + 0.05),
                    fontsize=9, ha='center')

    ax1.axhline(y=0.35, color='darkred', linestyle='--', alpha=0.7)
    ax1.text(2026, 0.36, 'Critical Threshold', fontsize=8, color='darkred')

    ax1.set_title('PATH A: REACTIVE LEARNING\nCost: $45-90 Trillion + Irreversible Harm',
                 fontsize=12, fontweight='bold', color='red')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('K-Index')
    ax1.set_ylim(0.25, 0.6)
    ax1.grid(True, alpha=0.3)

    # Path B: Investment
    ax2 = axes[1]
    k_rise = np.zeros_like(years, dtype=float)
    k_rise[0] = 0.52
    for i in range(1, len(years)):
        growth = 0.015 * (0.78 - k_rise[i-1]) / 0.26
        k_rise[i] = k_rise[i-1] + growth

    ax2.fill_between(years, 0.52, k_rise, alpha=0.3, color='green')
    ax2.plot(years, k_rise, 'g-', linewidth=3)

    milestones_b = [
        (2030, 'Stabilization'),
        (2040, 'Paris Threshold (0.72)'),
        (2048, 'AI Threshold (0.78)')
    ]

    for year, label in milestones_b:
        idx = year - 2025
        k_val = k_rise[idx]
        ax2.scatter([year], [k_val], color='green', s=100, zorder=5)
        ax2.annotate(label, xy=(year, k_val), xytext=(year, k_val - 0.05),
                    fontsize=9, ha='center')

    ax2.axhline(y=0.72, color='blue', linestyle='--', alpha=0.7)
    ax2.axhline(y=0.78, color='purple', linestyle='--', alpha=0.7)
    ax2.text(2026, 0.73, 'Paris Threshold', fontsize=8, color='blue')
    ax2.text(2026, 0.79, 'AI Threshold', fontsize=8, color='purple')

    ax2.set_title('PATH B: PROACTIVE INVESTMENT\nCost: $2.5-3.5 Trillion | ROI: 15-30x',
                 fontsize=12, fontweight='bold', color='green')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('K-Index')
    ax2.set_ylim(0.45, 0.85)
    ax2.grid(True, alpha=0.3)

    fig.suptitle('THE TWO PATHS OF HUMANITY', fontsize=16, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(output_dir, 'fig6_two_paths.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig6_two_paths.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig6_two_paths")


def fig7_unified_theory_map(output_dir):
    """Create the Unified Theory Map showing all concepts."""
    fig, ax = plt.subplots(figsize=(16, 12))

    # Create a conceptual map
    elements = {
        # Core
        'K-Index': (0.5, 0.5, '#2c3e50', 0.12),
        # Laws
        '35 Laws': (0.2, 0.8, '#1a5276', 0.08),
        # Thresholds
        '7 Thresholds': (0.8, 0.8, '#c0392b', 0.08),
        # Paradoxes
        '12 Paradoxes': (0.2, 0.2, '#e74c3c', 0.08),
        # Mechanisms
        '8 Escapes': (0.8, 0.2, '#27ae60', 0.08),
        # Harmonies
        '7 Harmonies': (0.5, 0.85, '#9b59b6', 0.08),
        # Papers
        '8 Papers': (0.5, 0.15, '#f39c12', 0.08)
    }

    # Draw elements
    for name, (x, y, color, radius) in elements.items():
        circle = Circle((x, y), radius, facecolor=color, edgecolor='white',
                        linewidth=2, alpha=0.85, transform=ax.transAxes)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center',
               fontsize=10, fontweight='bold', color='white',
               transform=ax.transAxes)

    # Draw connections
    connections = [
        ('K-Index', '35 Laws'),
        ('K-Index', '7 Thresholds'),
        ('K-Index', '12 Paradoxes'),
        ('K-Index', '8 Escapes'),
        ('K-Index', '7 Harmonies'),
        ('K-Index', '8 Papers'),
        ('35 Laws', '7 Thresholds'),
        ('12 Paradoxes', '8 Escapes'),
        ('7 Harmonies', '35 Laws'),
        ('8 Papers', '35 Laws'),
        ('8 Papers', '7 Thresholds'),
        ('8 Papers', '12 Paradoxes'),
        ('8 Papers', '8 Escapes')
    ]

    for start, end in connections:
        x1, y1, _, _ = elements[start]
        x2, y2, _, _ = elements[end]
        ax.plot([x1, x2], [y1, y2], '-', color='gray', alpha=0.3, lw=2,
               transform=ax.transAxes)

    ax.text(0.5, 0.98, 'THE UNIFIED THEORY MAP',
           ha='center', va='top', fontsize=18, fontweight='bold',
           transform=ax.transAxes)
    ax.text(0.5, 0.93, 'Complete Architecture of Coordination Science',
           ha='center', va='top', fontsize=12, style='italic',
           transform=ax.transAxes)

    # Statistics box
    stats_text = (
        'TOTAL FRAMEWORK:\n'
        '• 35 Fundamental Laws\n'
        '• 7 Critical Thresholds\n'
        '• 12 Core Paradoxes\n'
        '• 8 Escape Mechanisms\n'
        '• 7 Harmonies\n'
        '• 8 Research Papers\n'
        '• 197 Years of Data\n'
        '• 195 Nations Analyzed'
    )
    ax.text(0.02, 0.02, stats_text, transform=ax.transAxes,
           fontsize=9, va='bottom', ha='left',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig7_unified_theory_map.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig7_unified_theory_map.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig7_unified_theory_map")


def fig8_coordination_science(output_dir):
    """Create the Birth of Coordination Science visualization."""
    fig, ax = plt.subplots(figsize=(14, 10))

    # Timeline
    disciplines = [
        ('Physics', 1687, 'Newton', '#3498db'),
        ('Chemistry', 1789, 'Lavoisier', '#2ecc71'),
        ('Biology', 1859, 'Darwin', '#e67e22'),
        ('Psychology', 1879, 'Wundt', '#9b59b6'),
        ('Economics', 1776, 'Smith', '#e74c3c'),
        ('Sociology', 1838, 'Comte', '#1abc9c'),
        ('Computer Science', 1936, 'Turing', '#34495e'),
        ('COORDINATION\nSCIENCE', 2025, 'K-Index', '#d4ac0d')
    ]

    # Sort by year
    disciplines = sorted(disciplines, key=lambda x: x[1])

    for i, (name, year, founder, color) in enumerate(disciplines):
        y = 0.15 + i * 0.1

        # Box
        rect = FancyBboxPatch((0.15, y - 0.035), 0.25, 0.07,
                             boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='white',
                             linewidth=2, alpha=0.85 if year < 2025 else 1.0,
                             transform=ax.transAxes)
        ax.add_patch(rect)

        ax.text(0.275, y, name, ha='center', va='center',
               fontsize=9 if year < 2025 else 11,
               fontweight='bold', color='white',
               transform=ax.transAxes)

        # Year and founder
        ax.text(0.45, y, str(year), ha='center', va='center',
               fontsize=10, fontweight='bold' if year == 2025 else 'normal',
               transform=ax.transAxes)
        ax.text(0.6, y, founder, ha='center', va='center',
               fontsize=9, style='italic',
               transform=ax.transAxes)

        # Connect to timeline
        ax.plot([0.42, 0.42], [y - 0.035, y + 0.035], '-', color=color, lw=2,
               transform=ax.transAxes)

    # Highlight 2025
    ax.annotate('THE 21st CENTURY\nIMPERATIVE', xy=(0.45, 0.85),
               xytext=(0.75, 0.85), fontsize=11, fontweight='bold',
               color=COLORS['gold'], ha='center',
               arrowprops=dict(arrowstyle='->', color=COLORS['gold']))

    ax.text(0.5, 0.96, 'THE BIRTH OF COORDINATION SCIENCE',
           ha='center', va='top', fontsize=18, fontweight='bold',
           transform=ax.transAxes)
    ax.text(0.5, 0.91, 'The Essential Science of the 21st Century',
           ha='center', va='top', fontsize=12, style='italic',
           transform=ax.transAxes)

    # Headers
    ax.text(0.275, 0.05, 'DISCIPLINE', ha='center', va='center',
           fontsize=10, fontweight='bold', transform=ax.transAxes)
    ax.text(0.45, 0.05, 'YEAR', ha='center', va='center',
           fontsize=10, fontweight='bold', transform=ax.transAxes)
    ax.text(0.6, 0.05, 'FOUNDER', ha='center', va='center',
           fontsize=10, fontweight='bold', transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig8_coordination_science.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig8_coordination_science.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig8_coordination_science")


def main():
    parser = argparse.ArgumentParser(description='Generate Grand Synthesis figures')
    parser.add_argument('--output-dir', type=str, default='figures',
                       help='Output directory for figures')
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Generating Grand Synthesis figures in: {args.output_dir}")
    print("=" * 60)

    # Generate all figures
    fig1_seven_harmonies_mandala(args.output_dir)
    fig2_threshold_landscape(args.output_dir)
    fig3_paradoxes_wheel(args.output_dir)
    fig4_escape_mechanisms(args.output_dir)
    fig5_coordination_singularity(args.output_dir)
    fig6_two_paths(args.output_dir)
    fig7_unified_theory_map(args.output_dir)
    fig8_coordination_science(args.output_dir)

    print("=" * 60)
    print(f"All Grand Synthesis figures generated successfully!")


if __name__ == '__main__':
    main()
