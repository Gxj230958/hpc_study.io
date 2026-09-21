"""Symmetric per-tensor INT8 quantization; a numerical demo, not an INT8 kernel."""
import numpy as np

rng = np.random.default_rng(7)
weights = rng.normal(size=(128, 128)).astype(np.float32)
scale = np.max(np.abs(weights)) / 127
q = np.clip(np.rint(weights / scale), -127, 127).astype(np.int8)
restored = q.astype(np.float32) * scale
error = np.max(np.abs(weights - restored))
assert error <= scale / 2 + 1e-6
print(f"scale={scale:.8f} max_abs_error={error:.8f} weight_bytes={weights.nbytes} quantized_bytes={q.nbytes} PASS")
