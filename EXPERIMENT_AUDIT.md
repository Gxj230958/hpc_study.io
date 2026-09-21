# Experiment Audit Report

Date: 2026-09-21
Project: hpc_study.io
Auditor: /root/experiment_integrity, fresh Codex reviewer; GPT-6-Astra ultra requested
Review independence: same-family
Acceptance status: provisional
Overall verdict: PASS
Integrity status: pass

This verdict covers the final corrected teaching examples and the artifacts archived at 2026-09-21T13:50:31.761832+00:00. It is not independent cross-family assurance, an official benchmark certification, or evidence of model generalization. The reviewer read every example, configuration, and the four requested evaluation/archive scripts line by line, read the retained result files and claim pages, recomputed hashes and reported medians, and ran no GPU experiment. A supporting fresh agent crosschecked the documentation and benchmark outputs.

All references below are relative to the repository root. In tables, RESULTS means docs/zh/docs/learning/results/2026-09-21.

## A. Ground Truth Provenance: PASS

No evaluation target was found to be an undisclosed function of the tested model's predictions.

| Evaluation | Reference provenance | Exact evidence |
| --- | --- | --- |
| OpenMP and MPI sums | Closed-form integer sum, independent of parallel output | examples/cpu/sum.c:23; examples/mpi/sum.py:20 |
| Memory access | Expected count of visits to an array initialized to one | examples/cpu/memory.c:10; examples/cpu/memory.c:17 |
| MPI ping-pong | Known all-one message contents | examples/mpi/pingpong.py:11; examples/mpi/pingpong.py:24 |
| CUDA add/reduction/matmul | Host input arithmetic, host double accumulation, independent CPU matrix product | examples/cuda/labs.cu:60; examples/cuda/labs.cu:83; examples/cuda/labs.cu:105 |
| Sparse CG | Manufactured sine solution produces b before solving; dense solve and equation residual check the result | examples/science/solve.py:8; examples/science/solve.py:11; examples/science/solve.py:14 |
| INT8 representation | Original seeded weights and an analytic rounding bound | examples/ml/quantize.py:4; examples/ml/quantize.py:9 |
| FP32/FP16 matrix product | FP64 CPU product of the original inputs | examples/ml/precision.py:12; examples/ml/precision.py:30 |
| CUDA witness | CPU matrix product of the same fixed-seed inputs; explicitly a dispatch check | examples/ml/witness.py:1; examples/ml/witness.py:9 |
| Training loss | y = x @ truth + 0.1 is generated before the trained model; no prediction-derived training labels | examples/ml/train.py:11; examples/ml/train.py:14; examples/ml/train.py:27 |
| Training forward equivalence | CPU copy of the same initial model; legitimately a backend-equivalence reference, not task ground truth | examples/ml/train.py:15; examples/ml/train.py:21 |
| HPL/HPCG | Official reference implementations and their residual/validation procedures | scripts/run-reference-benchmarks.sh:10; scripts/run-reference-benchmarks.sh:16; scripts/run-reference-benchmarks.sh:43 |

The retained HPL tarball matches the recorded SHA256 at RESULTS/reference/hpl-archive-sha256.txt:1. The retained HPCG HEAD matches RESULTS/reference/hpcg-revision.txt:1. A tracked HPCG Makefile is configured locally; the numerical and evaluator sources have no tracked modifications. The script builds in its separate build directory (scripts/run-reference-benchmarks.sh:27). These checks support source provenance but do not provide signed binary attestation.

Synthetic training is explicitly described as checking a training loop, not model quality (examples/ml/train.py:1; docs/zh/docs/sci-mlsys/intro.md:39). No real dataset, held-out task labels, or official MLPerf evaluation is claimed (docs/zh/docs/benchmark/mlperf.md:25).

## B. Score Normalization: PASS

No arbitrary output-max/min/mean denominator is used to inflate a task score.

