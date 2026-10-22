# Distributed GPUs and Clusters

**Prerequisites:** MPI ranks, CUDA, training and the selected uv extra.

**Objective:** Separate one-process, multiple-GPU and two-node evidence.

A node is one machine in a distributed job. torchrun launches one process per local worker and coordinates discovery through a rendezvous endpoint. NCCL handles CUDA collectives; Gloo provides a CPU fallback. Check [the remote preflight](distributed.md) before replacing the placeholders below. Use a unique rendezvous ID per job, the same endpoint on all nodes, and one worker per visible GPU. Wrap launches in timeout 180s and capture logs on both nodes.

## One Process {#one-process}

**warm-up · 10 minutes · One CUDA GPU; CPU/Gloo fallback; under 1 GiB**

Verify one-process collective initialization and explain why its sum is 1.

```bash
env OMP_NUM_THREADS=1 NCCL_IB_DISABLE=1 NCCL_SOCKET_IFNAME==lo torchrun --nnodes=1 --nproc-per-node=1 --rdzv-backend=c10d --rdzv-endpoint=127.0.0.1:29621 --rdzv-id=course-one --max-restarts=0 examples/distributed/collectives.py --backend nccl
```

**Source:** [examples/distributed/collectives.py](/hpc_study.io/downloads/source/examples/distributed/collectives.py).

**Expected behavior and correctness:** Every rank asserts the arithmetic-series result p(p+1)/2. With one rank, this is 1. NCCL dispatch is real, but no peer GPU or network communication is tested.

### Local Fallback

```bash
env OMP_NUM_THREADS=1 GLOO_SOCKET_IFNAME=lo torchrun --nnodes=1 --nproc-per-node=1 --rdzv-backend=c10d --rdzv-endpoint=127.0.0.1:29621 --rdzv-id=course-one-cpu --max-restarts=0 examples/distributed/collectives.py --backend gloo
```

The fallback is separately recorded. It does not complete the unavailable hardware configuration.

**Troubleshooting:** A busy rendezvous port prevents startup; choose a free local port consistently. CPU/Gloo verifies semantics but not CUDA dispatch.

**Cleanup:** torchrun tears down workers on normal exit. On failure interrupt both launches and confirm owned workers exit. No allocation or scheduler job is created by these commands.

??? success "Answer"

    Every rank asserts the arithmetic-series result p(p+1)/2. With one rank, this is 1. NCCL dispatch is real, but no peer GPU or network communication is tested.

## Multi Gpu {#multi-gpu}

**core · 20 minutes · Two CUDA GPUs on one node; CPU/Gloo two-process fallback**

On an allocated two-GPU node, assign one worker per visible GPU and verify both ranks receive 3. Otherwise run the two-process CPU fallback and label it explicitly.

```bash
env OMP_NUM_THREADS=1 NCCL_IB_DISABLE=1 NCCL_SOCKET_IFNAME==lo torchrun --nnodes=1 --nproc-per-node=2 --rdzv-backend=c10d --rdzv-endpoint=127.0.0.1:29622 --rdzv-id=course-two-gpu --max-restarts=0 examples/distributed/collectives.py --backend nccl
```

**Source:** [examples/distributed/collectives.py](/hpc_study.io/downloads/source/examples/distributed/collectives.py).

**Expected behavior and correctness:** Ranks contribute 1 and 2 and both receive 3. The NCCL path assigns LOCAL_RANK to a distinct CUDA device. The CPU fallback checks multi-process reduction but provides no evidence about GPU peer access, NVLink or NCCL bandwidth.

### Local Fallback

```bash
env OMP_NUM_THREADS=1 GLOO_SOCKET_IFNAME=lo torchrun --nnodes=1 --nproc-per-node=2 --rdzv-backend=c10d --rdzv-endpoint=127.0.0.1:29622 --rdzv-id=course-two-cpu --max-restarts=0 examples/distributed/collectives.py --backend gloo
```

