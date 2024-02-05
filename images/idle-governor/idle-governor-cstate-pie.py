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

lineprops = {"linewidth": 1, "edgecolor": "white"}

# Alphanumeric sort for C-States
def cstate_key(cstate):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', str(cstate))]

def label_print(pct, allvals):
    return str(round(pct/100.*sum(allvals)))

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State'])
grouped_data = df.groupby('C-State')['C-State'].count().reset_index(name='Entries')
grouped_data = grouped_data.iloc[grouped_data['C-State'].apply(cstate_key).argsort()]
colors = plt.get_cmap('Paired')(np.linspace(0, 1, len(grouped_data)))

fig, ax = plt.subplots(figsize=(5, 5))

labels = grouped_data['C-State']
total_entries = grouped_data['Entries'].sum()
threshold = (20 * total_entries) / 100
explode_arr = [0.05 if dat < threshold else 0 for dat in grouped_data['Entries']]
ax.pie(grouped_data['Entries'],
        autopct=lambda pct: label_print(pct, grouped_data['Entries']),
        wedgeprops=lineprops, pctdistance=1.1, explode=explode_arr, colors=colors)
ax.axis('equal')
plt.legend(labels, loc='upper center', bbox_to_anchor=(1, 0, 0.5, 1), ncol=2)

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
