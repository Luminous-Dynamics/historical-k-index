#!/usr/bin/env python3
"""
Construct Infrastructure Density Index for H₇ Component

This script combines multiple infrastructure indicators to measure
technological and physical capacity of civilizations over time.

Data Sources:
- Railway density: International Railway Statistics
- Road density: World Bank, historical estimates
- Electricity access: World Bank, IEA
- Telecommunications: ITU, historical estimates

Author: Tristan Stoltz / Claude Code
Date: December 2, 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Configuration
OUTPUT_DIR = Path("data/raw/infrastructure")
PROCESSED_DIR = Path("data/processed/H7_components")


def collect_infrastructure_data():
    """
    Infrastructure data comes from multiple sources and needs integration.
    """

    print("=" * 80)
    print("Infrastructure Density Data Collection")
    print("=" * 80)
    print()
    print("Multiple data sources required:")
    print()

    print("1. Railway Density (1830-2023):")
    print("   - International Union of Railways (UIC)")
    print("   - https://uic.org/statistics")
    print("   - Historical estimates from Mitchell (1998)")
    print()

    print("2. Road Density (1900-2023):")
    print("   - World Bank: IS.ROD.TOTL.KM")
    print("   - https://data.worldbank.org/indicator/IS.ROD.TOTL.KM")
    print()

    print("3. Electricity Access (1880-2023):")
    print("   - World Bank: EG.ELC.ACCS.ZS")
    print("   - https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS")
    print("   - Historical: IEA electricity statistics")
    print()

    print("4. Telecommunications (1850-2023):")
    print("   - ITU: Fixed telephone subscriptions")
    print("   - Historical: Telegraph network coverage")
    print()

    print("Save downloaded files to: data/raw/infrastructure/")
    print()

    return True


def construct_infrastructure_index():
    """
    Combine multiple infrastructure indicators into single index.

    Time Period Approach:
    - 1810-1830: Minimal infrastructure (baseline ~0.01)
    - 1830-1900: Railways dominate, some telegraph
    - 1900-1950: Railways + roads + electricity beginning
    - 1950-2000: All four components
    - 2000-2023: Modern infrastructure (near maximum)

    Formula:
    Infrastructure(t) = weighted_mean([
        railways_per_capita(t),
        roads_per_capita(t),
        electricity_access(t),
        telecom_density(t)
    ])

    Weights adapt based on what's available/relevant in each period.
    """

    print("\n" + "=" * 80)
    print("Constructing Infrastructure Index")
    print("=" * 80)
    print()

    # Placeholder structure - actual implementation depends on collected data
    infrastructure_components = {
        '1810-1830': {
            'railways': 0.0,
            'roads': 0.01,
            'electricity': 0.0,
            'telecom': 0.0,
            'weight': [0.0, 1.0, 0.0, 0.0]
        },
        '1830-1900': {
            'railways': 'to_be_calculated',
            'roads': 'to_be_calculated',
            'electricity': 0.0,
            'telecom': 'to_be_calculated',
            'weight': [0.6, 0.2, 0.0, 0.2]
        },
        '1900-1950': {
            'railways': 'to_be_calculated',
            'roads': 'to_be_calculated',
            'electricity': 'to_be_calculated',
            'telecom': 'to_be_calculated',
            'weight': [0.3, 0.3, 0.2, 0.2]
        },
        '1950-2023': {
            'railways': 'to_be_calculated',
            'roads': 'to_be_calculated',
            'electricity': 'to_be_calculated',
            'telecom': 'to_be_calculated',
            'weight': [0.2, 0.3, 0.3, 0.2]
        }
    }

    print("Infrastructure index will combine:")
    print("- Railway density (km per capita)")
    print("- Road density (km per capita)")
    print("- Electricity access (% population)")
    print("- Telecommunications density (connections per capita)")
    print()
    print("Weights will adapt based on historical relevance.")
    print()

    return infrastructure_components


def create_infrastructure_collection_log():
    """Create documentation log."""

    log_file = OUTPUT_DIR / "DATA_COLLECTION_LOG.md"

    log_content = f"""# Infrastructure Density Data Collection Log

**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
**Component:** H₇ (Evolutionary Progression) - Infrastructure Density

## Data Source Information

### 1. Railway Statistics
**Primary:** International Union of Railways (UIC)
- **URL:** https://uic.org/statistics
- **Coverage:** 1950-2023
- **Variables:** Railway length, passengers, freight

**Historical:** Mitchell, B.R. (1998) International Historical Statistics
- Coverage: 1830-1998
- Source: University libraries, Cambridge University Press

