"""
Gaia DR3 Ecliptic Pipeline Query
Connects to ESA DPAC servers and returns anomalous sources as an Astropy Table/CSV.
"""
from astroquery.gaia import Gaia
import warnings

warnings.filterwarnings('ignore')

def fetch_giant_planets_anomalies(save_to_csv=False, output_filename="gaia_anomalies_sample.csv"):
    """
    Executes ADQL query to find astrometric excess noise in giant planet corridors.
    
    Returns:
        astropy.table.Table: The complete query results.
    """
    adql_query = """
    SELECT TOP 1000 
        source_id, ra, dec, phot_g_mean_mag, astrometric_excess_noise
    FROM gaiadr3.gaia_source
    WHERE phot_g_mean_mag < 12.0 
      AND astrometric_excess_noise > 1.5
      AND dec BETWEEN -5.0 AND 5.0
    ORDER BY astrometric_excess_noise DESC
    """
    
    job = Gaia.launch_job_async(adql_query)
    results = job.get_results()
    
    if save_to_csv:
        results.write(output_filename, format='csv', overwrite=True)
        
    return results

if __name__ == "__main__":
    print("Fetching Gaia DR3 anomalies...")
    data_table = fetch_giant_planets_anomalies(save_to_csv=False)
    print(f"Returned {len(data_table)} rows ready for research.")