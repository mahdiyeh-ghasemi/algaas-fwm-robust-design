from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "fwm_phase_matching.csv"
OUTPUT_FILE = ROOT_DIR / "figures" / "fwm_phase_matching.png"

PUMP_WAVELENGTH_NM = 1550.0


def main():
    data = pd.read_csv(DATA_FILE)

    signal = data["signal_wavelength_nm"].to_numpy()
    delta_beta = data["delta_beta_per_m"].to_numpy()

    frequency_detuning_thz = (
        299792.458 / signal
        - 299792.458 / PUMP_WAVELENGTH_NM
    )

    plt.figure(figsize=(8, 5))

    plt.plot(
        frequency_detuning_thz,
        delta_beta,
        marker="o",
        linewidth=1.8,
    )

    plt.axhline(0, linestyle="--", linewidth=1)
    plt.axvline(0, linestyle=":", linewidth=1)

    plt.xlabel("Signal frequency detuning from pump (THz)")
    plt.ylabel(r"Linear phase mismatch $\Delta\beta$ (m$^{-1}$)")
    plt.title("Degenerate FWM Phase Mismatch")

    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(OUTPUT_FILE, dpi=300)
    plt.close()

    print(f"Figure saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()