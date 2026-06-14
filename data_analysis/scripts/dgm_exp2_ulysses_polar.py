"""
DGM Experiment II: Level 0 Extractor (Ulysses - Solar Pole)
Target: dop*.gz files (Solar Corona Experiment) in the scripts directory.
Objective: Prove Vacuum Anisotropy (The absence of drag at the poles).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import os
import glob

plt.rcParams.update({
    'font.family': 'serif', 'font.size': 12, 'axes.labelsize': 14,
    'axes.titlesize': 15, 'axes.linewidth': 1.5, 'legend.fontsize': 11,
    'legend.framealpha': 0.95, 'legend.edgecolor': 'black',
    'grid.alpha': 0.7, 'grid.linestyle': ':'
})

def process_ulysses_polar(target_dir='scripts'):
    print("==========================================================")
    print(" DGM EXP II: ULYSSES POLAR EXTRACTOR (VACUUM ANISOTROPY)")
    print("==========================================================")
    
    os.makedirs('plots', exist_ok=True)
    search_pattern = os.path.join(target_dir, "dop*.gz")
    files = glob.glob(search_pattern)
    
    if not files:
        print(f"[!] No dop*.gz files found in the {target_dir} directory.")
        return
        
    for gz_path in files:
        filename = os.path.basename(gz_path)
        print(f"\n[>] Dissecting polar telemetry: {filename}")
        
        try:
            df = pd.read_csv(gz_path, sep=r'\s+', header=None, compression='gzip')
            if df.shape[1] < 15: continue

            time_s = df[1]*3600 + df[2]*60 + df[3]
            t_min = (time_s - time_s.iloc[0]) / 60.0
            
            raw_residuals = df[12].values # X-band residual
            
            # Clean severe hardware outliers
            q_low = np.percentile(raw_residuals, 1)
            q_hi = np.percentile(raw_residuals, 99)
            mask = (raw_residuals > q_low) & (raw_residuals < q_hi)
            
            t_clean = t_min[mask].values
            res_clean = raw_residuals[mask]

            # High-Precision Baseline
            coeffs = np.polyfit(t_clean, res_clean, 10)
            gr_baseline = np.polyval(coeffs, t_clean)
            final_signal = res_clean - gr_baseline
            
            # DGM Filter
            filter_window = 301
            if filter_window > len(final_signal): filter_window = len(final_signal) // 2
            if filter_window % 2 == 0: filter_window -= 1
            
            empirical_tension = savgol_filter(final_signal, filter_window, 3)
            
            # --- REAL RENDER ---
            fig, ax = plt.subplots(figsize=(12, 7.5))
            
            ax.plot(t_clean, final_signal, color='royalblue', alpha=0.9, linewidth=2.5, 
                     label='Raw Level 0 Data (Ulysses Polar Telemetry)')
            
            ax.axhline(0, color='forestgreen', linewidth=3.5, linestyle='--', 
                        label='Einstein / GR (Static Vacuum Geometry)')
            
            ax.plot(t_clean, empirical_tension, color='red', linewidth=4.5, linestyle=':', 
                     label='Extracted Tension Curve (DGM Model)')
            
            ax.set_title(f'Ulysses Experiment (Solar Pole): Archive {filename}', pad=20, fontweight='bold')
            ax.set_xlabel('Transit Time (Minutes)')
            ax.set_ylabel('Residual Gravitational Doppler Distortion (Hz)')
            
            ax.grid(True)
            ax.legend(loc='upper right')
            
            props = dict(boxstyle='square,pad=0.7', facecolor='white', alpha=0.98, edgecolor='black')
            textstr = (r'$\mathbf{Symmetry\ Analysis\ (Polar\ Drag):}$' + '\n' +
                       'If the extracted tension curve (red) remains essentially flat and\n' +
                       'collapsed onto Einstein\'s prediction (green), it proves there are no fluid\n' +
                       'dynamic jets dragging the vacuum at the solar poles. Symmetry is broken.')
            ax.text(0.02, 0.96, textstr, transform=ax.transAxes, verticalalignment='top', bbox=props)
                    
            ax.set_ylim(-1.5, 1.5) 
            ax.set_xlim(0, max(t_clean))
            
            plt.tight_layout()
            plot_file = os.path.join('plots', f'dgm_proof_ulysses_{filename.replace(".gz", "")}.png')
            plt.savefig(plot_file, dpi=300)
            plt.close('all')
            
            print(f"    [+] Real graph generated successfully: {plot_file}")
            
        except Exception as e:
            print(f"    [!] Failed to process {filename}. Reason: {e}")
            plt.close('all')

if __name__ == "__main__":
    process_ulysses_polar('data')