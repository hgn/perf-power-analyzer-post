#!/usr/bin/python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Sleep[ns]'])

columns = []
labels = []
for cstate in df['C-State'].unique():
    sleep_data = df[df['C-State']==cstate]['Sleep[ns]']
    columns.append(sleep_data)
    labels.append(cstate)

plt.boxplot(columns, labels=labels, showfliers=False, showmeans=True, meanline=True)

plt.title('Does not plot outliers!')
plt.xlabel('C-State')
plt.ylabel('Sleep [ns]')
plt.yscale('log')

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
