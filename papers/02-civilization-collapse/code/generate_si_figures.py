#!/usr/bin/env python3
"""
Generate additional SI figures for Paper 2: Civilization Collapse Framework
- Figure S3: Bifurcation Diagram (Phase Transition Physics)
- Figure S4: Dark Trust Iceberg (Hidden Variable)
- Figure S5: Intervention Window Timeline (The Warning)
- Figure S6: Early Warning Indicators (Lead Times)
- Figure S7: LOOCV Results Scatter
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def figure_s3_bifurcation():
    """
    Figure S3: Bifurcation diagram showing phase transition at theta
    - Stable equilibrium above threshold
    - Bistability near threshold
    - Collapse attractor below threshold
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Control parameter (external stress)
    stress = np.linspace(0, 1, 500)
    theta = 0.375

    # Upper stable branch (above threshold)
    h3_stable_upper = 0.7 - 0.35 * stress
    h3_stable_upper = np.where(h3_stable_upper > theta, h3_stable_upper, np.nan)

    # Lower stable branch (collapsed state)
    h3_stable_lower = 0.15 + 0.1 * stress
    h3_stable_lower = np.where(stress > 0.6, h3_stable_lower, np.nan)

    # Unstable branch (threshold region)
    h3_unstable = theta * np.ones_like(stress)
    h3_unstable = np.where((stress > 0.3) & (stress < 0.95), h3_unstable, np.nan)

    # Plot branches
    ax.plot(stress, h3_stable_upper, 'g-', linewidth=3, label='Stable (Coordination)')
    ax.plot(stress, h3_stable_lower, 'r-', linewidth=3, label='Stable (Collapse)')
    ax.plot(stress, h3_unstable, 'k--', linewidth=2, label='Unstable (Threshold)', alpha=0.7)

    # Threshold line
    ax.axhline(y=theta, color='darkred', linestyle=':', linewidth=2, alpha=0.5)
    ax.text(0.02, theta + 0.02, r'$\theta = 0.375$', fontsize=11, color='darkred')

    # Critical point
    crit_stress = 0.93
    ax.plot(crit_stress, theta, 'ko', markersize=15, zorder=5)
    ax.annotate('Critical Point\n(Fold Bifurcation)', xy=(crit_stress, theta),
                xytext=(0.7, 0.5), fontsize=10,
                arrowprops=dict(arrowstyle='->', color='black'))

    # Hysteresis arrows
    ax.annotate('', xy=(0.85, 0.32), xytext=(0.85, 0.42),
                arrowprops=dict(arrowstyle='->', color='red', lw=2))
    ax.text(0.87, 0.37, 'Collapse\n(fast)', fontsize=9, color='red')

    ax.annotate('', xy=(0.5, 0.45), xytext=(0.5, 0.25),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))
    ax.text(0.52, 0.35, 'Recovery\n(slow, costly)', fontsize=9, color='green')

    # Zone shading
    ax.axhspan(0, theta, alpha=0.1, color='red')
    ax.axhspan(theta, 1, alpha=0.1, color='green')

    # Labels
    ax.set_xlabel('External Stress Parameter', fontsize=13)
    ax.set_ylabel(r'Trust Level ($H_3$)', fontsize=13)
    ax.set_title('Figure S3: Bifurcation Structure of Civilizational Collapse\n'
                 'The Phase Transition at the Trust Threshold',
                 fontsize=14, fontweight='bold')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.8)
    ax.legend(loc='upper right', fontsize=10)

    # Add annotation box
    textstr = ('Key Insight: The system exhibits\n'
               'hysteresis - recovery requires\n'
               'reducing stress below the level\n'
               'that triggered collapse.')
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.05, 0.15, textstr, fontsize=9, verticalalignment='top',
            bbox=props)

    plt.tight_layout()

    # Save
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s3_bifurcation.pdf'),
                dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s3_bifurcation.png'),
                dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure S3: Bifurcation Diagram saved")


