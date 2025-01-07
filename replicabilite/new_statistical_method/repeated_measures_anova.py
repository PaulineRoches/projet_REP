import numpy as np
import pandas as pd
import aiohttp
import asyncio
from understat import Understat
import pingouin as pg
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

def repeated_measures_anova(home, away):
    """
    Perform Repeated Measures ANOVA on the given home and away data.
    """
    data = pd.DataFrame({
        'score': home + away,
        'condition': ['home'] * len(home) + ['away'] * len(away),
        'team': list(range(len(home))) + list(range(len(away)))
    })
    
    # Perform Repeated Measures ANOVA
    anova_results = pg.rm_anova(dv='score', within='condition', subject='team', data=data, detailed=True)
    
    # Print the ANOVA result to check available columns
    print(anova_results)
    
    return anova_results

def create_image(df):
    """
    Create a stylized image of the results table.
    """
    if not os.path.exists("./replicabilite/new_statistical_method/results"):
        os.makedirs("./replicabilite/new_statistical_method/results")

    file_path = os.path.join("./replicabilite/new_statistical_method/results", "reproduction_anova.png")
    
    def get_cell_color(val, col_name):
        if col_name.startswith('anova-pvalue') and val > 0.05:
            return 'red'
        return 'white'

    fig, ax = plt.subplots(figsize=(14, 12))  
    ax.axis('off')  # Hide axes
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
    plt.savefig(file_path, bbox_inches='tight', dpi=300)
    print("Image saved as 'results/reproduction_anova.png'")

async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)

        LEAGUES = ["Ligue_1", "La_liga", "EPL", "Bundesliga", "Serie_A", "RFPL"]
        SEASONS = list(range(2014, 2021))

        final_df = pd.DataFrame(columns=[
            "League", "Season", "anova-F", "anova-pvalue", "anova-eta-sq"
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

                # Perform Repeated Measures ANOVA for points, xPTS, and xG
                anova_results_points = repeated_measures_anova(home_results, away_results)
                
                # Inspect the column names
                print(anova_results_points.columns)  # Check the exact column names
                
                # Adjust the column name based on the output
                new_row = pd.DataFrame({
                    "League": [league],
                    "Season": [season],
                    "anova-F": [anova_results_points.loc[0, 'F']],
                    "anova-pvalue": [anova_results_points.loc[0, 'p-unc']],
                    "anova-eta-sq": [anova_results_points.loc[0, 'ng2']] 
                })
                final_df = pd.concat([final_df, new_row], ignore_index=True)

        # Create and save the stylized table image
        create_image(final_df)

if __name__ == "__main__":
    asyncio.run(main())
