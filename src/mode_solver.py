
import numpy as np
from modesolver.wgmodes import wgmodes

from src.waveguide_geometry import (
    WAVEGUIDE,
    create_permittivity_grid,
)


def solve_waveguide_modes(guess=2.5, wavelength_um=None):
    wavelength = (
        WAVEGUIDE["wavelength_um"]
        if wavelength_um is None
        else float(wavelength_um)
    )

    spacing = WAVEGUIDE["grid_spacing_um"]
    number_of_modes = WAVEGUIDE["number_of_modes"]

    x, y, eps = create_permittivity_grid(wavelength)

    neff, Ex, Ey, Ezj, Hx, Hy, Hzj = wgmodes(
        wavelength=wavelength,
        guess=guess,
        nmodes=number_of_modes,
        dx=spacing,
        dy=spacing,
        boundary="0000",
        eps=eps,
    )

    return neff, Ex, Ey, Ezj, Hx, Hy, Hzj
