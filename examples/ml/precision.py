"""Accuracy and synchronized timing of CPU FP32, CUDA FP32 and FP16."""
import json
import statistics
import time
import torch

torch.manual_seed(7)
torch.set_num_threads(4)
torch.backends.cuda.matmul.allow_tf32 = False
a = torch.randn(512, 512)
b = torch.randn(512, 512)
reference = a.double() @ b.double()
for device, dtype in [("cpu", torch.float32), ("cuda", torch.float32), ("cuda", torch.float16)]:
    if device == "cuda" and not torch.cuda.is_available():
        print("SKIP CUDA: no device")
        continue
    x, y = a.to(device=device, dtype=dtype), b.to(device=device, dtype=dtype)
    for _ in range(5):
        out = x @ y
    if device == "cuda":
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
    samples = []
    for _ in range(20):
        start = time.perf_counter()
        out = x @ y
        if device == "cuda":
            torch.cuda.synchronize()
        samples.append((time.perf_counter() - start) * 1000)
    relative_error = (out.cpu().double() - reference).norm() / reference.norm()
    assert relative_error < (1e-3 if dtype == torch.float16 else 1e-5)
    print(json.dumps({"device":device, "dtype":str(dtype), "median_ms":statistics.median(samples), "samples_ms":samples,
                      "relative_l2_error":relative_error.item(), "timing":"resident inputs, host clock, synchronized",
                      "peak_allocated_bytes":torch.cuda.max_memory_allocated() if device == "cuda" else None,
                      "status":"PASS"}))
