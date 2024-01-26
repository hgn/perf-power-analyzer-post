#!/usr/bin/python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

lineprops = {"linewidth": 1, "edgecolor": "white"}

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State'])
grouped_data = df.groupby('C-State')['C-State'].count().sort_values(ascending=False)
print(grouped_data)

def label_print(pct, allvals):
    absolute = int(round(pct/100.*sum(allvals)))
    return "{:.1f}%\n({:d})".format(pct, absolute)

fig, ax = plt.subplots(figsize=(5, 5))

labels=grouped_data.index
total_entries = sum(grouped_data.values)
threshold = (20 * total_entries) / 100
explode_arr = [0.25 if dat < threshold else 0 for dat in grouped_data.values]
ax.pie(grouped_data,
        autopct=lambda pct: label_print(pct, grouped_data),
        startangle=90, wedgeprops=lineprops, pctdistance=1.15, explode=explode_arr)
ax.axis('equal')
plt.legend(labels, loc='upper center', bbox_to_anchor=(1, 0, 0.5, 1), ncol=2)

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
