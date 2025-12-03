#!/usr/bin/env python3
"""
Automated World Bank Patent Data Download

This script automatically downloads patent data from the World Bank API as a
fallback/supplement to WIPO data. While World Bank has less historical coverage
(1960+ vs WIPO's 1883+), it can be downloaded programmatically.

Data Source: World Bank Open Data API
Indicator: IP.PAT.RESD (Patent applications, residents)
Coverage: 1960-2023
License: CC-BY-4.0

Author: Tristan Stoltz / Claude Code
Date: December 3, 2025
"""

import pandas as pd
import requests
from pathlib import Path
import time
from typing import Optional
import json

# Configuration
OUTPUT_DIR = Path("data/raw/wipo")
PROCESSED_DIR = Path("data/processed/H7_components")

# World Bank API endpoints
WB_BASE_URL = "https://api.worldbank.org/v2"
PATENT_INDICATOR = "IP.PAT.RESD"  # Patent applications, residents
PATENT_NONRESIDENT = "IP.PAT.NRES"  # Patent applications, non-residents


def download_worldbank_indicator(
    indicator: str,
    start_year: int = 1960,
    end_year: int = 2023,
    output_file: Optional[Path] = None
) -> Optional[pd.DataFrame]:
    """
    Download data from World Bank API for a specific indicator.

    Args:
        indicator: World Bank indicator code (e.g., 'IP.PAT.RESD')
        start_year: Start year for data collection
        end_year: End year for data collection
        output_file: Path to save raw JSON response

    Returns:
        DataFrame with columns: country_code, country_name, year, value
    """

    print(f"\n{'='*80}")
    print(f"Downloading World Bank Indicator: {indicator}")
    print(f"{'='*80}\n")

    # World Bank API parameters
    # Format: /v2/country/all/indicator/{indicator}?date={start}:{end}&format=json&per_page=20000
    url = f"{WB_BASE_URL}/country/all/indicator/{indicator}"
    params = {
        'date': f'{start_year}:{end_year}',
        'format': 'json',
        'per_page': 20000  # Large enough to get all data in one request
    }

    print(f"URL: {url}")
    print(f"Parameters: {params}")
    print(f"Requesting data...")

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        # World Bank API returns [metadata, data]
        if len(data) < 2 or data[1] is None:
            print("✗ No data returned from API")
            return None

        metadata = data[0]
        records = data[1]

        print(f"✓ Retrieved {metadata.get('total', 'unknown')} records")
        print(f"  Pages: {metadata.get('pages', 1)}")
        print(f"  Records in this page: {len(records)}")

        # Save raw JSON if requested
        if output_file:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Raw JSON saved: {output_file}")

        # Parse into DataFrame
        rows = []
        for record in records:
            if record['value'] is not None:  # Skip null values
                rows.append({
                    'country_code': record['countryiso3code'],
                    'country_name': record['country']['value'],
                    'year': int(record['date']),
                    'value': float(record['value']),
                    'indicator': record['indicator']['value']
                })

        df = pd.DataFrame(rows)

        if len(df) > 0:
            print(f"\n✓ Parsed {len(df)} data points")
            print(f"  Countries: {df['country_code'].nunique()}")
            print(f"  Year range: {df['year'].min()} - {df['year'].max()}")
            print(f"  Sample data:")
            print(df.head())
        else:
            print("\n✗ No valid data points found")
            return None

        return df

    except requests.exceptions.RequestException as e:
        print(f"✗ Error downloading data: {e}")
        return None
    except Exception as e:
        print(f"✗ Error processing data: {e}")
        return None


