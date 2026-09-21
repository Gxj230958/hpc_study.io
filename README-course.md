# HPC 入门课程与实验

课程面向有基本编程经验、尚未接触 HPC 的读者，覆盖硬件、并行编程、GPU、Benchmark、科学计算与机器学习系统。

## 起步

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-study.txt
make -C examples cpu
./build/sum 100003
mpiexec -n 3 python examples/mpi/sum.py --n 10
```

GPU 路径需要 NVIDIA 驱动和 CUDA 12.4 兼容环境：

```bash
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
python scripts/install-cuda.py --nsys
export PATH="$PWD/.tools/cuda/bin:$PWD/.tools/nsys/nsight-systems/2023.4.4/target-linux-x64:$PATH"
python examples/ml/witness.py
python scripts/validate.py --gpu
```

CPU 全套验证也需要 PyTorch，安装命令为 `python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu`，随后运行 `python scripts/validate.py`。从 CPU 版切换到 GPU 版前，先用 `python -m pip uninstall -y torch` 移除 CPU 包。原始输出在 `build/validation/`。HPL/HPCG 短跑需要系统 MPICH、OpenBLAS 开发包，执行 `bash scripts/run-reference-benchmarks.sh`，输出在 `build/reference/`。

独立站使用 `mkdocs.study.yml`；上游配置为 `docs/zh/mkdocs.yml`。五章文档与学习路线位于 `docs/zh/docs/`。

实验限于教学正确性与测量方法，不是正式基准提交。多卡 NCCL、多节点网络和 AMD GPU 不属于单张 NVIDIA GPU 的验证范围。来源及原作者署名保留在各篇文章中，文档、代码与图像遵循仓库的 CC BY-NC-SA 4.0 许可。
