# HPC Study

从一台普通电脑开始，学习高性能计算。

先理解程序怎样使用硬件，再把工作分给多个线程和进程。随后进入 GPU，学习怎样检查结果、测量性能，并把这些方法用在科学计算和机器学习中。

[开始第一课](hardware/hardware-intro.md){ .md-button .md-button--primary }
[准备实验环境](learning/setup.md){ .md-button }

## 你的学习路线

| 阶段 | 这一章要解决的问题 | 从这里开始 |
| --- | --- | --- |
| 01 · 硬件 | 程序在计算，还是在等待数据？ | [认识一台计算机](hardware/hardware-intro.md) |
| 02 · 并行编程 | 怎样分工，才能既正确又高效？ | [进程与线程](thread-process/intro.md) |
| 03 · GPU 编程 | 怎样让许多线程一起处理数组？ | [第一个 GPU 程序](gpu/intro.md) |
| 04 · Benchmark | 这个加速结果可靠吗？ | [建立测量方法](benchmark/intro.md) |
| 05 · 科学计算与机器学习 | 如何把这些方法用在真实计算中？ | [从方程到训练](sci-mlsys/intro.md) |

## 今天可以完成的第一个实验

用一个循环把数组元素加起来。再让四个线程分工，检查答案是否相同。

```bash
make -C examples cpu
OMP_NUM_THREADS=1 ./build/sum 100003
OMP_NUM_THREADS=4 ./build/sum 100003
```

运行前完成[环境准备](learning/setup.md)。两次都应显示 `PASS`。速度可能不同，也可能没有明显加速；这正是下一步要观察的问题。

## 按自己的设备学习

**普通电脑**：完成硬件、OpenMP、单机 MPI、稀疏求解与量化实验。

**NVIDIA GPU**：继续运行 CUDA、精度比较和单卡训练。没有 GPU 时，先跟随图解推导线程下标与数据流。

**集群或多卡**：选读 NUMA、通信拓扑、NCCL 和分布式训练，按照站点规则申请资源。

查看[全部实验](learning/labs.md)、[常用术语](learning/glossary.md)和[实际验证记录](learning/validation.md)。

<p><a href="downloads/hpc-study-examples.zip" download>下载完整实验源码</a></p>

## 来源与贡献

本课程基于 [HPC Wiki](https://github.com/hpcgame/hpc-wiki)，面向初学者补充中文讲解与可复现实验。保留原作者署名，遵循 CC BY-NC-SA 4.0。这里是独立学习站，内容贡献通过上游 Pull Request 交由维护者审阅。
