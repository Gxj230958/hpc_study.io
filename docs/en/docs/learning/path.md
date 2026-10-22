# Course Map

Each assessed module has three experiments: a ten-minute warm-up, twenty-minute core exercise and thirty-minute stretch. These durations include reading and interpretation. Setup, orientation and supplementary reference pages are not assessed modules.

| Order | Assessed module | Prerequisites | Deliverable |
| --- | --- | --- | --- |
| 1 | [Machine fundamentals](../hardware/hardware-intro.md) | Shell and arrays | Inventory and stride explanation |
| 2 | [CPU parallelism](../parallel-programming/parallel-programming-intro.md) | Module 1, C loops | Checked sums and race repair |
| 3 | [MPI and networking](../parallel-programming/mpi.md) | Module 2 | Checked messages and scaling table |
| 4 | [CUDA programming](../gpu/intro.md) | Module 2, C/C++ | Boundary and sanitizer evidence |
| 5 | [Measurement and benchmarks](../performance-analysis/intro.md) | Modules 2 and 4 | Repeated timings and validity report |
| 6 | [Scientific computing and ML](../sci-mlsys/intro.md) | Arrays and Module 5 | Residual, error and precision analysis |
| 7 | [Distributed GPUs and clusters](../clusters/platform-intro.md) | Modules 3, 4 and 6 | Collective and DDP correctness evidence |
| 8 | [Datacenter GPU study](../datacenter/intro.md) | Modules 4, 5 and 7 | Sourced hardware and porting plan |

On a CPU-only machine, use the documented CPU/Gloo fallbacks and record CUDA work as unexecuted. One-process NCCL verifies dispatch and collective API use but cannot test GPU-to-GPU communication. Two CPU processes verify distributed semantics but cannot establish NCCL performance.

For each deliverable retain the input, command, environment, raw output, independent reference, interpretation and limitations. Complete all three levels before marking a module complete. Next, [prepare the environment](setup.md).
