# MLPerf

**Prerequisites:** Training loops and measurement. **Objective:** Understand why a tiny training demo is not a standardized ML result.

MLPerf defines workloads, datasets, accuracy targets and measurement rules for machine-learning systems. Training and inference measure different outcomes, and latency-sensitive serving differs from offline throughput.

The course's synthetic regression and 512x512 matrix multiplication do not implement MLPerf. They validate dispatch, numerical behavior and timing discipline. Do not label their outputs as standardized benchmark scores.

For an actual submission consult the applicable [MLCommons benchmark rules](https://mlcommons.org/benchmarks/) and record the exact benchmark version and division. Next, run [scientific computing and ML](../sci-mlsys/intro.md).
