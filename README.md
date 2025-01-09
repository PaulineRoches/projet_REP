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
  | SciPy version | 1.7.0+ or before | Changes the Mann-Whitney U test and its conclusions |
  | Data classification | By team or by match | May change the conclusions for statistical tests |
  | Data source | Understat or another dataset | May change the way of collectig the data and give other indicators|

Here’s an improved version with the original context and the new addition:

We did not have the opportunity to test the last two factors thoroughly. During our initial attempt to reproduce the study, we analyzed data by team rather than by match. This methodological difference altered the results of the tests significantly. Since this approach was intertwined with web-scraping factors, we could not rely on these results, nor confirm their validity using the Python package due to time constraints.As a result, we were unable to take these findings into account and did not have sufficient time to verify them with the Python implementation.


#### Does It Confirm the Original Study?
All these variability factors ultimately supported the conclusions of the original study. While some factors introduced minor variations in the outcomes, the central hypothesis remains validated: the presence of fans significantly influences match results in most European leagues.

However, it is crucial to interpret these findings with caution. Changes in methodology, such as adjustments in how data is analyzed or aggregated, can lead to less pronounced differences in team performance and outcomes. This underlines the sensitivity of the results to the chosen approach.

## Conclusion
- Recap findings from the reproducibility and replicability sections.
- Discuss limitations of your
