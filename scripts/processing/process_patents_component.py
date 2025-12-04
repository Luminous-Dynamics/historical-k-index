#!/usr/bin/env python3
"""
Process Patents Component for H₇ (Evolutionary Progression)

This script processes raw patent data into a normalized component for the H₇ harmony.
Patents are a key indicator of innovation capacity and technological advancement.

Methodology:
- Use total patents (resident + non-resident) as primary measure
- Normalize per capita to account for population differences
- Scale to [0, 1] using min-max normalization
- Handle missing data gracefully

Data Sources:
- World Bank patent data (1980-2021)
- World Bank population data for normalization

Output:
- Normalized patents component in [0, 1] scale
- Visualizations showing global trends and country comparisons
- Summary statistics

Author: Historical K(t) Index Project
Date: December 3, 2025
License: CC-BY-4.0
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Tuple
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed" / "H7_components"
FIGURES_DIR = PROJECT_ROOT / "figures"

# World Bank indicator codes
POPULATION_INDICATOR = "SP.POP.TOTL"  # Total population

# Create output directories
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_patent_data() -> pd.DataFrame:
    """Load processed patent data from World Bank."""
    logger.info("Loading patent data...")

    patents_file = DATA_RAW / "wipo" / "worldbank_patents_combined.csv"

    if not patents_file.exists():
        raise FileNotFoundError(f"Patent data not found: {patents_file}")

    df = pd.read_csv(patents_file)
    logger.info(f"Loaded {len(df)} patent records")
    logger.info(f"Countries: {df['country_code'].nunique()}")
    logger.info(f"Year range: {df['year'].min()} - {df['year'].max()}")

    return df


def load_population_data() -> pd.DataFrame:
    """Load population data from World Bank for normalization."""
    logger.info("Loading population data for normalization...")

    # Try to find population data in supplementary files
    pop_file = DATA_RAW / "worldbank_supplementary" / "worldbank_population.csv"

    if pop_file.exists():
        df = pd.read_csv(pop_file)
        logger.info(f"Loaded {len(df)} population records")
        return df
    else:
        logger.warning("Population data not found - will skip per-capita normalization")
        return None


def calculate_patents_per_capita(patents_df: pd.DataFrame,
                                  population_df: Optional[pd.DataFrame]) -> pd.DataFrame:
    """
    Calculate patents per capita (per 1 million population).

    If population data is not available, return total patents only.
    """
    if population_df is None:
        logger.info("Using total patents (population data unavailable)")
        result = patents_df.copy()
        result['patents_per_capita'] = result['total']
        return result

    logger.info("Calculating patents per capita...")

    # Merge patent and population data
    merged = patents_df.merge(
        population_df[['country_code', 'year', 'value']],
        on=['country_code', 'year'],
        how='left',
        suffixes=('', '_pop')
    )

    # Calculate per capita (per 1 million people)
    merged['patents_per_capita'] = (
        merged['total'] / (merged['value'] / 1_000_000)
    )

    # Handle missing population data
    missing_pop = merged['value'].isna().sum()
    if missing_pop > 0:
        logger.warning(f"{missing_pop} records missing population data")
        # For records without population, use total patents as fallback
        merged.loc[merged['value'].isna(), 'patents_per_capita'] = merged.loc[merged['value'].isna(), 'total']

    logger.info(f"Calculated patents per capita for {len(merged)} records")

    return merged


def normalize_patents_component(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize patents data to [0, 1] scale.

    Uses min-max normalization after log transformation to handle
    the highly skewed distribution of patent counts.
    """
    logger.info("Normalizing patents component...")

    result = df.copy()

    # Log transformation to handle skewed distribution
    # Add 1 to avoid log(0)
    result['patents_log'] = np.log1p(result['patents_per_capita'])

    # Calculate min and max for normalization
    min_val = result['patents_log'].min()
    max_val = result['patents_log'].max()

    logger.info(f"Patents per capita range (log): {min_val:.4f} - {max_val:.4f}")

    # Normalize to [0, 1]
    result['patents_component'] = (
        (result['patents_log'] - min_val) / (max_val - min_val)
    )

    # Validate normalization
    assert result['patents_component'].min() >= 0, "Normalization failed: values < 0"
    assert result['patents_component'].max() <= 1, "Normalization failed: values > 1"

    logger.info(f"Normalized component range: {result['patents_component'].min():.4f} - {result['patents_component'].max():.4f}")

    return result


