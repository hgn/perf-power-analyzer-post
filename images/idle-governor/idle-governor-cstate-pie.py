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

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]'])
grouped_data = df.groupby('C-State')['Sleep[ns]'].sum()

def label_print(pct, allvals):
    absolute = int(round(pct/100.*sum(allvals)))
    return "{:.1f}%\n({:d})".format(pct, absolute)

fig, ax = plt.subplots(figsize=(5, 5))
ax.pie(grouped_data, labels=grouped_data.index,
        autopct=lambda pct: label_print(pct, grouped_data),
        startangle=90, colors=colors, wedgeprops=lineprops)
ax.axis('equal')

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
