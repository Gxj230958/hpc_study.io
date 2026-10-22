# HPC 入门课程与实验

课程面向有基本编程经验、尚未接触 HPC 的读者，覆盖硬件、并行编程、GPU、Benchmark、科学计算与机器学习系统。

## 起步

```bash
uv sync --locked
source scripts/activate-study.sh
make -C examples cpu
./build/sum 100003
mpiexec -n 3 python examples/mpi/sum.py --n 10
```

GPU 路径需要 NVIDIA 驱动和 CUDA 12.4 兼容环境：

```bash
uv run python scripts/install-cuda.py --nsys
source scripts/activate-study.sh
python examples/ml/witness.py
python scripts/validate.py --gpu
```

`uv sync --locked` installs the Python 3.10 environment, scientific Python, bundled MPICH/mpi4py, CUDA 12.4 PyTorch, and documentation tools from `uv.lock`. The GPU build also runs CPU experiments. Run `python scripts/validate.py` for CPU checks or `python scripts/validate.py --gpu` for both. Activation sets CPU library threads to 10 for this machine; the validation suite uses smaller fixed thread counts for reproducibility. For MPI experiments, use `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` and at most 10 ranks to avoid oversubscription.

Native experiments require GCC/G++, Make, and the CUDA compiler/sanitizer; uv manages Python packages, while `scripts/install-cuda.py` supplies the local CUDA tools. The existing NVIDIA driver supports the pinned CUDA runtime. Activation also disables forced TF32 so the FP32 correctness checks use full precision. Raw validation output is in `build/validation/`. HPL/HPCG additionally require system MPICH and OpenBLAS development packages (`apt-get install mpich libmpich-dev libopenblas-dev`); run `bash scripts/run-reference-benchmarks.sh`, with output in `build/reference/`.

独立站使用 `mkdocs.study.yml`；上游配置为 `docs/zh/mkdocs.yml`。五章文档与学习路线位于 `docs/zh/docs/`。

实验限于教学正确性与测量方法，不是正式基准提交。多卡 NCCL、多节点网络和 AMD GPU 不属于单张 NVIDIA GPU 的验证范围。来源及原作者署名保留在各篇文章中，文档、代码与图像遵循仓库的 CC BY-NC-SA 4.0 许可。
