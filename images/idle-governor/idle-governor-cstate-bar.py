#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Path to the file
file_path = 'idle-governor-cstate-bar.txt'

# Read data from file
df = pd.read_csv(file_path, delim_whitespace=True)

# Drop unneccesarry columns
df = df.drop(columns=['Time-Start', 'Delta[ns]', 'Miss', 'CPU'])

# Group by C-State and sum the sleeping times
grouped_data = df.groupby(['C-State']).sum('Sleep[ns]').reset_index()

# Creating labels for the bar chart by combining TimerType and Callback
grouped_data['Label'] = str(grouped_data['C-State'])

# Sort the data by Expires in descending order
sorted_data = grouped_data.sort_values(by='Sleep[ns]', ascending=False)

# Creating a sorted 90% rotated bar chart with logarithmic scale
fig, ax = plt.subplots()
bars = ax.barh(sorted_data['C-State'], sorted_data['Sleep[ns]'], log=True)

# format axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for c in ax.containers:
    ax.bar_label(c, fmt='{:,.0f}')

plt.xlabel('Sleep Time [ns]')
plt.ylabel('C-State')
plt.gca().invert_yaxis()
plt.savefig('idle-governor-cstate-bar.pdf')
plt.savefig('idle-governor-cstate-bar.png')
