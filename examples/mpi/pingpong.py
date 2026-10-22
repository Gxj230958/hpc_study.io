"""Two-rank round-trip latency with typed buffers."""
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
if comm.size != 2:
    if comm.rank == 0:
        print("Use exactly two ranks: mpiexec -n 2 python examples/mpi/pingpong.py")
    raise SystemExit(2)
for n in (1, 1024, 1048576):
    pattern = np.arange(n, dtype=np.uint8)
    data = np.empty(n, dtype=np.uint8)
    for i in range(110):
        if i == 10:
            comm.Barrier()
            start = MPI.Wtime()
        if comm.rank == 0:
            np.add(pattern, np.uint8(i), out=data)
            comm.Send(data, dest=1, tag=0)
            comm.Recv(data, source=1, tag=1)
            if not np.array_equal(data, np.bitwise_not(pattern + np.uint8(i))):
                comm.Abort(1)
        else:
            comm.Recv(data, source=0, tag=0)
            if not np.array_equal(data, pattern + np.uint8(i)):
                comm.Abort(1)
            np.bitwise_not(data, out=data)
            comm.Send(data, dest=0, tag=1)
    if comm.rank == 0:
        elapsed = MPI.Wtime() - start
        print(f"bytes={n} checked_round_trip_us={elapsed*1e6/100:.3f} PASS includes_payload_checks")
