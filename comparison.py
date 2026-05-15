from tabulate import tabulate


def show_comparisons():
    print("\n========== COMPARISON & ANALYSIS ==========")

    print("\n1. ROUND ROBIN vs FCFS")

    rr_table = [
        ["Waiting Time", "Lower", "Higher"],
        ["Response Time", "Fast", "Slow"],
        ["Fairness", "High", "Low"],
        ["Context Switching", "More", "Less"],
        ["Best Use", "Time Sharing Systems", "Batch Systems"]
    ]

    print(tabulate(rr_table,
                   headers=["Feature", "Round Robin", "FCFS"],
                   tablefmt="grid"))

    print("\nAdvantages of Round Robin:")
    print("- Fair CPU allocation")
    print("- Better response time")
    print("- Suitable for multitasking")

    print("\nDisadvantages:")
    print("- More context switching")
    print("- Performance depends on quantum")

    print("\n===========================================")

    print("\n2. BEST FIT vs FIRST FIT")

    memory_table = [
        ["Memory Usage", "Efficient", "Moderate"],
        ["Speed", "Slower", "Faster"],
        ["Fragmentation", "Less", "More"],
        ["Search Method", "Search entire list", "First suitable block"]
    ]

    print(tabulate(memory_table,
                   headers=["Feature", "Best Fit", "First Fit"],
                   tablefmt="grid"))

    print("\nAdvantages of Best Fit:")
    print("- Better memory utilization")
    print("- Reduces wasted space")

    print("\nDisadvantages:")
    print("- Slower searching")
    print("- Can create tiny fragments")

    print("\n===========================================")

    print("\n3. LRU vs FIFO")

    page_table = [
        ["Page Faults", "Lower", "Higher"],
        ["Efficiency", "Better", "Average"],
        ["Implementation", "Complex", "Simple"],
        ["Decision", "Least recently used", "Oldest page"]
    ]

    print(tabulate(page_table,
                   headers=["Feature", "LRU", "FIFO"],
                   tablefmt="grid"))

    print("\nAdvantages of LRU:")
    print("- Better performance")
    print("- Reduces unnecessary replacements")

    print("\nDisadvantages:")
    print("- More complex implementation")
    print("- Requires tracking recent usage")