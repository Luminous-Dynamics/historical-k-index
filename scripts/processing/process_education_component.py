#!/usr/bin/env python3
"""
Process Education Data into H₇ Component

Takes World Bank education indicators and creates a normalized education
component for H₇ (Evolutionary Progression) using:
- Adult literacy rate
- School enrollment (primary, secondary, tertiary)
- Mean years of schooling (Barro-Lee)

Author: Tristan Stoltz / Claude Code
Date: December 3, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
INPUT_FILE = Path("data/raw/worldbank_supplementary/worldbank_education.csv")
OUTPUT_DIR = Path("data/processed/H7_components")
FIGURES_DIR = Path("figures")

# Weights for education sub-indicators (must sum to 1.0)
WEIGHTS = {
    'literacy': 0.30,      # Adult literacy rate
    'primary': 0.20,       # Primary enrollment
    'secondary': 0.25,     # Secondary enrollment
    'tertiary': 0.15,      # Tertiary enrollment
    'years_schooling': 0.10  # Mean years of schooling
}


def load_education_data():
    """Load World Bank education indicators."""
    print(f"\nLoading education data from: {INPUT_FILE}")

    if not INPUT_FILE.exists():
        print(f"✗ File not found: {INPUT_FILE}")
        print("Run 06_download_worldbank_h7_supplementary.py first")
        return None

    df = pd.read_csv(INPUT_FILE)
    print(f"✓ Loaded {len(df)} records")
    print(f"  Indicators: {df['indicator_code'].nunique()}")
    print(f"  Countries: {df['country_code'].nunique()}")
    print(f"  Year range: {df['year'].min()} - {df['year'].max()}")

    return df


def normalize_indicator(df, indicator_code, min_val=None, max_val=None):
    """
    Normalize an indicator to [0, 1] scale.

    For percentages (literacy, enrollment), already in [0, 100] → divide by 100
    For years of schooling, use provided min/max or data min/max
    """

    indicator_data = df[df['indicator_code'] == indicator_code].copy()

    if len(indicator_data) == 0:
        print(f"  ✗ No data for {indicator_code}")
        return None

    # Check if already a percentage (0-100 range)
    if indicator_data['value'].max() <= 100 and indicator_data['value'].min() >= 0:
        # Already a percentage, normalize to [0, 1]
        indicator_data['normalized'] = indicator_data['value'] / 100.0
        print(f"  ✓ {indicator_code}: Percentage → normalized")
    else:
        # Use min-max normalization
        if min_val is None:
            min_val = indicator_data['value'].min()
        if max_val is None:
            max_val = indicator_data['value'].max()

        indicator_data['normalized'] = (indicator_data['value'] - min_val) / (max_val - min_val)
        print(f"  ✓ {indicator_code}: [{min_val:.1f}, {max_val:.1f}] → [0, 1]")

    return indicator_data[['country_code', 'country_name', 'year', 'normalized']]


def create_education_component(df):
    """Create composite education component from multiple indicators."""

    print("\n" + "="*80)
    print("Processing Education Indicators")
    print("="*80)

    # Process each indicator
    components = {}

    # 1. Literacy rate (adult, total)
    print("\n1. Adult Literacy Rate")
    literacy = normalize_indicator(df, 'SE.ADT.LITR.ZS')
    if literacy is not None:
        components['literacy'] = literacy.rename(columns={'normalized': 'literacy'})

    # 2. Primary enrollment
    print("\n2. Primary School Enrollment")
    primary = normalize_indicator(df, 'SE.PRM.ENRR')
    if primary is not None:
        # Cap at 100% (some gross enrollment rates can exceed 100%)
        primary['normalized'] = primary['normalized'].clip(upper=1.0)
        components['primary'] = primary.rename(columns={'normalized': 'primary'})

    # 3. Secondary enrollment
    print("\n3. Secondary School Enrollment")
    secondary = normalize_indicator(df, 'SE.SEC.ENRR')
    if secondary is not None:
        secondary['normalized'] = secondary['normalized'].clip(upper=1.0)
        components['secondary'] = secondary.rename(columns={'normalized': 'secondary'})

    # 4. Tertiary enrollment
    print("\n4. Tertiary Education Enrollment")
    tertiary = normalize_indicator(df, 'SE.TER.ENRR')
    if tertiary is not None:
        tertiary['normalized'] = tertiary['normalized'].clip(upper=1.0)
        components['tertiary'] = tertiary.rename(columns={'normalized': 'tertiary'})

    # 5. Mean years of schooling (Barro-Lee)
    print("\n5. Mean Years of Schooling (Barro-Lee)")
    # Assume max ~15 years (reasonable upper bound for population average)
    years_school = normalize_indicator(df, 'BAR.SCHL.15UP', min_val=0, max_val=15)
    if years_school is not None:
        components['years_schooling'] = years_school.rename(columns={'normalized': 'years_schooling'})

    if len(components) == 0:
        print("\n✗ No components successfully processed")
        return None

    # Merge all components
    print(f"\n{'='*80}")
    print("Merging Components")
    print(f"{'='*80}")

    # Start with first component
    merged = components[list(components.keys())[0]]

    # Merge others
    for name, comp in list(components.items())[1:]:
        merged = merged.merge(
            comp[['country_code', 'year', name]],
            on=['country_code', 'year'],
            how='outer'
        )

    print(f"\n✓ Merged data: {len(merged)} country-year observations")
    print(f"  Countries: {merged['country_code'].nunique()}")
    print(f"  Year range: {merged['year'].min()} - {merged['year'].max()}")

    # Calculate composite using weighted average
    print(f"\n{'='*80}")
    print("Creating Composite Education Index")
    print(f"{'='*80}")
    print("\nWeights:")
    for comp, weight in WEIGHTS.items():
        print(f"  {comp}: {weight:.0%}")

    # Calculate weighted average (only for available components)
    merged['education_component'] = 0
    merged['total_weight'] = 0

    for comp, weight in WEIGHTS.items():
        if comp in merged.columns:
            # Add weighted component where not null
            mask = merged[comp].notna()
            merged.loc[mask, 'education_component'] += merged.loc[mask, comp] * weight
            merged.loc[mask, 'total_weight'] += weight

    # Normalize by actual total weight (accounts for missing components)
    mask = merged['total_weight'] > 0
    merged.loc[mask, 'education_component'] = (
        merged.loc[mask, 'education_component'] / merged.loc[mask, 'total_weight']
    )

    # Set to NaN where no components available
    merged.loc[~mask, 'education_component'] = np.nan

    print(f"\n✓ Composite created")
    print(f"  Valid values: {merged['education_component'].notna().sum()}")
    print(f"  Coverage: {merged['education_component'].notna().sum() / len(merged):.1%}")
    print(f"  Range: [{merged['education_component'].min():.3f}, {merged['education_component'].max():.3f}]")

    return merged


def visualize_education_component(df):
    """Create visualizations of education component."""

    print(f"\n{'='*80}")
    print("Creating Visualizations")
    print(f"{'='*80}")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Filter to countries (exclude regional aggregates)
    aggregates = ['WLD', 'EAS', 'ECS', 'LCN', 'MEA', 'NAC', 'SAS', 'SSF',
                  'HIC', 'LIC', 'LMC', 'MIC', 'UMC', 'OED', 'ARB']
    countries = df[~df['country_code'].isin(aggregates)].copy()

    # 1. Global trend (world aggregate)
    world = df[df['country_code'] == 'WLD'].copy().sort_values('year')

    if len(world) > 0:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(world['year'], world['education_component'],
                marker='o', markersize=4, linewidth=2, color='steelblue')
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Education Component (0-1)', fontsize=12)
        ax.set_title('Global Education Component Evolution',
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1])

        plt.tight_layout()
        output_file = FIGURES_DIR / "education_global_trend.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()

    # 2. Top vs Bottom countries (latest year)
    latest_year = countries['year'].max()
    latest = countries[countries['year'] == latest_year].dropna(subset=['education_component'])

    if len(latest) >= 10:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Top 10
        top10 = latest.nlargest(10, 'education_component')
        colors_top = sns.color_palette("Greens_r", 10)
        ax1.barh(range(len(top10)), top10['education_component'], color=colors_top)
        ax1.set_yticks(range(len(top10)))
        ax1.set_yticklabels(top10['country_name'])
        ax1.set_xlabel('Education Component (0-1)', fontsize=12)
        ax1.set_title(f'Top 10 Countries ({latest_year})', fontsize=14, fontweight='bold')
        ax1.set_xlim([0, 1])
        ax1.invert_yaxis()

        # Bottom 10
        bottom10 = latest.nsmallest(10, 'education_component')
        colors_bottom = sns.color_palette("Reds_r", 10)
        ax2.barh(range(len(bottom10)), bottom10['education_component'], color=colors_bottom)
        ax2.set_yticks(range(len(bottom10)))
        ax2.set_yticklabels(bottom10['country_name'])
        ax2.set_xlabel('Education Component (0-1)', fontsize=12)
        ax2.set_title(f'Bottom 10 Countries ({latest_year})', fontsize=14, fontweight='bold')
        ax2.set_xlim([0, 1])
        ax2.invert_yaxis()

        plt.tight_layout()
        output_file = FIGURES_DIR / "education_top_bottom_countries.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()

    # 3. Distribution over time
    if len(countries) > 0:
        fig, ax = plt.subplots(figsize=(12, 6))

        # Sample years for clarity
        years = sorted(countries['year'].unique())
        sample_years = [y for y in years if y % 10 == 0]  # Every 10 years

        data_to_plot = []
        labels = []
        for year in sample_years:
            year_data = countries[countries['year'] == year]['education_component'].dropna()
            if len(year_data) > 0:
                data_to_plot.append(year_data)
                labels.append(str(year))

        if len(data_to_plot) > 0:
            ax.violinplot(data_to_plot, positions=range(len(data_to_plot)),
                         showmeans=True, showmedians=True)
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels)
            ax.set_xlabel('Year', fontsize=12)
            ax.set_ylabel('Education Component (0-1)', fontsize=12)
            ax.set_title('Education Component Distribution Over Time',
                        fontsize=14, fontweight='bold')
            ax.set_ylim([0, 1])
            ax.grid(True, alpha=0.3, axis='y')

            plt.tight_layout()
            output_file = FIGURES_DIR / "education_distribution_evolution.png"
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"✓ Saved: {output_file}")
            plt.close()


def main():
    """Main execution function."""

    print("\n📚 Processing Education Component for H₇")
    print("="*80)

    # Ensure output directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    df = load_education_data()
    if df is None:
        return

    # Create composite
    education_df = create_education_component(df)
    if education_df is None:
        return

    # Save processed component
    output_file = OUTPUT_DIR / "education_component.csv"
    education_df.to_csv(output_file, index=False)
    print(f"\n✓ Saved processed component: {output_file}")

    # Create visualizations
    visualize_education_component(education_df)

    print("\n" + "="*80)
    print("✓ Education Component Processing Complete!")
    print("="*80)
    print(f"\nOutput files:")
    print(f"  - {OUTPUT_DIR}/education_component.csv")
    print(f"  - {FIGURES_DIR}/education_global_trend.png")
    print(f"  - {FIGURES_DIR}/education_top_bottom_countries.png")
    print(f"  - {FIGURES_DIR}/education_distribution_evolution.png")
    print()
    print("Next step: Process other H₇ components (patents, infrastructure, governance)")
    print()


if __name__ == "__main__":
    main()
