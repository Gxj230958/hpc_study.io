# Troubleshooting FAQ

**Prerequisites:** [Setup](../../learning/setup.md). **Objective:** Diagnose failures from evidence.

## Why Is More Parallelism Slower?

Check fixed work size, thread counts, startup costs, memory bandwidth and oversubscription. Verify results before interpreting speedup.

## Why Can PyTorch Use CUDA While nvcc Is Missing?

PyTorch includes runtime dependencies, while compiling native CUDA requires a toolkit. Use the pinned installer described in setup when needed.

## Why Does MPI Hang?

Check launcher/library consistency, participating ranks, matching collectives and network reachability. Use timeouts and preserve every rank's output.

## Why Is a Reference Bound Higher Than My Result?

A roofline is a calculated limit using explicit assumptions. Transfers, dependency chains, unsupported precision and imperfect utilization can all lower performance.

Next, consult [validation](../../learning/validation.md) for known limits.
