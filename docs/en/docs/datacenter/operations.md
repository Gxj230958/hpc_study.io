# Scheduling and Cost

**Prerequisites:** [MIG and topology](topology.md), numerical checks and a workload description. **Objective:** Turn a candidate GPU into a testable allocation plan.

Specify the exact SKU or acceptable alternatives, full GPU or MIG profile, GPUs per node, CPU threads, host/device memory, wall time, network boundary, storage and software versions. Define the first small correctness run and a stop condition before scaling. Preserve a portable fallback.

Estimate memory from simultaneously live parameters, gradients, optimizer state, activations and workspace. A model's weight size alone is insufficient. Keep an explicit reserve and validate peak usage on the target before scheduling the full problem.

Calculate cost using a dated allocation quote and billed wall time, including setup and failed attempts. Queueing affects completion time; retries and preemption affect both time and cost. A hypothetical rate illustrates units but cannot establish current price/performance. Device TDP is not a bill or a measured energy result.

A one-page plan should include the correctness oracle, representative inputs, profiling permissions, source hash, launch placement, checkpoint/restart behavior, cleanup owner and unresolved assumptions. See the [hardware profile](/hpc_study.io/downloads/source/course/hardware-profile.json). Optional [AWS examples](../clusters/cloud.md) use already allocated instances only; provisioning is outside scope.

Next, complete [the porting-plan exercise](intro.md#porting-plan).
