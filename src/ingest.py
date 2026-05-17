import csv
from pathlib import Path

def stream_player_data(filepath):
    """
    Generator function to stream player data row by row.
    Demonstrates filesystem operations, exception handling, and generators.
    """
    path = Path(filepath)
    
    if not path.is_file():
        raise FileNotFoundError(f"CRITICAL ERROR: Dataset missing at {path.resolve()}")

    try:
        with open(path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, start=1):
                try:
                    # Using the EXACT headers from your dataset: 'short_name' and 'overall'
                    if not row.get('short_name') or not row.get('overall'):
                        raise ValueError(f"Corrupted data on row {row_num}")
                    
                    yield row
                    
                except ValueError as ve:
                    print(f"WARNING: Skipping row {row_num} - {ve}")
                    continue 

    except Exception as e:
        raise RuntimeError(f"System failure while reading dataset: {e}")

if __name__ == "__main__":
    # Bulletproof dynamic path resolution. 
    # This ensures it finds the data folder no matter where you run the script from.
    script_dir = Path(__file__).parent
    dataset_path = script_dir.parent / "data" / "players.csv"
    
    print(f"Initializing Data Stream from {dataset_path}...")
    try:
        player_stream = stream_player_data(dataset_path)
        
        for i in range(5):
            player = next(player_stream)
            print(f"Loaded: {player.get('short_name')} - Rating: {player.get('overall')}")
            
    except StopIteration:
        print("End of dataset reached.")
    except Exception as error:
        print(error)