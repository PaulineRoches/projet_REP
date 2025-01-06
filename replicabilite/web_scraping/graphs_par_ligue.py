import os
import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données CSV
df = pd.read_csv("./understat_team_stats_home_away.csv")

# Vérifier que les colonnes nécessaires existent
required_columns = ["League", "Season", "Location", "PTS", "xPTS", "M"]
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"Le fichier CSV doit contenir les colonnes suivantes : {required_columns}")

# Créer le dossier pour enregistrer les graphiques
output_dir = "results/evolutions_par_ligue"
os.makedirs(output_dir, exist_ok=True)

# Calculer les moyennes par league, season, et home/away
grouped = df.groupby(["League", "Season", "Location"]).agg(
    points_avg=("PTS", "sum"),
    xpoints_avg=("xPTS", "sum"),
    matchs_count=("M", "sum")
).reset_index()

# Calcul des points moyens par match
grouped["points_avg_per_game"] = grouped["points_avg"] / grouped["matchs_count"]
grouped["xpoints_avg_per_game"] = grouped["xpoints_avg"] / grouped["matchs_count"]

# Séparer les données à domicile et à l'extérieur
home_data = grouped[grouped["Location"] == "home"].rename(
    columns={"points_avg_per_game": "points_home", "xpoints_avg_per_game": "xpoints_home"}
)
away_data = grouped[grouped["Location"] == "away"].rename(
    columns={"points_avg_per_game": "points_away", "xpoints_avg_per_game": "xpoints_away"}
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

    # Créer une nouvelle figure
    plt.figure(figsize=(10, 6))

    # Tracer les courbes avec les couleurs demandées
    plt.plot(league_data["Season"], league_data["points_home"], label="Points à domicile", marker='o', linestyle='-', color='blue')
    plt.plot(league_data["Season"], league_data["xpoints_home"], label="Points attendus à domicile", marker='o', linestyle='-', color='orange')
    plt.plot(league_data["Season"], league_data["points_away"], label="Points à l'extérieur", marker='o', linestyle='-', color='green')
    plt.plot(league_data["Season"], league_data["xpoints_away"], label="Points attendus à l'extérieur", marker='o', linestyle='-', color='red')

    # Personnaliser le graphique
    plt.title(f"Points evolution for {league}", fontsize=16)
    plt.xlabel("Season", fontsize=12)
    plt.ylabel("Mean gained points per match", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.xticks(league_data["Season"], rotation=45)
    
    # Enregistrer le graphique en tant qu'image PNG dans le dossier
    file_path = os.path.join(output_dir, f"evolution_points_{league}.png")
    plt.tight_layout()
    plt.savefig(file_path)  # Enregistrer le graphique
    plt.close()  # Fermer la figure après l'avoir sauvegardée

print(f"graphs are in the repertory : '{output_dir}'.")
