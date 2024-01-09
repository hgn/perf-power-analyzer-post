#!/usr/bin/python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.basename(__file__).rstrip('.py')
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

colors = ['#3498db', '#e74c3c']
lineprops = {"linewidth": 1, "edgecolor": "white"}

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Miss', 'Below'])
df = df.replace(to_replace='-', value=0)
df['Below'] = pd.to_numeric(df['Below'], errors='coerce', downcast='integer')

#grouped_data = df.groupby(by=['C-State']).sum().reset_index()

grouped_data = df.groupby(by='C-State').agg({'Miss' : 'sum', 'Below' : 'sum', 'C-State' : 'size'})
grouped_data = grouped_data.rename(columns={'C-State': 'Entries'}).reset_index()
grouped_data['Above'] = grouped_data['Miss'] - grouped_data['Below']
grouped_data['Match'] = grouped_data['Entries'] - grouped_data['Miss']
grouped_data = grouped_data.drop(columns = ['Miss', 'Entries'])


# Creating a sorted 90% rotated bar chart
fig, ax = plt.subplots()
bars_match = ax.bar(grouped_data['C-State'], grouped_data['Match'])
bars_above = ax.bar(grouped_data['C-State'], grouped_data['Above'], bottom=grouped_data['Match'])
bars_below = ax.bar(grouped_data['C-State'], grouped_data['Below'], bottom=(grouped_data['Match'] + grouped_data['Above']))

# Format axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

"""
for bar_match, bar_above, bar_below in bars_match, bars_above, bars_below:
    ax.text(label_x_pos, bar_match.get_y() + bar_match.get_height() / 2, f'{int(width)}',
            va='center', ha='left')
"""

plt.xlabel('C-State')
plt.ylabel('Entries')
plt.legend(['Match', 'Above', 'Below'])

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
