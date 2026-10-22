# Tiling and Reduction

**Prerequisites:** [Safe CUDA indexing](cuda.md). **Objective:** Explain shared-memory reuse and barrier placement.

For C=AB, output C[row,col] sums A[row,k]*B[k,col]. A naive kernel repeatedly reads global memory for neighboring outputs. The course kernel loads a 16x16 tile from each input into shared memory, then reuses it for sixteen multiply-add steps.

All threads load one element from each tile. Out-of-range input coordinates load zero. The first __syncthreads ensures the complete tile is available. After consuming it, a second barrier prevents a faster thread from overwriting values a slower thread still needs. Threads outside the valid output region still participate in tile loading and barriers, but skip their final store.

The reduction kernel loads one value per thread into a 256-element shared array, padding the tail with zero. At each tree step, half the threads combine pairs, followed by a barrier. Thread zero writes the block's partial sum. The host combines block results and compares with an independent sum.

Shared-memory reuse has a resource cost: larger tiles can consume more shared memory and registers and reduce the number of resident blocks. The teaching kernel does not use Tensor Cores and should not be compared with a published tensor-throughput peak. Library GEMM is the production baseline.

Run [memcheck, synccheck and racecheck](intro.md#tiled-matmul) on both aligned and unaligned shapes. A passing sanitizer run supplements numerical checks; it does not prove arbitrary inputs safe.
