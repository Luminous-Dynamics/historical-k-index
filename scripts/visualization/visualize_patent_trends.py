#!/usr/bin/env python3
"""
Visualize Patent Trends from World Bank Data

Creates visualizations showing:
1. Global patent trends 1980-2021
2. Top countries over time
3. Regional comparisons
4. Patents per capita trends

Author: Tristan Stoltz / Claude Code
Date: December 3, 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Configuration
DATA_FILE = Path("data/raw/wipo/worldbank_patents_combined.csv")
FIGURES_DIR = Path("figures")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


def load_data():
    """Load World Bank patent data."""
    print(f"Loading data from: {DATA_FILE}")

    if not DATA_FILE.exists():
        print(f"✗ Data file not found: {DATA_FILE}")
        print("Run 00_download_worldbank_patents.py first")
        return None

    df = pd.read_csv(DATA_FILE)
    print(f"✓ Loaded {len(df)} records")
    print(f"  Countries: {df['country_code'].nunique()}")
    print(f"  Year range: {df['year'].min()} - {df['year'].max()}")
    return df


def plot_global_trends(df):
    """Plot global patent trends over time."""
    print("\nCreating global trends visualization...")

    # Get world data
    world_data = df[df['country_code'] == 'WLD'].copy()

    if len(world_data) == 0:
        print("✗ No world aggregate data found")
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Plot 1: Total patents over time
    if 'total' in world_data.columns:
        ax1.plot(world_data['year'], world_data['total'] / 1e6,
                marker='o', linewidth=2, markersize=4, color='steelblue')
        ax1.set_ylabel('Global Patents (millions)', fontsize=12)
        ax1.set_title('Global Patent Applications 1980-2021', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)

        # Annotate key points
        max_year = world_data.loc[world_data['total'].idxmax(), 'year']
        max_value = world_data['total'].max() / 1e6
        ax1.annotate(f'Peak: {max_value:.2f}M\n({int(max_year)})',
                    xy=(max_year, max_value),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    # Plot 2: Resident vs Non-resident
    if 'resident' in world_data.columns and 'non-resident' in world_data.columns:
        ax2.plot(world_data['year'], world_data['resident'] / 1e6,
                marker='s', linewidth=2, markersize=4, label='Resident', color='green')
        ax2.plot(world_data['year'], world_data['non-resident'] / 1e6,
                marker='^', linewidth=2, markersize=4, label='Non-resident', color='orange')
        ax2.set_xlabel('Year', fontsize=12)
        ax2.set_ylabel('Patents (millions)', fontsize=12)
        ax2.set_title('Resident vs Non-Resident Patent Applications', fontsize=14, fontweight='bold')
        ax2.legend(fontsize=11)
        ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    output_file = FIGURES_DIR / "patent_global_trends.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()


def plot_top_countries(df):
    """Plot top countries over time."""
    print("\nCreating top countries visualization...")

    # Get latest year data for top countries
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year].copy()

    # Exclude aggregates
    aggregates = ['WLD', 'EAS', 'ECS', 'LCN', 'MEA', 'NAC', 'SAS', 'SSF']
    latest_data = latest_data[~latest_data['country_code'].isin(aggregates)]

    # Get top 10 countries by total patents
    value_col = 'total' if 'total' in latest_data.columns else 'resident'
    top_countries = latest_data.nlargest(10, value_col)

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot 1: Bar chart of top countries in latest year
    colors = sns.color_palette("viridis", 10)
    ax1.barh(range(len(top_countries)), top_countries[value_col] / 1000, color=colors)
    ax1.set_yticks(range(len(top_countries)))
    ax1.set_yticklabels(top_countries['country_name'])
    ax1.set_xlabel('Patents (thousands)', fontsize=12)
    ax1.set_title(f'Top 10 Countries by Patents ({latest_year})', fontsize=14, fontweight='bold')
    ax1.invert_yaxis()

    # Add value labels
    for i, (_, row) in enumerate(top_countries.iterrows()):
        ax1.text(row[value_col] / 1000, i, f' {row[value_col]/1000:.0f}K',
                va='center', fontsize=9)

    # Plot 2: Trends over time for top 5 countries
    top_5 = top_countries.head(5)

    for _, country in top_5.iterrows():
        country_code = country['country_code']
        country_data = df[df['country_code'] == country_code].sort_values('year')

        if len(country_data) > 0:
            ax2.plot(country_data['year'], country_data[value_col] / 1000,
                    marker='o', markersize=3, linewidth=2,
                    label=country['country_name'])

    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Patents (thousands)', fontsize=12)
    ax2.set_title('Patent Trends: Top 5 Countries (1980-2021)', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    output_file = FIGURES_DIR / "patent_top_countries.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()


def plot_growth_analysis(df):
    """Analyze and plot patent growth rates."""
    print("\nCreating growth analysis visualization...")

    # Focus on countries with good data coverage
    value_col = 'total' if 'total' in df.columns else 'resident'

    # Get world data for reference
    world_data = df[df['country_code'] == 'WLD'].copy().sort_values('year')

    if len(world_data) == 0:
        print("✗ No world data for growth analysis")
        return

    # Calculate growth rate
    world_data['growth_rate'] = world_data[value_col].pct_change() * 100

    fig, ax = plt.subplots(figsize=(14, 6))

    # Plot growth rate
    ax.plot(world_data['year'], world_data['growth_rate'],
           marker='o', markersize=4, linewidth=2, color='steelblue')
    ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Year-over-Year Growth Rate (%)', fontsize=12)
    ax.set_title('Global Patent Application Growth Rate (1980-2021)',
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Annotate significant events
    # Find periods of high growth
    high_growth = world_data[world_data['growth_rate'] > 10]
    for _, row in high_growth.iterrows():
        ax.annotate(f"{row['growth_rate']:.1f}%",
                   xy=(row['year'], row['growth_rate']),
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=8, alpha=0.7)

    plt.tight_layout()

    output_file = FIGURES_DIR / "patent_growth_analysis.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()


def create_summary_stats(df):
    """Create summary statistics table."""
    print("\nCreating summary statistics...")

    value_col = 'total' if 'total' in df.columns else 'resident'

    # Overall statistics
    latest_year = df['year'].max()
    earliest_year = df['year'].min()

    stats = {
        'Coverage': f"{earliest_year}-{latest_year} ({latest_year - earliest_year + 1} years)",
        'Countries': df['country_code'].nunique(),
        'Total Records': len(df),
        'Latest Year': latest_year,
        'Global Patents (latest)': f"{df[df['country_code'] == 'WLD'][value_col].iloc[-1]:,.0f}" if len(df[df['country_code'] == 'WLD']) > 0 else "N/A",
    }

    # Top 5 countries in latest year
    latest_data = df[df['year'] == latest_year]
    aggregates = ['WLD', 'EAS', 'ECS', 'LCN', 'MEA', 'NAC', 'SAS', 'SSF']
    latest_countries = latest_data[~latest_data['country_code'].isin(aggregates)]
    top_5 = latest_countries.nlargest(5, value_col)

    print(f"\n{'='*60}")
    print("PATENT DATA SUMMARY")
    print(f"{'='*60}")
    for key, value in stats.items():
        print(f"{key:.<30} {value}")

    print(f"\nTop 5 Countries ({latest_year}):")
    print(f"{'='*60}")
    for i, (_, row) in enumerate(top_5.iterrows(), 1):
        print(f"{i}. {row['country_name']:<30} {row[value_col]:>15,.0f}")

    # Save to file
    output_file = FIGURES_DIR / "patent_summary_stats.txt"
    with open(output_file, 'w') as f:
        f.write("PATENT DATA SUMMARY\n")
        f.write("=" * 60 + "\n\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
        f.write(f"\nTop 5 Countries ({latest_year}):\n")
        f.write("=" * 60 + "\n")
        for i, (_, row) in enumerate(top_5.iterrows(), 1):
            f.write(f"{i}. {row['country_name']}: {row[value_col]:,.0f}\n")

    print(f"\n✓ Saved: {output_file}")


def main():
    """Main execution function."""

    print("\n📊 Visualizing Patent Trends")
    print("="*80)
    print()

    # Ensure output directory exists
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    df = load_data()

    if df is None:
        return

    # Create visualizations
    plot_global_trends(df)
    plot_top_countries(df)
    plot_growth_analysis(df)
    create_summary_stats(df)

    print("\n" + "="*80)
    print("✓ Visualization Complete!")
    print("="*80)
    print(f"\nGenerated files in {FIGURES_DIR}/:")
    print("  - patent_global_trends.png")
    print("  - patent_top_countries.png")
    print("  - patent_growth_analysis.png")
    print("  - patent_summary_stats.txt")
    print()
    print("These visualizations show:")
    print("  • Global patent trends 1980-2021")
    print("  • Top innovating countries")
    print("  • Growth patterns and dynamics")
    print()
    print("Next step: Normalize for population and integrate into H₇ component")
    print()


if __name__ == "__main__":
    main()