### 2. Road Statistics
**Primary:** World Bank Indicator IS.ROD.TOTL.KM
- **URL:** https://data.worldbank.org/indicator/IS.ROD.TOTL.KM
- **Coverage:** 1990-2023
- **Variables:** Total road network (km)

**Historical:** IRF World Road Statistics
- Coverage: 1960-2023
- International Road Federation

### 3. Electricity Access
**Primary:** World Bank Indicator EG.ELC.ACCS.ZS
- **URL:** https://data.worldbank.org/indicator/EG.ELC.ACCS.ZS
- **Coverage:** 1990-2023
- **Variables:** % population with electricity access

**Historical:** IEA Electricity Information
- Coverage: 1971-2023
- International Energy Agency

### 4. Telecommunications
**Primary:** ITU World Telecommunication Indicators
- **URL:** https://www.itu.int/en/ITU-D/Statistics/
- **Coverage:** 1960-2023
- **Variables:** Fixed telephone subscriptions, mobile, internet

**Historical:** Historical telegraph and telephone records
- Coverage: 1850-1960
- Various national sources

## Infrastructure Index Formula

```python
# Time-adaptive weights
if year < 1830:
    infrastructure = 0.01  # Baseline (roads only)
elif year < 1900:
    infrastructure = 0.6*railways + 0.2*roads + 0.2*telegraph
elif year < 1950:
    infrastructure = 0.3*railways + 0.3*roads + 0.2*electricity + 0.2*telecom
else:
    infrastructure = 0.2*railways + 0.3*roads + 0.3*electricity + 0.2*telecom
```

## Collection Status

- [ ] Railway data collected (UIC, Mitchell)
- [ ] Road data collected (World Bank, IRF)
- [ ] Electricity data collected (World Bank, IEA)
- [ ] Telecommunications data collected (ITU)
- [ ] Historical estimates integrated
- [ ] Per capita calculations complete
- [ ] Global aggregate calculated
- [ ] Normalization to [0,1] complete

## Per Capita Normalization

All infrastructure metrics normalized per capita or per unit area:
- Railways: km per 1000 people
- Roads: km per 1000 people
- Electricity: % access (already per capita)
- Telecom: subscriptions per 100 people

## Historical Challenges

**1810-1830:** Minimal infrastructure
- Roads exist but unmeasured
- Use constant baseline (~0.01)

**1830-1900:** Railway era
- Good railway data available
- Roads poorly documented
- Telegraph expanding but data sparse

**1900-1950:** Multi-modal transition
- Good data for all components
- Challenge: Integrate WWII disruptions

**1950-2023:** Modern infrastructure
- Excellent data availability
- Challenge: Shift from physical to digital infrastructure

## Citations

```
# Railways
International Union of Railways (UIC). 2024.
Railway Statistics. Paris: UIC.

Mitchell, B. R. 1998.
International Historical Statistics: Europe, 1750-1993.
London: Macmillan Reference.

# Roads
World Bank. 2024. World Development Indicators.
Indicator: IS.ROD.TOTL.KM (Total road network, km)

# Electricity
World Bank. 2024. World Development Indicators.
Indicator: EG.ELC.ACCS.ZS (Access to electricity, % population)

International Energy Agency. 2024.
IEA Electricity Information Statistics.

# Telecommunications
International Telecommunication Union (ITU). 2024.
World Telecommunication/ICT Indicators Database.
Geneva: ITU.
```

## Next Steps

1. Collect data from each source (4 components)
2. Harmonize to common country-year panel
3. Calculate per capita metrics
4. Apply time-adaptive weighting
5. Aggregate to global average
6. Save as `data/processed/H7_components/infrastructure.csv`
"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w') as f:
        f.write(log_content)

    print(f"✓ Collection log created: {log_file}")
    return log_file


def main():
    """Main execution."""

    print("\n🏗️ Starting Infrastructure Density Index Construction")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Processed directory: {PROCESSED_DIR}")
    print()

    # Ensure directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Document data sources
    collect_infrastructure_data()

    # Explain index construction
    construct_infrastructure_index()

    # Create collection log
    log_file = create_infrastructure_collection_log()

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)
    print()
    print("✓ Directory structure ready")
    print("✓ Data collection log created")
    print()
    print("Infrastructure index requires multiple data sources:")
    print("- Railway statistics (UIC, Mitchell)")
    print("- Road statistics (World Bank)")
    print("- Electricity access (World Bank, IEA)")
    print("- Telecommunications (ITU)")
    print()
    print("This is the most complex H₇ component to construct.")
    print("Consider using simplified proxy if full data not available.")
    print()


if __name__ == "__main__":
    main()
