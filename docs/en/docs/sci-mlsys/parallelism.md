# Training Parallelism

**Prerequisites:** Training loops and collectives. **Objective:** Relate gradient averaging to the global batch.

Data parallelism places a model replica on each worker and gives each a different input shard. DistributedDataParallel synchronizes gradients during backward. With equal local batch sizes and mean losses, averaging gradients matches a mean loss over the concatenated global batch.

Unequal local batch sizes require weighting. Repeating identical data on all ranks may pass parameter-equality checks while failing to represent the intended training problem. Validate against an independent global-batch update as the supplied DDP program does.

Tensor parallelism splits an operation across devices; pipeline parallelism places different model stages on different devices. These change communication patterns and memory use. Next, execute [checked DDP](../clusters/distributed.md) before investigating scaling.
