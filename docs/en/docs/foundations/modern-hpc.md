# Modern HPC

**Prerequisites:** Processes and memory. **Objective:** Decompose an application across compute, communication and storage.

A heterogeneous node combines CPUs, accelerators, host memory, device memory and storage. A distributed application adds network links and coordination among nodes. The slowest stage can change with problem size.

Useful performance includes time spent preparing inputs, moving data, computing and writing results. For repeated workloads, amortized setup may matter; for one-off work, total completion time can dominate.

Numerical reproducibility, deployment constraints and cost belong in the engineering decision alongside FLOPS. Next, study [cluster operation](../clusters/cluster.md).
