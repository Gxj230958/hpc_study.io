# NCCL

**Prerequisites:** CUDA and MPI collective concepts. **Objective:** Distinguish collective semantics from transport behavior.

NCCL implements GPU collectives such as AllReduce, combining contributions from every participating rank and returning the result to each. A sum of rank+1 must equal p(p+1)/2 on every rank. That independent formula is the course collective's correctness oracle.

One process on one GPU can initialize NCCL and execute a collective, but it cannot demonstrate a link between GPUs. Two local GPUs add PCIe or other available paths. Two hosts add a network boundary. Neither NVLink nor peer-to-peer access is assumed.

For the TCP baseline set NCCL_IB_DISABLE=1 and choose NCCL_SOCKET_IFNAME explicitly on each host. GLOO_SOCKET_IFNAME selects the CPU fallback's interface. The rendezvous endpoint handles membership; data traffic may use additional dynamically selected ports. See NVIDIA's [NCCL environment reference](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html).

Next, run [distributed experiments](../clusters/distributed.md) with one worker per visible GPU and a finite process-group timeout.
