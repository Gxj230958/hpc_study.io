# OpenACC：用指令描述加速

OpenACC 允许在 C、C++、Fortran 程序中添加编译指令，让编译器处理部分设备并行细节。本节目标是理解循环并行与数据区域的关系。

## 一个能直接编译的 CPU 示例

下面的程序保存为 `acc.c`。它先使用 GCC 的主机执行模式验证语义，不要求 GPU：

```c
#include <stdio.h>
int main(void) {
    float a[1000];
    #pragma acc parallel loop copyout(a[0:1000])
    for (int i = 0; i < 1000; ++i) a[i] = 2.0f * i;
    for (int i = 0; i < 1000; ++i)
        if (a[i] != 2.0f * i) return 1;
    puts("PASS");
    return 0;
}
```

```bash
gcc -O2 -fopenacc acc.c -o acc
ACC_DEVICE_TYPE=host ./acc
```

这证明主机路径能执行，不证明 GPU offload 已成功。使用 NVIDIA HPC SDK 时可用 `nvc -acc -Minfo=accel acc.c -o acc`，再根据编译反馈和运行时设备信息确认设备执行。本课程未把该可选编译器列为默认依赖。

## 数据区域往往比一行 pragma 更重要

`copyin` 将输入送往设备，`copyout` 把输出带回，`copy` 表示双向需求。多次循环可以放在一个较大的 data 区域中，让数据留在设备上。否则计算节省的时间可能被反复传输抵消。

编译器不能替你证明所有算法都可并行。若一次迭代读取前一次迭代刚写的结果，需要先改变算法或使用适当依赖表达。

练习：连续十次更新同一数组，每次都复制回主机，而主机只用最终结果，哪里可能浪费时间？

??? success "参考答案"
    中间九次回传可能没有必要。可以扩大数据区域，但要正确标记数据何时在主机或设备上更新，避免读到旧值。

参考：[OpenACC 规范](https://www.openacc.org/specification)、[GCC OpenACC](https://gcc.gnu.org/onlinedocs/libgomp/OpenACC.html)。
