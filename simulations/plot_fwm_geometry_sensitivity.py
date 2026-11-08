from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "fwm_geometry_sensitivity.csv"
OUTPUT_FILE = ROOT_DIR / "figures" / "fwm_geometry_sensitivity.png"


def main():
    data = pd.read_csv(DATA_FILE)

    nominal = abs(
        data.loc[data["geometry"] == "nominal", "delta_beta_per_m"].iloc[0]
    )

    data["mismatch_magnitude"] = data["delta_beta_per_m"].abs()
    data["relative_change_percent"] = (
        (data["mismatch_magnitude"] - nominal) / nominal * 100
    )

    labels = {
        "width_minus": "Width −0.01 µm",
        "nominal": "Nominal",
        "width_plus": "Width +0.01 µm",
        "thickness_minus": "Thickness −0.01 µm",
        "thickness_plus": "Thickness +0.01 µm",
    }

    order = list(labels.keys())
    data = data.set_index("geometry").loc[order].reset_index()

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.bar(
        [labels[name] for name in data["geometry"]],
        data["mismatch_magnitude"],
    )

    ax.axhline(
        nominal,
        linestyle="--",
        linewidth=1,
        label="Nominal mismatch",
    )

    for bar, value in zip(bars, data["relative_change_percent"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.08,
            f"{value:+.2f}%",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.set_ylabel(r"$|\Delta\beta|$ (m$^{-1}$)")
    ax.set_title("Geometrical Sensitivity of FWM Phase Mismatch")
    ax.tick_params(axis="x", rotation=15)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=300)
    plt.close(fig)

    print(f"Figure saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()