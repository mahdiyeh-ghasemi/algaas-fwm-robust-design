import numpy as np

C = 299792458.0


def calculate_fwm_phase_mismatch(
    omega,
    beta,
    pump_wavelength_m,
    signal_wavelength_m
):
    """
    Calculate the linear phase mismatch for degenerate FWM.

    Energy conservation:
        2 * omega_p = omega_s + omega_i

    Linear phase mismatch:
        delta_beta = 2 * beta_p - beta_s - beta_i

    Parameters
    ----------
    omega : array-like
        Angular-frequency grid (rad/s).
    beta : array-like
        Propagation constant corresponding to omega (rad/m).
    pump_wavelength_m : float
        Pump wavelength in meters.
    signal_wavelength_m : array-like
        Signal wavelength values in meters.

    Returns
    -------
    omega_idler : ndarray
        Idler angular frequencies (rad/s).
    delta_beta : ndarray
        Linear phase mismatch (rad/m).
    """

    omega = np.asarray(omega, dtype=float)
    beta = np.asarray(beta, dtype=float)
    signal_wavelength_m = np.atleast_1d(
        np.asarray(signal_wavelength_m, dtype=float)
    )

    if omega.ndim != 1 or beta.ndim != 1:
        raise ValueError("omega and beta must be one-dimensional.")

    if len(omega) != len(beta) or len(omega) < 2:
        raise ValueError("omega and beta must have equal lengths.")

    if not np.all(np.isfinite(omega)) or not np.all(np.isfinite(beta)):
        raise ValueError("omega and beta must contain finite values.")

    if np.any(np.diff(omega) <= 0):
        raise ValueError("omega must be strictly increasing.")

    if pump_wavelength_m <= 0 or np.any(signal_wavelength_m <= 0):
        raise ValueError("Wavelengths must be positive.")

    omega_p = 2.0 * np.pi * C / pump_wavelength_m
    omega_s = 2.0 * np.pi * C / signal_wavelength_m

    # Energy conservation for degenerate FWM
    omega_i = 2.0 * omega_p - omega_s

    if np.any(omega_i <= 0):
        raise ValueError("Calculated idler frequencies must be positive.")

    # Check interpolation range
    if (
        omega_p < omega[0] or omega_p > omega[-1]
        or np.any(omega_s < omega[0])
        or np.any(omega_s > omega[-1])
        or np.any(omega_i < omega[0])
        or np.any(omega_i > omega[-1])
    ):
        raise ValueError(
            "Pump, signal, and idler frequencies must lie "
            "within the supplied dispersion data range."
        )

    beta_p = np.interp(omega_p, omega, beta)
    beta_s = np.interp(omega_s, omega, beta)
    beta_i = np.interp(omega_i, omega, beta)

    delta_beta = 2.0 * beta_p - beta_s - beta_i

    return omega_i, delta_beta
