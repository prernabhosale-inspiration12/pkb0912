# Worst Fit Memory Allocation in Python

def find_block_worst_fit(blocks, allocated, size):
    """Find index of largest block that can fit the process."""
    idx = -1
    for j in range(len(blocks)):
        if not allocated[j] and blocks[j] >= size:
            if idx == -1 or blocks[j] > blocks[idx]:
                idx = j
    return idx


def worst_fit_allocation(processes, blocks):
    allocated = [False] * len(blocks)
    display = [-1] * len(blocks)

    print("=== Worst Fit Memory Allocation ===")
    for i, process_size in enumerate(processes):
        block_index = find_block_worst_fit(blocks, allocated, process_size)
        if block_index != -1:
            allocated[block_index] = True
            blocks[block_index] -= process_size
            display[block_index] = i
            print(f"Process {i+1} of size {process_size} allocated to Block {block_index+1}")
        else:
            print(f"Process {i+1} of size {process_size} not allocated")

    print("\nBlock allocation status:")
    for i, val in enumerate(display):
        if val == -1:
            print(f"Block {i+1}: Free")
        else:
            print(f"Block {i+1}: Process {val+1}")


# ---- Main ----
if __name__ == "__main__":
    blocks = [100, 500, 200, 300, 600]   # Memory block sizes
    processes = [212, 417, 112, 426]     # Process sizes

    worst_fit_allocation(processes, blocks)
