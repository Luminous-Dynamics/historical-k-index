#!/usr/bin/env python3
"""
Download Education Capital Data for H₇ Component

This script processes educational attainment data from the Barro-Lee dataset
to measure accumulated human capital and knowledge capacity.

Data Source: Barro-Lee Educational Attainment Dataset
Coverage: 1870-2023
Variables: Years of schooling, education levels

Author: Tristan Stoltz / Claude Code
Date: December 2, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("data/raw/barro_lee")
PROCESSED_DIR = Path("data/processed/H7_components")


def download_barro_lee_data():
    """
    Download Barro-Lee educational attainment data.

    The Barro-Lee dataset provides educational attainment estimates for
    146 countries from 1950 to 2010, with historical extensions to 1870.
    """

    print("=" * 80)
    print("Education Capital Data Collection")
    print("=" * 80)
    print()
    print("Barro-Lee Educational Attainment Dataset:")
    print("http://www.barrolee.com/")
    print()
    print("Download instructions:")
    print("1. Visit http://www.barrolee.com/")
    print("2. Click 'Download' in the menu")
    print("3. Download 'BL2013_MF1599_v2.0.csv' (5-year intervals)")
    print("4. Save as: data/raw/barro_lee/barro_lee_attainment.csv")
    print()
    print("Alternative: World Bank Education Statistics")
    print("https://data.worldbank.org/topic/education")
    print()

    # Check if file exists
    raw_file = OUTPUT_DIR / "barro_lee_attainment.csv"
    if raw_file.exists():
        print(f"✓ Found existing file: {raw_file}")
        return raw_file
    else:
        print(f"✗ File not found: {raw_file}")
        print("\nPlease download manually and run this script again.")
        return None


def calculate_education_capital(df):
    """
    Calculate cumulative education capital from attainment data.

    Education capital represents the stock of knowledge accumulated
    in the population through formal schooling.

    Formula:
    Education_Capital = Σ (population[age_group] × mean_years_schooling[age_group])
    Per capita: Education_Capital / total_population
    """

    print("\nCalculating education capital...")

    # Barro-Lee provides data by age groups (15-19, 20-24, ..., 60-64)
    # and education level (primary, secondary, tertiary)

    # Simplified calculation (actual implementation depends on data structure)
    if 'mean_years_schooling' in df.columns:
        df['education_capital_pc'] = df['mean_years_schooling']
    elif 'yr_sch' in df.columns:  # Barro-Lee variable name
        df['education_capital_pc'] = df['yr_sch']
    else:
        # Calculate from education levels
        df['education_capital_pc'] = (
            df.get('primary', 0) * 6 +     # 6 years primary
            df.get('secondary', 0) * 12 +  # 12 years through secondary
            df.get('tertiary', 0) * 16     # 16 years with tertiary
        )

    return df


def normalize(series):
    """Normalize series to [0, 1] scale."""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return series * 0
    return (series - min_val) / (max_val - min_val)


def process_education_data(input_file):
    """
    Process Barro-Lee data into H₇ component.

    Steps:
    1. Load raw education attainment data
    2. Calculate education capital per capita
    3. Aggregate to global average (population-weighted)
    4. Normalize to [0, 1]
    5. Interpolate for missing years (Barro-Lee is 5-year intervals)
    """

    print("\n" + "=" * 80)
    print("Processing Education Data")
    print("=" * 80)

    if not input_file or not Path(input_file).exists():
        print("✗ Input file not found. Cannot process.")
        return None

    try:
        print(f"\nLoading: {input_file}")
        df = pd.read_csv(input_file)

        print(f"✓ Loaded {len(df)} rows")
        print(f"Countries: {df['country'].nunique() if 'country' in df.columns else 'unknown'}")

        # Calculate education capital
        df = calculate_education_capital(df)

        # Save interim result
        output_file = PROCESSED_DIR / "education_interim.csv"
        df.to_csv(output_file, index=False)

        print(f"\n✓ Interim data saved: {output_file}")
        print("\nNext: Aggregate to global time series and interpolate")

        return output_file

    except Exception as e:
        print(f"✗ Error processing education data: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_barro_lee_collection_log():
    """Create documentation log."""

    log_file = OUTPUT_DIR / "DATA_COLLECTION_LOG.md"

    log_content = f"""# Education Capital Data Collection Log

**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Component:** H₇ (Evolutionary Progression) - Education Capital

## Data Source Information

### Barro-Lee Educational Attainment Dataset
- **URL:** http://www.barrolee.com/
- **Coverage:** 1950-2010 (5-year intervals), extended to 1870
- **Countries:** 146 countries
- **Variables:** Mean years of schooling by age group and education level
- **Format:** CSV
- **License:** Free for academic use

### Supplementary: World Bank Education Statistics
- **Indicator:** SE.ADT.LITR.ZS (Literacy rate, adult total)
- **URL:** https://data.worldbank.org/indicator/SE.ADT.LITR.ZS
- **Coverage:** 1970-2023
- **Use:** Validate and extend Barro-Lee estimates

## Education Capital Formula

```python
# For each age group g:
Education_Capital = Σ (Population[g] × Mean_Years_Schooling[g])

# Per capita:
Education_Capital_PC = Education_Capital / Total_Population

# Global aggregate (population-weighted):
Global_Education_Capital = Σ (Country_EC_PC[c] × Population[c]) / Total_Pop
```

## Collection Status

- [ ] Barro-Lee data downloaded
- [ ] Education capital calculated
- [ ] Global aggregate computed
- [ ] Interpolation for annual values
- [ ] Historical extension (1870-1950)
- [ ] Normalization to [0,1] complete

## Historical Extension Strategy

Barro-Lee provides estimates back to 1870, but data is sparse.
For 1810-1870, we'll use:

1. **Literacy rates** as proxy (UNESCO historical data)
2. **School enrollment** where available
3. **Linear extrapolation** from 1870 baseline
4. **Assumption**: Very low education capital pre-1850

## Citation

```
Barro, Robert J., and Jong-Wha Lee. 2013.
"A New Data Set of Educational Attainment in the World, 1950-2010."
Journal of Development Economics 104: 184-198.

Dataset available at: http://www.barrolee.com/
Accessed: {pd.Timestamp.now().strftime('%Y-%m-%d')}
```

## Notes

Education capital is a strong indicator of:
- Accumulated knowledge in society
- Capacity for innovation and adaptation
- Long-term economic productivity
- Institutional sophistication

For H₇ (Evolutionary Progression), it captures the "stock" of human
capabilities that enable civilizational advancement.

## Next Steps

1. Download Barro-Lee dataset (BL2013_MF1599_v2.0.csv)
2. Calculate education capital per capita
3. Create annual time series (interpolate 5-year data)
4. Extend backwards to 1810 using literacy proxies
5. Save as `data/processed/H7_components/education.csv`
"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w') as f:
        f.write(log_content)

    print(f"✓ Collection log created: {log_file}")
    return log_file


def main():
    """Main execution."""

    print("\n📚 Starting Education Capital Data Collection")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Processed directory: {PROCESSED_DIR}")
    print()

    # Ensure directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Try to locate Barro-Lee data
    bl_file = download_barro_lee_data()

    # Create collection log
    log_file = create_barro_lee_collection_log()

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    print("✓ Directory structure ready")
    print("✓ Data collection log created")
    print()
    print("Next steps:")
    print("1. Download Barro-Lee dataset from barrolee.com")
    print("2. Run this script again to process")
    print("3. Calculate global education capital time series")
    print()


if __name__ == "__main__":
    main()
