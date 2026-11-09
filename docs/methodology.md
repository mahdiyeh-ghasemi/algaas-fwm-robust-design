# Methodology: Numerical Modeling and Fabrication-Tolerant Design

## 1. Research Workflow

The project investigates the numerical design of AlGaAs-on-insulator waveguides for four-wave mixing (FWM), with an emphasis on phase matching and fabrication tolerance.

The methodology is organized into five stages:

1. Definition of the waveguide geometry and material parameters.
2. Calculation of modal properties and waveguide dispersion.
3. Evaluation of phase-matching conditions.
4. Analysis of sensitivity to geometrical variations.
5. Investigation of fabrication-tolerant geometries.

The model is developed progressively, with assumptions and parameter sources documented at each stage. The current work focuses on numerical modeling and preliminary sensitivity analysis.

## 2. Material and Geometrical Parameters

The initial model considers an AlGaAs core on a silica substrate, with air as the upper and lateral cladding.

The main geometrical parameters are:

- Waveguide width: \(W\)
- Core thickness: \(H\)
- Aluminium composition: \(x\)
- Operating wavelength: \(\lambda\)

The initial numerical model uses the following parameters:

| Parameter | Value |
|---|---:|
| Operating wavelength | 1.55 µm |
| Core width | 0.75 µm |
| Core thickness | 0.35 µm |
| Aluminium fraction | 0.21 |
| Grid spacing | 0.00625 µm |
| Simulation window | 4 × 4 µm |
| Number of calculated modes | 4 |

The AlGaAs refractive index is calculated using a wavelength-dependent dispersion model based on Adachi-type expressions. The silica refractive index is calculated using the Sellmeier equation.

The substrate is represented numerically as a silica region extending to the lower boundary of the computational window. Air is used in the upper and lateral cladding regions.

These parameters define an initial computational model and are not intended to represent a fully validated fabrication stack.

## 3. Waveguide Eigenmode Analysis

The guided modes are calculated using a finite-difference eigenmode solver.

The transverse computational domain is discretized using a uniform spatial grid. The relative-permittivity distribution is constructed from the refractive indices of the AlGaAs core, silica substrate, and air cladding.

The eigenmode solver calculates the effective indices and electromagnetic field components of the supported modes.

The propagation constant is obtained from:

\[
\beta = \frac{2\pi}{\lambda}n_{\mathrm{eff}}
\]

The calculations are repeated over the wavelength range of interest to characterize the wavelength dependence of the modal properties.

### 3.1 Modal Field Profiles

The transverse and longitudinal electric-field components are combined to visualize the spatial field distribution of each calculated mode.

For each mode, the total electric-field magnitude is evaluated as:

\[
|E| = \sqrt{|E_x|^2+|E_y|^2+|E_z|^2}
\]

The resulting field profiles are presented in Figure 1. Four guided modes are obtained using the numerical eigenmode solver.

![Comparison of the four calculated modal field profiles](../figures/all_modes_comparison.png)

**Figure 1.** Spatial electric-field magnitude distributions of the four calculated waveguide modes. Each panel shows one mode.

## 4. Mesh Convergence Analysis

A mesh convergence analysis is performed to evaluate the sensitivity of the calculated effective indices to the spatial discretization of the computational domain.

Three grid spacings are considered:

- 0.025 µm
- 0.0125 µm
- 0.00625 µm

For each grid resolution, the eigenmode solver is used to calculate the effective indices of the four guided modes at the reference wavelength of 1.55 µm. All other waveguide parameters and material properties are kept unchanged.

The calculated effective indices are summarized below.

| Grid spacing (µm) | Mode 1 | Mode 2 | Mode 3 | Mode 4 |
|---:|---:|---:|---:|---:|
| 0.02500 | 2.789443 | 2.484256 | 2.184165 | 2.042173 |
| 0.01250 | 2.790239 | 2.482065 | 2.179440 | 2.037194 |
| 0.00625 | 2.790250 | 2.481024 | 2.176761 | 2.034373 |

The relative changes in effective index between the two finest grid resolutions are approximately 0.0004%, 0.0420%, 0.1231%, and 0.1387% for modes 1–4, respectively.

