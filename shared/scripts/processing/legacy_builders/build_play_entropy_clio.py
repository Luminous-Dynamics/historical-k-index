"""Placeholder script for Clio Infra occupational diversity data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

OUTPUT = Path(__file__).resolve().parent / "occupation_diversity_entropy.csv"


def main() -> None:
    years = list(range(1800, 2021, 10))
    values = [0.3 + 0.0005 * (i - 1800) for i in years]
    df = pd.DataFrame({"year": years, "value": values})
    df.to_csv(OUTPUT, index=False)
    print(f"Wrote placeholder {OUTPUT}")


if __name__ == "__main__":
    main()
