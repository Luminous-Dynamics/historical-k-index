"""Generate proxy features from Our World in Data global energy dataset."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "OWID_energy.csv"
OUTPUT_DIR = Path(__file__).resolve().parent

DECADE_YEARS = list(range(1800, 2030, 10))


def normalize(series: pd.Series, invert: bool = False) -> pd.Series:
    s = series.astype(float)
    min_val, max_val = float(np.nanmin(s)), float(np.nanmax(s))
    if np.isclose(max_val, min_val):
        norm = pd.Series(0.5, index=s.index)
    else:
        norm = (s - min_val) / (max_val - min_val)
    if invert:
        norm = 1.0 - norm
    return norm.clip(0.0, 1.0)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError("OWID_energy.csv not found. Download before running.")

    df = pd.read_csv(DATA_PATH)
    world = df[df["country"] == "World"].set_index("year")

    # Interpolate yearly values from 1800 to 2020
    numeric = world.select_dtypes(include=[np.number])
    years = np.arange(1800, 2021, 1)
    numeric = numeric.reindex(years).interpolate(limit_direction="both")

    # Helper columns
    population = numeric["population"]
    population_change = population.diff().bfill()

    mapping: Dict[str, pd.Series] = {
        "network_modularity_inverse": normalize(numeric["electricity_demand"]),
        "communication_latency_inverse": normalize(numeric["carbon_intensity_elec"], invert=True),
        "trade_network_degree": normalize(numeric["gdp"]),
        "migration_flux_index": normalize(population_change.abs()),
        "bilateral_trade_symmetry": normalize(numeric["low_carbon_electricity"]),
        "alliance_reciprocity_ratio": normalize(numeric["biofuel_share_elec"]),
        "occupation_diversity_entropy": normalize(numeric["renewables_share_elec"]),
        "innovation_field_entropy": normalize(numeric["energy_per_capita"]),
        "forecast_skill_index": normalize(numeric["energy_per_gdp"], invert=True),
        "error_correction_speed": normalize(numeric["energy_cons_change_pct"].abs()),
    }

    decade_index = pd.Index(DECADE_YEARS, name="year")
    for feature, series in mapping.items():
        decade_series = series.reindex(DECADE_YEARS).interpolate(limit_direction="both")
        df_out = pd.DataFrame({"year": decade_series.index, "value": decade_series.values.round(4)})
        path = OUTPUT_DIR / f"{feature}.csv"
        df_out.to_csv(path, index=False)
        print(f"Wrote {path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
