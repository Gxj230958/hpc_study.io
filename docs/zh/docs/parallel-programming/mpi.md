# MPI：用消息连接多个进程

MPI 是消息传递接口标准，不是一台机器，也不是某个厂商的产品。MPICH、Open MPI 等提供具体实现。本节学习程序的基本生命周期。

## 一个最小 C 程序

将下面的完整内容保存为 `hello.c`：

```c
#include <mpi.h>
#include <stdio.h>
int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    printf("rank %d of %d\n", rank, size);
    MPI_Finalize();
    return 0;
}
```

```bash
mpicc -O2 hello.c -o hello
mpiexec -n 2 ./hello
```

`mpicc` 是编译器包装器，会补充 MPI 头文件与库。C 开发环境需要系统 MPI 开发包；Python 入门环境中的打包运行时不一定提供 `mpicc`。不要混用两个 MPI 实现的编译器和启动器。

## 怎样理解输出

每个进程从 main 开始执行，获得自己的 rank。输出顺序可能变化，不能用终端打印顺序判断计算先后。`MPI_COMM_WORLD` 是本次作业中的一个通信器，它定义参与者范围。

`MPI_Init` 建立运行环境，`MPI_Finalize` 结束 MPI 使用。异常退出要考虑其他进程是否仍在等待。

## 真正的并行工作

下一节的[mpi4py](mpi4py.md)实现分块求和。C 版本通常用 `MPI_Reduce` 合并结果。注意 datatype 必须匹配缓冲区的真实类型；元素个数不是字节数。

练习：用四个进程运行，是否会自动让同一个串行循环快四倍？

??? success "参考答案"
    不会。未分块的程序可能让每个进程重复做全部工作。需要按 rank 划分输入，并明确如何合并结果。

参考：[MPI Forum 文档](https://www.mpi-forum.org/docs/)、[MPICH](https://www.mpich.org/documentation/)。
