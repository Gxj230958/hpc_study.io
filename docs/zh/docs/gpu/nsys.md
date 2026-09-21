# Nsight Systems：在时间线上找等待

优化前先观察程序。Nsight Systems 展示 CPU 调用、CUDA kernel 和数据传输的时间线。本节不要求理解 GPU 的每个硬件计数器。

## 先提出问题

程序是否频繁复制数据？kernel 之间是否有很长的空白？CPU 是否每启动一次 kernel 就同步？带着一个问题采样，比收集大量图表更有效。

```bash
nsys profile --trace=cuda,nvtx --sample=none --cpuctxsw=none -o build/cuda-trace ./build/cuda_labs
nsys stats build/cuda-trace.nsys-rep
```

先确保示例编译成功。采样会增加开销，报告中的时间不应直接替代无 profiler 的正式计时。文件已存在时更换名字，避免覆盖需要保留的记录。

## 三种区域

CUDA API 区域表示 CPU 发出操作的过程。kernel 区域表示设备执行。Memcpy 区域表示数据传输。CPU 发出调用很快，不意味着设备工作已经完成。

把报告复制到有图形界面的电脑，可以用兼容版本的 Nsight Systems 打开。无图形界面的服务器先用 `nsys stats` 查看汇总。

## 与 Nsight Compute 的区别

Systems 适合先看整个应用的阶段与等待。Compute 更关注某个 kernel 内部的执行效率和硬件计数器。先找值得优化的 kernel，再深入研究访存、占用率等指标。

容器可能不允许 CPU 采样或 GPU 性能计数器访问。本文命令关闭 CPU 采样以减少权限要求；若 CUDA trace 仍失败，应记录实际错误，不把空报告视为测量成功。

练习：kernel 时间只占总时间的 10%，把它加速两倍，总程序能加速两倍吗？

??? success "参考答案"
    不能。忽略其他变化，总时间从 1 变成 0.9+0.1/2=0.95，加速比约为 1.053。应先关注占比更大的阶段。

参考：[Nsight Systems 用户指南](https://docs.nvidia.com/nsight-systems/UserGuide/index.html)。
