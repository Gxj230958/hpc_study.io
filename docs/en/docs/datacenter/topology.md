# NVLink, NVSwitch and MIG

**Prerequisites:** Collectives and [architecture variants](architectures.md). **Objective:** Include topology and isolation in a resource request.

NVLink provides supported high-bandwidth links; NVSwitch provides switching in supported multi-GPU platforms. A GPU's product capability is not proof that a given server wires every GPU together. Inspect topology, peer access and the actual NCCL transport. Ethernet remains the course's remote baseline.

Multi-Instance GPU (MIG) partitions supported GPUs into instances with dedicated compute and memory resources. A profile is a particular supported configuration, not an arbitrary percentage. Profiles, placements, driver requirements and visibility behavior must be checked against the actual SKU and software stack.

NVIDIA's [supported GPU list](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-gpus.html) includes A100, H100 and H200 variants. The RTX 4090 is not a MIG-capable substitute. Consult the [MIG user guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/) for profiles, device naming and deployment restrictions.

A MIG instance can be appropriate for a bounded independent job, while a large model may need full-device memory and a specific fabric. Never sum unrelated instance capacities and assume one process can allocate their total. This course performs no MIG reconfiguration. Next, write [the operations plan](operations.md).
