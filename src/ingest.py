import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_clean_data(filepath):
    print("--- STEP 1: Data Pre-processing ---")
    df = pd.read_csv(filepath, low_memory=False)
    
    # Select columns critical for our tactical analysis
    cols = ['short_name', 'player_positions', 'overall', 'preferred_foot', 
            'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    
    # Handle Missing Data
    initial_shape = df.shape[0]
    df = df[cols].dropna()
    print(f"Dropped {initial_shape - df.shape[0]} rows containing missing/NaN values.")

    # Data Transformation & Categorical Encoding
    df['primary_position'] = df['player_positions'].apply(lambda x: x.split(',')[0].strip())
    df['preferred_foot_encoded'] = df['preferred_foot'].map({'Right': 1, 'Left': 0})
    
    # Feature Scaling for ML
    scaler = StandardScaler()
    stats_to_scale = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    df[stats_to_scale] = scaler.fit_transform(df[stats_to_scale])
    
    print("Pre-processing complete: Missing data handled, categoricals encoded, features scaled.")
    return df