from src.mode_solver import solve_waveguide_modes
from src.polarization_analysis import analyze_polarization

neff, Ex, Ey, Ezj, Hx, Hy, Hzj = solve_waveguide_modes()

results = analyze_polarization(Ex, Ey, Ezj)

print("\nPolarization Analysis")
print("---------------------")

for result in results:
    print(f"\nMode {result['mode']}")
    print(f"Effective index: {neff[result['mode'] - 1]:.8f}")
    print(f"Ex transverse fraction: {100 * result['Ex_transverse']:.2f}%")
    print(f"Ey transverse fraction: {100 * result['Ey_transverse']:.2f}%")
    print(f"Ez fraction of total: {100 * result['Ez_total']:.2f}%")