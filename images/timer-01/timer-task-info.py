#!/usr/bin/python3

import os
import sys
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

FILE_BASE = os.path.basename(__file__).rstrip('.py')
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

df = pd.read_csv(FILE_DATA, delim_whitespace=True)

data_sorted = df.sort_values(by='Expires', ascending=False)

data_sorted = data_sorted.head(10)
index = np.arange(len(data_sorted))


# matplotlib settings
plt.rcParams.update({'font.size': 8})
fig, ax = plt.subplots(figsize=(10, 6))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
#ax.xaxis.grid(which='major', linestyle=':', linewidth='0.5', color='#bbbbbb')
#ax.xaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.yaxis.grid(which='major', linestyle='solid', linewidth='0.5', color='#bbbbbb')
ax.yaxis.grid(which='minor', linestyle=':', linewidth='0.3', color='#bbbbbb')
ax.set_axisbelow(True)
ax.ticklabel_format(style='plain')

# Plotting each category
colors = cm.inferno(np.linspace(0.25, 0.75, 4))
bar_width = 0.20

# Plotting each category for the top 10 tasks with labels
timers_expires = ax.bar(index, data_sorted['Timers'], bar_width, color=colors[0], label='Number of Timers')
bars_starts = ax.bar(index + bar_width, data_sorted['Starts'], bar_width, color=colors[1], label='Timer Starts')
bars_cancels = ax.bar(index + 2 * bar_width, data_sorted['Cancels'], bar_width, color=colors[2], label='Timer Cancels')
bars_expires = ax.bar(index + 3 * bar_width, data_sorted['Expires'], bar_width, color=colors[3], label='Timer Expires')

# Adding labels on top of each bar
ax.bar_label(timers_expires, padding=3, fontsize=5, rotation=45)
ax.bar_label(bars_starts, padding=3, fontsize=5, rotation=45)
ax.bar_label(bars_cancels, padding=3, fontsize=5, rotation=45)
ax.bar_label(bars_expires, padding=3, fontsize=5, rotation=45)


# Labeling
ax.set_xlabel('Task')
ax.set_ylabel('Timer Info [#]')
ax.set_xticks(index + bar_width)
ax.set_xticklabels(data_sorted['Comm'], rotation=45)
ax.legend()

ax.set_yscale('log')

print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
