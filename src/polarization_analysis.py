import numpy as np


def analyze_polarization(Ex, Ey, Ezj):

    results = []

    for mode in range(Ex.shape[2]):

        x = np.sum(np.abs(Ex[:, :, mode])**2)
        y = np.sum(np.abs(Ey[:, :, mode])**2)
        z = np.sum(np.abs(Ezj[:, :, mode])**2)

        transverse_total = x + y
        total = transverse_total + z

        if total == 0 or transverse_total == 0:
            raise ValueError(f"Mode {mode + 1} has zero field magnitude.")

        results.append({
            "mode": mode + 1,
            "Ex_transverse": x / transverse_total,
            "Ey_transverse": y / transverse_total,
            "Ez_total": z / total,
        })

    return results