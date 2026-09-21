# mpi4py：用 Python 练习消息传递

mpi4py 把 MPI 接口带到 Python。本节适合已经会写 Python 循环的读者，无需先熟悉 C。

## 从不均匀分块开始

```bash
mpiexec -n 3 python examples/mpi/sum.py --n 10
mpiexec -n 4 python examples/mpi/sum.py --n 100003
```

先按[环境准备](../learning/setup.md)激活环境。程序按 `n*rank//size` 和 `n*(rank+1)//size` 计算左右边界。右边界不包含在区间中，因此相邻区间不重叠。

## 看懂核心代码

```python
from mpi4py import MPI
comm = MPI.COMM_WORLD
lo = n * comm.rank // comm.size
hi = n * (comm.rank + 1) // comm.size
partial = sum(range(lo, hi))
total = comm.reduce(partial, op=MPI.SUM, root=0)
```

这是完整示例中的核心片段。`reduce` 的有效总结果位于 root，其他 rank 不应把返回值当成完整总和。所有参与进程都需要执行这个调用。

## 小写与大写接口

`send`、`recv` 等小写接口可以传 Python 对象，通常涉及序列化。`Send`、`Recv` 等大写接口面向缓冲区，适合连续 NumPy 数组。后者可以减少对象处理开销，但需要正确匹配数据布局和类型。

`examples/mpi/pingpong.py` 使用 `uint8` 数组和大写接口。初学时先用连续数组，避免切片步长导致的额外复杂性。

练习：为什么计时要取各 rank 耗时的最大值，而不是只看最快的 rank？

??? success "参考答案"
    整个作业需要等待相关工作全部完成。最快 rank 不能代表总体完成时间。示例用最大值汇总计时，但更严格的应用测量还要定义统一的起止范围。

参考：[mpi4py 官方教程](https://mpi4py.readthedocs.io/en/stable/tutorial.html)。
