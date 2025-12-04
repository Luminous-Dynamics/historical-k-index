#!/usr/bin/env python3
"""
Process Infrastructure Component for H₇ (Evolutionary Progression)

This script processes raw infrastructure indicator data into a normalized component
for the H₇ harmony. Infrastructure represents physical and digital connectivity
that enables civilizational development.

Methodology:
- Combine multiple infrastructure indicators into composite index
- Each indicator weighted by importance to development
- Normalize to [0, 1] scale using min-max normalization
- Handle missing data gracefully with weight renormalization

Indicators and Weights:
1. Access to electricity (35%) - Foundational infrastructure
2. Mobile cellular subscriptions (20%) - Communication infrastructure
3. Internet usage (25%) - Digital infrastructure
4. Rail lines (10%) - Physical transport
5. Roads total network (10%) - Physical transport

Data Sources:
- World Bank infrastructure indicators (1960-2023)

Output:
- Normalized infrastructure component in [0, 1] scale
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
from typing import Dict, Optional
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_RAW = PROJECT_ROOT / "data" / "raw" / "worldbank_supplementary"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed" / "H7_components"
FIGURES_DIR = PROJECT_ROOT / "figures"

# World Bank indicator codes and weights
INFRASTRUCTURE_INDICATORS = {
    'EG.ELC.ACCS.ZS': {
        'name': 'Access to electricity',
        'weight': 0.35,
        'max_value': 100,  # Percentage
        'unit': '%'
    },
    'IT.CEL.SETS.P2': {
        'name': 'Mobile cellular subscriptions',
        'weight': 0.20,
        'max_value': 200,  # Per 100 people (can exceed 100)
        'unit': 'per 100'
    },
    'IT.NET.USER.ZS': {
        'name': 'Internet usage',
        'weight': 0.25,
        'max_value': 100,  # Percentage
        'unit': '%'
    },
    'IS.RRS.TOTL.KM': {
        'name': 'Rail lines',
        'weight': 0.10,
        'max_value': None,  # Will calculate from data
        'unit': 'km'
    },
    'IS.ROD.TOTL.KM': {
        'name': 'Roads, total network',
        'weight': 0.10,
        'max_value': None,  # Will calculate from data
        'unit': 'km'
    }
}

# Create output directories
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_infrastructure_data() -> pd.DataFrame:
    """Load raw infrastructure data from World Bank."""
    logger.info("Loading infrastructure data...")

    infra_file = DATA_RAW / "worldbank_infrastructure.csv"

    if not infra_file.exists():
        raise FileNotFoundError(f"Infrastructure data not found: {infra_file}")

    df = pd.read_csv(infra_file)
    logger.info(f"Loaded {len(df)} infrastructure indicator records")
    logger.info(f"Indicators: {df['indicator_code'].nunique()}")
    logger.info(f"Countries: {df['country_code'].nunique()}")
    logger.info(f"Year range: {df['year'].min()} - {df['year'].max()}")

    return df


def normalize_indicator(df: pd.DataFrame,
                        indicator_code: str,
                        config: Dict) -> pd.DataFrame:
    """
    Normalize a single infrastructure indicator to [0, 1] scale.

    Args:
        df: DataFrame containing the indicator data
        indicator_code: World Bank indicator code
        config: Configuration dict with normalization parameters

    Returns:
        DataFrame with normalized values
    """
    indicator_name = config['name']
    logger.info(f"Normalizing: {indicator_name}")

    # Filter to this indicator
    indicator_data = df[df['indicator_code'] == indicator_code].copy()

    if len(indicator_data) == 0:
        logger.warning(f"No data found for {indicator_name}")
        return pd.DataFrame()

    # Determine normalization approach based on max_value
    if config['max_value'] is not None:
        # Known maximum (percentages, per capita measures)
        max_val = config['max_value']
        indicator_data['normalized'] = indicator_data['value'] / max_val
        # Clip to [0, 1] in case of values exceeding expected max
        indicator_data['normalized'] = indicator_data['normalized'].clip(0, 1)
    else:
        # Unknown maximum (absolute measures like km of rail/roads)
        # Use min-max normalization
        min_val = indicator_data['value'].min()
        max_val = indicator_data['value'].max()
        indicator_data['normalized'] = (
            (indicator_data['value'] - min_val) / (max_val - min_val)
        )

    logger.info(f"  Records: {len(indicator_data)}")
    logger.info(f"  Normalized range: {indicator_data['normalized'].min():.4f} - {indicator_data['normalized'].max():.4f}")
    logger.info(f"  Missing: {indicator_data['value'].isna().sum()}")

    return indicator_data[['country_code', 'country_name', 'year', 'normalized']]


def create_infrastructure_composite(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create composite infrastructure index from multiple indicators.

    Combines all infrastructure indicators using weighted average,
    with graceful handling of missing data.
    """
    logger.info("Creating infrastructure composite index...")

    all_normalized = {}

    # Normalize each indicator
    for indicator_code, config in INFRASTRUCTURE_INDICATORS.items():
        normalized = normalize_indicator(df, indicator_code, config)
        if len(normalized) > 0:
            # Rename normalized column to indicator-specific name
            indicator_key = config['name'].lower().replace(' ', '_').replace(',', '')
            normalized = normalized.rename(columns={'normalized': indicator_key})
            all_normalized[indicator_code] = (normalized, config['weight'])

    if not all_normalized:
        raise ValueError("No indicators could be normalized")

    # Merge all normalized indicators
    logger.info("Merging normalized indicators...")

    # Start with first indicator
    first_code = list(all_normalized.keys())[0]
    merged = all_normalized[first_code][0].copy()

    # Merge remaining indicators
    for indicator_code, (normalized_df, weight) in list(all_normalized.items())[1:]:
        indicator_key = list(normalized_df.columns)[-1]  # Get the normalized column name
        merged = merged.merge(
            normalized_df,
            on=['country_code', 'country_name', 'year'],
            how='outer',
            suffixes=('', f'_{indicator_code}')
        )

    logger.info(f"Merged data: {len(merged)} country-year observations")

    # Calculate weighted composite
    logger.info("Calculating weighted composite...")

    # Get column names for normalized indicators
    indicator_columns = []
    for code, config in INFRASTRUCTURE_INDICATORS.items():
        col_name = config['name'].lower().replace(' ', '_').replace(',', '')
        if col_name in merged.columns:
            indicator_columns.append(col_name)

    # Calculate weighted sum with graceful handling of missing data
    weighted_values = []
    total_weights = []

    for col_name in indicator_columns:
        # Find corresponding weight
        weight = next(
            config['weight']
            for config in INFRASTRUCTURE_INDICATORS.values()
            if config['name'].lower().replace(' ', '_').replace(',', '') == col_name
        )

        # Multiply by weight, handling NaN gracefully
        weighted_col = merged[col_name] * weight
        weighted_values.append(weighted_col.fillna(0))

        # Track valid weights (1 where data exists, 0 where missing)
        valid_weight = (~merged[col_name].isna()).astype(float) * weight
        total_weights.append(valid_weight)

    # Sum weighted values and total valid weights
    weighted_sum = sum(weighted_values)
    total_weight = sum(total_weights)

    # Calculate normalized composite (dividing by actual total weight)
    # This ensures we use available data even when some indicators are missing
    merged['infrastructure_component'] = np.where(
        total_weight > 0,
        weighted_sum / total_weight,
        np.nan
    )

    # Validate
    assert merged['infrastructure_component'].min() >= 0 or merged['infrastructure_component'].isna().all(), \
        "Composite values < 0"
    assert merged['infrastructure_component'].max() <= 1 or merged['infrastructure_component'].isna().all(), \
        "Composite values > 1"

    logger.info(f"Composite range: {merged['infrastructure_component'].min():.4f} - {merged['infrastructure_component'].max():.4f}")
    logger.info(f"Valid observations: {merged['infrastructure_component'].notna().sum()}")

    return merged


