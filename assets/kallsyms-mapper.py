#!/usr/bin/python3

import sys
import re

ADDR_PATTERN = re.compile(r'[0-9a-fA-F]{8,16}')

def load_kernel_symbols():
    symbols = {}
    try:
        with open("/proc/kallsyms", "r") as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 3:
                    address, type, name = parts[:3]
                    symbols[address] = name
    except IOError:
        pass
    return symbols

def substitute_kernel_addresses(line, symbols):
    return ADDR_PATTERN.sub(lambda match: symbols.get(match.group(), match.group()), line)

def main():
    symbols = load_kernel_symbols()
    for line in sys.stdin:
        print(substitute_kernel_addresses(line.strip(), symbols))

if __name__ == "__main__":
    main()
