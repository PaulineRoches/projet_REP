# Reproduction and Replication of "COVID and Home Advantage in Football"

This project is based on the paper [*"COVID and Home Advantage in Football: An Analysis of Results and xG Data in European Leagues"*](https://blog.mathieuacher.com/FootballAnalysis-xG-COVIDHome/) by Mathieu Acher.

## Introduction

The study conducted by Mathieu Acher aims to examine the impact of football supporters' presence on a team's performance. The question posed is: is there an advantage to playing at home? Intuitively, one might think the answer is yes, but the goal is to objectively verify this. The results of his study show that seasons without spectators affected team performance, as teams performed worse at home without their supporters, particularly in *Ligue 1* and  *Premier League* during the 2020-2021 season.

We replicated and reproduced this study to verify its findings.

## Reproducibility & Replicability

### How to see the Results
1. **Requirements**  

The project uses the dependencies listed in `requirements.txt`. They are installed with other ones in `Dockerfile`. 

2. **Setting Up the Environment**  

Here are the commands to build the Docker environnement :
```bash
 docker build -t reproducible-project .
 docker run -rm reproducible-project
```

3. **Reproducing & Replicability Results**  

The Docker container runs the various scripts needed to reproduce and replicate the study.
   - `entrypoint.sh` is executed at the end of the `Dockerfile` and runs all the scripts :
     ```sh
     sh ./entrypoint.sh
     ```
   - Our analysis work is contained in the Jupyter Notebook `analyse.ipynb`. There is a part named **Reproduction of the study** and another one named **Replication of the study**.

### Reproducibility

#### Encountered Issues and Improvements with reproduction
The main difficulty we had with the reproduction was that there was no clear indication about the environnement used in the original study. So it was challenging to obtain the same results. Our principal difficulty was the data extraction method as we did not find the exact same results with web scraping than in Mathieu Acher's work. Finding the existence of the library Understat was very useful to help us obtain similar results. The little errors we made by trying to reproduce the study allowed us to think about what affects the results of the study, like a sort of introduction to the replicability part.

#### Is the Original Study Reproducible?
Even though it's difficult as we have no given instructions, the original study is reproducible. We were able to match the findings of the original study (see part **Reproduction of the study** in `analyse.ipynb`) by trying to applicate the methods said to be used in Mathieu Acher's work. 

### Replicability

#### Variability Factors
- **List of Factors**: We identified different factors of variability :  

  | Variability Factor | Possible Values     | Relevance                                   |
  |--------------------|---------------------|--------------------------------------------|
  | Extraction Data method | Web-scraping or python package | Changes results for some statistical tests |
  | Statistical tests | ANOVA, Wilcoxon test, Mann-Whitney U test  | May affect the conclusions |
  | Seasons | 2014-2020 or 2014-2023 | May confirm the impact of fans |
  | SciPy version | 1.7.0+ or before | Changes the test |
  | Data classification | By team or by match | May change the conclusions for statistical tests |
  | Data source | Understat or another dataset | May change the way of collectig the data and give other indicators|

Here’s an improved version with the original context and the new addition:

We did not have the opportunity to test the last two factors thoroughly. During our initial attempt to reproduce the study, we analyzed data by team rather than by match. This methodological difference altered the results of the tests significantly. Since this approach was intertwined with web-scraping factors, we could not rely on these results, nor confirm their validity using the Python package due to time constraints.As a result, we were unable to take these findings into account and did not have sufficient time to verify them with the Python implementation.


#### Does It Confirm the Original Study?
All these variability factors ultimately supported the conclusions of the original study. While some factors introduced minor variations in the outcomes, the central hypothesis remains validated: the presence of fans significantly influences match results in most European leagues.

However, it is crucial to interpret these findings with caution. Changes in methodology, such as adjustments in how data is analyzed or aggregated, can lead to less pronounced differences in team performance and outcomes. This underlines the sensitivity of the results to the chosen approach.

## Conclusion
Reproduction of the study confirmed the initial hypothesis: having supporters in the stadium positively impacts team performance, boosting points and goals scored, as well as expected points and goals. In this phase, we carefully revisited the original analysis to ensure it was accurate and consistent. We found that playing at home generally gives teams a clear advantage. However, during the COVID-19 seasons, when games were played without fans, this advantage dropped significantly or even reversed.

In the replication phase, we went beyond just checking the original findings. We tested how solid these conclusions were by using different datasets, new statistical methods, and various tools. While the results mostly supported the original findings—showing that fan presence is crucial for home advantage—we also found some differences. For example, the drop in home advantage varied depending on the league, team, and specific match conditions. This suggests that the effect of having fans isn’t the same in every situation.

These differences show that home advantage is influenced by more than just whether fans are present. The replication highlighted that while the overall trend holds, certain situations may show different results. This points to the need for further research to better understand how factors like team tactics or mental toughness interact with fan presence.

In conclusion, the study confirms that supporters play a big role in boosting team performance, matching the initial hypothesis. However, the replication also showed that the story is more complex, especially under unusual conditions like those during the pandemic. Exploring more datasets and methods can help uncover a deeper understanding of how fans influence football outcomes.
