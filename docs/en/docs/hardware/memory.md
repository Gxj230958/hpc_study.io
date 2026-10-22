# Memory

**Prerequisites:** Arrays and [processors](processor.md). **Objective:** Estimate storage and distinguish capacity, latency and bandwidth.

Capacity tells you whether data fits. Latency tells you how long one access waits. Bandwidth tells you how many bytes can cross a boundary per second. A large capacity does not imply high bandwidth. Registers, caches, host DRAM and GPU memory occupy different points in this hierarchy.

An array of n FP64 values needs 8n bytes, before allocator metadata and temporary arrays. Matrix multiplication may require inputs, output, workspace and reference data simultaneously. Budget the peak live set, including framework allocations, rather than just a single tensor.

Memory controllers transfer cache lines. Adjacent accesses tend to use more of each line; irregular accesses may spend bandwidth on unused values. Huge pages and NUMA placement can change translation and locality, but do not change the algorithm's required bytes. Next, run [the memory experiments](hardware-intro.md#memory-patterns).
