# Power Measurement

**Prerequisites:** [Power and energy](intro.md). **Objective:** Interpret sampled telemetry.

A power sensor reports a measurement over a particular domain and sampling interval. Very short kernels can finish between samples. Idle baseline, sensor lag and concurrent workloads can distort an energy estimate.

For a longer steady workload, integrate sampled watts over seconds and state which devices are included. Report uncertainty and sampling frequency. GPU-only telemetry is not a wall-outlet measurement.

The course does not publish a new energy benchmark. Next, include energy assumptions in the [datacenter cost plan](../../datacenter/operations.md).
