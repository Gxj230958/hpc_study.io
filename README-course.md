# HPC Course Environment and Experiments

Run commands from the repository root or the root of the extracted source bundle. uv is authoritative; requirements files remain historical compatibility inputs.

## GPU Environment

```bash
uv sync --locked --extra gpu
source scripts/activate-study.sh
make -C examples cpu cuda
python examples/ml/witness.py
python scripts/validate.py --gpu
```

Python 3.10 and PyTorch 2.6.0+cu124 are pinned. A compatible NVIDIA driver is required. PyTorch's runtime does not include nvcc, Compute Sanitizer or Nsight Systems; python scripts/install-cuda.py --nsys installs the pinned local tools when needed. Source activation again after installation.

## CPU Environment

```bash
uv sync --locked --extra cpu
source scripts/activate-study.sh
python scripts/validate.py
```

CPU and GPU extras conflict by design. Use plain python after activation; an unqualified uv run may resync away an optional extra. To use uv run, repeat --extra cpu or --extra gpu explicitly.

If a container preloads an unrelated torch/lib through LD_LIBRARY_PATH, the CPU
wheel can fail with an undefined Python symbol. Confirm that conflict and test
the affected CPU command with env -u LD_LIBRARY_PATH; do not erase site-required
driver/MPI paths globally. See the setup troubleshooting page.

MPI labs use the bundled MPICH launcher from .venv/bin. Use OMP_NUM_THREADS=1 and OPENBLAS_NUM_THREADS=1 per rank and keep ranks within the allocated CPU quota. The activation helper's ten-thread defaults preserve the original machine setup; override them on smaller allocations.

Native HPL/HPCG builds additionally require system MPICH and OpenBLAS development packages (mpich, libmpich-dev, libopenblas-dev). Their script uses matching system compilers and /usr/bin/mpiexec in isolation; never mix that launcher with bundled mpi4py. Run bash scripts/run-reference-benchmarks.sh for small teaching workloads, not official scores.

## Documentation and Browser Checks

These build/browser commands require the full Git checkout. The downloadable
example bundle contains experiment sources and runners, not the documentation tree.

```bash
uv sync --locked --only-group docs --group browser
uv run --only-group docs --group browser playwright install chromium
uv run --only-group docs python scripts/build-site.py
uv run --only-group docs python scripts/serve-site.py --port 8008
```

In another shell run the browser check with the same documentation environment:

```bash
uv run --only-group docs --group browser python scripts/browser-check.py
```

A docs-only sync intentionally excludes experiment dependencies. Use a separate UV_PROJECT_ENVIRONMENT or checkout when preserving a GPU environment. Publishing uses only the docs group; CI uses the cpu extra plus docs/browser dependencies.

## Experiment Inventory

course/labs.json defines eight assessed modules with three levels each. scripts/check-labs.py validates metadata and closed answers; scripts/run-labs.py executes local commands with timeouts and source hashes. Its --gpu switch includes the CUDA path; --reference includes native benchmark source builds.

One process on one GPU cannot test GPU-to-GPU communication. Two CPU/Gloo workers test distributed semantics but cannot measure NCCL performance. Two-node commands require the separately documented hardware profile and remain unexecuted without access. Datacenter specifications and roofline results are read-only analyses and calculated bounds, not measurements on A100/H100/H200.

Generated data lives under build and tool downloads under .tools. Preserve logs before cleanup. No cloud provisioning is included and no AWS command is executed by the validation runner.

Course material and examples retain CC BY-NC-SA 4.0 terms and original author credit. Bundled renderers keep separate licenses.
