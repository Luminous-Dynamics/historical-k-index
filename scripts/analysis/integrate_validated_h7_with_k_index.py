#!/usr/bin/env python3
"""
Integrate Validated H₇ with Historical K(t) Index
==================================================

This script demonstrates the impact of replacing synthetic H₇ with validated
empirical H₇ on the overall K(t) index for the period 1996-2020.

Three K(t) formulations compared:
1. Six-harmony K(t): H₁-H₆ only (no H₇)
2. Seven-harmony K(t) (synthetic H₇): Current approach using HYDE-derived H₇
3. Seven-harmony K(t) (validated H₇): New approach using empirical H₇

Output:
- K(t) comparison CSV for 1996-2020
- Visualization showing all three formulations
- Statistical analysis of differences
- Manuscript-ready results summary
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

def load_existing_k_index():
    """Load existing K(t) index with synthetic H₇ (1810-2020)."""

    print("=" * 80)
    print("Loading Existing K(t) Index (1810-2020)")
    print("=" * 80)
    print()

    # Path to existing K(t) data
    k_path = Path('/srv/luminous-dynamics/kosmic-lab/historical_k/data_sources/processed/k_index_final_1810_2020.csv')

    if not k_path.exists():
        raise FileNotFoundError(f"K(t) index not found: {k_path}")

    df = pd.read_csv(k_path)

    print(f"✓ Loaded: {len(df)} years ({df['year'].min()}-{df['year'].max()})")
    print(f"  Columns: {', '.join(df.columns)}")
    print(f"  K(t) range: [{df['k_index'].min():.4f}, {df['k_index'].max():.4f}]")
    print()

    return df

def load_validated_h7():
    """Load validated H₇ component (1996-2021)."""

    print("=" * 80)
    print("Loading Validated H₇ Component (1996-2021)")
    print("=" * 80)
    print()

    # Path to validated H₇
    h7_path = Path('/srv/luminous-dynamics/historical-k-index/data/processed/H7_evolutionary_progression.csv')

    if not h7_path.exists():
        raise FileNotFoundError(f"Validated H₇ not found: {h7_path}")

    df = pd.read_csv(h7_path)

    # Select only year and H7 columns
    df_clean = df[['year', 'H7_evolutionary_progression']].copy()
    df_clean = df_clean.rename(columns={'H7_evolutionary_progression': 'h7_validated'})

    print(f"✓ Loaded: {len(df_clean)} observations ({df_clean['year'].min()}-{df_clean['year'].max()})")
    print(f"  Countries: 159")
    print(f"  H₇ range: [{df_clean['h7_validated'].min():.4f}, {df_clean['h7_validated'].max():.4f}]")
    print()

    # Since H₇ is country-level, we need to aggregate to global level
    # Use mean across all countries for each year
    h7_global = df_clean.groupby('year')['h7_validated'].mean().reset_index()

    print(f"✓ Aggregated to global level: {len(h7_global)} years")
    print(f"  Global H₇ range: [{h7_global['h7_validated'].min():.4f}, {h7_global['h7_validated'].max():.4f}]")
    print()

    return h7_global

def integrate_and_compare(k_existing, h7_validated):
    """Integrate validated H₇ and calculate three K(t) formulations."""

    print("=" * 80)
    print("Integrating Validated H₇ with K(t) Framework")
    print("=" * 80)
    print()

    # Filter to overlap period (1996-2020)
    overlap_years = range(1996, 2021)  # 1996-2020
    k_overlap = k_existing[k_existing['year'].isin(overlap_years)].copy()

    # Merge with validated H₇
    merged = k_overlap.merge(h7_validated, on='year', how='left')

    print(f"Overlap period: {merged['year'].min()}-{merged['year'].max()} ({len(merged)} years)")
    print(f"  Existing K(t) (with synthetic H₇): {merged['k_index'].mean():.4f}")
    print(f"  Synthetic H₇ mean: {merged['h7'].mean():.4f}")
    print(f"  Validated H₇ mean: {merged['h7_validated'].mean():.4f}")
    print()

    # Calculate three formulations
    print("Calculating three K(t) formulations:")
    print()

    # 1. Six-harmony K(t) (H₁-H₆ only)
    merged['k_six_harmony'] = (
        merged['h1'] * merged['h2'] * merged['h3'] *
        merged['h4'] * merged['h5'] * merged['h6']
    ) ** (1/6)
    print(f"1. Six-harmony K(t) (H₁-H₆):        Mean = {merged['k_six_harmony'].mean():.4f}")

    # 2. Seven-harmony K(t) with synthetic H₇ (current approach)
    merged['k_seven_synthetic'] = merged['k_index']  # Already calculated
    print(f"2. Seven-harmony K(t) (synthetic):  Mean = {merged['k_seven_synthetic'].mean():.4f}")

    # 3. Seven-harmony K(t) with validated H₇ (new approach)
    merged['k_seven_validated'] = (
        merged['h1'] * merged['h2'] * merged['h3'] * merged['h4'] *
        merged['h5'] * merged['h6'] * merged['h7_validated']
    ) ** (1/7)
    print(f"3. Seven-harmony K(t) (validated):  Mean = {merged['k_seven_validated'].mean():.4f}")
    print()

    # Calculate differences
    merged['diff_synthetic_vs_six'] = merged['k_seven_synthetic'] - merged['k_six_harmony']
    merged['diff_validated_vs_six'] = merged['k_seven_validated'] - merged['k_six_harmony']
    merged['diff_validated_vs_synthetic'] = merged['k_seven_validated'] - merged['k_seven_synthetic']

    return merged

def analyze_differences(df):
    """Analyze statistical differences between formulations."""

    print("=" * 80)
    print("Statistical Analysis of Differences")
    print("=" * 80)
    print()

    # Compare formulations
    comparisons = {
        'Seven-harmony (synthetic) vs Six-harmony': 'diff_synthetic_vs_six',
        'Seven-harmony (validated) vs Six-harmony': 'diff_validated_vs_six',
        'Seven-harmony (validated) vs Seven-harmony (synthetic)': 'diff_validated_vs_synthetic'
    }

    for name, col in comparisons.items():
        diff = df[col]
        mean_diff = diff.mean()
        std_diff = diff.std()
        min_diff = diff.min()
        max_diff = diff.max()

        # Calculate percentage change relative to six-harmony baseline
        baseline = df['k_six_harmony'].mean()
        pct_change = (mean_diff / baseline) * 100

        print(f"{name}:")
        print(f"  Mean difference: {mean_diff:+.6f} ({pct_change:+.2f}%)")
        print(f"  Std deviation:   {std_diff:.6f}")
        print(f"  Range:          [{min_diff:+.6f}, {max_diff:+.6f}]")
        print()

    # Year-by-year trends
    print("Temporal trends:")
    print(f"  1996-2000 (early): Validated vs Synthetic = {df[df['year'] <= 2000]['diff_validated_vs_synthetic'].mean():+.6f}")
    print(f"  2001-2010 (mid):   Validated vs Synthetic = {df[(df['year'] > 2000) & (df['year'] <= 2010)]['diff_validated_vs_synthetic'].mean():+.6f}")
    print(f"  2011-2020 (late):  Validated vs Synthetic = {df[df['year'] > 2010]['diff_validated_vs_synthetic'].mean():+.6f}")
    print()

    return df

def create_visualizations(df):
    """Create comprehensive visualization comparing all formulations."""

    print("=" * 80)
    print("Creating Visualization")
    print("=" * 80)
    print()

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Impact of Validated H₇ on K(t) Index (1996-2020)',
                 fontsize=16, fontweight='bold', y=0.995)

    # Panel A: All three K(t) formulations
    ax1 = axes[0, 0]
    ax1.plot(df['year'], df['k_six_harmony'],
             label='Six-harmony K(t) (H₁-H₆)', linewidth=2.5, color='#2E86AB', linestyle='--')
    ax1.plot(df['year'], df['k_seven_synthetic'],
             label='Seven-harmony K(t) (synthetic H₇)', linewidth=2.5, color='#A23B72', linestyle=':')
    ax1.plot(df['year'], df['k_seven_validated'],
             label='Seven-harmony K(t) (validated H₇)', linewidth=3, color='#F18F01')

    ax1.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax1.set_ylabel('K(t) Index', fontsize=11, fontweight='bold')
    ax1.set_title('A. Three K(t) Formulations Compared', fontsize=12, fontweight='bold', pad=10)
    ax1.legend(loc='lower right', framealpha=0.95, fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([0.5, 1.0])

    # Panel B: H₇ component comparison
    ax2 = axes[0, 1]
    ax2.plot(df['year'], df['h7'],
             label='H₇ synthetic (HYDE-based)', linewidth=2.5, color='#A23B72', linestyle=':')
    ax2.plot(df['year'], df['h7_validated'],
             label='H₇ validated (World Bank)', linewidth=3, color='#F18F01')

    ax2.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax2.set_ylabel('H₇ Component Value', fontsize=11, fontweight='bold')
    ax2.set_title('B. H₇ Component: Synthetic vs Validated', fontsize=12, fontweight='bold', pad=10)
    ax2.legend(loc='lower right', framealpha=0.95, fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0.0, 1.0])

    # Panel C: Difference between validated and synthetic
    ax3 = axes[1, 0]
    colors = ['green' if x >= 0 else 'red' for x in df['diff_validated_vs_synthetic']]
    ax3.bar(df['year'], df['diff_validated_vs_synthetic'], color=colors, alpha=0.6, edgecolor='black', linewidth=0.5)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax3.axhline(y=df['diff_validated_vs_synthetic'].mean(), color='blue', linestyle='--', linewidth=2,
                label=f"Mean = {df['diff_validated_vs_synthetic'].mean():+.6f}")

    ax3.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Difference (Validated - Synthetic)', fontsize=11, fontweight='bold')
    ax3.set_title('C. Impact of Validated H₇ on K(t)', fontsize=12, fontweight='bold', pad=10)
    ax3.legend(loc='upper left', framealpha=0.95, fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')

    # Panel D: Summary statistics table
    ax4 = axes[1, 1]
    ax4.axis('off')

    # Create summary table
    summary_data = [
        ['Metric', '1996', '2020', 'Mean', 'Change'],
        ['', '', '', '(1996-2020)', ''],
        ['Six-harmony K(t)', f"{df[df['year']==1996]['k_six_harmony'].values[0]:.4f}",
         f"{df[df['year']==2020]['k_six_harmony'].values[0]:.4f}",
         f"{df['k_six_harmony'].mean():.4f}",
         f"+{((df[df['year']==2020]['k_six_harmony'].values[0] - df[df['year']==1996]['k_six_harmony'].values[0]) / df[df['year']==1996]['k_six_harmony'].values[0] * 100):.1f}%"],
        ['Seven-harm. (synthetic)', f"{df[df['year']==1996]['k_seven_synthetic'].values[0]:.4f}",
         f"{df[df['year']==2020]['k_seven_synthetic'].values[0]:.4f}",
         f"{df['k_seven_synthetic'].mean():.4f}",
         f"+{((df[df['year']==2020]['k_seven_synthetic'].values[0] - df[df['year']==1996]['k_seven_synthetic'].values[0]) / df[df['year']==1996]['k_seven_synthetic'].values[0] * 100):.1f}%"],
        ['Seven-harm. (validated)', f"{df[df['year']==1996]['k_seven_validated'].values[0]:.4f}",
         f"{df[df['year']==2020]['k_seven_validated'].values[0]:.4f}",
         f"{df['k_seven_validated'].mean():.4f}",
         f"+{((df[df['year']==2020]['k_seven_validated'].values[0] - df[df['year']==1996]['k_seven_validated'].values[0]) / df[df['year']==1996]['k_seven_validated'].values[0] * 100):.1f}%"],
        ['', '', '', '', ''],
        ['H₇ synthetic', f"{df[df['year']==1996]['h7'].values[0]:.4f}",
         f"{df[df['year']==2020]['h7'].values[0]:.4f}",
         f"{df['h7'].mean():.4f}",
         f"+{((df[df['year']==2020]['h7'].values[0] - df[df['year']==1996]['h7'].values[0]) / df[df['year']==1996]['h7'].values[0] * 100):.1f}%"],
        ['H₇ validated', f"{df[df['year']==1996]['h7_validated'].values[0]:.4f}",
         f"{df[df['year']==2020]['h7_validated'].values[0]:.4f}",
         f"{df['h7_validated'].mean():.4f}",
         f"+{((df[df['year']==2020]['h7_validated'].values[0] - df[df['year']==1996]['h7_validated'].values[0]) / df[df['year']==1996]['h7_validated'].values[0] * 100):.1f}%"],
    ]

    table = ax4.table(cellText=summary_data, cellLoc='center', loc='center',
                     colWidths=[0.35, 0.15, 0.15, 0.15, 0.20])
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.5)

    # Style header row
    for i in range(5):
        table[(0, i)].set_facecolor('#2E86AB')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Style data rows with alternating colors
    for i in range(2, 8):  # Fixed: 8 rows total (0-7), styling rows 2-7
        for j in range(5):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#f0f0f0')

    ax4.set_title('D. Summary Statistics (1996-2020)', fontsize=12, fontweight='bold', pad=10)

    plt.tight_layout()

    # Save figure
    output_dir = Path('/srv/luminous-dynamics/historical-k-index/outputs/K_index_integration')
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / 'k_index_validated_h7_impact.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved visualization: {output_path}")
    print()

    return str(output_path)

def generate_manuscript_update(df, figure_path):
    """Generate manuscript Results section update."""

    print("=" * 80)
    print("Generating Manuscript Update")
    print("=" * 80)
    print()

    # Calculate key statistics
    k_six_mean = df['k_six_harmony'].mean()
    k_synthetic_mean = df['k_seven_synthetic'].mean()
    k_validated_mean = df['k_seven_validated'].mean()

    diff_validated_vs_synthetic = df['diff_validated_vs_synthetic'].mean()
    pct_change = (diff_validated_vs_synthetic / k_synthetic_mean) * 100

    k_2020_six = df[df['year'] == 2020]['k_six_harmony'].values[0]
    k_2020_validated = df[df['year'] == 2020]['k_seven_validated'].values[0]

    report = f"""
