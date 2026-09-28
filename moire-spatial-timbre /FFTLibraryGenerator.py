
"""
Created on Thu Feb 26 10:18:21 2026

@author: cedriccazorla
"""


import numpy as np
import os

def honeycomb_points_disk(L_nm, a_nm=0.246):
    a1, a2 = np.array([a_nm, 0.0]), np.array([0.5*a_nm, 0.5*np.sqrt(3)*a_nm])
    dAB = a_nm / np.sqrt(3)
    basis = [np.array([0.0, 0.0]), np.array([0.0, dAB])]
    nmax = int(np.ceil((L_nm/a_nm)*2.5)) + 2
    pts = []
    for n1 in range(-nmax, nmax + 1):
        for n2 in range(-nmax, nmax + 1):
            R = n1*a1 + n2*a2
            for b in basis:
                p = R + b
                if np.hypot(p[0], p[1]) <= L_nm: pts.append(p)
    return np.array(pts)

def rotate_points(pts, deg):
    ang = np.deg2rad(deg)
    R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    return pts @ R.T

def generate_targeted_library(L_nm=75, N_fft=2*2048, alpha_range=(1, 1.2, 0.001), k_limit=30, filename="moire_lib.npz"):
    """
    L_nm: Plus grand = pics plus fins.
    k_limit: 45 nm^-1 pour inclure les 2èmes pics de Bragg.
    """
    alphas = np.arange(alpha_range[0], alpha_range[1] + alpha_range[2], alpha_range[2])
    pts_base = honeycomb_points_disk(L_nm)
    extent = 1.1 * 2.0 * L_nm
    edges = np.linspace(-extent/2, extent/2, N_fft + 1)
    
    # Vecteur K complet
    dx = extent / N_fft
    k_full = np.fft.fftshift(2 * np.pi * np.fft.fftfreq(N_fft, d=dx))
    
    # Masque pour ne garder que le centre (Bragg + Moire)
    mask = (k_full >= -k_limit) & (k_full <= k_limit)
    k_cropped = k_full[mask]
    
    all_amps = []
    print(f"Targeting k_limit = {k_limit} nm^-1 | Resolution: {len(k_cropped)}px")
    
    for i, a in enumerate(alphas):
        pts_twist = rotate_points(pts_base, a)
        all_pts = np.vstack([pts_base, pts_twist])
        density, _, _ = np.histogram2d(all_pts[:, 1], all_pts[:, 0], bins=[edges, edges])
        amp = np.abs(np.fft.fftshift(np.fft.fft2(density)))
        
        # Crop
        amp_cropped = amp[mask, :][:, mask]
        all_amps.append(amp_cropped.astype(np.float32))
        
        if i % 10 == 0: print(f"Alpha {a:.2f}° done...")

    np.savez_compressed(filename, amplitudes=all_amps, angles=alphas, k_vec=k_cropped, L_nm=L_nm)
    print(f"Success! File saved as {filename}")

if __name__ == "__main__":
    # Paramètres suggérés pour une excellente qualité
    generate_targeted_library(L_nm=75, N_fft=2*2048, alpha_range=(1, 1.2, 0.001), k_limit=30)
    
    
    
    
    
    
    
    
    
