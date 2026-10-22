# Profiling Tools

**Prerequisites:** [Measurement](intro.md). **Objective:** Choose a tool that can test a specific hypothesis.

A sampling profiler estimates where CPU execution time is spent by periodically observing instruction pointers. Instrumentation records selected events. Hardware counters count events such as cache misses, but availability and interpretation depend on hardware, kernel permissions and multiplexing.

Start with elapsed time and a correct result. Use perf or a CPU profiler to locate expensive regions, Nsight Systems to inspect host/device coordination, and Nsight Compute to investigate a particular GPU kernel. Profiling overhead can change execution, especially for short workloads.

Retained example of a system timeline from the original course:

![Example timeline from the original profiling chapter](images/intro/timeline.png)

This illustration is historical teaching material, not a newly collected trace. Record tool version, sampling period, permissions and workload when collecting your own evidence. Next, examine [Nsight Systems](../gpu/nsys.md).