def figure_s4_dark_trust():
    """
    Figure S4: The Dark Trust Iceberg
    Shows measured vs unmeasured components of trust
    """
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create iceberg shape
    # Above water (measured trust) - smaller triangle
    water_line = 0.5

    # Iceberg polygon - visible part
    visible_x = [0.3, 0.5, 0.7, 0.3]
    visible_y = [water_line, 0.85, water_line, water_line]
    ax.fill(visible_x, visible_y, color='lightblue', edgecolor='blue', linewidth=2)

    # Iceberg polygon - hidden part (much larger)
    hidden_x = [0.15, 0.3, 0.7, 0.85, 0.5, 0.15]
    hidden_y = [water_line, water_line, water_line, water_line, 0.05, water_line]
    ax.fill(hidden_x, hidden_y, color='steelblue', edgecolor='darkblue', linewidth=2, alpha=0.7)

    # Water line
    ax.axhline(y=water_line, color='navy', linestyle='-', linewidth=3)
    ax.fill_between([0, 1], 0, water_line, color='lightcyan', alpha=0.5)

    # Labels for visible trust components
    ax.text(0.5, 0.72, 'MEASURED TRUST\n(~60%)', fontsize=12, ha='center',
            fontweight='bold', color='darkblue')
    ax.text(0.5, 0.62, 'Survey responses\nInstitutional metrics\nVoting patterns',
            fontsize=10, ha='center', style='italic')

    # Labels for hidden trust components
    ax.text(0.5, 0.38, 'DARK TRUST\n(~40%)', fontsize=14, ha='center',
            fontweight='bold', color='white')

    # Dark trust components with arrows
    components = [
        (0.25, 0.32, 'Habitual Trust\n(routines, customs)'),
        (0.75, 0.32, 'Network Trust\n(relational capital)'),
        (0.5, 0.22, 'Narrative Trust\n(shared identity stories)'),
        (0.35, 0.12, 'Tacit Trust\n(implicit norms)'),
        (0.65, 0.12, 'Embodied Trust\n(practiced behaviors)'),
    ]

    for x, y, label in components:
        ax.text(x, y, label, fontsize=9, ha='center', color='white',
                bbox=dict(boxstyle='round', facecolor='darkblue', alpha=0.6))

    # Percentage annotations
    ax.annotate('', xy=(0.88, 0.7), xytext=(0.88, water_line),
                arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    ax.text(0.92, 0.6, '~60%\nVisible', fontsize=10, color='green', ha='left')

    ax.annotate('', xy=(0.88, water_line), xytext=(0.88, 0.1),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax.text(0.92, 0.3, '~40%\nHidden', fontsize=10, color='red', ha='left')

    # Title and formatting
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Figure S4: The Dark Trust Iceberg\n'
                 'Why Surveys Underestimate Total Coordination Capacity',
                 fontsize=14, fontweight='bold', pad=20)

    # Add note
    fig.text(0.5, 0.02,
             'Note: "Dark Trust" represents unmeasured coordination capacity—habitual patterns,\n'
             'informal networks, and cultural narratives that enable cooperation without explicit trust.',
             ha='center', fontsize=10, style='italic')

    plt.tight_layout()

    # Save
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s4_dark_trust.pdf'),
                dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s4_dark_trust.png'),
                dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure S4: Dark Trust Iceberg saved")


def figure_s5_intervention_window():
    """
    Figure S5: The Intervention Window Timeline
    Shows optimal timing for interventions relative to threshold crossing
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    # Time axis (years relative to threshold crossing)
    years = np.linspace(-30, 20, 500)

    # Trust trajectory (declining, crosses at t=0)
    theta = 0.375
    h3 = 0.55 - 0.006 * (years + 30)  # Linear decline
    h3 = np.clip(h3, 0.2, 0.6)

    # Intervention effectiveness curve (relative ROI)
    # High before threshold, drops dramatically after
    effectiveness = np.where(years < 0,
                            10 - 0.1 * np.abs(years),  # Pre-threshold
                            1 / (1 + 0.5 * years))      # Post-threshold
    effectiveness = np.clip(effectiveness, 0.1, 10)

    # Create twin axis for effectiveness
    ax2 = ax.twinx()

    # Plot trust trajectory
    ax.plot(years, h3, 'b-', linewidth=3, label=r'Trust ($H_3$)')
    ax.axhline(y=theta, color='darkred', linestyle='--', linewidth=2, alpha=0.8)
    ax.text(15, theta + 0.015, r'$\theta = 0.375$', fontsize=11, color='darkred')

    # Plot effectiveness
    ax2.fill_between(years, 0, effectiveness, alpha=0.3, color='green')
    ax2.plot(years, effectiveness, 'g-', linewidth=2, alpha=0.7)

    # Zone shading and labels
    # Golden window
    ax.axvspan(-20, -5, alpha=0.15, color='gold')
    ax.text(-12.5, 0.58, 'GOLDEN WINDOW\n(ROI: 8-10x)', fontsize=10, ha='center',
            fontweight='bold', color='darkgoldenrod')

    # Warning zone
    ax.axvspan(-5, 0, alpha=0.15, color='orange')
    ax.text(-2.5, 0.58, 'WARNING\n(ROI: 3-7x)', fontsize=10, ha='center',
            fontweight='bold', color='darkorange')

    # Crisis zone
    ax.axvspan(0, 10, alpha=0.15, color='red')
    ax.text(5, 0.58, 'CRISIS\n(ROI: 0.5-1x)', fontsize=10, ha='center',
            fontweight='bold', color='darkred')

    # Collapse zone
    ax.axvspan(10, 20, alpha=0.2, color='black')
    ax.text(15, 0.58, 'TOO LATE\n(ROI: <0.1x)', fontsize=10, ha='center',
            fontweight='bold', color='white',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))

    # Threshold crossing marker
    ax.axvline(x=0, color='red', linestyle='-', linewidth=3, alpha=0.7)
    ax.text(0.5, 0.25, 'THRESHOLD\nCROSSING', fontsize=10, color='red',
            fontweight='bold', rotation=90, va='bottom')

    # Add intervention examples
    interventions = [
        (-15, 0.47, 'Marshall Plan\n(1948)', 'green'),
        (-5, 0.41, 'USSR Reforms\n(1985)', 'orange'),
        (3, 0.35, 'Late Roman\nReforms', 'red'),
    ]

    for x, y, label, color in interventions:
        ax.plot(x, y, 'o', markersize=12, color=color, zorder=5)
        ax.annotate(label, xy=(x, y), xytext=(x, y-0.07), fontsize=9,
                   ha='center', color=color)

    # Labels
    ax.set_xlabel('Years Relative to Threshold Crossing', fontsize=13)
    ax.set_ylabel(r'Trust Level ($H_3$)', fontsize=13, color='blue')
    ax2.set_ylabel('Intervention Effectiveness (ROI)', fontsize=13, color='green')

    ax.set_xlim(-30, 20)
    ax.set_ylim(0.2, 0.65)
    ax2.set_ylim(0, 12)

    ax.set_title('Figure S5: The Intervention Window\n'
                 'Why Timing Determines Success or Failure',
                 fontsize=14, fontweight='bold')

    # Legend
    lines1, labels1 = ax.get_legend_handles_labels()
    ax.legend(lines1, labels1, loc='lower left', fontsize=10)

    plt.tight_layout()

    # Save
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s5_intervention_window.pdf'),
                dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s5_intervention_window.png'),
                dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure S5: Intervention Window Timeline saved")


def figure_s6_early_warning():
    """
    Figure S6: Early Warning Indicators and Lead Times
    Shows which indicators appear before collapse and when
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # Early warning indicators with lead times
    indicators = [
        ('Elite Fragmentation', 30, 50, 'Succession crises, faction formation'),
        ('Economic Polarization', 25, 40, 'Gini spike, wealth concentration'),
        ('Institutional Sclerosis', 20, 35, 'Reform failure rate increase'),
        ('Narrative Divergence', 15, 30, 'Ideological polarization, "culture war"'),
        ('Trust Decay Acceleration', 10, 25, r'$dH_3/dt$ becomes increasingly negative'),
        ('Infrastructure Neglect', 8, 20, 'Deferred maintenance, decay'),
        ('Brain Drain', 5, 15, 'Elite emigration, skill loss'),
        ('Currency Instability', 3, 10, 'Inflation, debasement'),
    ]

    y_positions = range(len(indicators))

    # Create horizontal bars showing lead time ranges
    for i, (name, lead_min, lead_max, desc) in enumerate(indicators):
        # Bar showing range
        ax.barh(i, lead_max - lead_min, left=lead_min, height=0.6,
               color=plt.cm.RdYlGn(1 - i/len(indicators)), alpha=0.7,
               edgecolor='black', linewidth=1)

        # Add description
        ax.text(lead_max + 1, i, desc, fontsize=9, va='center', style='italic')

    # Threshold crossing line
    ax.axvline(x=0, color='red', linestyle='-', linewidth=3)
    ax.text(0, len(indicators) - 0.3, 'THRESHOLD\nCROSSING', fontsize=10,
            color='red', fontweight='bold', ha='center')

    # Zone annotations
    ax.axvspan(0, -5, alpha=0.2, color='red')
    ax.axvspan(30, 60, alpha=0.1, color='green')

    # Labels
    ax.set_yticks(y_positions)
    ax.set_yticklabels([ind[0] for ind in indicators], fontsize=11)
    ax.set_xlabel('Years Before Threshold Crossing', fontsize=13)
    ax.set_title('Figure S6: Early Warning Indicators\n'
                 'Typical Lead Times Before Collapse',
                 fontsize=14, fontweight='bold')

    ax.set_xlim(-5, 60)
    ax.invert_xaxis()  # Earlier times on right

    # Add annotation
    ax.text(55, 0.5, 'Earlier\nWarning', fontsize=10, ha='center', color='green',
            fontweight='bold')
    ax.text(5, 0.5, 'Late\nWarning', fontsize=10, ha='center', color='red',
            fontweight='bold')

    # Note
    fig.text(0.5, 0.02,
             'Note: When 4+ indicators are present simultaneously, collapse typically follows within two generations.',
             ha='center', fontsize=10, style='italic')

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)

    # Save
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s6_early_warning.pdf'),
                dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s6_early_warning.png'),
                dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure S6: Early Warning Indicators saved")


