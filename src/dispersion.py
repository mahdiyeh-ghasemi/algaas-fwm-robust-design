import numpy as np

# Speed of light in vacuum (m/s)
C = 299792458.0


def calculate_dispersion(wavelength_m, n_eff):
    """
    Calculate angular frequency, propagation constant,
    and group-velocity dispersion from effective-index data.

    Parameters
    ----------
    wavelength_m : array-like
        Wavelength values in meters.
    n_eff : array-like
        Effective refractive index at each wavelength.

    Returns
    -------
    omega : ndarray
        Angular frequency (rad/s).
    beta : ndarray
        Propagation constant (rad/m).
    beta2 : ndarray
        Group-velocity dispersion (s^2/m).
    """

    wavelength_m = np.asarray(wavelength_m, dtype=float)
    n_eff = np.asarray(n_eff, dtype=float)

    if wavelength_m.ndim != 1 or n_eff.ndim != 1:
        raise ValueError("Inputs must be one-dimensional arrays.")

    if len(wavelength_m) != len(n_eff):
        raise ValueError("Wavelength and n_eff arrays must have equal lengths.")

    if len(wavelength_m) < 3:
        raise ValueError("At least three data points are required.")

    if not np.all(np.isfinite(wavelength_m)) or not np.all(np.isfinite(n_eff)):
        raise ValueError("Inputs must contain only finite values.")

    if np.any(wavelength_m <= 0):
        raise ValueError("Wavelength values must be positive.")

    if np.any(n_eff <= 0):
        raise ValueError("Effective-index values must be positive.")

    omega = 2.0 * np.pi * C / wavelength_m
    beta = omega * n_eff / C

    # Sort data by increasing angular frequency
    order = np.argsort(omega)
    omega = omega[order]
    beta = beta[order]

    # Numerical calculation of second-order dispersion
    beta_first_derivative = np.gradient(
        beta, omega, edge_order=2
    )

    beta2 = np.gradient(
        beta_first_derivative, omega, edge_order=2
    )

    return omega, beta, beta2
