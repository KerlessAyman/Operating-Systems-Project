from collections import deque
from tabulate import tabulate
import matplotlib.pyplot as plt


# =========================
# GANTT CHART
# =========================
def draw_gantt_chart(gantt):
    fig, ax = plt.subplots(figsize=(10, 2))

    start = 0

    for process, duration in gantt:
        ax.barh(0, duration, left=start)
        ax.text(start + duration / 2, 0, process,
                ha='center', va='center')
        start += duration

    ax.set_xlabel("Time")
    ax.set_yticks([])
    plt.title("Round Robin Gantt Chart")
    plt.show()


# =========================
# PROCESS CLASS
# =========================
class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.completion = 0
        self.turnaround = 0
        self.waiting = 0


# =========================
# ROUND ROBIN SCHEDULER
# =========================
def round_robin_scheduler():

    print("\n===== ROUND ROBIN CPU SCHEDULING =====")

    n = int(input("Enter number of processes: "))

    processes = []

    for i in range(n):
        arrival = int(input(f"Enter Arrival Time for P{i+1}: "))
        burst = int(input(f"Enter Burst Time for P{i+1}: "))
        processes.append(Process(f"P{i+1}", arrival, burst))

    quantum = int(input("Enter Time Quantum: "))

    processes.sort(key=lambda x: x.arrival)

    time = 0
    queue = deque()
    completed = 0
    index = 0

    gantt = []

    # =========================
    # MAIN LOOP
    # =========================
    while completed < n:

        # add arrived processes
        while index < n and processes[index].arrival <= time:
            queue.append(processes[index])
            index += 1

        if not queue:
            time += 1
            continue

        current = queue.popleft()

        execute = min(quantum, current.remaining)

        print(f"\nTime {time} -> {time + execute}: {current.pid} executing")

        gantt.append((current.pid, execute))

        time += execute
        current.remaining -= execute

        # add newly arrived processes during execution
        while index < n and processes[index].arrival <= time:
            queue.append(processes[index])
            index += 1

        # =========================
        # FIX: re-queue or finish
        # =========================
        if current.remaining > 0:
            queue.append(current)
        else:
            completed += 1
            current.completion = time
            current.turnaround = current.completion - current.arrival
            current.waiting = current.turnaround - current.burst

    # =========================
    # FINAL TABLE
    # =========================
    table = []
    total_wt = 0
    total_tat = 0

    for p in processes:
        table.append([
            p.pid,
            p.arrival,
            p.burst,
            p.completion,
            p.turnaround,
            p.waiting
        ])
        total_wt += p.waiting
        total_tat += p.turnaround

    print("\n===== FINAL RESULTS =====")
    print(tabulate(
        table,
        headers=["Process", "Arrival", "Burst", "Completion", "TAT", "WT"],
        tablefmt="grid"
    ))

    print(f"\nAverage Waiting Time = {total_wt / n:.2f}")
    print(f"Average Turnaround Time = {total_tat / n:.2f}")

    # =========================
    # GANTT CHART
    # =========================
    draw_gantt_chart(gantt)