def create_global_trend_visualization(df: pd.DataFrame):
    """Create visualization of global patents component evolution."""
    logger.info("Creating global trend visualization...")

    # Calculate global average (weighted by population if available)
    yearly_avg = df.groupby('year')['patents_component'].mean().reset_index()

    plt.figure(figsize=(12, 7))
    plt.plot(yearly_avg['year'], yearly_avg['patents_component'],
             linewidth=2.5, marker='o', markersize=4, color='#2E86AB')

    plt.title('Global Patents Component Evolution\n(Innovation Capacity Measure)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=13)
    plt.ylabel('Patents Component (0-1)', fontsize=13)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.ylim(0, 1.0)

    # Add contextual annotations
    if len(yearly_avg) > 0:
        first_val = yearly_avg.iloc[0]['patents_component']
        last_val = yearly_avg.iloc[-1]['patents_component']
        improvement = ((last_val - first_val) / first_val) * 100

        plt.text(0.02, 0.98,
                f"Improvement: {improvement:+.1f}%\n"
                f"{yearly_avg.iloc[0]['year']:.0f}: {first_val:.3f}\n"
                f"{yearly_avg.iloc[-1]['year']:.0f}: {last_val:.3f}",
                transform=plt.gca().transAxes,
                fontsize=11,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

    plt.tight_layout()
    output_file = FIGURES_DIR / "patents_global_trend.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved global trend visualization: {output_file}")


def create_top_bottom_countries_visualization(df: pd.DataFrame):
    """Create visualization comparing top and bottom countries."""
    logger.info("Creating top/bottom countries visualization...")

    # Get most recent year data
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year].copy()

    # Get top 10 and bottom 10 countries
    top_10 = latest_data.nlargest(10, 'patents_component')
    bottom_10 = latest_data.nsmallest(10, 'patents_component')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Top 10 countries
    ax1.barh(range(len(top_10)), top_10['patents_component'], color='#06A77D')
    ax1.set_yticks(range(len(top_10)))
    ax1.set_yticklabels(top_10['country_name'], fontsize=10)
    ax1.set_xlabel('Patents Component (0-1)', fontsize=11)
    ax1.set_title(f'Top 10 Countries - Innovation Capacity ({latest_year:.0f})',
                  fontsize=13, fontweight='bold')
    ax1.set_xlim(0, 1.0)
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()

    # Bottom 10 countries
    ax2.barh(range(len(bottom_10)), bottom_10['patents_component'], color='#D74E09')
    ax2.set_yticks(range(len(bottom_10)))
    ax2.set_yticklabels(bottom_10['country_name'], fontsize=10)
    ax2.set_xlabel('Patents Component (0-1)', fontsize=11)
    ax2.set_title(f'Bottom 10 Countries - Innovation Capacity ({latest_year:.0f})',
                  fontsize=13, fontweight='bold')
    ax2.set_xlim(0, 1.0)
    ax2.grid(axis='x', alpha=0.3)
    ax2.invert_yaxis()

    plt.suptitle('Patents Component: Global Innovation Leaders and Challengers',
                 fontsize=15, fontweight='bold', y=1.00)
    plt.tight_layout()

    output_file = FIGURES_DIR / "patents_top_bottom_countries.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved top/bottom countries visualization: {output_file}")


