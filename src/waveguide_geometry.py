import numpy as np

# Physical constant
C = 299792458.0  # Speed of light (m/s)

# Initial waveguide design parameters
WAVEGUIDE = {
    "wavelength_um": 1.55,
    "width_um": 0.75,
    "core_thickness_um": 0.35,
    "aluminium_fraction": 0.21,
    "grid_spacing_um": 0.00625,
    "simulation_window_x_um": 4.0,
    "simulation_window_y_um": 4.0,
    "number_of_modes": 4,
}

from src.materials import (
    refractive_index_algaas,
    refractive_index_silica,
)

MATERIALS = {
    "algaas": refractive_index_algaas,
    "silica": refractive_index_silica,
    "air": 1.0,
}

def create_material_grid():
    wavelength = WAVEGUIDE["wavelength_um"]
    width = WAVEGUIDE["width_um"]
    thickness = WAVEGUIDE["core_thickness_um"]
    x_fraction = WAVEGUIDE["aluminium_fraction"]
    spacing = WAVEGUIDE["grid_spacing_um"]

    window_x = WAVEGUIDE["simulation_window_x_um"]
    window_y = WAVEGUIDE["simulation_window_y_um"]

    x = np.arange(-window_x / 2, window_x / 2 + spacing, spacing)
    y = np.arange(-window_y / 2, window_y / 2 + spacing, spacing)

    X, Y = np.meshgrid(x, y)

    n_algaas = MATERIALS["algaas"](wavelength, x_fraction)
    n_silica = MATERIALS["silica"](wavelength)
    n_air = MATERIALS["air"]

    refractive_index = np.full(X.shape, n_air, dtype=float)

    substrate = Y < -thickness / 2
    core = (np.abs(X) <= width / 2) & (np.abs(Y) <= thickness / 2)
    cladding = (Y >= -thickness / 2) & ~core

    refractive_index[substrate] = n_silica
    refractive_index[cladding] = n_air
    refractive_index[core] = n_algaas

    return x, y, refractive_index
def create_permittivity_grid():
    x, y, refractive_index = create_material_grid()
    relative_permittivity = refractive_index**2
    return x, y, relative_permittivity