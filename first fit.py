# Class to represent each process
class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0


# ---------- FCFS Algorithm ----------
def FCFS(processes):
    current_time = 0

    # Sort processes by arrival time
    processes.sort(key=lambda p: p.arrival_time)

    for p in processes:
        # If CPU is idle until the process arrives
        if current_time < p.arrival_time:
            current_time = p.arrival_time

        # Calculate Waiting Time, Turnaround Time, and Completion Time
        p.waiting_time = current_time - p.arrival_time
        current_time += p.burst_time
        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time


# ---------- Print Results ----------
def print_results(processes, algo_name):
    print(f"\n===== {algo_name} Scheduling =====")
    print("Process\tAT\tBT\tCT\tTAT\tWT")

    total_wt = 0
    total_tat = 0

    for p in processes:
        print(f"{p.name}\t{p.arrival_time}\t{p.burst_time}\t{p.completion_time}\t{p.turnaround_time}\t{p.waiting_time}")
        total_wt += p.waiting_time
        total_tat += p.turnaround_time

    print(f"\nAverage Turnaround Time: {total_tat / len(processes):.2f}")
    print(f"Average Waiting Time: {total_wt / len(processes):.2f}")


# ---------- Main Function ----------
if __name__ == "__main__":
    processes = [
        Process("P1", 0, 5),
        Process("P2", 1, 3),
        Process("P3", 2, 8),
        Process("P4", 3, 6)
    ]

    FCFS(processes)
    print_results(processes, "First Come First Serve (FCFS)")
