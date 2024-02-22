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


def save_json(data : list, file_name : str):
    '''Saves the data into a JSON'''
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)


def unique_res(residencies, target_cpu=0):
    res_dict = residencies[list(residencies.keys())[target_cpu]]
    res = set()
    for state in res_dict.values():
        res.add(state['residency'])
    res = sorted([int(x) for x in res])
    return res


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


def find_res(res : list, cstate : str, below : bool = None, target_cpu : int = 0):
    '''Returns the residency time in ns below or above the cstate
    If target is True then below is ignored and the res in ns corresponding to the
    cstate is returned'''
    res_dict = res[list(res.keys())[target_cpu]]
    res = unique_res(res)
    target_res = None

    for res_state in res_dict.values():
        if cstate == res_state['name']:
            target_res = int(res_state['residency'])
            break

    if below is None:
        return (target_res * 1000)

    index = res.index(int(target_res))
    if not below:
        return (res[index - 1] * 1000) if index > 0 else 0
    return (res[index + 1] * 1000) if index < len(res) - 1 else res[index]


def normalize(time : int, prev_res : int, next_res : int, target_res : int, weight : int):
    '''Normalizes a delta time according to the correspoding residency time'''
    # Still need this for the case, that the slight offset defines it below or above the bound,
    # even though the sleep time does not validate it
    # TODO: check if this can be None
    data_min = min(time, prev_res, next_res)
    data_max = max(time, prev_res, next_res)

    # TODO: this does not account for above / below (time - data_min)
    normalized_value = (time - data_min) / (data_max - data_min)
    scale_factor = (next_res - prev_res) / (data_max - data_min)
    return scale_factor * normalized_value


def extended_perf(gov_data : pd.DataFrame, res : dict, cstate : str):
    '''Returns the estimated performance of an idle-governor
    The extended version utilizes the delta of the sleep and the residency bounds'''
    gov_data = gov_data[gov_data['C-State'] == cstate].reset_index(drop=True)
    if len(gov_data) == 0:
        return None
    perf = 0
    for _, row in gov_data.iterrows():
        if row['Miss'] == 1:
            prev_res = find_res(res, cstate, False)
            next_res = find_res(res, cstate, True)
            target_res = find_res(res, cstate)
            weight = (BELOW_PEN_WEIGHT if row['Below'] == '1' else ABOVE_PEN_WEIGHT)
            pen = normalize(row['Sleep[ns]'], prev_res, next_res, target_res, weight)
            perf += (1 - pen)
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
    save_json(perf, PERFORMANCE_FILE)


if __name__ == '__main__':
    main()
