# FPGAs and ASICs

**Prerequisites:** Basic processor and memory concepts. **Objective:** Explain specialization tradeoffs.

An FPGA is reconfigurable hardware whose logic and data paths can be programmed. An ASIC implements a more fixed function in silicon. Both can exploit a carefully designed pipeline with tailored data movement.

Specialization can improve throughput or energy efficiency but introduces toolchain, development-time and flexibility costs. A fast pipeline must still receive data fast enough and implement the required numerical semantics.

This is a conceptual reference, with no FPGA/ASIC hardware validation in this course. Next, compare it with [GPU architecture](../gpu/arch.md).