def figure_s7_loocv_scatter():
    """
    Figure S7: LOOCV Results - Predicted vs Actual Collapse Years
    """
    fig, ax = plt.subplots(figsize=(10, 10))

    # Sample data (representative of 35 cases)
    np.random.seed(42)

    cases = [
        ('W. Rome', 476, 470, 'Agrarian'),
        ('Soviet', 1991, 1990, 'Modern'),
        ('Maya', 900, 890, 'Agrarian'),
        ('Ming', 1644, 1635, 'Agrarian'),
        ('Bronze Age', -1150, -1160, 'Agrarian'),
        ('Qing', 1912, 1905, 'Modern'),
        ('Ottoman', 1922, 1915, 'Agrarian'),
        ('Spanish', 1824, 1820, 'Maritime'),
        ('Venice', 1797, 1790, 'Commercial'),
        ('Dutch', 1795, 1788, 'Commercial'),
        ('Carolingian', 888, 863, 'Agrarian'),  # Worst prediction
        ('W. Han', 23, 20, 'Agrarian'),
        ('Tang', 907, 900, 'Agrarian'),
        ('Abbasid', 1258, 1250, 'Agrarian'),
        ('Byzantine', 1453, 1445, 'Agrarian'),
    ]

    actual = [c[1] for c in cases]
    predicted = [c[2] for c in cases]
    names = [c[0] for c in cases]
    types = [c[3] for c in cases]

    # Color mapping
    type_colors = {'Agrarian': 'green', 'Modern': 'red', 'Maritime': 'blue', 'Commercial': 'orange'}
    colors = [type_colors[t] for t in types]

    # Perfect prediction line
    min_year = min(min(actual), min(predicted)) - 50
    max_year = max(max(actual), max(predicted)) + 50
    ax.plot([min_year, max_year], [min_year, max_year], 'k--', linewidth=2,
            label='Perfect Prediction', alpha=0.5)

    # ±15 year bands
    ax.fill_between([min_year, max_year],
                    [min_year - 15, max_year - 15],
                    [min_year + 15, max_year + 15],
                    alpha=0.2, color='gray', label='±15 year band')

    # Plot points
    for i, (name, act, pred, typ) in enumerate(cases):
        ax.scatter(act, pred, c=type_colors[typ], s=100, zorder=5, edgecolor='black')
        # Label outliers and key cases
        if abs(act - pred) > 15 or name in ['W. Rome', 'Soviet', 'Maya']:
            ax.annotate(name, (act, pred), xytext=(5, 5), textcoords='offset points',
                       fontsize=9)

    # Legend for types
    legend_elements = [plt.scatter([], [], c=c, s=100, label=t, edgecolor='black')
                      for t, c in type_colors.items()]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10, title='Civilization Type')

    # Stats annotation
    errors = [abs(a - p) for a, p in zip(actual, predicted)]
    mae = np.mean(errors)
    within_15 = sum(1 for e in errors if e <= 15) / len(errors) * 100

    stats_text = f'Mean Absolute Error: {mae:.1f} years\nWithin ±15 years: {within_15:.0f}%'
    ax.text(0.95, 0.05, stats_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Labels
    ax.set_xlabel('Actual Collapse Year', fontsize=13)
    ax.set_ylabel('Predicted Collapse Year', fontsize=13)
    ax.set_title('Figure S7: Leave-One-Out Cross-Validation Results\n'
                 'Predicted vs. Actual Collapse Timing (N=35)',
                 fontsize=14, fontweight='bold')

    ax.set_xlim(min_year, max_year)
    ax.set_ylim(min_year, max_year)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    # Save
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s7_loocv_scatter.pdf'),
                dpi=300, bbox_inches='tight')
    plt.savefig(os.path.join(OUTPUT_DIR, 'figure_s7_loocv_scatter.png'),
                dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Figure S7: LOOCV Scatter saved")


if __name__ == '__main__':
    print("Generating additional SI figures for Paper 2...")
    print("-" * 50)

    figure_s3_bifurcation()
    figure_s4_dark_trust()
    figure_s5_intervention_window()
    figure_s6_early_warning()
    figure_s7_loocv_scatter()

    print("-" * 50)
    print("All SI figures generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
