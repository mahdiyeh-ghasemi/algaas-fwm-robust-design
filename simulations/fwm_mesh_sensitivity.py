from pathlib import Path

import numpy as np
import pandas as pd

from src.mode_solver import solve_waveguide_modes
from src.waveguide_geometry import WAVEGUIDE


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / "fwm_mesh_sensitivity.csv"

C = 299792458.0
PUMP_WAVELENGTH_NM = 1550.0
SIGNAL_DETUNING_THZ = 1.0

WAVELENGTHS_UM = np.linspace(1.50, 1.60, 21)

GRID_SPACINGS = [0.0125, 0.00625]

GEOMETRIES = [
    ("nominal", 0.75, 0.35),
    ("width_minus", 0.74, 0.35),
    ("thickness_minus", 0.75, 0.34),
]


def calculate_phase_mismatch():
    effective_indices = []

    for wavelength_um in WAVELENGTHS_UM:
        result = solve_waveguide_modes(wavelength_um=wavelength_um)
        effective_indices.append(float(result[0][0]))

    wavelength_m = WAVELENGTHS_UM * 1e-6
    beta = (
        2.0 * np.pi * np.array(effective_indices)
        / wavelength_m
    )

    pump_m = PUMP_WAVELENGTH_NM * 1e-9
    omega_p = 2.0 * np.pi * C / pump_m

    omega_s = omega_p + 2.0 * np.pi * SIGNAL_DETUNING_THZ * 1e12
    omega_i = 2.0 * omega_p - omega_s

    signal_m = 2.0 * np.pi * C / omega_s
    idler_m = 2.0 * np.pi * C / omega_i

    beta_p = np.interp(pump_m, wavelength_m, beta)
    beta_s = np.interp(signal_m, wavelength_m, beta)
    beta_i = np.interp(idler_m, wavelength_m, beta)

    return 2.0 * beta_p - beta_s - beta_i


def main():
    original_geometry = WAVEGUIDE.copy()
    results = []

    try:
        for spacing in GRID_SPACINGS:
            WAVEGUIDE.update(original_geometry)
            WAVEGUIDE["grid_spacing_um"] = spacing

            for name, width, thickness in GEOMETRIES:
                WAVEGUIDE["width_um"] = width
                WAVEGUIDE["core_thickness_um"] = thickness

                print(
                    f"\nGrid: {spacing:.5f} um | "
                    f"Geometry: {name}"
                )

                delta_beta = calculate_phase_mismatch()

                results.append({
                    "grid_spacing_um": spacing,
                    "geometry": name,
                    "width_um": width,
                    "thickness_um": thickness,
                    "delta_beta_per_m": delta_beta,
                })

                print(f"Delta beta: {delta_beta:.6e} 1/m")

    finally:
        WAVEGUIDE.update(original_geometry)

    data = pd.DataFrame(results)
    data.to_csv(OUTPUT_FILE, index=False)

    print("\nMesh sensitivity results:")
    print(data.to_string(index=False))
    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()