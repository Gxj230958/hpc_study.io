"""Force a lost update without C/C++ undefined behavior; then repair it."""
import argparse
import threading

parser = argparse.ArgumentParser()
parser.add_argument("--repair", action="store_true")
args = parser.parse_args()
total = 0
iterations = 1000
barrier = threading.Barrier(2, timeout=10)
lock = threading.Lock()


def worker():
    global total
    for _ in range(iterations):
        if args.repair:
            with lock:
                total += 1
        else:
            previous = total
            barrier.wait()
            total = previous + 1
            barrier.wait()


threads = [threading.Thread(target=worker) for _ in range(2)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join(timeout=30)
assert not any(thread.is_alive() for thread in threads)
expected = 2 * iterations
print(f"total={total} expected={expected} {'PASS' if total == expected else 'LOST UPDATE'}")
raise SystemExit(0 if total == expected else 1)
