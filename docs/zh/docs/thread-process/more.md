# 任务、线程池与混合并行

会使用进程与线程后，还需要决定任务大小。本节帮助你避免“创建更多工作者就更快”的误区。

## 任务不等于线程

任务是一份需要完成的工作。线程是执行工作的载体。一个线程可以连续执行很多任务。线程池保留一组工作线程，把新任务交给空闲线程，从而减少反复创建线程的开销。

任务太小，调度成本可能超过计算成本。任务太大，最后剩下的一个任务可能让其他工作者空闲。规则循环可以先均匀分块；任务耗时差异大时，再考虑动态调度。

## MPI 加 OpenMP

常见组合是一台节点运行几个 MPI 进程，每个进程使用多个 OpenMP 线程。例如 2 个进程各使用 4 个线程，总共可能占用 8 个计算线程。

Python 中调用 BLAS 时，也可能自动创建线程。若你启动 8 个进程，每个 BLAS 又开 8 个线程，可能出现 64 个线程争抢少量 CPU 的情况。先限制：

```bash
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
mpiexec -n 4 python examples/mpi/sum.py --n 100003
```

## Python 的补充说明

常规带 GIL 的 CPython 中，多个线程通常不能同时执行 Python 字节码。但数值库可能释放 GIL，并调用自己的并行实现。不要把 Python 线程限制直接套到 NumPy 或所有 Python 构建上。

练习：每个任务只做一次整数加法，启动一万个线程是否合理？

??? success "参考答案"
    通常不合理。创建和调度线程的成本远高于一次加法。把大量加法合成较大的任务，交给有限数量的工作线程更合适。

参考：[Python threading 文档](https://docs.python.org/3/library/threading.html)、[OpenMP 任务模型](https://www.openmp.org/specifications/)。
