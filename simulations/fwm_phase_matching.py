from pathlib import Path

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "dispersion_data.csv"
OUTPUT_FILE = ROOT_DIR / "fwm_phase_matching.csv"

C = 299792458.0  # Speed of light (m/s)
PUMP_WAVELENGTH_NM = 1550.0


def main():
    data = pd.read_csv(DATA_FILE)

    wavelength_m = data["wavelength_nm"].to_numpy() * 1e-9
    n_eff = data["n_eff"].to_numpy()

    beta = 2.0 * np.pi * n_eff / wavelength_m

    pump_m = PUMP_WAVELENGTH_NM * 1e-9
    omega_p = 2.0 * np.pi * C / pump_m

    beta_p = np.interp(pump_m, wavelength_m, beta)

    signal_wavelengths = []
    idler_wavelengths = []
    phase_mismatch = []

    for signal_m in wavelength_m:
        omega_s = 2.0 * np.pi * C / signal_m
        omega_i = 2.0 * omega_p - omega_s

        if omega_i <= 0:
            continue

        idler_m = 2.0 * np.pi * C / omega_i

        if idler_m < wavelength_m.min() or idler_m > wavelength_m.max():
            continue

        beta_s = np.interp(signal_m, wavelength_m, beta)
        beta_i = np.interp(idler_m, wavelength_m, beta)

        delta_beta = 2.0 * beta_p - beta_s - beta_i

        signal_wavelengths.append(signal_m * 1e9)
        idler_wavelengths.append(idler_m * 1e9)
        phase_mismatch.append(delta_beta)

    results = pd.DataFrame({
        "signal_wavelength_nm": signal_wavelengths,
        "idler_wavelength_nm": idler_wavelengths,
        "delta_beta_per_m": phase_mismatch,
    })

    results.to_csv(OUTPUT_FILE, index=False)

    print(results.to_string(index=False))
    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()