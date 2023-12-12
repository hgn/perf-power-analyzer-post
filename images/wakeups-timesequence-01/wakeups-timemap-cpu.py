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

tasks = data.shape[0]

fig, axs = plt.subplots(tasks, 1, sharex=True, figsize=(30, 20))
for i, data in enumerate(data.iterrows()):
    index, row = data
    cpu = row.iloc[0]
    row_max_value = row.iloc[1:].max()
    row_mean_value = row.iloc[1:].mean()
    reshaped_array = np.array(row.iloc[1:]).reshape((1, -1))
    im = axs[i].imshow(reshaped_array, cmap=plt.cm.inferno_r, extent=[0, 10, 0, 10], aspect='auto', interpolation='none', vmin=0, vmax=max_value)
    # I use TeX here for boldface font generatiom, remove textbf and usetex=False
    # to get rid of it
    text = f"\\textbf{{CPU {cpu}}}\nMax {row_max_value}  Mean {row_mean_value:.1f}"
    axs[i].text(-1, 5, text, multialignment='left', va='center', ha='left', fontsize=12, usetex=True)

cbar_ax = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cbar = fig.colorbar(im, cax=cbar_ax)

for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

plt.savefig('wakeups-timemap-cpu.pdf')
plt.savefig('wakeups-timemap-cpu.png')
