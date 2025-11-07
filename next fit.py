# ---------- Next Fit Memory Allocation Algorithm ----------

def next_fit_allocation(processes, blocks):
    total = sum(blocks)   # Total memory
    sum_allocated = 0     # Total allocated memory
    idx = 0               # Start index for next fit
    flag = [False] * len(blocks)  # Track allocated blocks
    display = [-1] * len(blocks)  # Stores which process is allocated to which block

    for i in range(len(processes)):
        allocated = False
        for j in range(len(blocks)):
            block_idx = (idx + j) % len(blocks)  # Wrap around
            if not flag[block_idx] and blocks[block_idx] >= processes[i]:
                sum_allocated += processes[i]
                blocks[block_idx] -= processes[i]  # Reduce block size
                display[block_idx] = i             # Store process index
                flag[block_idx] = True             # Mark block as allocated
                idx = (block_idx + 1) % len(blocks)  # Update next start index
                allocated = True
                break
        if not allocated:
            print(f"No suitable block found for process with size: {processes[i]}")

    print_allocation(display, blocks, sum_allocated, total)


# ---------- Print Allocation and Efficiency ----------
def print_allocation(display, blocks, sum_allocated, total):
    print("\nProcess Allocation in Blocks:")
    for i in range(len(display)):
        if display[i] == -1:
            print(f"Block {i + 1}\tFree")
        else:
            print(f"Block {i + 1}\tProcess {display[i] + 1}")
    print(f"\nMemory Utilization Efficiency: {(sum_allocated * 100.0) / total:.2f}%\n")


# ---------- Main Function ----------
if __name__ == "__main__":
    blocks = [100, 500, 200, 300, 600]   # Memory block sizes
    processes = [212, 417, 112, 426]     # Process sizes

    print("=== Next Fit Memory Allocation ===")
    next_fit_allocation(processes, blocks)
