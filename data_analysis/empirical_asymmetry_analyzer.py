"""
Empirical Asymmetry Analyzer (Gaia DR3 / VLBI)
Processes local CSV files and returns partitioned spatial-drag DataFrames.
"""

import pandas as pd
from astropy.coordinates import get_body
from astropy.time import Time
import warnings

warnings.filterwarnings('ignore')

def analyze_csv_asymmetry(csv_filepath, target_planet='jupiter', transit_time_str="2022-09-26T00:00:00"):
    """
    Calculates empirical spatial drag asymmetry (Delta) based on local CSV data.
    
    Args:
        csv_filepath (str): Path to the empirical data CSV.
        target_planet (str): Target planetary body for ephemeris calculation.
        transit_time_str (str): ISO formatted time string.
        
    Returns:
        dict: Contains DataFrames for prograde/retrograde sectors and statistical metrics.
    """
    transit_time = Time(transit_time_str)
    
    try:
        planet_pos = get_body(target_planet, transit_time)
        planet_ra = planet_pos.ra.deg
    except Exception as e:
        raise ValueError(f"Failed to calculate ephemeris: {e}")

    # Load data
    df = pd.read_csv(csv_filepath, header=0, skipinitialspace=True)
    df['ra'] = pd.to_numeric(df['ra'], errors='coerce')
    df['astrometric_excess_noise'] = pd.to_numeric(df['astrometric_excess_noise'], errors='coerce')
    df = df.dropna(subset=['ra', 'astrometric_excess_noise'])

    # Partition the spatial mesh (Prograde vs Retrograde)
    prograde_df = df[df['ra'] > planet_ra]
    retrograde_df = df[df['ra'] <= planet_ra]

    avg_pro = prograde_df['astrometric_excess_noise'].mean()
    avg_anti = retrograde_df['astrometric_excess_noise'].mean()
    delta = avg_pro - avg_anti

    return {
        "planet_ra": planet_ra,
        "total_sources": len(df),
        "prograde_df": prograde_df,
        "retrograde_df": retrograde_df,
        "prograde_mean_mas": avg_pro,
        "retrograde_mean_mas": avg_anti,
        "asymmetry_delta_mas": delta
    }

if __name__ == "__main__":
    # Example usage for other researchers:
    try:
        results = analyze_csv_asymmetry("gaia_anomalies.csv")
        print(f"Successfully processed {results['total_sources']} empirical sources.")
        print(f"Calculated Delta (DGM Signature): {results['asymmetry_delta_mas']:.4f} mas")
    except FileNotFoundError:
        print("Please ensure 'gaia_anomalies.csv' is available to run the test.")