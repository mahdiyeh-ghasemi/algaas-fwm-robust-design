from pathlib import Path

import numpy as np
import pandas as pd

from src.mode_solver import solve_waveguide_modes


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / "dispersion_data.csv"


def main():
    wavelengths_um = np.linspace(1.50, 1.60, 21)

    effective_indices = []

    for wavelength in wavelengths_um:
        result = solve_waveguide_modes(wavelength_um=wavelength)
        neff = result[0]

        effective_indices.append(neff[0])

        print(
            f"Wavelength: {wavelength:.3f} um | "
            f"Mode 1 neff: {neff[0]:.8f}"
        )

    data = pd.DataFrame({
        "wavelength_nm": wavelengths_um * 1000,
        "n_eff": effective_indices,
    })

    data.to_csv(OUTPUT_FILE, index=False)

    print(f"\nDispersion data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()