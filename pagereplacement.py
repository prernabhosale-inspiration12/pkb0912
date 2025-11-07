from collections import deque

# ---------- Common Base Class ----------
class CommonUtils:
    def __init__(self):
        self.hits = 0
        self.faults = 0
        self.pages_reference = []

        # Input reference string
        prs = int(input("Enter the no.of numbers in the page reference string: "))
        for _ in range(prs):
            n = int(input("Enter the number: "))
            self.pages_reference.append(n)

        # Input frames
        f = int(input("Enter the no.of frames: "))
        self.result = [[-1 for _ in range(prs)] for _ in range(f)]

    def show_result(self):
        print("\nPage Frame Table:")
        for row in self.result:
            print(" ".join(str(x) for x in row))
        print(f"No.of hits: {self.hits}")
        print(f"No.of faults: {self.faults}\n")

    def perform_algorithm(self):
        raise NotImplementedError


# ---------- FIFO Algorithm ----------
class FIFO(CommonUtils):
    def __init__(self):
        super().__init__()
        self.queue = deque()

    def perform_algorithm(self):
        j = 0
        ref = self.pages_reference.copy()
        while ref:
            num = ref.pop(0)
            frames = [self.result[i][j] for i in range(len(self.result))]
            if num in frames:
                self.hits += 1
                is_fault = False
            else:
                self.faults += 1
                is_fault = True
                if -1 in frames:
                    idx = frames.index(-1)
                    self.result[idx][j] = num
                    self.queue.append(num)
                else:
                    old = self.queue.popleft()
                    idx = frames.index(old)
                    self.result[idx][j] = num
                    self.queue.append(num)

            j += 1
            if j < len(self.result[0]):
                for x in range(len(self.result)):
                    self.result[x][j] = self.result[x][j - 1]


# ---------- LRU Algorithm ----------
class LRU(CommonUtils):
    def __init__(self):
        super().__init__()
        self.recorder = deque()

    def perform_algorithm(self):
        j = 0
        ref = self.pages_reference.copy()
        while ref:
            num = ref.pop(0)
            frames = [self.result[i][j] for i in range(len(self.result))]
            if num in frames:
                self.hits += 1
                self.recorder.remove(num)
                self.recorder.append(num)
                is_fault = False
            else:
                self.faults += 1
                is_fault = True
                if -1 in frames:
                    idx = frames.index(-1)
                    self.result[idx][j] = num
                else:
                    old = self.recorder.popleft()
                    idx = frames.index(old)
                    self.result[idx][j] = num
                self.recorder.append(num)

            j += 1
            if j < len(self.result[0]):
                for x in range(len(self.result)):
                    self.result[x][j] = self.result[x][j - 1]


# ---------- OPT (Optimal) Algorithm ----------
class OPT(CommonUtils):
    def __init__(self):
        super().__init__()

    def perform_algorithm(self):
        j = 0
        ref = self.pages_reference.copy()
        while ref:
            num = ref.pop(0)
            frames = [self.result[i][j] for i in range(len(self.result))]
            if num in frames:
                self.hits += 1
            elif -1 in frames:
                self.faults += 1
                idx = frames.index(-1)
                self.result[idx][j] = num
            else:
                self.faults += 1
                # Find the page not used for the longest future duration
                future = ref.copy()
                next_use = []
                for f in frames:
                    if f in future:
                        next_use.append(future.index(f))
                    else:
                        next_use.append(float('inf'))
                replace_index = next_use.index(max(next_use))
                self.result[replace_index][j] = num

            j += 1
            if j < len(self.result[0]):
                for x in range(len(self.result)):
                    self.result[x][j] = self.result[x][j - 1]


# ---------- Main Function ----------
def main():
    print("*********************************** FIFO *******************************************")
    fifo = FIFO()
    fifo.perform_algorithm()
    fifo.show_result()

    print("*********************************** LRU *******************************************")
    lru = LRU()
    lru.perform_algorithm()
    lru.show_result()

    print("*********************************** OPT *******************************************")
    opt = OPT()
    opt.perform_algorithm()
    opt.show_result()


if __name__ == "__main__":
    main()
