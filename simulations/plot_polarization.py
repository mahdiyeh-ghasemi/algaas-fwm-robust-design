import matplotlib.pyplot as plt
import numpy as np

from src.mode_solver import solve_waveguide_modes
from src.polarization_analysis import analyze_polarization


neff, Ex, Ey, Ezj, Hx, Hy, Hzj = solve_waveguide_modes()
results = analyze_polarization(Ex, Ey, Ezj)

modes = [f"Mode {r['mode']}" for r in results]
ex = [100 * r["Ex_transverse"] for r in results]
ey = [100 * r["Ey_transverse"] for r in results]
ez = [100 * r["Ez_total"] for r in results]

x = np.arange(len(modes))
width = 0.25

fig, ax = plt.subplots(figsize=(9, 5))

ax.bar(x - width, ex, width, label="Ex (transverse)")
ax.bar(x, ey, width, label="Ey (transverse)")
ax.bar(x + width, ez, width, label="Ez (total)")

ax.set_ylabel("Normalized squared-field metric (%)")
ax.set_title("Electric-Field Component Analysis of Waveguide Modes")
ax.set_xticks(x)
ax.set_xticklabels(modes)
ax.set_ylim(0, 110)
ax.legend()
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("figures/polarization_analysis.png", dpi=300)
plt.show()