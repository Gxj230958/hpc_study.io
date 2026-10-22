# CPU Parallelism

**Prerequisites:** Machine fundamentals; C loops, integer arithmetic and the concept of a shared variable.

**Objective:** Partition a loop, verify a reduction and diagnose a lost update.

A process owns an address space. Threads within that process share memory, so independent loop iterations can run concurrently without copying the array. OpenMP is a compiler-supported API for creating a thread team. A reduction gives each worker a private partial result and combines those results after the loop. It makes the ownership of updates explicit.

## Before You Run

Run commands from the repository root after [setup](../learning/setup.md). Use `source scripts/activate-study.sh` once per shell. These are 10, 20 and 30 minute exercises including interpretation, not promised program runtimes. Use `timeout 180s COMMAND` for individual local runs; allow up to 600 seconds for the native benchmark build. Keep allocations bounded and avoid other workloads during timing.

## Verify Serial and OpenMP Sums {#serial-openmp}

**warm-up · 10 minutes · CPU; GCC/OpenMP; below 1 MiB**

Compute n(n-1)/2 independently in Python and compare both outputs. Inspect the reduction pragma and explain why simply sharing sum would be incorrect.

```bash
make -C examples cpu
env OMP_NUM_THREADS=1 ./build/sum 100003
env OMP_NUM_THREADS=4 ./build/sum 100003
```

**Minimal excerpt:**

```c
uint64_t expected = (uint64_t)n * (n - 1) / 2;
```

**Source:** [examples/cpu/sum.c](/hpc_study.io/downloads/source/examples/cpu/sum.c). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** Serial and threaded totals must equal the independent arithmetic-series formula n(n-1)/2 in 64-bit arithmetic.

**Troubleshooting:** A missing omp.h indicates GCC/OpenMP development support is absent. Build with the provided Makefile; do not remove -fopenmp to silence a linker error.

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    For n=100003 the exact result is 5000250003. The program uses a 64-bit unsigned sum; a 32-bit integer would overflow. One OpenMP thread supplies a useful baseline, though it still includes the OpenMP loop machinery.

## Compare Thread Counts {#thread-counts}

**core · 20 minutes · CPU; at most 4 worker threads; 8 MiB**

Repeat each count five times. Compare median time, speedup T(1)/T(p), and efficiency speedup/p. Keep the input fixed and explain overhead at this small scale.

```bash
env OMP_NUM_THREADS=1 ./build/sum 1000003
env OMP_NUM_THREADS=2 ./build/sum 1000003
env OMP_NUM_THREADS=4 ./build/sum 1000003
```

**Minimal excerpt:**

```c
#pragma omp parallel for reduction(+:sum) schedule(static)
for (long i = 0; i < n; ++i) sum += a[i];
```

**Source:** [examples/cpu/sum.c](/hpc_study.io/downloads/source/examples/cpu/sum.c). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** Every thread count must produce the same exact total. Repeat timings need not show monotonic speedup.

**Troubleshooting:** Oversubscription occurs when runnable threads exceed available CPU capacity. Limit library threads as well and inspect quotas before increasing counts.

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    Every count must produce 500002500003. More threads can lose to startup, synchronization or memory bandwidth. A correct but slower run is useful evidence, not a failed correctness test.

## Diagnose and Repair a Bounded Race {#race-repair}

**stretch · 30 minutes · CPU; Python; two threads; below 32 MiB**

The first command intentionally exits 1. Predict its total before running it. Explain the two barriers, then examine the lock-protected repair and run it.

```bash
python examples/cpu/race.py
python examples/cpu/race.py --repair
```

**Minimal excerpt:**

```python
previous = total
barrier.wait()
total = previous + 1
barrier.wait()
```

**Source:** [examples/cpu/race.py](/hpc_study.io/downloads/source/examples/cpu/race.py). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** The unprotected demonstration intentionally exits 1 with LOST UPDATE. The repaired run must exit 0 with the independently expected 2000 updates.

**Troubleshooting:** Do not put a barrier inside a lock held by only one worker: the other worker could never reach it. The teaching example has fixed work and barrier timeouts.

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    Both workers read the same old value before either stores its increment, so 1000 updates survive where 2000 are expected. The repair holds a lock across the read-modify-write. This is a defined Python logical race; running a C data race would invoke undefined behavior. OpenMP reduction is the preferred repair for the C sum.

## Next Steps

Continue to [the next module](mpi.md). Review [experiment status](../learning/validation.md) before reusing a performance claim.
