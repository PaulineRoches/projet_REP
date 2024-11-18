import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données CSV
df = pd.read_csv("./understat_team_stats_home_away.csv")

# Vérifier que les colonnes nécessaires existent
required_columns = ["League", "Season", "Location", "PTS", "xPTS"]
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"Le fichier CSV doit contenir les colonnes suivantes : {required_columns}")

# Calculer les sommes par league, year, et home/away
grouped = df.groupby(["League", "Season", "Location"]).agg(
    points_sum=("PTS", "sum"),
    xpoints_sum=("xPTS", "sum")
).reset_index()

# Transformer les données pour séparer les stats à domicile et à l'extérieur
home_data = grouped[grouped["Location"] == "home"].rename(
    columns={"points_sum": "points_home", "xpoints_sum": "xpoints_home"}
)
away_data = grouped[grouped["Location"] == "away"].rename(
    columns={"points_sum": "points_away", "xpoints_sum": "xpoints_away"}
)

# Fusionner les données à domicile et à l'extérieur
merged = pd.merge(
    home_data[["League", "Season", "points_home", "xpoints_home"]],
    away_data[["League", "Season", "points_away", "xpoints_away"]],
    on=["League", "Season"]
)

# Créer un graphique pour chaque ligue
leagues = merged["League"].unique()

# Créer et enregistrer les graphiques
for league in leagues:
    league_data = merged[merged["League"] == league]

    plt.figure(figsize=(10, 6))

    # Tracer les courbes
    plt.plot(league_data["Season"], league_data["points_home"], label="Points à domicile", marker='o', linestyle='-', color='green')
    plt.plot(league_data["Season"], league_data["xpoints_home"], label="Points attendus à domicile", marker='o', linestyle='--', color='lightgreen')
    plt.plot(league_data["Season"], league_data["points_away"], label="Points à l'extérieur", marker='o', linestyle='-', color='red')
    plt.plot(league_data["Season"], league_data["xpoints_away"], label="Points attendus à l'extérieur", marker='o', linestyle='--', color='salmon')

    # Personnaliser le graphique
    plt.title(f"Évolution des points pour {league}", fontsize=16)
    plt.xlabel("Saison", fontsize=12)
    plt.ylabel("Points", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.xticks(league_data["Season"], rotation=45)
    
    # Enregistrer le graphique en tant qu'image PNG
    plt.tight_layout()
    plt.savefig(f"evolution_points_{league}.png")  # Enregistre le graphique sous le nom de la ligue
    plt.close()  # Ferme le graphique après l'avoir sauvegardé
