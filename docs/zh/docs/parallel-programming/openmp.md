# OpenMP：把第一个循环分给多个线程

OpenMP 用编译指令表达共享内存并行。本节从正确求和开始。需要会编译 C 程序，并读过[线程](../thread-process/thread.md)。

## 编译和运行

```bash
make -C examples cpu
OMP_NUM_THREADS=1 ./build/sum 100003
OMP_NUM_THREADS=4 ./build/sum 100003
```

完整源码在 `examples/cpu/sum.c`。`-fopenmp` 同时启用编译支持和运行库链接；只写 pragma 而未正确启用编译选项，可能仍然串行执行。

## 最重要的一行

```c
#pragma omp parallel for reduction(+:sum) schedule(static)
for (long i = 0; i < n; ++i) sum += a[i];
```

`parallel for` 让线程共同执行循环。`reduction` 为线程维护部分和，再合并。`static` 采用预先确定的分配方式，适合每次迭代工作量相近的循环。

数组只读，可以共享。循环下标由并行循环规则管理。若改为多个线程写相同元素，需要重新分析是否有数据竞争。不要把任意循环都直接加上 pragma。

## 从正确走向测量

程序用整数求和并与解析结果 `n*(n-1)/2` 对照。它限制 n 的范围，避免本例中的整数溢出和过大分配。先通过 `PASS`，再比较时间。

使用 n=1、17、100003 检查边界，再使用更大的数组观察性能。短任务会被线程启动开销主导。不能只记录最快的一次。

## 本章综合实验（约 3 小时）

用 1、2、4、8 个线程，各运行五次 n=10000000 的求和。计算中位数、加速比 `T1/Tp` 和效率 `T1/(p*Tp)`。把数组规模缩小，解释趋势是否改变。

练习：为什么不能删除 `reduction`，直接让所有线程修改 `sum`？

??? success "参考答案"
    普通读改写产生数据竞争。可用原子加法或锁保证特定操作正确，但每次迭代争抢同一位置通常代价较高，局部归约更合适。

参考：[OpenMP 规范与示例](https://www.openmp.org/specifications/)。
