#!/usr/bin/env python3
"""
Resolvent norm landscape: ||(zI - A)^-1|| for non-normal Jordan block.

Two images:
1. Complex plane heatmap — resolvent blowup away from diagonal (non-normality)
2. Real axis slice — blowup BEFORE eigenvalues (anticipation)

This is the pseudospectral ε-plate boundary as clutching function.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

A = np.array([[2+0j, 1+0j, 0+0j],
               [0+0j, 3+0j, 1+0j],
               [0+0j, 0+0j, 4+0j]])

re = np.linspace(-0.5, 5.5, 200)
im = np.linspace(-3, 3, 150)
R, I = np.meshgrid(re, im)
Z = R + 1j * I

norms = np.zeros_like(Z)
for i in range(R.shape[0]):
    for j in range(R.shape[1]):
        z = complex(R[i,j], I[i,j])
        try:
            norms[i,j] = np.linalg.norm(np.linalg.inv(z * np.eye(3) - A))
        except:
            norms[i,j] = 1e10

# Clamp for display
norms_clamped = np.clip(norms, 0, 20)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Image 1: Complex plane heatmap
im1 = axes[0].contourf(R, I, norms_clamped, levels=30, cmap='hot_r')
axes[0].axhline(0, color='white', linewidth=0.5, alpha=0.3)
axes[0].axvline(0, color='white', linewidth=0.5, alpha=0.3)
for ev in [2, 3, 4]:
    axes[0].plot(ev, 0, 'ko', markersize=8, label=f'λ={ev}')
axes[0].set_xlabel('Re(z)')
axes[0].set_ylabel('Im(z)')
axes[0].set_title('||(zI - A)⁻¹||')
plt.colorbar(im1, ax=axes[0], label='norm')

# Image 2: Real axis slice
real_slice = np.array([np.linalg.norm(np.linalg.inv((r+0j) * np.eye(3) - A))
                        for r in re])
real_clamped = np.clip(real_slice, 0, 20)
axes[1].plot(re, real_clamped, 'w', linewidth=2)
for ev in [2, 3, 4]:
    axes[1].axvline(ev, color='gray', linestyle='--', alpha=0.5)
axes[1].set_xlabel('Re(z)')
axes[1].set_ylabel('||R(z)||')
axes[1].set_title('Real axis slice — blowup before eigenvalues')

plt.tight_layout()
plt.savefig('./assets/resolvent-landscape.png', dpi=150, facecolor='black',
            edgecolor='none')
print("Saved: resolvent-landscape.png")
