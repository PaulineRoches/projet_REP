package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strconv"
)

// Wilcoxon Signed-Rank Test Placeholder (implémentation théorique nécessaire)
func wilcoxonTest(home []float64, away []float64) (float64, error) {
	// Vous pouvez utiliser une bibliothèque de test ou implémenter votre propre fonction
	// pour calculer le test de Wilcoxon. Ici, nous retournons simplement une valeur factice.
	return 0.05, nil // Exemple de p-value factice
}

func main() {
	// Charger les données depuis un fichier CSV
	file, err := os.Open("./understat_team_stats_home_away.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Lire les données CSV
	reader := csv.NewReader(file)
	// Ignore la première ligne d'en-tête
	_, err = reader.Read()

	// Initialiser les résultats
	results := make([]map[string]interface{}, 0)

	// Lire chaque ligne du fichier
	data := make(map[string]map[string]map[string][]float64) // Format: League -> Season -> Location -> Data
	for {
		record, err := reader.Read()
		if err != nil {
			break
		}

		// Extraire les données
		league := record[0]
		season := record[1]
		location := record[2]
		pts, _ := strconv.ParseFloat(record[3], 64)
		xpts, _ := strconv.ParseFloat(record[4], 64)
		xg, _ := strconv.ParseFloat(record[5], 64)

		// Initialiser les cartes pour chaque Ligue et Saison si nécessaire
		if _, ok := data[league]; !ok {
			data[league] = make(map[string]map[string][]float64)
		}
		if _, ok := data[league][season]; !ok {
			data[league][season] = make(map[string][]float64)
		}

		// Ajouter les données en fonction de la localisation
		if location == "home" {
			data[league][season]["home_pts"] = append(data[league][season]["home_pts"], pts)
			data[league][season]["home_xpts"] = append(data[league][season]["home_xpts"], xpts)
			data[league][season]["home_xg"] = append(data[league][season]["home_xg"], xg)
		} else if location == "away" {
			data[league][season]["away_pts"] = append(data[league][season]["away_pts"], pts)
			data[league][season]["away_xpts"] = append(data[league][season]["away_xpts"], xpts)
			data[league][season]["away_xg"] = append(data[league][season]["away_xg"], xg)
		}
	}

	// Parcourir chaque combinaison de ligue et saison
	for league, seasons := range data {
		for season, locations := range seasons {
			// Récupérer les points (PTS), les points attendus (xPTS) et les buts attendus (xG)
			homePts := locations["home_pts"]
			awayPts := locations["away_pts"]

			homeXpts := locations["home_xpts"]
			awayXpts := locations["away_xpts"]

			homeXg := locations["home_xg"]
			awayXg := locations["away_xg"]

			// Appliquer le test de Wilcoxon pour chaque mesure
			pValuePts, err := wilcoxonTest(homePts, awayPts)
			if err != nil {
				log.Printf("Erreur lors du test Wilcoxon pour %s %s: %v\n", league, season, err)
			}

			pValueXpts, err := wilcoxonTest(homeXpts, awayXpts)
			if err != nil {
				log.Printf("Erreur lors du test Wilcoxon pour %s %s: %v\n", league, season, err)
			}

			pValueXg, err := wilcoxonTest(homeXg, awayXg)
			if err != nil {
				log.Printf("Erreur lors du test Wilcoxon pour %s %s: %v\n", league, season, err)
			}

			// Ajouter les résultats à la liste
			results = append(results, map[string]interface{}{
				"League":       league,
				"Season":       season,
				"Wilcoxon_PTS": pValuePts,
				"Wilcoxon_xPTS": pValueXpts,
				"Wilcoxon_xG":  pValueXg,
			})
		}
	}

	// Afficher les résultats
	for _, result := range results {
		fmt.Printf("League: %s, Season: %s\n", result["League"], result["Season"])
		fmt.Printf("Wilcoxon PTS: %.4f, Wilcoxon xPTS: %.4f, Wilcoxon xG: %.4f\n", result["Wilcoxon_PTS"], result["Wilcoxon_xPTS"], result["Wilcoxon_xG"])
		fmt.Println("--------------------------------------------------")
	}
}
