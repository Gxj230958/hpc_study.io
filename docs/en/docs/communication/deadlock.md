# Deadlock

**Prerequisites:** [Message models](model.md). **Objective:** Identify circular waits and remove reliance on buffering.

If both ranks issue a blocking send before either posts a receive, small messages may appear to work because of buffering. A larger message can expose the circular wait. Successful small-input tests do not prove the protocol safe.

Arrange complementary ordering, use Sendrecv, or post receives and sends nonblockingly and complete every request. At larger scale, draw the dependency graph and ensure the protocol cannot form a cycle.

Collective mismatches can also hang: one rank calls a broadcast while another calls an AllReduce, or one exits on a local error. Use timeouts during development and preserve all rank logs. Next, inspect the ordering in [ping-pong](../parallel-programming/mpi.md#checked-pingpong).
