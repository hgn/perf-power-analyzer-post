#!/usr/bin/python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"
FILE_JSON = FILE_BASE + ".json"


def graph_scatter_sleeptime_by_sequence(df, graph_cstate):
    prev_color = 'red'
    next_color = 'orange'
    perfect_color = 'green'
    df = df[df['C-State'] == cstate]
    x = list(range(len(df)))
    if len(x) == 0:
        return
    y=df['Sleep[ns]']
    col = np.where(df['Miss'] == 0, perfect_color, np.where(df['Below'] == '0', prev_color, next_color))
    plt.scatter(x=x, y=y, alpha=0.4, s=20, c=col, edgecolors="none")
    plt.xlabel("Sequence")
    plt.ylabel("Idle Time (" + chr(181) + "s)")
    plt.grid(linewidth=0.3)
    """
    residency = df["residency"].iloc[0]
    prev_residency = df["prev_residency"].iloc[0]
    next_residency = df["next_residency"].iloc[0]
    plt.plot([0, len(df)], [residency, residency], color=perfect_color, alpha=0.5,
             label="Residency", linewidth=1.2)
    #TODO: change this, such that it is not that hacky with String None
    if prev_residency != "None":
        prev_residency = int(prev_residency)
        plt.plot([0, len(df)], [prev_residency, prev_residency], color=prev_color, alpha=0.5,
                 label="Previous Residency", linestyle="dotted")
    if next_residency != "None":
        next_residency = int(next_residency)
        plt.plot([0, len(df)], [next_residency, next_residency], color=next_color, alpha=0.5,
                 label="Next Residency", linestyle="dotted")
    """
    plt.yscale("log")
    plt.legend()
    ax = plt.subplot(111)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xlim(left=0)
    plt.savefig(f'cstates/scatter-{cstate}.png', dpi=300)
    plt.close()

# Read data from file
df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]', 'Miss', 'Below'])
residencies = pd.read_json(FILE_JSON)

for cstate in df['C-State'].unique():
    graph_scatter_sleeptime_by_sequence(df, cstate)
