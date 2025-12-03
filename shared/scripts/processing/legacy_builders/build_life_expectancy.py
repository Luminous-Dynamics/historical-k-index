"""Fetch global life expectancy from Our World In Data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

OUTPUT = Path(__file__).resolve().parent / "life_expectancy_global.csv"
OWID_URL = "https://ourworldindata.org/grapher/life-expectancy.csv"


def main() -> None:
    df = pd.read_csv(OWID_URL)
    if df.empty:
        raise RuntimeError("Life expectancy dataset empty")
    world = df[df["Entity"] == "World"][['Year', 'Period life expectancy at birth']]  # type: ignore[index]
    world.rename(columns={"Year": "year", "Period life expectancy at birth": "value"}, inplace=True)
    world = world[(world["year"] >= 1800) & (world["year"] <= 2022)]
    world["decade"] = (world["year"] // 10) * 10
    decade = world.groupby("decade")["value"].mean().reset_index()
    decade.rename(columns={"decade": "year"}, inplace=True)
    decade.to_csv(OUTPUT, index=False)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
