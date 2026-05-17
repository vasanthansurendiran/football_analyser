from collections import defaultdict
from ingest import stream_player_data
from pathlib import Path

def build_tactical_roster(filepath):
    """
    Consumes the generator, filters for a 4-1-2-3 formation, 
    and uses advanced collections/comprehensions to structure the data.
    """
    # ADVANCED COLLECTION: defaultdict prevents KeyError and auto-creates lists
    roster = defaultdict(list)
    
    # Target positions for a 4-1-2-3 (GK, CB, LB, RB, CDM, CM, CAM, RW, LW, ST, CF)
    target_positions = {'CB', 'RB', 'LB', 'CDM', 'CM', 'CAM', 'RW', 'LW', 'ST', 'CF', 'GK'}
    
    # Instantiate our memory-efficient generator
    player_stream = stream_player_data(filepath)
    
    # We only want these specific tactical stats for our ML clustering later
    stats_of_interest = ['short_name', 'overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    
    for player in player_stream:
        # EA datasets often comma-separate positions (e.g., "RW, ST, CF"). Grab the primary.
        raw_positions = player.get('player_positions', '').split(',')
        primary_position = raw_positions[0].strip()
        
        if primary_position in target_positions:
            try:
                # COMPREHENSION: Dictionary comprehension to dynamically build the player profile
                # We cast stats to integers for analysis, but leave the name as a string
                cleaned_player = {
                    key: int(player[key]) if key != 'short_name' else player[key]
                    for key in stats_of_interest if player.get(key)
                }
                
                # Add the position and append to our advanced collection
                cleaned_player['position'] = primary_position
                roster[primary_position].append(cleaned_player)
                
            except ValueError:
                # If a stat is blank or broken (e.g., Goalkeepers don't have 'pace'), skip casting
                continue
                
    return roster

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    dataset_path = script_dir.parent / "data" / "players.csv"
    
    print("Executing Tactical Roster Filter...")
    tactical_roster = build_tactical_roster(dataset_path)
    
    # Verify the sorting worked by checking a few key positions for our 4-1-2-3
    for pos in ['ST', 'CDM', 'CB']:
        player_count = len(tactical_roster[pos])
        print(f"\nFound {player_count} players for position: {pos}")
        
        if player_count > 0:
            # Sort to find the highest-rated player at this position
            top_player = sorted(tactical_roster[pos], key=lambda x: x.get('overall', 0), reverse=True)[0]
            print(f"  Top Tactical Option: {top_player['short_name']} (OVR: {top_player['overall']})")