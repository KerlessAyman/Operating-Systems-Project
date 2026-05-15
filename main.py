from cpu_round_robin import round_robin_scheduler
from memory_best_fit import best_fit_memory
from page_replacement_lru import lru_page_replacement
from comparison import show_comparisons


def main():
    while True:
        print("\n========== OPERATING SYSTEMS PROJECT ==========")
        print("1. CPU Scheduling - Round Robin")
        print("2. Memory Allocation - Best Fit")
        print("3. Page Replacement - LRU")
        print("4. Comparison & Analysis")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            round_robin_scheduler()

        elif choice == '2':
            best_fit_memory()

        elif choice == '3':
            lru_page_replacement()

        elif choice == '4':
            show_comparisons()

        elif choice == '5':
            print("Exiting Program...")
            break

        else:
            print("Invalid Choice!")


if __name__ == '__main__':
    main()