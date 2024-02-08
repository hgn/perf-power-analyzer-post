#!/usr/bin/python3

from pathlib import Path
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_JSON = FILE_BASE + ".json"
OUTPUT_FOLDER = "scatter"


def unique_res(residencies, target_cpu=0):
    res_dict = residencies[list(residencies.keys())[target_cpu]]
    res = set()
    for state in res_dict.values():
        res.add(state['residency'])
    res = sorted([int(x) for x in res])
    return res

# target_cpu is used for retrieving the residency times
def graph_scatter_sleeptime_by_sequence(df, graph_cstate, residencies, unique_res, target_cpu=0):
    df = df[df['C-State'] == cstate].reset_index(drop=True)
    if len(df) == 0:
        return

    prev_color = 'red'
    prev_marker = '^'
    prev_cond = (df['Below'] == '0') & (df['Miss'] != 0)

    next_color = 'orange'
    next_marker = 'v'
    next_cond = (df['Below'] == '1') & (df['Miss'] != 0)

    perfect_color = 'green'
    perfect_marker = 'o'
    perfect_cond = (df['Miss'] == 0)

    df_perfect = df[perfect_cond]
    df_prev = df[prev_cond]
    df_next = df[next_cond]

    i_perfect = df.loc[perfect_cond].index.to_list()
    i_next = df.loc[next_cond].index.to_list()
    i_prev = df.loc[prev_cond].index.to_list()

    plt.scatter(x=i_perfect, y=df_perfect['Sleep[ns]'].div(1000), alpha=0.4, s=20, c=perfect_color, marker=perfect_marker, edgecolors="none")
    plt.scatter(x=i_prev, y=df_prev['Sleep[ns]'].div(1000), alpha=0.4, s=20, c=prev_color, marker=prev_marker, edgecolors="none")
    plt.scatter(x=i_next, y=df_next['Sleep[ns]'].div(1000), alpha=0.4, s=20, c=next_color, marker=next_marker, edgecolors="none")

    res_dict = residencies[list(residencies.keys())[target_cpu]]
    prev_res = None
    target_res = None
    next_res = None

    for res_state in res_dict.values():
        if graph_cstate == res_state['name']:
            target_res = int(res_state['residency'])
            break

    prev_res = unique_res[0]

    index = unique_res.index(int(target_res))
    prev_res = unique_res[index - 1] if index > 0 else None
    next_res = unique_res[index + 1] if index < len(unique_res) - 1 else None

    plt.plot([0, len(df)], [target_res, target_res], color=perfect_color, alpha=0.5,
             label="Target Residency", linewidth=1.2)
    if prev_res is not None:
        plt.plot([0, len(df)], [prev_res, prev_res], color=prev_color, alpha=0.5,
                 label="Previous Residency", linestyle="dotted")
    if next_res is not None:
        plt.plot([0, len(df)], [next_res, next_res], color=next_color, alpha=0.5,
                 label="Next Residency", linestyle="dotted")

    plt.xlabel("Sequence")
    plt.ylabel("Idle Time (" + chr(181) + "s)")
    plt.grid(linewidth=0.3)

    plt.yscale("log")
    plt.legend()

    ax = plt.subplot(111)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlim(left=0)

    file_name = f'{OUTPUT_FOLDER}/scatter-{cstate}.png'
    print(f'generate {file_name}')
    plt.savefig(file_name, dpi=300)
    plt.close()

if __name__ == '__main__':
    # Read data from files
    df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]', 'Miss', 'Below'])
    with open(FILE_JSON, 'r') as res_file:
        residencies = json.load(res_file)
    unique_res = unique_res(residencies)
    Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    # Create Graphs
    for cstate in df['C-State'].unique():
        graph_scatter_sleeptime_by_sequence(df, cstate, residencies, unique_res)
