import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.cluster import KMeans
from processor import build_tactical_roster
from pathlib import Path

# --- 1. 3D Clustering Function ---
def generate_tactical_cluster(roster_data, positions, stats, title, output_filename):
    print(f"\n--- Extracting profiles for {positions} ---")
    players = []
    for pos in positions:
        players.extend(roster_data.get(pos, []))
        
    valid_players = [p for p in players if all(k in p for k in (stats[0], stats[1], stats[2], 'overall'))]
    elite_players = [p for p in valid_players if p['overall'] > 75]
    
    if not elite_players:
        print("Not enough elite players for clustering.")
        return

    X = [[p[stats[0]], p[stats[1]], p[stats[2]]] for p in elite_players]
    names = [p['short_name'] for p in elite_players]
    
    print(f"Applying K-Means clustering on {len(elite_players)} elite players...")
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    clusters = kmeans.fit_predict(X)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter([x[0] for x in X], [x[1] for x in X], [x[2] for x in X], 
               c=clusters, cmap='viridis', s=40, alpha=0.8, edgecolors='k')
    
    ax.set_title(title, fontsize=14)
    ax.set_xlabel(stats[0].capitalize())
    ax.set_ylabel(stats[1].capitalize())
    ax.set_zlabel(stats[2].capitalize())
    
    # Label top 5 absolute highest rated players in this line
    elite_sorted = sorted(elite_players, key=lambda x: x['overall'], reverse=True)[:5]
    top_names = [p['short_name'] for p in elite_sorted]
    for i, name in enumerate(names):
        if name in top_names:
            ax.text(X[i][0], X[i][1], X[i][2], name, fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    output_path = Path(__file__).parent.parent / output_filename
    plt.savefig(output_path, dpi=300)
    print(f"SUCCESS: Image saved to {output_path}. Close the window to continue to the next step.")
    plt.show()


# --- 2. Ultimate XI Pitch Function ---
def get_unique_top_players(roster, position, selected_names, count=1):
    """Sorts players and ensures NO DUPLICATES are drafted."""
    if position not in roster: return ["N/A"] * count if count > 1 else "N/A"
    
    sorted_players = sorted(roster[position], key=lambda x: x.get('overall', 0), reverse=True)
    chosen = []
    
    for p in sorted_players:
        if p['short_name'] not in selected_names:
            chosen.append(p)
            selected_names.add(p['short_name']) # Add to blacklist
            if len(chosen) == count:
                break
                
    if count == 1:
        return f"{chosen[0]['short_name']}\nOVR: {chosen[0]['overall']}" if chosen else "N/A"
    else:
        results = [f"{p['short_name']}\nOVR: {p['overall']}" for p in chosen]
        while len(results) < count: results.append("N/A")
        return results

def draw_tactical_pitch(roster_data):
    print("\n--- Assembling the Ultimate 4-1-2-3 Quick Counter XI ---")
    
    # Global tracking set to prevent duplicates across the entire team
    drafted_players = set()
    
    team = {}
    # Attack
    team['ST'] = get_unique_top_players(roster_data, 'ST', drafted_players)
    team['LW'] = get_unique_top_players(roster_data, 'LW', drafted_players)
    team['RW'] = get_unique_top_players(roster_data, 'RW', drafted_players)
    # Midfield
    team['CAM'] = get_unique_top_players(roster_data, 'CAM', drafted_players)
    team['CM'] = get_unique_top_players(roster_data, 'CM', drafted_players)
    team['CDM'] = get_unique_top_players(roster_data, 'CDM', drafted_players)
    # Defense
    cbs = get_unique_top_players(roster_data, 'CB', drafted_players, count=2)
    team['CB1'], team['CB2'] = cbs[0], cbs[1]
    team['LB'] = get_unique_top_players(roster_data, 'LB', drafted_players)
    team['RB'] = get_unique_top_players(roster_data, 'RB', drafted_players)
    team['GK'] = get_unique_top_players(roster_data, 'GK', drafted_players)

    # Pitch Generation
    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_facecolor('#2E8B57') 
    fig.patch.set_facecolor('#1a1a1a') 

    # Field Lines
    plt.plot([0, 0, 100, 100, 0], [0, 100, 100, 0, 0], color="white", linewidth=2) 
    plt.plot([0, 100], [50, 50], color="white", linewidth=2) 
    ax.add_patch(patches.Circle((50, 50), 12, fill=False, color="white", linewidth=2))
    ax.add_patch(patches.Circle((50, 50), 0.5, fill=True, color="white"))
    plt.plot([22, 22, 78, 78], [100, 82, 82, 100], color="white", linewidth=2)
    plt.plot([22, 22, 78, 78], [0, 18, 18, 0], color="white", linewidth=2)
    plt.plot([36, 36, 64, 64], [100, 94, 94, 100], color="white", linewidth=2)
    plt.plot([36, 36, 64, 64], [0, 6, 6, 0], color="white", linewidth=2)

    # 4-1-2-3 Coordinates
    coords = {
        'ST': (50, 88), 'LW': (20, 80), 'RW': (80, 80),
        'CAM': (35, 65), 'CM': (65, 65),
        'CDM': (50, 48),
        'LB': (15, 25), 'CB1': (35, 20), 'CB2': (65, 20), 'RB': (85, 25),
        'GK': (50, 5)
    }

    box_style = dict(boxstyle="round,pad=0.5", facecolor="#FFD700", edgecolor="black", linewidth=1.5)
    
    for pos, (x, y) in coords.items():
        ax.text(x, y, team[pos], ha="center", va="center", fontsize=10, fontweight='bold', color="black", bbox=box_style, zorder=5)

    ax.set_title("Optimal 4-1-2-3 Quick Counter XI", color="white", fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.axis('off') 
    
    output_path = Path(__file__).parent.parent / "final_optimal_xi.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"SUCCESS: Final XI image saved to {output_path}")
    plt.show()

# --- 3. Master Execution Sequence ---
if __name__ == "__main__":
    dataset_path = Path(__file__).parent.parent / "data" / "players.csv"
    print("Loading tactical roster into memory...")
    roster = build_tactical_roster(dataset_path)
    
    # Step 1: Attackers
    generate_tactical_cluster(roster, ['ST', 'RW', 'LW'], ['pace', 'shooting', 'dribbling'], '4-1-2-3 Attackers', 'tactical_attackers.png')
    
    # Step 2: Midfielders
    generate_tactical_cluster(roster, ['CDM', 'CM', 'CAM'], ['passing', 'dribbling', 'defending'], '4-1-2-3 Midfield', 'tactical_midfielders.png')
    
    # Step 3: Defenders
    generate_tactical_cluster(roster, ['CB', 'RB', 'LB'], ['defending', 'physic', 'pace'], '4-1-2-3 Defense', 'tactical_defenders.png')
    
    # Step 4: Final Pitch Diagram
    draw_tactical_pitch(roster)