================================================================================
VALIDATED H₇ INTEGRATION: MANUSCRIPT RESULTS UPDATE
================================================================================

**Date**: {datetime.now().strftime('%B %d, %Y')}
**Period**: 1996-2020 (25 years, overlap with validated H₇)

## Key Findings

### K(t) Index Comparison (Mean 1996-2020)

1. **Six-harmony K(t)** (H₁-H₆ only): {k_six_mean:.4f}
2. **Seven-harmony K(t)** (synthetic H₇): {k_synthetic_mean:.4f} ({((k_synthetic_mean - k_six_mean) / k_six_mean * 100):+.2f}% vs six-harmony)
3. **Seven-harmony K(t)** (validated H₇): {k_validated_mean:.4f} ({((k_validated_mean - k_six_mean) / k_six_mean * 100):+.2f}% vs six-harmony)

### Impact of Validated H₇

**Mean difference** (validated vs synthetic): {diff_validated_vs_synthetic:+.6f} ({pct_change:+.2f}%)

**Interpretation**: The validated H₇ component results in a {'higher' if diff_validated_vs_synthetic > 0 else 'lower'} K(t)
index compared to the synthetic H₇, with an average difference of {abs(pct_change):.2f}% over
the 1996-2020 period.

### K(t) Values in 2020