def create_global_trend_visualization(df: pd.DataFrame):
    """Create visualization of global infrastructure component evolution."""
    logger.info("Creating global trend visualization...")

    # Calculate global average by year
    yearly_avg = df.groupby('year')['infrastructure_component'].mean().reset_index()

    plt.figure(figsize=(12, 7))
    plt.plot(yearly_avg['year'], yearly_avg['infrastructure_component'],
             linewidth=2.5, marker='o', markersize=4, color='#7209B7')

    plt.title('Global Infrastructure Component Evolution\n(Physical & Digital Connectivity)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year', fontsize=13)
    plt.ylabel('Infrastructure Component (0-1)', fontsize=13)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.ylim(0, 1.0)

    # Add contextual annotations
    if len(yearly_avg) > 0:
        first_val = yearly_avg.iloc[0]['infrastructure_component']
        last_val = yearly_avg.iloc[-1]['infrastructure_component']
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
    output_file = FIGURES_DIR / "infrastructure_global_trend.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved global trend visualization: {output_file}")


def create_top_bottom_countries_visualization(df: pd.DataFrame):
    """Create visualization comparing top and bottom countries."""
    logger.info("Creating top/bottom countries visualization...")

    # Get most recent year data
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year].dropna(subset=['infrastructure_component'])

    # Get top 10 and bottom 10 countries
    top_10 = latest_data.nlargest(10, 'infrastructure_component')
    bottom_10 = latest_data.nsmallest(10, 'infrastructure_component')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Top 10 countries
    ax1.barh(range(len(top_10)), top_10['infrastructure_component'], color='#06A77D')
    ax1.set_yticks(range(len(top_10)))
    ax1.set_yticklabels(top_10['country_name'], fontsize=10)
    ax1.set_xlabel('Infrastructure Component (0-1)', fontsize=11)
    ax1.set_title(f'Top 10 Countries - Infrastructure ({latest_year:.0f})',
                  fontsize=13, fontweight='bold')
    ax1.set_xlim(0, 1.0)
    ax1.grid(axis='x', alpha=0.3)
    ax1.invert_yaxis()

    # Bottom 10 countries
    ax2.barh(range(len(bottom_10)), bottom_10['infrastructure_component'], color='#D74E09')
    ax2.set_yticks(range(len(bottom_10)))
    ax2.set_yticklabels(bottom_10['country_name'], fontsize=10)
    ax2.set_xlabel('Infrastructure Component (0-1)', fontsize=11)
    ax2.set_title(f'Bottom 10 Countries - Infrastructure ({latest_year:.0f})',
                  fontsize=13, fontweight='bold')
    ax2.set_xlim(0, 1.0)
    ax2.grid(axis='x', alpha=0.3)
    ax2.invert_yaxis()

    plt.suptitle('Infrastructure Component: Connectivity Leaders and Challengers',
                 fontsize=15, fontweight='bold', y=1.00)
    plt.tight_layout()

    output_file = FIGURES_DIR / "infrastructure_top_bottom_countries.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved top/bottom countries visualization: {output_file}")


