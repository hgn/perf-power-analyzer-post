#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import utils


BASE_FOLDER = 'examples/'
VIS_FOLDER = BASE_FOLDER + 'visualization/'
GOVS = ['ladder', 'menu', 'teo']


def save_plt(file_base : str):
    '''Saves a plot from the plt environment to pdf and png and resets plt afterwards'''
    print(f'generate {file_base}.pdf')
    plt.savefig(file_base + '.pdf', dpi=300, bbox_inches='tight')
    print(f'generate {file_base}.png')
    plt.savefig(file_base + '.png', dpi=300, bbox_inches='tight')
    plt.clf()


def density_plot(perf_df : pd.DataFrame):
    '''Generates a density plot in the plt environment'''
    perf_df = perf_df[perf_df['C-State'] != 'all']
    colors = ['g', 'deeppink', 'dodgerblue']
    plt.figure(figsize=(16,10), dpi=300)
    for col, gov in zip(colors, GOVS):
        sns.kdeplot(perf_df.loc[perf_df['Idle-Governor'] == gov, 'Perf-Extended'],
                    fill=True, color=col, label=gov, alpha=.4)
    plt.title('Density Plot of Perf-Extended Grouped by Idle-Governors', fontsize=22)
    plt.legend()


def line_plot(perf_df : pd.DataFrame):
    '''Generates a line plot in the plt environment'''
    perf_df = perf_df[perf_df['C-State'] != 'all']
    sns.lineplot(data=perf_df, x='C-State', y='Perf-Extended', hue='Idle-Governor')


def main():
    '''Generates and saves plots'''
    if not os.path.isdir(VIS_FOLDER):
        os.mkdir(VIS_FOLDER)
    perf_df = pd.DataFrame(utils.read_json(BASE_FOLDER + 'idle-governor-performance.json'))
    density_plot(perf_df)
    save_plt(VIS_FOLDER + 'idle-gov-comp-density')
    line_plot(perf_df)
    save_plt(VIS_FOLDER + 'idle-gov-comp-line')


if __name__ == '__main__':
    main()
