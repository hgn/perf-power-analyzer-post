#!/usr/bin/python3

import os
import sys
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.basename(__file__).rstrip('.py')
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

data = pd.read_csv(FILE_DATA, delim_whitespace=True)

# Convert 'Time' to numeric and round to nearest second for grouping
data['Time'] = pd.to_numeric(data['Time']).round()

# Group by CPU and Time, then count occurrences
grouped_data = data.groupby(['CPU', 'Time']).size().reset_index(name='EventCount')

# Filter for first 8 CPUs
limited_cpus = grouped_data['CPU'].unique()[:8]

# Determining the maximum y-axis value for uniform scaling
max_event_count = grouped_data['EventCount'].max()

# Creating subplots for the first 8 CPUs in two columns
num_cpus = len(limited_cpus)

plt.rcParams.update({'font.size': 9})
markersize = 2
linewidth = .7
fig, axs = plt.subplots((num_cpus + 1) // 2, 2, figsize=(20, 2 * ((num_cpus + 1) // 2)), sharex=True)

for i, cpu in enumerate(limited_cpus):
    row, col = i // 2, i % 2
    cpu_data = grouped_data[grouped_data['CPU'] == cpu]
    axs[row, col].fill_between(cpu_data['Time'], cpu_data['EventCount'], color="#008080")
    axs[row, col].set_title(f'CPU {cpu}')
    axs[row, col].set_xlabel('Time [s]')
    axs[row, col].set_ylim(0, max_event_count)
    axs[row, col].spines["top"].set_visible(False)
    axs[row, col].spines["right"].set_visible(False)
    axs[row, col].spines["left"].set_visible(False)
    axs[row, col].yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='#bbbbbb')
    axs[row, col].set_axisbelow(True)
    axs[row, col].ticklabel_format(style='plain')

plt.tight_layout()

print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')

