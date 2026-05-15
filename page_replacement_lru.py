from tabulate import tabulate
import matplotlib.pyplot as plt


def lru_page_replacement():
    print("\n===== LRU PAGE REPLACEMENT =====")

    pages = list(map(int, input("Enter page reference string (space separated): ").split()))
    capacity = int(input("Enter number of frames: "))

    frames = []
    last_used = {}
    faults = 0
    history = []

    time = 0

    for page in pages:
        time += 1
        fault = "No"

        # =========================
        # HIT CASE
        # =========================
        if page in frames:
            last_used[page] = time

        # =========================
        # FAULT CASE
        # =========================
        else:
            faults += 1
            fault = "Yes"

            # if free space
            if len(frames) < capacity:
                frames.append(page)
            else:
                # 🔥 TRUE LRU SELECTION (safe + correct)
                lru_page = min(frames, key=lambda x: last_used.get(x, 0))
                idx = frames.index(lru_page)
                frames[idx] = page

            last_used[page] = time

        # =========================
        # SAVE STATE
        # =========================
        frame_state = frames.copy()

        while len(frame_state) < capacity:
            frame_state.append('-')

        history.append([page] + frame_state + [fault])

    # =========================
    # OUTPUT TABLE
    # =========================
    headers = ["Page"] + [f"Frame {i+1}" for i in range(capacity)] + ["Fault"]

    print("\n===== FRAME STATUS =====")
    print(tabulate(history, headers=headers, tablefmt="grid"))

    print(f"\nTotal Page Faults = {faults}")

    hits = len(pages) - faults

    # =========================
    # VISUALIZATION
    # =========================
    plt.bar(["Hits", "Faults"], [hits, faults])
    plt.title("LRU Page Replacement")
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.show()