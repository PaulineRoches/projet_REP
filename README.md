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
- **List of Factors**: Identify all potential sources of variability (e.g., dataset splits, random seeds, hardware).  
  Example table:
  | Variability Factor | Possible Values     | Relevance                                   |
  |--------------------|---------------------|--------------------------------------------|
  | Random Seed        | [0, 42, 123]       | Impacts consistency of random processes    |
  | Hardware           | CPU, GPU (NVIDIA)  | May affect computation time and results    |
  | Dataset Version    | v1.0, v1.1         | Ensures comparability across experiments   |

- **Constraints Across Factors**:  
  - Document any constraints or interdependencies among variability factors.  
    For example:
    - Random Seed must align with dataset splits for consistent results.
    - Hardware constraints may limit the choice of GPU-based factors.

- **Exploring Variability Factors via CLI (Bonus)**  
   - Provide instructions to use the command-line interface (CLI) to explore variability factors and their combinations:  
     ```bash
     python explore_variability.py --random-seed 42 --hardware GPU --dataset-version v1.1
     ```
   - Describe the functionality and parameters of the CLI:
     - `--random-seed`: Specify the random seed to use.
     - `--hardware`: Choose between CPU or GPU.
     - `--dataset-version`: Select the dataset version.

#### Does It Confirm the Original Study?
- Summarize the extent to which the replication supports the original study’s conclusions.
- Highlight similarities and differences, if any.

## Conclusion
- Recap findings from the reproducibility and replicability sections.
- Discuss limitations of your
