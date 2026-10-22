# mpi4py

**Prerequisites:** Python arrays and [MPI](mpi.md). **Objective:** Distinguish Python-object messages from typed buffers.

mpi4py exposes communicators, point-to-point messages and collectives. Lowercase methods such as comm.send serialize Python objects. Uppercase Send/Recv operate on typed buffers and avoid Python pickle for payload transport.

The bundled mpi4py-mpich package supplies a matched MPICH runtime and launcher. After activation, inspect which mpiexec is selected and MPI.Get_library_version(). Do not use a system Open MPI launcher for this environment.

Every rank must call collectives in the same logical order. A rank with an empty local partition still participates. Reducing partial integer sums and broadcasting the pass/fail result prevents silent success on only the root rank. Next, run [checked partitioning](mpi.md#rank-partition).
