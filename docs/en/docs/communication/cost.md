# Communication Cost

**Prerequisites:** [Message models](model.md). **Objective:** Interpret latency and bandwidth without conflating them.

A simple model writes time as alpha + bytes/beta, where alpha is startup latency and beta is effective bandwidth. It omits contention, protocol thresholds, copies and synchronization, so treat it as an approximation.

Small messages often emphasize startup. Large messages can expose a throughput limit, but checked ping-pong also includes buffer preparation and validation. Dividing two payload transfers by round-trip time yields an effective rate for that procedure, not a direct hardware link specification.

Collectives depend on rank count, topology and algorithm. A fast same-host ping-pong result cannot predict two-node AllReduce. Next, run the [checked ping-pong lab](../parallel-programming/mpi.md#checked-pingpong) and state placement explicitly.
