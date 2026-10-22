# Interconnects

**Prerequisites:** [Memory](memory.md) and ranks. **Objective:** Identify which link a transfer crosses.

CPU sockets, CPU-to-GPU PCIe, GPU-to-GPU fabrics and host-to-host Ethernet are different boundaries. A bandwidth figure for one cannot be substituted for another. Directionality and concurrent traffic also affect the interpretation of a quoted rate.

NVLink connects supported GPUs or platform components; NVSwitch provides a fabric in supported systems. Neither is assumed on the RTX 4090 teaching setup. InfiniBand is also optional; the course remote baseline uses TCP/Ethernet.

Inspect actual topology and allocated devices before measuring. Next, use [the distributed preflight](../clusters/distributed.md), where unresolved fields remain explicit.
