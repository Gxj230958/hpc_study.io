# 环境准备：先让小程序运行

本课程以 Linux x86-64 为实践环境。Windows 可使用 WSL2；GPU 路径还需要兼容的 Windows NVIDIA 驱动和 WSL GPU 支持。不要在共享集群登录节点运行性能实验。

## 取得源码

```bash
git clone https://github.com/hpcgame/hpc-wiki.git
cd hpc-wiki
```

若使用课程 fork，使用页面右上角仓库地址克隆，并切换到该仓库目录。上游尚未合并课程时，应使用课程 fork。后续命令都从仓库根目录执行。

## CPU 与 Python

需要 Python 3.10、GCC、make。Ubuntu 可安装 `python3-venv build-essential`。使用虚拟环境隔离 Python 依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-study.txt
export OMP_NUM_THREADS=4
export OPENBLAS_NUM_THREADS=4
make -C examples cpu
./build/sum 100003
mpiexec -n 3 python examples/mpi/sum.py --n 10
python examples/science/solve.py
```

`mpi4py-mpich` 在本课程的 Linux 环境提供 Python MPI 与配套启动器。激活环境后，`which mpiexec` 应指向 `.venv/bin`。已有集群 MPI 时，应使用站点推荐的 mpi4py 安装方法，避免混用运行时。

C MPI 和 HPL 参考编译需要额外系统开发包 `libmpich-dev libopenblas-dev`。这条路径使用 `/usr/bin/mpicc` 和 `/usr/bin/mpiexec`，与 Python 打包运行时分开。

仅用 CPU 学习训练与精度实验时，另安装 CPU 版 PyTorch：

```bash
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
python scripts/validate.py
```

计划使用 GPU 的读者直接按下一节安装 GPU 版即可。若已有 CPU 版，切换前先执行 `python -m pip uninstall -y torch`，防止 pip 把同版本的 CPU 包视为已经满足要求。

## NVIDIA GPU

先检查 `nvidia-smi`。GPU 学习基线为 CUDA 12.4.1 与 PyTorch 2.6.0；这些是可复现版本，不代表最新版本。

```bash
python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
```

在 Linux x86-64 上，官方索引不可达时，可从 PyPI 安装 `torch==2.6.0`；安装后必须检查 `torch.version.cuda`，本课程期望 `12.4`。不要随意把 CUDA 13 软件包与旧驱动混装。

已经有兼容 nvcc 时直接使用。否则可在项目内安装校验过的官方组件，不安装或更换驱动：

```bash
python scripts/install-cuda.py --nsys
export PATH="$PWD/.tools/cuda/bin:$PWD/.tools/nsys/nsight-systems/2023.4.4/target-linux-x64:$PATH"
nvcc --version
python examples/ml/witness.py
make -C examples cuda
./build/cuda_labs
```

`WITNESS PASS` 表示实际执行过一个 GPU 矩阵乘法并检查结果，不只是导入成功。`CUDA_ARCH` 默认检测本机；交叉编译可显式指定，例如 `make -C examples cuda CUDA_ARCH=sm_89`。

## 网站预览

```bash
mkdocs serve -f docs/zh/mkdocs.yml -a 127.0.0.1:8008
```

打开终端显示的网址。新站专用配置存在时可改为 `-f mkdocs.study.yml`。完整检查入口为 `python scripts/validate.py`，GPU 环境添加 `--gpu`。原始日志写入 `build/validation/`。

## 常见问题

`nvcc: command not found` 表示编译工具路径缺失，不等于 GPU 不存在。`No module named ...` 时先确认虚拟环境。MPI 卡住时检查进程数与调用顺序。GPU 权限或显存不足时先运行小例子，记录错误，不修改共享机器的全局设置。

依赖基线记录在 `env-spec.json` 和 `requirements-study.txt`。CUDA 下载文件按 NVIDIA 清单校验 SHA256。参考：[CUDA 安装指南](https://docs.nvidia.com/cuda/archive/12.4.1/cuda-installation-guide-linux/index.html)。