The results indicate that the fundamental-mode effective index is highly stable under the tested mesh refinement. The higher-order modes exhibit larger changes, suggesting that their numerical convergence is less complete and requires further investigation.

The finest grid spacing of 0.00625 µm is therefore adopted for the subsequent simulations. This choice provides a stable fundamental-mode result while retaining the higher-order modes for further analysis.

The numerical results are stored in `mesh_convergence.csv` and can be reproduced using `simulations/mesh_convergence.py`.

The corresponding mesh convergence plot is shown below.

![Mesh convergence analysis](../figures/mesh_convergence.png)

## 5. Computational Domain Size Convergence

The influence of the computational window size is evaluated by comparing the calculated effective indices for different domain dimensions.

The 4 × 4 µm computational window is compared with a 3 × 3 µm window while maintaining the same spatial grid spacing.

The calculated effective indices show negligible differences between the two domain sizes for the four modes considered.

The field magnitude near the computational boundaries is also examined to assess possible boundary effects.

## 6. Modal Polarization Analysis

The relative contributions of the electric-field components are evaluated for each calculated mode.

The transverse component indicators are defined as:

\[
R_x = \frac{\sum |E_x|^2}
{\sum |E_x|^2+\sum |E_y|^2}
\]

\[
R_y = \frac{\sum |E_y|^2}
{\sum |E_x|^2+\sum |E_y|^2}
\]

The longitudinal-field indicator is defined as:

\[
R_z = \frac{\sum |E_z|^2}
{\sum |E_x|^2+\sum |E_y|^2+\sum |E_z|^2}
\]

These quantities are normalized squared-field component indicators. They are not physical modal power fractions, which would require evaluation of the Poynting flux.

The calculated results indicate that modes 1 and 3 are predominantly x-oriented in their transverse electric-field components, whereas modes 2 and 4 are predominantly y-oriented.

![Modal polarization analysis](../figures/polarization_analysis.png)

**Figure 2.** Normalized squared-field component indicators for the four calculated modes.

## 7. Waveguide Dispersion Analysis

Waveguide dispersion is characterized using derivatives of the propagation constant with respect to angular frequency.

The group-velocity dispersion parameter is:

\[
\beta_2 = \frac{\partial^2 \beta}{\partial \omega^2}
\]

The propagation constant is calculated from the wavelength-dependent effective index obtained from the eigenmode solver.

To evaluate the second-order derivative, the angular-frequency data are normalized and fitted using a fourth-degree polynomial. The analytical second derivative of the fitted polynomial is then evaluated over the wavelength range.

The polynomial degree is assessed by comparing degrees two through five. At 1550 nm, the fourth- and fifth-degree fits produce nearly identical values of \(\beta_2\).

The fourth-degree fit is also tested for sensitivity to endpoint removal. Removing up to three data points from each end of the wavelength interval results in negligible changes in the calculated value at 1550 nm.

These tests assess numerical fitting stability but do not independently validate the physical accuracy of the material or waveguide model.

The calculated effective-index and group-velocity-dispersion curves are presented in Figure 3.

![Waveguide dispersion analysis](../figures/dispersion_analysis.png)

**Figure 3.** Effective refractive index and calculated group-velocity dispersion as functions of wavelength.

### 7.1 Fundamental-Mode Continuity Analysis

To assess the continuity of the fundamental-mode electric-field distribution across the wavelength range, a normalized squared-overlap analysis is performed between consecutive wavelength points.

For two electric-field distributions, the normalized squared overlap is defined as:

\[
O =
\frac{
\left|\langle E_a,E_b\rangle\right|^2
}{
\langle E_a,E_a\rangle
\langle E_b,E_b\rangle
}
\]

The overlap calculation combines the three electric-field components \(E_x\), \(E_y\), and \(E_z\). The discrete inner product is evaluated as a sum over the transverse grid points and all three field components. Complex conjugation is applied to the first field in the inner product.

The calculations use the same spatial grid at all sampled wavelengths. The overlap is evaluated between the first mode returned by the eigenmode solver at each pair of consecutive wavelength points.

For the wavelength sweep from 1500 nm to 1600 nm, with a 5 nm increment, 20 consecutive-wavelength comparisons are performed.

