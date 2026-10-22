# HPCG

**Prerequisites:** Sparse operations and [benchmark design](intro.md). **Objective:** Separate numerical checks from official run validity.

HPCG combines sparse matrix-vector products, vector updates, reductions and multigrid preconditioning in a conjugate-gradient workload. It stresses memory access and communication differently from HPL.

The repository pins a source revision and supplies a small, short input. Inspect convergence, symmetry and residual reports. A line saying the numerical result is valid does not mean a run satisfies official runtime, problem-size or submission rules.

The benchmark has official requirements that should be checked against the [HPCG project](https://www.hpcg-benchmark.org/). The course's deliberately short run is educational. Keep source revision, input and output together. Next, compare it with [the sparse residual exercise](../sci-mlsys/intro.md#sparse-residual).