- **Six-harmony K(t)₂₀₂₀**: {k_2020_six:.4f}
- **Seven-harmony K(t)₂₀₂₀** (validated): {k_2020_validated:.4f}
- **Difference**: {(k_2020_validated - k_2020_six):+.6f} ({((k_2020_validated - k_2020_six) / k_2020_six * 100):+.2f}%)

## Manuscript Text Insert (Results Section)

### Option 1: Full Description (~150 words)

For the period 1996-2020 where validated H₇ data are available, we compare three
K(t) formulations: six-harmony (H₁-H₆ only), seven-harmony with synthetic H₇
(HYDE-based), and seven-harmony with validated H₇ (World Bank empirical measures).

The validated seven-harmony K(t) shows a mean value of {k_validated_mean:.4f} over this period,
representing a {((k_validated_mean - k_six_mean) / k_six_mean * 100):+.2f}% {'increase' if k_validated_mean > k_six_mean else 'decrease'} relative to the six-harmony
baseline (mean {k_six_mean:.4f}). Compared to the synthetic H₇ approach (mean {k_synthetic_mean:.4f}),
the validated H₇ results in a mean difference of {diff_validated_vs_synthetic:+.6f} ({pct_change:+.2f}%), indicating
{'stronger' if diff_validated_vs_synthetic > 0 else 'weaker'} evolutionary progression when measured with direct empirical
indicators rather than demographic proxies.

