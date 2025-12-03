#!/usr/bin/env python3
"""
Integrate All H₇ Components into Validated Harmony

This script combines the four H₇ components (patents, constitutions,
education, infrastructure) into a single validated H₇ time series.

Components:
1. Patent stock per capita (WIPO, 1883-2023)
2. Constitutional complexity (CCP, 1789-2023)
3. Education capital (Barro-Lee, 1870-2023)
4. Infrastructure density (multiple sources, 1810-2023)

Output: Validated H₇ (Evolutionary Progression) for K(t) calculation

Author: Tristan Stoltz / Claude Code
Date: December 2, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# Configuration
COMPONENTS_DIR = Path("data/processed/H7_components")
OUTPUT_DIR = Path("data/processed")
FIGURES_DIR = Path("figures")


def load_component(component_name):
    """Load a processed H₇ component."""

    file_path = COMPONENTS_DIR / f"{component_name}.csv"

    if not file_path.exists():
        print(f"⚠ Component not found: {component_name}")
        print(f"   Expected at: {file_path}")
        return None

    try:
        df = pd.read_csv(file_path)
        print(f"✓ Loaded {component_name}: {len(df)} observations")
        return df
    except Exception as e:
        print(f"✗ Error loading {component_name}: {e}")
        return None


def normalize_to_01(series):
    """Normalize series to [0, 1] scale using historical min-max."""
    min_val = series.min()
    max_val = series.max()

    if max_val == min_val:
        return pd.Series([0.5] * len(series), index=series.index)

    return (series - min_val) / (max_val - min_val)


def integrate_h7_components(patents=None, constitutions=None,
                            education=None, infrastructure=None):
    """
    Integrate four components into validated H₇.

    Method: Geometric mean of available components

    H₇(t) = [Π_i Component_i(t)]^(1/n)

    where n = number of available components at time t
    """

    print("\n" + "=" * 80)
    print("Integrating H₇ Components")
    print("=" * 80)
    print()

    # Create year range (1810-2020)
    years = range(1810, 2021)
    h7_data = pd.DataFrame({'year': years})

    # Add each component if available
    components_used = []

    if patents is not None:
        h7_data = h7_data.merge(
            patents[['year', 'patents_normalized']],
            on='year',
            how='left'
        )
        components_used.append('patents')

    if constitutions is not None:
        h7_data = h7_data.merge(
            constitutions[['year', 'complexity_normalized']],
            on='year',
            how='left'
        )
        components_used.append('constitutions')

    if education is not None:
        h7_data = h7_data.merge(
            education[['year', 'education_capital_normalized']],
            on='year',
            how='left'
        )
        components_used.append('education')

    if infrastructure is not None:
        h7_data = h7_data.merge(
            infrastructure[['year', 'infrastructure_normalized']],
            on='year',
            how='left'
        )
        components_used.append('infrastructure')

    print(f"Components available: {len(components_used)}")
    print(f"Components: {', '.join(components_used)}")
    print()

    # Calculate H₇ as geometric mean of available components
    # For each year, use only available (non-null) components

    def geometric_mean_row(row):
        """Calculate geometric mean of non-null values in row."""
        values = [v for v in row if pd.notna(v)]
        if len(values) == 0:
            return np.nan
        return np.prod(values) ** (1/len(values))

    # Extract component columns (exclude 'year')
    component_cols = [col for col in h7_data.columns if col != 'year']

    h7_data['H7_validated'] = h7_data[component_cols].apply(
        geometric_mean_row,
        axis=1
    )

    # Count how many components contributed to each year
    h7_data['components_count'] = h7_data[component_cols].notna().sum(axis=1)

    print("H₇ Integration Complete:")
    print(f"  Years with 4 components: {(h7_data['components_count'] == 4).sum()}")
    print(f"  Years with 3 components: {(h7_data['components_count'] == 3).sum()}")
    print(f"  Years with 2 components: {(h7_data['components_count'] == 2).sum()}")
    print(f"  Years with 1 component:  {(h7_data['components_count'] == 1).sum()}")
    print(f"  Years with 0 components: {(h7_data['components_count'] == 0).sum()}")
    print()

    return h7_data


def validate_h7(h7_data):
    """
    Validate the integrated H₇ time series.

    Checks:
    1. Values in [0, 1] range
    2. General upward trend (evolutionary progression)
    3. No impossible jumps
    4. Reasonable coverage
    """

    print("\n" + "=" * 80)
    print("Validating H₇")
    print("=" * 80)
    print()

    h7 = h7_data['H7_validated'].dropna()

    # Check 1: Range
    min_val = h7.min()
    max_val = h7.max()
    print(f"✓ Range check: [{min_val:.3f}, {max_val:.3f}]")

    if min_val < 0 or max_val > 1:
        print("  ⚠ WARNING: Values outside [0, 1] range!")

    # Check 2: Trend
    # Calculate linear trend
    years_with_data = h7_data[h7_data['H7_validated'].notna()]['year']
    h7_values = h7_data[h7_data['H7_validated'].notna()]['H7_validated']

    if len(h7_values) > 1:
        slope = np.polyfit(years_with_data, h7_values, 1)[0]
        print(f"✓ Trend check: slope = {slope:.6f} per year")

        if slope > 0:
            print("  ✓ Positive trend (expected for evolutionary progression)")
        else:
            print("  ⚠ WARNING: Negative trend (unexpected!)")

    # Check 3: Coverage
    coverage = (h7_data['H7_validated'].notna().sum() / len(h7_data)) * 100
    print(f"✓ Coverage: {coverage:.1f}% of years (1810-2020)")

    if coverage < 50:
        print("  ⚠ WARNING: Less than 50% coverage")
    elif coverage < 75:
        print("  ⚠ Moderate coverage, some interpolation needed")
    else:
        print("  ✓ Good coverage")

    # Check 4: Jumps
    h7_diff = h7.diff()
    max_jump = h7_diff.abs().max()
    print(f"✓ Maximum year-to-year change: {max_jump:.3f}")

    if max_jump > 0.1:
        print(f"  ⚠ WARNING: Large jump detected (>{0.1})")

    print()
    return True


def visualize_h7_components(h7_data):
    """
    Create visualization of H₇ and its components.
    """

    print("Creating H₇ visualization...")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Plot 1: All components
    component_cols = [col for col in h7_data.columns
                     if col not in ['year', 'H7_validated', 'components_count']]

    for col in component_cols:
        ax1.plot(h7_data['year'], h7_data[col],
                label=col.replace('_normalized', '').replace('_', ' ').title(),
                alpha=0.7, linewidth=1.5)

    ax1.set_xlabel('Year', fontsize=12)
    ax1.set_ylabel('Normalized Value [0, 1]', fontsize=12)
    ax1.set_title('H₇ Components Over Time', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(1810, 2020)
    ax1.set_ylim(-0.05, 1.05)

    # Plot 2: Integrated H₇
    ax2.plot(h7_data['year'], h7_data['H7_validated'],
            color='darkgreen', linewidth=2.5, label='H₇ (Validated)')
    ax2.fill_between(h7_data['year'], 0, h7_data['H7_validated'],
                     color='darkgreen', alpha=0.2)

    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('H₇ Value [0, 1]', fontsize=12)
    ax2.set_title('Integrated H₇: Evolutionary Progression (1810-2020)',
                 fontsize=14, fontweight='bold')
    ax2.legend(loc='upper left', framealpha=0.9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(1810, 2020)
    ax2.set_ylim(-0.05, 1.05)

    # Add annotations for key periods
    ax2.axvspan(1914, 1918, alpha=0.2, color='red', label='WWI')
    ax2.axvspan(1939, 1945, alpha=0.2, color='red', label='WWII')

    plt.tight_layout()

    # Save figure
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = FIGURES_DIR / "H7_validated_decomposition.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Figure saved: {output_path}")

    plt.close()


def save_h7_output(h7_data):
    """Save validated H₇ to CSV."""

    output_file = OUTPUT_DIR / "H7_validated_1810_2020.csv"
    h7_data.to_csv(output_file, index=False)

    print(f"✓ Validated H₇ saved: {output_file}")

    # Also save just year and H7 for easy integration
    h7_simple = h7_data[['year', 'H7_validated']].copy()
    simple_file = OUTPUT_DIR / "H7_for_K_calculation.csv"
    h7_simple.to_csv(simple_file, index=False)

    print(f"✓ H₇ for K(t) calculation saved: {simple_file}")

    return output_file


def main():
    """Main execution."""

    print("\n🔧 Starting H₇ Component Integration")
    print("=" * 80)
    print()

    # Load components
    print("Loading H₇ components...")
    print()

    patents = load_component("patents")
    constitutions = load_component("constitutions")
    education = load_component("education")
    infrastructure = load_component("infrastructure")

    # Check if we have at least 2 components
    available_components = sum([
        patents is not None,
        constitutions is not None,
        education is not None,
        infrastructure is not None
    ])

    print()
    print(f"Components available: {available_components}/4")
    print()

    if available_components < 2:
        print("✗ Need at least 2 components to construct H₇")
        print("✗ Please run data collection scripts first:")
        print("   1. 01_download_wipo_patents.py")
        print("   2. 02_download_ccp_constitutions.py")
        print("   3. 03_download_barro_lee_education.py")
        print("   4. 04_construct_infrastructure_index.py")
        print()
        return

    # Integrate components
    h7_data = integrate_h7_components(
        patents=patents,
        constitutions=constitutions,
        education=education,
        infrastructure=infrastructure
    )

    # Validate
    validate_h7(h7_data)

    # Visualize
    visualize_h7_components(h7_data)

    # Save
    output_file = save_h7_output(h7_data)

    print("\n" + "=" * 80)
    print("H₇ Integration Complete!")
    print("=" * 80)
    print()
    print(f"✓ Validated H₇ ready: {output_file}")
    print()
    print("Next steps:")
    print("1. Review H₇ visualization")
    print("2. Run K(t) recalculation with validated H₇")
    print("3. Compare to previous K(t) estimates")
    print("4. Update manuscript figures and tables")
    print()


if __name__ == "__main__":
    main()
