# SchedulingSimulator
This project implement a priority-based Round-Robin CPU scheduler in Python that simulates process scheduling with arrival, ready, and blocked queues using Python's PriorityQueue, given an input file of processes and command-line arguments for time slice and block duration.


# Round-Robin Scheduler(Non-preemptive)

A priority-based Round-Robin CPU scheduler simulation written in Python. Processes are scheduled using arrival, ready, and blocked queues, with output showing each scheduling interval and average turnaround time.

---

## Run

```bash
python3 scheduler.py input.txt 10 20
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `input file` | Path to the process list file |
| `time_slice` | Length of each time slice |
| `block_duration` | How long a process is unavailable after blocking |

---

## Input Format

One process per line. Lines starting with `#` are treated as comments and ignored.

```
name priority arrival_time total_time block_interval
```

| Field | Description |
|-------|-------------|
| `name` | Process name (no spaces) |
| `priority` | Priority level 1–9 (higher = runs first) |
| `arrival_time` | Time the process enters the system |
| `total_time` | Total CPU time the process needs |
| `block_interval` | How often the process blocks for I/O |

**Example:**
```
# Sample processes
A 1 0 100 25
B 5 1 50 20
C 2 2 90 45
```

---

## Output Format

```
timeSlice: 10     blockDuration: 20
0    A    10    P
10   B    10    B
...
Average turnaround time: 184.0
```

**Status codes:**
| Code | Meaning |
|------|---------|
| `P` | Preempted by time slice |
| `B` | Blocked for I/O |
| `T` | Process terminated |
| `I` | CPU idle |
