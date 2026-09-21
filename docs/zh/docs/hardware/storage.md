# 存储与 I/O：让数据跟上计算

程序需要把输入读进内存，并把结果保存下来。本节学习顺序读写、随机访问、文件系统与缓存的区别。

## 不要把磁盘当作慢一点的内存

文件按路径访问，文件系统负责目录、权限和数据位置。SSD、机械硬盘和网络文件系统的访问特征不同。打开一万个小文件，可能花很多时间在元数据操作上，尽管总字节数不大。

操作系统通常用空闲内存缓存文件。第二次读取可能直接命中页缓存。因此，“再次读取变快”不一定说明磁盘更快。

## 一个小而安全的观察

在自己的实验目录执行，先确认至少有 128 MiB 空间：

```bash
mkdir -p build/io
df -h build/io
dd if=/dev/zero of=build/io/sample.bin bs=1M count=64 conv=fdatasync
dd if=build/io/sample.bin of=/dev/null bs=1M
dd if=build/io/sample.bin of=/dev/null bs=1M
```

文件名固定为自己的示例文件，不要替换成块设备。`fdatasync` 要求结束前同步文件数据；它仍不能完全代表所有文件系统的持久化语义。这里的读取很可能命中缓存，所以这是缓存观察，不是正式磁盘测速。

## 科学计算和机器学习中的 I/O

检查点保存中间状态，便于中断后继续计算。写得太频繁会占用大量时间，写得太少则增加恢复时的损失。分布式程序还需要保证各进程保存的是同一训练步或迭代步。

数据加载可以与计算重叠，但后台线程过多会争抢 CPU 和磁盘。先测 GPU 是否在等数据，再增加预取。

练习：文件两次读取耗时不同，报告应该记录什么？

??? success "参考答案"
    记录文件大小、文件系统、命令、是否可能命中缓存、是否同步写入和重复次数。不随意清理共享机器的全局缓存，也不把缓存吞吐量当作磁盘速度。

参考：[GNU dd 手册](https://www.gnu.org/software/coreutils/manual/html_node/dd-invocation.html)、[Linux 页缓存](https://docs.kernel.org/mm/page_cache.html)。
