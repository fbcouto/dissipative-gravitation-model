import pandas as pd
import matplotlib.pyplot as plt

# Academic style
plt.style.use('default')
plt.rcParams.update({'font.family': 'serif', 'axes.titlesize': 14, 'legend.fontsize': 11})

# Load real data
df = pd.read_csv('gaia_anomalies.csv', header=0, skipinitialspace=True)
df['ra'] = pd.to_numeric(df['ra'], errors='coerce')
df['astrometric_excess_noise'] = pd.to_numeric(df['astrometric_excess_noise'], errors='coerce')
df = df.dropna(subset=['ra', 'astrometric_excess_noise'])

# Jupiter's position on the analyzed date
jup_ra = 3.8519

# Separate data
prograde = df[df['ra'] > jup_ra]['astrometric_excess_noise']
retrograde = df[df['ra'] <= jup_ra]['astrometric_excess_noise']

# Visual filter to remove extreme outliers and focus on the main distribution (up to 50 mas)
prograde_filtered = prograde[prograde < 50]
retrograde_filtered = retrograde[retrograde < 50]

fig, ax = plt.subplots(figsize=(10, 6))

# Overlay Histograms
ax.hist(prograde_filtered, bins=50, density=True, alpha=0.6, color='#1f77b4', 
        label=f'Prograde (East) [Mean: {prograde.mean():.3f} mas]')
ax.hist(retrograde_filtered, bins=50, density=True, alpha=0.6, color='#d62728', 
        label=f'Retrograde (West) [Mean: {retrograde.mean():.3f} mas]')

# Vertical Mean Lines
ax.axvline(prograde.mean(), color='#0b5394', linestyle='dashed', linewidth=2)
ax.axvline(retrograde.mean(), color='#8b0000', linestyle='dashed', linewidth=2)

# Annotation Box
delta = prograde.mean() - retrograde.mean()
textstr = f'Sample: {len(df):,} stars\n$\\Delta \\approx {delta:.3f}$ mas\nDGM V2 Signature'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.4)
ax.text(0.70, 0.50, textstr, transform=ax.transAxes, fontsize=12, verticalalignment='top', bbox=props)

# English Labels
ax.set_title('Astrometric Excess Noise Distribution (Gaia DR3) across Jovian Vortex')
ax.set_xlabel('Astrometric Excess Noise (mas)')
ax.set_ylabel('Frequency Density')
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='upper right')

# Output as PNG for GitHub
plt.tight_layout()
plt.savefig('gaia_dr3_vortex_histogram.png', format='png', dpi=300)
print("Real plot generated: gaia_dr3_vortex_histogram.png")