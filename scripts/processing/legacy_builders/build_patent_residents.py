"""Fetch global patent resident filings from World Bank API."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

OUTPUT = Path(__file__).resolve().parent / "patent_resident_filings.csv"


def fetch() -> pd.DataFrame:
    url = "https://api.worldbank.org/v2/country/WLD/indicator/IP.PAT.RESD?format=json&per_page=20000"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    rows = data[1]
    records = []
    for row in rows:
        year = row.get("date")
        val = row.get("value")
        if year is None or val is None:
            continue
        try:
            records.append({"year": int(year), "value": float(val)})
        except ValueError:
            continue
    return pd.DataFrame(records).sort_values("year")


def main() -> None:
    df = fetch()
    df = df[(df["year"] >= 1960) & (df["year"] <= 2022)]
    df["decade"] = (df["year"] // 10) * 10
    decade = df.groupby("decade")["value"].mean().reset_index()
    decade.rename(columns={"decade": "year"}, inplace=True)
    decade.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
