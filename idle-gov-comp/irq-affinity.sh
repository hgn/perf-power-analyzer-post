#!/usr/bin/env sh

# Migrate irqs to CPU 0-1 (exclude CPU 2,3)
for I in $(ls /proc/irq)
do
    if [[ -d "/proc/irq/$I" ]]
    then
        echo "Affining vector $I to CPUs 0-1"
        echo 0-1 > /proc/irq/$I/smp_affinity_list
    fi
done
