# NCCL：多张 GPU 怎样合并数据

NCCL 提供 GPU 集合通信。它常被用于分布式训练中的梯度同步。本节先学数据含义；完整多卡实验需要至少两张兼容 GPU，本课程的单卡验证不能覆盖它。

## 以 AllReduce 为例

两张卡分别得到梯度 `[1,2]` 和 `[3,4]`。求和 AllReduce 完成后，两边都得到 `[4,6]`。如果需要平均梯度，还要按照训练定义处理除数。NCCL 的求和本身不等于平均。

逻辑上的集合操作可以通过不同通信算法实现。环形方法会分阶段传递分块；树形方法组织不同的连接关系。实际算法选择受消息大小、拓扑和实现影响。

## PyTorch 中的最小多卡示例

下列程序保存为 `allreduce.py`，仅在至少两张 GPU 的机器运行：

```python
import os
import torch
import torch.distributed as dist
local_rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(local_rank)
dist.init_process_group("nccl")
x = torch.tensor([float(dist.get_rank() + 1)], device="cuda")
dist.all_reduce(x, op=dist.ReduceOp.SUM)
assert x.item() == dist.get_world_size() * (dist.get_world_size() + 1) / 2
print(dist.get_rank(), x.item())
dist.destroy_process_group()
```

```bash
torchrun --standalone --nproc-per-node=2 allreduce.py
```

不要在一张 GPU 上启动两个进程后，把结果写成双卡通信性能。单机 CPU 多进程可以练习集合通信含义，但不能验证 NCCL 的 GPU 传输路径。

## 常见故障

rank 对应错 GPU、集合调用顺序不同、网络接口不可达，都可能导致失败或等待。先核对设备映射和进程数，再使用 `NCCL_DEBUG=INFO` 收集诊断信息。日志中的主机和网络信息不应原样公开到不相关位置。

练习：只有 rank 0 调用 AllReduce，其他 rank 跳过，是否正确？

??? success "参考答案"
    不正确。相关进程必须执行匹配的集合操作。先检查所有 rank 的控制流是否一致。

参考：[NCCL 用户指南](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/)、[PyTorch distributed](https://pytorch.org/docs/stable/distributed.html)。
