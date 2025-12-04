#!/usr/bin/env python3
"""
Integrate H₇ Components into Final Composite

This script combines all four processed H₇ components (education, patents,
infrastructure, governance) into the final H₇ (Evolutionary Progression) measure
for the Historical K(t) Index.

Methodology:
- Use geometric mean to combine components (penalizes imbalances)
- H₇ = (Education × Patents × Infrastructure × Governance)^(1/4)
- Only include country-years where all components are available
- Validate temporal consistency and construct validity

Components:
1. Education (16,592 obs, 1960-2023)
2. Patents (4,663 obs, 1980-2021)
3. Infrastructure (14,001 obs, 1960-2023)
4. Governance (5,083 obs, 1996-2023)

Expected Coverage:
- Full overlap: 1996-2021 (limited by Governance start and Patents end)
- Partial overlap possible if components have gaps

Output:
- Final H₇ composite in [0, 1] scale
- Comprehensive visualizations
- Validation statistics
- Summary report

Author: Historical K(t) Index Project
Date: December 3, 2025
License: CC-BY-4.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed" / "H7_components"
DATA_FINAL = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"

# Create output directories
DATA_FINAL.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_all_components() -> dict:
    """Load all four processed H₇ components."""
    logger.info("Loading all H₇ components...")

    components = {}

    # Education component
    edu_file = DATA_PROCESSED / "education_component.csv"
    components['education'] = pd.read_csv(edu_file)
    logger.info(f"  Education: {len(components['education'])} observations")

    # Patents component
    patents_file = DATA_PROCESSED / "patents_component.csv"
    components['patents'] = pd.read_csv(patents_file)
    logger.info(f"  Patents: {len(components['patents'])} observations")

    # Infrastructure component
    infra_file = DATA_PROCESSED / "infrastructure_component.csv"
    components['infrastructure'] = pd.read_csv(infra_file)
    logger.info(f"  Infrastructure: {len(components['infrastructure'])} observations")

    # Governance component
    gov_file = DATA_PROCESSED / "governance_component.csv"
    components['governance'] = pd.read_csv(gov_file)
    logger.info(f"  Governance: {len(components['governance'])} observations")

    return components


def integrate_components(components: dict) -> pd.DataFrame:
    """
    Integrate all components using geometric mean.

    Geometric mean is appropriate because:
    1. It's multiplicative (components interact)
    2. Penalizes imbalances (can't compensate weak governance with strong education)
    3. Standard for composite indices
    """
    logger.info("Integrating components via geometric mean...")

    # Start with education (largest coverage)
    merged = components['education'][['country_code', 'country_name', 'year', 'education_component']].copy()

    # Merge patents
    merged = merged.merge(
        components['patents'][['country_code', 'year', 'patents_component']],
        on=['country_code', 'year'],
        how='inner'  # Only keep where both exist
    )

    # Merge infrastructure
    merged = merged.merge(
        components['infrastructure'][['country_code', 'year', 'infrastructure_component']],
        on=['country_code', 'year'],
        how='inner'
    )

    # Merge governance
    merged = merged.merge(
        components['governance'][['country_code', 'year', 'governance_component']],
        on=['country_code', 'year'],
        how='inner'
    )

    logger.info(f"Merged data: {len(merged)} country-year observations")
    logger.info(f"Countries: {merged['country_code'].nunique()}")
    logger.info(f"Year range: {merged['year'].min():.0f} - {merged['year'].max():.0f}")

    # Calculate geometric mean: (a × b × c × d)^(1/4)
    merged['H7_evolutionary_progression'] = (
        merged['education_component'] *
        merged['patents_component'] *
        merged['infrastructure_component'] *
        merged['governance_component']
    ) ** 0.25

    # Validate
    assert merged['H7_evolutionary_progression'].min() >= 0, "H₇ values < 0"
    assert merged['H7_evolutionary_progression'].max() <= 1, "H₇ values > 1"

    logger.info(f"H₇ range: {merged['H7_evolutionary_progression'].min():.4f} - {merged['H7_evolutionary_progression'].max():.4f}")

    return merged


def create_global_trend_visualization(df: pd.DataFrame):
    """Create visualization of global H₇ evolution."""
    logger.info("Creating global H₇ trend visualization...")

    # Calculate global average by year
    yearly_avg = df.groupby('year')['H7_evolutionary_progression'].mean().reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # Left: Time series
    ax1.plot(yearly_avg['year'], yearly_avg['H7_evolutionary_progression'],
             linewidth=3, marker='o', markersize=5, color='#9D4EDD', label='H₇ Composite')
    ax1.set_title('Global H₇ (Evolutionary Progression) Evolution',
                  fontsize=14, fontweight='bold')
    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('H₇ Component (0-1)', fontsize=12)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_ylim(0, 1.0)
    ax1.legend(fontsize=11)

    # Add statistics
    first_val = yearly_avg.iloc[0]['H7_evolutionary_progression']
    last_val = yearly_avg.iloc[-1]['H7_evolutionary_progression']
    improvement = ((last_val - first_val) / first_val) * 100

    ax1.text(0.02, 0.98,
            f"Improvement: {improvement:+.1f}%\n"
            f"{yearly_avg.iloc[0]['year']:.0f}: {first_val:.3f}\n"
            f"{yearly_avg.iloc[-1]['year']:.0f}: {last_val:.3f}",
            transform=ax1.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

    # Right: Component breakdown (most recent year)
    latest_year = df['year'].max()
    latest = df[df['year'] == latest_year]

    components = ['Education', 'Patents', 'Infrastructure', 'Governance', 'H₇ Composite']
    values = [
        latest['education_component'].mean(),
        latest['patents_component'].mean(),
        latest['infrastructure_component'].mean(),
        latest['governance_component'].mean(),
        latest['H7_evolutionary_progression'].mean()
    ]
    colors = ['#06A77D', '#2E86AB', '#7209B7', '#560BAD', '#9D4EDD']

    bars = ax2.barh(components, values, color=colors)
    ax2.set_xlabel('Component Value (0-1)', fontsize=12)
    ax2.set_title(f'H₇ Component Breakdown ({latest_year:.0f})',
                  fontsize=14, fontweight='bold')
    ax2.set_xlim(0, 1.0)
    ax2.grid(axis='x', alpha=0.3)

    # Add value labels
    for bar, val in zip(bars, values):
        ax2.text(val + 0.02, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}',
                va='center', fontsize=10)

    plt.suptitle('H₇ (Evolutionary Progression): Civilizational Advancement Measure',
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()

    output_file = FIGURES_DIR / "H7_global_evolution.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved global H₇ visualization: {output_file}")


def create_country_comparison_visualization(df: pd.DataFrame):
    """Create visualization comparing countries on H₇."""
    logger.info("Creating country comparison visualization...")

    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year].sort_values('H7_evolutionary_progression', ascending=False)

    # Top 15 and bottom 15
    top_15 = latest_data.head(15)
    bottom_15 = latest_data.tail(15)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))

    # Top 15
    y_pos = range(len(top_15))
    ax1.barh(y_pos, top_15['H7_evolutionary_progression'], color='#06A77D')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(top_15['country_name'], fontsize=9)
    ax1.set_xlabel('H₇ (Evolutionary Progression)', fontsize=11)
    ax1.set_title(f'Top 15 Countries - H₇ ({latest_year:.0f})',
                  fontsize=13, fontweight='bold')
    ax1.set_xlim(0, 1.0)
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()

    # Add values
    for i, (idx, row) in enumerate(top_15.iterrows()):
        ax1.text(row['H7_evolutionary_progression'] + 0.02, i,
                f"{row['H7_evolutionary_progression']:.3f}",
                va='center', fontsize=9)

    # Bottom 15
    y_pos = range(len(bottom_15))
    ax2.barh(y_pos, bottom_15['H7_evolutionary_progression'], color='#D74E09')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(bottom_15['country_name'], fontsize=9)
    ax2.set_xlabel('H₇ (Evolutionary Progression)', fontsize=11)
    ax2.set_title(f'Bottom 15 Countries - H₇ ({latest_year:.0f})',
                  fontsize=13, fontweight='bold')
    ax2.set_xlim(0, 1.0)
    ax2.grid(axis='x', alpha=0.3)
    ax2.invert_yaxis()

    # Add values
    for i, (idx, row) in enumerate(bottom_15.iterrows()):
        ax2.text(row['H7_evolutionary_progression'] + 0.02, i,
                f"{row['H7_evolutionary_progression']:.3f}",
                va='center', fontsize=9)

    plt.suptitle('H₇ Global Rankings: Evolutionary Progression Leaders and Challengers',
                 fontsize=15, fontweight='bold', y=0.995)
    plt.tight_layout()

    output_file = FIGURES_DIR / "H7_country_rankings.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved country rankings visualization: {output_file}")


def create_component_correlation_heatmap(df: pd.DataFrame):
    """Create correlation heatmap showing relationships between components."""
    logger.info("Creating component correlation heatmap...")

    components = ['education_component', 'patents_component',
                  'infrastructure_component', 'governance_component',
                  'H7_evolutionary_progression']

    # Calculate correlation matrix
    corr_matrix = df[components].corr()

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(corr_matrix, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')

    # Set ticks and labels
    labels = ['Education', 'Patents', 'Infrastructure', 'Governance', 'H₇']
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_yticklabels(labels)

    # Add correlation values
    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                          ha='center', va='center', color='black', fontsize=11)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Correlation', fontsize=11)

    plt.title('H₇ Component Correlations\n(Pearson Correlation Coefficients)',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()

    output_file = FIGURES_DIR / "H7_component_correlations.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved correlation heatmap: {output_file}")


def generate_summary_report(df: pd.DataFrame, components: dict) -> str:
    """Generate comprehensive integration report."""
    logger.info("Generating integration summary report...")

    report = []
    report.append("=" * 80)
    report.append("H₇ INTEGRATION COMPLETE - EVOLUTIONARY PROGRESSION")
    report.append("=" * 80)
    report.append("")

    # Component overview
    report.append("📊 Component Overview:")
    report.append(f"  Education: {len(components['education']):,} obs (1960-2023)")
    report.append(f"  Patents: {len(components['patents']):,} obs (1980-2021)")
    report.append(f"  Infrastructure: {len(components['infrastructure']):,} obs (1960-2023)")
    report.append(f"  Governance: {len(components['governance']):,} obs (1996-2023)")
    report.append("")

    # Integrated data
    report.append("✅ Integrated H₇ Statistics:")
    report.append(f"  Total observations: {len(df):,}")
    report.append(f"  Countries: {df['country_code'].nunique()}")
    report.append(f"  Year range: {df['year'].min():.0f} - {df['year'].max():.0f}")
    report.append(f"  Years covered: {df['year'].nunique()}")
    report.append("")

    # H₇ statistics
    report.append("📈 H₇ Component Statistics:")
    report.append(f"  Mean: {df['H7_evolutionary_progression'].mean():.4f}")
    report.append(f"  Median: {df['H7_evolutionary_progression'].median():.4f}")
    report.append(f"  Std Dev: {df['H7_evolutionary_progression'].std():.4f}")
    report.append(f"  Min: {df['H7_evolutionary_progression'].min():.4f}")
    report.append(f"  Max: {df['H7_evolutionary_progression'].max():.4f}")
    report.append("")

    # Temporal evolution
    report.append("🌍 Global Temporal Evolution:")
    yearly_avg = df.groupby('year')['H7_evolutionary_progression'].mean()
    first_year = yearly_avg.index[0]
    last_year = yearly_avg.index[-1]
    first_val = yearly_avg.iloc[0]
    last_val = yearly_avg.iloc[-1]
    improvement = ((last_val - first_val) / first_val) * 100

    report.append(f"  {first_year:.0f}: {first_val:.4f}")
    report.append(f"  {last_year:.0f}: {last_val:.4f}")
    report.append(f"  Change: {improvement:+.2f}%")
    report.append("")

    # Top 10 countries
    report.append("🏆 Top 10 Countries (Most Recent Year):")
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year].nlargest(10, 'H7_evolutionary_progression')
    for idx, row in latest_data.iterrows():
        report.append(f"  {row['country_name']:<40} {row['H7_evolutionary_progression']:.4f}")
    report.append("")

    # Component correlations
    report.append("🔗 Component Correlations with H₇:")
    for comp in ['education_component', 'patents_component',
                 'infrastructure_component', 'governance_component']:
        corr = df[comp].corr(df['H7_evolutionary_progression'])
        comp_name = comp.replace('_component', '').capitalize()
        report.append(f"  {comp_name:<20} r = {corr:.3f}")
    report.append("")

    # Methodology note
    report.append("📐 Methodology:")
    report.append("  Integration method: Geometric mean")
    report.append("  Formula: H₇ = (Education × Patents × Infrastructure × Governance)^0.25")
    report.append("  Rationale: Geometric mean penalizes imbalances and reflects")
    report.append("            multiplicative interactions between dimensions")
    report.append("")

    report.append("=" * 80)
    report.append("✨ H₇ (Evolutionary Progression) integration complete!")
    report.append("   Ready for K(t) recalculation and manuscript update")
    report.append("=" * 80)

    return "\n".join(report)


def main():
    """Main integration pipeline."""
    logger.info("Starting H₇ component integration...")
    logger.info("=" * 80)

    try:
        # Load all components
        components = load_all_components()

        # Integrate into H₇
        integrated_df = integrate_components(components)

        # Create visualizations
        create_global_trend_visualization(integrated_df)
        create_country_comparison_visualization(integrated_df)
        create_component_correlation_heatmap(integrated_df)

        # Save integrated data
        output_file = DATA_FINAL / "H7_evolutionary_progression.csv"
        integrated_df.to_csv(output_file, index=False)
        logger.info(f"Saved integrated H₇ data: {output_file}")

        # Generate and display report
        report = generate_summary_report(integrated_df, components)
        print("\n" + report)

        # Save report
        report_file = DATA_FINAL / "H7_integration_report.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        logger.info(f"Saved integration report: {report_file}")

        logger.info("=" * 80)
        logger.info("✅ H₇ integration completed successfully!")

        return integrated_df

    except Exception as e:
        logger.error(f"Error during H₇ integration: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    result = main()
