from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.dispersion import calculate_dispersion


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "dispersion_data.csv"
FIGURE_DIR = ROOT_DIR / "figures"


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dispersion data file not found: {DATA_FILE}"
        )

    data = pd.read_csv(DATA_FILE)

    required_columns = {"wavelength_nm", "n_eff"}

    if not required_columns.issubset(data.columns):
        raise ValueError(
            "CSV file must contain wavelength_nm and n_eff columns."
        )

    if data[list(required_columns)].isnull().any().any():
        raise ValueError("Input data must not contain missing values.")

    wavelength_nm = data["wavelength_nm"].to_numpy(dtype=float)
    n_eff = data["n_eff"].to_numpy(dtype=float)

    if len(wavelength_nm) < 5:
        raise ValueError("At least five data points are recommended.")

    if len(np.unique(wavelength_nm)) != len(wavelength_nm):
        raise ValueError("Wavelength values must be unique.")

    wavelength_m = wavelength_nm * 1e-9

    omega, beta, beta2 = calculate_dispersion(
        wavelength_m,
        n_eff
    )

    # Sort by increasing wavelength
    order = np.argsort(wavelength_m)

    wavelength_plot_nm = wavelength_m[order] * 1e9
    n_eff_plot = n_eff[order]

    # Match beta2 values to increasing wavelength
    wavelength_from_omega_nm = (
        2.0 * np.pi * 299792458.0 / omega * 1e9
    )

    beta2_order = np.argsort(wavelength_from_omega_nm)
    beta2_plot = beta2[beta2_order]

    # Convert from s^2/m to ps^2/km
    beta2_ps2_km = beta2_plot * 1e27

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(8, 8))

    axes[0].plot(wavelength_plot_nm, n_eff_plot)
    axes[0].set_ylabel("Effective refractive index")
    axes[0].set_title("Waveguide Effective Index")
    axes[0].grid(True)

    axes[1].plot(wavelength_plot_nm, beta2_ps2_km)
    axes[1].set_xlabel("Wavelength (nm)")
    axes[1].set_ylabel(r"$\beta_2$ (ps$^2$/km)")
    axes[1].set_title("Group-Velocity Dispersion")
    axes[1].grid(True)

    fig.tight_layout()

    output_file = FIGURE_DIR / "dispersion_analysis.png"
    fig.savefig(output_file, dpi=300, bbox_inches="tight")

    print(f"Dispersion analysis saved to: {output_file}")

    plt.close(fig)


if __name__ == "__main__":
    main()