# Memory Hierarchy and Roofline

**Prerequisites:** FLOPs, bytes and [architecture variants](architectures.md). **Objective:** Calculate bounds with an explicit memory boundary and precision.

Registers and shared memory are close to an SM; caches can serve reused data; HBM supplies global memory capacity and bandwidth. Published HBM bandwidth is a theoretical interface figure. Effective application traffic depends on reuse, access patterns and additional copies.

Arithmetic intensity I is useful FLOPs divided by bytes crossing a stated boundary. With compute peak P and bandwidth B, a roofline gives performance no greater than min(P, B*I). Use a dense scalar or tensor peak that matches the actual operation and precision. Do not apply sparse tensor peaks to a dense scalar CUDA loop.

For FP32 vector addition, two input reads and one output write require at least 12 bytes for one addition, so I=1/12 FLOP/byte. For H100 SXM's sourced 3350 GB/s and 67 TFLOP/s scalar FP32 figures, the bandwidth bound is about 0.279167 TFLOP/s. This idealized calculation excludes launch overhead and host transfers.

Three vectors of n FP32 elements require 12n bytes. Reserving 20% of 80 decimal GB yields n at most 5,333,333,333 in that simplified capacity model. This is not a recommended allocation and is not executed. Workspaces, fragmentation, other processes and runtime overhead can reduce usable capacity.

Use the [calculator source](/hpc_study.io/downloads/source/examples/datacenter/bounds.py) to check arithmetic after working it out by hand. Next, assess [precision and porting](porting.md).
