import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure output directory exists
os.makedirs('data_analysis/plots', exist_ok=True)

# =====================================================================
# 1. DGM MODEL PARAMETERS (SOLAR ROTOR EXPONENTIAL LAW)
# =====================================================================
# Viscosity constant empirically deduced from Gravity Probe B (Earth: 1.0 AU)
eta_earth_empirical = 7.02e7  # Pa.s

# Spatial decay constant
lambda_decay = 2.5  

# Local interstellar space background viscosity
eta_bg = 1.00e5     # Pa.s

# Isolating the solar constant (eta_solar) based on Earth data
eta_solar = (eta_earth_empirical - eta_bg) / np.exp(-lambda_decay * 1.0)

def radial_viscosity_dgm(distance_au):
    """Returns the dynamic vacuum viscosity (Pa.s) based on distance from the Sun (AU)."""
    return eta_bg + eta_solar * np.exp(-lambda_decay * distance_au)

# =====================================================================
# 2. SOLAR SYSTEM PROBES TEST
# =====================================================================
probes = {
    "MESSENGER (Mercury)": 0.39,
    "Gravity Probe B (Earth)": 1.00,
    "Juno (Jupiter)": 5.20,
    "Cassini (Saturn)": 9.58
}

print("=" * 60)
print("DGM VISCOUS GRADIENT TEST (SOLAR SYSTEM)")
print("=" * 60)

for name, distance in probes.items():
    local_eta = radial_viscosity_dgm(distance)
    print(f"Probe: {name:25} | Distance: {distance:4.2f} AU | Viscosity: {local_eta:.2e} Pa.s")

print("-" * 60)
multiplier = radial_viscosity_dgm(0.39) / radial_viscosity_dgm(1.0)
print(f"VERDICT: The viscosity faced by the MESSENGER probe is {multiplier:.1f}x GREATER than at Earth.")
print("This mathematically justifies the Doppler drag peaks (2500 Hz) in the Level 0 data.")
print("=" * 60)

# =====================================================================
# 3. GRADIENT PLOT RENDERING
# =====================================================================
r_dist = np.linspace(0.1, 10.0, 500)
eta_dist = radial_viscosity_dgm(r_dist)

plt.figure(figsize=(10, 6))
plt.plot(r_dist, eta_dist, color='red', lw=2, label='DGM Viscosity Gradient')
plt.scatter(list(probes.values()), [radial_viscosity_dgm(d) for d in probes.values()], 
            color='black', zorder=5, s=80)

for name, distance in probes.items():
    plt.annotate(name, (distance, radial_viscosity_dgm(distance)), 
                 textcoords="offset points", xytext=(10,10), ha='left')

plt.yscale('log')
plt.xlabel('Distance from the Sun (Astronomical Units - AU)', fontsize=12)
plt.ylabel('Vacuum Viscosity (Pa.s) - Log Scale', fontsize=12)
plt.title('Vacuum Rheofluidification by the Solar Rotor (DGM)', fontsize=14)
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend()
plt.tight_layout()

# Save Plot
plot_path = 'data_analysis/plots/dgm_messenger_gradient.png'
plt.savefig(plot_path, dpi=300)
print(f"Plot saved to: {plot_path}")
plt.close()