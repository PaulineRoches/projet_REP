from scipy.stats import wilcoxon
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table


def getHomeAwayResultPerMatch(row, home, away, xpts_home, xpts_away, xg_home, xg_away):
    """
    Fonction qui attribue les points pour les matchs à domicile et à l'extérieur.
    Les buts sont extraits des colonnes 'Goals' et 'Goals_Against'.
    Les xPTS et xG sont aussi extraits.
    """
    if row['Home_Away'] == 'h':  # Match à domicile
        if row['Result'] == 'w':  # Victoire à domicile
            home.append(3)
            xpts_home.append(row['xPTS'])
            xg_home.append(row['xG'])
        elif row['Result'] == 'd':  # Match nul
            home.append(1)
            xpts_home.append(row['xPTS'])
            xg_home.append(row['xG'])
        else:  # Défaite à domicile
            home.append(0)
            xpts_home.append(row['xPTS'])
            xg_home.append(row['xG'])
    elif row['Home_Away'] == 'a':  # Match à l'extérieur
        if row['Result'] == 'w':  # Victoire à l'extérieur
            away.append(3)
            xpts_away.append(row['xPTS'])
            xg_away.append(row['xG'])
        elif row['Result'] == 'd':  # Match nul
            away.append(1)
            xpts_away.append(row['xPTS'])
            xg_away.append(row['xG'])
        else:  # Défaite à l'extérieur
            away.append(0)
            xpts_away.append(row['xPTS'])
            xg_away.append(row['xG'])


def cohen_d(home, away):
    """
    Calcul de la taille de l'effet de Cohen (d) entre les résultats à domicile et à l'extérieur.
    """
    mean_a = np.mean(home)
    mean_b = np.mean(away)
    std_a = np.std(home, ddof=1)
    std_b = np.std(away, ddof=1)

    n_a = len(home)
    n_b = len(away)

    s_p = np.sqrt(((n_a - 1) * std_a**2 + (n_b - 1) * std_b**2) / (n_a + n_b - 2))
    cohen_d_value = (mean_a - mean_b) / s_p
    return cohen_d_value


def wilcoxon_test(home, away):
    """
    Effectue le test de Wilcoxon pour comparer les résultats à domicile et à l'extérieur.
    """
    stat, p = wilcoxon(home, away)
    return stat, p


def create_image(df):
    """
    Fonction pour créer et enregistrer une image avec les résultats sous forme de tableau stylisé.
    """
    # Styling function
    def get_cell_color(val, col_name):
        if col_name.startswith('wilco-result-pvalue') and val > 0.05:
            return 'red'
        elif col_name.startswith('result-cohend') and val < 0.2:
            return 'yellow'
        return 'white'

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    table = Table(ax, bbox=[0, 0, 1, 1])
    n_rows, n_cols = df.shape

    # Add headers
    for (i, col_name) in enumerate(df.columns):
        table.add_cell(0, i, width=1 / n_cols, height=0.1, text=col_name, loc='center',
                       facecolor='gray', edgecolor='black')

    # Add data rows
    for row_idx, row in df.iterrows():
        for col_idx, (col_name, value) in enumerate(row.items()):
            color = get_cell_color(value, col_name)
            table.add_cell(row_idx + 1, col_idx, width=1 / n_cols, height=0.1,
                           text=f"{value:.4f}" if isinstance(value, float) else str(value),
                           loc='center', facecolor=color, edgecolor='black')

    ax.add_table(table)
    plt.savefig("styled_results.png", bbox_inches='tight', dpi=300)
    print("Image saved as 'styled_results.png'")


def main():
    # Charger les données depuis un fichier CSV
    understat = pd.read_csv('./understat_match_stats.csv')
    
    final_df = pd.DataFrame(columns=["League", "Season", "wilco-result", "wilco-result-pvalue", "result-cohend",
                                     "wilco-xPTS", "wilco-xPTS-pvalue", "result-cohend-xPTS", 
                                     "wilco-xG", "wilco-xG-pvalue", "result-cohend-xG"])
    leagues = understat['League'].unique()
    seasons = understat['Season'].unique()

    # Parcours des ligues et saisons
    for league in leagues:
        for season in seasons:
            # Filtrer les données pour chaque ligue et saison
            group = understat[(understat['League'] == league) & (understat['Season'] == season)]

            # Initialisation des listes pour les résultats à domicile et à l'extérieur
            home_results = []
            away_results = []
            home_xpts = []
            away_xpts = []
            home_xg = []
            away_xg = []

            # Parcours des résultats de chaque match
            for _, row in group.iterrows():
                getHomeAwayResultPerMatch(row, home_results, away_results, home_xpts, away_xpts, home_xg, away_xg)

            # Effectuer les tests de Wilcoxon et le calcul de Cohen's d pour les différentes mesures
            wilco_pts = wilcoxon_test(home_results, away_results)
            cohend_pts = cohen_d(home_results, away_results)

            wilco_xpts = wilcoxon_test(home_xpts, away_xpts)
            cohend_xpts = cohen_d(home_xpts, away_xpts)

            wilco_xg = wilcoxon_test(home_xg, away_xg)
            cohend_xg = cohen_d(home_xg, away_xg)

            # Ajouter les résultats dans un nouveau DataFrame
            new_row = pd.DataFrame({
                "League": [league],
                "Season": [season],
                "wilco-result": [wilco_pts[0]],
                "wilco-result-pvalue": [wilco_pts[1]],
                "result-cohend": [cohend_pts],
                "wilco-xPTS": [wilco_xpts[0]],
                "wilco-xPTS-pvalue": [wilco_xpts[1]],
                "result-cohend-xPTS": [cohend_xpts],
                "wilco-xG": [wilco_xg[0]],
                "wilco-xG-pvalue": [wilco_xg[1]],
                "result-cohend-xG": [cohend_xg],
            })
            final_df = pd.concat([final_df, new_row], ignore_index=True)

    # Créer et sauvegarder l'image stylisée
    create_image(final_df)

# Exécution du script
main()
