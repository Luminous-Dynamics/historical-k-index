"""Fetch global aid vs. extraction proxy from World Bank API."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

OUTPUT_PATH = Path(__file__).resolve().parent / "aid_extraction_balance.csv"


def fetch_indicator(indicator: str) -> pd.DataFrame:
    url = f"https://api.worldbank.org/v2/country/WLD/indicator/{indicator}?format=json&per_page=20000"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if len(data) < 2:
        raise RuntimeError(f"Unexpected response for {indicator}")
    rows = data[1]
    records = []
    for row in rows:
        year = row.get("date")
        value = row.get("value")
        if year is None or value is None:
            continue
        try:
            year_int = int(year)
        except ValueError:
            continue
        records.append({"year": year_int, "value": float(value)})
    df = pd.DataFrame(records).sort_values("year")
    return df


def build() -> None:
    aid = fetch_indicator("DT.ODA.ODAT.CD")  # Net official development assistance (current US$)
    extraction = fetch_indicator("BM.KLT.DINV.CD.WD")  # FDI net outflows (current US$)
    merged = pd.merge(aid, extraction, on="year", how="inner", suffixes=("_aid", "_fdi"))
    merged["balance"] = merged["value_aid"] / (merged["value_fdi"].abs() + 1e-9)
    merged = merged[(merged["year"] >= 1960) & (merged["year"] <= 2022)]
    merged = merged.dropna(subset=["balance"])

    # Convert to decadal averages to match K-config windows
    merged["decade"] = (merged["year"] // 10) * 10
    decade_series = merged.groupby("decade")["balance"].mean().reset_index()
    decade_series.rename(columns={"decade": "year", "balance": "value"}, inplace=True)
    decade_series.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    build()
