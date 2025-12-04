#!/usr/bin/env python3
"""
Download WIPO Patent Statistics for H₇ Component

This script downloads patent application data from WIPO (World Intellectual
Property Organization) for use in constructing the validated H₇ (Evolutionary
Progression) harmony.

Data Source: WIPO IP Statistics Data Center
Coverage: 1883-2023
Variables: Patent applications by country of origin

Author: Tristan Stoltz / Claude Code
Date: December 2, 2025
"""

import pandas as pd
import requests
from pathlib import Path
import time

# Configuration
OUTPUT_DIR = Path("data/raw/wipo")
PROCESSED_DIR = Path("data/processed/H7_components")

# WIPO publishes data through their statistics portal
# We'll use their publicly available datasets

def download_wipo_data():
    """
    Download WIPO patent statistics.

    Note: WIPO data is available through multiple channels:
    1. WIPO IP Statistics Data Center (interactive portal)
    2. WIPO Open Data (bulk downloads)
    3. World Bank indicators (subset)

    For now, we'll document the manual download process and provide
    processing code for the downloaded files.
    """

    print("=" * 80)
    print("WIPO Patent Data Collection")
    print("=" * 80)
    print()
    print("WIPO patent data needs to be downloaded manually from:")
    print("https://www.wipo.int/ipstats/en/")
    print()
    print("Navigation:")
    print("1. Visit WIPO IP Statistics portal")
    print("2. Go to 'Statistics' → 'Statistical Data'")
    print("3. Select 'Patents' → 'Applications'")
    print("4. Choose 'By country/region of origin'")
    print("5. Select 'All countries' and date range '1883-2023'")
    print("6. Download as CSV")
    print()
    print("Alternative: WIPO also provides data via their API")
    print("https://www.wipo.int/ipstats/en/statistics/patents/")
    print()
    print("Save the downloaded file as:")
    print(f"  {OUTPUT_DIR}/wipo_patent_applications_raw.csv")
    print()

    # Check if file already exists
    raw_file = OUTPUT_DIR / "wipo_patent_applications_raw.csv"
    if raw_file.exists():
        print(f"✓ Found existing file: {raw_file}")
        return raw_file
    else:
        print(f"✗ File not found: {raw_file}")
        print()
        print("Please download the data manually and run this script again.")
        return None


def load_world_bank_patent_data():
    """
    As a fallback, we can use World Bank patent data which is more limited
    but automatically downloadable.

    World Bank Indicator: IP.PAT.RESD (Patent applications, residents)
    Coverage: 1960-2023 (less historical depth than WIPO)
    """
    print("\n" + "=" * 80)
    print("Alternative: World Bank Patent Data")
    print("=" * 80)
    print()
    print("Attempting to download World Bank patent indicator data...")
    print("Note: This has less historical coverage (1960+) than WIPO (1883+)")
    print()

    try:
        # World Bank data can be accessed via pandas_datareader or wbdata
        # For now, we'll use a direct CSV download link

        wb_indicator = "IP.PAT.RESD"  # Patent applications, residents
        url = f"https://api.worldbank.org/v2/en/indicator/{wb_indicator}"
        url += "?downloadformat=csv"

        print(f"Downloading from World Bank API...")
        print(f"Indicator: {wb_indicator}")

        # Note: Actual implementation would parse the World Bank CSV format
        # which has a specific structure with metadata rows

        output_file = OUTPUT_DIR / "worldbank_patents.csv"
        print(f"\nFor now, please download manually from:")
        print(f"https://data.worldbank.org/indicator/IP.PAT.RESD")
        print(f"And save as: {output_file}")

        return output_file if output_file.exists() else None

    except Exception as e:
        print(f"Error downloading World Bank data: {e}")
        return None


