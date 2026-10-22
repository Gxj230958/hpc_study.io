# Processors

**Prerequisites:** [Machine fundamentals](hardware-intro.md). **Objective:** Distinguish cores, SIMD lanes and hardware threads.

A CPU core pipelines instructions and may issue several independent operations in one cycle. Instruction-level parallelism depends on dependencies: a chain of dependent additions is less flexible than several independent accumulators. SIMD (single instruction, multiple data) applies one operation to several values in a vector register. OpenMP threads and SIMD lanes are different levels of parallel execution.

Simultaneous multithreading exposes more than one hardware thread per core. It can fill otherwise idle execution slots but does not double caches, execution units or memory bandwidth. Report physical cores and allowed logical CPUs separately. A cgroup quota can limit CPU time even when affinity lists many CPUs.

Compiler vectorization depends on aliasing, alignment, loop structure and numerical semantics. Start with correct code and inspect compiler reports before adding architecture-specific instructions. Next, compare [OpenMP](../parallel-programming/openmp.md) thread counts.
