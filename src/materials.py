import numpy as np

PLANCK_CONSTANT = 6.62607015e-34
SPEED_OF_LIGHT = 299792458.0
ELEMENTARY_CHARGE = 1.602176634e-19


def refractive_index_algaas(wavelength_um, aluminium_fraction):
    wavelength_um = np.asarray(wavelength_um, dtype=float)
    x = float(aluminium_fraction)

    if not 0 <= x <= 1:
        raise ValueError("Aluminium fraction must be between 0 and 1.")

    if np.any(wavelength_um <= 0):
        raise ValueError("Wavelength must be positive.")

    photon_energy = (
        PLANCK_CONSTANT * SPEED_OF_LIGHT
        / (wavelength_um * 1e-6)
        / ELEMENTARY_CHARGE
    )

    A0 = 6.3 + 19 * x
    B0 = 9.4 - 10.2 * x
    E0 = 1.425 + 1.155 * x + 0.37 * x**2
    E0_plus_delta0 = 1.765 + 1.115 * x + 0.37 * x**2

    if np.any(photon_energy >= E0):
        raise ValueError(
            "Photon energy must be below the direct bandgap "
            "for this model."
        )

    X = photon_energy / E0
    X_so = photon_energy / E0_plus_delta0

    def f(value):
        return (
            2 - np.sqrt(1 + value) - np.sqrt(1 - value)
        ) / value**2

    f_X = f(X)
    f_X_so = f(X_so)

    n_squared = A0 * (
        f_X
        + 0.5 * (E0 / E0_plus_delta0)**1.5 * f_X_so
    ) + B0

    return np.sqrt(n_squared)


def refractive_index_silica(wavelength_um):
    wavelength_um = np.asarray(wavelength_um, dtype=float)

    if np.any(wavelength_um < 0.2139) or np.any(wavelength_um > 3.7067):
        raise ValueError(
            "Wavelength is outside the Sellmeier model range."
        )

    B1, B2, B3 = 0.6961663, 0.4079426, 0.8974794
    L1, L2, L3 = 0.0684043, 0.1162414, 9.896161

    wavelength_squared = wavelength_um**2

    n_squared = (
        1
        + B1 * wavelength_squared / (wavelength_squared - L1**2)
        + B2 * wavelength_squared / (wavelength_squared - L2**2)
        + B3 * wavelength_squared / (wavelength_squared - L3**2)
    )

    return np.sqrt(n_squared)