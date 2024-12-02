# Charger les bibliothèques nécessaires
library(tidyr)
library(dplyr)

# Charger les données
df <- read.csv("./understat_team_stats_home_away.csv")

# Filtrer les données pour les matchs à domicile
df_home <- df %>% filter(Location == "home")

# Liste des ligues et saisons uniques
leagues <- unique(df_home$League)
seasons <- unique(df_home$Season)

# Initialiser un data frame pour les résultats
results <- data.frame(
  League = character(),
  Season1 = integer(),
  Season2 = integer(),
  P_value = numeric(),
  stringsAsFactors = FALSE
)

# Effectuer le test Mann-Whitney pour chaque paire de saisons dans chaque ligue
for (league in leagues) {
  # Filtrer les données pour la ligue actuelle
  df_league <- df_home %>% filter(League == league)
  
  for (i in 1:(length(seasons) - 1)) {
    for (j in (i + 1):length(seasons)) {
      season1 <- seasons[i]
      season2 <- seasons[j]
      
      # Extraire les données pour chaque saison
      data_season1 <- df_league %>% filter(Season == season1) %>% pull(xPTS)
      data_season2 <- df_league %>% filter(Season == season2) %>% pull(xPTS)
      
      # Vérifier s'il y a suffisamment de données
      if (length(data_season1) > 1 && length(data_season2) > 1) {
        # Effectuer le test de Mann-Whitney
        test_result <- wilcox.test(data_season1, data_season2, exact = FALSE)
        p_value <- test_result$p.value
      } else {
        p_value <- NA
      }
      
      # Ajouter le résultat au tableau
      results <- rbind(results, data.frame(
        League = league,
        Season1 = season1,
        Season2 = season2,
        P_value = p_value
      ))
    }
  }
}

# Afficher les résultats
print(results)

# Sauvegarder les résultats dans un fichier CSV
write.csv(results, "mann_whitney_results.csv", row.names = FALSE)
