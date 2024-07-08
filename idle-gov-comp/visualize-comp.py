#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import utils


BASE_FOLDER = 'examples/'
VIS_FOLDER = BASE_FOLDER + 'visualization/'
GOVS = ['ladder', 'menu', 'teo', 'eagle']
COLORS = ['g', 'deeppink', 'dodgerblue', 'y']
LINE_STYLES = [':', '--', '-.']
COMP_METRIC = 'Perf-Extended'


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
        sns.kdeplot(perf_df.loc[perf_df['Idle-Governor'] == gov, COMP_METRIC],
                    fill=True, color=col, label=gov, alpha=.4)
    plt.title('Density Plot of ' + COMP_METRIC + ' Grouped by Idle-Governors', fontsize=22)
    plt.legend()


@save
def line_plot(perf_df : pd.DataFrame, file_name : str = 'line'):
    '''Generates a line plot in the plt environment'''
    perf_df = perf_df[perf_df['C-State'] != 'all']
    perf_df = perf_df.iloc[perf_df['C-State'].apply(utils.cstate_key).argsort()]
    for col, gov, line_style in zip(COLORS,GOVS, LINE_STYLES):
        sns.lineplot(perf_df.loc[perf_df['Idle-Governor'] == gov], x='C-State', y=COMP_METRIC, alpha=.4, linestyle=line_style)


@save
def scatter_plot(perf_df : pd.DataFrame, file_name : str = 'scatter'):
    '''Generates a scatter plot in the plt environment'''
    perf_df = perf_df[perf_df['C-State'] != 'all']
    perf_df = perf_df.iloc[perf_df['C-State'].apply(utils.cstate_key).argsort()]
    sns.scatterplot(x='C-State', y=COMP_METRIC, hue='Idle-Governor', size='Occurences',
                    sizes=(10, 200), palette=COLORS, data=perf_df, alpha=0.4)


@save
def bar_plot(perf_df: pd.DataFrame, file_name: str = 'bar_plot'):
    '''Generates a bar plot in the plt environment'''
    plt.figure(figsize=(10, 6))
    sorted_perf_df = perf_df.sort_values(by=COMP_METRIC, ascending=False)
    sns.barplot(x='Idle-Governor', y=COMP_METRIC, data=sorted_perf_df, palette='viridis')
    plt.xlabel('Approach')
    plt.ylabel('Performance Score')
    plt.title('Performance Scores of Different Approaches')
    plt.xticks(rotation=45)
    plt.ylim(0, 1)  # Assuming scores are normalized between 0 and 1


@save
def line_plot_2(perf_df: pd.DataFrame, file_name: str = 'line_plot_2'):
    '''Generates a line plot in the plt environment'''
    plt.figure(figsize=(12, 8))
    for approach, group in perf_df.groupby('Idle-Governor'):
        sns.lineplot(x='C-State', y=COMP_METRIC, data=group, marker='o', label=approach)

    plt.xlabel('C-State')
    plt.ylabel('Performance Score')
    plt.legend()
    plt.ylim(0, 1)  # Assuming scores are normalized between 0 and 1
    plt.grid(True)


@save
def heatmap(perf_df: pd.DataFrame, file_name: str = 'heatmap'):
    '''Generates a heatmap in the plt environment'''
    pivot_df = perf_df.pivot('Idle-Governor', 'C-State', COMP_METRIC)

    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_df, annot=True, cmap='coolwarm', cbar=True, vmin=0, vmax=1)
    plt.xlabel('C-State')
    plt.ylabel('Approach')
    plt.title('Heatmap of Performance Scores')


def main():
    '''Generates and saves plots'''
    if not os.path.isdir(VIS_FOLDER):
        os.mkdir(VIS_FOLDER)
    perf_df = pd.DataFrame(utils.read_json(BASE_FOLDER + 'idle-governor-performance.json'))
    density_plot(perf_df, 'density')
    line_plot(perf_df, 'line')
    scatter_plot(perf_df, 'scatter')
    bar_plot(perf_df, 'bar')
    line_plot_2(perf_df, 'line_plot_2')
    heatmap(perf_df, 'heatmap')


if __name__ == '__main__':
    main()
