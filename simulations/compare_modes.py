import matplotlib.pyplot as plt
from PIL import Image

fig, axes = plt.subplots(2, 2, figsize=(12, 9))

for i, ax in enumerate(axes.flat, start=1):
    image = Image.open(f"figures/mode_{i}.png")
    ax.imshow(image)
    ax.set_title(f"Mode {i}")
    ax.axis("off")

plt.tight_layout()
plt.savefig("figures/all_modes_comparison.png", dpi=200)
plt.close()

print("Combined mode comparison saved.")
