import heapq

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


# ---------- SJF Preemptive (Shortest Remaining Time First) ----------
def sjf_preemptive(processes):
    current_time = 0
    completed = 0
    n = len(processes)
    processes.sort(key=lambda p: p.arrival_time)  # Sort by arrival time
    pq = []  # Min-heap based on remaining time
    i = 0  # Index for arriving processes

    while completed < n:
        # Add all processes that have arrived up to current_time
        while i < n and processes[i].arrival_time <= current_time:
            heapq.heappush(pq, (processes[i].remaining_time, i))
            i += 1

        if pq:
            rt, idx = heapq.heappop(pq)
            current_process = processes[idx]
            # Execute process for 1 time unit
            current_process.remaining_time -= 1
            current_time += 1

            # If finished
            if current_process.remaining_time == 0:
                completed += 1
                current_process.completion_time = current_time
                current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
                current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            else:
                # Push back with updated remaining time
                heapq.heappush(pq, (current_process.remaining_time, idx))
        else:
            current_time += 1  # CPU idle

    print_results(processes, "SJF (Preemptive)")


# ---------- Print Results ----------
def print_results(processes, algo_name):
    print(f"\n===== {algo_name} Scheduling =====")
    print("Process\tAT\tBT\tCT\tTAT\tWT")

    total_wt = sum(p.waiting_time for p in processes)
    total_tat = sum(p.turnaround_time for p in processes)

    for p in processes:
        print(f"{p.name}\t{p.arrival_time}\t{p.burst_time}\t{p.completion_time}\t{p.turnaround_time}\t{p.waiting_time}")

    print(f"\nAverage Turnaround Time: {total_tat / len(processes):.2f}")
    print(f"Average Waiting Time: {total_wt / len(processes):.2f}")


# ---------- Main ----------
if __name__ == "__main__":
    processes = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1),
        Process("P4", 5, 4)
    ]

    sjf_preemptive(processes)
