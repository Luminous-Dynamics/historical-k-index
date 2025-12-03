#!/usr/bin/env python3
"""
Download Constitutional Complexity Data for H₇ Component

This script processes constitutional data from the Comparative Constitutions
Project (CCP) to measure institutional sophistication and governance evolution.

Data Source: Comparative Constitutions Project
Coverage: 1789-2023
Variables: Constitutional complexity, rights enumerated, amendment procedures

Author: Tristan Stoltz / Claude Code
Date: December 2, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("data/raw/ccp")
PROCESSED_DIR = Path("data/processed/H7_components")


def download_ccp_data():
    """
    Download CCP constitutional data.

    CCP provides rich data on constitutional design across countries and time.
    """

    print("=" * 80)
    print("Constitutional Complexity Data Collection")
    print("=" * 80)
    print()
    print("Comparative Constitutions Project (CCP) data:")
    print("https://comparativeconstitutionsproject.org/download-data/")
    print()
    print("Download instructions:")
    print("1. Visit CCP website")
    print("2. Click 'Download Data'")
    print("3. Register (free academic access)")
    print("4. Download 'Characteristics of National Constitutions' dataset")
    print("5. Save as: data/raw/ccp/ccp_characteristics.csv")
    print()

    # Check if file exists
    raw_file = OUTPUT_DIR / "ccp_characteristics.csv"
    if raw_file.exists():
        print(f"✓ Found existing file: {raw_file}")
        return raw_file
    else:
        print(f"✗ File not found: {raw_file}")
        print("\nPlease download manually and run this script again.")
        return None


def calculate_constitutional_complexity(df):
    """
    Calculate constitutional complexity index from CCP data.

    Components:
    1. Number of articles (length)
    2. Rights enumerated (scope)
    3. Amendment difficulty (stability)
    4. Checks and balances (separation of powers)
    """

    print("\nCalculating constitutional complexity index...")

    # Example calculation (actual variables depend on CCP dataset structure)
    df['complexity'] = (
        0.3 * normalize(df.get('num_articles', 0)) +
        0.3 * normalize(df.get('rights_enumerated', 0)) +
        0.2 * normalize(df.get('amendment_difficulty', 0)) +
        0.2 * normalize(df.get('checks_balances_score', 0))
    )

    return df


def normalize(series):
    """Normalize series to [0, 1] scale."""
    min_val = series.min()
    max_val = series.max()
    if max_val == min_val:
        return series * 0  # All zeros if constant
    return (series - min_val) / (max_val - min_val)


def process_constitutional_data(input_file):
    """
    Process CCP data into H₇ component.

    Steps:
    1. Load raw CCP data
    2. Calculate complexity index
    3. Aggregate to global average (population-weighted)
    4. Normalize to [0, 1]
    """

    print("\n" + "=" * 80)
    print("Processing Constitutional Data")
    print("=" * 80)

    if not input_file or not Path(input_file).exists():
        print("✗ Input file not found. Cannot process.")
        return None

    try:
        print(f"\nLoading: {input_file}")
        df = pd.read_csv(input_file)

        print(f"✓ Loaded {len(df)} rows")
        print(f"Columns available: {len(df.columns)}")

        # Calculate complexity
        df = calculate_constitutional_complexity(df)

        # Save interim result
        output_file = PROCESSED_DIR / "constitutions_interim.csv"
        df.to_csv(output_file, index=False)

        print(f"\n✓ Interim data saved: {output_file}")
        print("\nNext: Aggregate to global time series")

        return output_file

    except Exception as e:
        print(f"✗ Error processing constitutional data: {e}")
        return None


def create_ccp_collection_log():
    """Create documentation log."""

    log_file = OUTPUT_DIR / "DATA_COLLECTION_LOG.md"

    log_content = f"""# Constitutional Complexity Data Collection Log

**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Component:** H₇ (Evolutionary Progression) - Constitutional Complexity

## Data Source Information

### Comparative Constitutions Project (CCP)
- **URL:** https://comparativeconstitutionsproject.org/
- **Coverage:** 1789-2023 (234 years!)
- **Countries:** ~200 countries with constitutional history
- **Variables:** Constitutional characteristics, rights, procedures
- **Format:** CSV, Stata
- **License:** Free for academic use (registration required)

## Key Variables

1. **Constitutional Length:** Number of articles/words
2. **Rights Enumerated:** Count of explicit rights protections
3. **Amendment Difficulty:** Procedural requirements for changes
4. **Judicial Review:** Power of courts to review legislation
5. **Federalism:** Division of powers across levels
6. **Electoral Rules:** Constitutional provisions for elections

## Complexity Index Formula

```python
Constitutional_Complexity = (
    0.30 × length_normalized +
    0.30 × rights_enumerated_normalized +
    0.20 × amendment_difficulty_normalized +
    0.20 × checks_balances_normalized
)
```

## Collection Status

- [ ] CCP data downloaded
- [ ] Complexity index calculated
- [ ] Country-year panel constructed
- [ ] Global aggregate calculated
- [ ] Normalization to [0,1] complete

## Citation

```
Elkins, Zachary, Tom Ginsburg, and James Melton. 2024.
The Comparative Constitutions Project: A Cross-National Historical Dataset
of Written Constitutions. Version 5.0.
Available at: https://comparativeconstitutionsproject.org/
Accessed: {pd.Timestamp.now().strftime('%Y-%m-%d')}
```

## Notes

CCP provides excellent temporal coverage back to 1789, making it ideal for
H₇ construction. The United States Constitution (1789) provides a natural
starting point for measuring constitutional evolution.

For pre-1789 period (1810 still predates many constitutions):
- Use proxy: Presence/absence of written constitution
- Interpolate from earliest available data
- Consider historical governance structures

## Next Steps

1. Download CCP characteristics dataset
2. Calculate complexity index
3. Create country-year time series
4. Aggregate to global average (population-weighted)
5. Save as `data/processed/H7_components/constitutions.csv`
"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w') as f:
        f.write(log_content)

    print(f"✓ Collection log created: {log_file}")
    return log_file


def main():
    """Main execution."""

    print("\n🏛️ Starting Constitutional Complexity Data Collection")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Processed directory: {PROCESSED_DIR}")
    print()

    # Ensure directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Try to locate CCP data
    ccp_file = download_ccp_data()

    # Create collection log
    log_file = create_ccp_collection_log()

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    print("✓ Directory structure ready")
    print("✓ Data collection log created")
    print()
    print("Next steps:")
    print("1. Register at Comparative Constitutions Project")
    print("2. Download 'Characteristics' dataset")
    print("3. Run this script again to process")
    print()


if __name__ == "__main__":
    main()
