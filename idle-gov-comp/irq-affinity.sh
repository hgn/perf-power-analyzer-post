#!/usr/bin/env sh

# Migrate irqs to CPU 0-2 (exclude CPU 3)
for I in $(ls /proc/irq)
do
    if [[ -d "/proc/irq/$I" ]]
    then
        echo "Affining vector $I to CPUs 0-2"
        echo 0-2 > /proc/irq/$I/smp_affinity_list
    fi
done
