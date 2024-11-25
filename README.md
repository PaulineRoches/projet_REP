# Reproduction and Replication of "COVID and Home Advantage in Football"

This project is based on the paper [*"COVID and Home Advantage in Football: An Analysis of Results and xG Data in European Leagues"*](https://blog.mathieuacher.com/FootballAnalysis-xG-COVIDHome/) by Mathieu Acher.

## Introduction

> *Briefly introduce the subject of the study, the problem it addresses, and the key results or insights obtained from the reproduction and replication effort.*

ChatGPT

The study conducted by Mathieu Acher aims to examine the impact of football supporters' presence on a team's performance. The question posed is: is there an advantage to playing at home? Intuitively, one might think the answer is yes, but the goal is to objectively verify this. The results of his study show that seasons without spectators affected team performance, as teams performed worse at home without their supporters, particularly in *Ligue 1* and  *Premier League* during the 2020-2021 season.

We replicated and reproduced this study to verify its findings.

**/!\ CONCLUSIONS de notre  étude /!\\**

## Reproducibility

### How to Reproduce the Results
1. **Requirements**  

The project uses the dependencies listed in `requirements.txt`. They are installed with other ones in `Dockerfile`. 

2. **Setting Up the Environment**  

Here are the commands to build the Docker environnement :
```bash
 docker build -t reproducible-project .
 docker run -rm reproducible-project
```

3. **Reproducing Results**  

The Docker container runs the various scripts needed to reproduce the study.
   - `entrypoint.sh` is executed at the end of the `Dockerfile` and runs all the scripts :
     ```sh
     sh ./entrypoint.sh
     ```
   - Our analysis work is contained in the Jupyter Notebook `analyse.ipynb`.

4. **Automation (Bonus)**  
   - Explain the included GitHub Action that produces or analyzes data automatically.  
    
### Encountered Issues and Improvements
- Report any challenges, errors, or deviations from the original study.
- Describe how these issues were resolved or improved, if applicable.

### Is the Original Study Reproducible?
- Summarize the success or failure of reproducing the study.
- Include supporting evidence, such as comparison tables, plots, or metrics.

## Replicability

### Variability Factors
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


### Replication Execution
1. **Instructions**  
   - Provide detailed steps or commands for running the replication(s):  
     ```bash
     bash scripts/replicate_experiment.sh
     ```

2. **Presentation and Analysis of Results**  
   - Include results in text, tables, or figures.
   - Analyze and compare with the original study's findings.

### Does It Confirm the Original Study?
- Summarize the extent to which the replication supports the original study’s conclusions.
- Highlight similarities and differences, if any.

## Conclusion
- Recap findings from the reproducibility and replicability sections.
- Discuss limitations of your
