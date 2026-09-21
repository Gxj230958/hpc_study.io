"""Small synthetic regression, for learning the training loop, not model quality."""
import argparse
import copy
import torch

p = argparse.ArgumentParser()
p.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
args = p.parse_args()
torch.manual_seed(7)
torch.set_num_threads(4)
x = torch.randn(256, 8)
truth = torch.arange(8, dtype=torch.float32).view(8, 1) / 8
y = x @ truth + 0.1
model = torch.nn.Linear(8, 1)
cpu_model = copy.deepcopy(model)
with torch.no_grad():
    expected = cpu_model(x)
model = model.to(args.device)
x, y = x.to(args.device), y.to(args.device)
with torch.no_grad():
    torch.testing.assert_close(model(x).cpu(), expected, rtol=1e-4, atol=1e-5)
opt = torch.optim.SGD(model.parameters(), lr=0.1)
losses = []
for step in range(100):
    opt.zero_grad()
    prediction = model(x)
    loss = torch.nn.functional.mse_loss(prediction, y)
    loss.backward()
    opt.step()
    losses.append(loss.item())
assert losses[-1] < losses[0] * 0.01
print(f"device={args.device} initial_loss={losses[0]:.6f} final_loss={losses[-1]:.9f} PASS synthetic_regression")
