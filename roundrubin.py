# ---------- Class to represent each process ----------
class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0


# ---------- Round Robin Algorithm ----------
def round_robin(processes, quantum):
    current_time = 0
    completed = 0
    queue = []
    processes.sort(key=lambda p: p.arrival_time)  # Sort by arrival time

    i = 0
    while completed < len(processes):
        # Add all processes that have arrived by current time
        while i < len(processes) and processes[i].arrival_time <= current_time:
            queue.append(processes[i])
            i += 1

        if queue:
            current = queue.pop(0)
            exec_time = min(current.remaining_time, quantum)
            current.remaining_time -= exec_time
            current_time += exec_time

            # Add new processes that arrived during execution
            while i < len(processes) and processes[i].arrival_time <= current_time:
                queue.append(processes[i])
                i += 1

            if current.remaining_time == 0:
                completed += 1
                current.completion_time = current_time
                current.turnaround_time = current.completion_time - current.arrival_time
                current.waiting_time = current.turnaround_time - current.burst_time
            else:
                queue.append(current)
        else:
            current_time += 1  # CPU idle time

    print_results(processes, "Round Robin", quantum)


# ---------- Print Results ----------
def print_results(processes, algo_name, quantum):
    print(f"\n===== {algo_name} Scheduling (Quantum = {quantum}) =====")
    print("Process\tAT\tBT\tCT\tTAT\tWT")
    for p in processes:
        print(f"{p.name}\t{p.arrival_time}\t{p.burst_time}\t{p.completion_time}\t{p.turnaround_time}\t{p.waiting_time}")

    avg_tat = sum(p.turnaround_time for p in processes) / len(processes)
    avg_wt = sum(p.waiting_time for p in processes) / len(processes)
    print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time: {avg_wt:.2f}")


# ---------- Main Function ----------
if __name__ == "__main__":
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 4),
        Process("P3", 2, 2),
        Process("P4", 3, 1)
    ]

    quantum = 2
    round_robin(processes, quantum)
