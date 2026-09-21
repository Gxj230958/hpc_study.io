# GPU 架构：线程怎样组织起来

本节学习程序执行所需的最小硬件概念。先理解[硬件导论](../hardware/hardware-intro.md)中的计算与搬运。

## CPU 与 GPU 的分工

CPU 通常重视复杂控制流和单线程响应。GPU 通常重视大量并行任务的吞吐量。两者都可以进行并行运算；不能简单地说 CPU 只能串行。

![CPU 与 GPU 的结构示意](images/cuda/cpu-gpu-arch-diff.png)

图片沿用原教程，来源为 [NVIDIA CUDA Refresher](https://developer.nvidia.com/blog/cuda-refresher-reviewing-the-origins-of-gpu-computing/)。它是设计取向的示意，不代表每种芯片的精确面积比例。

## Thread、block、grid

CUDA 线程组成 block，多个 block 组成 grid。常见一维下标计算为：

```cpp
int i = blockIdx.x * blockDim.x + threadIdx.x;
if (i < n) output[i] = input[i] * 2;
```

block 中的线程可以通过共享内存协作。`__syncthreads()` 是 block 范围的同步，不能同步整个 grid。不同 block 的调度顺序不应成为算法的前提。

在 NVIDIA CUDA 中，warp 包含 32 个线程。SM 调度 warp 来隐藏部分等待。不要把 warp 大小推广为所有厂商 GPU 的固定规则。

## 四种需要认识的存储

寄存器主要保存线程自己的值。共享内存由同一个 block 的线程协作使用。全局内存容量大，供 kernel 访问。缓存帮助复用数据，但命中情况取决于访问模式。

线程分支不一致可能让同一 warp 分批执行不同路径。这叫分支发散。它影响性能，并不表示所有 `if` 都应该删除；边界检查首先保证正确性。

练习：n=1000，每个 block 256 个线程，要启动多少个 block？

??? success "参考答案"
    向上取整得到 4 个，共 1024 个线程。最后 24 个线程必须通过 `i < n` 避免访问越界。

参考：[CUDA 编程模型](https://docs.nvidia.com/cuda/archive/12.4.1/cuda-c-programming-guide/index.html#programming-model)。
