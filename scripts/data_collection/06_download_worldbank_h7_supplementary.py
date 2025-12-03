#!/usr/bin/env python3
"""
Download World Bank Indicators for H₇ Components

This script downloads additional World Bank indicators that can supplement
or serve as proxies for H₇ components:
- Education: Literacy rates, school enrollment, mean years of schooling
- Infrastructure: Electricity access, mobile subscriptions, internet access
- Governance: Government effectiveness, rule of law (proxy for constitutional quality)

Author: Tristan Stoltz / Claude Code
Date: December 3, 2025
"""

import pandas as pd
import requests
from pathlib import Path
import time
from typing import Optional, Dict, List

# Configuration
OUTPUT_DIR = Path("data/raw/worldbank_supplementary")
PROCESSED_DIR = Path("data/processed/H7_components")

WB_BASE_URL = "https://api.worldbank.org/v2"

# Well-known World Bank indicator codes relevant to H₇
H7_INDICATORS = {
    'education': {
        'SE.ADT.LITR.ZS': 'Literacy rate, adult total (% of people ages 15 and above)',
        'SE.ADT.LITR.FE.ZS': 'Literacy rate, adult female (% of females ages 15 and above)',
        'SE.ADT.LITR.MA.ZS': 'Literacy rate, adult male (% of males ages 15 and above)',
        'SE.PRM.ENRR': 'School enrollment, primary (% gross)',
        'SE.SEC.ENRR': 'School enrollment, secondary (% gross)',
        'SE.TER.ENRR': 'School enrollment, tertiary (% gross)',
        'BAR.SCHL.15UP': 'Barro-Lee: Average years of schooling, age 15+ (years)',
    },
    'infrastructure': {
        'EG.ELC.ACCS.ZS': 'Access to electricity (% of population)',
        'IT.CEL.SETS.P2': 'Mobile cellular subscriptions (per 100 people)',
        'IT.NET.USER.ZS': 'Individuals using the Internet (% of population)',
        'IS.RRS.TOTL.KM': 'Rail lines (total route-km)',
        'IS.ROD.TOTL.KM': 'Roads, total network (km)',
    },
    'governance': {
        'CC.EST': 'Control of Corruption: Estimate',
        'GE.EST': 'Government Effectiveness: Estimate',
        'PV.EST': 'Political Stability and Absence of Violence/Terrorism: Estimate',
        'RQ.EST': 'Regulatory Quality: Estimate',
        'RL.EST': 'Rule of Law: Estimate',
        'VA.EST': 'Voice and Accountability: Estimate',
    }
}


def download_indicator(indicator_code: str, indicator_name: str,
                       start_year: int = 1960, end_year: int = 2023) -> Optional[pd.DataFrame]:
    """
    Download a single World Bank indicator.

    Args:
        indicator_code: World Bank indicator code
        indicator_name: Human-readable name
        start_year: Start year
        end_year: End year

    Returns:
        DataFrame with data or None if failed
    """

    print(f"\n  Downloading: {indicator_code}")
    print(f"  Name: {indicator_name}")

    url = f"{WB_BASE_URL}/country/all/indicator/{indicator_code}"
    params = {
        'date': f'{start_year}:{end_year}',
        'format': 'json',
        'per_page': 20000
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if len(data) < 2 or data[1] is None:
            print(f"  ✗ No data available")
            return None

        records = data[1]

        # Parse into DataFrame
        rows = []
        for record in records:
            if record['value'] is not None:
                rows.append({
                    'indicator_code': indicator_code,
                    'indicator_name': indicator_name,
                    'country_code': record['countryiso3code'],
                    'country_name': record['country']['value'],
                    'year': int(record['date']),
                    'value': float(record['value'])
                })

        df = pd.DataFrame(rows)

        if len(df) > 0:
            print(f"  ✓ {len(df)} data points | {df['country_code'].nunique()} countries | {df['year'].min()}-{df['year'].max()}")
            return df
        else:
            print(f"  ✗ No valid data points")
            return None

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def download_category(category: str, indicators: Dict[str, str]) -> Optional[pd.DataFrame]:
    """Download all indicators for a category."""

    print(f"\n{'='*80}")
    print(f"Category: {category.upper()}")
    print(f"{'='*80}")
    print(f"Downloading {len(indicators)} indicators...")

    all_data = []

    for code, name in indicators.items():
        df = download_indicator(code, name)

        if df is not None:
            all_data.append(df)

        time.sleep(0.5)  # Be nice to API

    if len(all_data) > 0:
        combined = pd.concat(all_data, ignore_index=True)
        print(f"\n✓ Category complete: {len(combined)} total data points")
        return combined
    else:
        print(f"\n✗ No data downloaded for {category}")
        return None


def main():
    """Main execution function."""

    print("\n🌍 Downloading World Bank H₇ Supplementary Indicators")
    print("="*80)
    print()
    print("This script downloads indicators that can supplement H₇ components:")
    print("  • Education: Literacy, enrollment, years of schooling")
    print("  • Infrastructure: Electricity, mobile, internet, transport")
    print("  • Governance: Control of corruption, rule of law, effectiveness")
    print()

    # Ensure directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    results = {}

    # Download each category
    for category, indicators in H7_INDICATORS.items():
        df = download_category(category, indicators)

        if df is not None:
            # Save category data
            output_file = OUTPUT_DIR / f"worldbank_{category}.csv"
            df.to_csv(output_file, index=False)
            print(f"✓ Saved: {output_file}")

            results[category] = df

    # Create summary
    print("\n" + "="*80)
    print("Download Summary")
    print("="*80)
    print()

    total_indicators = sum(len(indicators) for indicators in H7_INDICATORS.values())
    successful = len(results)

    for category, df in results.items():
        print(f"{category.title()}:")
        print(f"  Data points: {len(df):,}")
        print(f"  Countries: {df['country_code'].nunique()}")
        print(f"  Year range: {df['year'].min()} - {df['year'].max()}")
        print(f"  Indicators: {df['indicator_code'].nunique()}")
        print()

    print(f"✓ Downloaded {successful} of {len(H7_INDICATORS)} categories")
    print(f"✓ Total data points: {sum(len(df) for df in results.values()):,}")
    print()

    if successful > 0:
        print("Next steps:")
        print("1. Process education indicators into education capital measure")
        print("2. Process infrastructure indicators into composite index")
        print("3. Process governance indicators as constitutional quality proxy")
        print("4. Integrate with other H₇ components")
    else:
        print("No data downloaded. Check internet connection and try again.")

    print()


if __name__ == "__main__":
    main()