In 2020, the validated seven-harmony K(t) reaches {k_2020_validated:.4f}, compared to {k_2020_six:.4f}
for the six-harmony formulation, demonstrating that the inclusion of validated
evolutionary progression measures {'enhances' if k_2020_validated > k_2020_six else 'moderates'} the overall coherence assessment by
{abs((k_2020_validated - k_2020_six) / k_2020_six * 100):.2f}%.

### Option 2: Concise Version (~50 words)

For 1996-2020, validated seven-harmony K(t) (mean {k_validated_mean:.4f}) differs from
synthetic H₇ formulation by {diff_validated_vs_synthetic:+.6f} ({pct_change:+.2f}%), indicating {'stronger' if diff_validated_vs_synthetic > 0 else 'weaker'}
evolutionary progression with empirical measures. K(t)₂₀₂₀ = {k_2020_validated:.4f} (validated)
vs {k_2020_six:.4f} (six-harmony), demonstrating H₇'s {abs((k_2020_validated - k_2020_six) / k_2020_six * 100):.2f}% contribution.

## Visualization

**Figure**: {figure_path}

**Caption**: Impact of validated H₇ on K(t) Index (1996-2020). (A) Comparison of
six-harmony K(t) (H₁-H₆), seven-harmony K(t) with synthetic H₇ (HYDE-based), and
seven-harmony K(t) with validated H₇ (World Bank empirical measures). (B) H₇
component comparison showing validated empirical measures vs synthetic demographic
proxies. (C) Year-by-year difference between validated and synthetic formulations,
with mean difference indicated. (D) Summary statistics for all formulations
across the validation period.

