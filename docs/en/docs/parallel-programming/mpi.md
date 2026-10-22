# MPI and Networking

**Prerequisites:** CPU parallelism; activate the uv environment and use its bundled MPICH launcher.

**Objective:** Verify uneven partitions, measure checked messages and distinguish strong from weak scaling.

MPI is an interface for communication among processes. A rank is a process's identifier inside a communicator, which is a group of participating processes. Ranks have separate memory, unlike threads. A hostname identifies a machine, not a rank: several ranks may share one host. Start locally before introducing SSH launch, remote paths, interfaces and ports.

## Before You Run

Run commands from the repository root after [setup](../learning/setup.md). Use `source scripts/activate-study.sh` once per shell. These are 10, 20 and 30 minute exercises including interpretation, not promised program runtimes. Use `timeout 180s COMMAND` for individual local runs; allow up to 600 seconds for the native benchmark build. Keep allocations bounded and avoid other workloads during timing.

## Verify Rank Partitioning {#rank-partition}

**warm-up · 10 minutes · CPU; bundled MPICH; 3 ranks; under 256 MiB**

Write down [nr/p, n(r+1)/p) with integer division for every rank. Verify the union is complete and the intervals do not overlap, including ranks with no elements.

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 3 python examples/mpi/sum.py --n 10
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 4 python examples/mpi/sum.py --n 2
```

**Minimal excerpt:**

```python
lo, hi = n * rank // size, n * (rank + 1) // size
partial = sum(range(lo, hi))
```

**Source:** [examples/mpi/sum.py](/hpc_study.io/downloads/source/examples/mpi/sum.py). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** All elements must be covered once, and the reduced total must match the exact formula, including empty partitions.

**Troubleshooting:** If ranks all report size 1 or the job hangs, check which mpiexec and Python are selected. Mixing Open MPI and MPICH is unsupported; source scripts/activate-study.sh and inspect MPI.Get_library_version().

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    For n=10 and p=3 the intervals are [0,3), [3,6), [6,10) and the total is 45. With n=2 and four ranks, some intervals are empty but all ranks still participate in the collective. Reduction checks the independent arithmetic-series formula.

## Measure Checked Ping-Pong Messages {#checked-pingpong}

**core · 20 minutes · CPU; bundled MPICH; exactly 2 ranks; under 256 MiB**

Run three message sizes with ten warm-ups and one hundred measured round trips. Inspect the rank-dependent send/receive ordering and payload checks. Report round-trip time and identify the placement.

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 2 python examples/mpi/pingpong.py
```

**Minimal excerpt:**

```python
np.add(pattern, np.uint8(i), out=data)
comm.Send(data, dest=1, tag=0)
comm.Recv(data, source=1, tag=1)
```

**Source:** [examples/mpi/pingpong.py](/hpc_study.io/downloads/source/examples/mpi/pingpong.py). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** Each message size reports PASS only after both ranks validate changing position-dependent payloads. The reported round-trip time includes these checks.

**Troubleshooting:** Exactly two ranks are required. Remote launch needs resolved hostnames, SSH access, identical environments and permitted dynamic MPI ports. A two-sided blocking send/send sequence can deadlock for large messages.

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    The sender transmits a position-dependent byte pattern and the receiver verifies it, returns its complement, and the sender verifies the reply. Different iterations change the pattern. A local run measures same-host transport, often shared memory, and cannot establish Ethernet bandwidth.

## Compare Strong and Weak Scaling {#mpi-scaling}

**stretch · 30 minutes · CPU; bundled MPICH; at most 4 ranks; under 512 MiB**

Tabulate median maximum-rank times. Fixed total n is strong scaling; fixed n per rank is weak scaling. Explain why these Python integer loops are teaching workloads rather than network benchmarks.

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 1 python examples/mpi/scaling.py --mode strong
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 2 python examples/mpi/scaling.py --mode strong
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 4 python examples/mpi/scaling.py --mode strong
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 1 python examples/mpi/scaling.py --mode weak
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 2 python examples/mpi/scaling.py --mode weak
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 4 python examples/mpi/scaling.py --mode weak
```

**Minimal excerpt:**

```python
n = args.n if args.mode == 'strong' else args.n * c.size
assert total == n * (n - 1) // 2
```

**Source:** [examples/mpi/scaling.py](/hpc_study.io/downloads/source/examples/mpi/scaling.py). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** Every repetition checks an exact integer total. Compare fixed-total and fixed-per-rank work using the maximum rank's elapsed time.

**Troubleshooting:** Use one numerical-library thread per rank. Four local ranks cannot reveal the cost of a second machine or a congested switch.

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    Strong efficiency is T(1)/(p*T(p)). Weak efficiency is T(1)/T(p) with per-rank work held fixed. The independent exact sum checks every repetition. Startup is outside the timed region; collectives and load imbalance remain inside. Small jobs may show no speedup.

## Next Steps

Continue to [the next module](../gpu/intro.md). Review [experiment status](../learning/validation.md) before reusing a performance claim.
