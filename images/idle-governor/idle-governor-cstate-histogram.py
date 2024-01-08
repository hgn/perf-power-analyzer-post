#!/usr/bin/env python3
#
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.basename(__file__).rstrip('.py')
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"


# Import Data
df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Miss'])

# Prepare data
grouped_data = df.loc[:, ['C-State', 'Miss']].groupby('Miss')
vals = [df['C-State'].values.tolist() for i, df in grouped_data]

fig, ax = plt.subplots()
bars = ax.barh(grouped_data['C-State'], sorted_data['Sleep[ns]'], log=True)

# Format axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_yticklabels(['{:,}'.format(int(x)) for x in ax.get_yticks().tolist()])

for bar in bars:
    width = bar.get_width()
    label_x_pos = width + (width * 0.05)  # Adding 5% of the width as padding
    ax.text((label_x_pos, bar.get_y() + bar.get_height() / 2, f'{int(width)}',
            va='center', ha='left').format

plt.xlabel('C-State')
plt.ylabel('Entered')
plt.legend(['Match', 'Miss'], loc='best')
#plt.xticks(ticks=bins, labels=np.unique(df['C-State']).tolist(), rotation=90, horizontalalignment='left')

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
