import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.table import Table

# Charger les données
df = pd.read_csv('./understat_team_stats_home_away.csv')

# Initialiser la liste des résultats
results = []

# Parcourir chaque combinaison de ligue et saison
for (league, season), group in df.groupby(['League', 'Season']):
    # Séparer home et away
    home = group[group['Location'] == 'home']
    away = group[group['Location'] == 'away']

    home_pts_list = home['PTS'].tolist()
    away_pts_list = away['PTS'].tolist()
    home_xpts_list = home['xPTS'].tolist()
    away_xpts_list = away['xPTS'].tolist()
    home_xg_list = home['xG'].tolist()
    away_xg_list = away['xG'].tolist()

    total_pts_home = home['PTS'].sum()
    total_pts_away = away['PTS'].sum()
    total_xpts_home = home['xPTS'].sum()
    total_xpts_away = away['xPTS'].sum()
    total_xg_home = home['xG'].sum()
    total_xg_away = away['xG'].sum()
    total_xga_home = home['xGA'].sum()
    total_xga_away = away['xGA'].sum()

    wilco_pts, p_pts = stats.wilcoxon(home_pts_list, away_pts_list)
    wilco_xpts, p_xpts = stats.wilcoxon(home_xpts_list, away_xpts_list)
    wilco_xg, p_xg = stats.wilcoxon(home_xg_list, away_xg_list)

    def cohen_d(series1, series2):
        arr1 = np.array(series1)
        arr2 = np.array(series2)
        diff = arr1.mean() - arr2.mean()
        pooled_std = np.sqrt(((arr1.std() ** 2 + arr2.std() ** 2) / 2))
        return diff / pooled_std if pooled_std != 0 else 0


    cohen_pts = cohen_d(home_pts_list, away_pts_list)
    cohen_xpts = cohen_d(home_xpts_list, away_xpts_list)
    cohen_xg = cohen_d(home_xg_list, away_xg_list)

    results.append({
        'League': league,
        'Season': season,
        'Wilcoxon_PTS': wilco_pts,
        'p_value_PTS': p_pts,
        'Cohen_d_PTS': cohen_pts,
        'Wilcoxon_xPTS': wilco_xpts,
        'p_value_xPTS': p_xpts,
        'Cohen_d_xPTS': cohen_xpts,
        'Wilcoxon_xG': wilco_xg,
        'p_value_xG': p_xg,
        'Cohen_d_xG': cohen_xg,
    })

# Convertir les résultats en DataFrame
result_df = pd.DataFrame(results)

# Définir les styles conditionnels
def get_cell_color(val, col_name):
    if col_name.startswith('p_value') and val > 0.05:
        return 'red'
    elif col_name.startswith('Cohen_d') and val < 0.2:
        return 'yellow'
    return 'white'

# Créer une image avec les styles conditionnels appliqués
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis('off')

# Ajouter un tableau avec les styles
table = Table(ax, bbox=[0, 0, 1, 1])
n_rows, n_cols = result_df.shape

# Ajouter les cellules avec des styles
for (i, col_name) in enumerate(result_df.columns):
    table.add_cell(0, i, width=1/n_cols, height=0.1, text=col_name, loc='center', facecolor='gray', edgecolor='black')

for row_idx, row in result_df.iterrows():
    for col_idx, (col_name, value) in enumerate(row.items()):
        color = get_cell_color(value, col_name)
        table.add_cell(row_idx + 1, col_idx, width=1/n_cols, height=0.1,
                       text=f"{value:.10f}" if isinstance(value, float) else str(value),
                       loc='center', facecolor=color, edgecolor='black')

# Ajouter le tableau à l'axe
ax.add_table(table)

# Sauvegarder l'image
plt.savefig("resultats_stylises.png", bbox_inches='tight', dpi=300)
print("Les résultats stylisés ont été sauvegardés dans 'resultats_stylises.png'.")
