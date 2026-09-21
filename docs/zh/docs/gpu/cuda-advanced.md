# CUDA 优化：先少搬数据，再测量

本节在正确 kernel 的基础上学习三个方法：合并访存、共享内存分块和减少同步。先完成 [CUDA 入门](cuda.md)。

## 相邻线程读相邻数据

若一个 warp 的线程访问相邻的数组元素，硬件往往能用较少的内存事务完成访问。让相邻线程跨很大步长读取，可能浪费带宽。实际事务还受对齐和数据类型影响。

合并访存与缓存复用不同。前者关注一组线程怎样发起访问，后者关注同一数据能否再次利用。

## 分块矩阵乘法

计算 C=A×B 时，C 的一个元素需要一行 A 和一列 B。朴素实现会重复读取很多元素。仓库的 `matmul` kernel 把 A、B 的 16×16 小块先放入共享内存，再由 block 内线程复用。

每轮需要两次同步：第一次保证小块已经载入，第二次保证所有线程都用完旧数据，才能覆盖共享内存。边缘线程也要参加同步，只把越界加载替换成零。

```bash
make -C examples cuda
./build/cuda_labs
compute-sanitizer --tool memcheck ./build/cuda_labs
compute-sanitizer --tool synccheck ./build/cuda_labs
```

完整源码为 `examples/cuda/labs.cu`。n=15、16、17 可以专门检查分块边界。该教学实现用于理解分块，不声称优于 cuBLAS。

## 归约与流

归约 kernel 让 256 个线程分层相加，输出每个 block 的部分和；CPU 完成最后一次合并。缺失元素填零，所有线程参加 barrier。

流是设备工作的有序队列。同一流中的操作按规定顺序执行，不同流可能重叠。异步传输通常还需要合适的主机内存和硬件条件。先在时间线上确认重叠，不要把 API 名字中的 Async 当成加速证明。

## 综合实验（约 3 小时）

阅读三个 kernel，画出 n=17 矩阵的边界块。记录正确性与 sanitizer 结果。再比较向量加法的内核时间和含传输时间，解释小输入为什么不适合直接讨论峰值吞吐量。

练习：能否在矩阵 kernel 开头让所有越界线程立即 return？

??? success "参考答案"
    不能简单这样改，因为后面有 block 同步。应让边缘线程参与协作和 barrier，只对加载、写回进行边界判断。

参考：[CUDA 最佳实践指南](https://docs.nvidia.com/cuda/archive/12.4.1/cuda-c-best-practices-guide/index.html)。
