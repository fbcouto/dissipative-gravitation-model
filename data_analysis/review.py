"""
DGM V2: Paradigm Review Validator
Generates a comparative DataFrame between Legacy Volume Drag and Elastic Coupling Regime.
"""

import pandas as pd
from theoretical_deflection_calculator import calculate_elastic_deflection

def generate_paradigm_review_df():
    """
    Evaluates specific celestial bodies using the DGM V2 equations.
    
    Returns:
        pd.DataFrame: Comparative table of gravitational metrics.
    """
    targets = [
        {"name": "Sun", "M": 1.989e30, "R": 6.9634e8, "V_eq": 1997.0, "kappa_2": 0.059},
        {"name": "Jupiter", "M": 1.898e27, "R": 7.1492e7, "V_eq": 12600.0, "kappa_2": 0.2756},
        {"name": "Saturn", "M": 5.683e26, "R": 6.0268e7, "V_eq": 9800.0, "kappa_2": 0.2200},
        {"name": "Neutron Star (Pulsar)", "M": 1.4 * 1.989e30, "R": 10000.0, "V_eq": 1.0e8, "kappa_2": 0.400}
    ]

    results = []
    for t in targets:
        # Fetch calculated physics data
        data = calculate_elastic_deflection(t["name"], t["M"], t["R"], t["V_eq"], t["kappa_2"])
        
        results.append({
            "Target": data["target"],
            "Boundary Potential": f"{data['boundary_potential']:.3e}",
            "Vortex Velocity (m/s)": f"{data['v_vortex_m_s']:.3e}",
            "Kerr Drag (uas)": f"{data['kerr_drag_uas']:.6f}",
            "Elastic Asymmetry (uas)": f"{data['dgm_asym_uas']:.10f}"
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    df = generate_paradigm_review_df()
    print(df.to_string(index=False))