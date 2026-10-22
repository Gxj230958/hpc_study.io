# Quantization

**Prerequisites:** Floating-point arrays and error norms. **Objective:** Derive the error and storage cost of a simple quantizer.

Symmetric per-tensor INT8 quantization uses one scale for a tensor: q=round(w/scale), clipped to [-127,127], then restores w approximately as scale*q. The course chooses scale from the maximum absolute input.

For calibrated inputs, rounding error is bounded by scale/2 up to floating-point roundoff. Calibration outliers, clipping and all-zero tensors require additional handling in a general implementation. Per-channel scales can improve accuracy at the cost of more metadata and a different implementation.

Storing INT8 weights does not prove an INT8 arithmetic kernel executed. Actual acceleration depends on operator support, layouts, scale handling and hardware. Next, measure [quantization error](intro.md#quantization-error).
