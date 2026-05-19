import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

def run_eda(df, output_dir):
    print("\n--- STEP 2: Exploratory Data Analysis (EDA) ---")
    sns.set_theme(style="whitegrid")
    
    # 1. Histogram
    print("Opening EDA 1: Histogram. Close the window to continue.")
    plt.figure(figsize=(8, 5))
    sns.histplot(df['overall'], bins=30, kde=True, color='blue')
    plt.title('Distribution of Player Overall Ratings')
    plt.savefig(output_dir / 'eda_histogram.png', dpi=300)
    plt.show()

    # 2. Box Plot
    print("Opening EDA 2: Box Plot. Close the window to continue.")
    attackers = ['ST', 'RW', 'LW', 'CF']
    defenders = ['CB', 'RB', 'LB', 'RWB', 'LWB']
    df['Role'] = np.where(df['primary_position'].isin(attackers), 'Attacker',
                 np.where(df['primary_position'].isin(defenders), 'Defender', 'Midfielder'))
    
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Role', y='pace', data=df, palette='Set2')
    plt.title('Pace Distribution by Tactical Role (Scaled)')
    plt.savefig(output_dir / 'eda_boxplot.png', dpi=300)
    plt.show()

    # 3. Heatmap
    print("Opening EDA 3: Correlation Heatmap. Close the window to continue.")
    plt.figure(figsize=(10, 8))
    corr_cols = ['overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']
    sns.heatmap(df[corr_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Feature Correlation Heatmap')
    plt.savefig(output_dir / 'eda_heatmap.png', dpi=300)
    plt.show()

def run_ml_model(df):
    print("\n--- STEP 3: ML Regression (Predicting Overall Rating) ---")
    # Exclude goalkeepers from core outfield regression model to preserve accuracy metrics
    outfield_df = df[df['primary_position'] != 'GK']
    
    features = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'preferred_foot_encoded']
    X = outfield_df[features]
    y = outfield_df['overall']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print(f"- Root Mean Square Error (RMSE): {rmse:.4f}")