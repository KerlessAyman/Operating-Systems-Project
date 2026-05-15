from tabulate import tabulate
import matplotlib.pyplot as plt


def best_fit_memory():
    print("\n===== BEST FIT MEMORY ALLOCATION =====")

    num_blocks = int(input("Enter number of memory blocks: "))

    blocks = []

    for i in range(num_blocks):
        size = int(input(f"Enter size of Block {i+1}: "))
        blocks.append(size)

    num_processes = int(input("Enter number of processes: "))

    processes = []

    for i in range(num_processes):
        size = int(input(f"Enter size of Process {i+1}: "))
        processes.append(size)

    allocation = [-1] * num_processes
    fragmentation = [0] * num_processes

    for i in range(num_processes):
        best_idx = -1

        for j in range(num_blocks):
            if blocks[j] >= processes[i]:

                if best_idx == -1 or blocks[j] < blocks[best_idx]:
                    best_idx = j

        if best_idx != -1:
            allocation[i] = best_idx
            fragmentation[i] = blocks[best_idx] - processes[i]
            blocks[best_idx] -= processes[i]

    table = []

    total_fragmentation = 0

    for i in range(num_processes):

        if allocation[i] != -1:
            result = f"Block {allocation[i] + 1}"
        else:
            result = "Not Allocated"

        table.append([
            f"P{i+1}",
            processes[i],
            result,
            fragmentation[i]
        ])

        total_fragmentation += fragmentation[i]

    print("\n===== ALLOCATION TABLE =====")

    print(tabulate(table,
                   headers=["Process", "Size", "Allocated Block", "Fragmentation"],
                   tablefmt="grid"))

    print(f"\nTotal Internal Fragmentation = {total_fragmentation}")

    labels = [f"P{i+1}" for i in range(num_processes)]

    plt.bar(labels, fragmentation)
    plt.xlabel("Processes")
    plt.ylabel("Fragmentation")
    plt.title("Best Fit Fragmentation")
    plt.show()