def download_all_patent_indicators():
    """Download both resident and non-resident patent applications."""

    print("\n" + "="*80)
    print("World Bank Patent Data Collection")
    print("="*80)
    print()
    print("This script will download patent data from the World Bank API.")
    print("Note: Coverage is 1960-2023 (less than WIPO's 1883-2023)")
    print()

    # Ensure directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Download resident patent applications
    print("\n📊 Downloading resident patent applications...")
    df_resident = download_worldbank_indicator(
        PATENT_INDICATOR,
        output_file=OUTPUT_DIR / "worldbank_patents_resident_raw.json"
    )

    if df_resident is not None:
        output_csv = OUTPUT_DIR / "worldbank_patents_resident.csv"
        df_resident.to_csv(output_csv, index=False)
        print(f"✓ Saved to: {output_csv}")

    # Small delay to be nice to the API
    time.sleep(1)

    # Download non-resident patent applications
    print("\n📊 Downloading non-resident patent applications...")
    df_nonresident = download_worldbank_indicator(
        PATENT_NONRESIDENT,
        output_file=OUTPUT_DIR / "worldbank_patents_nonresident_raw.json"
    )

    if df_nonresident is not None:
        output_csv = OUTPUT_DIR / "worldbank_patents_nonresident.csv"
        df_nonresident.to_csv(output_csv, index=False)
        print(f"✓ Saved to: {output_csv}")

    # Combine resident and non-resident
    if df_resident is not None or df_nonresident is not None:
        print("\n📊 Combining resident and non-resident data...")

        # Add type column
        if df_resident is not None:
            df_resident['type'] = 'resident'
        if df_nonresident is not None:
            df_nonresident['type'] = 'non-resident'

        # Combine
        frames = [df for df in [df_resident, df_nonresident] if df is not None]
        df_combined = pd.concat(frames, ignore_index=True)

        # Pivot to have resident and non-resident as columns
        df_pivot = df_combined.pivot_table(
            index=['country_code', 'country_name', 'year'],
            columns='type',
            values='value',
            aggfunc='first'
        ).reset_index()

        # Calculate total
        if 'resident' in df_pivot.columns and 'non-resident' in df_pivot.columns:
            df_pivot['total'] = df_pivot['resident'].fillna(0) + df_pivot['non-resident'].fillna(0)

        output_csv = OUTPUT_DIR / "worldbank_patents_combined.csv"
        df_pivot.to_csv(output_csv, index=False)
        print(f"✓ Combined data saved: {output_csv}")
        print(f"\n  Total records: {len(df_pivot)}")
        print(f"  Countries: {df_pivot['country_code'].nunique()}")
        print(f"  Year range: {df_pivot['year'].min()} - {df_pivot['year'].max()}")

        return df_pivot

    return None


