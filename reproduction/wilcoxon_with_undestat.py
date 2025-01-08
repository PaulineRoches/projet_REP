import numpy as np
import pandas as pd
from scipy.stats import wilcoxon
from understat import Understat
import aiohttp
import asyncio
import matplotlib.pyplot as plt
from matplotlib.table import Table
import os

def getHomeAwayResultPerMatch(result, home, away, xpts_home, xpts_away, xg_home, xg_away):
    """
    Attribue les points et enregistre les statistiques avancées pour les matchs à domicile et à l'extérieur.
    """
    # Points réels
    if int(result['goals']['h']) > int(result['goals']['a']):
        home.append(3)
        away.append(0)
    elif int(result['goals']['h']) < int(result['goals']['a']):
        home.append(0)
        away.append(3)
    else:
        home.append(1)
        away.append(1)

    # xPTS (calculés à partir de forecast)
    forecast = result['forecast']
    home_xpts, away_xpts = calculate_xpts(forecast)
    xpts_home.append(home_xpts)
    xpts_away.append(away_xpts)

    # xG
    xg_home.append(float(result['xG']['h']))
    xg_away.append(float(result['xG']['a']))

def calculate_xpts(forecast):
    """
    Calcule les xPTS (Expected Points) à partir des probabilités de victoire, nul et défaite.
    """
    home_xpts = (float(forecast['w']) * 3) + (float(forecast['d']) * 1) + (float(forecast['l']) * 0)
    away_xpts = (float(forecast['l']) * 3) + (float(forecast['d']) * 1) + (float(forecast['w']) * 0)
    return home_xpts, away_xpts


def cohen_d(home, away):
    """
    Calcul du score de taille d'effet (Cohen's d) entre deux groupes.
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


def wilcoxon_test(home_points, away_points, home_xpts, away_xpts, home_xg, away_xg):
    # Test de Wilcoxon pour les points
    stat_points, p_points = wilcoxon(home_points, away_points)
    
    # Test de Wilcoxon pour les xPTS
    stat_xpts, p_xpts = wilcoxon(home_xpts, away_xpts)
    
    # Test de Wilcoxon pour les xG
    stat_xg, p_xg = wilcoxon(home_xg, away_xg)
    
    return (stat_points, p_points), (stat_xpts, p_xpts), (stat_xg, p_xg)


def create_image(df):
    """
    Create a stylized image of the results table.
    """
    if not os.path.exists("./reproduction/results"):
        os.makedirs("./reproduction/results")

    file_path = os.path.join("./reproduction/results", "reproduction_wilcoxon.png")
    
    def get_cell_color(val, col_name):
        if col_name.startswith('wilco-pvalue') and val > 0.05:
            return 'red'
        elif col_name.startswith('cohend') and val < 0.2:
            return 'yellow'
        return 'white'

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.axis('off')
    table = Table(ax, bbox=[0, 0, 1, 1])
    n_rows, n_cols = df.shape

    # Add headers
    for (i, col_name) in enumerate(df.columns):
        cell = table.add_cell(0, i, width=1 / n_cols, height=0.1, text=col_name, loc='center',
                       facecolor='gray', edgecolor='black')
        cell.get_text().set_fontsize(20)

    # Add data rows
    for row_idx, row in df.iterrows():
        for col_idx, (col_name, value) in enumerate(row.items()):
            color = get_cell_color(value, col_name)
            cell = table.add_cell(row_idx + 1, col_idx, width=1 / n_cols, height=0.1,
                           text=f"{value:.6f}" if isinstance(value, float) else str(value),
                           loc='center', facecolor=color, edgecolor='black')
            cell.get_text().set_fontsize(20)

    ax.add_table(table)
    plt.savefig(file_path, bbox_inches='tight', dpi=300)
    print("Image saved as 'reproduction/results/reproduction_wilcoxon.png'")


async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)

        LEAGUES = ["Ligue_1", "La_liga", "EPL", "Bundesliga", "Serie_A", "RFPL"]
        SEASONS = list(range(2014, 2021))

        final_df = pd.DataFrame(columns=[
            "League", "Season", "wilco-result", "wilco-pvalue-result", "cohend-result",
            "wilco-xPoints", "wilco-pvalue-xPoints", "cohend-xPoints",
            "wilco-xG", "wilco-pvalue-xG", "cohend-xG"
        ])       

        for league in LEAGUES:
            for season in SEASONS:
                home_results = []
                away_results = []
                home_xpts = []
                away_xpts = []
                home_xg = []
                away_xg = []

                fixtures = await understat.get_league_results(league, season)

                # Remplissage des résultats pour chaque match
                for fixture in fixtures:
                    getHomeAwayResultPerMatch(
                        result=fixture,
                        home=home_results,
                        away=away_results,
                        xpts_home=home_xpts,
                        xpts_away=away_xpts,
                        xg_home=home_xg,
                        xg_away=away_xg
                    )

                # Calcul des tests de Wilcoxon pour points, xPTS et xG
                wilco_test = wilcoxon_test(home_results, away_results, home_xpts, away_xpts, home_xg, away_xg)
                
                # Calcul de Cohen's d pour points, xPTS et xG
                cohend_points = cohen_d(home_results, away_results)
                cohend_xpts = cohen_d(home_xpts, away_xpts)
                cohend_xg = cohen_d(home_xg, away_xg)

                # Création de la nouvelle ligne pour le DataFrame
                new_row = pd.DataFrame({
                    "League": [league],
                    "Season": [season],
                    "wilco-result": [wilco_test[0][0]],  # Statistique pour les points
                    "wilco-pvalue-result": [wilco_test[0][1]],  # P-value pour les points
                    "cohend-result": [cohend_points],  # Cohen's d pour les points
                    "wilco-xPoints": [wilco_test[1][0]],  # Statistique pour les xPTS
                    "wilco-pvalue-xPoints": [wilco_test[1][1]],  # P-value pour les xPTS
                    "cohend-xPoints": [cohend_xpts],  # Cohen's d pour les xPTS
                    "wilco-xG": [wilco_test[2][0]],  # Statistique pour les xG
                    "wilco-pvalue-xG": [wilco_test[2][1]],  # P-value pour les xG
                    "cohend-xG": [cohend_xg]  # Cohen's d pour les xG
                })
                final_df = pd.concat([final_df, new_row], ignore_index=True)


        # Create and save the stylized table image
        create_image(final_df)

if __name__ == "__main__":
    asyncio.run(main())