The normalized squared-overlap values range from approximately 0.99999285 to 0.99999335. These results indicate strong continuity of the calculated fundamental-mode electric-field distribution over the sampled wavelength range.

The effective-index data used in the dispersion analysis are therefore supported by this fundamental-mode continuity check.

The results are stored in `modal_continuity.csv` and can be reproduced using `simulations/generate_dispersion_data.py`.

This analysis checks the continuity of the solver's first returned mode. It does not implement automatic mode matching across all calculated modes or a linear-assignment tracking algorithm. It also does not independently establish the physical accuracy of the waveguide model.

## 8. Geometrical Sensitivity Analysis

The sensitivity of the calculated effective indices to variations in the waveguide core width and thickness is investigated using independent parameter sweeps.

The nominal geometry is defined by:

- Core width: 0.75 µm
- Core thickness: 0.35 µm

Each geometrical parameter is varied independently while the other geometrical parameter, material properties, wavelength, and numerical settings are kept unchanged.

For the width sweep, the core width ranges from 0.73 µm to 0.77 µm. For the thickness sweep, the core thickness ranges from 0.33 µm to 0.37 µm. Five values are evaluated for each parameter.

The calculated effective indices of the four modes are stored in `geometrical_tolerance.csv`. The analysis can be reproduced using `simulations/geometrical_tolerance.py`.

The resulting sensitivity curves are shown below.

![Geometrical tolerance analysis](../figures/geometrical_tolerance.png)

The results show that the effective indices increase with both core width and core thickness over the investigated ranges. The magnitude of the response differs between modes and geometrical parameters.

For the fundamental mode, the effective index changes from approximately 2.7807 to 2.7991 over the investigated width range, and from 2.7602 to 2.8171 over the investigated thickness range.

These results represent numerical geometrical sensitivity under the current simplified waveguide model. Since the spatial grid is fixed, changes in the discretized core boundaries may also influence the calculated effective indices. Further mesh-refinement and mode-continuity checks are therefore required before interpreting these results as realistic fabrication tolerances.

## 9. Dimensionless Geometrical Sensitivity Coefficients

To quantify the relative response of the effective refractive index to geometrical variations, dimensionless sensitivity coefficients are calculated for the core width and thickness.

The sensitivity coefficient for a geometrical parameter \(p\) is defined as:

\[
S_p = \frac{p}{n_{\mathrm{eff}}}
\frac{\partial n_{\mathrm{eff}}}{\partial p}
\]

The derivative is approximated numerically using a central finite difference around the nominal geometry:

\[
\frac{\partial n_{\mathrm{eff}}}{\partial p}
\approx
\frac{n_{\mathrm{eff}}(p+0.01)-n_{\mathrm{eff}}(p-0.01)}
{0.02}
\]

The nominal core width and thickness are 0.75 µm and 0.35 µm, respectively. Each parameter is varied independently while the other geometrical parameter is held fixed.

The calculated dimensionless sensitivity coefficients are summarized below.

| Parameter | Mode 1 | Mode 2 | Mode 3 | Mode 4 |
|---|---:|---:|---:|---:|
| Width | 0.0821 | 0.0637 | 0.5060 | 0.2881 |
| Thickness | 0.1187 | 0.3677 | 0.1915 | 0.5120 |

The results indicate that the relative sensitivity depends on both the geometrical parameter and the mode. Mode 3 exhibits the highest sensitivity to core width, whereas Mode 4 exhibits the highest sensitivity to core thickness among the calculated modes.

A dimensionless coefficient of 0.506 indicates that, locally around the nominal geometry, a 1% increase in core width produces approximately a 0.506% increase in the effective refractive index of Mode 3.

The calculated coefficients are local numerical sensitivity indicators. They do not directly represent fabrication tolerances or phase-matching sensitivity. Their accuracy is also subject to the discretization and convergence limitations discussed in Section 8.

The numerical results are stored in `sensitivity_coefficients.csv` and can be reproduced using `simulations/sensitivity_coefficients.py`. The corresponding comparison plot is shown below.

![Dimensionless geometrical sensitivity coefficients](../figures/sensitivity_coefficients.png)

**Figure 4.** Dimensionless sensitivity coefficients of the effective refractive index with respect to core width and thickness for the four calculated modes.

