# 实验索引

先完成[环境准备](setup.md)。源码位于仓库 `examples/`，文档短片段不一定是完整程序。每次先检查 `PASS`，再讨论速度。

| 实验 | 入口 | 资源 | 检查方法 |
| --- | --- | --- | --- |
| 并行整数求和 | `./build/sum 100003` | CPU、GCC | 与解析结果比较 |
| 内存访问步长 | `./build/memory` | CPU、约 128 MiB 内存 | 核对访问次数与和 |
| MPI 不均匀分块 | `mpiexec -n 3 python examples/mpi/sum.py --n 10` | 单机 3 进程 | 总和为 45 |
| MPI 往返通信 | `mpiexec -n 2 python examples/mpi/pingpong.py` | 单机 2 进程 | 校验接收内容 |
| 稀疏方程求解 | `python examples/science/solve.py` | CPU | 残差与稠密解对照 |
| INT8 表示 | `python examples/ml/quantize.py` | CPU | 误差不超过半量化步长附近 |
| CUDA 设备见证 | `python examples/ml/witness.py` | NVIDIA GPU | CPU／GPU 矩阵乘法对照 |
| CUDA 三个 kernel | `./build/cuda_labs` | NVIDIA GPU、nvcc | 多种边界尺寸与 CPU 对照 |
| FP32／FP16 | `python examples/ml/precision.py` | CPU；GPU 可选 | 相对 L2 误差 |
| 小型训练 | `python examples/ml/train.py --device cuda` | 单卡；可改 cpu | 前向一致性与损失下降 |
| HPL／HPCG 参考短跑 | `bash scripts/run-reference-benchmarks.sh` | CPU、系统 MPI、BLAS | 官方验证输出 |

## 推荐的五份实验报告

1. **硬件，约 2 小时**：画资源图，改变内存访问步长，解释有效流量与实际内存流量的区别。
2. **并行，约 3 小时**：比较 1、2、4、8 个线程或进程，固定总规模与每进程规模各做一次。
3. **GPU，约 3 小时**：画线程下标和矩阵边界块，运行 sanitizer，比较内核与传输计时范围。
4. **Benchmark，约 2 小时**：为同一个程序建立重复测量记录，报告中位数、波动与配置。
5. **应用，约 3 小时**：比较稠密／稀疏解，观察混合精度与量化误差，说明训练例子的结论边界。

报告至少包括：目的、环境、命令、输入、原始输出、正确性、测量范围和解释。没有观察到加速也是有效结果。

## 验证边界

多卡 NCCL、多节点网络、AMD HIP、OpenCL 设备执行与 NVIDIA OpenACC 编译器不属于默认单卡验证。相应章节提供入门解释和环境要求。具体已执行项目见[验证记录](validation.md)。
