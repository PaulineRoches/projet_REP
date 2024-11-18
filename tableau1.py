import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Charger les données
file_path = "understat_team_stats_home_away.csv"
df = pd.read_csv(file_path)

# Calcul des différences de points (PTS) et de points attendus (xPTS) entre home et away pour chaque ligue et saison
def calculate_diff_points(df):
    grouped_data = df.groupby(['League', 'Season', 'Location']).agg({
        'PTS': 'sum',
        'xPTS': 'sum'
    }).reset_index()

    pivot_pts = grouped_data.pivot(index=['League', 'Season'], columns='Location', values='PTS').fillna(0)
    pivot_xpts = grouped_data.pivot(index=['League', 'Season'], columns='Location', values='xPTS').fillna(0)

    pivot_pts['DIFF_POINTS_HOMEWAY'] = pivot_pts['home'] - pivot_pts['away']
    pivot_xpts['DIFF_XPOINTS_HOMEAWAY'] = pivot_xpts['home'] - pivot_xpts['away']

    diff_df = pd.merge(
        pivot_pts[['DIFF_POINTS_HOMEWAY']],
        pivot_xpts[['DIFF_XPOINTS_HOMEAWAY']],
        left_index=True, right_index=True
    ).reset_index()

    return diff_df

diff_df = calculate_diff_points(df)

# Affichage des résultats
print(diff_df)

# Fonction pour créer des bar charts
def create_barchart_table(diff_df):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Axes du graphique
    leagues_seasons = [f"{row['League']} {int(row['Season'])}" for _, row in diff_df.iterrows()]
    diff_points = diff_df['DIFF_POINTS_HOMEWAY']
    diff_xpoints = diff_df['DIFF_XPOINTS_HOMEAWAY']
    
    bar_width = 0.35
    index = np.arange(len(leagues_seasons))
    
    # Barres pour les différences de points
    bar1 = ax.bar(index, diff_points, bar_width, label='Diff Points (Home - Away)', color='skyblue')
    bar2 = ax.bar(index + bar_width, diff_xpoints, bar_width, label='Diff xPoints (Home - Away)', color='lightcoral')
    
    # Configuration des labels
    ax.set_xlabel('League and Season')
    ax.set_ylabel('Difference')
    ax.set_title('Differences in Points and Expected Points (Home vs Away)')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(leagues_seasons, rotation=45, ha='right')
    ax.legend()
    
    # Affichage des valeurs sur les barres
    for bar in bar1 + bar2:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, f'{yval:.1f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

# Générer le graphique
create_barchart_table(diff_df)
