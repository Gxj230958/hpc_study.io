# Distributed Preflight and Launch

**Prerequisites:** [MPI](../parallel-programming/mpi.md), CUDA and an allocated host. **Objective:** Verify remote prerequisites before launching workers.

The [hardware profile](/hpc_study.io/downloads/source/course/hardware-profile.json) records what is known. Node count, remote GPU counts, network speed/topology, software versions, SSH access, scheduler and permitted ports remain unresolved. Do not infer them from the local validation host.

## Ranks, Threads, Hosts and Ports

A rank is a process in a distributed group. Each rank may create threads. A hostname resolves to a machine's address. SSH uses its configured management port to start a shell; collective data does not automatically travel through that SSH connection.

The rendezvous endpoint lets torchrun workers discover membership. Additional TCP ports can carry collective data. Ask the allocation's network policy which data ports are permitted; allowing port 29500 alone may not suffice. These examples assume two mutually reachable allocated nodes with ordinary TCP/Ethernet. InfiniBand, NVLink, peer access and a scheduler are not required.

## Verify on Each Allocated Node

```bash
hostname
ip -br address
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.device_count())"
sha256sum examples/distributed/collectives.py uv.lock
```

Record the interface on each node and the reachable address of node 0. Interfaces can have different names across nodes. Ensure both nodes agree on source hash, selected extra and dependencies. Verify DNS, SSH access if using SSH to open the remote shell, and the chosen port policy before launch.

## One Node, One GPU

Run the [one-process experiment](platform-intro.md#one-process). Its formula checks reduction semantics; it cannot transfer data between different GPUs.

## One Node, Two GPUs

Use the [two-GPU experiment](platform-intro.md#multi-gpu) only when two GPUs are allocated and visible. LOCAL_RANK selects the device; CUDA_VISIBLE_DEVICES can remap the allocation's device IDs. Do not override a scheduler's device isolation. The CPU/Gloo fallback creates two processes and verifies the same formula.

## Two Nodes

Open a shell on each allocated node. Replace NODE0_IP with node 0's reachable address, YOUR_INTERFACE with that node's TCP interface, and course-UNIQUE-ID with the same unique job ID on both nodes. Run rank-0 and rank-1 commands from the [training experiment](platform-intro.md#two-node-training) on their respective nodes.

The NCCL_SOCKET_IFNAME value begins with an equals sign to request an exact interface match; in env syntax the visible double equals is intentional. NCCL_IB_DISABLE=1 selects a TCP baseline rather than relying on InfiniBand. GLOO_SOCKET_IFNAME configures the CPU path. Do not set a loopback interface for cross-node traffic.

torchrun's c10d rendezvous assigns global ranks; --node-rank records the intended node role but static rank numbering should not be assumed with dynamic rendezvous. The same job ID and endpoint are essential. With one worker per node, the global world size is two.

## DDP Correctness and Failure Handling

The program checks AllReduce against p(p+1)/2 on every rank. For training, each rank sees a different equal-size shard; five SGD updates must match a separate CPU model trained on the concatenated global batch. Merely checking that all replicas match would miss duplicated-data and normalization errors.

A 60-second process-group timeout bounds collective waits. An outer timeout 180s bounds launch failures as well. On failure, stop both launches, preserve both logs and verify only your own workers have exited. Do not disable interface restrictions or open arbitrary ports to make a hang disappear.

The one-node two-process fallback validates DDP semantics. It cannot validate Ethernet, remote rendezvous, remote driver compatibility or two-node performance. Next, inspect [scheduling](scheduling.md).
