# Methodology: Numerical Modeling and Fabrication-Tolerant Design

## 1. Overview

This project uses a numerical approach to investigate degenerate four-wave mixing (FWM) in AlGaAs-on-insulator (AlGaAsOI) waveguides.

The methodology is organized into five stages:

1. Definition of the waveguide geometry and material parameters.
2. Calculation of modal properties and waveguide dispersion.
3. Evaluation of phase-matching conditions.
4. Analysis of sensitivity to geometrical variations.
5. Numerical optimization of fabrication-tolerant geometries.

The model will be developed progressively, with assumptions and parameter sources documented at each stage.

## 2. Material and Geometrical Parameters

The initial model will consider an AlGaAs core surrounded by an insulating lower-cladding layer and an upper-cladding environment.

The main geometrical parameters are:

- Waveguide width: \(W\)
- Core thickness: \(H\)
- Aluminium composition: \(x\)

The refractive indices of the constituent materials will be specified as functions of wavelength and, where necessary, composition.

The initial geometry and material parameters will be selected from published experimental studies. No parameter will be treated as an experimentally validated value unless supported by a suitable reference.

## 3. Modal Analysis and Dispersion Calculation

The fundamental transverse-electric (TE) mode will be investigated first.

For each waveguide geometry, the effective refractive index will be calculated as a function of wavelength:

$$
n_{\mathrm{eff}} = n_{\mathrm{eff}}(\lambda,W,H)
$$

The propagation constant is then obtained from:

$$
\beta(\omega,W,H) = \frac{\omega}{c} n_{\mathrm{eff}}(\omega,W,H)
$$

where \(c\) is the speed of light in vacuum.

The propagation constant will be evaluated over a wavelength range covering the pump, signal, and idler frequencies.

Waveguide dispersion will be characterized using derivatives of the propagation constant with respect to angular frequency.

The group-velocity dispersion parameter is:

$$
\beta_2 = \frac{\partial^2 \beta}{\partial \omega^2}
$$

Numerical differentiation will be used where analytical derivatives are unavailable.

## 4. Four-Wave Mixing Phase Matching

For degenerate four-wave mixing, energy conservation requires:

$$
2\omega_p = \omega_s + \omega_i
$$

where:

- \(\omega_p\) is the pump angular frequency.
- \(\omega_s\) is the signal angular frequency.
- \(\omega_i\) is the idler angular frequency.

The linear phase mismatch is defined as:

$$
\Delta\beta_{\mathrm{lin}} = 2\beta_p - \beta_s - \beta_i
$$

where \(\beta_p\), \(\beta_s\), and \(\beta_i\) represent the propagation constants of the pump, signal, and idler waves, respectively.

Efficient four-wave mixing requires the total phase mismatch to be sufficiently close to zero. In addition to the linear contribution, the total phase mismatch may include nonlinear contributions arising from the Kerr effect and optical intensities.

The total phase mismatch can therefore be expressed generally as:

$$
\Delta\beta_{\mathrm{total}}
=
\Delta\beta_{\mathrm{lin}}
+
\Delta\beta_{\mathrm{NL}}
$$

where \(\Delta\beta_{\mathrm{NL}}\) represents the nonlinear phase-mismatch contribution.

Phase matching will initially be investigated by evaluating the linear mismatch over the relevant signal and idler frequency range. Nonlinear contributions will be incorporated in a subsequent modeling stage.

The effects of pump wavelength and waveguide geometry on phase matching will then be compared.
