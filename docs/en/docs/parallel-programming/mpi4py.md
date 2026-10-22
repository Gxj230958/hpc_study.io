# mpi4py

**Prerequisites:** Python arrays and [MPI](mpi.md). **Objective:** Distinguish Python-object messages from typed buffers.

mpi4py exposes communicators, point-to-point messages and collectives. Lowercase methods such as comm.send serialize Python objects. Uppercase Send/Recv operate on typed buffers and avoid Python pickle for payload transport.

The bundled mpi4py-mpich package supplies a matched MPICH runtime and launcher. After activation, inspect which mpiexec is selected and MPI.Get_library_version(). Do not use a system Open MPI launcher for this environment.

Every rank must call collectives in the same logical order. A rank with an empty local partition still participates. Reducing partial integer sums and broadcasting the pass/fail result prevents silent success on only the root rank. Next, run [checked partitioning](mpi.md#rank-partition).

## Optional Remote MPICH Launch

This configuration is not executed in local validation. First complete the
[remote preflight](../clusters/distributed.md): two allocated hosts must resolve
each other's names, permit noninteractive SSH launch, expose the same absolute
course/environment paths, and permit the MPI runtime's data ports. SSH management
access alone does not establish MPI connectivity. Keep one library thread per
rank and avoid placing more ranks than the allocated CPU capacity.

Replace both node names and every absolute path before running:

```bash
timeout 180s env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -launcher ssh -hosts NODE0,NODE1 -n 2 -wdir /ABSOLUTE/COURSE /ABSOLUTE/COURSE/.venv/bin/python examples/mpi/pingpong.py
```

Use the bundled launcher from the activated environment, with matching bundled
MPICH on each host. If the filesystem is not shared, install and hash the same
sources and environment on both hosts first. The checked exchange includes
payload validation; record host placement and do not compare it directly with a
same-host result as if only message size changed. On failure retain both rank
logs and confirm your remote workers have exited. See the [MPICH launcher
manual](https://www.mpich.org/static/docs/latest/www1/mpiexec.html).
