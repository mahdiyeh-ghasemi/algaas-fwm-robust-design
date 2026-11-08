
import numpy as np

from src.materials import (
    refractive_index_algaas,
    refractive_index_silica,
)

# Physical constant
C = 299792458.0

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

MATERIALS = {
    "air": 1.0,
}


def create_material_grid(wavelength_um=None):
    wavelength = (
        WAVEGUIDE["wavelength_um"]
        if wavelength_um is None
        else float(wavelength_um)
    )

    width = WAVEGUIDE["width_um"]
    thickness = WAVEGUIDE["core_thickness_um"]
    x_fraction = WAVEGUIDE["aluminium_fraction"]

    spacing = WAVEGUIDE["grid_spacing_um"]
    window_x = WAVEGUIDE["simulation_window_x_um"]
    window_y = WAVEGUIDE["simulation_window_y_um"]

    x = np.arange(-window_x / 2, window_x / 2 + spacing, spacing)
    y = np.arange(-window_y / 2, window_y / 2 + spacing, spacing)

    X, Y = np.meshgrid(x, y)

    core = (
        (np.abs(X) <= width / 2)
        & (np.abs(Y) <= thickness / 2)
    )

    substrate = Y < -thickness / 2
    cladding = (Y >= -thickness / 2) & ~core

    refractive_index = np.full(
        X.shape,
        MATERIALS["air"],
        dtype=float,
    )

    refractive_index[substrate] = refractive_index_silica(wavelength)

    refractive_index[core] = refractive_index_algaas(
        wavelength,
        x_fraction,
    )

    return x, y, refractive_index


def create_permittivity_grid(wavelength_um=None):
    x, y, refractive_index = create_material_grid(wavelength_um)

    relative_permittivity = refractive_index**2

    return x, y, relative_permittivity
