# Precision, Profiling and Porting

**Prerequisites:** [CUDA tiling](../gpu/cuda-advanced.md) and [numerical checks](../sci-mlsys/intro.md). **Objective:** Separate compatibility work from target-specific optimization.

FP64, FP32, TF32, FP16, BF16 and FP8 differ in range, precision and supported operations. Tensor Core throughput applies to supported matrix operations with specific input and accumulation formats. A table marked with sparsity cannot be used as a dense throughput claim.

Preserve a small independent reference and declared tolerances before changing precision. Check finite outputs, residuals and final application quality. BF16's exponent range does not give it FP32's significand precision. FP8 paths need scaling and application-level validation; converting a tensor alone does not guarantee an efficient kernel.

Build code for the target architecture and verify library/runtime/driver compatibility. Keep a portable baseline first. Hopper features such as Tensor Memory Accelerator and thread-block clusters may need explicit programming and do not exist on the Ada teaching card in the same form. Use the [Hopper tuning guide](https://docs.nvidia.com/cuda/archive/12.4.1/hopper-tuning-guide/index.html) for a specific optimization.

On target hardware, begin with Nsight Systems to locate transfers and idle intervals, then Nsight Compute for a selected kernel's resource/counter hypothesis. Record permissions and collect actual target data before changing launch geometry or assuming a new bottleneck. Next, plan [fabric and partition requirements](topology.md).
