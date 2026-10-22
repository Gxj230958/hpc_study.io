# Task Granularity

**Prerequisites:** [Threads](thread.md). **Objective:** Choose work units large enough to amortize scheduling.

Granularity is the amount of useful work in a task. Tiny tasks pay scheduling overhead repeatedly. Very large tasks can leave most workers idle while one finishes the last expensive item. The right size depends on compute cost, memory traffic and task variability.

Static scheduling assigns predictable ranges ahead of time and usually has low overhead. Dynamic scheduling lets workers request more work and can balance irregular tasks at a coordination cost. Try one change at a time and retain correctness checks.

Nested parallel libraries can accidentally multiply thread counts. With four MPI ranks and four BLAS threads each, sixteen threads may compete for a four-core allocation. Next, examine [OpenMP](../parallel-programming/openmp.md) scheduling.
