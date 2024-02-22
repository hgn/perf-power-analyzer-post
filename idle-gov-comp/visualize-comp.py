#!/usr/bin/env python3

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import utils

df = pd.DataFrame(utils.read_json('examples/idle-governor-performance.json'))

df = df[df['C-State'] != 'all']
plt.figure(figsize=(16,10), dpi= 80)
print(df.loc[df['Idle-Governor'] == 'ladder', 'Perf-Extended'])
sns.kdeplot(df.loc[df['Idle-Governor'] == 'ladder', 'Perf-Extended'], fill=True, color='g', label='ladder', alpha=.2)
sns.kdeplot(df.loc[df['Idle-Governor'] == 'teo', 'Perf-Extended'], fill=True, color='deeppink', label='teo', alpha=.2)
sns.kdeplot(df.loc[df['Idle-Governor'] == 'menu', 'Perf-Extended'], fill=True, color='dodgerblue', label='menu', alpha=.2)

plt.title('Density Plot of Perf-Extended Grouped by Idle-Governors', fontsize=22)
plt.legend()
plt.show()
