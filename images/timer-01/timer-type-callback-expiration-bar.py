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

def load_kallsyms():
    kallsyms = {}
    with open('/proc/kallsyms', 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 3:
                address, typ, name = parts[:3]
                kallsyms[address] = name
    return kallsyms

def get_function_name(address, kallsyms):
    return kallsyms.get(address, address)

def uid0_check():
    if not os.geteuid():
        return
    print("Warning: please run as root to resolve addresses to function names",
            file=sys.stderr)

uid0_check()
kallsyms = load_kallsyms()

df = pd.read_csv(FILE_DATA, delim_whitespace=True)

df['Callback'] = df['Callback'].apply(lambda x: get_function_name(x, kallsyms))
grouped_data = df.groupby(['TimerType', 'Callback'])['Expires'].sum().reset_index()
grouped_data['Label'] = grouped_data['TimerType'] + ": " + grouped_data['Callback']
sorted_data = grouped_data.sort_values(by='Expires', ascending=False)

plt.rcParams.update({'font.size': 4})
fig, ax = plt.subplots()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.xaxis.grid(which='major', linestyle='-', linewidth='0.5', color='#bbbbbb')
ax.xaxis.grid(which='minor', linestyle=':', linewidth='0.5', color='#bbbbbb')
ax.set_axisbelow(True)
ax.ticklabel_format(style='plain')

num_bars = len(sorted_data['Expires'])
colors = plt.cm.plasma(np.linspace(0.1, 0.9, num_bars))
bars = ax.barh(sorted_data['Label'], sorted_data['Expires'], log=True, color=colors)

for bar in bars:
    width = bar.get_width()
    label_x_pos = width + (width * 0.05)
    ax.text(label_x_pos, bar.get_y() + bar.get_height() / 2, f'{int(width)}', 
            va='center', ha='left')

plt.xlabel('Expires Count (Log Scale)')
plt.ylabel('Timer Type and Kernel Callback Function')
plt.gca().invert_yaxis()

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
