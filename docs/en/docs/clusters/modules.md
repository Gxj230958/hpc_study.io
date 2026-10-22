# Software Modules

**Prerequisites:** Shell environment variables. **Objective:** Capture a reproducible application toolchain.

Environment modules adjust variables such as PATH and library search paths. A module name is a site-specific convenience, not a portable version guarantee. Record module list, compiler version and actual executable paths.

Use one MPI implementation per process tree. A preloaded HPC-X/Open MPI library path can interfere with a native MPICH build; the teaching benchmark script explicitly prioritizes its matching system libraries. Bundled mpi4py labs instead use the activated uv launcher.

If your site provides modules, obtain its recommended compiler/MPI combination before building. Keep uv's Python environment and native toolchain assumptions explicit. Next, inspect [scheduler requests](scheduling.md).
