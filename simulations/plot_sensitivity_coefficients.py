from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "sensitivity_coefficients.csv"
OUTPUT_FILE = ROOT_DIR / "figures" / "sensitivity_coefficients.png"


def main():
    data = pd.read_csv(DATA_FILE)

    modes = np.arange(1, 5)
    width = 0.35

    width_sensitivity = (
        data[data["parameter"] == "width"]
        .sort_values("mode")["sensitivity_coefficient"]
        .to_numpy()
    )

    thickness_sensitivity = (
        data[data["parameter"] == "thickness"]
        .sort_values("mode")["sensitivity_coefficient"]
        .to_numpy()
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.bar(
        modes - width / 2,
        width_sensitivity,
        width,
        label="Width",
    )

    ax.bar(
        modes + width / 2,
        thickness_sensitivity,
        width,
        label="Thickness",
    )

    ax.set_xlabel("Mode")
    ax.set_ylabel("Dimensionless sensitivity coefficient")
    ax.set_title("Geometrical Sensitivity of Effective Refractive Index")
    ax.set_xticks(modes)
    ax.set_xticklabels([f"Mode {mode}" for mode in modes])
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=300)
    plt.show()

    print(f"Figure saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()