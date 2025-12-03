"""Download global trade volume (Imports + Exports) from World Bank WDI."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

OUTPUT = Path(__file__).resolve().parent / "global_trade_volume.csv"
INDICATORS = {
    "imports": "NE.IMP.GNFS.CD",  # Imports of goods and services (current US$)
    "exports": "NE.EXP.GNFS.CD",  # Exports of goods and services (current US$)
}
# Use '1W' for 'World' aggregate
COUNTRY_CODE = "1W"
API_URL = "https://api.worldbank.org/v2/country"


def fetch(
    indicator: str, year_from: int = 1960, year_to: int = 2022
) -> pd.DataFrame:
    """Fetch a single indicator for the World from WDI."""
    url = (
        f"{API_URL}/{COUNTRY_CODE}/indicator/{indicator}"
        f"?date={year_from}:{year_to}&format=json&per_page=100"
    )
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if not data or len(data) < 2 or data[1] is None:
        raise RuntimeError(f"No data returned for indicator {indicator}")

    records = []
    for row in data[1]:
        year = row.get("date")
        value = row.get("value")
        if year is None or value is None:
            continue
        records.append({"year": int(year), "value": float(value)})

    return pd.DataFrame(records).sort_values("year")


def main() -> None:
    """Fetch imports and exports, sum them, and save."""
    try:
        df_imports = fetch(INDICATORS["imports"])
        df_exports = fetch(INDICATORS["exports"])
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return

    if df_imports.empty or df_exports.empty:
        raise RuntimeError("Empty dataset returned from World Bank API")

    df = pd.merge(df_imports, df_exports, on="year", suffixes=("_imp", "_exp"))
    df["value"] = df["value_imp"] + df["value_exp"]
    df = df[["year", "value"]]

    df["decade"] = (df["year"] // 10) * 10
    decade = df.groupby("decade")["value"].sum().reset_index()
    decade.rename(columns={"decade": "year"}, inplace=True)
    decade.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
