# Scheduling

**Prerequisites:** Cluster allocations and GPU visibility. **Objective:** Request the resources a workload actually uses.

A scheduler assigns jobs to resources. Typical request dimensions include nodes, tasks per node, CPUs per task, memory, GPUs, wall time and partition/account. Syntax and policy vary by site; the portable experiments do not require a scheduler.

For two-node DDP, request two allocated nodes with one GPU and enough CPU capacity on each. Start one torchrun launcher per node and one worker per GPU. Do not accidentally multiply worker counts through both a scheduler's task launcher and torchrun.

A MIG allocation is a specific logical GPU profile, not a full accelerator. Request a compatible profile and verify CUDA visibility. Queue delay, preemption and checkpoint/restart policy belong in the completion-time estimate. Next, write a [datacenter operations plan](../datacenter/operations.md).
