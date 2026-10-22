# OpenACC

**Prerequisites:** C/Fortran loops and accelerator memory. **Objective:** Understand directive-based offload.

OpenACC annotates regions and loops for execution on an accelerator. A data region can retain arrays on the device across multiple operations, avoiding repeated transfers. Correctness depends on both parallel-loop independence and data ownership.

A present clause asserts that data is already available on the device; it does not perform an implicit missing transfer. Reductions and private variables need explicit reasoning just as in OpenMP.

Compiler support and target behavior vary. Consult the [OpenACC specification](https://www.openacc.org/specification) for your toolchain. No OpenACC execution is claimed here. Next, compare explicit [CUDA kernels](../../gpu/cuda.md).
