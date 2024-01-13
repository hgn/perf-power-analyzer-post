#!/usr/bin/python3

import os
import sys
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

df = pd.read_csv(FILE_DATA, delim_whitespace=True)

df['RoundedTime'] = df['Time'].round()
grouped = df.groupby(['RoundedTime', 'PID', 'Comm']).size().reset_index(name='EventCount')

# filter out task with less events
min_events_per_task = 500
total_events_per_pid = grouped.groupby(['PID', 'Comm'])['EventCount'].sum()
pids_to_include = total_events_per_pid[total_events_per_pid > min_events_per_task].index
filtered_grouped = grouped[grouped.set_index(['PID', 'Comm']).index.isin(pids_to_include)]

pivot_df = filtered_grouped.pivot(index='RoundedTime', columns=['PID', 'Comm'], values='EventCount')

# fill missing time values with 0
complete_time_index = pd.RangeIndex(start=df['RoundedTime'].min(), stop=df['RoundedTime'].max() + 1)
pivot_df = pivot_df.reindex(complete_time_index, fill_value=0)

plt.rcParams.update({'font.size': 6})
markersize = 2
linewidth = .7

fig, ax = plt.subplots(figsize=(10, 6))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.xaxis.grid(which='major', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.xaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.yaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.set_axisbelow(True)
ax.ticklabel_format(style='plain')
marker = itertools.cycle(('o', 's', '^', 'v', '*', '+', 'x', 'D')) 

for (pid, comm) in pivot_df:
    ax.plot(pivot_df.index, pivot_df[(pid, comm)], label=f'{comm} ({pid})',
            marker=next(marker), markersize=markersize, linewidth=linewidth)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Timer Expires [Hz]')
ax.legend()
#ax.set_yscale('log')

print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
