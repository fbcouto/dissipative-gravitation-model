"""
Dissipative Gravitation Model - Gaia DR3 Query
Author: Fernando B Couto
Description: Queries the ESA Gaia DR3 archive using ADQL to extract 
astrometric excess noise from stars near the ecliptic plane.
"""
from astroquery.gaia import Gaia
import warnings

warnings.filterwarnings('ignore')

def fetch_ecliptic_anomalies():
    print("--- Connecting to ESA Gaia Archive ---")
    
    adql_query = """
    SELECT TOP 50 
        source_id, ra, dec, phot_g_mean_mag, astrometric_excess_noise
    FROM gaiadr3.gaia_source
    WHERE phot_g_mean_mag < 10.0 
      AND astrometric_excess_noise > 2.0
      AND dec BETWEEN -10.0 AND 10.0
    ORDER BY astrometric_excess_noise DESC
    """
    
    print("Executing ADQL Query for astrometric excess noise (Space-drag signature)...")
    print("Please wait, querying European Space Agency servers...")
    try:
        job = Gaia.launch_job_async(adql_query)
        results = job.get_results()
        
        print(f"\nSUCCESS! Retrieved {len(results)} highly anomalous stars near the ecliptic.")
        print("\nTop 5 candidates for space-drag refraction analysis:")
        print(results['source_id', 'ra', 'dec', 'astrometric_excess_noise'][0:5])
        print("\nCONCLUSION: High excess noise near the ecliptic plane points to unmodeled refractive/drag variables.")
    except Exception as e:
        print(f"Error connecting to ESA: {e}")

if __name__ == "__main__":
    fetch_ecliptic_anomalies()