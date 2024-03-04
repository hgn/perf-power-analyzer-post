#!/usr/bin/env python3

import json
import pandas as pd
import re


def read_gov(file_name : str):
    """Read csv and return a pandas dataframe."""
    gov_data = pd.read_csv(file_name, delim_whitespace=True,
                      usecols=['C-State', 'Sleep[ns]', 'Miss', 'Below'])
    return gov_data


def read_json(file_name : str):
    """Read JSON file and return the data."""
    with open(file_name, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def save_json(data : list, file_name : str):
    """Save data into JSON."""
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)


def unique_res(residencies, target_cpu=0):
    """Return the set of residencies for given CPU default is 0."""
    res_dict = residencies[list(residencies.keys())[target_cpu]]
    res = set()
    for state in res_dict.values():
        res.add(state['residency'])
    res = sorted([int(x) for x in res])
    return res


def find_res(res : list, cstate : str, below : bool = None, target_cpu : int = 0):
    """
    Return the residency time in ns below or above the cstate.

    If target is True then below is ignored and the res in ns corresponding to the
    cstate is returned.
    """
    res_dict = res[list(res.keys())[target_cpu]]
    res = unique_res(res)
    target_res = None

    for res_state in res_dict.values():
        if cstate == res_state['name']:
            target_res = int(res_state['residency'])
            break

    if below is None:
        return target_res * 1000

    index = res.index(int(target_res))
    if not below:
        return (res[index - 1] * 1000) if index > 0 else 0
    return (res[index + 1] * 1000) if index < len(res) - 1 else res[index]


def normalize(time : int, prev_res : int, next_res : int, target_res : int, weight : int):
    '''Normalizes a delta time according to the correspoding residency time'''
    # Still need this for the case, that the slight offset defines it below or above the bound,
    # even though the sleep time does not validate it
    data_min = min(time, target_res, prev_res)
    data_max = max(time, target_res, next_res)
    norm_value = (time - data_min) / (data_max - data_min)
    scale_factor = (target_res * weight) / (data_max - data_min)
    return scale_factor * norm_value


def normalize_above(time : int, target_res : int, weight : int):
    """Normalize a delta time according to the correspoding residency time.

    In order to have values between 0 and 1, weight needs to be in that range too.
    This function ensures to normalize values disregarding the underlying data."""
    data_min = 0
    data_max = target_res
    norm_value = (time - data_min) / (data_max - data_min)
    return weight * norm_value


def normalize_below(time : int, max_res : int, next_res : int, weight : int):
    """
    Normalize a delta time according to the correspoding residency time.

    In order to have values between 0 and 1, weight needs to be in that range too.
    This function ensures to normalize values disregarding the underlying data.
    """
    # Still need this for the case, that the slight offset defines it below or above the bound,
    # even though the sleep time does not validate it
    data_min = next_res
    data_max = max_res
    if data_min == data_max:
        # If we enter the second to last and last C-State we just return the weight
        return weight
    time = min(time, max_res)
    norm_value = (time - data_min) / (data_max - data_min)
    return weight * abs(1 - norm_value)



def cstate_key(cstate):
    """Alphanumeric sort for C-States."""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', str(cstate))]
