#!/usr/bin/python3

import os
import pandas as pd
import matplotlib.pyplot as plt

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

lineprops = {"linewidth": 1, "edgecolor": "white"}

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]'])
grouped_data = df.groupby('C-State')['Sleep[ns]'].sum().reset_index()

largest_i = grouped_data.nlargest(2, 'Sleep[ns]').index
without_largest = grouped_data.drop(largest_i)

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

labels_first = grouped_data['C-State']
axs[0].pie(grouped_data['Sleep[ns]'],
           startangle=90, wedgeprops=lineprops, labels=labels_first)# pctdistance=1.15)# explode=explode_arr)

labels_scnd = without_largest['C-State']
axs[1].pie(without_largest['Sleep[ns]'],
           startangle=90, wedgeprops=lineprops, labels=labels_scnd)

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
