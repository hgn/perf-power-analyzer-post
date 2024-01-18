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


# Read data from file
df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]', 'CPU'])
residencies = pd.read_json(FILE_JSON)


# Calculates the optimal matching C-State
for i in range(len(df)):
    sleep = df.loc[i]['Sleep[ns]']
    state = df.loc[i]['C-State']
    # The smallest residency is always 0
    opt_res_time = -1
    opt_res_name = None
    for res in residencies['cpu' + str(df.loc[i]['CPU'])].items():
        if int(res[1]['residency'])*1000 <= sleep and int(res[1]['residency']) >= opt_res_time:
            opt_res_time = int(res[1]['residency'])
            opt_res_name = res[1]['name']
    if opt_res_name is None:
        df.loc[i, 'Optimal-State'] = df.loc[i, 'C-State']
    else:
        df.loc[i, 'Optimal-State'] = opt_res_name


i_col = sorted(set(df['C-State'].unique()).union(df['Optimal-State'].unique()))

# Correlate Optimal State and Chosen State
tab = pd.crosstab(df['C-State'], df['Optimal-State']).reindex(index=i_col, columns=i_col, fill_value=0)
norm_trans = np.array(tab.div(tab.sum(axis=1), axis=0).fillna(0))

# Create heatmap
fig, ax = plt.subplots()
im = ax.imshow(norm_trans)

# Set Ticks
ax.set_xticks(np.arange(len(tab.axes[1])), labels=tab.axes[1])
ax.set_yticks(np.arange(len(tab.axes[0])), labels=tab.axes[0])

# Create Annotations
for i in range(len(tab.axes[0])):
    for j in range(len(tab.axes[1])):
        text = ax.text(j, i, f'{norm_trans[i, j]:.2f}',
                       ha="center", va="center", color="w")


plt.xlabel('Optimal C-State')
plt.ylabel('Chosen C-State')
plt.gca().invert_yaxis()

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
