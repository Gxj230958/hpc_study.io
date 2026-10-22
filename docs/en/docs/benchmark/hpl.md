# HPL

**Prerequisites:** Dense linear algebra and [benchmark design](intro.md). **Objective:** Interpret a dense benchmark's correctness and scope.

High Performance Linpack solves a dense linear system using distributed LU factorization. Most arithmetic is matrix multiplication, making it sensitive to optimized BLAS, process grids and block sizes. A good HPL score does not predict every scientific application's performance.

The teaching input uses a small matrix and one MPI process. Its system MPICH/OpenBLAS build is isolated from bundled mpi4py. The script retains the source archive hash, build output and run output. Check the scaled residual and the count of passed tests before discussing FLOPS.

HPL's dense matrix alone needs approximately 8N² bytes in double precision, plus workspace. Do not copy a production N onto a laptop. Run the [reference workload experiment](../performance-analysis/intro.md#reference-benchmarks). Its output is a teaching result, not a submission.
