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

df = pd.read_csv(FILE_DATA, delim_whitespace=True, usecols=['C-State', 'Miss', 'Below', 'Sleep[ns]', 'CPU', 'Time-Start'])
df = df.replace(to_replace='-', value=0)
df = df.head(1000)
print("The produced visualizations only represent the first 1000 events.")

plt.figure(figsize=(40,8))
for cpu in df['CPU'].unique():
    sleep_data = (df.loc[df['CPU']==cpu])
    sleep_data['norm_sleep'] = (sleep_data['Sleep[ns]']-sleep_data['Sleep[ns]'].min()) / (sleep_data['Sleep[ns]'].max() - sleep_data['Sleep[ns]'].min())
    sleep_data['Time-Start'] = sleep_data['Time-Start'] - sleep_data['Time-Start'].min()
    plt.scatter(sleep_data['Time-Start'], sleep_data['C-State'], s=100**sleep_data['norm_sleep'], alpha=0.3, label=f'CPU{cpu}', c=[next(colors)])

plt.xlabel('Time [s]')
plt.ylabel('C-State')
plt.legend()


print(f'generate {FILE_PDF}')
plt.savefig(FILE_PDF, dpi=300, bbox_inches='tight')
print(f'generate {FILE_PNG}')
plt.savefig(FILE_PNG, dpi=300, bbox_inches='tight')
