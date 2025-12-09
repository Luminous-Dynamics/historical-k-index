#!/usr/bin/env python3
"""
Paper 8: K-Index Policy Framework - Figure Generation

Generates publication-quality figures for the policy framework paper:
1. The Five Policy Domains
2. Three Intervention Timescales
3. K Trajectory Projections
4. Investment vs Returns Analysis
5. Implementation Architecture
6. Seven Strategic Principles
7. Regional Investment Allocation
8. The Path Forward Comparison
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Rectangle
from matplotlib.lines import Line2D
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
plt.rcParams['figure.figsize'] = (10, 8)

# Color schemes
POLICY_COLORS = {
    'institutional': '#2E86AB',     # Blue
    'social': '#A23B72',            # Magenta
    'economic': '#F18F01',          # Orange
    'communication': '#C73E1D',     # Red
    'global': '#3B1F2B',            # Dark
    'primary': '#1a5276',
    'secondary': '#2ecc71',
    'warning': '#e74c3c',
    'neutral': '#95a5a6'
}


def fig1_five_policy_domains(output_dir):
    """Create visualization of the five policy domains."""
    fig, ax = plt.subplots(figsize=(12, 10))

    # Domain data
    domains = [
        ('Domain 1:\nInstitutional\nCapacity', 'H1', '$25-30B', '+0.15-0.20', POLICY_COLORS['institutional']),
        ('Domain 2:\nSocial\nCohesion', 'H3', '$40-50B', '+0.18-0.25', POLICY_COLORS['social']),
        ('Domain 3:\nEconomic\nCoordination', 'H2', '$30-35B', '+0.12-0.18', POLICY_COLORS['economic']),
        ('Domain 4:\nCommunication\nInfrastructure', 'H4, H7', '$15-20B', '+0.20-0.28', POLICY_COLORS['communication']),
        ('Domain 5:\nGlobal\nArchitecture', 'All', '$15-20B', '+0.08-0.12', POLICY_COLORS['global'])
    ]

    # Create circular arrangement
    center_x, center_y = 0.5, 0.5
    radius = 0.35

    for i, (name, harmony, investment, impact, color) in enumerate(domains):
        angle = np.pi/2 - (2 * np.pi * i / 5)  # Start from top
        x = center_x + radius * np.cos(angle)
        y = center_y + radius * np.sin(angle)

        # Draw domain circle
        circle = Circle((x, y), 0.12, facecolor=color, edgecolor='white',
                        linewidth=2, alpha=0.9, transform=ax.transAxes)
        ax.add_patch(circle)

        # Add domain name
        ax.text(x, y + 0.02, name, ha='center', va='center',
               fontsize=9, fontweight='bold', color='white',
               transform=ax.transAxes)

        # Add details below
        detail_y = y - 0.18
        ax.text(x, detail_y, f'Target: {harmony}', ha='center', va='top',
               fontsize=8, transform=ax.transAxes)
        ax.text(x, detail_y - 0.04, f'Investment: {investment}/yr', ha='center', va='top',
               fontsize=8, transform=ax.transAxes)
        ax.text(x, detail_y - 0.08, f'Impact: {impact}', ha='center', va='top',
               fontsize=8, color=color, fontweight='bold', transform=ax.transAxes)

        # Draw connection to center
        ax.annotate('', xy=(center_x, center_y), xytext=(x, y),
                   arrowprops=dict(arrowstyle='-', color=color, alpha=0.3, lw=2),
                   transform=ax.transAxes)

    # Central hub
    center_circle = Circle((center_x, center_y), 0.08, facecolor='#2c3e50',
                          edgecolor='gold', linewidth=3, transform=ax.transAxes)
    ax.add_patch(center_circle)
    ax.text(center_x, center_y + 0.015, 'K-Index', ha='center', va='center',
           fontsize=11, fontweight='bold', color='white', transform=ax.transAxes)
    ax.text(center_x, center_y - 0.02, 'Framework', ha='center', va='center',
           fontsize=9, color='gold', transform=ax.transAxes)

    # Title and summary
    ax.text(0.5, 0.98, 'The Five Policy Domains', ha='center', va='top',
           fontsize=14, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.93, 'Total Investment: $125-150B annually (0.15% of global GDP)',
           ha='center', va='top', fontsize=10, style='italic', transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig1_five_policy_domains.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig1_five_policy_domains.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig1_five_policy_domains")


def fig2_three_timescales(output_dir):
    """Create visualization of the three intervention timescales."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 8))

    timescales = [
        {
            'name': 'Immediate\n(0-3 Years)',
            'objective': 'STABILIZATION',
            'target': 'Halt K decline at 0.52',
            'cost': '$20-25B total',
            'priorities': [
                'Crisis prevention',
                'Trust protection',
                'Polarization reduction',
                'Essential services'
            ],
            'color': '#e74c3c'
        },
        {
            'name': 'Medium-term\n(3-10 Years)',
            'objective': 'CAPACITY BUILDING',
            'target': 'Raise K to 0.62',
            'cost': '$70-85B/year',
            'priorities': [
                'Institutional reform',
                'Social cohesion programs',
                'Economic coordination',
                'Technology deployment'
            ],
            'color': '#f39c12'
        },
        {
            'name': 'Long-term\n(10-25 Years)',
            'objective': 'CIVILIZATIONAL CAPACITY',
            'target': 'Achieve K 0.72-0.78',
            'cost': '$100-130B/year',
            'priorities': [
                'Generational culture change',
                'Institutional maturation',
                'Economic transformation',
                'AI-enhanced coordination'
            ],
            'color': '#27ae60'
        }
    ]

    for ax, ts in zip(axes, timescales):
        # Background
        ax.add_patch(FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                    boxstyle="round,pad=0.02",
                                    facecolor=ts['color'], alpha=0.1,
                                    edgecolor=ts['color'], linewidth=3,
                                    transform=ax.transAxes))

        # Header
        ax.text(0.5, 0.92, ts['name'], ha='center', va='top',
               fontsize=14, fontweight='bold', color=ts['color'],
               transform=ax.transAxes)

        # Objective
        ax.text(0.5, 0.78, ts['objective'], ha='center', va='top',
               fontsize=12, fontweight='bold', color='#2c3e50',
               transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor=ts['color'], alpha=0.3))

        # Target
        ax.text(0.5, 0.65, ts['target'], ha='center', va='top',
               fontsize=11, style='italic', transform=ax.transAxes)

        # Cost
        ax.text(0.5, 0.55, ts['cost'], ha='center', va='top',
               fontsize=10, fontweight='bold', color=ts['color'],
               transform=ax.transAxes)

        # Priority list
        ax.text(0.5, 0.45, 'Key Priorities:', ha='center', va='top',
               fontsize=10, fontweight='bold', transform=ax.transAxes)

        for i, priority in enumerate(ts['priorities']):
            ax.text(0.5, 0.38 - i*0.08, f'• {priority}', ha='center', va='top',
                   fontsize=9, transform=ax.transAxes)

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    # Overall title
    fig.suptitle('Three Timescales of Intervention', fontsize=16, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(output_dir, 'fig2_three_timescales.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig2_three_timescales.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig2_three_timescales")


def fig3_k_trajectory(output_dir):
    """Create K-Index trajectory projections under different scenarios."""
    fig, ax = plt.subplots(figsize=(12, 8))

    years = np.arange(2025, 2051)

    # Status quo trajectory (decline)
    k_status_quo = 0.52 - 0.008 * (years - 2025)  # Linear decline

    # Full implementation trajectory
    k_full = np.zeros_like(years, dtype=float)
    k_full[0] = 0.52
    for i in range(1, len(years)):
        # S-curve growth with saturation around 0.78
        growth = 0.015 * (0.78 - k_full[i-1]) / 0.26
        k_full[i] = k_full[i-1] + growth

    # Partial implementation
    k_partial = np.zeros_like(years, dtype=float)
    k_partial[0] = 0.52
    for i in range(1, len(years)):
        growth = 0.008 * (0.68 - k_partial[i-1]) / 0.16
        k_partial[i] = k_partial[i-1] + growth

    # Plot trajectories
    ax.fill_between(years, k_status_quo, 0.32, alpha=0.2, color='red',
                    label='Crisis Zone (K < 0.35)')
    ax.fill_between(years, 0.72, 0.85, alpha=0.2, color='green',
                    label='Climate/AI Capable Zone')

    ax.plot(years, k_status_quo, 'r-', linewidth=3, label='Status Quo Trajectory')
    ax.plot(years, k_partial, 'y-', linewidth=3, label='Partial Implementation')
    ax.plot(years, k_full, 'g-', linewidth=3, label='Full Implementation')

    # Threshold lines
    ax.axhline(y=0.72, color='blue', linestyle='--', alpha=0.7, label='K_Paris (Climate)')
    ax.axhline(y=0.78, color='purple', linestyle='--', alpha=0.7, label='K_AI (Governance)')
    ax.axhline(y=0.35, color='red', linestyle=':', alpha=0.7, label='K_critical')

    # Key milestones
    ax.annotate('Paris Target\nAchieved', xy=(2040, 0.72), xytext=(2042, 0.65),
               fontsize=9, ha='left',
               arrowprops=dict(arrowstyle='->', color='blue'))
    ax.annotate('AI Governance\nCapable', xy=(2048, 0.78), xytext=(2043, 0.82),
               fontsize=9, ha='left',
               arrowprops=dict(arrowstyle='->', color='purple'))
    ax.annotate('Crisis\nThreshold', xy=(2048, 0.35), xytext=(2044, 0.40),
               fontsize=9, ha='left', color='red',
               arrowprops=dict(arrowstyle='->', color='red'))

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Global K-Index', fontsize=12)
    ax.set_title('K-Index Trajectory Projections: Status Quo vs Implementation',
                fontsize=14, fontweight='bold')
    ax.set_xlim(2025, 2050)
    ax.set_ylim(0.25, 0.85)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)

    # Add difference annotation
    ax.annotate('', xy=(2050, k_full[-1]), xytext=(2050, k_status_quo[-1]),
               arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(2051, (k_full[-1] + k_status_quo[-1])/2, 'Gap: 0.46',
           fontsize=10, fontweight='bold', va='center')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig3_k_trajectory.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig3_k_trajectory.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig3_k_trajectory")


def fig4_investment_returns(output_dir):
    """Create investment vs returns analysis."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # Left: Investment breakdown
    ax1 = axes[0]
    categories = ['Institutional\nCapacity', 'Social\nCohesion', 'Economic\nCoordination',
                  'Communication\nInfra', 'Global\nArchitecture']
    investments = [27.5, 45, 32.5, 17.5, 17.5]  # Mid-range estimates in billions
    colors = [POLICY_COLORS['institutional'], POLICY_COLORS['social'],
              POLICY_COLORS['economic'], POLICY_COLORS['communication'],
              POLICY_COLORS['global']]

    bars = ax1.bar(categories, investments, color=colors, edgecolor='white', linewidth=2)
    ax1.set_ylabel('Annual Investment (Billions USD)', fontsize=11)
    ax1.set_title('Investment by Policy Domain', fontsize=12, fontweight='bold')
    ax1.set_ylim(0, 55)

    # Add value labels
    for bar, inv in zip(bars, investments):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'${inv}B', ha='center', fontsize=10, fontweight='bold')

    ax1.axhline(y=sum(investments)/len(investments), color='gray', linestyle='--',
               alpha=0.7, label=f'Average: ${sum(investments)/len(investments):.1f}B')
    ax1.legend()

    # Right: Cost-benefit analysis
    ax2 = axes[1]
    metrics = ['Framework\nCost', 'Climate\nDamages\nAvoided', 'Inequality\nCosts\nAvoided',
               'Coordination\nFailure\nCosts', 'Total\nBenefits']
    values = [-3, 35, 12.5, 20, 67.5]  # Trillions over 25 years
    colors2 = ['#e74c3c', '#27ae60', '#27ae60', '#27ae60', '#2ecc71']

    bars2 = ax2.bar(metrics, values, color=colors2, edgecolor='white', linewidth=2)
    ax2.set_ylabel('Value (Trillions USD, 25-year period)', fontsize=11)
    ax2.set_title('Cost-Benefit Analysis', fontsize=12, fontweight='bold')
    ax2.axhline(y=0, color='black', linewidth=1)

    # Add value labels
    for bar, val in zip(bars2, values):
        y_pos = bar.get_height() + 1 if val > 0 else bar.get_height() - 3
        ax2.text(bar.get_x() + bar.get_width()/2, y_pos,
                f'${abs(val):.1f}T', ha='center', fontsize=10, fontweight='bold')

    # Add ROI annotation
    ax2.text(0.95, 0.95, 'Return on Investment:\n15-30x', transform=ax2.transAxes,
            fontsize=12, fontweight='bold', ha='right', va='top',
            bbox=dict(boxstyle='round', facecolor='gold', alpha=0.8))

    ax2.set_ylim(-10, 80)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig4_investment_returns.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig4_investment_returns.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig4_investment_returns")


def fig5_implementation_architecture(output_dir):
    """Create implementation architecture visualization."""
    fig, ax = plt.subplots(figsize=(14, 10))

    # Governance levels
    levels = [
        ('Global Coordination Council', 0.85, '#1a5276'),
        ('Regional Coordination Bodies', 0.65, '#2874a6'),
        ('National Coordination Agencies', 0.45, '#3498db'),
        ('Local Coordination Networks', 0.25, '#85c1e9')
    ]

    # Draw levels
    for name, y, color in levels:
        # Main box
        width = 0.6 + 0.1 * (0.85 - y)  # Wider at bottom
        x = 0.5 - width/2
        rect = FancyBboxPatch((x, y - 0.06), width, 0.12,
                             boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='white',
                             linewidth=2, alpha=0.9, transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(0.5, y, name, ha='center', va='center',
               fontsize=12, fontweight='bold', color='white',
               transform=ax.transAxes)

    # Draw arrows
    for i in range(len(levels) - 1):
        y_top = levels[i][1] - 0.06
        y_bottom = levels[i+1][1] + 0.06
        ax.annotate('', xy=(0.4, y_bottom), xytext=(0.4, y_top),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=2),
                   transform=ax.transAxes)
        ax.annotate('', xy=(0.6, y_top), xytext=(0.6, y_bottom),
                   arrowprops=dict(arrowstyle='->', color='gray', lw=2),
                   transform=ax.transAxes)

    # Add phase timeline on the right
    ax.text(0.92, 0.92, 'Implementation Phases', ha='center', va='top',
           fontsize=11, fontweight='bold', transform=ax.transAxes)

    phases = [
        ('Phase 1 (1-3 yrs)', 'Foundation', '#e74c3c'),
        ('Phase 2 (4-7 yrs)', 'Scaling', '#f39c12'),
        ('Phase 3 (8-15 yrs)', 'Transformation', '#3498db'),
        ('Phase 4 (15-25 yrs)', 'Maturation', '#27ae60')
    ]

    for i, (name, desc, color) in enumerate(phases):
        y = 0.82 - i * 0.15
        rect = FancyBboxPatch((0.82, y - 0.05), 0.16, 0.1,
                             boxstyle="round,pad=0.01",
                             facecolor=color, alpha=0.8,
                             transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(0.90, y + 0.02, name, ha='center', va='center',
               fontsize=8, fontweight='bold', color='white',
               transform=ax.transAxes)
        ax.text(0.90, y - 0.02, desc, ha='center', va='center',
               fontsize=7, color='white', transform=ax.transAxes)

    # Funding mechanisms on the left
    ax.text(0.08, 0.92, 'Funding Mechanisms', ha='center', va='top',
           fontsize=11, fontweight='bold', transform=ax.transAxes)

    funding = [
        ('Coordination\nCapacity Fund', '$125-150B/yr'),
        ('Coordination\nBonds', 'K-linked returns'),
        ('Regional\nRebalancing', '$25-30B/yr')
    ]

    for i, (name, amount) in enumerate(funding):
        y = 0.78 - i * 0.18
        rect = FancyBboxPatch((0.02, y - 0.06), 0.14, 0.12,
                             boxstyle="round,pad=0.01",
                             facecolor='#2c3e50', alpha=0.8,
                             transform=ax.transAxes)
        ax.add_patch(rect)
        ax.text(0.09, y + 0.02, name, ha='center', va='center',
               fontsize=8, fontweight='bold', color='white',
               transform=ax.transAxes)
        ax.text(0.09, y - 0.025, amount, ha='center', va='center',
               fontsize=7, color='gold', transform=ax.transAxes)

    ax.text(0.5, 0.98, 'Implementation Architecture', ha='center', va='top',
           fontsize=16, fontweight='bold', transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig5_implementation_architecture.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig5_implementation_architecture.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig5_implementation_architecture")


def fig6_seven_principles(output_dir):
    """Create visualization of the seven strategic principles."""
    fig, ax = plt.subplots(figsize=(14, 10))

    principles = [
        ('1. Sequence Before Scale', 'Build capacity in proper sequence\nregardless of scaling urgency', '#e74c3c'),
        ('2. Trust Before Technology', 'Social trust must precede\ntechnological deployment', '#f39c12'),
        ('3. Local to Global', 'Build from local scales\nupward to global', '#f1c40f'),
        ('4. Measure What Matters', 'Deploy K-Index metrics\nto guide policy', '#2ecc71'),
        ('5. Invest in Bottlenecks', 'Target binding constraints\non coordination capacity', '#3498db'),
        ('6. Plan for Asymmetry', 'Building takes 3-7x longer\nthan destroying', '#9b59b6'),
        ('7. Embrace Complexity', 'Simple interventions have\ncomplex effects', '#34495e')
    ]

    # Create hexagonal arrangement with center
    center_x, center_y = 0.5, 0.48
    radius = 0.32

    # Center principle
    circle = Circle((center_x, center_y), 0.1, facecolor='#2c3e50',
                   edgecolor='gold', linewidth=3, transform=ax.transAxes)
    ax.add_patch(circle)
    ax.text(center_x, center_y + 0.015, 'K-Index', ha='center', va='center',
           fontsize=12, fontweight='bold', color='white', transform=ax.transAxes)
    ax.text(center_x, center_y - 0.025, 'Principles', ha='center', va='center',
           fontsize=10, color='gold', transform=ax.transAxes)

    # Outer principles
    for i, (name, desc, color) in enumerate(principles):
        if i < 6:  # First 6 in hexagon
            angle = np.pi/2 - (2 * np.pi * i / 6)
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
        else:  # 7th at bottom
            x = 0.5
            y = 0.08

        # Draw principle box
        rect = FancyBboxPatch((x - 0.11, y - 0.06), 0.22, 0.12,
                             boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='white',
                             linewidth=2, alpha=0.9, transform=ax.transAxes)
        ax.add_patch(rect)

        # Add principle name
        ax.text(x, y + 0.025, name, ha='center', va='center',
               fontsize=8, fontweight='bold', color='white',
               transform=ax.transAxes)
        ax.text(x, y - 0.02, desc, ha='center', va='center',
               fontsize=6, color='white', transform=ax.transAxes)

        # Draw connection to center
        if i < 6:
            ax.plot([center_x, x], [center_y, y], '-', color=color, alpha=0.3, lw=2,
                   transform=ax.transAxes)

    ax.text(0.5, 0.98, 'Seven Strategic Principles', ha='center', va='top',
           fontsize=16, fontweight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.93, 'Derived from K-Index Research Program', ha='center', va='top',
           fontsize=11, style='italic', transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig6_seven_principles.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig6_seven_principles.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig6_seven_principles")


def fig7_regional_allocation(output_dir):
    """Create regional investment allocation visualization."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    # Left: Regional K levels and needs
    ax1 = axes[0]
    regions = ['North\nAmerica', 'Europe', 'East\nAsia', 'South\nAsia',
               'Latin\nAmerica', 'Sub-Saharan\nAfrica', 'MENA']
    k_current = [0.68, 0.71, 0.62, 0.41, 0.48, 0.32, 0.44]
    k_target = [0.75, 0.78, 0.72, 0.60, 0.62, 0.55, 0.60]

    x = np.arange(len(regions))
    width = 0.35

    bars1 = ax1.bar(x - width/2, k_current, width, label='Current K',
                   color='#3498db', edgecolor='white')
    bars2 = ax1.bar(x + width/2, k_target, width, label='Target K (2040)',
                   color='#27ae60', edgecolor='white')

    ax1.axhline(y=0.72, color='purple', linestyle='--', alpha=0.7,
               label='K_Paris threshold')

    ax1.set_ylabel('K-Index', fontsize=11)
    ax1.set_title('Regional K-Index: Current vs Target', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(regions, fontsize=9)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.set_ylim(0, 0.85)
    ax1.grid(True, alpha=0.3, axis='y')

    # Right: Investment allocation (inverse to K)
    ax2 = axes[1]

    # Investment proportional to gap
    gaps = [k_target[i] - k_current[i] for i in range(len(regions))]
    total_gap = sum(gaps)
    allocations = [g / total_gap * 100 for g in gaps]  # Percentage

    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(regions)))

    bars = ax2.barh(regions, allocations, color=colors, edgecolor='white')
    ax2.set_xlabel('Share of Regional Rebalancing Fund (%)', fontsize=11)
    ax2.set_title('Investment Allocation by Region', fontsize=12, fontweight='bold')

    # Add value labels
    for bar, alloc in zip(bars, allocations):
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f'{alloc:.1f}%', va='center', fontsize=9)

    ax2.set_xlim(0, 35)
    ax2.grid(True, alpha=0.3, axis='x')

    # Add note
    ax2.text(0.95, 0.02, 'Allocation proportional to\ncoordination capacity gap',
            transform=ax2.transAxes, fontsize=8, style='italic',
            ha='right', va='bottom')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig7_regional_allocation.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig7_regional_allocation.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig7_regional_allocation")


