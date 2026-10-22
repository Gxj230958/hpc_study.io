# What Is HPC?

**Prerequisites:** Basic programming. **Objective:** Define a useful HPC problem.

High-performance computing uses parallel hardware and efficient algorithms to solve workloads whose time, memory or throughput requirements exceed a convenient serial approach. A faster answer is useful only when its correctness is established.

Parallelism can exist inside an instruction, among CPU threads, across GPU threads or between networked processes. Each level adds constraints on data movement and synchronization. A cluster is a group of cooperating machines; owning a cluster does not make a serial algorithm parallel.

Start with the question, input size and acceptable numerical error. Next, take [machine fundamentals](../hardware/hardware-intro.md).
