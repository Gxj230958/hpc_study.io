# HIP

**Prerequisites:** [CUDA kernels](../../gpu/cuda.md). **Objective:** Plan a GPU port beyond syntax translation.

HIP provides a C++ GPU programming interface with familiar launch and memory concepts. Translating API names is only one part of porting; library availability, hardware execution width, numerical behavior and resource limits also matter.

Preserve independent correctness tests, replace unsupported libraries deliberately and profile the actual target. Do not assume CUDA-specific warp behavior or NVIDIA-only profiling tools transfer unchanged.

Consult the [HIP documentation](https://rocm.docs.amd.com/projects/HIP/en/latest/). AMD execution is not validated on the NVIDIA teaching machine. Next, use the [porting checklist](../../datacenter/porting.md).
