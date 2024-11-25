#!/bin/sh

# Exécuter scrap.py
echo "Exécution de scrap.py..."
python3 /app/scrap.py

# Exécuter reproduce_diff_points.py
echo "Exécution de reproduce_diff_points.py..."
python3 /app/reproduce_diff_points.py

# Exécuter graph_par_ligue.py
echo "Exécution de graph_par_ligue.py..."
python3 /app/graphs_par_ligue.py

# Exécuter analyse.ipynb (en utilisant nbconvert pour le convertir et l'exécuter)
echo "Exécution de analyse.ipynb..."
jupyter nbconvert --to notebook --execute --inplace /app/analyse.ipynb

echo "Tous les scripts ont été exécutés avec succès!"
