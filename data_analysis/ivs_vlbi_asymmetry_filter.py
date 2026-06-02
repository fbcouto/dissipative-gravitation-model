"""
DGM V2: Academic Plot Generator
Reads the CSVs from the extractor and outputs publication-ready histograms.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import warnings

warnings.filterwarnings('ignore')

def generate_comparative_plot():
    planets = ['jupiter', 'venus']
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    for ax, planet in zip(axes, planets):
        csv_file = f"{planet}_dr3_anomalies.csv"
        
        if not os.path.exists(csv_file):
            ax.set_title(f"{planet.capitalize()} - Data missing")
            ax.axis('off')
            continue
            
        df = pd.read_csv(csv_file)
        pro_data = df[df['dgm_sector'] == 'Prograde']['astrometric_excess_noise'].values
        anti_data = df[df['dgm_sector'] == 'Retrograde']['astrometric_excess_noise'].values
        
        mean_pro = np.mean(pro_data)
        mean_anti = np.mean(anti_data)
        delta = mean_pro - mean_anti
        
        bins = np.linspace(df['astrometric_excess_noise'].min(), df['astrometric_excess_noise'].max(), 30)
        
        ax.hist(pro_data, bins=bins, alpha=0.6, color='#1f77b4', edgecolor='black', linewidth=0.5, label='Prograde (Aligned to Vortex)')
        ax.hist(anti_data, bins=bins, alpha=0.6, color='#d62728', edgecolor='black', linewidth=0.5, label='Retrograde (Against Vortex)')
        
        ax.axvline(mean_pro, color='#1f77b4', linestyle='dashed', linewidth=2)
        ax.axvline(mean_anti, color='#d62728', linestyle='dashed', linewidth=2)
        
        title_suffix = "(Standard Rotator)" if planet == 'jupiter' else "(Retrograde Rotator)"
        ax.set_title(f"{planet.capitalize()} {title_suffix}\nEmpirical Asymmetry (Δ) = {delta:.4f} mas", pad=15, fontsize=12, fontweight='bold')
        ax.set_xlabel("Astrometric Excess Noise (mas)", fontsize=11)
        ax.set_ylabel("Star Count (N)", fontsize=11)
        
        props = dict(boxstyle='round', facecolor='white', alpha=0.9)
        ax.text(0.95, 0.5, f"μ_Pro = {mean_pro:.2f}\nμ_Retro = {mean_anti:.2f}\nn = {len(df)}", 
                transform=ax.transAxes, fontsize=10, verticalalignment='center', horizontalalignment='right', bbox=props)
        
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, linestyle=':', alpha=0.7)

    plt.suptitle("DGM V2: Spatial Mesh Drag Asymmetry (Gaia DR3)", fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    file_name = "dgm_empirical_validation_plot.png"
    plt.savefig(file_name, format='png', bbox_inches='tight')
    print(f"[*] Academic plot successfully generated: '{file_name}'")

if __name__ == "__main__":
    generate_comparative_plot()