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
grouped_data = df.groupby(by='C-State').agg({'Sleep[ns]' : 'sum', 'C-State' : 'size'})
grouped_data = grouped_data.rename(columns={'C-State' : 'Entries'}).reset_index()
for res in residencies.items():
    grouped_data.loc[grouped_data['C-State'] == res[1]['name'], 'Residency'] = int(res[1]['residency'])

# Sort the data by Sleep Time in descending order
sorted_data = grouped_data.sort_values(by='Sleep[ns]', ascending=False)

# Parameters for Grouped Barchart
width = 0.4
sleep_colors = plt.cm.summer(np.linspace(0.1, 0.9, len(grouped_data)))
res_colors = plt.cm.winter(np.linspace(0.1, 0.9, len(grouped_data)))

# Creating a sorted 90% rotated bar chart with logarithmic scale
fig, ax = plt.subplots()
sleep_bar = ax.barh(sorted_data['C-State'], sorted_data['Sleep[ns]'], width, log=True, label='Total Sleep', color=sleep_colors)
res_bar = ax.barh(sorted_data['C-State'], sorted_data['Residency']*1000*sorted_data['Entries'], width/3, log=True, label='Total Residency', color=res_colors)

# format axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#for c in ax.containers:
#    ax.bar_label(c, fmt='{:,.0f}')
#ax.bar_label(sleep_bar, fmt='{:,.0f}')
#ax.bar_label(res_bar, label_type='edge', fmt='{:,.0f}')


plt.xlabel('Time [ns]')
plt.ylabel('C-State')
plt.legend()

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
