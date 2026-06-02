"""
Theoretical Deflection Calculator (DGM V2)
Calculates optical deformation in the strictly elastic regime.
"""

import numpy as np
from scipy.constants import c, G, pi

RAD_TO_MAS = (180.0 / pi) * 3600.0 * 1000.0 
RAD_TO_UAS = RAD_TO_MAS * 1000.0            
GAMMA_0 = 4.82e42                            
N_VAC = 2.79e31                              

def calculate_elastic_deflection(target_name, mass, radius, v_eq, kappa_2):
    theta_gr_rad = (4.0 * G * mass) / ((c**2) * radius)
    theta_gr_arcsec = theta_gr_rad * (180.0 / pi) * 3600.0

    pot_dimensionless = (G * mass) / (c**2 * radius)
    v_vortex = 4.0 * kappa_2 * pot_dimensionless * v_eq

    delta_kerr_rad = theta_gr_rad * (v_eq / c)
    delta_kerr_uas = delta_kerr_rad * RAD_TO_UAS

    tension_ratio = GAMMA_0 / N_VAC
    delta_dgm_rad = (4.0 * tension_ratio * G * mass * v_vortex) / (c**3 * radius)
    
    delta_dgm_mas = delta_dgm_rad * RAD_TO_MAS
    delta_dgm_uas = delta_dgm_rad * RAD_TO_UAS
    
    kerr_multiple = (delta_dgm_uas / delta_kerr_uas) if delta_kerr_uas > 0 else 0.0

    return {
        "target": target_name,
        "einstein_deflection_arcsec": theta_gr_arcsec,
        "boundary_potential": pot_dimensionless,
        "v_vortex_m_s": v_vortex,
        "kerr_drag_uas": delta_kerr_uas,
        "dgm_asym_mas": delta_dgm_mas,
        "dgm_asym_uas": delta_dgm_uas,
        "multiple_of_kerr": kerr_multiple
    }

if __name__ == "__main__":
    print("==========================================================")
    print(" DGM V2: THEORETICAL DEFLECTION CALCULATOR (NORMALIZED)")
    print("==========================================================\n")
    
    # Physics parameters
    jupiter = calculate_elastic_deflection("Jupiter", 1.898e27, 7.1492e7, 12600.0, 0.2756)
    # Venus is extremely slow (V_eq = 1.81 m/s) and spins backwards.
    venus = calculate_elastic_deflection("Venus", 4.867e24, 6.0518e6, 1.81, 0.33)
    
    print(f"Júpiter Asymmetry (DGM V2): {jupiter['dgm_asym_mas']:.4f} mas")
    print(f"Vénus Asymmetry (DGM V2):   {venus['dgm_asym_mas']:.6f} mas")