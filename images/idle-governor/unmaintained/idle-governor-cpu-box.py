#!/usr/bin/python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

colors = iter([plt.cm.tab10(i) for i in range(20)])
lineprops = {"linewidth": 1, "edgecolor": "white"}


df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['CPU', 'Sleep[ns]'])

columns = []
positions = []
for cpu in df['CPU'].unique():
    sleep_data = df[df['CPU']==cpu]['Sleep[ns]']
    columns.append(sleep_data)
    positions.append(cpu)

plt.boxplot(columns, positions=positions, showfliers=False, showmeans=True, meanline=True)

plt.title('Does not plot outliers!')
plt.xlabel('CPU')
plt.ylabel('Sleep [ns]')
plt.yscale('log')

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
