import requests
import re
import json
import pandas as pd

# Configuration des ligues et des saisons
leagues = ["Ligue_1", "La_liga", "EPL", "Bundesliga", "Serie_A",  "RFPL"]
seasons = [str(year) for year in range(2014, 2021)]  # De 2014 à 2020

# Fonction pour extraire et analyser les données de `teamsData` pour home et away
def extract_team_stats_by_location(league, season):
    url = f"https://understat.com/league/{league}/{season}"
    response = requests.get(url)
    html = response.text
    
    # Regex pour extraire `teamsData`
    match = re.search(r"var teamsData\s*=\s*JSON\.parse\(\'(.*?)\'\);", html)
    if not match:
        print(f"Data not found for {league} {season}")
        return []

    # Décodage des caractères unicode et parsing du JSON
    json_data = bytes(match.group(1), "utf-8").decode("unicode_escape")
    data_teams = json.loads(json_data)

    # Liste pour stocker les résultats
    stats = []

    # Extraction des informations pour chaque équipe
    for team_id, team_data in data_teams.items():
        team_name = team_data['title']
        matches = team_data['history']

        # Séparer les matchs "home" et "away"
        home_matches = [match for match in matches if match['h_a'] == 'h']
        away_matches = [match for match in matches if match['h_a'] == 'a']

        # Fonction pour calculer les statistiques
        def calculate_stats(matches, location):
            M = len(matches)
            W = sum(1 for match in matches if match['result'] == 'w')
            D = sum(1 for match in matches if match['result'] == 'd')
            L = sum(1 for match in matches if match['result'] == 'l')
            G = sum(match.get('scored', 0) for match in matches)
            GA = sum(match.get('missed', 0) for match in matches)
            PTS = sum(match.get('pts', 0) for match in matches)
            xG = sum(match.get('xG', 0) for match in matches)
            xGA = sum(match.get('xGA', 0) for match in matches)
            xPTS = sum(match.get('xpts', 0) for match in matches)

            # Ajouter les données à la liste
            return {
                "League": league,
                "Season": season,
                "Team": team_name,
                "Location": location,
                "M": M,
                "W": W,
                "D": D,
                "L": L,
                "G": G,
                "GA": GA,
                "PTS": PTS,
                "xG": round(xG, 2),
                "xGA": round(xGA, 2),
                "xPTS": round(xPTS, 2)
            }

        # Calcul des statistiques pour "home" et "away"
        home_stats = calculate_stats(home_matches, "home")
        away_stats = calculate_stats(away_matches, "away")

        # Ajouter les résultats aux statistiques globales
        stats.extend([home_stats, away_stats])

    return stats

# Collecte des données pour chaque combinaison de ligue et saison
all_stats = []
for league in leagues:
    for season in seasons:
        print(f"Processing {league} {season}")
        team_stats = extract_team_stats_by_location(league, season)
        all_stats.extend(team_stats)

# Sauvegarde des données dans un fichier CSV
df = pd.DataFrame(all_stats)
df.to_csv("understat_team_stats_home_away.csv", index=False)
print("Data saved to understat_team_stats_home_away.csv")
