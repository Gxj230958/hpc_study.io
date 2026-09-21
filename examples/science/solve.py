"""A small SPD system: dense solve, sparse CG and residual verification."""
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import cg

n = 127
a = diags([-np.ones(n-1), 2*np.ones(n), -np.ones(n-1)], [-1, 0, 1], format="csr")
expected = np.sin(np.pi * np.arange(1, n+1) / (n+1))
b = a @ expected
x, info = cg(a, b, rtol=1e-10, atol=0, maxiter=1000)
dense = np.linalg.solve(a.toarray(), b)
relative_residual = np.linalg.norm(a @ x - b) / np.linalg.norm(b)
assert info == 0
assert np.isfinite(relative_residual) and relative_residual <= 1e-10
np.testing.assert_allclose(x, dense, rtol=1e-7, atol=1e-8)
print(f"n={n} nnz={a.nnz} relative_residual={relative_residual:.3e} PASS")
