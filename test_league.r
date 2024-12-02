# Test Wilcoxon
home <- c(22, 43, 42, 26, 44, 19, 22, 30, 29, 40, 52, 39, 24, 30, 18, 17, 19, 13, 11, 22)
away <- c(21, 20, 26, 15, 34, 21, 20, 22, 33, 37, 39, 39, 16, 49, 19, 6, 18, 20, 9, 17)

# Appliquer le test de Wilcoxon
result <- wilcox.test(away, home, paired = TRUE)

# Afficher les résultats
print(result)