## Data Availability

**File**: data/processed/K_index_validated_h7_integration_1996_2020.csv

**Columns**:
- year: Year (1996-2020)
- h1-h6: Individual harmony components
- h7: Synthetic H₇ (HYDE-based)
- h7_validated: Validated H₇ (World Bank empirical)
- k_six_harmony: Six-harmony K(t) formulation
- k_seven_synthetic: Seven-harmony K(t) with synthetic H₇
- k_seven_validated: Seven-harmony K(t) with validated H₇
- diff_*: Difference calculations

================================================================================
✨ Validated H₇ integration complete - Ready for manuscript incorporation
================================================================================
"""

    # Save report
    output_dir = Path('/srv/luminous-dynamics/historical-k-index/manuscript')
    report_path = output_dir / 'K_INDEX_VALIDATED_H7_INTEGRATION_RESULTS.md'

    with open(report_path, 'w') as f:
        f.write(report)

    print(f"✓ Saved manuscript update: {report_path}")
    print()

    return str(report_path)

def save_integration_data(df):
    """Save integrated K(t) data with all formulations."""

    print("=" * 80)
    print("Saving Integration Data")
    print("=" * 80)
    print()

    # Select and order columns
    output_cols = [
        'year',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'h7', 'h7_validated',
        'k_six_harmony', 'k_seven_synthetic', 'k_seven_validated',
        'diff_synthetic_vs_six', 'diff_validated_vs_six', 'diff_validated_vs_synthetic'
    ]

    df_output = df[output_cols].copy()

    # Save CSV
    output_dir = Path('/srv/luminous-dynamics/historical-k-index/data/processed')
    output_path = output_dir / 'K_index_validated_h7_integration_1996_2020.csv'

    df_output.to_csv(output_path, index=False, float_format='%.8f')

    print(f"✓ Saved: {output_path}")
    print(f"  Years: {len(df_output)} ({df_output['year'].min()}-{df_output['year'].max()})")
    print(f"  Columns: {len(output_cols)}")
    print()

    return str(output_path)

def main():
    """Main execution function."""

    print()
    print("=" * 80)
    print("INTEGRATE VALIDATED H₇ WITH HISTORICAL K(t) INDEX")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()

    try:
        # Load data
        k_existing = load_existing_k_index()
        h7_validated = load_validated_h7()

        # Integrate and compare
        integrated = integrate_and_compare(k_existing, h7_validated)

        # Analyze differences
        analyzed = analyze_differences(integrated)

        # Create visualizations
        figure_path = create_visualizations(analyzed)

        # Generate manuscript update
        report_path = generate_manuscript_update(analyzed, figure_path)

        # Save integration data
        data_path = save_integration_data(analyzed)

        # Final summary
        print("=" * 80)
        print("✅ INTEGRATION COMPLETE")
        print("=" * 80)
        print()
        print("Deliverables:")
        print(f"  1. Visualization: {figure_path}")
        print(f"  2. Manuscript update: {report_path}")
        print(f"  3. Integration data: {data_path}")
        print()
        print("Next steps:")
        print("  1. Review visualization and manuscript text")
        print("  2. Insert K(t) findings into manuscript Results section")
        print("  3. Update figures list with K(t) comparison figure")
        print("  4. Add integration data to supplementary materials")
        print()
        print("✨ Validated H₇ successfully integrated with K(t) framework!")
        print("=" * 80)
        print()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
