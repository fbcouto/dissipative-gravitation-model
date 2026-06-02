"""
DGM V2: Paradigm Review Validator
Generates a comparative DataFrame between standard metrics and the Elastic Coupling Regime.
"""

import pandas as pd
from theoretical_deflection_calculator import calculate_elastic_deflection

def generate_paradigm_review_df():
    targets = [
        {"name": "Sun (Baseline)", "M": 1.989e30, "R": 6.9634e8, "V_eq": 1997.0, "kappa_2": 0.059},
        {"name": "Jupiter (Prograde)", "M": 1.898e27, "R": 7.1492e7, "V_eq": 12600.0, "kappa_2": 0.2756},
        {"name": "Venus (Retrograde)", "M": 4.867e24, "R": 6.0518e6, "V_eq": 1.81, "kappa_2": 0.33},
        {"name": "Neutron Star", "M": 1.4 * 1.989e30, "R": 10000.0, "V_eq": 1.0e8, "kappa_2": 0.400}
    ]

    results = []
    for t in targets:
        data = calculate_elastic_deflection(t["name"], t["M"], t["R"], t["V_eq"], t["kappa_2"])
        
        results.append({
            "Target": data["target"],
            "Boundary Potential": f"{data['boundary_potential']:.3e}",
            "Vortex Velocity (m/s)": f"{data['v_vortex_m_s']:.3e}",
            "Kerr Drag (uas)": f"{data['kerr_drag_uas']:.6f}",
            "Elastic Asym DGM (mas)": f"{data['dgm_asym_mas']:.6f}"
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = generate_paradigm_review_df()
    print(df.to_string(index=False))