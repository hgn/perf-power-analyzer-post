#!/usr/bin/python3

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

df = pd.read_csv(FILE_DATA, delim_whitespace=True)

# Filter for process with PID -1
df = df[df['PID'] == -1]
#df = df[df['CPU'] == 0]

df['RoundedTime'] = df['Time'].round()
grouped = df.groupby(['RoundedTime', 'Function']).size().reset_index(name='EventCount')


total_events_by_function = grouped.groupby('Function')['EventCount'].sum().sort_values(ascending=False)
functions_to_include = total_events_by_function[total_events_by_function > 1].index
filtered_grouped = grouped[grouped['Function'].isin(functions_to_include)]
full_range = np.arange(df['RoundedTime'].min(), df['RoundedTime'].max() + 1)
#pivot_df = filtered_grouped.pivot(index='RoundedTime', columns='Function', values='EventCount')


pivot_df = filtered_grouped.pivot(index='RoundedTime', columns='Function', values='EventCount')

pivot_df = pivot_df.reindex(full_range, fill_value=0)

plt.rcParams.update({'font.size': 6})
fig, ax = plt.subplots(figsize=(15, 8))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.xaxis.grid(which='major', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.xaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.yaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.set_axisbelow(True)
ax.ticklabel_format(style='plain')

ax.stackplot(pivot_df.index, *[pivot_df[function] for function in functions_to_include], 
             labels=total_events_by_function.index)

ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Number of Events')
ax.legend(title='Kernel Function Name', loc='upper left')

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
