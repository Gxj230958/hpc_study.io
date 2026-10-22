# CUDA Kernels

**Prerequisites:** C/C++ arrays and [CUDA orientation](intro.md). **Objective:** Derive safe indexing and check every asynchronous boundary.

The host allocates device memory and copies inputs before launching a kernel. A launch specifies a grid and a block shape. Within the kernel, blockIdx identifies a block, blockDim gives its dimensions and threadIdx identifies a thread within that block.

```cuda
__global__ void add(const float *a, const float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];
}
```

For 256 threads per block, use (n+255)/256 blocks. The guard matters when n is not divisible by 256. Allocate n elements, not a padded size that hides an indexing bug. Test both sides of block boundaries and tiny inputs.

cudaMalloc allocates device storage. cudaMemcpy moves data across the selected memory boundary. The host must not assume a kernel has finished merely because launch returned. Check cudaGetLastError after launch, then check a synchronization or blocking copy so asynchronous execution errors become visible. The supplied CUDA macro reports the expression's source location and error text.

The vector reference is computed on the CPU from known input values. For these binary-fraction additions, exact comparison is appropriate. General floating-point algorithms require stated tolerances, finite-value checks and a justified reference.

Keep allocations small while debugging. A boundary error can otherwise corrupt later results or surface only at synchronization. Next, run [vector boundaries](intro.md#vector-boundaries), then study [shared-memory tiling](cuda-advanced.md).

The original tutorial's derivation and illustrations informed this chapter. Original author: interestingLSY, Peking University supercomputing team.
