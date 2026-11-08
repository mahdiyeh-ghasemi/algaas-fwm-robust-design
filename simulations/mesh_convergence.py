from pathlib import Path

import pandas as pd

from src.mode_solver import solve_waveguide_modes
from src.waveguide_geometry import WAVEGUIDE


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / "mesh_convergence.csv"

GRID_SPACINGS = [0.025, 0.0125, 0.00625]


def main():
    original_spacing = WAVEGUIDE["grid_spacing_um"]
    results = []

    try:
        for spacing in GRID_SPACINGS:
            WAVEGUIDE["grid_spacing_um"] = spacing

            neff = solve_waveguide_modes()[0]

            row = {"grid_spacing_um": spacing}

            for mode_index, effective_index in enumerate(neff, start=1):
                row[f"mode_{mode_index}_neff"] = effective_index

            results.append(row)

            print(
                f"Grid spacing: {spacing:.5f} um | "
                f"Effective indices: {neff}"
            )

    finally:
        WAVEGUIDE["grid_spacing_um"] = original_spacing

    data = pd.DataFrame(results)
    data.to_csv(OUTPUT_FILE, index=False)

    print(f"\nMesh convergence results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()