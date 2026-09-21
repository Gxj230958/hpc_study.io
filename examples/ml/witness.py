"""A seeded CUDA dispatch check, not a benchmark."""
import torch

torch.manual_seed(7)
assert torch.cuda.is_available(), "CUDA device unavailable"
a = torch.randn(32, 32)
b = torch.randn(32, 32)
actual = (a.cuda() @ b.cuda()).cpu()
torch.testing.assert_close(actual, a @ b, rtol=1e-4, atol=1e-4)
print("WITNESS PASS", tuple(actual.shape), torch.cuda.get_device_name(0))
