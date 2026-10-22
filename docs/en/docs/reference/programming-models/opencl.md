# OpenCL

**Prerequisites:** Parallel indexing and buffers. **Objective:** Recognize a portable heterogeneous API.

OpenCL represents devices, contexts, queues, memory objects and kernels. Work-items are grouped into work-groups; barriers coordinate a work-group, not arbitrary work-items across the full launch.

Portability of source does not guarantee identical optional features, work-group limits or performance. Query capabilities and check return codes instead of assuming every device matches a CUDA teaching GPU.

Consult [Khronos OpenCL](https://www.khronos.org/opencl/) for specifications. This is reference material, not a validated OpenCL lab. Next, compare [HIP](hip.md).
