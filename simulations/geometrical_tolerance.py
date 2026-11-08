from pathlib import Path

import pandas as pd

from src.mode_solver import solve_waveguide_modes
from src.waveguide_geometry import WAVEGUIDE


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / "geometrical_tolerance.csv"

BASE_WIDTH = 0.75
BASE_THICKNESS = 0.35

WIDTH_VARIATIONS = [-0.02, -0.01, 0.0, 0.01, 0.02]
THICKNESS_VARIATIONS = [-0.02, -0.01, 0.0, 0.01, 0.02]


def run_sweep(parameter, variations):
    results = []

    for variation in variations:
        if parameter == "width":
            WAVEGUIDE["width_um"] = BASE_WIDTH + variation
            WAVEGUIDE["core_thickness_um"] = BASE_THICKNESS
            actual_value = WAVEGUIDE["width_um"]

        else:
            WAVEGUIDE["width_um"] = BASE_WIDTH
            WAVEGUIDE["core_thickness_um"] = BASE_THICKNESS + variation
            actual_value = WAVEGUIDE["core_thickness_um"]

        neff = solve_waveguide_modes()[0]

        row = {
            "parameter": parameter,
            "geometry_um": actual_value,
            "variation_um": variation,
        }

        for mode_index, effective_index in enumerate(neff, start=1):
            row[f"mode_{mode_index}_neff"] = effective_index

        results.append(row)

        print(
            f"{parameter}: {actual_value:.4f} um | "
            f"Effective indices: {neff}"
        )

    return results


def main():
    original_width = WAVEGUIDE["width_um"]
    original_thickness = WAVEGUIDE["core_thickness_um"]

    try:
        results = []

        results.extend(
            run_sweep("width", WIDTH_VARIATIONS)
        )

        results.extend(
            run_sweep("thickness", THICKNESS_VARIATIONS)
        )

    finally:
        WAVEGUIDE["width_um"] = original_width
        WAVEGUIDE["core_thickness_um"] = original_thickness

    data = pd.DataFrame(results)
    data.to_csv(OUTPUT_FILE, index=False)

    print(f"\nGeometrical tolerance results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()