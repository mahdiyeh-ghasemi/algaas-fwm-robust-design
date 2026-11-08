from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "fwm_mesh_sensitivity.csv"
OUTPUT_FILE = ROOT_DIR / "figures" / "fwm_mesh_sensitivity.png"


def main():
    data = pd.read_csv(DATA_FILE)

    geometries = [
        "nominal",
        "width_minus",
        "thickness_minus",
    ]

    labels = [
        "Nominal",
        "Width −0.01 µm",
        "Thickness −0.01 µm",
    ]

    grid_spacings = sorted(
        data["grid_spacing_um"].unique(),
        reverse=True,
    )

    x = range(len(geometries))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))

    for i, spacing in enumerate(grid_spacings):
        subset = (
            data[data["grid_spacing_um"] == spacing]
            .set_index("geometry")
            .loc[geometries]
        )

        values = subset["delta_beta_per_m"].abs()

        positions = [
            j + (i - 0.5) * bar_width
            for j in x
        ]

        ax.bar(
            positions,
            values,
            width=bar_width,
            label=f"Grid = {spacing:.5f} µm",
        )

    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel(r"$|\Delta\beta|$ (m$^{-1}$)")
    ax.set_title("Mesh Sensitivity of FWM Phase Mismatch")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=300)
    plt.close(fig)

    print(f"Figure saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()