#!/usr/bin/env python3

'''
This module defines a metric used for comparing idle-governors.

For input it uses the data collected by the perf-power module.
'''

import json
import pandas as pd


GOVS = ['ladder', 'menu', 'teo']
EVENT_FILE = 'idle-governor-events.txt'
RES_FILE = 'c-state-idle-residency.json'
PERFORMANCE_FILE = 'idle-governor-performance.json'
ABOVE_PEN_WEIGHT = 10
BELOW_PEN_WEIGHT = 1


def read_gov(file_name : str):
    '''Reads a csv and returns a pandas dataframe'''
    gov_data = pd.read_csv(file_name, delim_whitespace=True,
                      usecols=['C-State', 'Sleep[ns]', 'Miss', 'Below'])
    return gov_data


def read_json(file_name : str):
    '''Reads a JSON file and returns the data'''
    with open(file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def save_perf(data : list, file_name : str):
     with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)


def calc_perf(gov_data : pd.DataFrame, res : dict, cstate : str):
    '''Returns the estimated performance of an idle-governor'''
    gov_data = gov_data[gov_data['C-State'] == cstate].reset_index(drop=True)
    if len(gov_data) == 0:
        return None
    perf = 0
    for _, row in gov_data.iterrows():
        if row['Miss'] == 1:
            if row['Below'] == 0:
                perf -= ABOVE_PEN_WEIGHT
            else:
                perf -= BELOW_PEN_WEIGHT
        else:
            perf += 1
    perf = perf / len(gov_data)
    return perf


def main():
    perf = []
    for gov in GOVS:
        #gov_data = read_gov(f'{gov}/{EVENT_FILE}')
        gov_data = read_gov(f'{EVENT_FILE}')
        res = read_json(RES_FILE)
        cstates = gov_data['C-State'].unique()
        for cstate in cstates:
            perf.append({'Idle-Governor' : gov, 'C-State' : cstate,
                         'Perf' : calc_perf(gov_data, res, cstate)})

        perf_total = sum(entry['Perf'] for entry in perf if entry.get('Idle-Governor') == gov)
        perf.append({'Idle-Governor' : gov, 'C-State' : 'all',
                     'Perf' : perf_total})
    save_perf(perf, PERFORMANCE_FILE)


if __name__ == '__main__':
    main()
