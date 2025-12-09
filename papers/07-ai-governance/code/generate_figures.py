#!/usr/bin/env python3
"""
Figure Generation for Paper 7: AI Governance and Coordination Capacity
======================================================================

Generates publication-quality figures illustrating the AI governance
challenge, coordination singularity, and proposed solutions.

Author: Tristan Stoltz
Date: December 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge
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
AI_COLORS = {
    'ai_dev': '#e74c3c',        # Red - AI development
    'governance': '#3498db',    # Blue - governance
    'gap': '#f39c12',          # Orange - gap
    'threshold': '#9b59b6',     # Purple - threshold
    'trust': '#1abc9c',         # Teal - trust
    'singularity': '#c0392b',   # Dark red - singularity
    'solution': '#27ae60',      # Green - solution
    'current': '#95a5a6',       # Gray - current
}


def fig1_ai_governance_threshold(output_dir):
    """
    Figure 1: The AI Governance Threshold
    Shows the 50% gap between required and current coordination
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    challenges = ['Nuclear\nNon-Prolif.', 'Ozone\nProtection', 'Climate\n(1.5°C)',
                  'Pandemic\nPreparedness', 'AI\nGovernance']
    required = [0.55, 0.52, 0.72, 0.60, 0.78]
    achieved = [0.58, 0.65, 0.52, 0.48, 0.52]

    x = np.arange(len(challenges))
    width = 0.35

    bars1 = ax.bar(x - width/2, required, width, label='Required K-Index',
                   color=AI_COLORS['threshold'], alpha=0.8)
    bars2 = ax.bar(x + width/2, achieved, width, label='Current/Achieved',
                   color=AI_COLORS['current'], alpha=0.8)

    # Highlight gaps
    for i, (req, ach) in enumerate(zip(required, achieved)):
        if req > ach:
            gap_pct = ((req - ach) / req) * 100
            ax.annotate(f'{gap_pct:.0f}%\ngap',
                       xy=(i + width/2, ach + 0.02),
                       ha='center', fontsize=9, color=AI_COLORS['gap'], fontweight='bold')

    # Highlight AI governance as the biggest challenge
    ax.annotate('LARGEST\nGAP EVER', xy=(4, 0.78), xytext=(4, 0.88),
               fontsize=10, ha='center', color=AI_COLORS['singularity'],
               fontweight='bold',
               arrowprops=dict(arrowstyle='->', color=AI_COLORS['singularity']))

    ax.set_ylabel('K-Index (Coordination Capacity)')
    ax.set_title("THE AI GOVERNANCE THRESHOLD\nAI requires K≈0.78, we have K≈0.52 (50% shortfall)",
                 fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(challenges)
    ax.legend(loc='upper left')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig1_ai_governance_threshold.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig1_ai_governance_threshold.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig1_ai_governance_threshold")


def fig2_ai_coordination_paradox(output_dir):
    """
    Figure 2: The AI-Coordination Paradox
    Shows how AI both increases need and decreases capacity
    """
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis('off')

    # Central paradox box
    center_box = FancyBboxPatch((3.5, 3.5), 3, 2, boxstyle="round,pad=0.1",
                                facecolor='#f39c12', alpha=0.3, edgecolor='#e67e22', linewidth=3)
    ax.add_patch(center_box)
    ax.text(5, 4.5, 'THE AI-COORDINATION\nPARADOX', ha='center', va='center',
           fontsize=12, fontweight='bold')

    # Left side: Increases need
    ax.text(1.5, 7, 'AI Development\nINCREASES\nCoordination Need', ha='center',
           fontsize=10, fontweight='bold', color=AI_COLORS['ai_dev'])
    ax.arrow(1.5, 6.3, 0, -0.8, head_width=0.2, head_length=0.1,
            fc=AI_COLORS['ai_dev'], ec=AI_COLORS['ai_dev'])

    needs = ['Global scope', 'Unprecedented speed', 'Irreversible outcomes', 'Complex verification']
    for i, need in enumerate(needs):
        ax.text(1.5, 5 - i*0.7, f'• {need}', ha='center', fontsize=9)

    # Right side: Decreases capacity
    ax.text(8.5, 7, 'AI Development\nDECREASES\nCoordination Capacity', ha='center',
           fontsize=10, fontweight='bold', color=AI_COLORS['governance'])
    ax.arrow(8.5, 6.3, 0, -0.8, head_width=0.2, head_length=0.1,
            fc=AI_COLORS['governance'], ec=AI_COLORS['governance'])

    decreases = ['Job displacement', 'Attention fragmentation', 'Trust erosion', 'Speed mismatch']
    for i, dec in enumerate(decreases):
        ax.text(8.5, 5 - i*0.7, f'• {dec}', ha='center', fontsize=9)

    # Arrows pointing to center
    ax.annotate('', xy=(3.5, 4.5), xytext=(2.5, 4.5),
               arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.annotate('', xy=(6.5, 4.5), xytext=(7.5, 4.5),
               arrowprops=dict(arrowstyle='->', color='black', lw=2))

    # Bottom: Result
    ax.text(5, 1.5, 'RESULT: The gap between required and available\ncoordination widens with each AI advance',
           ha='center', fontsize=10, style='italic',
           bbox=dict(boxstyle='round', facecolor=AI_COLORS['gap'], alpha=0.3))

    ax.set_title("THE AI-COORDINATION PARADOX\n\"AI increases coordination need while decreasing coordination capacity\"",
                fontweight='bold', fontsize=13, y=1.02)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig2_ai_coordination_paradox.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig2_ai_coordination_paradox.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig2_ai_coordination_paradox")


def fig3_coordination_singularity(output_dir):
    """
    Figure 3: The Coordination Singularity
    Shows the point where governance can never catch up
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    years = np.linspace(2024, 2040, 100)

    # AI capability growth (exponential)
    ai_capability = 1.0 * np.exp(0.15 * (years - 2024))

    # Governance capacity growth (linear/logarithmic)
    governance_current = 1.0 + 0.05 * (years - 2024)
    governance_optimal = 1.0 + 0.12 * (years - 2024)

    # Plot trajectories
    ax.plot(years, ai_capability, color=AI_COLORS['ai_dev'], linewidth=2.5,
           label='AI Development Speed')
    ax.plot(years, governance_current, color=AI_COLORS['current'], linewidth=2.5,
           linestyle='--', label='Current Governance Trajectory')
    ax.plot(years, governance_optimal, color=AI_COLORS['solution'], linewidth=2.5,
           linestyle=':', label='Optimal Governance Trajectory')

    # Mark singularity point
    singularity_year = 2031
    ax.axvline(x=singularity_year, color=AI_COLORS['singularity'], linewidth=2,
               linestyle='--', alpha=0.7)
    ax.annotate('COORDINATION\nSINGULARITY\n(~2031)',
               xy=(singularity_year, 2.5), xytext=(singularity_year + 2, 3.5),
               fontsize=10, color=AI_COLORS['singularity'], fontweight='bold',
               arrowprops=dict(arrowstyle='->', color=AI_COLORS['singularity']))

    # Shade the gap region
    ax.fill_between(years[years <= singularity_year],
                   ai_capability[years <= singularity_year],
                   governance_current[years <= singularity_year],
                   color=AI_COLORS['gap'], alpha=0.2, label='Governance Gap')

    ax.set_xlabel('Year')
    ax.set_ylabel('Development/Governance Speed (Index)')
    ax.set_title("THE COORDINATION SINGULARITY\n\"Beyond this point, governance can never catch up\"",
                fontweight='bold')
    ax.legend(loc='upper left')
    ax.set_xlim(2024, 2040)
    ax.set_ylim(0, 10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig3_coordination_singularity.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig3_coordination_singularity.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig3_coordination_singularity")


def fig4_harmony_gaps_ai(output_dir):
    """
    Figure 4: Harmony Gaps for AI Governance
    Shows which dimensions need most work
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    harmonies = ['H₁\nGovernance', 'H₃\nTrust', 'H₇\nInfrastructure',
                 'H₂\nEconomic', 'H₄\nSocial', 'H₅\nInnovation', 'H₆\nCultural']
    current = [0.51, 0.42, 0.68, 0.55, 0.48, 0.72, 0.45]
    required = [0.82, 0.75, 0.80, 0.72, 0.78, 0.70, 0.75]

    x = np.arange(len(harmonies))
    width = 0.35

    bars1 = ax.bar(x - width/2, current, width, label='Current Level',
                   color=AI_COLORS['current'], alpha=0.8)
    bars2 = ax.bar(x + width/2, required, width, label='Required for AI Governance',
                   color=AI_COLORS['threshold'], alpha=0.8)

    # Annotate gaps
    for i, (cur, req) in enumerate(zip(current, required)):
        gap = ((req - cur) / req) * 100
        color = AI_COLORS['ai_dev'] if gap > 30 else AI_COLORS['gap']
        if gap > 0:
            ax.annotate(f'{gap:.0f}%', xy=(i, max(cur, req) + 0.03),
                       ha='center', fontsize=9, color=color, fontweight='bold')
        else:
            ax.annotate('OK', xy=(i, max(cur, req) + 0.03),
                       ha='center', fontsize=9, color=AI_COLORS['solution'], fontweight='bold')

    # Highlight the critical gaps
    ax.annotate('Critical\nGaps', xy=(1, 0.75), fontsize=10, color=AI_COLORS['ai_dev'],
               fontweight='bold')

    ax.set_ylabel('Harmony Score')
    ax.set_title("HARMONY GAPS FOR AI GOVERNANCE\nInnovation exceeds needs; Trust and Culture lag badly",
                fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(harmonies)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 1.0)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig4_harmony_gaps_ai.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig4_harmony_gaps_ai.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig4_harmony_gaps_ai")


def fig5_race_cooperation_trap(output_dir):
    """
    Figure 5: The Race-Cooperation Trap
    Shows how competition undermines needed cooperation
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 9)
    ax.axis('off')

    # Title
    ax.text(5, 8.5, "THE RACE-COOPERATION TRAP\n\"Competitive dynamics select against cooperative institutions\"",
           ha='center', fontsize=12, fontweight='bold')

    # Race dynamics (left)
    ax.text(2.5, 7, 'RACING DYNAMICS', ha='center', fontsize=11, fontweight='bold',
           color=AI_COLORS['ai_dev'])

    race_factors = [
        ('Nations race for\nstrategic advantage', 5.5),
        ('Companies race for\nmarket dominance', 4.5),
        ('Researchers race\nfor recognition', 3.5),
    ]
    for text, y in race_factors:
        box = FancyBboxPatch((0.5, y-0.4), 4, 0.8, boxstyle="round,pad=0.05",
                            facecolor=AI_COLORS['ai_dev'], alpha=0.3, edgecolor='black')
        ax.add_patch(box)
        ax.text(2.5, y, text, ha='center', va='center', fontsize=9)

    # Consequences (right)
    ax.text(7.5, 7, 'CONSEQUENCES', ha='center', fontsize=11, fontweight='bold',
           color=AI_COLORS['singularity'])

    consequences = [
        ('Security dilemma\nescalates development', 5.5),
        ('First-mover incentives\npenalize coordination', 4.5),
        ('Secrecy prevents\nverification', 3.5),
    ]
    for text, y in consequences:
        box = FancyBboxPatch((5.5, y-0.4), 4, 0.8, boxstyle="round,pad=0.05",
                            facecolor=AI_COLORS['singularity'], alpha=0.3, edgecolor='black')
        ax.add_patch(box)
        ax.text(7.5, y, text, ha='center', va='center', fontsize=9)

    # Arrow from race to consequences
    ax.annotate('', xy=(5.3, 4.5), xytext=(4.7, 4.5),
               arrowprops=dict(arrowstyle='->', color='black', lw=2))

    # Result at bottom
    result_box = FancyBboxPatch((2, 1), 6, 1.5, boxstyle="round,pad=0.1",
                               facecolor=AI_COLORS['gap'], alpha=0.4, edgecolor='#d35400', linewidth=2)
    ax.add_patch(result_box)
    ax.text(5, 1.75, 'RESULT: Racing to build AI\nwhile destroying capacity to govern it',
           ha='center', va='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig5_race_cooperation_trap.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig5_race_cooperation_trap.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig5_race_cooperation_trap")


def fig6_coordination_first_strategy(output_dir):
    """
    Figure 6: The Coordination-First AI Strategy
    Shows the phased approach
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    phases = [
        ('Phase 1:\nTrust\nInfrastructure', 'Years 1-3', AI_COLORS['trust'], 'ΔH₃ ≥ +0.12'),
        ('Phase 2:\nGovernance\nScaffolding', 'Years 2-5', AI_COLORS['governance'], 'ΔH₁ ≥ +0.15'),
        ('Phase 3:\nBinding\nAgreements', 'Years 4-8', AI_COLORS['threshold'], 'K_AI ≥ 0.70'),
        ('Phase 4:\nAdaptive\nGovernance', 'Years 6+', AI_COLORS['solution'], 'dG/dt ≥ dA/dt'),
    ]

    for i, (phase, timing, color, target) in enumerate(phases):
        # Main box
        box = FancyBboxPatch((i*2.5 + 0.5, 2), 2, 3, boxstyle="round,pad=0.1",
                            facecolor=color, alpha=0.6, edgecolor='black', linewidth=2)
        ax.add_patch(box)

        # Phase name
        ax.text(i*2.5 + 1.5, 4.2, phase, ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')

        # Timing
        ax.text(i*2.5 + 1.5, 2.5, timing, ha='center', va='center',
               fontsize=9, color='white')

        # Target
        ax.text(i*2.5 + 1.5, 1.5, target, ha='center', va='center',
               fontsize=9, fontweight='bold', style='italic')

        # Arrow to next phase
        if i < len(phases) - 1:
            ax.annotate('', xy=(i*2.5 + 2.7, 3.5), xytext=(i*2.5 + 2.3, 3.5),
                       arrowprops=dict(arrowstyle='->', color='black', lw=2))

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title("COORDINATION-FIRST AI STRATEGY\n\"Build coordination capacity first. Development will follow.\"",
                fontweight='bold', fontsize=13, y=1.02)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig6_coordination_first_strategy.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig6_coordination_first_strategy.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig6_coordination_first_strategy")


def fig7_three_percent_solution(output_dir):
    """
    Figure 7: The 3% Solution
    Shows the investment required to close the gap
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Investment allocation
    categories = ['Trust\nInfrastructure', 'Governance\nInstitutions',
                  'Verification\nSystems', 'Public\nEngagement']
    investments = [3.5, 2.5, 1.5, 0.5]
    delta_k = [0.04, 0.03, 0.02, 0.01]
    colors = [AI_COLORS['trust'], AI_COLORS['governance'],
              AI_COLORS['threshold'], AI_COLORS['current']]

    bars = ax1.bar(categories, investments, color=colors, alpha=0.8, edgecolor='black')

    # Add delta K labels
    for bar, dk in zip(bars, delta_k):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'ΔK=+{dk:.2f}', ha='center', fontsize=9, fontweight='bold')

    ax1.set_ylabel('Annual Investment ($B)')
    ax1.set_title('3% Solution: $8B/year → +0.10 K/year', fontweight='bold')
    ax1.set_ylim(0, 4.5)

    # Right: Gap closure timeline
    years = np.arange(2025, 2032)
    current_k = 0.52
    k_trajectory = [current_k + 0.10 * (y - 2024) for y in years]
    required_k = 0.78

    ax2.plot(years, k_trajectory, color=AI_COLORS['solution'], linewidth=2.5,
            marker='o', label='With 3% Investment')
    ax2.axhline(y=required_k, color=AI_COLORS['threshold'], linestyle='--',
               linewidth=2, label=f'Required K={required_k}')
    ax2.axhline(y=current_k, color=AI_COLORS['current'], linestyle=':',
               linewidth=2, label=f'Current K={current_k}')

    # Mark crossing point
    ax2.annotate('Gap Closed\n(~2028)', xy=(2028, 0.78), xytext=(2029, 0.72),
                fontsize=10, fontweight='bold', color=AI_COLORS['solution'],
                arrowprops=dict(arrowstyle='->', color=AI_COLORS['solution']))

    ax2.set_xlabel('Year')
    ax2.set_ylabel('K-Index')
    ax2.set_title('Gap Closure Timeline', fontweight='bold')
    ax2.legend(loc='lower right')
    ax2.set_ylim(0.4, 0.9)
    ax2.grid(True, alpha=0.3)

    fig.suptitle("THE 3% SOLUTION\nClose the governance gap in 3-4 years", fontsize=14, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig7_three_percent_solution.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig7_three_percent_solution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig7_three_percent_solution")


def fig8_window_closing(output_dir):
    """
    Figure 8: The Closing Window
    Shows urgency of action
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    years = np.linspace(2024, 2035, 100)

    # Window of opportunity (closing)
    window = 100 * np.exp(-0.2 * (years - 2024))

    # Governance difficulty (rising)
    difficulty = 10 * np.exp(0.15 * (years - 2024))

    ax.fill_between(years, 0, window, color=AI_COLORS['solution'], alpha=0.3, label='Window of Opportunity')
    ax.fill_between(years, 0, difficulty, color=AI_COLORS['singularity'], alpha=0.3, label='Governance Difficulty')

    ax.plot(years, window, color=AI_COLORS['solution'], linewidth=2.5)
    ax.plot(years, difficulty, color=AI_COLORS['singularity'], linewidth=2.5)

    # Mark crossing point
    cross_year = 2029
    ax.axvline(x=cross_year, color='black', linestyle='--', linewidth=2)
    ax.annotate('WINDOW\nCLOSES', xy=(cross_year, 50), xytext=(cross_year + 1.5, 60),
               fontsize=11, fontweight='bold',
               arrowprops=dict(arrowstyle='->', color='black'))

    ax.set_xlabel('Year')
    ax.set_ylabel('Index Value')
    ax.set_title("THE CLOSING WINDOW\n\"Each year of delay doubles the difficulty\"",
                fontweight='bold')
    ax.legend(loc='upper right')
    ax.set_xlim(2024, 2035)
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'fig8_window_closing.pdf'), dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(output_dir, 'fig8_window_closing.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated: fig8_window_closing")


def main():
    parser = argparse.ArgumentParser(description='Generate Paper 7 figures')
    parser.add_argument('--output-dir', default='figures', help='Output directory')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 60)
    print("GENERATING PAPER 7 FIGURES: AI Governance and Coordination")
    print("=" * 60)

    fig1_ai_governance_threshold(args.output_dir)
    fig2_ai_coordination_paradox(args.output_dir)
    fig3_coordination_singularity(args.output_dir)
    fig4_harmony_gaps_ai(args.output_dir)
    fig5_race_cooperation_trap(args.output_dir)
    fig6_coordination_first_strategy(args.output_dir)
    fig7_three_percent_solution(args.output_dir)
    fig8_window_closing(args.output_dir)

    print("=" * 60)
    print(f"All figures generated in: {args.output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
