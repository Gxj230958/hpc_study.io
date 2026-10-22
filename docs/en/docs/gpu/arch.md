# GPU Architecture

**Prerequisites:** CPU threads, memory and [CUDA terminology](intro.md). **Objective:** Relate a kernel's work to the GPU hierarchy.

![CPU and GPU organization, retained from the original CUDA tutorial](images/cuda/cpu-gpu-arch-diff.png)

A streaming multiprocessor (SM) schedules groups of 32 CUDA threads called warps. A block stays on one SM, and several blocks may reside there if registers, shared memory and thread limits allow. Occupancy is the fraction of the SM's supported warps that are active; maximum occupancy is not always maximum performance.

Threads have registers, blocks share explicitly managed shared memory, and all SMs can access global memory through caches. Coalesced accesses let neighboring threads use nearby addresses efficiently. Shared-memory bank conflicts and uncoalesced global access are separate issues.

The RTX 4090 is Ada, not a small H100. Architecture limits, FP64 capability, tensor formats, memory and interconnects differ. Use NVIDIA's [Ada tuning guide](https://docs.nvidia.com/cuda/ada-tuning-guide/) for architecture-specific limits. Next, study [CUDA indexing](cuda.md) and the [datacenter variants](../datacenter/architectures.md).
