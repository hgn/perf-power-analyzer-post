#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# Read the data into a DataFrame
data = pd.read_csv("wakeups-timemap-cpu.txt", sep='\s+', header=None)

# Set the column names
columns = ['cpu'] + [f'time{i}' for i in range(2, len(data.columns) + 1)]
data.columns = columns
max_value = data.iloc[:, 1:].max().max()
data = data.head(30)

tasks = data.shape[0]


fig, ax = plt.subplots(tasks, 1, sharex=True, figsize=(30, 20))
for i, data in enumerate(data.iterrows()):
    index, row = data
    cpu = row.iloc[0]
    row_max_value = row.iloc[1:].max()
    row_mean_value = row.iloc[1:].mean()
    reshaped_array = np.array(row.iloc[1:]).reshape((1, -1))
    im = ax[i].imshow(reshaped_array, cmap=plt.cm.inferno_r, extent=[0, 10, 0, 10], aspect='auto', interpolation='none', vmin=0, vmax=max_value)
    text = f"\\textbf{{CPU {cpu}}}\nMax {row_max_value}  Mean {row_mean_value:.1f}"
    ax[i].text(-1, 5, text, multialignment='left', va='center', ha='left', fontsize=12, usetex=True)

cbar_ax = fig.add_axes([0.95, 0.1, 0.03, 0.8])  # [left, bottom, width, height]
cbar = fig.colorbar(im, cax=cbar_ax)

for a in ax:
    a.set_xticks([])
    a.set_yticks([])
    a.set_xticklabels([])
    a.set_yticklabels([])
    a.spines['top'].set_visible(False)
    a.spines['right'].set_visible(False)
    a.spines['bottom'].set_visible(False)
    a.spines['left'].set_visible(False)

plt.savefig('wakeups-timemap-cpu.pdf')
plt.savefig('wakeups-timemap-cpu.png')
