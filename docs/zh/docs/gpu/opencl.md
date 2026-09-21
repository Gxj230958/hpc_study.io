# OpenCL：平台、设备与命令队列

OpenCL 提供跨多种设备的计算接口。可移植接口不等于在所有设备上具有相同性能。本节学习 host 与 kernel 的分工。

## 主机负责安排工作

主机先枚举平台与设备，创建 context 和命令队列，再分配缓冲区、构建程序、设置 kernel 参数并提交执行。一个 work-item 类似一次工作实例，work-group 把一组实例组织在一起。

kernel 端的向量加法可以写成：

```c
__kernel void add(__global const float *a,
                  __global const float *b,
                  __global float *c, const int n) {
    size_t i = get_global_id(0);
    if (i < n) c[i] = a[i] + b[i];
}
```

这只是设备端程序，不能直接当成普通 C 程序运行。完整主机代码还必须负责参数、缓冲区、执行范围和结果读取。可从 Khronos 的 [OpenCL SDK 示例](https://github.com/KhronosGroup/OpenCL-SDK)取得完整程序。

## 环境练习

安装厂商支持的 OpenCL 实现及 `clinfo` 后运行：

```bash
clinfo
```

记录平台、设备类型、OpenCL 版本和最大工作组大小。没有平台通常意味着运行时或 ICD 配置缺失，不等于机器没有任何计算设备。

OpenCL 不同版本的功能并非在所有设备上都强制提供。代码使用某个特性前，需要查询设备支持情况。初学先使用基础缓冲区和简单 kernel。

## 迁移时检查什么

检查工作组大小、局部存储限制、精度支持和同步范围。一个 work-group 的 barrier 不能作为整个设备的全局 barrier。

练习：向量长度 1000，工作组大小 256，将全局范围补齐到 1024 后，还需要什么？

??? success "参考答案"
    kernel 中保留 `i < n` 边界检查，并确保所选工作组大小被设备和 kernel 支持。多出来的实例不应访问数组。

参考：[Khronos OpenCL 文档](https://registry.khronos.org/OpenCL/)。本课程未把本页列为 OpenCL 设备实测。
