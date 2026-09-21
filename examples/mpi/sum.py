"""Distribute uneven intervals and reduce exact integer partial sums."""
import argparse
from mpi4py import MPI

parser = argparse.ArgumentParser()
parser.add_argument("--n", type=int, default=100003)
args = parser.parse_args()
if args.n < 0:
    parser.error("n must be nonnegative")
comm = MPI.COMM_WORLD
rank, size = comm.rank, comm.size
lo, hi = args.n * rank // size, args.n * (rank + 1) // size
comm.Barrier()
start = MPI.Wtime()
partial = sum(range(lo, hi))
total = comm.reduce(partial, op=MPI.SUM, root=0)
elapsed = comm.reduce(MPI.Wtime() - start, op=MPI.MAX, root=0)
ok = None
if rank == 0:
    ok = total == args.n * (args.n - 1) // 2
    print(f"ranks={size} n={args.n} sum={total} max_seconds={elapsed:.9f} {'PASS' if ok else 'FAIL'}")
if not comm.bcast(ok, root=0):
    raise SystemExit(1)
