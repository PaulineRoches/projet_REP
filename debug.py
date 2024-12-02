import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Charger les données
df = pd.read_csv('./understat_team_stats_home_away.csv')

# Initialiser la liste des résultats
results = []

# Parcourir chaque combinaison de ligue et saison
for (league, season), group in df.groupby(['League', 'Season']):
    # Séparer home et away
    home = group[group['Location'] == 'home']
    away = group[group['Location'] == 'away']
    # Initialiser les listes pour stocker les valeurs
    home_pts_list = home['PTS'].tolist()
    away_pts_list = away['PTS'].tolist()

    home_xpts_list = home['xPTS'].tolist()
    away_xpts_list = away['xPTS'].tolist()

    home_xg_list = home['xG'].tolist()
    away_xg_list = away['xG'].tolist()

    # Calculer les totaux
    total_pts_home = home['PTS'].sum()
    total_pts_away = away['PTS'].sum()
    total_xpts_home = home['xPTS'].sum()
    total_xpts_away = away['xPTS'].sum()
    total_xg_home = home['xG'].sum()
    total_xg_away = away['xG'].sum()
    total_xga_home = home['xGA'].sum()
    total_xga_away = away['xGA'].sum()

    # Wilcoxon Signed-Rank Test
    print (stats.wilcoxon(home_pts_list, away_pts_list))
    print (stats.wilcoxon(home_xpts_list, away_xpts_list))
    print (stats.wilcoxon(home_xg_list, away_xg_list))



