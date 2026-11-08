
# Methodology: Numerical Modeling and Fabrication-Tolerant Design

## 1. Research Workflow

The project investigates the numerical design of AlGaAs-on-insulator waveguides for four-wave mixing (FWM), with an emphasis on phase matching and fabrication tolerance.

The methodology is organized into five stages:

1. Definition of the waveguide geometry and material parameters.
2. Calculation of modal properties and waveguide dispersion.
3. Evaluation of phase-matching conditions.
4. Analysis of sensitivity to geometrical variations.
5. Numerical optimization of fabrication-tolerant geometries.

The model will be developed progressively, with assumptions and parameter sources documented at each stage.

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

## 4. Numerical Mesh Convergence

The influence of spatial discretization on the calculated effective indices is assessed by repeating the eigenmode calculations with different grid spacings.

The following grid spacings are considered:

- 0.025 µm
- 0.0125 µm
- 0.00625 µm

The effective indices obtained at successive grid resolutions are compared to evaluate numerical convergence.

The results indicate that the fundamental mode is relatively stable with respect to mesh refinement. Higher-order modes exhibit larger changes and therefore require additional convergence assessment.

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

### 7.1 Modal Identity Tracking

To assess the continuity of the calculated modes across the wavelength range, an electric-field overlap analysis is performed between consecutive wavelength points.

For each pair of adjacent wavelengths, the normalized squared overlap between the electric-field distributions is calculated:

\[
O_{ij} =
\frac{
|\langle E_i(\lambda_k), E_j(\lambda_{k+1}) \rangle|^2
}{
\langle E_i(\lambda_k), E_i(\lambda_k) \rangle
\langle E_j(\lambda_{k+1}), E_j(\lambda_{k+1}) \rangle
}
\]

The overlap calculation combines the three electric-field components \(E_x\), \(E_y\), and \(E_z\). The mode correspondence between successive wavelength points is determined by maximizing the total overlap using the linear assignment algorithm.

The discrete inner product is evaluated as a sum over all transverse grid points and the three electric-field components, using the same spatial grid at both wavelengths.

For the wavelength sweep from 1500 nm to 1600 nm, with a 5 nm increment, the calculated mode correspondence remains unchanged across all consecutive wavelength pairs.

The minimum matched overlap obtained in this analysis is approximately 0.999963.

These results indicate strong continuity of the calculated electric-field profiles across the sampled wavelength range. They support the use of the fundamental-mode effective-index data for the current dispersion analysis.

This overlap analysis is a numerical mode-tracking check. It does not independently establish the physical accuracy of the waveguide model or replace validation against experimental or reference data.

## 8. Phase Matching and Fabrication Tolerance

The next stage of the project will investigate four-wave-mixing phase-matching conditions using the calculated modal propagation constants.

The phase mismatch will be evaluated for the interacting pump, signal, and idler waves.

Subsequently, the sensitivity of phase matching to variations in waveguide width, core thickness, and material composition will be investigated.

The final objective is to identify geometrical configurations that maintain acceptable phase-matching conditions under realistic fabrication variations.
