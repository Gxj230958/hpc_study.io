# Shell Essentials

**Prerequisites:** A Linux terminal. **Objective:** Run bounded commands and retain useful output.

The working directory determines relative paths. Run course commands from the repository root. source scripts/activate-study.sh changes the current shell's environment; executing it as a child script does not activate the parent shell.

```bash
pwd
which python
timeout 180s python examples/ml/train.py --device cpu
```

Exit code zero means the command's checks succeeded; nonzero requires inspection. The race demonstration deliberately exits 1 before repair. A timeout is a failed execution, not evidence of numerical success.

Redirect logs only to a task-specific path, and inspect them before removing generated files. Next, learn [Git](git.md) for tracking experiments.
