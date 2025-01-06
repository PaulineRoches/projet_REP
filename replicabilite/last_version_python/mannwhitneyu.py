import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
from understat import Understat
import aiohttp
import asyncio
import matplotlib.pyplot as plt
from matplotlib.table import Table
import os

async def fetch_xpoints(understat, league, season):
    """Récupère les xPoints pour une ligue et une saison."""
    fixtures = await understat.get_league_results(league, season)
    home_xpts = []
    
    for fixture in fixtures:
        forecast = fixture['forecast']
        home_xpt = (float(forecast['w']) * 3) + (float(forecast['d']) * 1)
        home_xpts.append(home_xpt)

    return home_xpts

async def calculate_mann_whitney():
    """Calcule les tests de Mann-Whitney U pour les xPoints entre saisons."""
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)

        LEAGUES = ["Ligue_1", "La_liga", "EPL", "Bundesliga", "Serie_A", "RFPL"]
        SEASONS = list(range(2014, 2021))

        results = {}

        for league in LEAGUES:
            league_results = {}
            
            # Récupérer les xPoints pour chaque saison
            xpoints_per_season = {}
            for season in SEASONS:
                xpoints_per_season[season] = await fetch_xpoints(understat, league, season)

            # Comparer les saisons deux à deux sans doublons
            for i, season1 in enumerate(SEASONS):
                league_results[season1] = {}
                for season2 in SEASONS[i+1:]:  # Comparer chaque saison à toutes celles qui viennent après
                    stat, p_value = mannwhitneyu(
                        xpoints_per_season[season1], 
                        xpoints_per_season[season2]
                    )
                    league_results[season1][season2] = p_value  # Ajuster la p-value pour un test one-sided
                # Remplir la diagonale avec NaN (pas de comparaison pour une saison avec elle-même)
                for season2 in SEASONS:
                    if season2 == season1:
                        league_results[season1][season2] = np.nan
            
            # Convertir les résultats en DataFrame et trier explicitement les lignes et colonnes
            df = pd.DataFrame(league_results)
            
            # S'assurer que les saisons sont dans l'ordre correct (2014 à 2020)
            df = df.sort_index(axis=0, ascending=True)  # Trie les lignes par saison croissante
            df = df.sort_index(axis=1, ascending=True)  # Trie les colonnes par saison croissante

            results[league] = df

        return results

def create_stylized_table(results, league):
    # Créer le dossier pour enregistrer les graphiques
    print("Répertoire courant :", os.getcwd())
    output_dir = "replicabilite/last_version_python/results/tableau_ligues"
    os.makedirs(output_dir, exist_ok=True)

    """Crée un tableau croisé stylisé avec les p-values pour une ligue donnée."""
    df = results[league]

    def get_cell_color(val):
        if val < 0.05:
            return 'red'
        return 'white'

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    table = Table(ax, bbox=[0, 0, 1, 1])
    n_rows, n_cols = df.shape

    # Add headers
    for (i, col_name) in enumerate(df.columns):
        table.add_cell(0, i + 1, width=1 / (n_cols + 1), height=0.1, text=col_name, loc='center',
                       facecolor='gray', edgecolor='black')
    for (i, row_name) in enumerate(df.index):
        table.add_cell(i + 1, 0, width=1 / (n_cols + 1), height=0.1, text=row_name, loc='center',
                       facecolor='gray', edgecolor='black')

    # Add data rows
    for row_idx, row in enumerate(df.iterrows()):
        for col_idx, (col_name, value) in enumerate(row[1].items()):
            color = get_cell_color(value)
            table.add_cell(row_idx + 1, col_idx + 1, width=1 / (n_cols + 1), height=0.1,
                           text=f"{value:.4f}" if pd.notna(value) else "", loc='center',
                           facecolor=color, edgecolor='black')

    ax.add_table(table)
    plt.title(f"xPoints_home significance with mann: {league}")
    file_path = os.path.join(output_dir, f"mann_whitney_{league}.png")
    plt.savefig(file_path, bbox_inches='tight', dpi=300)
    plt.close()

async def main():
    results = await calculate_mann_whitney()

    for league in results.keys():
        create_stylized_table(results, league)
        print(f"Tableau pour {league} enregistré.")

if __name__ == "__main__":
    asyncio.run(main())
