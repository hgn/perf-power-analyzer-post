#!/usr/bin/python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Miss', 'Below'])
df = df.replace(to_replace='-', value=0)
df['Below'] = pd.to_numeric(df['Below'], errors='coerce')

grouped_data = df.groupby(by='C-State').agg({'Miss' : 'sum', 'Below' : 'sum', 'C-State' : 'size'})
grouped_data = grouped_data.rename(columns={'C-State': 'Entries'}).reset_index()

def cstate_key(cstate):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', cstate)]

grouped_data = grouped_data.iloc[grouped_data['C-State'].apply(cstate_key).argsort()].reset_index()

grouped_data['Above'] = grouped_data['Miss'] - grouped_data['Below']
grouped_data['Match'] = grouped_data['Entries'] - grouped_data['Miss']
grouped_data['Above_perc'] = 100 * grouped_data['Above'] / grouped_data['Entries']
grouped_data['Match_perc'] = 100 * grouped_data['Match'] / grouped_data['Entries']
grouped_data['Below_perc'] = 100 * grouped_data['Below'] / grouped_data['Entries']
grouped_data = grouped_data.drop(columns = ['Miss'])

fig, ax = plt.subplots()
bars_above = ax.bar(grouped_data['C-State'], grouped_data['Above_perc'], color= '#e15353')
bars_match = ax.bar(grouped_data['C-State'], grouped_data['Match_perc'], bottom=grouped_data['Above_perc'], color='#79ff66')
bars_below = ax.bar(grouped_data['C-State'], grouped_data['Below_perc'], bottom=(grouped_data['Above_perc'] + grouped_data['Match_perc']), color='#ffab66')

FONTSIZE = 8

for i, bar_above in enumerate(bars_above):
    if grouped_data['Above'][i] > 0:
        height=bar_above.get_height()
        ax.text(bar_above.get_x() + bar_above.get_width() / 2, bar_above.get_y() + bar_above.get_height() / 2, grouped_data['Above'][i],
                va='center', ha='center', fontsize=FONTSIZE)

for i, bar_match in enumerate(bars_match):
    if grouped_data['Match'][i] > 0:
        height=bar_match.get_height()
        ax.text(bar_match.get_x() + bar_match.get_width() / 2, bar_match.get_y() + bar_match.get_height() / 2, grouped_data['Match'][i],
                va='center', ha='center', fontsize=FONTSIZE)

for i, bar_below in enumerate(bars_below):
    if grouped_data['Below'][i] > 0:
        height=bar_below.get_height()
        ax.text(bar_below.get_x() + bar_below.get_width() / 2, bar_below.get_y() + bar_below.get_height() / 2, grouped_data['Below'][i],
                va='center', ha='center', fontsize=FONTSIZE)

# Format axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


plt.xlabel('C-State')
plt.ylabel('Percentage')
plt.legend(['Above\n(Too Deep)', 'Ideal', 'Below\n(Too Shallow)'], loc='upper center', bbox_to_anchor=(0.87, 0, 0.5, 1))

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
