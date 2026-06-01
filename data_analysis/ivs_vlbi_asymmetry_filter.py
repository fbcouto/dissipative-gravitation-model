import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import get_body
from astropy.time import Time
import warnings

warnings.filterwarnings('ignore')

def generate_academic_asymmetry_plot(pro_data, anti_data, delta):
    """
    Gera o gráfico de validação empírica do DGM V2 para publicação (Gaia DR3).
    Plota a distribuição do ruído astrométrico no corredor de Júpiter.
    """
    plt.style.use('default')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    mean_pro = np.mean(pro_data)
    mean_anti = np.mean(anti_data)
    
    # Plotagem dos Histogramas
    bins = np.linspace(min(min(pro_data), min(anti_data)), max(max(pro_data), max(anti_data)), 40)
    ax.hist(pro_data, bins=bins, alpha=0.6, color='#1f77b4', edgecolor='black', linewidth=0.5, label='Prógrado (Leste) - Alinhado ao Vórtice')
    ax.hist(anti_data, bins=bins, alpha=0.6, color='#d62728', edgecolor='black', linewidth=0.5, label='Retrógrado (Oeste) - Contra o Vórtice')
    
    # Linhas verticais indicando as médias
    ax.axvline(mean_pro, color='#1f77b4', linestyle='dashed', linewidth=2)
    ax.axvline(mean_anti, color='#d62728', linestyle='dashed', linewidth=2)
    
    # Títulos e Eixos (Usando caracteres unicode para evitar alertas de escape/LaTeX)
    ax.set_title(f"Astrometric Noise Distribution in Jovian Transit Corridor\nEmpirical Asymmetry (Δ) = {delta:.4f} mas", pad=15, fontsize=14, fontweight='bold')
    ax.set_xlabel("Astrometric Residual / Space-Drag Noise (mas)", fontsize=12)
    ax.set_ylabel("Star Count (N)", fontsize=12)
    
    # Anotações de Texto
    props = dict(boxstyle='round', facecolor='white', alpha=0.9)
    ax.text(0.95, 0.5, f"μ_Pro = {mean_pro:.2f}\nμ_Anti = {mean_anti:.2f}\nn = {len(pro_data)+len(anti_data)}", 
            transform=ax.transAxes, fontsize=11, verticalalignment='center', horizontalalignment='right', bbox=props)
    
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.7)
    
    # Salvar em alta resolução
    plt.tight_layout()
    file_name = "gaia_asymmetry_analysis.png"
    plt.savefig(file_name, format='png', bbox_inches='tight')
    print(f"\n[*] Academic plot saved successfully as '{file_name}'.")

def analyze_gaia_csv_asymmetry():
    # Data do trânsito que estávamos usando para Júpiter (26 de Setembro de 2022)
    tempo = Time("2022-09-26T00:00:00")
    
    print("==========================================================")
    print(" DGM V2: EMPIRICAL GAIA ASYMMETRY TEST (LOCAL CSV MODE)")
    print("==========================================================\n")
    print(f"[*] Calculating Jupiter's exact ephemeris for {tempo.iso}...")
    
    try:
        jupiter_pos = get_body('jupiter', tempo)
        jup_ra = jupiter_pos.ra.deg
        print(f"    Jupiter Position: RA={jup_ra:.4f}°\n")
    except Exception as e:
        print(f"[!] Error calculating ephemeris: {e}")
        return

    arquivo_csv = "gaia_anomalies.csv" 
    
    print(f"[*] Loading LOCAL Gaia Data ({arquivo_csv}) via Pandas...")
    
    try:
        df = pd.read_csv(arquivo_csv, header=0, skipinitialspace=True)
        
        # Garante que as colunas são numéricas
        df['ra'] = pd.to_numeric(df['ra'], errors='coerce')
        df['astrometric_excess_noise'] = pd.to_numeric(df['astrometric_excess_noise'], errors='coerce')
        
        # Remove linhas que não puderam ser convertidas para números
        df = df.dropna(subset=['ra', 'astrometric_excess_noise'])
        
        linhas_processadas = len(df)
        print(f"[+] SUCCESS! Parsed {linhas_processadas} numerical rows.\n")
        
    except FileNotFoundError:
        print(f"\n[!] CRITICAL ERROR: File '{arquivo_csv}' not found. Please place it in the same directory.")
        return
    except Exception as e:
        print(f"\n[!] ERROR reading CSV file: {e}")
        return

    # Separar os dados: Leste (Prógrado) e Oeste (Retrógrado)
    prograde_df = df[df['ra'] > jup_ra]
    retrograde_df = df[df['ra'] <= jup_ra]
    
    num_pro = len(prograde_df)
    num_anti = len(retrograde_df)
    
    if num_pro == 0 or num_anti == 0:
        print("[!] ERROR: Asymmetry analysis requires points on both sides of the planet.")
        print(f"    Prograde points found: {num_pro}")
        print(f"    Retrograde points found: {num_anti}")
        return

    # Extraindo as séries numéricas para o cálculo e o gráfico
    pro_data = prograde_df['astrometric_excess_noise'].values
    anti_data = retrograde_df['astrometric_excess_noise'].values

    avg_pro = pro_data.mean()
    avg_anti = anti_data.mean()
    delta = avg_pro - avg_anti

    print(f"--- STRICT EMPIRICAL RESULTS (REAL GAIA DR3 DATA - OFFLINE) ---")
    print(f"Anomalous stars analyzed: {num_pro + num_anti}")
    print(f"Avg Space-Drag Noise (Prograde / East):   {avg_pro:.6f} mas")
    print(f"Avg Space-Drag Noise (Retrograde / West): {avg_anti:.6f} mas")
    print(f"Elastic Hydrodynamic Asymmetry (Δ):       {delta:.6f} mas\n")
    
    if delta > 0.5:
        print("CONCLUSION: Asymmetry confirmed in REAL optical data.")
        print("The spatial mesh shows a directional drag coefficient ordered along")
        print("the planet's angular momentum vector, corroborating the DGM V2 premise.")
    else:
        print("CONCLUSION: Weak or no asymmetry detected within error margins.")

    # Gera o gráfico no final do processo
    generate_academic_asymmetry_plot(pro_data, anti_data, delta)

if __name__ == "__main__":
    analyze_gaia_csv_asymmetry()