def process_patent_data(input_file):
    """
    Process raw WIPO patent data into normalized H₇ component.

    Steps:
    1. Load raw patent applications by country
    2. Calculate patents per capita (requires population data)
    3. Normalize to [0, 1] scale
    4. Aggregate to global average (population-weighted)
    """

    print("\n" + "=" * 80)
    print("Processing Patent Data")
    print("=" * 80)
    print()

    if not input_file or not Path(input_file).exists():
        print("✗ Input file not found. Cannot process.")
        return None

    try:
        # Load the raw data
        print(f"Loading: {input_file}")
        df = pd.read_csv(input_file)

        print(f"✓ Loaded {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        print(f"Date range: {df['year'].min()} - {df['year'].max()}")

        # Note: Actual processing depends on the CSV structure
        # WIPO data typically has columns like:
        # - country_code (ISO3)
        # - country_name
        # - year
        # - patent_applications (count)

        # TODO: Need population data to calculate per capita
        # Will integrate with existing HYDE population data

        output_file = PROCESSED_DIR / "patents_interim.csv"
        df.to_csv(output_file, index=False)

        print(f"\n✓ Interim data saved: {output_file}")
        print("\nNext step: Integrate with population data for per capita calculation")

        return output_file

    except Exception as e:
        print(f"✗ Error processing patent data: {e}")
        return None


def create_patent_collection_log():
    """Create a log documenting data collection attempts."""

    log_file = OUTPUT_DIR / "DATA_COLLECTION_LOG.md"

    log_content = f"""# WIPO Patent Data Collection Log

**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Component:** H₇ (Evolutionary Progression) - Patents

## Data Source Information

### Primary Source: WIPO IP Statistics
- **URL:** https://www.wipo.int/ipstats/en/
- **Coverage:** 1883-2023 (140 years)
- **Variables:** Patent applications by country of origin
- **Format:** CSV
- **License:** Public use for research (attribution required)

### Alternative Source: World Bank
- **Indicator:** IP.PAT.RESD (Patent applications, residents)
- **URL:** https://data.worldbank.org/indicator/IP.PAT.RESD
- **Coverage:** 1960-2023 (63 years)
- **Format:** CSV
- **License:** CC-BY-4.0

## Collection Status

- [ ] WIPO primary data downloaded
- [ ] World Bank fallback data downloaded
- [ ] Data quality checked
- [ ] Population data integrated
- [ ] Per capita calculation complete
- [ ] Normalization to [0,1] complete
- [ ] Global aggregate calculated

## Notes

WIPO provides the most comprehensive historical coverage going back to 1883.
This is critical for constructing H₇ over the full 1810-2020 period.

For pre-1883 period (1810-1882), we may need to:
1. Extrapolate backwards using proxy indicators
2. Use historical patent office records from major countries
3. Interpolate from earliest available data

## Citation

If using WIPO data:
```
World Intellectual Property Organization (WIPO). 2024.
WIPO IP Statistics Data Center. Geneva: WIPO.
Available at: https://www.wipo.int/ipstats/
Accessed: {pd.Timestamp.now().strftime('%Y-%m-%d')}
```

## Next Steps

1. Download WIPO patent data manually
2. Integrate with HYDE population data (already available)
3. Calculate patents per capita by country-year
4. Aggregate to global weighted average
5. Normalize to [0, 1] scale using historical min-max
6. Save as `data/processed/H7_components/patents.csv`
"""

    with open(log_file, 'w') as f:
        f.write(log_content)

    print(f"\n✓ Data collection log created: {log_file}")
    return log_file


def main():
    """Main execution function."""

    print("\n🚀 Starting WIPO Patent Data Collection")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Processed directory: {PROCESSED_DIR}")
    print()

    # Ensure directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Try to download/locate WIPO data
    wipo_file = download_wipo_data()

    # If WIPO not available, try World Bank
    if not wipo_file:
        wb_file = load_world_bank_patent_data()

    # Create collection log
    log_file = create_patent_collection_log()

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    print("✓ Directory structure ready")
    print("✓ Data collection log created")
    print()
    print("Next steps:")
    print("1. Download WIPO data manually (see instructions above)")
    print("2. Run this script again to process the downloaded data")
    print("3. Integrate with population data from HYDE")
    print("4. Calculate normalized global aggregate")
    print()


if __name__ == "__main__":
    main()
