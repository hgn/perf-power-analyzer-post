#!/usr/bin/python3

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.basename(__file__).rstrip('.py')
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

markers = ['o', 's', '^', 'v', '*', '+', 'x', 'D']
marker_iter = iter(markers)


timer_events = []
with open(FILE_DATA, 'r') as file:
    for line in file:
        parts = line.split()
        pid, process_name = parts[:2]
        timers = parts[2:]
        for timer in timers:
            timer_type, timer_func, time_str = timer.split(':')
            time = round(float(time_str))  # round to the nearest second
            timer_events.append({'PID': int(pid), 'ProcessName': process_name, 'TimerType': timer_type, 'TimerFunc': timer_func, 'Time': time})

# Create DataFrame
df = pd.DataFrame(timer_events)
#df = df[(df['PID'] > 100)]

# Group by ProcessName and Time and count occurrences
timer_counts = df.groupby(['ProcessName', 'Time']).size().reset_index(name='Count')

marker_size = 2
line_width = .7
plt.rcParams.update({'font.size': 6})

fig, ax = plt.subplots(figsize=(10, 6))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.xaxis.grid(which='major', linestyle='-', linewidth='0.5', color='#bbbbbb')
ax.xaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.yaxis.grid(which='major', linestyle='-', linewidth='0.5', color='#bbbbbb')
ax.yaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.set_axisbelow(True)
ax.ticklabel_format(style='plain')



# Group by ProcessName and count timer events
timer_event_counts = df.groupby('ProcessName').size()

# Filter out processes with fewer than 100 timer events
processes_with_100_or_more_events = timer_event_counts[timer_event_counts >= 300].index
df_filtered = df[df['ProcessName'].isin(processes_with_100_or_more_events)]

# Group by ProcessName and Time and count occurrences
timer_counts = df_filtered.groupby(['ProcessName', 'Time']).size().reset_index(name='Count')


for process_name, group in timer_counts.groupby('ProcessName'):
    # Extracting x and y values
    x_values = group['Time']
    y_values = group['Count']

    # Plotting using Matplotlib's ax.plot()
    marker = next(marker_iter, 'o')
    ax.plot(x_values, y_values, marker=marker, linestyle='-',
            markersize=marker_size, linewidth=line_width, label=process_name)

ax.set_yscale('log')

ax.set_xlabel('Time')
ax.set_ylabel('Process ID')
ax.legend()

# Save the plot as PDF and PNG
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')

#  # Read and parse the file
#  timer_events = []
#  with open(FILE_DATA, 'r') as file:
#      for line in file:
#          parts = line.split()
#          pid, process_name = parts[:2]
#          timers = parts[2:]
#          for timer in timers:
#              timer_type, timer_func, time_str = timer.split(':')
#              time = round(float(time_str))  # round to the nearest second
#              timer_events.append({'PID': int(pid), 'ProcessName': process_name, 'TimerType': timer_type, 'TimerFunc': timer_func, 'Time': time})
#  
#  # Create DataFrame
#  df = pd.DataFrame(timer_events)
#  df = df[(df['PID'] > 100)]
#  df = df[~(df['ProcessName'] == 'chromium')]
#  
#  # Plotting with native Matplotlib
#  fig, ax = plt.subplots(figsize=(10, 6))
#  
#  for process_name, group in df.groupby('ProcessName'):
#      # Extracting x and y values
#      x_values = group['Time']
#      y_values = group['Count']
#  
#      # Plotting using Matplotlib's ax.plot()
#      ax.plot(x_values, y_values, marker='o', linestyle='-', label=process_name)
#  
#  
#  # Group by ProcessName and Time and count occurrences
#  timer_counts = df.groupby(['ProcessName', 'Time']).size().reset_index(name='Count')
#  
#  # Plotting
#  fig, ax = plt.subplots(figsize=(10, 6))
#  for process_name, group in timer_counts.groupby('ProcessName'):
#      group.plot(x='Time', y='Count', ax=ax, label=process_name, marker='o', linestyle='-')
#  
#  
#  ax.set_xlabel('Time')
#  ax.set_ylabel('Process ID')
#  ax.set_title('Timer Expires Per Task')
#  ax.legend()
#  plt.show()
#  
#  
#  print(f'generate {FILE_PDF}')
#  plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
#  print(f'generate {FILE_PNG}')
#  plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
