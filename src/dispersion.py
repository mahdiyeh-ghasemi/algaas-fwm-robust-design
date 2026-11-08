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
        Angular frequency (rad/s), sorted in ascending order.
    beta : ndarray
        Propagation constant (rad/m), sorted by angular frequency.
    beta2 : ndarray
        Group-velocity dispersion (s^2/m).

    Notes
    -----
    The second derivative is calculated using a fourth-degree
    polynomial fitted to normalized angular-frequency data.
    At least five unique wavelength values are required.
    """

    wavelength_m = np.asarray(wavelength_m, dtype=float)
    n_eff = np.asarray(n_eff, dtype=float)

    if wavelength_m.ndim != 1 or n_eff.ndim != 1:
        raise ValueError("Inputs must be one-dimensional arrays.")

    if len(wavelength_m) != len(n_eff):
        raise ValueError("Input arrays must have equal lengths.")

    if len(wavelength_m) < 5:
        raise ValueError("At least five data points are required.")

    if not np.all(np.isfinite(wavelength_m)):
        raise ValueError("Wavelength values must be finite.")

    if not np.all(np.isfinite(n_eff)):
        raise ValueError("Effective-index values must be finite.")

    if np.any(wavelength_m <= 0) or np.any(n_eff <= 0):
        raise ValueError(
            "Wavelength and effective index must be positive."
        )

    if len(np.unique(wavelength_m)) != len(wavelength_m):
        raise ValueError("Wavelength values must be unique.")

    omega = 2.0 * np.pi * C / wavelength_m
    beta = omega * n_eff / C

    order = np.argsort(omega)
    omega = omega[order]
    beta = beta[order]

    # Normalize angular frequency for numerical stability
    omega_center = np.mean(omega)
    omega_scale = np.ptp(omega) / 2.0
    u = (omega - omega_center) / omega_scale

    # Fourth-degree polynomial fit
    coefficients = np.polynomial.polynomial.polyfit(u, beta, 4)

    # Second derivative with respect to normalized frequency
    second_derivative = np.polynomial.polynomial.polyder(
        coefficients, m=2
    )

    beta2 = np.polynomial.polynomial.polyval(
        u, second_derivative
    ) / omega_scale**2

    return omega, beta, beta2