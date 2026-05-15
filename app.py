import streamlit as st
from collections import deque
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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
# ROUND ROBIN
# =========================
def round_robin(processes, quantum):
    time = 0
    queue = deque()
    index = 0
    completed = 0
    n = len(processes)

    gantt = []

    processes.sort(key=lambda x: x.arrival)

    while completed < n:

        while index < n and processes[index].arrival <= time:
            queue.append(processes[index])
            index += 1

        if not queue:
            time += 1
            continue

        current = queue.popleft()
        exec_time = min(quantum, current.remaining)

        gantt.append((current.pid, exec_time))

        time += exec_time
        current.remaining -= exec_time

        while index < n and processes[index].arrival <= time:
            queue.append(processes[index])
            index += 1

        if current.remaining > 0:
            queue.append(current)
        else:
            completed += 1
            current.completion = time
            current.turnaround = time - current.arrival
            current.waiting = current.turnaround - current.burst

    return processes, gantt


# =========================
# GANTT CHART (FIXED)
# =========================
def draw_gantt(gantt):
    fig, ax = plt.subplots(figsize=(10, 2))
    start = 0
    
    # Create a color map for different processes
    unique_processes = list(set(p for p, _ in gantt))
    color_map = plt.cm.tab10(np.linspace(0, 1, len(unique_processes)))
    process_color = {proc: color_map[i] for i, proc in enumerate(unique_processes)}

    for p, t in gantt:
        ax.barh(0, t, left=start, color=process_color[p], edgecolor='black', linewidth=1)
        ax.text(start + t / 2, 0, p, ha='center', va='center', fontsize=10, fontweight='bold')
        start += t

    ax.set_yticks([])
    ax.set_ylabel("CPU", fontsize=12)
    ax.set_xlabel("Time", fontsize=12)
    ax.set_title("Gantt Chart - Round Robin Scheduling", fontsize=14, fontweight='bold')
    ax.set_xlim(0, start)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    return fig


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="OS Project", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #2e4053;'>🖥 Operating Systems Project</h1>
    <hr>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "⚙️ CPU Scheduling",
    "💾 Memory Allocation", 
    "📄 Page Replacement",
    "📊 Comparison & Analysis"
])


