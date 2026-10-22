"""Repeat the exact checked partition sum at fixed and per-rank problem sizes."""
import argparse
import statistics
from mpi4py import MPI

p = argparse.ArgumentParser()
p.add_argument("--mode", choices=["strong", "weak"], required=True)
p.add_argument("--n", type=int, default=200003)
args = p.parse_args()
if not 1 <= args.n <= 10000000:
    p.error("n must be in [1, 10000000]")
c = MPI.COMM_WORLD
n = args.n if args.mode == "strong" else args.n * c.size
lo, hi = n * c.rank // c.size, n * (c.rank + 1) // c.size
times = []
for _ in range(6):
    c.Barrier()
    start = MPI.Wtime()
    total = c.allreduce(sum(range(lo, hi)), op=MPI.SUM)
    elapsed = c.allreduce(MPI.Wtime() - start, op=MPI.MAX)
    assert total == n * (n - 1) // 2
    times.append(elapsed)
if c.rank == 0:
    print(f"mode={args.mode} ranks={c.size} n={n} median_seconds={statistics.median(times[1:]):.9f} PASS")
