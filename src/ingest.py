import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_clean_data(filepath):
    print("--- STEP 1: Data Pre-processing ---")
    df = pd.read_csv(filepath, low_memory=False)
    
    # Retain all necessary attributes for both outfield players and goalkeepers
    cols = ['short_name', 'player_positions', 'overall', 'preferred_foot', 
            'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    
    # Filter columns and remove rows missing fundamental data
    df = df[df['overall'].notna() & df['short_name'].notna()]
    df['primary_position'] = df['player_positions'].apply(lambda x: str(x).split(',')[0].strip())
    df['preferred_foot_encoded'] = df['preferred_foot'].map({'Right': 1, 'Left': 0}).fillna(1)
    
    # Fill NaN values for outfield/goalkeeper specific stats with 0 before scaling to prevent errors
    stats_to_scale = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    df[stats_to_scale] = df[stats_to_scale].fillna(0)
    
    scaler = StandardScaler()
    df[stats_to_scale] = scaler.fit_transform(df[stats_to_scale])
    
    print("Pre-processing complete: Positional data preserved, features scaled.")
    return df