#!/usr/bin/env python3

"""
This module defines a metric used for comparing idle-governors.

For input it uses the data collected by the perf-power module.
"""

import pandas as pd
import utils


GOVS = ['ladder', 'menu', 'teo', 'eagle']
EVENT_FILE = 'idle-governor-events.txt'
RES_FILE = 'c-state-idle-residency.json'
PERFORMANCE_FILE = 'idle-governor-performance.json'
ABOVE_PEN_WEIGHT = 0.2
BELOW_PEN_WEIGHT = 0.95


def simple_perf(gov_data : pd.DataFrame, cstate : str):
    """Return the estimated performance of an idle-governor."""
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

def calculate_penalty(actual, target, max_val, weight, penalty_type):
    deviation = abs(actual - target)
    if penalty_type == 'above':
        if max_val == target:
            return 0
        else:
            normalized_deviation = deviation / (max_val - target)
    else:
        if target == 0:
            normalized_deviation = 0
        else:
            normalized_deviation = deviation / target

    penalty = weight * (normalized_deviation ** 2)  # Quadratic penalty
    return min(penalty, 1)  # Ensure penalty doesn't exceed 1

def calculate_performance(gov_data, res, cstate):
    gov_data = gov_data[gov_data['C-State'] == cstate].reset_index(drop=True)
    if len(gov_data) == 0:
        return None

    total_score = 0
    max_res = max(utils.unique_res(res)) * 1000

    for _, row in gov_data.iterrows():
        if row['Miss'] == 1:
            target_res = utils.find_res(res, cstate)
            next_res = utils.find_res(res, cstate, True)
            weight = BELOW_PEN_WEIGHT if row['Below'] == '1' else ABOVE_PEN_WEIGHT

            if row['Below'] == '0':
                penalty = calculate_penalty(row['Sleep[ns]'], target_res, max_res, weight, 'above')
            else:
                penalty = calculate_penalty(row['Sleep[ns]'], next_res, max_res, weight, 'below')

            score = 1 - penalty
        else:
            score = 1  # Perfect score if no miss

        total_score += score

    average_score = total_score / len(gov_data)
    return average_score

def extended_perf(gov_data : pd.DataFrame, res : dict, cstate : str):
    """Return the estimated performance of an idle-governor utilizing the delta of sleep and res."""
    gov_data = gov_data[gov_data['C-State'] == cstate].reset_index(drop=True)
    if len(gov_data) == 0:
        return None
    perf = 0.0
    #TODO: DELEEEEEEEEEEEEEEEEEEEEEEEEETE
    printy = True
    for _, row in gov_data.iterrows():
        if row['Miss'] == 1:
            prev_res = utils.find_res(res, cstate, False)
            next_res = utils.find_res(res, cstate, True)
            target_res = utils.find_res(res, cstate)
            weight = (BELOW_PEN_WEIGHT if row['Below'] == '1' else ABOVE_PEN_WEIGHT)
            max_res = (max(utils.unique_res(res)) * 1000)
            if row['Below'] == '0':
                pen = utils.normalize_above(row['Sleep[ns]'], target_res, weight)
                perf += pen
                if printy:
                    print('this is above: ' + str(pen))
                    printy = False
            else:
                pen = utils.normalize_below(row['Sleep[ns]'], max_res, next_res, weight)
                perf += pen
                if not printy:
                    print('this is below:' + str(pen))
                    printy = True
            #perf += (1 - pen)
        else:
            perf += 1.0
    perf = perf / len(gov_data)
    return perf


def main():
    """Compare all Governors in the GOVS variable."""
    perf = []
    for gov in GOVS:
        gov_data = utils.read_gov(f'examples/{gov}/{EVENT_FILE}')
        res = utils.read_json(f'examples/{gov}/{RES_FILE}')
        cstates = gov_data['C-State'].unique()
        for cstate in cstates:
            perf_simple = simple_perf(gov_data, cstate)
            perf_extended = extended_perf(gov_data, res, cstate)
            perf_v2 = calculate_performance(gov_data, res, cstate)
            perf.append({'Idle-Governor' : gov, 'C-State' : cstate,
                         'Perf-Simple' : perf_simple,
                         'Perf-Extended' : perf_extended,
                         'Perf-V2' : perf_v2,
                         'Occurences' : len(gov_data[gov_data['C-State'] == cstate])})
        occ_total = sum(entry['Occurences'] for entry in perf if entry.get('Idle-Governor') == gov)
        perf_simple_total = sum(entry['Perf-Simple']*entry['Occurences']/occ_total
                                for entry in perf if entry.get('Idle-Governor') == gov)
        perf_extended_total = sum(entry['Perf-Extended']*entry['Occurences']/occ_total
                                for entry in perf if entry.get('Idle-Governor') == gov)
        perf_v2_total = sum(entry['Perf-V2']*entry['Occurences']/occ_total
                                for entry in perf if entry.get('Idle-Governor') == gov)
        perf.append({'Idle-Governor' : gov, 'C-State' : 'all',
                     'Perf-Simple' : perf_simple_total,
                     'Perf-Extended' : perf_extended_total,
                     'Perf-V2' : perf_v2_total,
                     'Occurences' : occ_total})
    utils.save_json(perf, f'examples/{PERFORMANCE_FILE}')


if __name__ == '__main__':
    main()
