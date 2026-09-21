# 一致性与 happens-before

为什么“代码写在前面”不一定足够？本节用生产者与消费者解释同步。需要先读[内存模型导论](intro.md)。

## 建立先后关系

生产者先准备数据，再通知消费者。消费者必须在收到有效通知后读取数据。我们希望建立一条可以推理的先后链，而不是依赖运行速度。

下面是 C++ 的教学片段，`data` 只有一个生产者写，且不会再次修改：

```cpp
std::atomic<bool> ready{false};
int data = 0;
// 生产者线程
data = 42;
ready.store(true, std::memory_order_release);
// 消费者线程
while (!ready.load(std::memory_order_acquire)) {}
assert(data == 42);
```

需要包含 `<atomic>` 和 `<cassert>`，并由两个线程分别执行相应部分。消费者的 acquire 读取到生产者 release 写入的 `true` 时，先前的数据写入得到正确发布。这是特定协议，不能任意扩展成多生产者、多次重用的队列。

## 初学时选择简单规则

默认顺序一致的原子操作更容易推理。`memory_order_relaxed` 只保证该原子操作自身的规则，不能直接代替上面的发布关系。能用锁或成熟容器解决的问题，先不要手写无锁算法。

忙等还会持续消耗 CPU。实际应用经常使用条件变量，让等待线程休眠，并在醒来后重新检查条件。

练习：消费者没有读到 `true`，却提前读取 `data`，上面的论证还成立吗？

??? success "参考答案"
    不成立。同步依赖于 acquire 实际观察到相应发布。不能把原子变量的存在当作保护所有共享数据的万能屏障。

参考：[C++ 标准草案：原子内存序](https://eel.is/c++draft/atomics.order)。本页是理解概念的选读内容，入门实验优先使用 OpenMP 归约。
