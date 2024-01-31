#!/usr/bin/python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from pathlib import Path

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"
FILE_JSON = FILE_BASE + ".json"
OUTPUT_FOLDER = "cstates"


def unique_res(residencies, target_cpu=0):
    res_dict = residencies[list(residencies.keys())[target_cpu]]
    res = set()
    for state in res_dict.values():
        res.add(state['residency'])
    res = sorted([int(x) for x in res])
    return res

def graph_scatter_sleeptime_by_sequence(df, graph_cstate, residencies, unique_res, target_cpu=0):
    prev_color = 'red'
    next_color = 'orange'
    perfect_color = 'green'
    df = df[df['C-State'] == cstate]
    x = list(range(len(df)))
    if len(x) == 0:
        return
    y=df['Sleep[ns]'].div(1000)
    col = np.where(df['Miss'] == 0, perfect_color, np.where(df['Below'] == '0', prev_color, next_color))
    plt.scatter(x=x, y=y, alpha=0.4, s=20, c=col, edgecolors="none")

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
    plt.savefig(f'cstates/scatter-{cstate}.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    # Read data from files
    df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]', 'Miss', 'Below'])
    with open(FILE_JSON, 'r') as res_file:
        residencies = json.load(res_file)
    Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
    unique_res = unique_res(residencies)
    # Create Graphs
    for cstate in df['C-State'].unique():
        graph_scatter_sleeptime_by_sequence(df, cstate, residencies, unique_res)
