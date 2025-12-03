"""Fetch global education index (Enrolment-based proxy)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

OUTPUT = Path(__file__).resolve().parent / "education_enrolment_index.csv"
API_URL = (
    "https://api.worldbank.org/v2/country/all/indicator/SE.SCH.LIFE"
    "?format=json&per_page=20000"
)


def main() -> None:
    resp = requests.get(API_URL, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if not data or len(data) < 2 or not data[1]:
        raise RuntimeError("No education data fetched")

    records = []
    for row in data[1]:
        year = row.get("date")
        value = row.get("value")
        if year is None or value is None:
            continue
        records.append({"year": int(year), "school_life": float(value)})

    if not records:
        raise RuntimeError("No valid records")

    df = pd.DataFrame(records).sort_values("year")
    df_mean = df.groupby("year")["school_life"].mean().reset_index()
    df_mean = df_mean[(df_mean["year"] >= 1960) & (df_mean["year"] <= 2022)]
    if df_mean.empty:
        raise RuntimeError("No data in selected period")

    max_val = df_mean["school_life"].max()
    df_mean["index"] = df_mean["school_life"] / max_val

    df_mean["decade"] = (df_mean["year"] // 10) * 10
    decade = df_mean.groupby("decade")["index"].mean().reset_index()
    decade.rename(columns={"decade": "year", "index": "value"}, inplace=True)
    decade.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
