"""Checked AllReduce and DDP update against an independent global-batch model."""
import argparse
from datetime import timedelta
import os
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

p = argparse.ArgumentParser()
p.add_argument("--backend", choices=["gloo", "nccl"], default="gloo")
p.add_argument("--train", action="store_true")
args = p.parse_args()
torch.set_num_threads(1)
local_rank = int(os.environ["LOCAL_RANK"])
device = torch.device("cpu")
if args.backend == "nccl":
    if local_rank >= torch.cuda.device_count():
        p.error("NCCL requires one visible GPU per local worker")
    torch.cuda.set_device(local_rank)
    device = torch.device("cuda", local_rank)
    torch.backends.cuda.matmul.allow_tf32 = False
dist.init_process_group(args.backend, timeout=timedelta(seconds=60))
try:
    rank, world = dist.get_rank(), dist.get_world_size()
    value = torch.tensor([rank + 1.0], device=device)
    dist.all_reduce(value)
    assert value.item() == world * (world + 1) / 2
    print(f"rank={rank} world={world} backend={args.backend} allreduce={value.item()} PASS", flush=True)
    if args.train:
        torch.manual_seed(7)
        initial = torch.nn.Linear(4, 1)
        reference = torch.nn.Linear(4, 1)
        reference.load_state_dict(initial.state_dict())
        model = DDP(initial.to(device), device_ids=[local_rank] if args.backend == "nccl" else None)
        # Every rank reconstructs the same global batch; each trains on its own shard.
        g = torch.Generator().manual_seed(19)
        x = torch.randn(world * 8, 4, generator=g)
        y = x.sum(dim=1, keepdim=True) * 0.25
        optimizer = torch.optim.SGD(model.parameters(), lr=0.05)
        reference_optimizer = torch.optim.SGD(reference.parameters(), lr=0.05)
        for _ in range(5):
            optimizer.zero_grad()
            prediction = model(x[rank*8:(rank+1)*8].to(device))
            torch.nn.functional.mse_loss(prediction, y[rank*8:(rank+1)*8].to(device)).backward()
            optimizer.step()
            reference_optimizer.zero_grad()
            torch.nn.functional.mse_loss(reference(x), y).backward()
            reference_optimizer.step()
        for actual, expected in zip(model.module.parameters(), reference.parameters()):
            torch.testing.assert_close(actual.cpu(), expected, rtol=1e-4, atol=1e-6)
        print(f"rank={rank} DDP matches global-batch SGD PASS", flush=True)
finally:
    dist.destroy_process_group()
