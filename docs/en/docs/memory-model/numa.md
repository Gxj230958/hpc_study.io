# NUMA

**Prerequisites:** Caches and processes. **Objective:** Explain why memory placement matters on multiple sockets.

Non-uniform memory access means access cost depends on which socket owns a physical page and which socket runs the thread. Local and remote memory may differ in latency and available bandwidth. A single-socket allocation cannot validate remote-socket behavior.

Many systems place a page near the thread that first writes it. Parallel initialization with the same partition used for computation can improve placement. Thread migration and shared allocations can undo a simple first-touch plan.

Inspect CPU and memory topology before requesting binding options. Record binding, page placement and job allocation with results; do not assume every machine provides the same numactl permissions or topology. Next, revisit [thread scaling](../parallel-programming/parallel-programming-intro.md#thread-counts).