- Precision relative L2 error divides by the independent FP64 reference norm (examples/ml/precision.py:30).
- Solver relative residual divides by the input right-hand-side norm (examples/science/solve.py:12).
- CUDA reduction tolerance scales with the CPU reference sum; the raw absolute error is printed (examples/cuda/labs.cu:83; examples/cuda/labs.cu:86).
- INT8 scale uses the original input weight range as part of the quantization algorithm. The reported error is raw absolute reconstruction error, not an output-normalized score (examples/ml/quantize.py:6; examples/ml/quantize.py:11).
- The training decrease condition compares final and initial loss; both are raw MSE values against independently generated y. This is a convergence smoke check, not a normalized accuracy claim (examples/ml/train.py:27; examples/ml/train.py:31).
- HPL's official backward-error denominator includes the computed solution norm by mathematical definition. This is a standard residual criterion, not a prediction-statistic normalization intended to inflate a model-quality score (RESULTS/reference/hpl/output.txt:39; RESULTS/reference/hpl/output.txt:53).
- CUDA time is divided by the known batch count of 100 launches, memory metrics by known visits/bytes, and ping-pong time by 100 round trips (examples/cuda/labs.cu:68; examples/cpu/memory.c:17; examples/mpi/pingpong.py:25).

Recomputed all three precision medians exactly from 20 saved samples each (RESULTS/checks/precision.txt:1). Recomputed all five unprofiled CUDA vector medians from 20 saved samples each, matching the reported values within six-decimal printing precision (RESULTS/checks/cuda.txt:2). Sanitizer and profiler timings are not pooled with normal timings (docs/zh/docs/learning/validation.md:27).

The printed training final_loss=0.000000000 is rounded to nine decimal places, not evidence of mathematically exact zero (examples/ml/train.py:32; RESULTS/checks/train-cpu.txt:1). No audited prose claims exact zero loss.

## C. Result Existence and Claim Matching: PASS

The final suite started at 2026-09-21T13:48:28.207585+00:00 and completed at 2026-09-21T13:49:15.003744+00:00. All 40 unique records have their matching text logs, all 40 passed, and every actual exit code equals its recorded expected code. Only sum-invalid returns 2; the other 39 return 0 (RESULTS/checks/summary.json:2; RESULTS/checks/summary.json:196; RESULTS/checks/summary.json:610). The count includes compilation and device checks; it is not 40 independent scientific experiments.

All 18 run-start hashes match current files (RESULTS/checks/summary.json:4); all 21 archive hashes also match (RESULTS/environment.json:14). The validator captures hashes before execution and rechecks after execution; the archiver rejects a change since that run (scripts/validate.py:21; scripts/validate.py:62; scripts/archive-validation.py:17). The browser report's script hash also matches current scripts/browser-check.py (RESULTS/browser-summary.json:3).

| Claim | Retained evidence | Impact |
| --- | --- | --- |
| 40 checks passed, invalid input expected to return 2 | docs/zh/docs/learning/validation.md:13; RESULTS/checks/summary.json:196; RESULTS/checks/summary.json:610 | Supported |
| Integer and MPI sums match references | RESULTS/checks/sum-4-100003.txt:1; RESULTS/checks/mpi-3-100003.txt:1; all other recorded configurations were read | Supported for listed inputs |
| CG converges and residual passes | RESULTS/checks/solve.txt:1, residual 3.852e-11, below 1e-10 | Supported for the 127-equation problem |
| INT8 representation error obeys the bound | RESULTS/checks/quantize.txt:1, scale 0.03198115 and error 0.01598990 | Supported; no INT8 inference-speed claim |
| CUDA boundary cases match CPU references | RESULTS/checks/cuda.txt:3; RESULTS/checks/cuda.txt:12 | Supported for five vector and five matrix sizes |
| Sanitizers report no errors | RESULTS/checks/cuda-memcheck.txt:18; RESULTS/checks/cuda-synccheck.txt:18; RESULTS/checks/cuda-racecheck.txt:18 | Supported for exercised kernels and inputs |
| Synthetic CPU/CUDA training and precision checks pass | RESULTS/checks/train-cpu.txt:1; RESULTS/checks/train-cuda.txt:1; RESULTS/checks/precision.txt:1 | Supported as toy numerical/training-loop checks |
| HPL residual and HPCG numerical validity pass | RESULTS/reference/hpl/output.txt:53; RESULTS/reference/HPCG-Benchmark_3.1_2026-09-21_13-08-17.txt:60; same report:119 | Supported as short reference runs only |
| Browser runs cover the stated two viewports and seven pages | RESULTS/browser-summary.json:4; RESULTS/browser-summary.json:14; RESULTS/browser-summary.json:26; scripts/browser-check.py:14; scripts/browser-check.py:17 | Supported by matching script and final result |
| Nsight captured three kernels and transfers | RESULTS/nsys-stats.txt:8; RESULTS/nsys-stats.txt:18 | Supported as a separate earlier capture |

