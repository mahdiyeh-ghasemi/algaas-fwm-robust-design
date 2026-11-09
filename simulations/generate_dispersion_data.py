
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.mode_solver import solve_waveguide_modes


ROOT_DIR = Path(__file__).resolve().parents[1]
DISPERSION_FILE = ROOT_DIR / "dispersion_data.csv"
CONTINUITY_FILE = ROOT_DIR / "modal_continuity.csv"


def normalized_field_overlap(field_a, field_b):
    """
    Calculate normalized squared overlap between two vector
    electric fields defined on the same spatial grid.
    """

    inner_product = np.sum(
        np.conjugate(field_a) * field_b
    )

    norm_a = np.sum(np.abs(field_a) ** 2)
    norm_b = np.sum(np.abs(field_b) ** 2)

    denominator = norm_a * norm_b

    if denominator <= 0:
        raise ValueError("A field has zero or invalid norm.")

    overlap = np.abs(inner_product) ** 2 / denominator

    return float(np.clip(overlap.real, 0.0, 1.0))


def electric_field_vector(Ex, Ey, Ez, mode_index):
    """
    Assemble the three electric-field components of one mode.
    """

    return np.stack(
        [
            Ex[:, :, mode_index],
            Ey[:, :, mode_index],
            Ez[:, :, mode_index],
        ],
        axis=-1,
    )


def main():
    wavelengths_um = np.linspace(1.50, 1.60, 21)

    effective_indices = []
    continuity_results = []

    previous_field = None
    previous_wavelength = None

    for wavelength in wavelengths_um:

        result = solve_waveguide_modes(
            wavelength_um=wavelength
        )

        neff, Ex, Ey, Ez = result[:4]

        current_field = electric_field_vector(
            Ex, Ey, Ez, mode_index=0
        )

        effective_indices.append(neff[0])

        if previous_field is not None:

            overlap = normalized_field_overlap(
                previous_field,
                current_field,
            )

            continuity_results.append({
                "wavelength_1_nm": previous_wavelength * 1000,
                "wavelength_2_nm": wavelength * 1000,
                "mode_1_neff": effective_indices[-2],
                "mode_2_neff": neff[0],
                "normalized_squared_overlap": overlap,
            })

            print(
                f"{previous_wavelength:.3f} -> {wavelength:.3f} um | "
                f"Mode 1 overlap: {overlap:.8f}"
            )

        print(
            f"Wavelength: {wavelength:.3f} um | "
            f"Mode 1 neff: {neff[0]:.8f}"
        )

        previous_field = current_field.copy()
        previous_wavelength = wavelength

    dispersion_data = pd.DataFrame({
        "wavelength_nm": wavelengths_um * 1000,
        "n_eff": effective_indices,
    })

    continuity_data = pd.DataFrame(continuity_results)

    dispersion_data.to_csv(
        DISPERSION_FILE,
        index=False,
    )

    continuity_data.to_csv(
        CONTINUITY_FILE,
        index=False,
    )

    print(f"\nDispersion data saved to: {DISPERSION_FILE}")
    print(f"Modal continuity data saved to: {CONTINUITY_FILE}")

    print(
        "\nMinimum adjacent-wavelength overlap:",
        f"{continuity_data['normalized_squared_overlap'].min():.8f}",
    )


if __name__ == "__main__":
    main()
