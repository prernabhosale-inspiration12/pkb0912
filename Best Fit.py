def find_block_best_fit(blocks, allocated, size):
    idx = -1
    for j in range(len(blocks)):
        if not allocated[j] and blocks[j] >= size:
            if idx == -1 or blocks[j] < blocks[idx]:
                idx = j  # Choose the smallest suitable block
    return idx


def best_fit_allocation(processes, blocks):
    allocated = [False] * len(blocks)
    display = [-1] * len(blocks)

    print("=== Best Fit Memory Allocation ===")
    for i in range(len(processes)):
        block_index = find_block_best_fit(blocks, allocated, processes[i])
        if block_index != -1:
            allocated[block_index] = True
            blocks[block_index] -= processes[i]  # Reduce block size
            display[block_index] = i
            print(f"Process {i + 1} of size {processes[i]} allocated to block {block_index + 1}")
        else:
            print(f"Process {i + 1} of size {processes[i]} not allocated")

    print("\nBlock allocation status:")
    for i in range(len(display)):
        status = f"Process {display[i] + 1}" if display[i] != -1 else "Free"
        print(f"Block {i + 1}: {status}")


if __name__ == "__main__":
    blocks = [100, 500, 200, 300, 600]   # Memory block sizes
    processes = [212, 417, 112, 426]     # Process sizes
    best_fit_allocation(processes, blocks)
