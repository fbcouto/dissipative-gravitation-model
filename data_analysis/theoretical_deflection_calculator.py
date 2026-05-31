"""
Theoretical Deflection Calculator (DGM V2)
Author: Fernando B Couto
Description: Calculates optical deformation in the strictly elastic regime,
returning physical parameters for further research integration.
"""

import numpy as np
from scipy.constants import c, G, pi

# Conversion factor: Radians to Microarcseconds (uas)
RAD_TO_UAS = (180.0 * 3600.0 * 1e6) / pi

def calculate_elastic_deflection(target_name, mass, radius, v_eq, kappa_2, gamma_0=2.5):
    """
    Calculates the theoretical spacetime drag asymmetry (DGM V2) versus standard Kerr metrics.
    
    Returns:
        dict: A dictionary containing the theoretical values ready for data analysis.
    """
    # 1. Classical Einstein Deflection (Schwarzschild)
    theta_gr_rad = (4.0 * G * mass) / ((c**2) * radius)
    theta_gr_arcsec = theta_gr_rad * (180.0 / pi) * 3600.0

    # 2. Dimensionless Potential and Elastic Vortex Velocity
    pot_dimensionless = (G * mass) / (c**2 * radius)
    v_vortex = 4.0 * kappa_2 * pot_dimensionless * v_eq

    # 3. Lense-Thirring Asymmetry (Kerr Frame-Dragging)
    delta_kerr_rad = theta_gr_rad * (v_eq / c)
    delta_kerr_uas = delta_kerr_rad * RAD_TO_UAS

    # 4. Viscoelastic Asymmetry (DGM Theory)
    delta_dgm_rad = (4.0 * gamma_0 * G * mass * v_vortex) / (c**3 * radius)
    delta_dgm_uas = delta_dgm_rad * RAD_TO_UAS
    
    kerr_multiple = (delta_dgm_uas / delta_kerr_uas) if delta_kerr_uas > 0 else 0.0

    return {
        "target": target_name,
        "einstein_deflection_arcsec": theta_gr_arcsec,
        "boundary_potential": pot_dimensionless,
        "v_vortex_m_s": v_vortex,
        "kerr_drag_uas": delta_kerr_uas,
        "dgm_asym_uas": delta_dgm_uas,
        "multiple_of_kerr": kerr_multiple
    }

if __name__ == "__main__":
    # Example of how another researcher would use this module
    sun_data = calculate_elastic_deflection("Sun", 1.989e30, 6.9634e8, 1997.0, 0.059)
    print(f"Sun DGM Asymmetry: {sun_data['dgm_asym_uas']:.6f} uas")