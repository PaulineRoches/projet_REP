import pandas as pd
import numpy as np
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
from pandas.plotting import table

# Charger les données
df = pd.read_csv('./understat_team_stats_home_away.csv')

# Filtrer les données pour les matchs à domicile
df_home = df[df['Location'] == 'home']

# Initialiser une liste pour stocker les résultats
results = []

# Obtenir toutes les ligues et saisons uniques
leagues = df_home['League'].unique()
seasons = df_home['Season'].unique()

# Effectuer un test de Mann-Whitney pour chaque paire de saisons, par ligue
for league in leagues:
    # Filtrer les données pour chaque ligue
    df_league = df_home[df_home['League'] == league]

    # Comparer chaque paire de saisons
    for i in range(len(seasons) - 1):
        for j in range(i + 1, len(seasons)):
            season1 = seasons[i]
            season2 = seasons[j]
            
            # Extraire les données pour chaque saison
            data_season1 = df_league[df_league['Season'] == season1]['xPTS'].tolist()
            data_season2 = df_league[df_league['Season'] == season2]['xPTS'].tolist()

            print(season1)
            print(season2)
            print(league)
            print (data_season1)
            print (data_season2)
            
            # Vérifier si les deux séries ont suffisamment de données pour effectuer le test
            if len(data_season1) > 1 and len(data_season2) > 1:  # S'assurer qu'il y a plus d'une valeur dans chaque série
                # Effectuer le test de Mann-Whitney
                stat, p_value = mannwhitneyu(x=data_season1, y=data_season2, alternative = 'one-sided')
                
                # Ajouter le résultat à la liste
                results.append({
                    'League': league,
                    'Season1': season1,
                    'Season2': season2,
                    'P-value': p_value
                })
            else:
                # Si pas assez de données, ajouter NaN comme p-value
                results.append({
                    'League': league,
                    'Season1': season1,
                    'Season2': season2,
                    'P-value': np.nan
                })

# Convertir les résultats en DataFrame
results_df = pd.DataFrame(results)

# Créer un tableau croisé par ligue
pivot_tables = {}
for league in leagues:
    # Filtrer les résultats par ligue
    league_results = results_df[results_df['League'] == league]
    
    # Créer un tableau croisé, inversé (Saisons en colonnes)
    pivot = league_results.pivot(index='Season2', columns='Season1', values='P-value')
    
    # Remplir les valeurs manquantes par NaN
    pivot = pivot.fillna(np.nan)
    
    # Ajouter la table croisée au dictionnaire
    pivot_tables[league] = pivot

# Fonction pour styliser les tableaux avec des couleurs rouges
def apply_colored_styles(ax, df):
    """Ajoute des styles conditionnels avec coloration rouge pour les p-values < 0.05"""
    rows, cols = df.shape
    cell_text = []
    cell_colors = []

    for row in range(rows):
        row_text = []
        row_colors = []
        for col in range(cols):
            value = df.iloc[row, col]
            # Style conditionnel
            if pd.notnull(value) and value < 0.05:
                row_colors.append("red")  # Rouge pour les p-values significatives
            else:
                row_colors.append("white")  # Blanc sinon
            row_text.append(f"{value:.4f}" if pd.notnull(value) else "NaN")
        cell_text.append(row_text)
        cell_colors.append(row_colors)

    # Ajout des couleurs dans la table
    table(
        ax, 
        df, 
        loc='center', 
        cellLoc='center', 
        colWidths=[0.1] * cols,
        cellColours=cell_colors
    )

# Afficher et sauvegarder les tableaux croisés
for league, pivot in pivot_tables.items():
    print(f"Tableau croisé pour la ligue : {league}")
    
    # Créer une figure pour matplotlib
    fig, ax = plt.subplots(figsize=(8, 6))  # Ajuste la taille du graphique
    ax.axis('off')  # Cacher les axes

    # Appliquer les styles colorés
    apply_colored_styles(ax, pivot)

    # Sauvegarder le tableau sous forme d'image PNG
    plt.savefig(f"tableau_{league}.png", format='png', bbox_inches='tight', dpi=300)  # Sauvegarder en haute résolution
    plt.show()  # Afficher la table dans la fenêtre
