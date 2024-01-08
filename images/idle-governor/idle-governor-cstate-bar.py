#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Path to the file
file_path = 'idle-governor-cstate-bar.txt'

# Read data from file
df = pd.read_csv(file_path, delim_whitespace=True)

# Drop unneccesarry columns
df = df.drop(columns=['Time-Start'])
df = df.drop(columns=['Delta[ns]'])
df = df.drop(columns=['Miss'])
df = df.drop(columns=['CPU'])

# Group by C-State CPU and sum the sleeping times
#grouped_data = df.groupby(['C-State', 'CPU']).sum('Sleep[ns]').reset_index()
# Group by C-State and sum the sleeping times
grouped_data = df.groupby(['C-State']).sum('Sleep[ns]').reset_index()
print(grouped_data)

# Creating labels for the bar chart by combining TimerType and Callback
#grouped_data['Label'] = str(grouped_data['C-State']) + ": " + str(grouped_data['CPU'])
# Creating labels for the bar chart by combining TimerType and Callback
grouped_data['Label'] = str(grouped_data['C-State'])

# Sort the data by Expires in descending order
sorted_data = grouped_data.sort_values(by='Sleep[ns]', ascending=False)

# Creating a sorted 90% rotated bar chart with logarithmic scale
fig, ax = plt.subplots()
bars = ax.barh(grouped_data['C-State'], sorted_data['Sleep[ns]'], log=True)

# Format axes
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar in bars:
    width = bar.get_width()
    label_x_pos = width + (width * 0.05)  # Adding 5% of the width as padding
    ax.text(label_x_pos, bar.get_y() + bar.get_height() / 2, f'{int(width)}',
            va='center', ha='left')

plt.xlabel('Sleep Time [ns]')
plt.ylabel('C-State')
plt.savefig('idle-governor-cstate-bar.pdf')
plt.savefig('idle-governor-cstate-bar.png')
