from pathlib import Path

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT_DIR / "geometrical_tolerance.csv"
OUTPUT_FILE = ROOT_DIR / "sensitivity_coefficients.csv"

NOMINAL_VALUES = {
    "width": 0.75,
    "thickness": 0.35,
}


def main():
    data = pd.read_csv(DATA_FILE)
    results = []

    for parameter, nominal_value in NOMINAL_VALUES.items():
        subset = data[data["parameter"] == parameter]

        nominal = subset[
            subset["geometry_um"] == nominal_value
        ].iloc[0]

        lower = subset[
            subset["geometry_um"] == nominal_value - 0.01
        ].iloc[0]

        upper = subset[
            subset["geometry_um"] == nominal_value + 0.01
        ].iloc[0]

        for mode in range(1, 5):
            column = f"mode_{mode}_neff"

            neff_0 = nominal[column]

            derivative = (
                upper[column] - lower[column]
            ) / 0.02

            sensitivity = (
                nominal_value / neff_0
            ) * derivative

            results.append({
                "parameter": parameter,
                "mode": mode,
                "nominal_neff": neff_0,
                "sensitivity_coefficient": sensitivity,
            })

    output = pd.DataFrame(results)
    output.to_csv(OUTPUT_FILE, index=False)

    print(output.to_string(index=False))
    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()