import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.cluster import KMeans
from pathlib import Path

from ingest import load_and_clean_data
from processor import run_eda, run_ml_model

def generate_tactical_cluster(df, positions, stats, title, output_path):
    print(f"\n--- Generating 3D Plot: {title} ---")
    subset = df[(df['primary_position'].isin(positions))].copy()
    
    if len(subset) < 3:
        print("Insufficient positional data for clustering.")
        return

    X = subset[[stats[0], stats[1], stats[2]]]
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    subset['cluster'] = kmeans.fit_predict(X)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(subset[stats[0]], subset[stats[1]], subset[stats[2]], 
               c=subset['cluster'], cmap='viridis', s=40, alpha=0.8, edgecolors='k')
    
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(f"Scaled {stats[0].capitalize()}")
    ax.set_ylabel(f"Scaled {stats[1].capitalize()}")
    ax.set_zlabel(f"Scaled {stats[2].capitalize()}")
    
    top_players = subset.sort_values(by='overall', ascending=False).head(3)
    for _, row in top_players.iterrows():
        ax.text(row[stats[0]], row[stats[1]], row[stats[2]], row['short_name'], fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print("Window opened. Close the interactive window to proceed.")
    plt.show()

def draw_tactical_pitch(output_path):
    print("\n--- Assembling the Final 4-1-2-3 Legend XI ---")
    
    # Enforce specified legend lineup names and historical ratings directly
    team = {
        'ST': "Ronaldo\nOVR: 94",
        'LW': "Neymar\nOVR: 91",
        'RW': "Messi\nOVR: 94",
        'AMF': "Iniesta\nOVR: 91",
        'CM': "Xavi\nOVR: 92",
        '專MF': "F. Rijkaard\nOVR: 91", # Labeled as DMF dynamically on coordinates
        'LB': "Maldini\nOVR: 94",
        'CB1': "F. Beckenbauer\nOVR: 93",
        'CB2': "A. Nesta\nOVR: 94",
        'RB': "Lahm\nOVR: 89",
        'GK': "Buffon\nOVR: 92"
    }

    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_facecolor('#2E8B57') 
    fig.patch.set_facecolor('#1a1a1a') 

    # Field Boundary and Line Markings
    plt.plot([0, 0, 100, 100, 0], [0, 100, 100, 0, 0], color="white", linewidth=2) 
    plt.plot([0, 100], [50, 50], color="white", linewidth=2) 
    ax.add_patch(patches.Circle((50, 50), 12, fill=False, color="white", linewidth=2))
    ax.add_patch(patches.Circle((50, 50), 0.5, fill=True, color="white"))
    plt.plot([22, 22, 78, 78], [100, 82, 82, 100], color="white", linewidth=2)
    plt.plot([22, 22, 78, 78], [0, 18, 18, 0], color="white", linewidth=2)
    plt.plot([36, 36, 64, 64], [100, 94, 94, 100], color="white", linewidth=2)
    plt.plot([36, 36, 64, 64], [0, 6, 6, 0], color="white", linewidth=2)

    coords = {
        'ST': (50, 88), 'LW': (20, 80), 'RW': (80, 80),
        'AMF': (35, 65), 'CM': (65, 65), '專MF': (50, 48),
        'LB': (15, 25), 'CB1': (35, 20), 'CB2': (65, 20), 'RB': (85, 25),
        'GK': (50, 5)
    }

    box_style = dict(boxstyle="round,pad=0.5", facecolor="#FFD700", edgecolor="black", linewidth=1.5)
    for pos, (x, y) in coords.items():
        ax.text(x, y, team[pos], ha="center", va="center", fontsize=10, fontweight='bold', color="black", bbox=box_style, zorder=5)

    ax.set_title("Optimal 4-1-2-3 Legend XI", color="white", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.axis('off') 
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    print("Final Legend XI field layout rendered.")
    plt.show()

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    dataset_path = script_dir.parent / "data" / "players.csv"
    output_dir = script_dir.parent
    
    # Pipeline execution sequence
    df_clean = load_and_clean_data(dataset_path)
    run_eda(df_clean, output_dir)
    run_ml_model(df_clean)
    
    # Sequential visualization rendering
    generate_tactical_cluster(df_clean, ['ST', 'RW', 'LW', 'CF'], ['pace', 'shooting', 'dribbling'], 
                              '4-1-2-3 Attackers', output_dir / 'tactical_attackers_3d.png')
                              
    generate_tactical_cluster(df_clean, ['CDM', 'CM', 'CAM'], ['passing', 'dribbling', 'defending'], 
                              '4-1-2-3 Midfield', output_dir / 'tactical_midfielders_3d.png')
                              
    generate_tactical_cluster(df_clean, ['CB', 'RB', 'LB', 'RWB', 'LWB'], ['defending', 'physic', 'pace'], 
                              '4-1-2-3 Defense', output_dir / 'tactical_defenders_3d.png')
                              
    generate_tactical_cluster(df_clean, ['GK'], ['overall', 'defending', 'physic'], 
                              'Goalkeeper Distribution Cluster', output_dir / 'tactical_goalkeepers_3d.png')
                              
    draw_tactical_pitch(output_dir / 'final_optimal_xi.png')