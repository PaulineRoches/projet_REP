from scipy.stats import wilcoxon
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table
import aiohttp


def getHomeAwayResultPerMatch(result, home, away):
    if result['h'] > result['a']:
        home.append(3)
        away.append(0)
    elif result['h'] < result['a']:
        home.append(0)
        away.append(3)
    else:
        home.append(1)
        away.append(1)

def cohen_d(home, away):
    mean_a = np.mean(home)
    mean_b = np.mean(away)
    std_a = np.std(home, ddof=1)
    std_b = np.std(away, ddof=1)

    n_a = len(home)
    n_b = len(away)

    s_p = np.sqrt(((n_a - 1) * std_a**2 + (n_b - 1) * std_b**2) / (n_a + n_b - 2))
    cohen_d_value = (mean_a - mean_b) / s_p
    return cohen_d_value

def wilcoxon_test(array, home, away):
    for i in range(len(array)):
        getHomeAwayResultPerMatch(array[i]['goals'], home, away)
    stat, p = wilcoxon(home, away)
    return stat, p

def create_image(df):
    # Styling function
    def get_cell_color(val, col_name):
        if col_name.startswith('wilco-result-pvalue') and val > 0.05:
            return 'red'
        elif col_name.startswith('result-cohend') and val < 0.2:
            return 'yellow'
        return 'white'

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    table = Table(ax, bbox=[0, 0, 1, 1])
    n_rows, n_cols = df.shape

    # Add headers
    for (i, col_name) in enumerate(df.columns):
        table.add_cell(0, i, width=1 / n_cols, height=0.1, text=col_name, loc='center',
                       facecolor='gray', edgecolor='black')

    # Add data rows
    for row_idx, row in df.iterrows():
        for col_idx, (col_name, value) in enumerate(row.items()):
            color = get_cell_color(value, col_name)
            table.add_cell(row_idx + 1, col_idx, width=1 / n_cols, height=0.1,
                           text=f"{value:.4f}" if isinstance(value, float) else str(value),
                           loc='center', facecolor=color, edgecolor='black')

    ax.add_table(table)
    plt.savefig("styled_results.png", bbox_inches='tight', dpi=300)
    print("Image saved as 'styled_results.png'")

async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        final_df = pd.DataFrame(columns=["League", "Season", "wilco-result", "wilco-result-pvalue", "result-cohend"])
        for league in LEAGUES:
            for season in SEASONS:
                home_results = []
                away_results = []
                fixtures = await understat.get_league_results(league, season)
                num_array = np.array(fixtures)
                wilco_test = wilcoxon_test(num_array, home_results, away_results)
                cohend_test = cohen_d(home_results, away_results)
                new_row = pd.DataFrame({
                    "League": [league],
                    "Season": [season],
                    "wilco-result": [wilco_test[0]],
                    "wilco-result-pvalue": [wilco_test[1]],
                    "result-cohend": [cohend_test]
                })
                final_df = pd.concat([final_df, new_row], ignore_index=True)

        # Create and save the styled image
        create_image(final_df)

await main()
