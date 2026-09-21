"""Two-rank round-trip latency with typed buffers."""
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
if comm.size != 2:
    if comm.rank == 0:
        print("Use exactly two ranks: mpiexec -n 2 python examples/mpi/pingpong.py")
    raise SystemExit(2)
for n in (1, 1024, 1048576):
    data = np.ones(n, dtype=np.uint8)
    for i in range(110):
        if i == 10:
            comm.Barrier()
            start = MPI.Wtime()
        if comm.rank == 0:
            comm.Send(data, dest=1, tag=0)
            comm.Recv(data, source=1, tag=1)
        else:
            comm.Recv(data, source=0, tag=0)
            comm.Send(data, dest=0, tag=1)
    if comm.rank == 0:
        elapsed = MPI.Wtime() - start
        assert np.all(data == 1)
        print(f"bytes={n} round_trip_us={elapsed*1e6/100:.3f} PASS")
