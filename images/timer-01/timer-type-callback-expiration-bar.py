#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

import pandas as pd
import matplotlib.pyplot as plt

def load_kallsyms():
    """Load /proc/kallsyms into a dictionary mapping addresses to function names."""
    kallsyms = {}
    with open('/proc/kallsyms', 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 3:
                address, typ, name = parts[:3]
                kallsyms[address] = name
    return kallsyms

def get_function_name(address, kallsyms):
    """Return the function name for a given address."""
    return kallsyms.get(address, address)

# Load kallsyms
kallsyms = load_kallsyms()

# Path to the file
file_path = 'timer-type-callback-expiration-bar.txt'

# Read data from file
df = pd.read_csv(file_path, delim_whitespace=True)

df['Callback'] = df['Callback'].apply(lambda x: get_function_name(x, kallsyms))

# Group by TimerType and Callback, and sum the Expires values
grouped_data = df.groupby(['TimerType', 'Callback'])['Expires'].sum().reset_index()

# Creating labels for the bar chart by combining TimerType and Callback
grouped_data['Label'] = grouped_data['TimerType'] + ": " + grouped_data['Callback']

# Sort the data by Expires in descending order
sorted_data = grouped_data.sort_values(by='Expires', ascending=False)

# Creating a sorted 90% rotated bar chart with logarithmic scale
fig, ax = plt.subplots()
bars = ax.barh(sorted_data['Label'], sorted_data['Expires'], log=True)

for bar in bars:
    width = bar.get_width()
    label_x_pos = width + (width * 0.05)  # Adding 5% of the width as padding
    ax.text(label_x_pos, bar.get_y() + bar.get_height() / 2, f'{int(width)}', 
            va='center', ha='left')

plt.title('Timer Counts by Type and Callback')
plt.xlabel('Expires Count (Log Scale)')
plt.ylabel('Timer Type and Callback')
plt.gca().invert_yaxis()  # Invert y-axis to have higher numbers at the top
plt.show()


#  # since column <n>, the data starts
#  DATA_COLUMN = 2
#  
#  data = pd.read_csv("timer-type-callback-expiration.txt", sep='\s+', header=0)
#  max_value = data.iloc[:, DATA_COLUMN:].max().max()
#  data = data.head(30)
#  no_tasks = data.shape[0]
#  
#  fig, axs = plt.subplots(no_tasks, 1, sharex=True, figsize=(30, 20))
#  for i, data in enumerate(data.iterrows()):
#      index, row = data
#      irq_no = row.iloc[0]
#      irq_name = row.iloc[1]
#      row_mean = row.iloc[DATA_COLUMN:].mean()
#      row_max = row.iloc[DATA_COLUMN:].max()
#      reshaped_array = np.array(row.iloc[DATA_COLUMN:].tolist()).reshape((1, -1))
#      im = axs[i].imshow(reshaped_array, cmap=plt.cm.viridis_r, extent=[0, 10, 0, 10],
#                         aspect='auto', interpolation='none', vmin=0, vmax=max_value)
#      # I use TeX here for boldface font generatiom, remove textbf and usetex=False
#      # to get rid of it
#      text = f"\\textbf{{{irq_name } - {irq_no}}}\nMean:{row_mean:.1f}  Max:{row_max}"
#      axs[i].text(-1, 5, text, multialignment='left', va='center', ha='left', fontsize=12, usetex=True)
#  
#  # add colorbar legend
#  cbar_ax = fig.add_axes([0.95, 0.1, 0.03, 0.8])
#  cbar = fig.colorbar(im, cax=cbar_ax)
#  
#  # remove borders and make is look more modern
#  for ax in axs:
#      ax.set_xticks([])
#      ax.set_yticks([])
#      ax.set_xticklabels([])
#      ax.set_yticklabels([])
#      ax.spines['top'].set_visible(False)
#      ax.spines['right'].set_visible(False)
#      ax.spines['bottom'].set_visible(False)
#      ax.spines['left'].set_visible(False)
#  
#  
#  plt.savefig('wakeups-timemap-irq.pdf')
#  plt.savefig('wakeups-timemap-irq.png')
