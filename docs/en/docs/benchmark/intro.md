# Benchmark Design

**Prerequisites:** [Measurement](../performance-analysis/intro.md). **Objective:** Define a fair comparison.

A result is a tuple: workload, input, correctness criterion, implementation, machine, placement, precision and timing procedure. Changing any member can invalidate a direct comparison. Report both speedup and the cost of obtaining it.

Strong scaling fixes total work; weak scaling fixes work per worker. Amdahl's law gives speedup at most 1/(s+(1-s)/p) for serial fraction s under ideal parallel execution. Communication, imbalance and memory contention can make actual scaling worse.

Keep raw samples, warm-ups and failed correctness runs. Distinguish kernel-only, end-to-end and job completion time, including queueing when it affects the user's objective. Next, compare [HPL](hpl.md) and [HPCG](hpcg.md).
