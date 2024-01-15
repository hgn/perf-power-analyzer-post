#!/usr/bin/python3

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

FILE_BASE = os.path.splitext(__file__)[0]
FILE_DATA = FILE_BASE + ".txt"
FILE_PNG  = FILE_BASE + ".png"
FILE_PDF  = FILE_BASE + ".pdf"

colors = iter([plt.cm.tab20(i) for i in range(20)])

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Below', 'Miss', 'Sleep[ns]'])
# Currently checking miss is not necessary, however this may change if below gets reworked
df = df.loc[df['Miss'] == 1]
df = df.loc[df['Below'] == '0']

plt.figure(figsize=(40,8))
for cstate in df['C-State'].unique():
    sleep_data = (df.loc[df['C-State']==cstate])
    plt.scatter(range(0,len(sleep_data.index)), sleep_data['Sleep[ns]'], alpha=0.3, label=f'{cstate}', c=[next(colors)])


plt.xlabel('Sequence')
plt.ylabel('Sleep [ns]')
plt.yscale('log')
plt.legend()

print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
