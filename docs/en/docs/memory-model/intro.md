# Memory Models

**Prerequisites:** Threads and shared variables. **Objective:** Separate storage sharing from ordering guarantees.

A memory model defines which values a concurrent read may observe and what ordering synchronization establishes. A cache-coherent machine does not automatically make a sequence of reads and writes atomic. Compiler optimizations and hardware execution also affect ordering.

Use the language's synchronization primitives: OpenMP reductions and barriers, C/C++ atomics and mutexes, or Python locks. A C/C++ data race on ordinary storage can make program behavior undefined; adding volatile does not repair it.

Reason in terms of ownership and happens-before relationships. Identify who writes each location and what event makes that write visible before a reader uses it. Next, study [consistency](consistency.md) and [cache behavior](cache.md).
