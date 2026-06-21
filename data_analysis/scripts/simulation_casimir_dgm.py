import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure output directory exists
os.makedirs('data_analysis/plots', exist_ok=True)

# =====================================================================
# 1. UNIVERSAL PHYSICAL CONSTANTS (SI)
# =====================================================================
c = 299792458.0              # Speed of light (m/s)
G = 6.67430e-11              # Gravitational Constant (m^3 kg^-1 s^-2)
hbar = 1.054571817e-34       # Reduced Planck Constant (J.s)
pi = np.pi

# =====================================================================
# 2. DGM DIMENSIONAL DECOMPOSITION
# =====================================================================
# Maximum force of the spatial tissue (Planck Force)
F_planck = (c**4) / G

# Smallest topological mesh (Planck Area)
l_planck_sq = (hbar * G) / (c**3)

# Primordial Base Tension of the Universe (The grand DGM constant)
gamma_0 = F_planck / (8 * pi)

print("=" * 60)
print("QUANTUM VACUUM DECOMPOSITION (DGM)")
print("=" * 60)
print(f"Planck Force (F_p):                {F_planck:.2e} Newtons")
print(f"Primordial Base Tension (Gamma_0): {gamma_0:.2e} Pa")
print("-" * 60)

# DGM Geometric Identity Verification (F_p * l_p^2 == hbar * c)
gravitational_term = F_planck * l_planck_sq
quantum_term = hbar * c
identity_error = abs(gravitational_term - quantum_term) / quantum_term

if identity_error < 1e-10:
    print("QUANTUM VERDICT: The DGM Identity (F_p * l_p^2 = hbar * c) is MATHEMATICALLY EXACT.")
    print("The Planck constant was successfully dissolved into the Base Tension of space.")

# =====================================================================
# 3. FORCE CALCULATION (DGM vs QED) AT NANOSCALE
# =====================================================================
# Distance 'd' between Casimir plates (from 10 nm to 200 nm)
d_nm = np.linspace(10, 200, 500)
d_m = d_nm * 1e-9

# A) Standard Quantum Electrodynamics Pressure (Zero-Point Fluctuations)
Pressure_QED = (pi**2 * hbar * c) / (240 * d_m**4)

# B) DGM Acoustic Pressure (Macroscopic Crushing by Gamma_0)
Pressure_DGM = (pi**3 / 30) * gamma_0 * (l_planck_sq / d_m**4)

# =====================================================================
# 4. ACOUSTIC SHADOW PLOT RENDERING
# =====================================================================
plt.figure(figsize=(10, 6), facecolor='white')

plt.plot(d_nm, Pressure_QED, '-', color='#2c7bb6', linewidth=4, alpha=0.6,
         label='Standard QED (Virtual Particles)')
plt.plot(d_nm, Pressure_DGM, '--', color='#d7191c', linewidth=2.5,
         label=r'DGM (Crushing by Primordial Tension $\gamma_0$)')

plt.yscale('log')
plt.xlabel('Distance between Plates (nm)', fontsize=12)
plt.ylabel('Crushing Pressure (Pascals)', fontsize=12)
plt.title('Casimir-DGM Unification: Acoustic Shadow vs False Vacuum', fontsize=14, pad=15)
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=11)
plt.tight_layout()

# Save Plot
plot_path = 'data_analysis/plots/dgm_casimir_unification.png'
plt.savefig(plot_path, dpi=300)
print(f"\nPlot saved to: {plot_path}")
plt.close()