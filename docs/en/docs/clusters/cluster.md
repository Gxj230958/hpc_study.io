# Cluster Operation

**Prerequisites:** MPI ranks and Linux shells. **Objective:** Explain the operational boundary between a local job and remote work.

A cluster typically separates login access, compute allocation, shared storage and scheduling. Those services are not assumed in the portable course: local experiments work without a scheduler, remote filesystem or administrator privileges.

An SSH connection is a way to access a host or start a process. It does not reserve CPUs, memory or GPUs. Verify an allocation before starting a workload. Avoid long computation on shared login hosts.

Remote processes need the same source and compatible environments. A shared path may help, but identical text paths do not prove identical content. Compare hashes, driver/runtime compatibility, Python and PyTorch versions. Next, complete [distributed preflight](distributed.md).
