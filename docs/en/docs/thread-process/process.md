# Processes

**Prerequisites:** [Execution models](intro.md). **Objective:** Explain isolation and process launch costs.

The operating system maps a process's virtual addresses to physical pages. Two processes can use the same numerical address without sharing the same storage. Interprocess communication therefore needs messages or explicitly shared mappings.

Starting a fresh Python worker loads modules and initializes runtime state. These startup costs can dominate tiny jobs. Measure startup separately from steady-state computation, and state which interval your benchmark includes.

A hostname identifies a host; a PID identifies an operating-system process; an MPI rank identifies a member of a communicator. These identifiers are not interchangeable. Next, use [MPI](../parallel-programming/mpi.md) to launch checked processes.