The fallback is separately recorded. It does not complete the unavailable hardware configuration.

**Troubleshooting:** The program rejects more local NCCL workers than visible GPUs. Do not run two workers on the same GPU to imitate a two-GPU experiment. The current validation machine has one visible GPU.

**Cleanup:** torchrun tears down workers on normal exit. On failure interrupt both launches and confirm owned workers exit. No allocation or scheduler job is created by these commands.

??? success "Answer"

    Ranks contribute 1 and 2 and both receive 3. The NCCL path assigns LOCAL_RANK to a distinct CUDA device. The CPU fallback checks multi-process reduction but provides no evidence about GPU peer access, NVLink or NCCL bandwidth.

## Two Node Training {#two-node-training}

**stretch · 30 minutes · Two allocated Linux nodes; one CUDA GPU per node; TCP interface and permitted ports**

Complete the remote preflight, replace placeholders and run one command on each node. Verify the AllReduce and five DDP updates against a global-batch reference. Without two allocated nodes, execute only the local CPU fallback.

```bash
env OMP_NUM_THREADS=1 NCCL_IB_DISABLE=1 NCCL_SOCKET_IFNAME==YOUR_INTERFACE GLOO_SOCKET_IFNAME=YOUR_INTERFACE torchrun --nnodes=2 --node-rank=0 --nproc-per-node=1 --rdzv-backend=c10d --rdzv-endpoint=NODE0_IP:29500 --rdzv-id=course-UNIQUE-ID --rdzv-conf=join_timeout=60,read_timeout=60 --max-restarts=0 examples/distributed/collectives.py --backend nccl --train
env OMP_NUM_THREADS=1 NCCL_IB_DISABLE=1 NCCL_SOCKET_IFNAME==YOUR_INTERFACE GLOO_SOCKET_IFNAME=YOUR_INTERFACE torchrun --nnodes=2 --node-rank=1 --nproc-per-node=1 --rdzv-backend=c10d --rdzv-endpoint=NODE0_IP:29500 --rdzv-id=course-UNIQUE-ID --rdzv-conf=join_timeout=60,read_timeout=60 --max-restarts=0 examples/distributed/collectives.py --backend nccl --train
```

**Source:** [examples/distributed/collectives.py](/hpc_study.io/downloads/source/examples/distributed/collectives.py), [course/hardware-profile.json](/hpc_study.io/downloads/source/course/hardware-profile.json).

**Expected behavior and correctness:** Each rank uses a different eight-sample shard from a reproducible global batch. DDP's mean gradients match an independent CPU SGD update over the concatenated global batch within declared tolerances. The two-process local fallback cannot demonstrate remote rendezvous, Ethernet transport or network scaling.

### Local Fallback

```bash
env OMP_NUM_THREADS=1 GLOO_SOCKET_IFNAME=lo torchrun --nnodes=1 --nproc-per-node=2 --rdzv-backend=c10d --rdzv-endpoint=127.0.0.1:29623 --rdzv-id=course-ddp-cpu --max-restarts=0 examples/distributed/collectives.py --backend gloo --train
```

The fallback is separately recorded. It does not complete the unavailable hardware configuration.

**Troubleshooting:** Both nodes must share job ID, endpoint, software and code but use the intended host-specific interface. A rendezvous port alone is insufficient: NCCL/Gloo may need additional TCP data ports. Preserve both rank logs and stop both commands on failure.

**Cleanup:** torchrun tears down workers on normal exit. On failure interrupt both launches and confirm owned workers exit. No allocation or scheduler job is created by these commands.

??? success "Answer"

    Each rank uses a different eight-sample shard from a reproducible global batch. DDP's mean gradients match an independent CPU SGD update over the concatenated global batch within declared tolerances. The two-process local fallback cannot demonstrate remote rendezvous, Ethernet transport or network scaling.

## Next Steps

Continue to [datacenter GPU study](../datacenter/intro.md). Keep two-GPU and two-node configurations marked unexecuted when only one GPU is available.
