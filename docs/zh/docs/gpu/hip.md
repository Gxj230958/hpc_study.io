# HIP：理解 CUDA 风格代码的迁移

HIP 提供与 CUDA 相近的 C++ GPU 编程模型。本节介绍迁移的起点，AMD 设备上的完整验证需要相应硬件与 ROCm 环境。

## 熟悉的结构

线程、block、grid、设备内存和流等概念仍然适用。下面是 kernel 与启动方式的示意：

```cpp
#include <hip/hip_runtime.h>
__global__ void twice(const float *a, float *b, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) b[i] = 2 * a[i];
}
// 主机已正确分配 da、db，并设定 n 后：
// hipLaunchKernelGGL(twice, dim3((n+255)/256), dim3(256), 0, 0, da, db, n);
```

完整程序仍需分配、复制、错误检查与释放资源。安装 ROCm 后，先运行 `hipcc --version` 和设备查询，再运行官方 HIP 示例。不应仅把扩展名改成 `.cpp` 就认定迁移完成。

## 从 API 替换到真正可移植

HIPIFY 可以辅助替换部分 API。之后仍要检查第三方库、编译选项、内联汇编、warp 假设和数值行为。与厂商库绑定的代码通常比简单 kernel 更难迁移。

尤其不要把 CUDA 的 32 线程 warp 常数传播到所有 GPU。使用后端提供的查询或抽象，并理解具体同步语义。相同源码也可能需要不同的线程块大小才能获得合适性能。

## 迁移清单练习

阅读 `examples/cuda/labs.cu`，把需要变化的部分分成三类：运行时 API、编译配置、硬件假设。边界检查和 CPU 正确性参考应继续保留。

??? success "参考答案"
    `cudaMalloc` 等属于 API；`nvcc` 和 `sm_89` 属于构建配置；共享内存大小、线程组织和 warp 相关优化属于硬件约束。本例的基本矩阵算法不因 API 名字变化而改变。

参考：[AMD HIP 文档](https://rocm.docs.amd.com/projects/HIP/en/latest/)、[HIPIFY](https://rocm.docs.amd.com/projects/HIPIFY/en/latest/)。只有 NVIDIA 单卡的验证环境不能声称通过了 AMD 后端测试。
