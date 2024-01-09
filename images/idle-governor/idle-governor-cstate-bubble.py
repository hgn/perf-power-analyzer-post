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

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Miss', 'Below', 'Sleep[ns]', 'CPU'])
df = df.replace(to_replace='-', value=0)
df['Below'] = pd.to_numeric(df['Below'], errors='coerce', downcast='integer')

grouped_data = df.groupby(by=['C-State', 'CPU']).agg({'Miss' : 'sum', 'Below' : 'sum', 'C-State' : 'size', 'Sleep[ns]' : 'sum'})
grouped_data = grouped_data.rename(columns={'C-State': 'Entries'}).reset_index()
grouped_data['Above'] = grouped_data['Miss'] - grouped_data['Below']
grouped_data['Match'] = grouped_data['Entries'] - grouped_data['Miss']
grouped_data = grouped_data.drop(columns = ['Miss', 'Entries'])


for cpu in df['CPU'].unique():
    sleep_data = (df.loc[df['CPU']==cpu])
    sleep_data['norm_sleep'] = (sleep_data['Sleep[ns]']-sleep_data['Sleep[ns]'].min()) / (sleep_data['Sleep[ns]'].max() - sleep_data['Sleep[ns]'].min())
    plt.scatter(range(0,len(sleep_data.index)), sleep_data['C-State'], s=100**sleep_data['norm_sleep'], alpha=0.3, label=f'CPU{cpu}', c=[next(colors)])

plt.xlabel('Sequence')
plt.ylabel('Sleep [ns]')
plt.legend()


print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