def create_distribution_evolution_visualization(df: pd.DataFrame):
    """Create visualization showing how the distribution evolves over time."""
    logger.info("Creating distribution evolution visualization...")

    # Select key years for comparison
    years = sorted(df['year'].unique())
    if len(years) > 5:
        selected_years = [
            years[0],  # First year
            years[len(years)//4],  # 25%
            years[len(years)//2],  # 50%
            years[3*len(years)//4],  # 75%
            years[-1]  # Last year
        ]
    else:
        selected_years = years

    plt.figure(figsize=(14, 8))

    for year in selected_years:
        year_data = df[df['year'] == year]['infrastructure_component'].dropna()
        if len(year_data) > 10:  # Only plot if sufficient data
            plt.hist(year_data, bins=30, alpha=0.5, label=f'{year:.0f}', density=True)

    plt.title('Evolution of Global Infrastructure Distribution\n(Infrastructure Component Across Countries)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Infrastructure Component (0-1)', fontsize=13)
    plt.ylabel('Density', fontsize=13)
    plt.legend(title='Year', fontsize=11)
    plt.grid(True, alpha=0.3, axis='y')
    plt.xlim(0, 1.0)

    plt.tight_layout()
    output_file = FIGURES_DIR / "infrastructure_distribution_evolution.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    logger.info(f"Saved distribution evolution visualization: {output_file}")


def generate_summary_statistics(df: pd.DataFrame) -> str:
    """Generate comprehensive summary statistics."""
    logger.info("Generating summary statistics...")

    summary = []
    summary.append("=" * 80)
    summary.append("INFRASTRUCTURE COMPONENT PROCESSING SUMMARY")
    summary.append("=" * 80)
    summary.append("")

    # Basic statistics
    valid_obs = df['infrastructure_component'].notna()
    summary.append("📊 Dataset Overview:")
    summary.append(f"  Total observations: {len(df):,}")
    summary.append(f"  Valid observations: {valid_obs.sum():,}")
    summary.append(f"  Countries: {df['country_code'].nunique()}")
    summary.append(f"  Year range: {df['year'].min():.0f} - {df['year'].max():.0f}")
    summary.append(f"  Years covered: {df['year'].nunique()}")
    summary.append("")

    # Component statistics
    summary.append("📈 Infrastructure Component Statistics:")
    valid_data = df.loc[valid_obs, 'infrastructure_component']
    summary.append(f"  Mean: {valid_data.mean():.4f}")
    summary.append(f"  Median: {valid_data.median():.4f}")
    summary.append(f"  Std Dev: {valid_data.std():.4f}")
    summary.append(f"  Min: {valid_data.min():.4f}")
    summary.append(f"  Max: {valid_data.max():.4f}")
    summary.append("")

    # Temporal trends
    summary.append("🌍 Global Trends:")
    yearly_avg = df.groupby('year')['infrastructure_component'].mean()
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
    latest_data = df[df['year'] == latest_year].dropna(subset=['infrastructure_component'])
    top_5 = latest_data.nlargest(5, 'infrastructure_component')
    for idx, row in top_5.iterrows():
        summary.append(f"  {row['country_name']:<40} {row['infrastructure_component']:.4f}")
    summary.append("")

    # Data quality
    summary.append("✅ Data Quality:")
    missing_pct = ((~valid_obs).sum() / len(df)) * 100
    summary.append(f"  Missing values: {(~valid_obs).sum()} ({missing_pct:.2f}%)")
    summary.append(f"  Coverage: {valid_obs.sum():,} observations")
    summary.append("")

    summary.append("=" * 80)
    summary.append("✨ Infrastructure component processing complete!")
    summary.append("=" * 80)

    return "\n".join(summary)


def main():
    """Main processing pipeline for infrastructure component."""
    logger.info("Starting infrastructure component processing...")
    logger.info("=" * 80)

    try:
        # Load data
        raw_df = load_infrastructure_data()

        # Create composite
        composite_df = create_infrastructure_composite(raw_df)

        # Create visualizations
        create_global_trend_visualization(composite_df)
        create_top_bottom_countries_visualization(composite_df)
        create_distribution_evolution_visualization(composite_df)

        # Save processed data
        output_columns = ['country_code', 'country_name', 'year', 'infrastructure_component']
        output_df = composite_df[output_columns].copy()

        output_file = DATA_PROCESSED / "infrastructure_component.csv"
        output_df.to_csv(output_file, index=False)
        logger.info(f"Saved processed data: {output_file}")

        # Generate and display summary
        summary = generate_summary_statistics(composite_df)
        print("\n" + summary)

        # Save summary to file
        summary_file = FIGURES_DIR / "infrastructure_summary_stats.txt"
        with open(summary_file, 'w') as f:
            f.write(summary)
        logger.info(f"Saved summary statistics: {summary_file}")

        logger.info("=" * 80)
        logger.info("✅ Infrastructure component processing completed successfully!")

        return composite_df

    except Exception as e:
        logger.error(f"Error processing infrastructure component: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    result = main()
