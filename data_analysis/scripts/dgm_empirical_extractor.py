"""
DGM V4: Dynamic Cylindrical Section Astrometric Extractor (Gaia DR3)
Targets: Jupiter, Venus, Sun (Applicable observational limitations)
Tactics: Cylindrical Mask Filter and Dynamic Ephemerides.
"""

from astroquery.gaia import Gaia
from astropy.time import Time
from astropy.coordinates import get_body, solar_system_ephemeris, EarthLocation
import numpy as np
import pandas as pd
import warnings
import math
import os

warnings.filterwarnings('ignore')

# Target Configuration and Ideal Epochs (Oppositions/Transits)
TARGETS = {
    'jupiter': {'date': '2016-03-08T00:00:00', 'radius_km': 71492.0},
    'venus': {'date': '2016-10-25T00:00:00', 'radius_km': 6051.8},
    'sun': {'date': '2016-06-01T00:00:00', 'radius_km': 696340.0} 
}

# Primary scan (degrees)
RADIUS_DEG = 200.0 / 3600.0  

def extract_cylindrical_poles(target_name, config):
    print(f"\n==========================================================")
    print(f" DGM V4: POLAR CYLINDRICAL EXTRACTION - {target_name.upper()} (GAIA DR3)")
    print(f"==========================================================")
    
    t = Time(config['date'])
    loc = EarthLocation.of_site('greenwich') # Terrestrial reference point
    
    with solar_system_ephemeris.set('builtin'):
        body = get_body(target_name, t, loc)
        
    ra = body.ra.deg
    dec = body.dec.deg
    dist_au = body.distance.au
    
    # Approximate Angular Radius Calculation in mas (milliarcseconds)
    # 1 AU = 149597870.7 km
    angular_radius_rad = config['radius_km'] / (dist_au * 149597870.7)
    r_target_mas = angular_radius_rad * (180.0 / math.pi) * 3600.0 * 1000.0
    
    print(f"[*] Base Thresholds ({config['date']}): RA={ra:.4f}°, DEC={dec:.4f}°")
    print(f"[*] Calculated Angular Radius: {r_target_mas:.2f} mas")

    adql_query = f"""
    SELECT source_id, ra, dec, phot_g_mean_mag, astrometric_excess_noise, ruwe
    FROM gaiadr3.gaia_source
    WHERE 1=CONTAINS(POINT(ra, dec), CIRCLE({ra}, {dec}, {RADIUS_DEG}))
    AND astrometric_excess_noise IS NOT NULL
    AND ruwe <= 1.4
    AND phot_g_mean_mag <= 21.0
    """
    
    try:
        job = Gaia.launch_job_async(adql_query)
        df = job.get_results().to_pandas()
    except Exception as e:
        print(f"[!] ESA communication error for {target_name}: {e}")
        return

    radial_dist_list = []
    fluid_sector = []
    
    # Virtual Cylinder: 1.5 Target Radii
    MAX_X_CYLINDER = 1.5 * r_target_mas 
    
    for _, row in df.iterrows():
        dra = (row['ra'] - ra) * math.cos(math.radians(dec))
        ddec = row['dec'] - dec
        
        dx_mas = dra * 3600.0 * 1000.0
        dy_mas = ddec * 3600.0 * 1000.0
        
        radial_dist = math.sqrt(dx_mas**2 + dy_mas**2)
        radial_dist_list.append(radial_dist)
        
        if abs(dx_mas) <= MAX_X_CYLINDER and abs(dy_mas) >= r_target_mas:
            fluid_sector.append('Pure_Laminar_Polar')
        elif abs(dy_mas) <= MAX_X_CYLINDER and abs(dx_mas) >= r_target_mas:
            fluid_sector.append('Turbulent_Equatorial')
        else:
            fluid_sector.append('Diagonal_Discard')

    df['radial_distance_mas'] = radial_dist_list
    df['dgm_sector'] = fluid_sector

    df_clean = df[df['dgm_sector'] != 'Diagonal_Discard']
    df_clean = df_clean[(df_clean['radial_distance_mas'] >= r_target_mas) & 
                        (df_clean['radial_distance_mas'] <= 6.0 * r_target_mas)]

    # Save output to the plots directory as requested
    os.makedirs('plots', exist_ok=True)
    output_file = os.path.join('plots', f"{target_name}_dr3_cylindrical.csv")
    df_clean.to_csv(output_file, index=False)
    
    polars = len(df_clean[df_clean['dgm_sector'] == 'Pure_Laminar_Polar'])
    equatorials = len(df_clean[df_clean['dgm_sector'] == 'Turbulent_Equatorial'])
    
    print(f"\n[+] Vault integrity ({target_name}):")
    print(f"    - Polar Cylinder: {polars} stars")
    print(f"    - Equatorial Cylinder: {equatorials} stars")
    print(f"    - Data saved to: {output_file}")

if __name__ == "__main__":
    for target, config in TARGETS.items():
        extract_cylindrical_poles(target, config)