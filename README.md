# Perf Power Statistics Module Documentation

perf power-statistics provides several modules, they can be queried via

```
$ perf script -i /tmp/perf.out -s ~/src/code/linux/tools/perf/scripts/python/power-statistics.py -- --mode help
usage: power-statistics.py [-h] [-m [{idle-cluster,task,timer,frequency,summary,all}]] [-C CPU] [-v] [--highlight-tasks HIGHLIGHT_TASKS] [--stdio-color {always,never,auto}] [--csv]
power-statistics.py: error: argument -m/--mode: invalid choice: 'help' (choose from 'idle-cluster', 'task', 'timer', 'frequency', 'summary', 'all')
```

Suppord modules are

- idle-cluster
- task
- timer
- frequency
- summary
- all


Subsequent sections describe all modules in detail and how to post-process the data

## General Aspects

## Recording

## CPU Filtering

Via `-C <n>` or `--cpu <n>` it is possible to restrict the output to one CPU.
However, it is important to note that not all commands understand this option.
The often better alternative is to specify a CPU when recording, if this is
possible, for example because processes have been pinned to a specific CPU with
taskset.

```
perf script -i /tmp/perf.out -s ~/src/code/linux/tools/perf/scripts/python/power-statistics.py -- --mode wakeups-timesequence -C 1
```

# Timer (mode: timer)

*Required events: ...*


## Timer Type Callback Expiration

Output Format:

```
TimerType      Callback         Expires 
HRTimer        ffffffffb6da37c0 34051 
HRTimer        ffffffffb6d8d650 6468 
HRTimer        ffffffffb75615e0 4040 
HRTimer        ffffffffb6de6a80 800 
HRTimer        ffffffffc0b0cd20 413 
HRTimer        ffffffffb6d9f280 1 
KernelTimer    ffffffffb6cddab0 2647 
KernelTimer    ffffffffb6d8b610 1629 
KernelTimer    ffffffffb743fb50 745 
KernelTimer    ffffffffb718bfc0 415 
[...]
```

![](./images/timer-01/timer-type-callback-expiration-pie.png)

![](./images/timer-01/timer-type-callback-expiration-bar.png)


# Wakeups Timesequence (mode: wakeups-timesequence)

*Required events: sched_switch*

Show on a per process and thread basis the wakeups for every second. This
analyse can be used to get an idea about periods where a process triggers many
wakeups vs. periods of a task where only a few wakeups are triggered.

These data can be used to visualize the data to provide a human overview.

> **Note:** process wakeups are not the only way to wake up a CPU core from a sleep
> phase. Interrupts also lead to a change to a C0 status. But: the analysis at
> process/thread level allows the easiest intervention, as the execution
> control is in the hands of the developer - this is not the case with IRQs
> that occur asynchronously. 


## Wakeup Task per CPU View

The following picture shows a nearly idle system, only a wild process, which is
always migrated to different cores by the scheduler, generates a constantly
high wakeup load.

![](./images/wakeups-timesequence-01/wakeups-timemap-task-cpu.png)

## Wakeup Task View

The following illustration show the exact same data, but with a  focus on a
task level. Here the former crazy task - a clipboard process gone wild - which
asks for clipboard data much too eagerly, causes a high wakeup load.


![](./images/wakeups-timesequence-01/wakeups-timemap-task.png)

## Wakeup IRQ View

![](./images/wakeups-timesequence-01/wakeups-timemap-irq.png)

## Wakeup IRQ per CPU View

![](./images/wakeups-timesequence-01/wakeups-timemap-irq-cpu.png)

