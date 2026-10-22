# Consistency and Synchronization

**Prerequisites:** [Memory models](intro.md). **Objective:** Identify the synchronization needed by a producer and consumer.

A producer must finish writing data before publishing that it is ready. The consumer must observe publication through a matching synchronization mechanism before reading the data. Correct synchronization establishes ordering as well as mutual exclusion.

Sequential consistency is a useful reasoning model in which operations appear in a single order consistent with each worker's program order. Real APIs may provide weaker orderings. Start with well-defined locks or high-level collectives before attempting relaxed atomics.

A barrier only helps threads that all participate under the same protocol. Divergent control flow that skips a required barrier can hang. Next, trace both barriers in the [CUDA tiled kernel](../gpu/cuda-advanced.md).
