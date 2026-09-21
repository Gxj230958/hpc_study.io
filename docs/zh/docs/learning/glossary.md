# 常用术语

| 术语 | 平实解释 | 继续阅读 |
| --- | --- | --- |
| 核心 / Core | 可以执行程序的一组 CPU 计算资源 | [CPU](../hardware/processor.md) |
| 延迟 / Latency | 等待一次操作完成的时间 | [互连](../hardware/interconnect.md) |
| 吞吐量 / Throughput | 单位时间完成的工作量 | [Benchmark](../benchmark/intro.md) |
| 带宽 / Bandwidth | 单位时间传输的字节数 | [内存](../hardware/memory.md) |
| 工作集 | 一段计算实际使用的数据集合 | [缓存](../memory-model/cache.md) |
| NUMA | 内存位置不同，访问代价也可能不同 | [NUMA](../memory-model/numa.md) |
| 进程 / Process | 通常拥有独立地址空间的运行实例 | [进程](../thread-process/process.md) |
| 线程 / Thread | 共享进程地址空间的执行单元 | [线程](../thread-process/thread.md) |
| 数据竞争 | 未正确同步的冲突数据访问 | [内存模型](../memory-model/intro.md) |
| Rank | 进程在通信器里的编号 | [MPI](../parallel-programming/mpi.md) |
| 归约 / Reduction | 将多个结果按某种运算合并 | [通信](../communication/intro.md) |
| Kernel | 在 GPU 上由许多线程执行的函数 | [GPU](../gpu/intro.md) |
| Warp | NVIDIA CUDA 中的 32 线程调度分组 | [GPU 架构](../gpu/arch.md) |
| 残差 / Residual | 把算出的解代回方程后的差 | [科学计算](../sci-mlsys/intro.md) |
| Batch | 一起处理的一组样本 | [并行训练](../sci-mlsys/parallelism.md) |
| 量化 / Quantization | 用有限的离散值近似原始数值 | [量化](../sci-mlsys/quantization.md) |

遇到新名词时，先回到它在程序中的作用，再记缩写。GB 表示十进制字节单位，GiB 表示二进制字节单位；FLOP 是一次浮点运算，FLOP/s 是每秒浮点运算数。
