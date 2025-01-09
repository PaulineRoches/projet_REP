#!/bin/sh

# Exécuter les fichiers liés à la reproduction
echo "Exécution des fichiers liés à la reproduction..."
python3 /app/reproduction/reproduce_diff_points.py
python3 /app/reproduction/graphs_par_ligue.py
python3 /app/reproduction/wilcoxon_with_undestat.py
python3 /app/reproduction/mannwhitneyu.py

# Exécuter les fichiers liés à la replicabilité : web scraping
echo "Exécution des fichiers liés à la replicabilité : web scraping..."
python3 /app/replicabilite/web_scraping/scrap.py
python3 /app/replicabilite/web_scraping/reproduce_diff_points.py
python3 /app/reproduction/web_scraping/graphs_par_ligue.py
python3 /app/reproduction/web_scraping/wilcoxon_replic.py
python3 /app/reproduction/web_scraping/mannwhitneyu.py

# Exécuter les fichiers liés à la replicabilité : new statistical method
echo "Exécution des fichiers liés à la replicabilité : new statistical method..."
python3 /app/replicabilite/new_statistical_method/repeated_measures_anova.py

# Exécuter les fichiers liés à la replicabilité : more seasons
echo "Exécution des fichiers liés à la replicabilité : more seasons..."
python3 /app/replicabilite/more_seasons/scrap_2023.py
python3 /app/replicabilite/more_seasons/reproduce_diff_points_2023.py
python3 /app/reproduction/more_seasons/graphs_par_ligue_2023.py
python3 /app/reproduction/more_seasons/wilcoxon_with_undestat_2023.py
python3 /app/reproduction/more_seasons/mannwhitneyu_2023.py

# Exécuter les fichiers liés à la replicabilité : last version
echo "Exécution des fichiers liés à la replicabilité : last version..."
python3 /app/replicabilite/last_version_python/mannwhitneyu.py

# Exécuter analyse.ipynb (en utilisant nbconvert pour le convertir et l'exécuter)
echo "Exécution de analyse.ipynb..."
jupyter nbconvert --to notebook --execute --inplace /app/analyse.ipynb

echo "Tous les scripts ont été exécutés avec succès!"
