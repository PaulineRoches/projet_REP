import numpy as np
import pandas as pd
from understat import Understat
import aiohttp
import asyncio
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def getHomeAwayResultPerMatch(result, home, away, xpts_home, xpts_away):
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


def calculate_xpts(forecast):
    """
    Calcule les xPTS (Expected Points) à partir des probabilités de victoire, nul et défaite.
    """
    home_xpts = (float(forecast['w']) * 3) + (float(forecast['d']) * 1) + (float(forecast['l']) * 0)
    away_xpts = (float(forecast['l']) * 3) + (float(forecast['d']) * 1) + (float(forecast['w']) * 0)
    return home_xpts, away_xpts


async def fetch_understat_data(leagues, seasons):
    """
    Récupère les données depuis l'API Understat pour plusieurs ligues et saisons.
    """
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = []

        for league in leagues:
            for season in seasons:
                print(f"Fetching data for {league} {season}...")
                try:
                    fixtures = await understat.get_league_results(league, season)
                except Exception as e:
                    print(f"Erreur lors de la récupération des données pour {league} {season}: {e}")
                    continue

                home, away, xpts_home, xpts_away = [], [], [], []
                for fixture in fixtures:
                    # Calculer les résultats Home et Away
                    getHomeAwayResultPerMatch(fixture, home, away, xpts_home, xpts_away)

                data.append({
                    "League": league,
                    "Season": season,
                    "points_home": sum(home),
                    "points_away": sum(away),
                    "xpoints_home": sum(xpts_home),
                    "xpoints_away": sum(xpts_away),
                })

        return pd.DataFrame(data)


def create_graph(data):
    """
    Crée un graphique pour visualiser les différences Home-Away pour les points et xPTS.
    """
    # Calcul des différences
    data["diff_points_homeaway"] = data["points_home"] - data["points_away"]
    data["diff_xpoints_homeaway"] = (data["xpoints_home"] - data["xpoints_away"]).round()

    # Définir l'ordre personnalisé des ligues
    leagues_order = ["Ligue_1", "La_liga", "EPL", "Bundesliga", "Serie_A", "RFPL"]
    data["League"] = pd.Categorical(data["League"], categories=leagues_order, ordered=True)

    # Trier les données en fonction de l'ordre des ligues et de la saison
    data = data.sort_values(by=["League", "Season"]).reset_index(drop=True)

    # Création du graphique
    fig, axs = plt.subplots(len(data) + 1, 4, figsize=(14, len(data) * 1.5), gridspec_kw={'width_ratios': [1, 1, 3, 3]})

    # Normalisation pour ajuster la longueur des barres
    max_value = max(data["diff_points_homeaway"].abs().max(), data["diff_xpoints_homeaway"].abs().max())

    # Titres des colonnes
    columns = ["League", "Season", "Diff Points (Home-Away)", "Diff XPoints (Home-Away)"]
    for j, col in enumerate(columns):
        axs[0, j].text(0.5, 0.5, col, ha='center', va='center', fontsize=14, fontweight='bold')
        axs[0, j].axis('off')

    # Ajout des données
    for i, row in data.iterrows():
        # Fond alterné pour les lignes
        if i % 2 == 0:
            for j in range(4):
                axs[i + 1, j].add_patch(patches.Rectangle((-0.5, -0.5), 1.5, 1.5, color="#f0f0f0", zorder=-1))

        # Colonne League
        axs[i + 1, 0].text(0.5, 0.5, row["League"], ha='center', va='center', fontsize=12)
        axs[i + 1, 0].axis('off')

        # Colonne Season
        axs[i + 1, 1].text(0.5, 0.5, str(row["Season"]), ha='center', va='center', fontsize=12)
        axs[i + 1, 1].axis('off')

        # Colonne diff_points_homeaway
        draw_bar(axs[i + 1, 2], row["diff_points_homeaway"], max_value)

        # Colonne diff_xpoints_homeaway
        draw_bar(axs[i + 1, 3], row["diff_xpoints_homeaway"], max_value)

    # Suppression des espaces entre colonnes et lignes
    plt.subplots_adjust(wspace=0, hspace=0)

    # Sauvegarde du graphique
    output_file = "reproduction/results/diff_points_xpoints_2.png"
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.close()

    print(f"Graphique généré : {output_file}")


def draw_bar(ax, value, max_value, color_positive='lightgreen', color_negative='red'):
    bar_length = (value / max_value) * 0.5  # Longueur relative
    color = color_positive if value > 0 else color_negative
    ax.barh(0, bar_length, color=color)
    margin = 0.02
    ax.text(bar_length - margin, 0, f"{int(value)}", ha='right', va='center', fontsize=14, color='black')
    ax.set_xlim(-0.5, 0.5)
    ax.axis('off')


async def main():
    leagues = ["Ligue_1", "La_liga", "EPL", "Bundesliga", "Serie_A", "RFPL"]
    seasons = range(2014, 2021)

    data = await fetch_understat_data(leagues, seasons)
    create_graph(data)


if __name__ == "__main__":
    asyncio.run(main())
