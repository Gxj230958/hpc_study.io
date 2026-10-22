# Datacenter GPU Study

**Prerequisites:** CUDA architecture, timing boundaries, precision and distributed collectives.

**Objective:** Produce a sourced hardware comparison and a defensible porting plan.

These exercises are read-only analysis. The course does not have A100, H100 or H200 execution evidence. Manufacturer specifications, calculated bounds and actual measurements are different kinds of evidence. Start with [architecture variants](architectures.md), then consult [roofline](roofline.md), [precision and porting](porting.md), [fabrics and MIG](topology.md), and [operations](operations.md). The optional calculator checks units and capacity arithmetic on the CPU; it never allocates a datacenter-sized tensor.

## Specifications {#specifications}

**warm-up · 10 minutes · Read-only browser analysis; no datacenter GPU**

Compare the sourced A100 80 GB PCIe/SXM, H100 SXM/NVL and H200 SXM/NVL rows. Record form factor, memory, bandwidth, precision mode and source date. Identify at least two values that cannot be compared without qualification.

**Minimal excerpt:**

```text
comparison_key = (SKU, package, memory_variant, precision, dense_or_sparse)
```

**Source:** [course/specifications.json](/hpc_study.io/downloads/source/course/specifications.json).

**Expected behavior and correctness:** Produce a comparison with exact SKUs, units, precision modes and dated source links. Identify ambiguous or incomparable entries.

**Troubleshooting:** If a source is inaccessible, record that fact and retain the dated supplied row. Do not invent a current specification or silently substitute another SKU.

**Cleanup:** No hardware or cloud resource is created. Retain the worksheet with source dates; remove only your own temporary notes.

??? success "Answer"

    A GPU family name is not a complete specification. A100 80 GB PCIe and SXM have different bandwidth; H100 NVL has 94 GB per GPU and 188 GB per pair, not 188 GB on each device. Sparse tensor peaks and dense scalar peaks describe different operations.

## Roofline Capacity {#roofline-capacity}

**core · 20 minutes · Read-only analysis and optional CPU calculator; no A100/H100/H200**

Calculate an FP32 vector-add roofline and a three-array capacity limit for H100 SXM using the sourced inputs. Repeat the calculation on paper in base units before checking the calculator.

```bash
python examples/datacenter/bounds.py --bandwidth-gbps 3350 --peak-tflops 67 --capacity-gb 80
```

**Minimal excerpt:**

```python
intensity = 1 / 12
bound_tflops = min(67, 3350 * intensity / 1000)
max_elements = int(80 * 1e9 * 0.8 / 12)
```

**Source:** [examples/datacenter/bounds.py](/hpc_study.io/downloads/source/examples/datacenter/bounds.py), [course/specifications.json](/hpc_study.io/downloads/source/course/specifications.json).

**Expected behavior and correctness:** The calculator reports CALCULATED bounds and checks units/capacity arithmetic. Compare with your separate base-unit calculation; allocate no large arrays.

**Troubleshooting:** Keep GB versus GiB and dense versus sparse peaks explicit. Capacity bounds omit workspace and runtime allocations beyond the teaching reserve; never allocate the bound on the local GPU.

**Cleanup:** No hardware or cloud resource is created. Retain the worksheet with source dates; remove only your own temporary notes.

??? success "Answer"

    One addition uses one FLOP and at least 12 bytes, so intensity is 1/12 FLOP/byte. At 3350 GB/s the bandwidth bound is about 0.279167 TFLOP/s, below the 67 TFLOP/s scalar FP32 peak. Reserving 20% of 80 decimal GB leaves at most 5,333,333,333 three-array elements. These are calculated limits, not measured performance or safe recommended allocations.

## Porting Plan {#porting-plan}

**stretch · 30 minutes · Read-only planning; no cloud account or datacenter GPU needed**

Write a one-page plan selecting a concrete SKU, precision, memory budget, topology, scheduler request, profiling method, correctness oracle and stop condition. Calculate cost from an explicitly hypothetical rate and include setup, retries, storage and transfer assumptions.

**Minimal excerpt:**

```text
estimated_cost = quoted_instance_rate * billed_hours + storage + transfer
```

**Source:** [course/hardware-profile.json](/hpc_study.io/downloads/source/course/hardware-profile.json), [course/specifications.json](/hpc_study.io/downloads/source/course/specifications.json).

**Expected behavior and correctness:** Produce a concrete plan with a correctness gate, resource request, dated cost assumptions, cleanup and explicit unresolved fields.

**Troubleshooting:** A vendor peak cannot predict billed time. MIG profiles cannot be treated as freely composable fractions or automatically aggregated memory. Cloud provisioning is outside this exercise and no cloud command should be executed.

**Cleanup:** No hardware or cloud resource is created. Retain the worksheet with source dates; remove only your own temporary notes.

??? success "Answer"

    A complete plan separates prerequisites from observations, calculates job cost as instance-rate times billed hours plus storage/transfer, and uses a small correctness gate before scaling. It identifies whether a full GPU or a particular MIG profile is required. Unknown ports, scheduler, interconnect and remote versions remain unresolved until verified.

## Next Steps

Review [your validation evidence](../learning/validation.md) and list unresolved hardware assumptions before requesting an allocation.