def fig8_path_forward(output_dir):
    """Create visualization comparing the two paths forward."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 9))

    # Path A: Reactive Learning
    ax1 = axes[0]
    ax1.add_patch(FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                boxstyle="round,pad=0.02",
                                facecolor='#e74c3c', alpha=0.1,
                                edgecolor='#e74c3c', linewidth=3,
                                transform=ax1.transAxes))

    ax1.text(0.5, 0.92, 'PATH A: Reactive Learning', ha='center', va='top',
            fontsize=14, fontweight='bold', color='#c0392b',
            transform=ax1.transAxes)

    path_a = [
        ('Continue current trajectory', '0.52 → 0.32 by 2050'),
        ('Learn through catastrophic failures', 'Trillions in damages'),
        ('Rebuild capacity from crisis', '3-7x harder than prevention'),
        ('Hope for sufficient resilience', 'High risk of failure'),
        ('K at critical threshold', 'Civilizational crisis')
    ]

    for i, (step, outcome) in enumerate(path_a):
        y = 0.78 - i * 0.14
        ax1.text(0.1, y, f'{i+1}. {step}', ha='left', va='top',
                fontsize=10, transform=ax1.transAxes)
        ax1.text(0.9, y, outcome, ha='right', va='top',
                fontsize=9, color='#e74c3c', style='italic',
                transform=ax1.transAxes)

    # Cost summary
    ax1.text(0.5, 0.15, 'Total Cost: $45-90 TRILLION in damages',
            ha='center', va='top', fontsize=12, fontweight='bold',
            color='#c0392b', transform=ax1.transAxes)
    ax1.text(0.5, 0.08, 'Plus: Potential irreversible harm',
            ha='center', va='top', fontsize=10, color='#e74c3c',
            transform=ax1.transAxes)

    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.axis('off')

    # Path B: Proactive Investment
    ax2 = axes[1]
    ax2.add_patch(FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                boxstyle="round,pad=0.02",
                                facecolor='#27ae60', alpha=0.1,
                                edgecolor='#27ae60', linewidth=3,
                                transform=ax2.transAxes))

    ax2.text(0.5, 0.92, 'PATH B: Proactive Investment', ha='center', va='top',
            fontsize=14, fontweight='bold', color='#1e8449',
            transform=ax2.transAxes)

    path_b = [
        ('Implement K-Index framework', '0.52 → 0.78 by 2050'),
        ('Build capacity before challenges peak', 'Prevention > cure'),
        ('Navigate challenges from strength', 'Coordinated response'),
        ('Achieve sustainable flourishing', 'Self-reinforcing dynamics'),
        ('Address climate, AI, inequality', 'Civilizational success')
    ]

    for i, (step, outcome) in enumerate(path_b):
        y = 0.78 - i * 0.14
        ax2.text(0.1, y, f'{i+1}. {step}', ha='left', va='top',
                fontsize=10, transform=ax2.transAxes)
        ax2.text(0.9, y, outcome, ha='right', va='top',
                fontsize=9, color='#27ae60', style='italic',
                transform=ax2.transAxes)

    # Cost summary
    ax2.text(0.5, 0.15, 'Total Cost: $2.5-3.5 TRILLION investment',
            ha='center', va='top', fontsize=12, fontweight='bold',
            color='#1e8449', transform=ax2.transAxes)
    ax2.text(0.5, 0.08, 'ROI: 15-30x returns',
            ha='center', va='top', fontsize=10, color='#27ae60',
            transform=ax2.transAxes)

    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')

    fig.suptitle('The Choice Before Humanity', fontsize=16, fontweight='bold', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(os.path.join(output_dir, 'fig8_path_forward.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig8_path_forward.png'), bbox_inches='tight')
    plt.close()
    print("Generated: fig8_path_forward")


def main():
    parser = argparse.ArgumentParser(description='Generate Paper 8 figures')
    parser.add_argument('--output-dir', type=str, default='figures',
                       help='Output directory for figures')
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Generating Paper 8 figures in: {args.output_dir}")
    print("=" * 50)

    # Generate all figures
    fig1_five_policy_domains(args.output_dir)
    fig2_three_timescales(args.output_dir)
    fig3_k_trajectory(args.output_dir)
    fig4_investment_returns(args.output_dir)
    fig5_implementation_architecture(args.output_dir)
    fig6_seven_principles(args.output_dir)
    fig7_regional_allocation(args.output_dir)
    fig8_path_forward(args.output_dir)

    print("=" * 50)
    print(f"All figures generated successfully in: {args.output_dir}")


if __name__ == '__main__':
    main()
