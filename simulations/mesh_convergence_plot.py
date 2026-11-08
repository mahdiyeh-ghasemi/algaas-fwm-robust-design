from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "mesh_convergence.csv"
OUTPUT_FILE = ROOT_DIR / "figures" / "mesh_convergence.png"


def main():
    data = pd.read_csv(DATA_FILE)

    plt.figure(figsize=(8, 5))

    for mode in range(1, 5):
        column = f"mode_{mode}_neff"

        plt.plot(
            data["grid_spacing_um"],
            data[column],
            marker="o",
            linewidth=2,
            label=f"Mode {mode}",
        )

    plt.xscale("log")
    plt.gca().invert_xaxis()

    plt.xlabel("Grid spacing (µm)")
    plt.ylabel("Effective refractive index")
    plt.title("Mesh Convergence Analysis")

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_FILE, dpi=300)
    plt.close()

    print(f"Mesh convergence plot saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()