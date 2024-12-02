import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le fichier CSV
df = pd.read_csv('understat_team_stats_home_away.csv')

# Convertir la colonne 'Season' en type catégorique si ce n'est pas déjà le cas
df['Season'] = df['Season'].astype(str)

# Filtrer les saisons de 2014 à 2021 incluses
df = df[df['Season'].between('2014', '2021')]

# Filtrer les données pour ne conserver que les colonnes pertinentes
df = df[['League', 'Season', 'xPTS']]

# Créer un dictionnaire pour stocker les résultats p-value par ligue et saison
results = {}

# Parcourir chaque ligue
for league in df['League'].unique():
    league_data = df[df['League'] == league]
    
    # Créer une liste des saisons uniques pour cette ligue
    seasons = sorted(league_data['Season'].unique())  # Tri des saisons pour avoir 2014-2021 dans l'ordre croissant
    
    # Comparer chaque paire de saisons
    p_values = []
    for i, season1 in enumerate(seasons):
        for season2 in seasons[i:]:  # Comparaison de chaque saison avec toutes les saisons suivantes
            if season1 != season2:  # Ne pas comparer une saison avec elle-même
                # Extraire les données pour les saisons en comparaison
                data1 = league_data[league_data['Season'] == season1]['xPTS']
                data2 = league_data[league_data['Season'] == season2]['xPTS']
                
                # Appliquer le test de Mann-Whitney U
                stat, p_value = mannwhitneyu(data1, data2, alternative='two-sided')
                
                # Ajouter la p-value et les saisons comparées
                p_values.append((season1, season2, p_value))
    
    # Ajouter les résultats dans le dictionnaire pour la ligue
    results[league] = p_values

    # Créer un DataFrame pour les résultats de cette ligue
    p_values_df = pd.DataFrame(p_values, columns=['Season1', 'Season2', 'p_value'])
    
    # Appliquer un format avec une précision de 6 chiffres après la virgule
    p_values_df['p_value'] = p_values_df['p_value'].apply(lambda x: f'{x:.6f}')
    
    # Créer une table pivot pour mieux visualiser les p-values entre saisons
    pivot_table = p_values_df.pivot_table(index='Season1', columns='Season2', values='p_value', aggfunc='first')

    # Convertir les p-values de la table pivot en flottants
    pivot_table = pivot_table.apply(pd.to_numeric, errors='coerce')

    # Plot the heatmap of p-values
    plt.figure(figsize=(10, 8))  # Ajuster la taille de la figure pour plus de clarté
    sns.heatmap(pivot_table, annot=True, fmt='.6f', cmap='coolwarm', cbar=True, linewidths=0.5)
    
    # Ajouter un titre et ajuster les axes pour avoir les saisons sur les deux axes
    plt.title(f'Mann-Whitney U p-values - {league}')
    plt.xticks(rotation=45)  # Pour que les étiquettes des saisons en haut ne se chevauchent pas
    plt.yticks(rotation=0)   # Garder les étiquettes des saisons à gauche bien lisibles

    # Sauvegarder l'image au format PNG
    plt.savefig(f'{league}_mann_whitney_p_values.png', dpi=300)
    plt.close()

print("Les PNG ont été générés pour chaque ligue.")
