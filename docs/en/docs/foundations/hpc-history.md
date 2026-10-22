# HPC History

**Prerequisites:** [What is HPC?](what-is-hpc.md). **Objective:** Connect historical architectures with current tradeoffs.

Vector machines emphasized operations over long arrays. Distributed-memory systems combined many machines through message passing. Commodity multicore processors and accelerators added more parallelism within each node.

These approaches coexist: contemporary applications may use MPI among nodes, threads within a CPU and CUDA within each GPU. Moving data has remained a central cost even as arithmetic throughput has grown.

Historical peak performance and dated validation logs describe their original systems. They are not current measurements. Next, read [modern HPC](modern-hpc.md) and distinguish architectural capability from an application's result.
