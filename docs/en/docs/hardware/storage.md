# Storage

**Prerequisites:** Files and memory. **Objective:** Separate storage throughput from compute throughput.

Local SSDs, network filesystems and object stores have different latency, throughput and consistency characteristics. Many small file operations may be limited by metadata service rather than bulk bandwidth.

A training loop can wait on decoding, preprocessing or transfer even when the GPU is idle. Measure the data pipeline before increasing accelerator count. Warm filesystem caches can also change repeated results.

The course uses synthetic inputs so the initial experiments isolate numerical behavior. A production extension should record dataset location, cache state, I/O concurrency and failure recovery. Next, examine [benchmark design](../benchmark/intro.md).
