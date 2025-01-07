import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
from matplotlib.table import Table
import os


def fetch_xpoints_from_csv(df, league, season):
    """Récupère les xPoints pour une ligue et une saison depuis le CSV."""
    group = df[(df['League'] == league) & (df['Season'] == season) & (df['Home_Away'] == 'h')]
    xpoints = group['xPTS'].tolist()
    return xpoints


def calculate_mann_whitney_from_csv(csv_file):
    """Calcule les tests de Mann-Whitney U pour les xPoints entre saisons à partir d'un fichier CSV."""
    df = pd.read_csv(csv_file)
    
    LEAGUES = df['League'].unique()
    SEASONS = sorted(df['Season'].unique())
    results = {}

    for league in LEAGUES:
        league_results = {}
        
        # Récupérer les xPoints pour chaque saison
        xpoints_per_season = {}
        for season in SEASONS:
            xpoints_per_season[season] = fetch_xpoints_from_csv(df, league, season)

        # Comparer les saisons deux à deux sans doublons
        for i, season1 in enumerate(SEASONS):
            league_results[season1] = {}
            for season2 in SEASONS[i + 1:]:  # Comparer chaque saison à toutes celles qui viennent après
                stat, p_value = mannwhitneyu(
                    xpoints_per_season[season1],
                    xpoints_per_season[season2]
                )
                league_results[season1][season2] = p_value / 2  # Ajuster la p-value pour un test one-sided

            # Remplir la diagonale avec NaN (pas de comparaison pour une saison avec elle-même)
            for season2 in SEASONS:
                if season2 == season1:
                    league_results[season1][season2] = np.nan
        
        # Convertir les résultats en DataFrame et trier explicitement les lignes et colonnes
        df_results = pd.DataFrame(league_results)
        df_results = df_results.sort_index(axis=0, ascending=True)  # Trie les lignes par saison croissante
        df_results = df_results.sort_index(axis=1, ascending=True)  # Trie les colonnes par saison croissante
        results[league] = df_results

    return results


def create_stylized_table(results, league):
    """Crée un tableau croisé stylisé avec les p-values pour une ligue donnée."""
    # Créer le dossier pour enregistrer les graphiques
    print("Répertoire courant :", os.getcwd())
    output_dir = "replicabilite/web_scraping/results/tableau_ligues"
    os.makedirs(output_dir, exist_ok=True)

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
                           text=f"{value:.6f}" if pd.notna(value) else "", loc='center',
                           facecolor=color, edgecolor='black')

    ax.add_table(table)
    plt.title(f"xPoints_home significance with mann: {league}")
    file_path = os.path.join(output_dir, f"mann_whitney_{league}.png")
    plt.savefig(file_path, bbox_inches='tight', dpi=300)
    plt.close()


def main():
    csv_file = './replicabilite/web_scraping/understat_match_stats.csv'  # Remplacez par le chemin correct
    results = calculate_mann_whitney_from_csv(csv_file)

    for league in results.keys():
        create_stylized_table(results, league)
        print(f"Tableau pour {league} enregistré.")


if __name__ == "__main__":
    main()