Device name, 49140 MiB and driver 550.163.01 match RESULTS/checks/gpu-info.txt:2; compute capability 8.9 matches RESULTS/checks/cuda.txt:1. The unusual memory amount is explicitly an observed device report, not a general RTX 4090 specification (docs/zh/docs/learning/validation.md:9). Resource limits match RESULTS/environment.json:12. The checker transcript records installed PyTorch 2.6.0+cu124 and CUDA 12.4 (.aris/documented-invocation.md:12).

The final public prose no longer claims a separately archived independent replication. The retained task-agent response records documented invocation and explicitly says the archive contains only the final corrected run (.aris/documented-invocation.md:20; .aris/documented-invocation.md:28). This is evidence of a separate invocation-checking agent, not an additional performance sample or cross-family review.

## D. Dead Code and Unexecuted Metrics: PASS

Every metric in the claimed validation path is executed and has corresponding output.

- CUDA vectors() and matrices() are called for every documented boundary size by main(); all three kernels are launched and their correctness is checked (examples/cuda/labs.cu:56; examples/cuda/labs.cu:77; examples/cuda/labs.cu:100; examples/cuda/labs.cu:117).
- Python checks execute their metrics at module top level and are launched from scripts/validate.py:49 and scripts/validate.py:60.
- Official benchmark validity checks are invoked after each reference run (scripts/run-reference-benchmarks.sh:43).
- Browser assertions run over the declared page/view loops and the retained output has no failures (scripts/browser-check.py:14; scripts/browser-check.py:74).
- examples/cpu/acc.c and examples/mpi/hello.c are present and hashed but are not called by this 40-case suite. The Makefile CPU target only builds sum and memory (examples/Makefile:7). No successful execution of those two standalone examples is inferred from their presence or hashes. NVIDIA OpenACC offload is explicitly untested (docs/zh/docs/learning/validation.md:46).

## E. Scope Assessment: PASS

The claims are appropriately limited to teaching correctness on one node and one visible GPU. Actual retained coverage is:

| Workload | Inputs/configurations | Repeats/seeds retained |
| --- | --- | --- |
| OpenMP sum | 1/2/4/8 requested threads by n=1/17/100003; one invalid input | One invocation per configuration |
| Memory loop | 128 MiB array; stride 1/8/64 | One aggregate timing per stride, eight internal passes |
| MPI sum | 1/2/3/4 ranks by n=0/2/100003 | One invocation per configuration |
| MPI ping-pong | Two local ranks, 1/1024/1048576 bytes | Ten warm-ups then 100 timed round trips; one aggregate per size |
| CUDA | Vector n=1/255/256/257/100003; matrix n=1/15/16/17/65 | Five vector warm-ups; 20 batches of 100 add launches; separate sanitizer runs |
| Sparse solve | One manufactured SPD problem, n=127 | One input |
| INT8 representation | One 128x128 normal weight array | Seed 7 |
| CUDA witness | One 32x32 product | Seed 7 |
| Training | 256 examples, eight input features; CPU and CUDA | Seed 7; 100 training steps; no held-out set |
| Precision | One 512x512 pair; CPU FP32, CUDA FP32/FP16 | Seed 7; five warm-ups; 20 synchronized samples per mode |
| HPL | N=256, NB=64, P=Q=1 | One short reference run |
| HPCG | 16x16x16, one MPI process, two threads | One short run; measured 1.05638 seconds |
| Browser | 1440x1000 and 390x844; seven pages each | One retained final browser invocation |

Coverage evidence: scripts/validate.py:40; examples/cpu/memory.c:7; examples/mpi/pingpong.py:10; examples/cuda/labs.cu:61; examples/ml/train.py:9; examples/ml/precision.py:7; RESULTS/reference/hpl/output.txt:19; RESULTS/reference/HPCG-Benchmark_3.1_2026-09-21_13-08-17.txt:5.

HPCG itself states that the actual 1.05638-second run is below its 1800-second official minimum (RESULTS/reference/HPCG-Benchmark_3.1_2026-09-21_13-08-17.txt:125). Documentation disclaims official scores, hardware-peak claims, real-task generalization, INT8 inference speed, and multi-GPU/multi-node validation (docs/zh/docs/learning/validation.md:42; docs/zh/docs/learning/validation.md:44; docs/zh/docs/learning/validation.md:46). The multiple timing samples are not independent seeds or repeated full-suite trials.

