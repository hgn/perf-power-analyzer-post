#!/usr/bin/python3

import multiprocessing
import requests
import random
import math
import os
import time
import itertools

BENCH_TIME = 20

def cpu_load():
    end_time = time.time() + BENCH_TIME
    while time.time() < end_time:
        [math.sqrt(random.randint(1, 10000)) for _ in range(100000)]
        time.sleep(random.choice([0.01, 0.05]))

def io_load():
    end_time = time.time() + BENCH_TIME
    while time.time() < end_time:
        filename = f"/tmp/tempfile_{os.getpid()}"
        with open(filename, "w+") as f:
            for _ in range(1000):
                f.write("Some random text\n")
        with open(filename, "r") as f:
            _ = f.read()
        os.remove(filename)
        time.sleep(random.choice([0.01, 0.05]))

def network_load():
    end_time = time.time() + BENCH_TIME
    urls = ["http://google.com", "http://heise.de", "http://www.cloudflare.com", "http://facebook.com" ]
    url_cycle = itertools.cycle(urls)
    while time.time() < end_time:
        try:
            requests.get(next(url_cycle))
        except requests.RequestException:
            pass
        time.sleep(random.choice([0.01, 0.05]))

def run_benchmark():
    processes = []

    # CPU Load
    for i in range(2):
        print(f"  start CPU load process ({i + 1})")
        p = multiprocessing.Process(target=cpu_load)
        p.start()
        processes.append(p)

    # IO Load
    time.sleep(0.001)
    print(f"  start IO load process")
    p = multiprocessing.Process(target=io_load)
    p.start()
    processes.append(p)

    # Network Load
    time.sleep(0.001)
    print(f"  start NETWORK load process")
    p = multiprocessing.Process(target=network_load)
    p.start()
    processes.append(p)

    for p in processes:
        p.join()

def run_benchmarks_in_parallel():
    benchmark_processes = []

    for i in range(5):
        print(f"Initiate worker processes now ({i + 1})")
        p = multiprocessing.Process(target=run_benchmark)
        p.start()
        benchmark_processes.append(p)
        time.sleep(0.5)

    for p in benchmark_processes:
        p.join()

if __name__ == "__main__":
    print("Start Benchmark Suite now")
    print("now sleep for 20 seconds")
    time.sleep(20)
    run_benchmarks_in_parallel()
    print("now sleep for 20 seconds")
    time.sleep(20)
