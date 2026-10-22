# Nsight Systems

**Prerequisites:** Correct CUDA execution and [timing boundaries](../performance-analysis/intro.md). **Objective:** Locate transfers and launches on a timeline.

Nsight Systems records activity over time: CPU work, CUDA API calls, memory copies and GPU kernels. A gap between kernels can be caused by host work, dependencies, synchronization or resource contention. Inspect surrounding events before assigning a cause.

```bash
nsys profile --force-overwrite true --trace=cuda --output=build/course-profile ./build/cuda_labs
nsys stats --report cuda_gpu_kern_sum,cuda_gpu_mem_time_sum build/course-profile.nsys-rep
```

These commands overwrite only the named course trace. The program's independent correctness checks still run. Save its output together with the trace and tool version.

Nsight Compute provides kernel-level counters and resource analysis; it answers a different question from a system timeline and can require additional permissions. Start with the [transfer profiling experiment](../performance-analysis/intro.md#profile-transfers), then choose counters for a specific hypothesis.
