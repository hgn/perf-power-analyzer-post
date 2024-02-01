#!/usr/bin/python3

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

lineprops = {"linewidth": 1, "edgecolor": "white"}

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]'])
grouped_data = df.groupby('C-State')['Sleep[ns]'].sum().reset_index()
grouped_data['Perc'] = (grouped_data['Sleep[ns]'] / grouped_data['Sleep[ns]'].sum()) * 100

largest_i = grouped_data.nlargest(2, 'Sleep[ns]').index
without_largest = grouped_data.drop(largest_i)

# Sum up all but the largest rows and add them to 'Others'
others_row = {'C-State' : 'Others', 'Sleep[ns]' : without_largest['Sleep[ns]'].sum()}
with_largest = grouped_data.loc[largest_i]
with_largest.loc[len(with_largest)] = others_row
with_largest['Perc'] = (with_largest['Sleep[ns]'] / with_largest['Sleep[ns]'].sum()) * 100

colors1 = plt.get_cmap('Pastel2')(np.linspace(0, 1, len(grouped_data['C-State'])))
colors2 = plt.get_cmap('Pastel1')(np.linspace(0, 1, len(grouped_data['C-State'])))

fig, axs = plt.subplots(1, 2, figsize=(10, 30))

# Left pie chart with all States
labels_first = with_largest['C-State'] + ' (' + with_largest['Perc'].round(2).astype(str) + '%)'
axs[0].pie(with_largest['Sleep[ns]'],
           startangle=0, wedgeprops=lineprops, labels=labels_first, colors=colors1)

# Right pie chart without the 2 longest sleeping C-States
labels_scnd = without_largest['C-State'] + ' (' + without_largest['Perc'].round(2).astype(str) + '%)'
axs[1].pie(without_largest['Sleep[ns]'],
           startangle=90, wedgeprops=lineprops, labels=labels_scnd, radius=0.8, colors=colors2)
plt.title('Subset \'Others\'', y=0.06)

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
