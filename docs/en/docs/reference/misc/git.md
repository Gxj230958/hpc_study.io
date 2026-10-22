# Git for Experiments

**Prerequisites:** [Shell essentials](shell.md). **Objective:** Associate results with exact source.

Use git status to inspect local changes and git diff to review a patch. Commit a known-correct baseline before experimenting so a result can identify its source revision.

```bash
git status --short
git diff
git rev-parse HEAD
```

A commit hash alone does not describe uncommitted source changes. Retain source hashes alongside validation output, as the course runner does. Do not commit generated toolchains, credentials or multi-gigabyte traces.

Next, read [contribution requirements](../contribute/before-contributing.md).
