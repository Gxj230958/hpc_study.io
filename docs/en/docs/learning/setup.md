# Setup

**Prerequisites:** A shell, Git and basic Python/C. **Objective:** Create a reproducible environment and identify which experiments your allocation supports.

The primary path is Ubuntu Linux with GCC, Make and Python 3.10 managed by uv. Experiments deliberately stay below 1 GiB of application data and target a conventional 24 GB RTX 4090. Framework initialization consumes additional memory. Do not size allocations from this validation host's unusual GPU memory report.

## Select an Environment

Clone the repository or extract the downloadable bundle and run commands from its root. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first.

```bash
uv sync --locked --extra gpu
source scripts/activate-study.sh
make -C examples cpu
python examples/ml/witness.py
```

The GPU extra pins PyTorch 2.6.0 with CUDA 12.4 runtime support. A compatible NVIDIA driver is required. For a CPU-only machine, use the mutually exclusive CPU extra:

```bash
uv sync --locked --extra cpu
source scripts/activate-study.sh
python examples/ml/train.py --device cpu
```

Select exactly one extra. Running uv sync with another selection updates the environment. After activation use plain python and mpiexec; bare uv run can sync without your selected extra. Use uv run --extra gpu or --extra cpu when choosing that workflow.

Documentation publishing requires no scientific or GPU packages:

```bash
uv sync --locked --only-group docs
uv run --only-group docs python scripts/build-site.py
```

Use a separate checkout or UV_PROJECT_ENVIRONMENT for docs-only work if you want to preserve an active experiment environment.

## Native Tools

The CPU Makefile requires GCC/G++, Make and OpenMP. PyTorch's CUDA runtime does not supply nvcc, Compute Sanitizer or Nsight Systems. If those tools are absent, install the pinned local course toolchain:

```bash
python scripts/install-cuda.py --nsys
source scripts/activate-study.sh
nvcc --version
compute-sanitizer --version
nsys --version
make -C examples cuda
```

This installer downloads archives into .tools and does not replace the NVIDIA driver. Allow download space and inspect the installer before running it. The validation driver supports the pinned runtime; other systems must check compatibility.

## MPI and Threads

Activation puts .venv/bin and local CUDA tools first on PATH. Use bundled MPICH from mpi4py-mpich, not a preloaded system Open MPI launcher:

```bash
which python
which mpiexec
python -c "from mpi4py import MPI; print(MPI.Get_library_version())"
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 mpiexec -n 3 python examples/mpi/sum.py --n 10
```

Set one numerical-library thread per rank. The activation helper's ten-thread defaults describe the validation allocation; override them downward on smaller allocations. CPU quotas, CPU affinity and memory cgroups may differ from host totals.

Native HPL/HPCG builds are an isolated system-MPICH toolchain requiring mpich, libmpich-dev and libopenblas-dev development packages. They use matching /usr/bin compilers and launcher. They do not import bundled mpi4py.

## Troubleshooting and Cleanup

If imports fail, verify the active Python and selected extra. If CUDA is unavailable, inspect nvidia-smi before reinstalling PyTorch. If MPI hangs, check launcher/library consistency before changing network settings. A profiler permission failure means data was not collected; it is not a zero-duration result.

On a preconfigured container, LD_LIBRARY_PATH may include another Python installation's torch/lib. An undefined Python symbol while importing the CPU wheel can be caused by that unrelated shared library. Confirm the path, then test only the affected CPU command with the inherited path removed:

```bash
env -u LD_LIBRARY_PATH python examples/ml/train.py --device cpu
```

Do not remove site-required driver or MPI paths globally. The dated CPU-extra validation used this per-command isolation because this host preloads a Python 3.12 PyTorch library directory.

Generated executables and logs live in build; downloaded toolchains live in .tools. Retain evidence before removing those directories. uv sync --locked recreates an environment using the chosen extras. Next, run [the inventory experiment](../hardware/hardware-intro.md).
