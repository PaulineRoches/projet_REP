import os
import pandas as pd
import matplotlib.pyplot as plt
import aiohttp
import asyncio
from understat import Understat


async def fetch_understat_data(leagues, seasons):
    """
    Récupère les données des ligues et saisons depuis Understat.
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

                home_points, away_points, home_xpts, away_xpts = [], [], [], []
                for fixture in fixtures:
                    # Récupérer les résultats et les xPTS
                    home_goals, away_goals = int(fixture['goals']['h']), int(fixture['goals']['a'])
                    forecast = fixture['forecast']

                    # Points réels
                    if home_goals > away_goals:
                        home_points.append(3)
                        away_points.append(0)
                    elif home_goals < away_goals:
                        home_points.append(0)
                        away_points.append(3)
                    else:
                        home_points.append(1)
                        away_points.append(1)

                    # xPTS
                    home_xpts.append((float(forecast['w']) * 3) + (float(forecast['d']) * 1))
                    away_xpts.append((float(forecast['l']) * 3) + (float(forecast['d']) * 1))

                data.append({
                    "League": league,
                    "Season": season,
                    "points_home": sum(home_points),
                    "points_away": sum(away_points),
                    "xpoints_home": sum(home_xpts),
                    "xpoints_away": sum(away_xpts),
                    "matchs_home": len(home_points),
                    "matchs_away": len(away_points)
                })

        return pd.DataFrame(data)


def create_graphs(df):
    """
    Crée les graphiques pour chaque ligue en fonction des données.
    """
    # Calcul des moyennes par match
    df["points_home_avg"] = df["points_home"] / df["matchs_home"]
    df["xpoints_home_avg"] = df["xpoints_home"] / df["matchs_home"]
    df["points_away_avg"] = df["points_away"] / df["matchs_away"]
    df["xpoints_away_avg"] = df["xpoints_away"] / df["matchs_away"]

    # Créer le dossier pour enregistrer les graphiques
    output_dir = "results/evolutions_par_ligue"
    os.makedirs(output_dir, exist_ok=True)

    # Tracer les graphiques pour chaque ligue
    for league in df["League"].unique():
        league_data = df[df["League"] == league]

        plt.figure(figsize=(10, 6))
        plt.plot(league_data["Season"], league_data["points_home_avg"], label="Points à domicile", marker='o', color='blue')
        plt.plot(league_data["Season"], league_data["xpoints_home_avg"], label="xPoints à domicile", marker='o', color='orange')
        plt.plot(league_data["Season"], league_data["points_away_avg"], label="Points à l'extérieur", marker='o', color='green')
        plt.plot(league_data["Season"], league_data["xpoints_away_avg"], label="xPoints à l'extérieur", marker='o', color='red')

        plt.title(f"Évolution des points pour {league}", fontsize=16)
        plt.xlabel("Saison", fontsize=12)
        plt.ylabel("Points moyens par match", fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.xticks(league_data["Season"], rotation=45)

        file_path = os.path.join(output_dir, f"evolution_points_{league}.png")
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()

    print(f"Graphiques enregistrés dans le répertoire : {output_dir}.")


async def main():
    leagues = ["Ligue_1", "La_liga", "EPL", "Bundesliga", "Serie_A", "RFPL"]
    seasons = range(2014, 2021)  # Adapter la plage des saisons selon les données disponibles

    # Récupérer les données via Understat
    data = await fetch_understat_data(leagues, seasons)

    # Créer les graphiques
    create_graphs(data)


if __name__ == "__main__":
    asyncio.run(main())
