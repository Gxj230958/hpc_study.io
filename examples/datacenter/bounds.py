"""Calculated teaching bounds from explicit inputs, never hardware measurements."""
import argparse

p = argparse.ArgumentParser()
p.add_argument("--bandwidth-gbps", type=float, default=3350)
p.add_argument("--peak-tflops", type=float, default=67)
p.add_argument("--capacity-gb", type=float, default=80)
args = p.parse_args()
assert all(x > 0 for x in vars(args).values())
# FP32 vector addition: two reads and one write, one FLOP per output.
intensity = 1 / 12
bound = min(args.peak_tflops, args.bandwidth_gbps * intensity / 1000)
max_elements = int(args.capacity_gb * 1e9 * 0.8 / 12)
assert bound <= args.peak_tflops
assert max_elements * 12 <= args.capacity_gb * 1e9 * 0.8
print(f"CALCULATED roofline_TFLOPS={bound:.6f} three_vector_elements_at_80pct={max_elements} PASS units_and_capacity")