## F. Evaluation Type Classification: PASS With Explicit Taxonomy Limits

The prescribed five-type taxonomy targets model-quality evaluations and does not fully describe numerical teaching checks. Forcing every check into real_gt or simulation_only would be misleading: these programs execute on actual CPU/GPU hardware and most references are mathematical or independent numerical calculations.

| Evaluation | Classification | Explanation |
| --- | --- | --- |
| Training initial CPU/GPU forward equivalence | synthetic_proxy, narrowly for backend equivalence | Reference comes from a CPU copy of the same initialized model; it is not task-quality ground truth (examples/ml/train.py:15) |
| CPU/MPI integer and memory checks, CUDA kernels, sparse solve, quantization, precision, witness | analytic_or_numerical_reference (outside supplied taxonomy) | Known inputs/formulas or independent CPU/FP64 calculations; no dataset labels and no trained-model-derived task target |
| Synthetic regression loss | synthetic_supervised_toy (outside supplied taxonomy) | Manufactured analytic labels, not labels from the evaluated model; describes no real-task generalization (examples/ml/train.py:12) |
| HPL/HPCG | official_generated_problem_validation (outside supplied taxonomy) | Real hardware runs of generated numerical problems with official residual/validity checks |
| Sanitizers, compilation, GPU query, browser checks, Nsight capture | execution_or_instrumentation_check (outside supplied taxonomy) | Software/hardware observation, not model-quality evaluation |

No dataset-provided real_gt evaluation, self_supervised_proxy task, human_eval, or simulated-hardware performance evaluation is present. The synthetic supervised toy is simulation-like only in its data generation; labeling the measured hardware execution simulation_only would obscure what was actually run. These taxonomy extensions are descriptive and do not upgrade the strength of evidence.

## Resolved Findings

The executor addressed findings during this review, after which the final files and refreshed artifacts were directly rechecked:

1. MPI ping-pong now stops the timer before validating contents (examples/mpi/pingpong.py:23). Final retained values are 3.231, 5.047 and 186.809 microseconds (RESULTS/checks/pingpong.txt:1); they are still single aggregate local measurements.
2. CUDA reduction and matrix comparison now reject nonfinite values, closing false-PASS paths from NaN comparisons (examples/cuda/labs.cu:84; examples/cuda/labs.cu:106).
3. The sparse solver now explicitly checks a finite relative residual at or below 1e-10 (examples/science/solve.py:14).
4. Run-start hashes, end-of-run equality, exact expected exit codes and archive-time hash comparison bind the final result to its reviewed sources (scripts/validate.py:25; scripts/validate.py:32; scripts/validate.py:62; scripts/archive-validation.py:17).
5. The browser result now retains a timestamp, script hash, viewports and check list, and the diagram assertion inspects a rendered SVG through CDP instead of accepting a tall source-text container (scripts/browser-check.py:27; scripts/browser-check.py:75).
6. Reproduction wording and the retained checker transcript distinguish the documented final invocation from a separate archived performance trial (docs/zh/docs/learning/validation.md:13; .aris/documented-invocation.md:28).

## Claim Impact and Remaining Limits

- Supported: the final recorded teaching suite passes its stated correctness checks on the recorded machine; official reference short runs validate their small numerical problems; the declared representative browser checks pass.
- Supported with existing qualifiers: timings describe these exact small inputs and timing boundaries; synthetic loss reduction demonstrates a working loop; quantization demonstrates representation error.
- Unsupported by this evidence, and not claimed in the reviewed final prose: broad algorithmic robustness, real-task quality/generalization, official HPL/HPCG/MLPerf scores, multi-node or multi-GPU scaling, INT8 inference speedup, or universal RTX 4090 performance.
- Not independently established by this review: repeatability across independent full runs, all standalone example files, all website pages, browser visual quality at every viewport, or signed execution provenance. Browser screenshots and the raw Nsight binary remain local build artifacts; the public archive retains browser metadata and profiler text statistics.
- The audit checked artifact consistency and source logic, not external attestation. HPL/HPCG and Nsight are separately captured earlier runs; they are not part of the final 40-case count.
- No mandatory integrity correction remains for the present bounded claims. Future performance-comparison or generalization claims require additional configurations/repeats and appropriate real-task references.

The JSON companion retains the 82 audited input hashes, deterministic verification details, and same-family/provisional metadata.

