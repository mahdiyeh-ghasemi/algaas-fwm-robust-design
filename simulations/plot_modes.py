import os
import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.mode_solver import solve_waveguide_modes
from src.waveguide_geometry import WAVEGUIDE


def plot_modes():
    neff, Ex, Ey, Ez, Hx, Hy, Hz = solve_waveguide_modes()

    spacing = WAVEGUIDE["grid_spacing_um"]
    window_x = WAVEGUIDE["simulation_window_x_um"]
    window_y = WAVEGUIDE["simulation_window_y_um"]

    x = np.linspace(-window_x / 2, window_x / 2, Ex.shape[1])
    y = np.linspace(-window_y / 2, window_y / 2, Ex.shape[0])

    os.makedirs("figures", exist_ok=True)

    for mode in range(len(neff)):
        field = np.sqrt(
            np.abs(Ex[:, :, mode])**2
            + np.abs(Ey[:, :, mode])**2
            + np.abs(Ez[:, :, mode])**2
        )

        plt.figure(figsize=(7, 5))

        plt.imshow(
            field,
            extent=[x.min(), x.max(), y.min(), y.max()],
            origin="lower",
            aspect="equal",
            cmap="inferno"
        )

        plt.colorbar(label="Electric field magnitude (a.u.)")
        plt.xlabel("x (µm)")
        plt.ylabel("y (µm)")
        plt.title(f"Mode {mode + 1}: neff = {neff[mode]:.4f}")

        plt.tight_layout()

        plt.savefig(
            f"figures/mode_{mode + 1}.png",
            dpi=300
        )

        plt.close()

    print("Mode field plots saved successfully.")


if __name__ == "__main__":
    plot_modes()