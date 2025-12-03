"""Fetch global indicators from World Bank API and generate proxy CSVs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict
from urllib.request import urlopen

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent
DECADE_YEARS = list(range(1800, 2030, 10))


INDICATORS: Dict[str, str] = {
    "trade_share_gdp": "NE.TRD.GNFS.ZS",  # Trade (% of GDP)
    "net_migration": "SM.POP.NETM",      # Net migration
    "remittance_inflows": "BX.TRF.PWKR.CD.DT",  # Personal remittances (current US$)
}


def fetch_indicator(indicator: str) -> pd.Series:
    url = f"https://api.worldbank.org/v2/country/WLD/indicator/{indicator}?format=json&per_page=2000"
    with urlopen(url) as response:
        payload = json.load(response)
    records = payload[1]
    data = {
        int(item["date"]): float(item["value"])
        for item in records
        if item["value"] is not None
    }
    series = pd.Series(data).sort_index()
    # Convert to numeric index (year) and ensure floats
    series.index = series.index.astype(int)
    return series


def resample_to_decades(series: pd.Series) -> pd.Series:
    if series.empty:
        return pd.Series(np.zeros(len(DECADE_YEARS)), index=DECADE_YEARS)
    # Interpolate annual between first and last year, then reindex to decades
    start, end = series.index.min(), series.index.max()
    annual_index = np.arange(start, end + 1)
    annual = series.reindex(annual_index).astype(float)
    annual = annual.interpolate(limit_direction="both")
    decade_series = annual.reindex(DECADE_YEARS).interpolate(limit_direction="both")
    return decade_series.astype(float)


def normalize(series: pd.Series, invert: bool = False) -> pd.Series:
    arr = series.to_numpy(dtype=float)
    if np.allclose(arr.max(), arr.min()):
        norm = np.full_like(arr, 0.5)
    else:
        norm = (arr - arr.min()) / (arr.max() - arr.min())
    if invert:
        norm = 1.0 - norm
    return pd.Series(norm, index=series.index).clip(0.0, 1.0)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name, code in INDICATORS.items():
        try:
            raw = fetch_indicator(code)
        except Exception as exc:  # noqa: BLE001
            print(f"Failed to fetch {code}: {exc}")
            continue
        decade_series = resample_to_decades(raw)
        norm_series = normalize(decade_series)
        df = pd.DataFrame({"year": norm_series.index, "value": norm_series.values.round(4)})
        path = DATA_DIR / f"{name}.csv"
        df.to_csv(path, index=False)
        print(f"Wrote {path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
