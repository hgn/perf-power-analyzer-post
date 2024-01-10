#!/usr/bin/python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.basename(__file__).rstrip('.py')
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

colors = iter([plt.cm.tab10(i) for i in range(20)])
lineprops = {"linewidth": 1, "edgecolor": "white"}

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['CPU', 'Sleep[ns]'])

plt.figure(figsize=(40,8))
for cpu in df['CPU'].unique():
    sleep_data = (df.loc[df['CPU']==cpu])
    plt.scatter(range(0,len(sleep_data.index)), sleep_data['Sleep[ns]'], alpha=0.3, label=f'CPU{cpu}', c=[next(colors)])


plt.xlabel('Sequence')
plt.ylabel('Sleep [ns]')
plt.yscale('log')
plt.legend()

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
