#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

file_path = 'timer-type-callback-expiration-pie.txt'

# Read data from file
df = pd.read_csv(file_path, delim_whitespace=True)

# Group by TimerType and sum the Expires values
grouped_data = df.groupby('TimerType')['Expires'].sum()

# Creating a pie chart
fig, ax = plt.subplots()
ax.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

plt.title('Timer Counts by Type')
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
