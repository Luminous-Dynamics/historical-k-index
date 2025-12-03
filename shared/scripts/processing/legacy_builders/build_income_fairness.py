"""
Fetch Gini coefficients for all countries from World Bank WDI,
calculate the global mean, and convert to a fairness index.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

OUTPUT = Path(__file__).resolve().parent / "income_fairness_index.csv"
API_URL = (
    "https://api.worldbank.org/v2/country/all/indicator/SI.POV.GINI"
    "?format=json&per_page=20000"
)


def main() -> None:
    """Fetch, process, and save Gini data as fairness index."""
    try:
        resp = requests.get(API_URL, timeout=60)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        raise RuntimeError("API request failed") from e

    if not data or len(data) < 2 or not data[1]:
        raise RuntimeError("No Gini data fetched from World Bank (country/all)")

    records = []
    for row in data[1]:
        year = row.get("date")
        value = row.get("value")
        if year is None or value is None:
            continue
        records.append({"year": int(year), "gini": float(value)})

    if not records:
        raise RuntimeError("No valid GINI records found in API response")

    df = pd.DataFrame(records).sort_values("year")
    df_mean = df.groupby("year")["gini"].mean().reset_index()

    df_mean = df_mean[(df_mean["year"] >= 1960) & (df_mean["year"] <= 2022)]
    if df_mean.empty:
        raise RuntimeError("No Gini data found for the period 1960-2022")

    df_mean["fairness"] = 1.0 - (df_mean["gini"] / 100.0)

    df_mean["decade"] = (df_mean["year"] // 10) * 10
    decade = df_mean.groupby("decade")["fairness"].mean().reset_index()
    decade.rename(columns={"decade": "year", "fairness": "value"}, inplace=True)
    decade.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
