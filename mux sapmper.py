import threading
import time
from collections import deque

# ------------------ Mutex Version ------------------
class ProducerConsumerWithMutex:
    def __init__(self, capacity=5):
        self.buffer = deque()
        self.capacity = capacity
        self.condition = threading.Condition()

    def produce(self, items):
        for value in range(items):
            with self.condition:
                while len(self.buffer) == self.capacity:
                    self.condition.wait()
                self.buffer.append(value)
                print(f"Mutex Producer produced: {value}")
                self.condition.notify()
            time.sleep(0.5)

    def consume(self, items):
        for _ in range(items):
            with self.condition:
                while not self.buffer:
                    self.condition.wait()
                val = self.buffer.popleft()
                print(f"Mutex Consumer consumed: {val}")
                self.condition.notify()
            time.sleep(0.5)


# ------------------ Semaphore Version ------------------
class ProducerConsumerWithSemaphore:
    def __init__(self, capacity=5):
        self.buffer = deque()
        self.capacity = capacity
        self.empty = threading.Semaphore(capacity)
        self.full = threading.Semaphore(0)
        self.mutex = threading.Semaphore(1)

    def produce(self, items):
        for value in range(items):
            self.empty.acquire()
            self.mutex.acquire()
            self.buffer.append(value)
            print(f"Semaphore Producer produced: {value}")
            self.mutex.release()
            self.full.release()
            time.sleep(0.5)

    def consume(self, items):
        for _ in range(items):
            self.full.acquire()
            self.mutex.acquire()
            val = self.buffer.popleft()
            print(f"Semaphore Consumer consumed: {val}")
            self.mutex.release()
            self.empty.release()
            time.sleep(0.5)


# ------------------ Main Simulation ------------------
def main():
    items_to_produce = 10

    # Mutex version
    print("Running Producer-Consumer with Mutex...")
    pc_mutex = ProducerConsumerWithMutex()

    t1 = threading.Thread(target=pc_mutex.produce, args=(items_to_produce,))
    t2 = threading.Thread(target=pc_mutex.consume, args=(items_to_produce,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Semaphore version
    print("\nRunning Producer-Consumer with Semaphore...")
    pc_semaphore = ProducerConsumerWithSemaphore()

    t3 = threading.Thread(target=pc_semaphore.produce, args=(items_to_produce,))
    t4 = threading.Thread(target=pc_semaphore.consume, args=(items_to_produce,))

    t3.start()
    t4.start()
    t3.join()
    t4.join()

    print("\nSimulation Completed!")


if __name__ == "__main__":
    main()
