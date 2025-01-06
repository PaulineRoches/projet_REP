import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Chargement des données CSV
df = pd.read_csv("./replicabilite/more_seasons/understat_team_stats_home_away_2023.csv")

# Vérifier que les colonnes nécessaires existent
required_columns = ["League", "Season", "Team", "Location", "PTS", "xPTS"]
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"Le fichier CSV doit contenir les colonnes suivantes : {required_columns}")

# Calculer les sommes par league, year, et home/away
grouped = df.groupby(["League", "Season", "Location"]).agg(
    points_sum=("PTS", "sum"),
    xpoints_sum=("xPTS", "sum")
).reset_index()

# Transformer les données pour calculer les différences home-away
home_data = grouped[grouped["Location"] == "home"].rename(
    columns={"points_sum": "points_home", "xpoints_sum": "xpoints_home"}
)
away_data = grouped[grouped["Location"] == "away"].rename(
    columns={"points_sum": "points_away", "xpoints_sum": "xpoints_away"}
)

# Fusionner les données
merged = pd.merge(
    home_data[["League", "Season", "points_home", "xpoints_home"]],
    away_data[["League", "Season", "points_away", "xpoints_away"]],
    on=["League", "Season"]
)

# Définir l'ordre personnalisé des ligues
leagues_order = ["Ligue_1", "La_liga", "EPL", "Bundesliga", "Serie_A", "RFPL"]
merged["League"] = pd.Categorical(merged["League"], categories=leagues_order, ordered=True)

# Trier les données en fonction de l'ordre des ligues et de la saison
merged = merged.sort_values(by=["League", "Season"]).reset_index(drop=True)

# Calcul des différences
merged["diff_points_homeaway"] = merged["points_home"] - merged["points_away"]
# Calcul des différences arrondies à l'entier le plus proche
merged["diff_xpoints_homeaway"] = (merged["xpoints_home"] - merged["xpoints_away"]).round()


# Fonction pour ajouter des barres colorées avec des étiquettes
def draw_bar(ax, value, max_value, color_positive='lightgreen', color_negative='red'):
    bar_length = (value / max_value) * 0.5  # Longueur relative
    color = color_positive if value > 0 else color_negative
    ax.barh(0, bar_length, color=color)  # Hauteur de la barre ajustée à 0.5 pour correspondre à la ligne
    # Calculer la position du texte pour être à droite de la barre (le long de l'axe x)
    margin = 0.02  # Une petite marge à droite
    ax.text(bar_length - margin, 0, f"{int(value)}", ha='right', va='center', fontsize=14, color='black')
    ax.set_xlim(-0.5, 0.5)
    ax.axis('off')

# Création de la figure avec taille fixe
fig, axs = plt.subplots(len(merged) + 1, 4, figsize=(14, len(merged) * 1.5), gridspec_kw={'width_ratios': [1, 1, 3, 3]})

# Normalisation pour ajuster la longueur des barres
max_value = max(merged["diff_points_homeaway"].abs().max(), merged["diff_xpoints_homeaway"].abs().max())

# Ajout des titres des colonnes
columns = ["League", "Season", "Diff Points (Home-Away)", "Diff XPoints (Home-Away)"]
for j, col in enumerate(columns):
    axs[0, j].text(0.5, 0.5, col, ha='center', va='center', fontsize=14, fontweight='bold')
    axs[0, j].axis('off')

# Ajout des données
for i, row in merged.iterrows():
    # Fond alterné pour les lignes
    if i % 2 == 0:
        for j in range(2):
            axs[i + 1, j].add_patch(patches.Rectangle((-0.5, -0.5), 1.5, 1.5, color="#f0f0f0", zorder=-1))
        for j in range(2, 4):
            # On applique le fond uniquement sans affecter la mise en page de la barre
            axs[i + 1, j].add_patch(patches.Rectangle((-0.5, -0.5), 1.0, 1.0, color="#f0f0f0", zorder=-1))
    
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
plt.subplots_adjust(wspace=0, hspace=0)  # Pas d'espace entre les lignes

# Enregistrement de l'image dans un fichier
output_file = "replicabilite/more_seasons/results/diff_points_xpoints.png"
plt.savefig(output_file, bbox_inches='tight', dpi=300)

# Affichage de l'image
plt.close()

print(f"graph is in directory : {output_file}")