## 10. Phase Matching and Fabrication-Tolerant Design

Four-wave-mixing phase matching is investigated using the calculated modal propagation constants. The analysis evaluates the linear phase mismatch for interacting pump, signal, and idler waves.

The subsequent sensitivity analysis examines how changes in waveguide geometry influence the calculated phase mismatch. In particular, core width and thickness variations are considered around the nominal waveguide geometry.

The present analysis provides a preliminary numerical assessment of phase mismatch and its dependence on spatial discretization and geometrical variations. It does not yet establish an optimized phase-matched design or demonstrate fabrication tolerance under experimental conditions.

The main FWM phase-matching analysis samples signal wavelengths from the available dispersion data and determines the corresponding idler frequencies through energy conservation. In contrast, the geometrical and mesh sensitivity analyses use a fixed signal-frequency detuning of +1 THz relative to the pump frequency. This distinction allows the main analysis to examine multiple signal–idler pairs, while the sensitivity analyses compare different geometries and grid resolutions under a consistent frequency configuration.

## 11. Mesh Sensitivity of FWM Phase Mismatch

The influence of spatial discretization on the calculated four-wave mixing (FWM) phase mismatch was examined using two grid spacings: 0.0125 µm and 0.00625 µm.

Three waveguide configurations were evaluated:

- Nominal geometry: width = 0.75 µm, thickness = 0.35 µm.
- Reduced width: width = 0.74 µm, thickness = 0.35 µm.
- Reduced thickness: width = 0.75 µm, thickness = 0.34 µm.

For each configuration, the fundamental-mode effective index was recalculated over 21 wavelengths between 1.50 and 1.60 µm. The linear phase mismatch was then evaluated for a pump wavelength of 1550 nm and a signal frequency detuned by 1 THz.

The calculated phase mismatch magnitudes were:

| Geometry | Grid = 0.0125 µm (m⁻¹) | Grid = 0.00625 µm (m⁻¹) |
|---|---:|---:|
| Nominal | 45.9051 | 45.1689 |
| Reduced width | 43.6062 | 44.0130 |
| Reduced thickness | 46.5919 | 45.4615 |

The relative differences between the two grid resolutions were approximately 1.6%, 0.9%, and 2.4% for the nominal, reduced-width, and reduced-thickness configurations, respectively.

These results indicate a moderate dependence of the calculated phase mismatch on spatial discretization. The comparison provides a preliminary numerical sensitivity check rather than a complete mesh-convergence demonstration, since only two grid resolutions were considered. Further refinement and geometry-boundary accuracy checks are required before drawing quantitative conclusions about fabrication tolerances.

![Mesh sensitivity of FWM phase mismatch](../figures/fwm_mesh_sensitivity.png)

## 12. Geometrical Sensitivity of FWM Phase Mismatch

The influence of waveguide geometry on the linear FWM phase mismatch was investigated by varying the core width and thickness around their nominal values.

The pump wavelength was fixed at 1550 nm, with the signal frequency detuned by 1 THz from the pump. The idler frequency was determined through energy conservation.

Five geometrical configurations were evaluated:

| Geometry | Width (µm) | Thickness (µm) | Phase mismatch magnitude (m⁻¹) |
|---|---:|---:|---:|
| Width −0.01 µm | 0.74 | 0.35 | 44.0130 |
| Nominal | 0.75 | 0.35 | 45.1689 |
| Width +0.01 µm | 0.76 | 0.35 | 46.2922 |
| Thickness −0.01 µm | 0.75 | 0.34 | 45.4615 |
| Thickness +0.01 µm | 0.75 | 0.36 | 44.9180 |

The results indicate that, within the investigated parameter range, the phase mismatch is more sensitive to changes in core width than to changes in core thickness.

A width reduction of 0.01 µm decreased the mismatch magnitude by approximately 2.56%, whereas a width increase of the same amount increased it by approximately 2.49%. Thickness variations produced smaller changes, below 0.7%.

These findings represent a preliminary numerical sensitivity assessment. They do not establish an optimized phase-matched design. The calculations use a simplified material and waveguide model, and further mesh refinement and broader parameter sweeps are needed.

![Geometrical sensitivity of FWM phase mismatch](../figures/fwm_geometry_sensitivity.png)
