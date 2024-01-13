#!/usr/bin/python3

import os
import sys
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter

FILE_BASE = os.path.basename(__file__).rstrip('.py')
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

df = pd.read_csv(FILE_DATA, delim_whitespace=True)

plt.rcParams.update({'font.size': 6})
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(18, 7), sharex=True)

ymin=0.001
ymax=15.0

scpu = 0
for cpu, ax_row in enumerate(axes):
    for sub_cpu, ax in enumerate(ax_row):

        # Filter data for CPU 1
        cpu = scpu
        cpu_df = df[df['CPU'] == cpu]

        filtered_df = cpu_df[cpu_df['Kernel-Function'] == 'tick_sched_timer']
        time_values = np.array(filtered_df['Time'])
        time_diff = np.diff(time_values)
        num_tick_sched_timer_events = len(filtered_df)

        tick_stop_df = cpu_df[(cpu_df['Event'] == 'TICK_STOP') & (cpu_df['Success'] == 1)]
        time_values_tick_stop = np.array(tick_stop_df['Time'])
        num_tick_stop_events = len(tick_stop_df)

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='#bbbbbb')
        ax.set_axisbelow(True)

        ax.set_ylim(ymin=ymin, ymax=ymax) 


        # Set x-axis as the time values and y-axis as the time differences
        sc = ax.scatter(time_values[1:], time_diff, c="red", marker='o', s=30, alpha=0.3, edgecolor='none')
        sc.set_zorder(2)

        # Add a horizontal line at y=0.004 (250Hz)
        ax.axhline(y=0.004, color='black', linewidth=0.5, linestyle='--', label='250Hz (0.004s)', zorder=1)
        ax.text(.95, 0.005, '250Hz (0.004s)', color='black', fontsize=4, verticalalignment='top', transform=ax.get_yaxis_transform())

        for x in time_values_tick_stop[1:]:
            ax.axvline(x=x, color='#bbbbbb', linestyle='-', alpha=0.3, linewidth=0.5, zorder=0)

        # Add labels and a title
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Time Difference [s]')
        ax.set_title(f'CPU {cpu} [TimerTicks: {num_tick_sched_timer_events}, TickStops: {num_tick_stop_events}]')


        # Set y-axis to logarithmic scale
        ax.set_yscale('log')
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

        scpu += 1

plt.tight_layout()

print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')










#   df = pd.read_csv(FILE_DATA, delim_whitespace=True)
#   
#   # Filter data for CPU 1
#   cpu_1_df = df[df['CPU'] == 0]
#   
#   # Filter further based on the conditions
#   filtered_df = cpu_1_df[cpu_1_df['Kernel-Function'] == 'tick_sched_timer']
#   # Convert the 'Time' column to a NumPy array
#   time_values = np.array(filtered_df['Time'])
#   # Calculate time differences between events
#   time_diff = np.diff(time_values)
#   
#   tick_stop_df = cpu_1_df[cpu_1_df['Event'] == 'TICK_STOP']
#   time_values_tick_stop = np.array(tick_stop_df['Time'])
#   
#   
#   # Create a Matplotlib figure and axis
#   plt.rcParams.update({'font.size': 6})
#   fig, ax = plt.subplots(figsize=(10, 6))
#   ax.spines["top"].set_visible(False)
#   ax.spines["right"].set_visible(False)
#   ax.yaxis.grid(which='major', linestyle=':', linewidth='0.5', color='#bbbbbb')
#   ax.set_axisbelow(True)
#   
#   ax.set_ylim(ymin=0.001, ymax=2) 
#   
#   
#   # Set x-axis as the time values and y-axis as the time differences
#   sc = ax.scatter(time_values[1:], time_diff, c="red", marker='o', s=30, alpha=0.3, edgecolor='none')
#   sc.set_zorder(2)
#   
#   # Add a horizontal line at y=0.004 (250Hz)
#   ax.axhline(y=0.004, color='black', linewidth=0.5, linestyle='--', label='250Hz (0.004s)', zorder=1)
#   
#   for x in time_values_tick_stop[1:]:
#       ax.axvline(x=x, color='#bbbbbb', linestyle='-', alpha=0.1, linewidth=0.5, zorder=0)
#   
#   # Add labels and a title
#   ax.set_xlabel('Time')
#   ax.set_ylabel('Time Difference')
#   
#   
#   # Set y-axis to logarithmic scale
#   ax.set_yscale('log')
#   ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
#   
#   
#   print(f'generate {FILE_PNG}')
#   plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
#   print(f'generate {FILE_PDF}')
#   plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
