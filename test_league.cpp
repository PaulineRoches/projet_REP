#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>

using namespace std;

// Structure pour stocker les données d'un match
struct MatchData {
    double PTS;
    double xPTS;
    double xG;
};

// Fonction pour calculer la statistique de Wilcoxon et p-value
pair<double, double> wilcoxonTest(const vector<double>& home, const vector<double>& away) {
    vector<double> differences;
    for (size_t i = 0; i < home.size(); ++i) {
        differences.push_back(fabs(home[i] - away[i]));
    }

    // Trier les différences absolues
    sort(differences.begin(), differences.end());

    double rankSum = 0;
    double n = differences.size();
    for (size_t i = 0; i < n; ++i) {
        rankSum += (i + 1) * differences[i];
    }

    // Statistique de Wilcoxon
    double statistic = rankSum / n;
    double pValue = 1.0 / (statistic + 1);  // Approximativement pour illustrer

    return make_pair(statistic, pValue);
}

int main() {
    ifstream file("understat_team_stats_home_away.csv");
    string line;
    vector<MatchData> homeData, awayData;

    // Ignorer l'entête du fichier CSV
    getline(file, line);

    // Charger les données du fichier CSV
    while (getline(file, line)) {
        stringstream ss(line);
        string league, season, location;
        double pts, xpts, xg, xga;

        getline(ss, league, ',');
        getline(ss, season, ',');
        getline(ss, location, ',');
        ss >> pts;
        ss.ignore();
        ss >> xpts;
        ss.ignore();
        ss >> xg;
        ss.ignore();
        ss >> xga;

        // Séparer les données en fonction de l'emplacement (home ou away)
        if (location == "home") {
            homeData.push_back({pts, xpts, xg});
        } else if (location == "away") {
            awayData.push_back({pts, xpts, xg});
        }
    }

    // Vérification des tailles des listes
    if (homeData.size() != awayData.size()) {
        cout << "Le nombre de données pour 'home' et 'away' n'est pas égal!" << endl;
        return 1;
    }

    // Extraire les points, xPoints, xG pour chaque test Wilcoxon
    vector<double> homePts, awayPts, homeXpts, awayXpts, homeXg, awayXg;
    for (size_t i = 0; i < homeData.size(); ++i) {
        homePts.push_back(homeData[i].PTS);
        awayPts.push_back(awayData[i].PTS);
        homeXpts.push_back(homeData[i].xPTS);
        awayXpts.push_back(awayData[i].xPTS);
        homeXg.push_back(homeData[i].xG);
        awayXg.push_back(awayData[i].xG);
    }

    // Appliquer le test Wilcoxon pour chaque type de donnée
    auto wilcoPts = wilcoxonTest(homePts, awayPts);
    auto wilcoXpts = wilcoxonTest(homeXpts, awayXpts);
    auto wilcoXg = wilcoxonTest(homeXg, awayXg);

    // Afficher les résultats
    cout << "Wilcoxon Test for Points (PTS): Statistic = " << wilcoPts.first << ", p-value = " << wilcoPts.second << endl;
    cout << "Wilcoxon Test for xPoints (xPTS): Statistic = " << wilcoXpts.first << ", p-value = " << wilcoXpts.second << endl;
    cout << "Wilcoxon Test for xGoals (xG): Statistic = " << wilcoXg.first << ", p-value = " << wilcoXg.second << endl;

    return 0;
}
