#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['CPU', 'C-State'])

no_tasks = df['CPU'].unique().shape[0]

fig, axs = plt.subplots(no_tasks, 1, sharex=True, figsize=(30, 20))
cstate_map = {}
cstates = df['C-State'].unique()
cstates.sort()
for i, cstate in enumerate(cstates):
    cstate_map[cstate] = i
df['C-State-Mapped'] = df['C-State'].map(cstate_map)

for i, cpu in enumerate(df['CPU'].unique()):
    row = df[df['CPU'] == cpu]
    reshaped_array = np.array(row['C-State-Mapped'].tolist()).reshape((1,-1))
    row_most_used_state = row.groupby('C-State').size().idxmax()
    row_most_used_amount = row.groupby('C-State').size().max()
    im = axs[i].imshow(reshaped_array, cmap='tab20b')
    text = f"\nCPU: {cpu}\nMost Used: {row_most_used_state} ({row_most_used_amount:,})"
    axs[i].text(-1, 5, text, multialignment='left', va='center', ha='left', fontsize=12, usetex=False)

# add colorbar legend
bounds = np.linspace(0,len(cstates),len(cstates)+1)
cbar_ax = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cbar = fig.colorbar(im, cax=cbar_ax, boundaries=bounds, ticks=bounds)
cbar.set_ticks(list(set(cstate_map.values())))
cbar.set_ticklabels([cstate for cstate, value in sorted(cstate_map.items(), key=lambda x: x[1])])

# remove borders and make is look more modern
for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
