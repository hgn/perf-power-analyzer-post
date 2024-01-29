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

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['CPU', 'Sleep[ns]'])

no_tasks = df['CPU'].unique().shape[0]

fig, axs = plt.subplots(no_tasks, 1, sharex=True, figsize=(30, 20))

for i, cpu in enumerate(df['CPU'].unique()):
    row = df[df['CPU'] == cpu]
    reshaped_array = np.array(row['Sleep[ns]'].tolist()).reshape((1,-1))
    row_mean_value = row['Sleep[ns]'].mean()
    row_median_value = row['Sleep[ns]'].median()
    row_highest_value = row['Sleep[ns]'].max()
    im = axs[i].imshow(reshaped_array, cmap=plt.cm.inferno_r, extent=[0,10,0,10], aspect='auto', vmin=0, vmax=row_highest_value)
    text = f"CPU: {cpu}\nMean: {row_mean_value:,.0f} ns\nMedian: {row_median_value:,.0f} ns\nHighest: {row_highest_value:,.0f} ns"
    axs[i].text(-1, 5, text, multialignment='left', va='center', ha='left', fontsize=12, usetex=False)

# add colorbar legend
cbar_ax = fig.add_axes([0.95, 0.1, 0.03, 0.8])
cbar = fig.colorbar(im, cax=cbar_ax)

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
