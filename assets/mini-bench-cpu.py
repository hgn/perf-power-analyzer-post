#!/usr/bin/python3

""" Mini Bench CPU

This script is designed to create somewhat deterministic workload on a single core.
The workload is especially useful for observing the C-State usage of an Idle Governor.

Adjustable Parameters:
CPU_LOAD : bool
    Defines which kind of load should be generated.
        True    =>  CPU has load inbetween sleeps.
        False   =>  CPU primarily goes into sleep states.

USAGE:

Call this script with taskset to set the process affinity to a specific core:
    taskset --cpu-list ${CPU_CORE} ./mini-bench-cpu.py

"""

import random
import math
import time

PRE_POST_SLEEP = 20
BENCH_TIME = 20
# Adjust the type of workload with CPU_LOAD
CPU_LOAD = False
# Set a seed for reproducibility
random.seed(0)

def cpu_load():
    end_time = time.time() + BENCH_TIME
    while time.time() < end_time:
        [math.sqrt(random.randint(1, 10000)) for _ in range(100000)]
        time.sleep(random.choice([0.0, 0.006]))

def sleep_load():
    end_time = time.time() + BENCH_TIME
    while time.time() < end_time:
        time.sleep(random.choice([0.0, 0.006]))


if __name__ == "__main__":
    print("Start Benchmark Suite now")
    print(f"now sleep for {PRE_POST_SLEEP} seconds")
    time.sleep(PRE_POST_SLEEP)
    print(f"now bench for {BENCH_TIME} seconds")
    if CPU_LOAD:
        print("Starting CPU Load")
        cpu_load()
    else:
        print("Starting Sleep Load")
        sleep_load()
    print(f"now sleep for {PRE_POST_SLEEP} seconds")
    time.sleep(PRE_POST_SLEEP)
