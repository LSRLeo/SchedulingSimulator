"""
Project: Scheduling Simulator 
Author: Shirui Liu
Date: 2026-03-14

"""


from queue import PriorityQueue
import sys


class Process:
    def __init__(self, name, priority, arrival_time, total_time, block_time):

        self.name = name
        self.arrival_time = arrival_time
        self.total_time = total_time
        self.priority = priority
        self.block_interval = block_time
        self.last_run = 0

        self.time_used = 0
        self.current_block_time = 0
        self.unlock_time = 0

    def is_finished(self):
        return self.time_used >= self.total_time

    def remaining_time(self):
        return self.total_time - self.time_used

    def remained_block_time(self):
        if self.block_interval == 0:
            return float('inf')
        return self.block_interval - self.current_block_time

    def __lt__(self, other):
        return self.name < other.name


def load_processes(filename):
    processes = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                name, priority, arrival_time, total_time, block_time = line.split()
                processes.append(Process(name, int(priority), int(arrival_time), int(total_time), int(block_time)))

    for i, process in enumerate(processes):
        process.last_run = i - len(processes)

    return processes


def check_and_enqueue(arrival_queue, blocked_queue, ready_queue, current_time, ready_queue_counter):
    run1 = True
    run2 = True
    while not arrival_queue.empty() and run1:
        arrival_time, process = arrival_queue.queue[0]
        if arrival_time <= current_time:
            arrival_queue.get()
            ready_queue.put((-process.priority, process.last_run, process))
            ready_queue_counter += 1
        else:
            run1 = False

    while not blocked_queue.empty() and run2:
        unblock_time, process = blocked_queue.queue[0]
        if unblock_time <= current_time:
            blocked_queue.get()
            ready_queue.put((-process.priority, process.last_run, process))
            ready_queue_counter += 1
        else:
            run2 = False

    return ready_queue_counter


def round_robin(arrival_queue, blocked_queue, ready_queue, current_time, ready_queue_counter, time_slice, block_duration, run_order):
    turnaround_times = []
    while not (arrival_queue.empty() and blocked_queue.empty() and ready_queue.empty()):
        ready_queue_counter = check_and_enqueue(arrival_queue, blocked_queue, ready_queue, current_time, ready_queue_counter)

        if ready_queue.empty():
            next_process = []
            if not arrival_queue.empty():
                next_process.append(arrival_queue.queue[0][0])
            if not blocked_queue.empty():
                next_process.append(blocked_queue.queue[0][0])

            idle_start = current_time
            current_time = min(next_process)
            print_output_interval("(IDLE)", idle_start, current_time, "I")
            ready_queue_counter = check_and_enqueue(arrival_queue, blocked_queue, ready_queue, current_time, ready_queue_counter)

        else:
            _, _, process = ready_queue.get()

            run_time = min(time_slice, process.remaining_time(), process.remained_block_time())

            start_time = current_time
            process.last_run = run_order
            run_order += 1
            current_time += run_time
            process.time_used += run_time
            process.current_block_time += run_time

            if not process.is_finished():
                if process.current_block_time >= process.block_interval and process.block_interval != 0:
                    print_output_interval(process.name, start_time, current_time, "B")
                    process.unlock_time = current_time + block_duration
                    process.current_block_time = 0
                    blocked_queue.put((process.unlock_time, process))
                    ready_queue_counter = check_and_enqueue(arrival_queue, blocked_queue, ready_queue, current_time, ready_queue_counter)
                else:
                    print_output_interval(process.name, start_time, current_time, "P")
                    ready_queue.put((-process.priority, process.last_run, process))
            else:
                turnaround_times.append(current_time - process.arrival_time)
                print_output_interval(process.name, start_time, current_time, "T")

    print(f"Average turnaround time: {sum(turnaround_times) / len(turnaround_times)}")


def print_output_interval(name, start_time, end_time, status):
    print(f"{start_time}\t{name}\t{end_time - start_time}\t{status}")


def main():
    filename = sys.argv[1]
    time_slice = int(sys.argv[2])
    block_duration = int(sys.argv[3])

    arrival_queue = PriorityQueue()
    blocked_queue = PriorityQueue()
    ready_queue = PriorityQueue()

    current_time = 0
    ready_queue_counter = 0
    run_order = 0

    processes = load_processes(filename)
    for process in processes:
        arrival_queue.put((process.arrival_time, process))

    ready_queue_counter = check_and_enqueue(arrival_queue, blocked_queue, ready_queue, current_time, ready_queue_counter)

    print(f"timeSlice: {time_slice}\tblockDuration: {block_duration}")
    round_robin(arrival_queue, blocked_queue, ready_queue, current_time, ready_queue_counter, time_slice, block_duration, run_order)


if __name__ == "__main__":
    main()