# =========================
# CPU TAB
# =========================
with tab1:
    st.header("⚙️ Round Robin CPU Scheduling")
    
    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Number of Processes", min_value=1, max_value=10, step=1, value=3)
    with col2:
        quantum = st.number_input("Time Quantum", min_value=1, max_value=10, step=1, value=2)

    processes = []

    if n > 0:
        st.subheader("📝 Process Details")
        
        # Create header
        cols = st.columns([1, 2, 2])
        cols[0].write("**Process**")
        cols[1].write("**Arrival Time**")
        cols[2].write("**Burst Time**")
        
        for i in range(int(n)):
            cols = st.columns([1, 2, 2])
            with cols[0]:
                pid = f"P{i+1}"
                st.write(f"**{pid}**")
            with cols[1]:
                arrival = st.number_input(f"Arrival", key=f"arr_{i}", min_value=0, step=1, label_visibility="collapsed")
            with cols[2]:
                burst = st.number_input(f"Burst", key=f"bur_{i}", min_value=1, step=1, label_visibility="collapsed")
            processes.append(Process(pid, arrival, burst))

    if st.button("▶️ Run CPU Scheduler", type="primary"):
        if processes:
            result, gantt = round_robin(processes.copy(), quantum)

            st.success("✅ Scheduling Completed Successfully!")

            df = pd.DataFrame([
                [p.pid, p.arrival, p.burst, p.completion, p.turnaround, p.waiting]
                for p in result
            ], columns=["Process", "Arrival", "Burst", "Completion", "Turnaround", "Waiting"])
            
            st.dataframe(df, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                avg_waiting = sum(p.waiting for p in result) / len(result)
                st.metric("📊 Average Waiting Time", f"{avg_waiting:.2f}")
            with col2:
                avg_turnaround = sum(p.turnaround for p in result) / len(result)
                st.metric("📊 Average Turnaround Time", f"{avg_turnaround:.2f}")

            st.pyplot(draw_gantt(gantt))
        else:
            st.warning("Please add at least one process.")


# =========================
# MEMORY TAB (FIXED)
# =========================
with tab2:
    st.header("💾 Best Fit Memory Allocation")
    
    col1, col2 = st.columns(2)
    with col1:
        blocks_input = st.text_input("Memory Blocks (space-separated)", "100 500 200 300 600")
    with col2:
        processes_input = st.text_input("Processes (space-separated)", "212 417 112 426")

    if st.button("▶️ Run Memory Allocation", type="primary"):
        try:
            blocks = list(map(int, blocks_input.split()))
            procs = list(map(int, processes_input.split()))
            
            original_blocks = blocks.copy()
            allocation = [-1] * len(procs)
            internal_frag = [0] * len(procs)

            for i in range(len(procs)):
                best_idx = -1
                for j in range(len(blocks)):
                    if blocks[j] >= procs[i]:
                        if best_idx == -1 or blocks[j] < blocks[best_idx]:
                            best_idx = j

                if best_idx != -1:
                    allocation[i] = best_idx
                    internal_frag[i] = blocks[best_idx] - procs[i]
                    blocks[best_idx] -= procs[i]

            # Calculate external fragmentation
            external_frag = sum(blocks)

            # Display results
            df = pd.DataFrame([
                [f"P{i+1}", procs[i], f"Block {allocation[i]}" if allocation[i] != -1 else "Not Allocated", 
                 internal_frag[i] if allocation[i] != -1 else "-"]
                for i in range(len(procs))
            ], columns=["Process", "Size (KB)", "Allocated Block", "Internal Frag. (KB)"])
            
            st.dataframe(df, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("💡 Total Internal Fragmentation", f"{sum(internal_frag)} KB")
            with col2:
                st.metric("🗑️ External Fragmentation", f"{external_frag} KB")
            
            # Visualization
            fig, ax = plt.subplots(figsize=(10, 4))
            allocated = [x >= 0 for x in allocation]
            colors = ['#2ecc71' if allocated[i] else '#e74c3c' for i in range(len(procs))]
            y_pos = range(len(procs))
            bars = ax.barh(y_pos, procs, color=colors)
            ax.set_yticks(y_pos)
            ax.set_yticklabels([f"P{i+1}" for i in range(len(procs))])
            ax.set_xlabel("Memory Size (KB)", fontsize=12)
            ax.set_title("Memory Allocation Visualization", fontsize=14)
            ax.grid(axis='x', alpha=0.3)
            
            # Add legend
            from matplotlib.patches import Patch
            legend_elements = [Patch(facecolor='#2ecc71', label='Allocated'),
                             Patch(facecolor='#e74c3c', label='Not Allocated')]
            ax.legend(handles=legend_elements, loc='upper right')
            
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error: {e}. Please check input format.")


# =========================
# PAGE REPLACEMENT (FIXED LRU)
# =========================
with tab3:
    st.header("📄 LRU Page Replacement Algorithm")
    
    col1, col2 = st.columns(2)
    with col1:
        pages_input = st.text_input("Page Reference String", "7 0 1 2 0 3 0 4 2 3 0 3 2")
    with col2:
        frames = st.number_input("Number of Frames", min_value=1, max_value=10, step=1, value=3)

    if st.button("▶️ Run LRU Simulation", type="primary"):
        pages = list(map(int, pages_input.split()))
        
        frames_list = []
        last_used = {}
        page_faults = 0
        current_time = 0
        history = []
        hits = 0

        for page in pages:
            current_time += 1
            is_fault = False

            if page in frames_list:
                # HIT - Update last used time
                last_used[page] = current_time
                hits += 1
                fault_text = "❌ Hit"
            else:
                # FAULT
                page_faults += 1
                is_fault = True
                fault_text = "✅ Fault"

                if len(frames_list) < frames:
                    frames_list.append(page)
                else:
                    # Find LRU page (oldest last_used)
                    lru_page = min(frames_list, key=lambda x: last_used[x])
                    lru_index = frames_list.index(lru_page)
                    frames_list[lru_index] = page
                
                last_used[page] = current_time

            # Prepare display row
            display_frames = frames_list.copy()
            while len(display_frames) < frames:
                display_frames.append("-")
            
            history.append([current_time, page] + display_frames + [fault_text])

        # Display results
        columns = ["Time", "Page"] + [f"Frame {i}" for i in range(frames)] + ["Status"]
        df = pd.DataFrame(history, columns=columns)
        st.dataframe(df, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📄 Total Page Faults", page_faults)
        with col2:
            st.metric("✅ Total Hits", hits)
        with col3:
            fault_rate = (page_faults / len(pages)) * 100
            st.metric("📊 Fault Rate", f"{fault_rate:.1f}%")
        
        # Fault visualization
        fig, ax = plt.subplots(figsize=(10, 3))
        fault_indicators = [1 if "Fault" in row[-1] else 0 for row in history]
        colors = ['#e74c3c' if x == 1 else '#2ecc71' for x in fault_indicators]
        ax.bar(range(1, len(pages)+1), fault_indicators, color=colors, edgecolor='black')
        ax.set_xlabel("Page Reference Number", fontsize=12)
        ax.set_ylabel("Fault (1) / Hit (0)", fontsize=12)
        ax.set_title("Page Fault Pattern", fontsize=14)
        ax.set_xticks(range(1, len(pages)+1))
        ax.set_ylim(-0.1, 1.1)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)


# =========================
# COMPARISON TAB
# =========================
with tab4:
    st.header("📊 Comparison & Analysis")
    
    # CPU Scheduling Comparison
    st.subheader("⚙️ CPU Scheduling Algorithms")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔄 Round Robin (RR)")
        st.info("**✅ Advantages:**\n- Fair distribution of CPU time\n- Good response time for interactive systems\n- No starvation\n\n**❌ Disadvantages:**\n- Performance depends on quantum size\n- More context switches overhead")
        
    with col2:
        st.markdown("### 📋 First Come First Serve (FCFS)")
        st.info("**✅ Advantages:**\n- Simple to implement\n- No starvation\n- Low overhead\n\n**❌ Disadvantages:**\n- Convoy effect (short processes wait for long ones)\n- Poor response time\n- Not suitable for interactive systems")
    
    st.markdown("---")
    
    # Memory Allocation Comparison
    st.subheader("💾 Memory Allocation Algorithms")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Best Fit")
        st.success("**✅ Advantages:**\n- Minimizes wasted space\n- Reduces internal fragmentation\n\n**❌ Disadvantages:**\n- Slower search time\n- Creates many small unusable holes")
        
    with col2:
        st.markdown("### 🏃 First Fit")
        st.success("**✅ Advantages:**\n- Fast allocation\n- Simple implementation\n\n**❌ Disadvantages:**\n- May waste larger blocks\n- Higher external fragmentation")
    
    st.markdown("---")
    
    # Page Replacement Comparison
    st.subheader("📄 Page Replacement Algorithms")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⏰ LRU (Least Recently Used)")
        st.warning("**✅ Advantages:**\n- Better hit ratio\n- Reflects program locality\n- Good performance in practice\n\n**❌ Disadvantages:**\n- Hardware support needed\n- Higher implementation cost")
        
    with col2:
        st.markdown("### 🗓️ FIFO (First In First Out)")
        st.warning("**✅ Advantages:**\n- Simple to implement\n- Low overhead\n\n**❌ Disadvantages:**\n- Belady's anomaly possible\n- May remove frequently used pages")
    
    st.markdown("---")
    
    # Performance Recommendations
    st.subheader("💡 Performance Recommendations")
    
    rec_df = pd.DataFrame({
        "Scenario": ["🎮 Interactive Systems", "📊 Batch Processing", "⚡ Real-time Systems", "🔌 Embedded Systems"],
        "Recommended CPU": ["Round Robin", "FCFS", "Priority-based", "Round Robin"],
        "Recommended Memory": ["Best Fit", "First Fit", "Best Fit", "First Fit"],
        "Recommended Page": ["LRU", "FIFO", "LRU", "FIFO"]
    })
    
    st.dataframe(rec_df, use_container_width=True, hide_index=True)
    
    # Summary metrics
    st.subheader("📈 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.expander("💻 CPU Scheduling Insights"):
            st.write("• Round Robin ensures fairness")
            st.write("• Smaller quantum = better response but more overhead")
            st.write("• FCFS is optimal for batch systems")
    
    with col2:
        with st.expander("💾 Memory Allocation Insights"):
            st.write("• Best Fit minimizes waste but slower")
            st.write("• First Fit is faster but may fragment memory")
            st.write("• External fragmentation is unavoidable")
    
    with col3:
        with st.expander("📄 Page Replacement Insights"):
            st.write("• LRU approaches optimal performance")
            st.write("• FIFO suffers from Belady's anomaly")
            st.write("• More frames ≠ fewer faults in FIFO")