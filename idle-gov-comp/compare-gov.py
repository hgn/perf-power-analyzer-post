#!/usr/bin/env python3

'''
This module defines a metric used for comparing idle-governors.

For input it uses the data collected by the perf-power module.
'''

import pandas as pd
import utils


GOVS = ['ladder', 'menu', 'teo']
EVENT_FILE = 'idle-governor-events.txt'
RES_FILE = 'c-state-idle-residency.json'
PERFORMANCE_FILE = 'idle-governor-performance.json'
ABOVE_PEN_WEIGHT = 10
BELOW_PEN_WEIGHT = 1


def simple_perf(gov_data : pd.DataFrame, cstate : str):
    '''Returns the estimated performance of an idle-governor'''
    gov_data = gov_data[gov_data['C-State'] == cstate].reset_index(drop=True)
    if len(gov_data) == 0:
        return None
    perf = 0
    for _, row in gov_data.iterrows():
        if row['Miss'] == 1:
            if row['Below'] == '0':
                perf -= ABOVE_PEN_WEIGHT
            else:
                perf -= BELOW_PEN_WEIGHT
        else:
            perf += 1
    perf = perf / len(gov_data)
    return perf


def extended_perf(gov_data : pd.DataFrame, res : dict, cstate : str):
    '''Returns the estimated performance of an idle-governor
    The extended version utilizes the delta of the sleep and the residency bounds'''
    gov_data = gov_data[gov_data['C-State'] == cstate].reset_index(drop=True)
    if len(gov_data) == 0:
        return None
    perf = 0
    for _, row in gov_data.iterrows():
        if row['Miss'] == 1:
            prev_res = utils.find_res(res, cstate, False)
            next_res = utils.find_res(res, cstate, True)
            target_res = utils.find_res(res, cstate)
            weight = (BELOW_PEN_WEIGHT if row['Below'] == '1' else ABOVE_PEN_WEIGHT)
            pen = utils.normalize(row['Sleep[ns]'], prev_res, next_res, target_res, weight)
            perf += (1 - pen)
        else:
            perf += 1
    perf = perf / len(gov_data)
    return perf


def main():
    perf = []
    for gov in GOVS:
        #gov_data = read_gov(f'{gov}/{EVENT_FILE}')
        gov_data = utils.read_gov(f'examples/{EVENT_FILE}')
        res = utils.read_json(f'examples/{RES_FILE}')
        cstates = gov_data['C-State'].unique()
        for cstate in cstates:
            perf_simple = simple_perf(gov_data, cstate)
            perf_extended = extended_perf(gov_data, res, cstate)
            perf.append({'Idle-Governor' : gov, 'C-State' : cstate,
                         'Perf-Simple' : perf_simple,
                         'Perf-Extended' : perf_extended,
                         'Occurences' : len(gov_data[gov_data['C-State'] == cstate])})
            extended_perf(gov_data, res, cstate)
        occ_total = sum(entry['Occurences'] for entry in perf if entry.get('Idle-Governor') == gov)
        perf_simple_total = sum(entry['Perf-Simple']*entry['Occurences']/occ_total
                                for entry in perf if entry.get('Idle-Governor') == gov)
        perf_extended_total = sum(entry['Perf-Extended']*entry['Occurences']/occ_total
                                for entry in perf if entry.get('Idle-Governor') == gov)
        perf.append({'Idle-Governor' : gov, 'C-State' : 'all',
                     'Perf-Simple' : perf_simple_total,
                     'Perf-Extended' : perf_extended_total,
                     'Occurences' : occ_total})
    utils.save_json(perf, f'examples/{PERFORMANCE_FILE}')


if __name__ == '__main__':
    main()
