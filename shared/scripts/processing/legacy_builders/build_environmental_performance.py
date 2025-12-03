"""Fetch electricity use per capita (World Bank) and derive environmental performance index."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

OUTPUT = Path(__file__).resolve().parent / "environmental_performance_index.csv"
API_URL = (
    "https://api.worldbank.org/v2/country/all/indicator/EG.USE.ELEC.KH.PC"
    "?format=json&per_page=20000"
)


def main() -> None:
    resp = requests.get(API_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if not data or len(data) < 2 or not data[1]:
        raise RuntimeError("No electricity data fetched")

    records = []
    for row in data[1]:
        year = row.get("date")
        value = row.get("value")
        if year is None or value is None:
            continue
        records.append({"year": int(year), "elec_per_cap": float(value)})

    if not records:
        raise RuntimeError("No valid electricity records")

    df = pd.DataFrame(records).sort_values("year")
    df_mean = df.groupby("year")["elec_per_cap"].mean().reset_index()
    df_mean = df_mean[(df_mean["year"] >= 1960) & (df_mean["year"] <= 2022)]
    if df_mean.empty:
        raise RuntimeError("No data in selected period")

    max_val = df_mean["elec_per_cap"].max()
    df_mean["value"] = 1.0 - df_mean["elec_per_cap"] / max_val
    df_mean["value"] = df_mean["value"].clip(lower=0.0)

    df_mean["decade"] = (df_mean["year"] // 10) * 10
    decade = df_mean.groupby("decade")["value"].mean().reset_index()
    decade.rename(columns={"decade": "year"}, inplace=True)
    decade.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
