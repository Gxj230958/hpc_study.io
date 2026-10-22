# CUDA Programming

**Prerequisites:** C/C++ arrays and CPU parallelism; NVIDIA driver, CUDA compiler and GPU PyTorch environment.

**Objective:** Prove GPU execution, handle tail elements safely and validate shared-memory tiling.

CUDA launches a kernel, a function executed by many GPU threads. A block groups threads that can cooperate through shared memory and a block barrier. A grid contains all blocks in a launch. The host is the CPU and its memory; the device is the GPU and its memory. Explicit copies and asynchronous launches make both correctness checks and timing boundaries important.

## Before You Run

Run commands from the repository root after [setup](../learning/setup.md). Use `source scripts/activate-study.sh` once per shell. These are 10, 20 and 30 minute exercises including interpretation, not promised program runtimes. Use `timeout 180s COMMAND` for individual local runs; allow up to 600 seconds for the native benchmark build. Keep allocations bounded and avoid other workloads during timing.

## Verify GPU Dispatch {#gpu-dispatch}

**warm-up · 10 minutes · One NVIDIA GPU; below 1 GiB device memory**

Read the witness script, run it and record the device name, PyTorch CUDA version and visible device count. Identify the CPU reference used to verify the result.

```bash
python examples/ml/witness.py
```

**Source:** [examples/ml/witness.py](/hpc_study.io/downloads/source/examples/ml/witness.py). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** CUDA availability alone is insufficient. The witness checks that tensors and matrix multiplication results live on CUDA, compares against a CPU result and synchronizes before reporting PASS. It does not benchmark a datacenter GPU.

**Troubleshooting:** If CUDA is unavailable, use the CPU path for other modules. Check driver visibility and install the gpu extra; the CPU extra deliberately cannot dispatch CUDA.

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    CUDA availability alone is insufficient. The witness checks that tensors and matrix multiplication results live on CUDA, compares against a CPU result and synchronizes before reporting PASS. It does not benchmark a datacenter GPU.

## Implement Boundary-Safe Vector Addition {#vector-boundaries}

**core · 20 minutes · One CUDA GPU; CUDA toolkit; below 256 MiB**

Before viewing add(), write a kernel that computes i=blockIdx.x*blockDim.x+threadIdx.x and guards i<n. Compare it with the checked implementation. Explain the cases 1, 255, 256, 257 and 100003.

```bash
make -C examples cuda
./build/cuda_labs
```

**Source:** [examples/cuda/labs.cu](/hpc_study.io/downloads/source/examples/cuda/labs.cu). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** The ceiling division (n+255)/256 launches enough blocks; the guard prevents tail threads from reading or writing out of bounds. Every element is compared with an independent host sum. The same executable also checks reduction and matrix multiplication.

**Troubleshooting:** Missing nvcc is a toolkit issue even if PyTorch CUDA works. Source activation after installing local tools. For another GPU, use CUDA_ARCH appropriate to that GPU instead of copying sm_89 blindly.

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    The ceiling division (n+255)/256 launches enough blocks; the guard prevents tail threads from reading or writing out of bounds. Every element is compared with an independent host sum. The same executable also checks reduction and matrix multiplication.

## Validate Tiled Matrix Multiplication {#tiled-matmul}

**stretch · 30 minutes · One CUDA GPU; Compute Sanitizer; below 256 MiB**

Trace the two 16x16 shared-memory tiles and both barriers. Verify dimensions 1, 15, 16, 17 and 65, then run all three sanitizers. Explain why out-of-range tile entries must be zeroed.

```bash
compute-sanitizer --error-exitcode 1 --tool memcheck ./build/cuda_labs
compute-sanitizer --error-exitcode 1 --tool synccheck ./build/cuda_labs
compute-sanitizer --error-exitcode 1 --tool racecheck ./build/cuda_labs
```

**Source:** [examples/cuda/labs.cu](/hpc_study.io/downloads/source/examples/cuda/labs.cu). Read the bounded inputs and independent checks in the source before editing a working copy.

**Expected behavior and correctness:** All threads must reach both barriers, including threads whose output is outside the matrix. The first barrier completes tile loading; the second prevents overwriting a tile while others still use it. A double-precision host loop independently checks each result, and sanitizer success adds memory/synchronization evidence.

**Troubleshooting:** Use the sanitizer error exit flag so an error fails automation. A clean sanitizer run covers these inputs, not every possible shape. Check profiler/sanitizer permissions if instrumentation cannot attach.

**Cleanup:** Programs release memory on exit. Keep your measurements; make clean is unnecessary. Generated executables are confined to build/.

??? success "Answer"

    All threads must reach both barriers, including threads whose output is outside the matrix. The first barrier completes tile loading; the second prevents overwriting a tile while others still use it. A double-precision host loop independently checks each result, and sanitizer success adds memory/synchronization evidence.

## Next Steps

Continue to [the next module](../performance-analysis/intro.md). Review [experiment status](../learning/validation.md) before reusing a performance claim.

