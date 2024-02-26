#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import utils


BASE_FOLDER = 'examples/'
VIS_FOLDER = BASE_FOLDER + 'visualization/'
GOVS = ['ladder', 'menu', 'teo']
COLORS = ['g', 'deeppink', 'dodgerblue']


def save(plot):
    '''file_name_index has to be the index of the file_name arg for the plot function'''
    def wrapper(*args, **kwargs):
        result = plot(*args, **kwargs)
        file_name_index = 1
        file_base = VIS_FOLDER + 'idle-gov-comp-' + args[file_name_index]
        print(f'generate {file_base}.pdf')
        plt.savefig(file_base + '.pdf', dpi=300, bbox_inches='tight')
        print(f'generate {file_base}.png')
        plt.savefig(file_base + '.png', dpi=300, bbox_inches='tight')
        plt.clf()
        return result
    return wrapper


@save
def density_plot(perf_df : pd.DataFrame, file_name : str = 'density'):
    '''Generates a density plot in the plt environment'''
    perf_df = perf_df[perf_df['C-State'] != 'all']
    perf_df = perf_df.iloc[perf_df['C-State'].apply(utils.cstate_key).argsort()]
    plt.figure(figsize=(16,10), dpi=300)
    for col, gov in zip(COLORS, GOVS):
        sns.kdeplot(perf_df.loc[perf_df['Idle-Governor'] == gov, 'Perf-Extended'],
                    fill=True, color=col, label=gov, alpha=.4)
    plt.title('Density Plot of Perf-Extended Grouped by Idle-Governors', fontsize=22)
    plt.legend()


@save
def line_plot(perf_df : pd.DataFrame, file_name : str = 'line'):
    '''Generates a line plot in the plt environment'''
    perf_df = perf_df[perf_df['C-State'] != 'all']
    perf_df = perf_df.iloc[perf_df['C-State'].apply(utils.cstate_key).argsort()]
    sns.lineplot(data=perf_df, x='C-State', y='Perf-Extended', hue='Idle-Governor')


@save
def scatter_plot(perf_df : pd.DataFrame, file_name : str = 'scatter'):
    '''Generates a scatter plot in the plt environment'''
    perf_df = perf_df[perf_df['C-State'] != 'all']
    perf_df = perf_df.iloc[perf_df['C-State'].apply(utils.cstate_key).argsort()]
    sns.scatterplot(x='C-State', y='Perf-Extended', hue='Idle-Governor', size='Occurences',
                    sizes=(10, 200), palette=COLORS, data=perf_df, alpha=0.6)


def main():
    '''Generates and saves plots'''
    if not os.path.isdir(VIS_FOLDER):
        os.mkdir(VIS_FOLDER)
    perf_df = pd.DataFrame(utils.read_json(BASE_FOLDER + 'idle-governor-performance.json'))
    density_plot(perf_df, 'density')
    line_plot(perf_df, 'line')
    scatter_plot(perf_df, 'scatter')


if __name__ == '__main__':
    main()
