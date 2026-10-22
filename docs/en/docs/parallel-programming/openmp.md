# OpenMP

**Prerequisites:** C loops and [shared state](../thread-process/thread.md). **Objective:** Explain a correct parallel reduction.

OpenMP directives tell a compiler how to create worker teams and divide loop iterations. Compile and link with -fopenmp. The course sum uses a static schedule and a private partial sum for each worker:

```c
uint64_t sum = 0;
#pragma omp parallel for reduction(+:sum) schedule(static)
for (long i = 0; i < n; ++i) sum += a[i];
```

The implicit barrier at the end ensures the combined result is ready before validation. A shared sum without reduction would have competing updates. An atomic update could repair correctness but serialize every addition; reduction combines partials less often.

Check all variables: loop indices are private, the input array is shared and read-only, and sum follows reduction semantics. Integer sums use a range that avoids overflow. Floating-point reductions may change summation order, requiring an error tolerance instead of exact equality.

Next, complete the [CPU experiments](parallel-programming-intro.md) with OMP_NUM_THREADS set explicitly.
