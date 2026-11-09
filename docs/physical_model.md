# Physical Model: Four-Wave Mixing in AlGaAs-on-Insulator Waveguides

## 1. Introduction

This project presents a preliminary numerical investigation of waveguide modes, dispersion, and degenerate four-wave mixing (FWM) in an AlGaAs-on-insulator waveguide.

The main objective is to examine the linear phase mismatch of FWM and investigate how spatial discretization and geometrical variations influence the calculated results.

The current implementation combines a finite-difference eigenmode calculation with wavelength-dependent material models and numerical post-processing.

## 2. Waveguide Structure and Material Model

The computational structure consists of:

- An aluminium gallium arsenide (AlGaAs) rectangular waveguide core.
- A silica substrate.
- Air in the upper and lateral cladding regions.

The nominal waveguide parameters are:

| Parameter | Value |
|---|---:|
| Operating wavelength | 1.55 µm |
| Core width | 0.75 µm |
| Core thickness | 0.35 µm |
| Aluminium fraction | 0.21 |
| Nominal grid spacing | 0.00625 µm |
| Computational window | 4 × 4 µm |
| Number of calculated modes | 4 |

The AlGaAs refractive index is calculated using an Adachi-type wavelength-dependent dispersion expression implemented in `src/materials.py`.

The silica refractive index is calculated using a Sellmeier model. Air is represented by a refractive index of 1.

The present structure is a simplified numerical representation. It does not include a complete fabrication stack, measured material dispersion, or experimentally determined waveguide parameters.

## 3. Eigenmode Analysis

The transverse electromagnetic eigenmodes are calculated using a finite-difference eigenmode solver.

The computational domain is discretized on a uniform spatial grid. The relative permittivity distribution is constructed from the refractive-index profiles of the AlGaAs core, silica substrate, and air cladding.

The propagation constant is obtained from:

\[
\beta(\omega)=\frac{\omega}{c}n_{\mathrm{eff}}(\omega)
\]

where \(n_{\mathrm{eff}}\) is the effective refractive index and \(c\) is the speed of light in vacuum.

The solver calculates the effective indices and electric-field distributions of the requested modes.

The current implementation evaluates four modes at the nominal geometry. Subsequent wavelength-dependent calculations use the fundamental mode.

## 4. Waveguide Dispersion

The wavelength dependence of the propagation constant is used to estimate the group-velocity dispersion parameter:

\[
\beta_2=\frac{\partial^2\beta}{\partial\omega^2}
\]

The propagation constant is calculated from the wavelength-dependent effective index.

The angular-frequency data are normalized by subtracting their mean and dividing by half of their range. A fourth-degree polynomial is fitted to the propagation constant as a function of the normalized angular frequency. The second derivative is then evaluated analytically from the fitted polynomial and converted to the derivative with respect to angular frequency using the corresponding frequency-scale factor.

Polynomial degrees and endpoint sensitivity are compared to assess numerical fitting stability.

These checks evaluate the consistency of the numerical fitting procedure; they do not independently validate the physical accuracy of the material model or waveguide structure.

## 5. Degenerate Four-Wave Mixing

Degenerate four-wave mixing is a third-order nonlinear optical process in which two pump photons interact to generate signal and idler frequency components.

The energy conservation condition is:

\[
2\omega_p=\omega_s+\omega_i
\]

where:

- \(\omega_p\) is the pump angular frequency.
- \(\omega_s\) is the signal angular frequency.
- \(\omega_i\) is the idler angular frequency.

The corresponding linear phase mismatch is defined as:

\[
\Delta\beta_{\mathrm{lin}}
=2\beta_p-\beta_s-\beta_i
\]

where the propagation constants are evaluated at the pump, signal, and idler frequencies using the calculated fundamental-mode dispersion.

The current FWM analysis uses:

- Pump wavelength: 1550 nm.
- Signal wavelengths: sampled from the available dispersion data.
- Idler frequency: determined from energy conservation.
- Fundamental guided mode for all three frequency components.
- Only signal–idler pairs within the sampled wavelength range are considered.

For the geometrical and mesh sensitivity analyses, the signal frequency is fixed at +1 THz relative to the pump frequency, and the idler frequency is determined through energy conservation. At a pump wavelength of 1550 nm, this corresponds to signal and idler wavelengths of approximately 1542.027 nm and 1558.056 nm, respectively. The same frequency configuration is used across the geometrical and mesh sensitivity calculations to ensure consistent comparisons.

The current implementation evaluates the linear phase mismatch. It does not calculate nonlinear phase shifts, nonlinear conversion efficiency, or output power.

## 6. Geometrical Sensitivity

The influence of geometrical variations is investigated by changing the waveguide core width and thickness around their nominal values.

Two types of sensitivity analysis are implemented:

1. Effective-index sensitivity for the calculated guided modes.
2. Linear FWM phase-mismatch sensitivity for the fundamental mode.

The FWM geometrical analysis considers independent changes in width and thickness around the nominal geometry.

These calculations provide a preliminary numerical comparison of the response to the tested geometrical variations. They do not establish fabrication tolerances or identify a globally optimized geometry.

## 7. Numerical Discretization and Mesh Sensitivity

The waveguide cross-section is represented on a uniform spatial grid.

The nominal grid spacing is 0.00625 µm. Additional grid resolutions are used in the effective-index convergence and FWM mesh-sensitivity analyses.

The FWM mesh-sensitivity analysis compares grid spacings of 0.0125 µm and 0.00625 µm for three geometrical configurations.

Since the core boundary is represented on a discrete grid, changes in nominal geometry may also change its rasterized representation.

Consequently, the calculated geometrical sensitivity may include discretization effects. More extensive mesh refinement and boundary-treatment studies are required for stronger quantitative conclusions.

## 8. Scope of the Current Nonlinear Model

Although the project investigates FWM, the implemented calculations currently focus on the linear phase mismatch.

The following effects are not yet included in the numerical FWM calculation:

- Nonlinear phase shifts.
- Nonlinear coefficient and effective nonlinear mode area.
- Pump-power-dependent phase matching.
- Two-photon absorption.
- Free-carrier absorption and carrier dynamics.
- Nonlinear propagation and conversion efficiency.

A complete nonlinear FWM model would require additional material parameters, nonlinear mode calculations, and propagation equations.

These effects are therefore treated as future extensions rather than completed results.

## 9. Scientific Limitations

The current study has several limitations:

1. The waveguide geometry and material stack are simplified.
2. The material models have not been independently validated against measurements for the specific structure.
3. The numerical mesh studies do not establish complete convergence for every calculated mode or FWM quantity.
4. The geometrical sensitivity study covers a limited range of parameter variations.
5. The FWM analysis evaluates linear phase mismatch rather than nonlinear conversion efficiency.
6. No experimental measurements or independent reference-device results are used for validation.

The reported results should therefore be interpreted as preliminary numerical findings within the assumptions and parameter ranges of the implemented model.

## 10. Future Development

Further work may include:

- More extensive mesh-refinement and boundary-discretization studies.
- Validation of material dispersion against reliable experimental or published data.
- Broader geometrical parameter sweeps.
- Evaluation of nonlinear mode properties and effective nonlinear coefficients.
- Inclusion of nonlinear phase mismatch and pump-power dependence.
- Modeling of nonlinear propagation and absorption.
- Comparison with published or experimentally measured AlGaAs waveguide results.

These extensions would provide a stronger basis for evaluating phase matching and fabrication-tolerant FWM performance.
