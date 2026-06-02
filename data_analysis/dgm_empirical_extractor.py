"""
DGM V2: Robust Empirical Extractor (Gaia DR3)
Focuses exclusively on Jupiter (Prograde Control) and Venus (Retrograde Control).
Downloads optimal DR3 epoch data, applies Axial Tilt matrices, and saves CSVs.
"""

from astroquery.gaia import Gaia
from astropy.time import Time
from astropy.coordinates import get_body, solar_system_ephemeris
import numpy as np
import pandas as pd
import warnings
import math
import os

warnings.filterwarnings('ignore')

PLANET_CONFIG = {
    'jupiter': {
        'optimal_date': '2016-03-08T00:00:00', # DR3 Epoch: Opposition in Leo
        'obliquity_deg': 3.13,
        'is_retrograde': False
    },
    'venus': {
        'optimal_date': '2016-10-25T00:00:00', # DR3 Epoch: Conjunction near Milky Way
        'obliquity_deg': 177.36,
        'is_retrograde': True
    }
}

def rotate_to_true_equator(x_arcsec, y_arcsec, tilt_deg):
    theta = math.radians(tilt_deg)
    x_rot = x_arcsec * math.cos(theta) - y_arcsec * math.sin(theta)
    y_rot = x_arcsec * math.sin(theta) + y_arcsec * math.cos(theta)
    return x_rot, y_rot

def fetch_and_analyze(target_planet, config):
    print(f"\n==========================================================")
    print(f" DGM V2: EXTRACTION - {target_planet.upper()}")
    print(f"==========================================================")
    
    transit_time = Time(config['optimal_date'])
    with solar_system_ephemeris.set('builtin'):
        planet_pos = get_body(target_planet, transit_time)
    
    planet_ra = planet_pos.ra.deg
    planet_dec = planet_pos.dec.deg
    tilt = config['obliquity_deg']
    
    print(f"[*] Ephemeris ({config['optimal_date']}): RA={planet_ra:.4f}°, DEC={planet_dec:.4f}°")
    
    ra_min, ra_max = planet_ra - 3.0, planet_ra + 3.0
    dec_min, dec_max = planet_dec - 3.0, planet_dec + 3.0
    
    if ra_min < 0:
        ra_condition = f"(ra >= {ra_min + 360.0} OR ra <= {ra_max})"
    elif ra_max > 360:
        ra_condition = f"(ra >= {ra_min} OR ra <= {ra_max - 360.0})"
    else:
        ra_condition = f"(ra BETWEEN {ra_min} AND {ra_max})"

    adql_query = f"""
    SELECT TOP 25000 
        source_id, ra, dec, phot_g_mean_mag, astrometric_excess_noise
    FROM gaiadr3.gaia_source
    WHERE phot_g_mean_mag < 15.0 
      AND astrometric_excess_noise > 1.0
      AND {ra_condition}
      AND dec BETWEEN {dec_min} AND {dec_max}
    ORDER BY astrometric_excess_noise DESC
    """
    
    print("[*] Executing ADQL Query...")
    job = Gaia.launch_job_async(adql_query)
    results = job.get_results()

    # Convert to Pandas for processing and saving
    df = results.to_pandas()
    
    x_true_list, side_list = [], []
    
    for _, row in df.iterrows():
        dra = (row['ra'] - planet_ra) * math.cos(math.radians(planet_dec))
        ddec = row['dec'] - planet_dec
        
        # Apply matrix rotation
        x_true, _ = rotate_to_true_equator(dra * 3600.0, ddec * 3600.0, tilt)
        x_true_list.append(x_true)
        
        # Determine logical side based on rotation direction
        if config['is_retrograde']:
            side_list.append('Prograde' if x_true < 0 else 'Retrograde')
        else:
            side_list.append('Prograde' if x_true > 0 else 'Retrograde')

    df['x_true_equator'] = x_true_list
    df['dgm_sector'] = side_list
    
    output_file = f"{target_planet}_dr3_anomalies.csv"
    df.to_csv(output_file, index=False)
    print(f"[+] Extraction complete. Saved {len(df)} sources to '{output_file}'.")

if __name__ == "__main__":
    for planet, config in PLANET_CONFIG.items():
        fetch_and_analyze(planet, config)