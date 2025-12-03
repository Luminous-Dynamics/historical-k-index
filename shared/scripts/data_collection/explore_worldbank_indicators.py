#!/usr/bin/env python3
"""
Explore World Bank Indicators for H₇ Components

This script searches World Bank indicators to find data relevant to:
- Education capital (literacy, school enrollment, attainment)
- Infrastructure density (railways, roads, electricity, telecom)
- Governance/institutions (for constitutional complexity proxy)

Author: Tristan Stoltz / Claude Code
Date: December 3, 2025
"""

import requests
import pandas as pd
from typing import List, Dict
import time

WB_BASE_URL = "https://api.worldbank.org/v2"

def search_indicators(search_terms: List[str], per_page: int = 100) -> pd.DataFrame:
    """
    Search World Bank indicators by keywords.

    Args:
        search_terms: List of keywords to search for
        per_page: Number of results per page

    Returns:
        DataFrame with matching indicators
    """

    print(f"\n{'='*80}")
    print("Searching World Bank Indicators")
    print(f"{'='*80}\n")

    all_indicators = []

    for term in search_terms:
        print(f"Searching for: '{term}'...")

        url = f"{WB_BASE_URL}/indicator"
        params = {
            'format': 'json',
            'per_page': per_page
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if len(data) < 2:
                continue

            indicators = data[1]

            # Filter by search term in name or description
            matching = []
            for ind in indicators:
                if ind is None:
                    continue

                name = ind.get('name', '').lower()
                desc = ind.get('sourceNote', '').lower()
                ind_id = ind.get('id', '')

                if term.lower() in name or term.lower() in desc:
                    matching.append({
                        'id': ind_id,
                        'name': ind.get('name'),
                        'description': desc[:200] + '...' if len(desc) > 200 else desc,
                        'source': ind.get('source', {}).get('value', 'Unknown'),
                        'search_term': term
                    })

            all_indicators.extend(matching)
            print(f"  Found {len(matching)} matching indicators")

            time.sleep(0.5)  # Be nice to the API

        except Exception as e:
            print(f"  Error searching for '{term}': {e}")
            continue

    return pd.DataFrame(all_indicators)


def find_h7_indicators():
    """Find World Bank indicators relevant to H₇ components."""

    print("\n" + "="*80)
    print("H₇ Component Indicator Search")
    print("="*80)

    # Define search terms for each H₇ sub-component
    search_categories = {
        'Education': [
            'literacy',
            'school enrollment',
            'educational attainment',
            'mean years schooling',
            'secondary education',
            'tertiary education'
        ],
        'Infrastructure': [
            'railway',
            'road',
            'electricity',
            'telephone',
            'internet',
            'mobile',
            'transport',
            'energy access'
        ],
        'Governance': [
            'government effectiveness',
            'rule of law',
            'regulatory quality',
            'control of corruption',
            'voice accountability'
        ]
    }

    results = {}

    for category, terms in search_categories.items():
        print(f"\n{'='*80}")
        print(f"Category: {category}")
        print(f"{'='*80}")

        df = search_indicators(terms)

        if len(df) > 0:
            print(f"\n✓ Found {len(df)} total indicators for {category}")
            print(f"\nTop matches:")
            for i, row in df.head(10).iterrows():
                print(f"\n  {row['id']}: {row['name']}")
                print(f"  Description: {row['description'][:100]}...")
        else:
            print(f"\n✗ No indicators found for {category}")

        results[category] = df

    return results


def main():
    """Main execution function."""

    print("\n🔍 Exploring World Bank Indicators for H₇ Components")
    print("="*80)
    print()
    print("This script will search for indicators related to:")
    print("  1. Education capital (literacy, enrollment, attainment)")
    print("  2. Infrastructure density (transport, energy, telecom)")
    print("  3. Governance quality (proxy for constitutional complexity)")
    print()
    print("Note: This is exploratory - we'll download the most relevant ones")
    print()

    # Search for relevant indicators
    results = find_h7_indicators()

    # Save results
    output_file = "data/raw/worldbank_indicator_search_results.csv"

    all_results = pd.concat(results.values(), ignore_index=True)

    if len(all_results) > 0:
        all_results.to_csv(output_file, index=False)
        print(f"\n✓ Results saved to: {output_file}")
        print(f"  Total indicators found: {len(all_results)}")

        # Summary by category
        print("\nSummary by category:")
        for category, df in results.items():
            print(f"  {category}: {len(df)} indicators")
    else:
        print("\n✗ No indicators found")

    print()


if __name__ == "__main__":
    main()
