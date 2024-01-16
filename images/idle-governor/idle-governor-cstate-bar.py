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
df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]'])
residencies = pd.read_json(FILE_JSON)
with open(FILE_JSON, 'r') as file:
    residencies = json.load(file)
RES_CPU = 'cpu0'
print(f'WARNING: only using residencies of {RES_CPU}!')
residencies = residencies[RES_CPU]

# Group by C-State and sum the sleeping times
grouped_data = df.groupby(['C-State']).sum('Sleep[ns]').reset_index()
for res in residencies.items():
    grouped_data.loc[grouped_data['C-State'] == res[1]['name'], 'Residency'] = res[1]['residency']
#TODO: remove columns drop, if residency has been visualized correctly
grouped_data = grouped_data.drop(columns='Residency')

# Sort the data by Sleep Time in descending order
sorted_data = grouped_data.sort_values(by='Sleep[ns]', ascending=False)

# Parameters for Grouped Barchart
width = 0.4

# Creating a sorted 90% rotated bar chart with logarithmic scale
fig, ax = plt.subplots()
ax.barh(sorted_data['C-State'], sorted_data['Sleep[ns]'], width, log=True, color='orange')
#TODO: use residency time for second bar
ax.barh(sorted_data['C-State'], sorted_data['Sleep[ns]'], width/2, log=True, color='green')

# format axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for c in ax.containers:
    ax.bar_label(c, fmt='{:,.0f}')

plt.xlabel('Sleep Time [ns]')
plt.ylabel('C-State')
plt.gca().invert_yaxis()

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
