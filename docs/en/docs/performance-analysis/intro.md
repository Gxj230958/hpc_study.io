# Measurement and Benchmarks

**Prerequisites:** CPU and CUDA correctness labs; CUDA profiling is optional on CPU-only systems.

**Objective:** Define timing boundaries, profile transfer costs and interpret HPL/HPCG validity.

Latency is elapsed time for one operation; throughput is work completed per unit time. A benchmark specifies both a workload and a measurement procedure. Warm-up, synchronization, repetitions, data placement and accuracy determine what a result means. Preserve raw samples and input sizes so somebody else can reproduce your comparison.

## Before You Run

Run commands from the repository root after [setup](../learning/setup.md). Use `source scripts/activate-study.sh` once per shell. These are 10, 20 and 30 minute exercises including interpretation, not promised program runtimes. Use `timeout 180s COMMAND` for individual local runs; allow up to 600 seconds for the native benchmark build. Keep allocations bounded and avoid other workloads during timing.

## Collect Repeated Timings {#repeated-timings}

**warm-up · 10 minutes · CPU; 8 MiB; one worker**

Make a five-sample table, report the median and range, and state that allocation and initialization are outside the timed loop. Verify every sample's integer total before comparing time.

```bash
env OMP_NUM_THREADS=1 ./build/sum 1000003
env OMP_NUM_THREADS=1 ./build/sum 1000003
env OMP_NUM_THREADS=1 ./build/sum 1000003
env OMP_NUM_THREADS=1 ./build/sum 1000003
env OMP_NUM_THREADS=1 ./build/sum 1000003
```

**Source:** [examples/cpu/sum.c](/hpc_study.io/downloads/source/examples/cpu/sum.c). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** The sample median describes this workload under these conditions. It is not a peak FLOPS measurement. Report input size, compiler flags, threads, timer and placement alongside it; a fast wrong result is rejected.

**Troubleshooting:** Run make -C examples cpu if build/sum is missing. Tiny runs may approach timer resolution. Do not discard inconvenient samples without a recorded reason.

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    The sample median describes this workload under these conditions. It is not a peak FLOPS measurement. Report input size, compiler flags, threads, timer and placement alongside it; a fast wrong result is rejected.

## Profile Transfers and Kernels {#profile-transfers}

**core · 20 minutes · One CUDA GPU; Nsight Systems; under 100 MiB trace output**

Identify host-to-device copies, launches and device-to-host copies. Compare event-based resident-kernel time with the first transfer-and-kernel host interval. Verify PASS in the profiled program output.

```bash
nsys profile --force-overwrite true --trace=cuda --output=build/course-profile ./build/cuda_labs
nsys stats --report cuda_gpu_kern_sum,cuda_gpu_mem_time_sum build/course-profile.nsys-rep
```

**Source:** [examples/cuda/labs.cu](/hpc_study.io/downloads/source/examples/cuda/labs.cu). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** The end-to-end interval includes copies and first launch effects; resident CUDA events measure a different boundary after warm-up. Profiling adds overhead, so retain unprofiled measurements too. A timeline reveals idle gaps; it does not by itself prove their cause.

**Troubleshooting:** On systems without profiler access, retain program timing output and mark the trace uncollected. Do not report missing hardware-counter data as zero.

**Cleanup:** Remove build/course-profile.nsys-rep and build/course-profile.sqlite after retaining your report.

??? success "Answer"

    The end-to-end interval includes copies and first launch effects; resident CUDA events measure a different boundary after warm-up. Profiling adds overhead, so retain unprofiled measurements too. A timeline reveals idle gaps; it does not by itself prove their cause.

## Run HPL and HPCG Teaching Workloads {#reference-benchmarks}

**stretch · 30 minutes · CPU; native MPICH and OpenBLAS development tools; below 1 GiB; network for source download**

Inspect the small supplied inputs before running. Check HPL's residual and HPCG's verification report, record source revisions and explain why these short runs are not official submissions.

```bash
bash scripts/run-reference-benchmarks.sh
```

**Source:** [scripts/run-reference-benchmarks.sh](/hpc_study.io/downloads/source/scripts/run-reference-benchmarks.sh), [examples/benchmark/HPL.dat](/hpc_study.io/downloads/source/examples/benchmark/HPL.dat), [examples/benchmark/hpcg.dat](/hpc_study.io/downloads/source/examples/benchmark/hpcg.dat). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** HPL factors a dense system and checks a scaled residual. HPCG exercises sparse operations and checks convergence/symmetry; its short runtime and small local problem fail official submission requirements even when the teaching correctness checks pass. Never promote these runs into leaderboard scores.

**Troubleshooting:** These native benchmarks use the system MPICH compiler and matching /usr/bin/mpiexec as an isolated toolchain. mpi4py labs use bundled MPICH. Do not combine a system launcher with bundled mpi4py or an Open MPI library with these native binaries.

**Cleanup:** Remove build/reference and .tools/hpl-2.3 / .tools/hpcg only when you no longer need source and raw results.

??? success "Answer"

    HPL factors a dense system and checks a scaled residual. HPCG exercises sparse operations and checks convergence/symmetry; its short runtime and small local problem fail official submission requirements even when the teaching correctness checks pass. Never promote these runs into leaderboard scores.

## A Performance Bound

Arithmetic intensity is useful FLOPs per byte crossing a specified memory boundary. The roofline bound is

$$P \leq \min(P_{\mathrm{peak}}, B I).$$

Use consistent units and precision. This is a calculated upper bound, not a measured result.

## Next Steps

Continue to [the next module](../sci-mlsys/intro.md). Review [experiment status](../learning/validation.md) before reusing a performance claim.

