#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"
FILE_JSON = FILE_BASE + ".json"


# Read data from file
df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]', 'Miss'])
residencies = pd.read_json(FILE_JSON)

with open(FILE_JSON, 'r') as file:
    residencies = json.load(file)

RES_CPU = 'cpu0'
print(f'WARNING: only using residencies of {RES_CPU}!')
residencies = residencies[RES_CPU]

# Calculates the optimal matching C-State
for i in range(len(df)):
    sleep = df.loc[i]['Sleep[ns]']
    state = df.loc[i]['C-State']
    # The smallest residency is always 0
    opt_res_time = -1
    opt_res_name = None
    for res in residencies.items():
        if int(res[1]['residency'])*1000 <= sleep and int(res[1]['residency']) >= opt_res_time:
            opt_res_time = int(res[1]['residency'])
            opt_res_name = res[1]['name']
    if opt_res_name is None:
        df.loc[i, 'Optimal-State'] = df.loc[i, 'C-State']
    else:
        df.loc[i, 'Optimal-State'] = opt_res_name

# Correlate Optimal State and Chosen State
tab = pd.crosstab(df['C-State'], df['Optimal-State'], normalize=0)
norm_trans = np.array(tab.div(tab.sum(axis=1), axis=0))

# Create heatmap
fig, ax = plt.subplots()
im = ax.imshow(norm_trans)

# Set Ticks
ax.set_xticks(np.arange(len(tab.axes[1])), labels=tab.axes[1])
ax.set_yticks(np.arange(len(tab.axes[0])), labels=tab.axes[0])

# Format Axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Create Annotations
for i in range(len(df['C-State'].unique())):
    for j in range(len(df['Optimal-State'].unique())):
        text = ax.text(j, i, f'{norm_trans[i, j]:.2f}',
                       ha="center", va="center", color="w")


plt.xlabel('Optimal C-State')
plt.ylabel('Chosen C-State')

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
