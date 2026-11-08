from pathlib import Path

import numpy as np
import pandas as pd

from src.mode_solver import solve_waveguide_modes
from src.waveguide_geometry import WAVEGUIDE


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT_DIR / "fwm_geometry_sensitivity.csv"

C = 299792458.0
PUMP_WAVELENGTH_NM = 1550.0
SIGNAL_DETUNING_THZ = 1.0

WAVELENGTHS_UM = np.linspace(1.50, 1.60, 21)

GEOMETRIES = [
    ("nominal", None, None),
    ("width_minus", 0.74, None),
    ("width_plus", 0.76, None),
    ("thickness_minus", None, 0.34),
    ("thickness_plus", None, 0.36),
]


def calculate_dispersion():
    effective_indices = []

    for wavelength_um in WAVELENGTHS_UM:
        result = solve_waveguide_modes(wavelength_um=wavelength_um)
        effective_indices.append(float(result[0][0]))

    wavelength_m = WAVELENGTHS_UM * 1e-6
    beta = (
        2.0 * np.pi * np.array(effective_indices)
        / wavelength_m
    )

    return wavelength_m, beta


def calculate_phase_mismatch(wavelength_m, beta):
    pump_m = PUMP_WAVELENGTH_NM * 1e-9
    omega_p = 2.0 * np.pi * C / pump_m

    omega_s = omega_p + 2.0 * np.pi * SIGNAL_DETUNING_THZ * 1e12
    omega_i = 2.0 * omega_p - omega_s

    signal_m = 2.0 * np.pi * C / omega_s
    idler_m = 2.0 * np.pi * C / omega_i

    if not (
        wavelength_m.min() <= signal_m <= wavelength_m.max()
        and wavelength_m.min() <= idler_m <= wavelength_m.max()
    ):
        raise ValueError("Signal or idler wavelength is outside the dispersion range.")

    beta_p = np.interp(pump_m, wavelength_m, beta)
    beta_s = np.interp(signal_m, wavelength_m, beta)
    beta_i = np.interp(idler_m, wavelength_m, beta)

    return {
        "signal_wavelength_nm": signal_m * 1e9,
        "idler_wavelength_nm": idler_m * 1e9,
        "delta_beta_per_m": 2.0 * beta_p - beta_s - beta_i,
    }


def main():
    original_geometry = WAVEGUIDE.copy()
    results = []

    try:
        for name, width, thickness in GEOMETRIES:
            WAVEGUIDE.update(original_geometry)

            if width is not None:
                WAVEGUIDE["width_um"] = width

            if thickness is not None:
                WAVEGUIDE["core_thickness_um"] = thickness

            print(f"\nCalculating geometry: {name}")
            print(
                f"Width = {WAVEGUIDE['width_um']:.3f} um, "
                f"Thickness = {WAVEGUIDE['core_thickness_um']:.3f} um"
            )

            wavelength_m, beta = calculate_dispersion()
            phase = calculate_phase_mismatch(wavelength_m, beta)

            results.append({
                "geometry": name,
                "width_um": WAVEGUIDE["width_um"],
                "thickness_um": WAVEGUIDE["core_thickness_um"],
                **phase,
            })

            print(
                f"Delta beta = {phase['delta_beta_per_m']:.6e} 1/m"
            )

    finally:
        WAVEGUIDE.update(original_geometry)

    data = pd.DataFrame(results)
    data.to_csv(OUTPUT_FILE, index=False)

    print("\nGeometry sensitivity results:")
    print(data.to_string(index=False))
    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()