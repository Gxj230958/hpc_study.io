# Architecture Variants

**Prerequisites:** [GPU architecture](../gpu/arch.md). **Objective:** Compare exact products rather than family names.

The RTX 4090 uses Ada and conventional GDDR6X memory; the course targets the standard 24 GB model. A100 is Ampere with HBM2e variants. H100 and H200 use Hopper; H200 increases capacity and bandwidth with HBM3e. Architecture, package and memory variant must all be recorded.

| Concrete variant | Memory GB | Bandwidth GB/s | Dense scalar FP32 TFLOP/s |
| --- | ---: | ---: | ---: |
| A100 80 GB PCIe | 80 | 1935 | 19.5 |
| A100 80 GB SXM | 80 | 2039 | 19.5 |
| H100 SXM | 80 | 3350 | 67 |
| H100 NVL, per GPU | 94 | 3900 | 60 |
| H200 SXM | 141 | 4800 | 67 |
| H200 NVL | 141 | 4800 | 60 |

These are dated manufacturer specifications checked on 2026-10-22, not local measurements. Sources: [A100](https://www.nvidia.com/en-us/data-center/a100/), [H100](https://www.nvidia.com/en-us/data-center/h100/), [H200](https://www.nvidia.com/en-us/data-center/h200/). The [machine-readable table](/hpc_study.io/downloads/source/course/specifications.json) retains units and source links.

SXM modules and PCIe cards belong to different server configurations. H100 NVL's two-GPU 188 GB total is not a single GPU's capacity. Older H100 PCIe and A100 40 GB products require their own briefs; do not borrow these rows. Memory bandwidth is not NVLink bandwidth, and the number of GPUs in a server is not proof of an all-to-all fabric.

Read the [Ada tuning guide](https://docs.nvidia.com/cuda/ada-tuning-guide/), [Ampere tuning guide](https://docs.nvidia.com/cuda/ampere-tuning-guide/) and pinned [CUDA 12.4 Hopper guide](https://docs.nvidia.com/cuda/archive/12.4.1/hopper-tuning-guide/index.html) for architectural limits. Next, calculate [memory bounds](roofline.md).
