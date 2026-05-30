"""
Dissipative Gravitation Model - Theoretical Deflection Calculator
Author: Fernando B Couto
Description: Calculates the theoretical asymmetric deflection of light 
(space-drag anomaly) around a rotating massive body using the 
viscoelastic vacuum tension parameter (gamma_0).
"""

import math
from scipy.constants import c, G, pi

def calculate_theoretical_deflection(mass_kg, radius_m, v_eq_m_s, gamma_0):
    print("==========================================================")
    print(" DISSIPATIVE GRAVITATION MODEL - THEORETICAL PREDICTION")
    print("==========================================================")
    
    # 1. DEFLEXÃO CLÁSSICA (Relatividade Geral - Schwarzschild)
    # Fórmula: theta_GR = 4GM / (c^2 * R)
    theta_gr_rad = (4 * G * mass_kg) / ((c**2) * radius_m)
    
    # Conversão de Radianos para Segundos de Arco (arcsec) e Micro-arcosegundos (µas)
    rad_to_arcsec = (180.0 / pi) * 3600.0
    theta_gr_arcsec = theta_gr_rad * rad_to_arcsec
    
    print(f"\n[1] EINSTEIN'S STATIC DEFLECTION (Baseline)")
    print(f"    Expected: {theta_gr_arcsec:.6f} arcsec")

    # 2. ASSIMETRIA DE ARRASTAMENTO CLÁSSICA (Efeito Lense-Thirring / Kerr)
    # A rotação do Sol "arrasta" a geometria do espaço
    # Aproximação do frame-dragging: delta_kerr = theta_GR * (v_eq / c)
    vortex_velocity_ratio = v_eq_m_s / c
    delta_kerr_rad = theta_gr_rad * vortex_velocity_ratio
    delta_kerr_uas = (delta_kerr_rad * rad_to_arcsec) * 1e6
    
    print(f"\n[2] STANDARD FRAME-DRAGGING (Kerr Metric Geometry)")
    print(f"    Expected asymmetry: {delta_kerr_uas:.6f} µas")

    # 3. AMPLIFICAÇÃO VISCOELÁSTICA (A Assinatura DGM - Teoria de Couto)
    # O vácuo tem tensão (gamma_0). A luz sofre arrastamento de Fresnel análogo.
    # Se gamma_0 = 1, comporta-se como a Relatividade Geral. 
    # Se gamma_0 > 1, o fluido cria mais arrasto refrativo.
    
    delta_dgm_rad = delta_kerr_rad * gamma_0
    delta_dgm_uas = (delta_dgm_rad * rad_to_arcsec) * 1e6
    
    print(f"\n[3] COUTO'S VISCOELASTIC DRAG (DGM Prediction with γ₀ = {gamma_0})")
    print(f"    Left Side Deflection (With Vortex):    + {delta_dgm_uas/2:.6f} µas")
    print(f"    Right Side Deflection (Against Vortex): - {delta_dgm_uas/2:.6f} µas")
    print(f"    --------------------------------------------------")
    print(f"    TOTAL THEORETICAL ASYMMETRY (Δ):          {delta_dgm_uas:.6f} µas")
    print("==========================================================\n")
    
    return delta_dgm_uas

if __name__ == "__main__":
    # PARÂMETROS FÍSICOS DO SOL
    M_sun = 1.989e30        # Massa do Sol em kg
    R_sun = 6.9634e8        # Raio do Sol em metros
    V_eq_sun = 1997.0       # Velocidade de rotação no equador (m/s)
    
    # PARÂMETRO DA TEORIA DGM (Afinável)
    # Um vácuo perfeitamente "vazio" teria gamma_0 = 1.0
    # O modelo Dissipativo sugere um vácuo "tenso" / viscoso. Vamos testar um valor de 2.5
    GAMMA_0 = 2.5           
    
    calculate_theoretical_deflection(M_sun, R_sun, V_eq_sun, GAMMA_0)