from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "geometrical_tolerance.csv"
OUTPUT_FILE = ROOT_DIR / "figures" / "geometrical_tolerance.png"


def main():
    data = pd.read_csv(DATA_FILE)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for ax, parameter, title, xlabel in [
        (
            axes[0],
            "width",
            "Width Sensitivity",
            "Core width (µm)",
        ),
        (
            axes[1],
            "thickness",
            "Thickness Sensitivity",
            "Core thickness (µm)",
        ),
    ]:
        subset = data[data["parameter"] == parameter]

        for mode in range(1, 5):
            column = f"mode_{mode}_neff"

            ax.plot(
                subset["geometry_um"],
                subset[column],
                marker="o",
                linewidth=2,
                label=f"Mode {mode}",
            )

        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Effective refractive index")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()

    fig.suptitle("Geometrical Tolerance Analysis")
    fig.tight_layout()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=300)
    plt.close(fig)

    print(f"Geometrical tolerance plot saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()