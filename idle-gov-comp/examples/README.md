# Examples

The provided examples are gathered using different setups.

Isolated tasks are recorded and executed on a Core that has been isolated from
the scheduler. This is done to minimize the amount of noise from a system.

The unisolated recordings may represent a more real-world system.

## Setup for Isolated Examples

Set the Kernel Parameter `isolcpus={cpu}`.
In the future the IRQs will also be disabled.
We may also switch to using `cpuset` instead of `isolcpus`.
Record on the {cpu} with `perf`.
Then execute a workload with core affinity `taskset` on {cpu}.

## Intel Examples (Intel Driver)

### Intel Isolated

| Sample | Workload     | Length | IRQ      | HZ       | Parameters                    |
|--------|--------------|--------|----------|----------|-------------------------------|
| 1      | Mini-Bench   | 20s    | Enabled  | -        |                               |
| 2      | Mini-Bench   | 20s    | Enabled  | -        |                               |
| 3      | Mini-Bench   | 120s   | Enabled  | -        |                               |
| 4      | Mini-Bench   | 120s   | Enabled  | -        |                               |
| 5      | Mini-Bench   | 120s   | Disabled | Enabled  |                               |
| 6      | Mini-Bench   | 120s   | Disabled | Disabled |                               |
| 7      | io-net-bench | 120s   | Disabled | Enabled  | 1 Worker, No net, No Pre-Post |
| 8      | io-net-bench | 120s   | Disabled | Disabled | 1 Worker, No net, No Pre-Post |
| 9      | stress       | 120s   | Disabled | Enabled  | 1 CPU Worker                  |
| 10     | stress       | 120s   | Disabled | Disabled | 1 CPU Worker                  |
| 11     | stress       | 120s   | Disabled | Enabled  | 8 IO Workers                  |
| 12     | stress       | 120s   | Disabled | Disabled | 8 IO Workers                  |


## AMD Examples (ACPI)

### AMD Isolated

| Sample | Workload     | Length | IRQ      | HZ       | Parameters                     |
|--------|--------------|--------|----------|----------|--------------------------------|
| 1      | Mini-Bench   | 20s    | Enabled  | -        | -                              |
| 2      | Mini-Bench   | 120s   | Disabled | -        | -                              |
| 3      | Mini-Bench   | 120s   | Disabled | Enabled  | -                              |
| 4      | Mini-Bench   | 120s   | Disabled | Enabled  | -                              |
| 5      | Mini-Bench   | 120s   | Disabled | Disabled | -                              |
| 6      | io-net-bench | 120s   | Disabled | Enabled  | 2 Workers, No net, No Pre-Post |
| 7      | stress       | 120s   | Disabled | Enabled  | 1 CPU Worker                   |
| 8      | stress       | 120s   | Disabled | Enabled  | 8 IO Workers                   |


### AMD Unisolated

| Sample | Workload   | Length | IRQ     |
|--------|------------|--------|---------|
| 1      | Mini-Bench | 20s    | Enabled |