def create_distribution_evolution_visualization(df: pd.DataFrame):
    """Create visualization showing how the distribution evolves over time."""
    logger.info("Creating distribution evolution visualization...")

    # Select key years for comparison
    years = df['year'].unique()
    if len(years) > 5:
        selected_years = [
            years[0],  # First year
            years[len(years)//4],  # 25%
            years[len(years)//2],  # 50%
            years[3*len(years)//4],  # 75%
            years[-1]  # Last year
        ]
    else:
        selected_years = sorted(years)

    plt.figure(figsize=(14, 8))

    for year in selected_years:
        year_data = df[df['year'] == year]['patents_component'].dropna()
        if len(year_data) > 0:
            plt.hist(year_data, bins=30, alpha=0.5, label=f'{year:.0f}', density=True)

    plt.title('Evolution of Global Innovation Distribution\n(Patents Component Across Countries)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Patents Component (0-1)', fontsize=13)
    plt.ylabel('Density', fontsize=13)
    plt.legend(title='Year', fontsize=11)
    plt.grid(True, alpha=0.3, axis='y')
    plt.xlim(0, 1.0)

    plt.tight_layout()
    output_file = FIGURES_DIR / "patents_distribution_evolution.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved distribution evolution visualization: {output_file}")


def generate_summary_statistics(df: pd.DataFrame) -> str:
    """Generate comprehensive summary statistics."""
    logger.info("Generating summary statistics...")

    summary = []
    summary.append("=" * 80)
    summary.append("PATENTS COMPONENT PROCESSING SUMMARY")
    summary.append("=" * 80)
    summary.append("")

    # Basic statistics
    summary.append("📊 Dataset Overview:")
    summary.append(f"  Total observations: {len(df):,}")
    summary.append(f"  Countries: {df['country_code'].nunique()}")
    summary.append(f"  Year range: {df['year'].min():.0f} - {df['year'].max():.0f}")
    summary.append(f"  Years covered: {df['year'].nunique()}")
    summary.append("")

    # Component statistics
    summary.append("📈 Patents Component Statistics:")
    summary.append(f"  Mean: {df['patents_component'].mean():.4f}")
    summary.append(f"  Median: {df['patents_component'].median():.4f}")
    summary.append(f"  Std Dev: {df['patents_component'].std():.4f}")
    summary.append(f"  Min: {df['patents_component'].min():.4f}")
    summary.append(f"  Max: {df['patents_component'].max():.4f}")
    summary.append("")

    # Temporal trends
    summary.append("🌍 Global Trends:")
    yearly_avg = df.groupby('year')['patents_component'].mean()
    first_year = yearly_avg.index[0]
    last_year = yearly_avg.index[-1]
    first_val = yearly_avg.iloc[0]
    last_val = yearly_avg.iloc[-1]
    improvement = ((last_val - first_val) / first_val) * 100

    summary.append(f"  {first_year:.0f}: {first_val:.4f}")
    summary.append(f"  {last_year:.0f}: {last_val:.4f}")
    summary.append(f"  Change: {improvement:+.1f}%")
    summary.append("")

    # Top performers
    summary.append("🏆 Top 5 Countries (Most Recent Year):")
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year].nlargest(5, 'patents_component')
    for idx, row in latest_data.iterrows():
        summary.append(f"  {row['country_name']:<40} {row['patents_component']:.4f}")
    summary.append("")

    # Data quality
    summary.append("✅ Data Quality:")
    missing_pct = (df['patents_component'].isna().sum() / len(df)) * 100
    summary.append(f"  Missing values: {df['patents_component'].isna().sum()} ({missing_pct:.2f}%)")
    summary.append(f"  Valid observations: {df['patents_component'].notna().sum():,}")
    summary.append("")

    summary.append("=" * 80)
    summary.append("✨ Patents component processing complete!")
    summary.append("=" * 80)

    return "\n".join(summary)


def main():
    """Main processing pipeline for patents component."""
    logger.info("Starting patents component processing...")
    logger.info("=" * 80)

    try:
        # Load data
        patents_df = load_patent_data()
        population_df = load_population_data()

        # Calculate per capita
        patents_per_capita = calculate_patents_per_capita(patents_df, population_df)

        # Normalize component
        normalized_df = normalize_patents_component(patents_per_capita)

        # Create visualizations
        create_global_trend_visualization(normalized_df)
        create_top_bottom_countries_visualization(normalized_df)
        create_distribution_evolution_visualization(normalized_df)

        # Save processed data
        output_columns = [
            'country_code', 'country_name', 'year',
            'resident', 'nonresident', 'total',
            'patents_per_capita', 'patents_component'
        ]

        # Only include columns that exist
        available_columns = [col for col in output_columns if col in normalized_df.columns]
        output_df = normalized_df[available_columns].copy()

        output_file = DATA_PROCESSED / "patents_component.csv"
        output_df.to_csv(output_file, index=False)
        logger.info(f"Saved processed data: {output_file}")

        # Generate and display summary
        summary = generate_summary_statistics(normalized_df)
        print("\n" + summary)

        # Save summary to file
        summary_file = FIGURES_DIR / "patents_summary_stats.txt"
        with open(summary_file, 'w') as f:
            f.write(summary)
        logger.info(f"Saved summary statistics: {summary_file}")

        logger.info("=" * 80)
        logger.info("✅ Patents component processing completed successfully!")

        return normalized_df

    except Exception as e:
        logger.error(f"Error processing patents component: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    result = main()
