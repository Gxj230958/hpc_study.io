# Validation Record: 2026-10-22

The English course was checked on Ubuntu 24.04.2 with a 10-CPU-equivalent quota, a 100 GiB memory limit and one visible RTX 4090. Driver 570.124.06, CUDA toolkit 12.4.131, Python 3.10.20 and PyTorch 2.6.0+cu124 were used. Labs target a conventional 24 GB GPU; this host's unusual memory report is not a requirement.

The [dated machine-readable report](/hpc_study.io/downloads/validation.json) contains exact commands, raw outputs, versions, source SHA256 hashes, changed files and remaining TODOs. Source hashes identify the tested files even before the final commit. September audit artifacts and the [Chinese validation page](/hpc_study.io/archive/zh/learning/validation/) remain historical.

## Executed Checks

| Check | Command or procedure | Result |
| --- | --- | --- |
| Expanded CPU/CUDA suite | python scripts/validate.py --gpu | 40 checks passed |
| Full local lab manifest | python scripts/run-labs.py --gpu --reference | 66 commands passed |
| Isolated CPU extra | env -u LD_LIBRARY_PATH /tmp/hpc-study-cpu/bin/python scripts/run-labs.py --output build/labs-cpu | 53 commands passed with PyTorch 2.6.0+cpu |
| Curriculum contract | python scripts/check-labs.py --final | Eight modules, 24 labs, all sources and closed answers checked |
| Checker failure cases | python -m unittest discover -s tests | Six tests passed |
| Frozen sources and mapping | python scripts/course.py --check | All 71 original Markdown sources and hashes checked |
| English and archive builds | python scripts/build-site.py | Both strict builds passed; 179 HTML pages; zero internal link, asset, anchor or redirect failures |
| Browser behavior | python scripts/browser-check.py | Passed at 1440x1000 and 390x844 |
| Dependency separation | uv sync --locked --only-group docs in an isolated environment | No PyTorch installed; strict builds passed |
| Extra conflicts | uv sync --locked --extra cpu --extra gpu --dry-run | Correctly rejected incompatible extras |

Browser checks cover 14 representative pages at each size, English and Chinese archive search, all 24 answers closed by default and able to open/close, code copy controls, diagrams, formulas, images, downloads, mobile navigation, themes and representative legacy redirects. Screenshots are retained in build/browser-english and CI artifacts.

The manifest includes repeated stride measurements, five samples per thread count, checked MPI payloads and scaling, GPU dispatch, boundary shapes, three Compute Sanitizer tools, transfer/kernel profiling, sparse residuals, quantization, training/precision and collective/DDP references. HPL/HPCG source hashes and numerical reports are retained; these deliberately short teaching runs are not official submissions.

## External References

The separate audit scanned 110 external URLs across the generated English/archive site: 101 responded, five returned HTTP 403, and four timed out. An inaccessible request does not prove a page is gone. The [audit download](/hpc_study.io/downloads/external-links.json) records each URL and affected pages; external fragment anchors and remote content correctness are not verified.

The HTTP-403 responses came from two GNU/GCC pages and three Intel pages. The timeouts affected ASC, STREAM, GNU coreutils and a YouTube playlist. Archived text is frozen, so these limitations are reported rather than silently changing its sources.

## Resolved During Validation

Repeating Nsight Systems statistics initially found a stale SQLite export. The documented command now uses --force-export=true, and the repeated run passed. Chromium download retries and missing Linux libraries were resolved before browser checks.

CI's wider system-font metrics exposed a mobile language-menu overflow that did
not appear under the initial local fonts. A shared presentation fix aligns the
menu within the viewport without modifying Chinese sources. Browser checks now
also open both language menus under wider monospace metrics.

The isolated CPU wheel initially loaded an unrelated Python 3.12 PyTorch shared library through the container's inherited LD_LIBRARY_PATH. CPU-extra validation used per-command isolation with env -u LD_LIBRARY_PATH. The main GPU environment remained usable. See [setup troubleshooting](setup.md).

## Not Executed and Remaining Work

One-process NCCL passed on the local GPU. Two-process Gloo AllReduce and DDP passed, including parameter comparison with independent global-batch SGD. The primary two-GPU NCCL and two-node TCP configurations remain **not executed**. Their fallbacks do not validate GPU peer access, Ethernet performance or remote software compatibility.

No A100, H100 or H200 experiment was executed. Datacenter specifications are sourced; roofline/capacity values are calculated. The optional CPU calculator checked arithmetic only. No AWS commands ran, and no cloud resources were provisioned.

Complete the unresolved node/GPU counts, network speed/topology, remote versions, SSH, scheduler and ports in the [hardware profile](/hpc_study.io/downloads/source/course/hardware-profile.json) before remote execution. Recheck the nine inaccessible/unverified references from another network. Validate target-specific porting/profiling assumptions only after obtaining an allocation.

Compatibility anchors preserve old IDs but can lead to the source-attribution area when English sections have been reorganized. Use the archived original for the old section context. See the [URL map](../reference/url-map.md) and [experiment inventory](labs.md).
