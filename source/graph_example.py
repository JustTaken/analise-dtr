import numpy as np
import matplotlib.pyplot as plt

# Use LaTeX for all text rendering
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 12,
    "axes.labelsize": 12,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

# Example data
t = np.linspace(0, 24, 100)
h2 = 20 * (1 - np.exp(-0.15 * t))

# Figure size in inches
PAGE_WIDTH = 455.24
INCHES_PER_PT = 1 / 72.27
width = PAGE_WIDTH * INCHES_PER_PT
height = width * 0.5
fig, ax = plt.subplots(figsize=(width, height))

ax.plot(t, h2, label=r"$H_2$ Production")

ax.set_xlabel(r"Time (h)")
ax.set_ylabel(r"$H_2$ Concentration (mmol L$^{-1}$)")
ax.set_title(r"Dark Fermentation of Glucose")
ax.legend()

plt.tight_layout()

plt.savefig("h2_production.pdf")
