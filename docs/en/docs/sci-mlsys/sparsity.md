# Sparse Solving

**Prerequisites:** Matrix-vector multiplication. **Objective:** Interpret sparse storage and independent solution checks.

A sparse matrix stores selected entries instead of every zero. Compressed sparse row (CSR) stores values, column indices and row offsets. Savings depend on nonzero count, index width and storage overhead, not just the fraction of zeros.

Conjugate gradients applies to symmetric positive definite systems. The course constructs a tridiagonal matrix and manufactures a right-hand side from a known sine-vector solution. It checks solver status, a relative residual, a dense solve and the manufactured solution.

A residual measures equation satisfaction; the condition number controls how residual error can translate to solution error. Irregular sparsity can also reduce locality, so fewer FLOPs do not guarantee faster execution. Next, run [the residual experiment](intro.md#sparse-residual).
