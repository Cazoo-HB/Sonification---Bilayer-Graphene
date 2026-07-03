import numpy as np
import matplotlib.pyplot as plt
import os

"""
Simplified twisted bilayer honeycomb lattice generator.
Generates two separate figures:
1. Direct space (zoomed view)
2. Fourier space (log scale, grayscale, no decorations)
"""

# ============================================================
# USER PARAMETERS
# ============================================================
# Lattice generation
L_nm = 8*10.0          # real-space disk radius (nm)
alpha_deg = 1.10      # twist angle (deg)

# FFT parameters
N_fft = 8*512          # grid size for FFT (power of 2)
margin = 1.10         # extend real-space box beyond points (>=1.0)

# Graphene lattice constant
a_graphene_A = 2.46   # Å
a_nm = a_graphene_A * 0.1  # nm

# Direct space view limits (zoom control)
RS_XLIM = (-7.0, 7.0)   # nm
RS_YLIM = (-7.0, 7.0)   # nm

# Fourier space colormap limits (log10 scale)
VMIN_LOG = 2.0        # minimum value for log10(1 + amp)
VMAX_LOG = 5.0        # maximum value for log10(1 + amp)

# Fourier space zoom control
K_LIM = 50.0          # max k-value to display (rad/nm), set to None for full range

# Save parameters
SAVE_DIR = os.getcwd()  # default folder (current working directory)
DPI = 300               # resolution for PNG files

# ============================================================
# HONEYCOMB LATTICE GENERATION
# ============================================================
def honeycomb_points_disk(L_nm, a_nm):
    """
    Generates honeycomb lattice points inside a disk of radius L_nm.
    """
    a1 = np.array([a_nm, 0.0])
    a2 = np.array([0.5 * a_nm, 0.5 * np.sqrt(3) * a_nm])
    dAB = a_nm / np.sqrt(3)  # nearest-neighbor bond length
    basis = [np.array([0.0, 0.0]), np.array([0.0, dAB])]

    nmax = int(np.ceil((L_nm / a_nm) * 2.5)) + 2

    pts = []
    for n1 in range(-nmax, nmax + 1):
        for n2 in range(-nmax, nmax + 1):
            R = n1 * a1 + n2 * a2
            for b in basis:
                p = R + b
                if np.hypot(p[0], p[1]) <= L_nm:
                    pts.append(p)

    return np.array(pts) if pts else np.zeros((0, 2))

def rotate_points(points, angle_deg):
    """Rotate points by angle_deg."""
    ang = np.deg2rad(angle_deg)
    R = np.array([[np.cos(ang), -np.sin(ang)],
                  [np.sin(ang),  np.cos(ang)]], dtype=float)
    return points @ R.T

# ============================================================
# DENSITY IMAGE AND FFT
# ============================================================
def points_to_density(points, N, extent_nm):
    """
    Convert points to density image on grid.
    """
    half = extent_nm / 2.0
    x = points[:, 0]
    y = points[:, 1]
    edges = np.linspace(-half, half, N + 1)
    H, _, _ = np.histogram2d(y, x, bins=[edges, edges])
    return H

def fft_amplitude(density, extent_nm):
    """
    Compute FFT amplitude and k-space coordinates.
    Returns: amp(kx,ky), kx array, ky array (all in rad/nm)
    """
    N = density.shape[0]
    dx = extent_nm / N  # nm per pixel

    fx = np.fft.fftfreq(N, d=dx)  # cycles/nm
    fy = np.fft.fftfreq(N, d=dx)

    kx = 2 * np.pi * fx  # rad/nm
    ky = 2 * np.pi * fy

    F = np.fft.fft2(density)
    F = np.fft.fftshift(F)
    amp = np.abs(F)

    kx = np.fft.fftshift(kx)
    ky = np.fft.fftshift(ky)

    return amp, kx, ky

# ============================================================
# GENERATE LATTICES
# ============================================================
print("Generating honeycomb lattices...")
ptsA = honeycomb_points_disk(L_nm=L_nm, a_nm=a_nm)
ptsB = rotate_points(ptsA, alpha_deg)
all_points = np.vstack([ptsA, ptsB])

print(f"Layer A: {len(ptsA)} atoms")
print(f"Layer B: {len(ptsB)} atoms")

# ============================================================
# COMPUTE FFT
# ============================================================
max_xy = np.max(np.abs(all_points)) if all_points.size else L_nm
extent_nm = margin * 2.0 * max(max_xy, L_nm)

print(f"Creating density grid ({N_fft}x{N_fft})...")
density = points_to_density(all_points, N=N_fft, extent_nm=extent_nm)

print("Computing FFT...")
amp, kx, ky = fft_amplitude(density, extent_nm)
amp_log = np.log10(1 + amp)

# ============================================================
# PLOT AND SAVE
# ============================================================
print("Creating plots...")

# Figure 1: Direct space
fig1 = plt.figure(figsize=(8, 8))
ax1 = fig1.add_subplot(111)
ax1.set_aspect("equal", "box")
ax1.set_xlabel("x (nm)")
ax1.set_ylabel("y (nm)")
ax1.set_title(f"Direct space (α = {alpha_deg}°)")
ax1.scatter(ptsA[:, 0], ptsA[:, 1], s=0.6, alpha=0.55, label="Layer A")
ax1.scatter(ptsB[:, 0], ptsB[:, 1], s=0.6, alpha=0.55, label="Layer B")
ax1.legend(loc="upper right", fontsize=9)
ax1.set_xlim(RS_XLIM)
ax1.set_ylim(RS_YLIM)
plt.tight_layout()

# Save Figure 1
filename1 = os.path.join(SAVE_DIR, f"direct_space_alpha_{alpha_deg:.3f}deg.png")
fig1.savefig(filename1, dpi=DPI, bbox_inches='tight')
print(f"Saved: {filename1}")

# Figure 2: Fourier space (no decorations)
fig2 = plt.figure(figsize=(8, 8))
ax2 = fig2.add_subplot(111)
ax2.imshow(
    amp_log,
    origin="lower",
    extent=[kx[0], kx[-1], ky[0], ky[-1]],
    aspect="equal",
    cmap="gray",
    vmin=VMIN_LOG,
    vmax=VMAX_LOG,
    interpolation="nearest"
)

# Apply k-space zoom if K_LIM is set
if K_LIM is not None:
    ax2.set_xlim(-K_LIM, K_LIM)
    ax2.set_ylim(-K_LIM, K_LIM)

ax2.axis('off')  # Remove all axes, labels, ticks
plt.tight_layout()

# Save Figure 2
filename2 = os.path.join(SAVE_DIR, f"fourier_space_alpha_{alpha_deg:.3f}deg.png")
fig2.savefig(filename2, dpi=DPI, bbox_inches='tight')
print(f"Saved: {filename2}")

plt.show()

print("Done!")