def create_collection_log(df: Optional[pd.DataFrame] = None):
    """Create a detailed log of the World Bank data collection."""

    log_file = OUTPUT_DIR / "WORLDBANK_COLLECTION_LOG.md"

    status_resident = "✓" if (OUTPUT_DIR / "worldbank_patents_resident.csv").exists() else "✗"
    status_nonresident = "✓" if (OUTPUT_DIR / "worldbank_patents_nonresident.csv").exists() else "✗"
    status_combined = "✓" if (OUTPUT_DIR / "worldbank_patents_combined.csv").exists() else "✗"

    stats = ""
    if df is not None:
        # Determine which columns are available
        value_col = 'total' if 'total' in df.columns else 'resident'

        # Get top countries data
        latest_year_df = df[df['year'] == df['year'].max()]
        if len(latest_year_df) > 0 and value_col in latest_year_df.columns:
            top_df = latest_year_df.nlargest(10, value_col)[['country_name', 'year', value_col]]
            # Create simple text table
            top_countries = "```\n"
            top_countries += f"{'Country':<40} {'Year':<6} {value_col.title():<15}\n"
            top_countries += "-" * 65 + "\n"
            for _, row in top_df.iterrows():
                top_countries += f"{row['country_name']:<40} {row['year']:<6} {row[value_col]:>15,.0f}\n"
            top_countries += "```"
        else:
            top_countries = "*Data processing in progress*"

        stats = f"""
## Data Statistics

- **Total records**: {len(df):,}
- **Countries**: {df['country_code'].nunique()}
- **Year range**: {df['year'].min()} - {df['year'].max()}
- **Years covered**: {df['year'].nunique()}
- **Average years per country**: {len(df) / df['country_code'].nunique():.1f}

### Top 10 Countries by Patents (latest year: {df['year'].max()})
{top_countries}
"""

    log_content = f"""# World Bank Patent Data Collection Log

**Date**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Component**: H₇ (Evolutionary Progression) - Patents (World Bank fallback)

## Data Source Information

### World Bank Open Data API
- **URL**: https://data.worldbank.org/indicator/IP.PAT.RESD
- **API Endpoint**: https://api.worldbank.org/v2/
- **Coverage**: 1960-2023 (63 years)
- **License**: CC-BY-4.0 (Creative Commons Attribution)
- **Update Frequency**: Annual

### Indicators Downloaded

1. **IP.PAT.RESD**: Patent applications, residents
   - Patent applications filed by residents of a country

2. **IP.PAT.NRES**: Patent applications, non-residents
   - Patent applications filed by foreign applicants

3. **Total**: Sum of resident + non-resident applications

## Collection Status

- [{status_resident}] Resident patent applications downloaded
- [{status_nonresident}] Non-resident patent applications downloaded
- [{status_combined}] Combined dataset created
- [ ] Data quality validated
- [ ] Population normalization applied
- [ ] Integration with WIPO data (if available)
{stats}

## Comparison: World Bank vs WIPO

| Aspect | World Bank | WIPO |
|--------|-----------|------|
| Coverage | 1960-2023 (63 years) | 1883-2023 (140 years) |
| Download | Automated via API ✓ | Manual selection required |
| License | CC-BY-4.0 (explicit) | Public use (attribution) |
| Update | Annual | Annual |
| Best Use | Quick automated baseline | Comprehensive historical analysis |

## Usage Recommendations

### For 1810-1959
- Use WIPO data if available (extends to 1883)
- Extrapolate backward using historical growth rates
- Consider historical patent office records

### For 1960-2023
- **Primary**: WIPO data (more comprehensive)
- **Fallback**: World Bank data (automated, reliable)
- **Validation**: Cross-check WIPO vs World Bank for overlap period

## Citation

```
The World Bank. 2024. World Development Indicators.
Patent applications, residents (IP.PAT.RESD) and non-residents (IP.PAT.NRES).
Available at: https://data.worldbank.org/indicator/IP.PAT.RESD
Accessed: {pd.Timestamp.now().strftime('%Y-%m-%d')}
License: CC-BY-4.0
```

## Next Steps

1. Download WIPO data for more comprehensive coverage (1883-2023)
2. Compare World Bank vs WIPO for 1960-2023 overlap
3. Integrate with HYDE population data
4. Calculate patents per capita by country-year
5. Normalize to [0, 1] scale
6. Aggregate to global weighted average

## Technical Notes

- World Bank API accessed via Python `requests` library
- Data returned in JSON format, parsed to CSV
- Null values excluded from analysis
- Both resident and non-resident applications captured
- Total calculated as sum of resident + non-resident

---

*This data was downloaded automatically via the World Bank API.*
*For the most comprehensive historical coverage, also download WIPO data manually.*
"""

    with open(log_file, 'w') as f:
        f.write(log_content)

    print(f"\n✓ Collection log created: {log_file}")
    return log_file


def main():
    """Main execution function."""

    print("\n🚀 Starting World Bank Patent Data Collection (Automated)")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Processed directory: {PROCESSED_DIR}")

    # Download all patent indicators
    df_combined = download_all_patent_indicators()

    # Create collection log
    create_collection_log(df_combined)

    print("\n" + "="*80)
    print("Summary")
    print("="*80)
    print()

    if df_combined is not None:
        print("✓ World Bank patent data downloaded successfully!")
        print("✓ Automated collection complete")
        print()
        print("Files created:")
        print("  - worldbank_patents_resident.csv")
        print("  - worldbank_patents_nonresident.csv")
        print("  - worldbank_patents_combined.csv")
        print("  - WORLDBANK_COLLECTION_LOG.md")
        print()
        print(f"Coverage: {df_combined['year'].min()} - {df_combined['year'].max()}")
        print(f"Countries: {df_combined['country_code'].nunique()}")
        print(f"Total records: {len(df_combined):,}")
        print()
        print("✓ This provides a working baseline for H₇ component!")
        print()
        print("Recommended next steps:")
        print("1. Download WIPO data manually for extended coverage (1883-2023)")
        print("2. Compare World Bank vs WIPO for validation")
        print("3. Proceed with other H₇ components (CCP, Barro-Lee, Infrastructure)")
    else:
        print("✗ Failed to download World Bank data")
        print()
        print("Troubleshooting:")
        print("- Check internet connection")
        print("- Verify World Bank API is accessible")
        print("- Try again in a few minutes (API may be temporarily down)")

    print()


if __name__ == "__main__":
    main()
