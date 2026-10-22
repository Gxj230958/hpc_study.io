# Processes and Threads

**Prerequisites:** Basic functions and arrays. **Objective:** Choose a worker model and assign ownership of data.

A process has an address space, file descriptors and execution state. Threads share an address space but have separate instruction pointers and stacks. A context switch changes the currently executing worker; concurrency does not guarantee simultaneous execution.

Use threads when sharing data is useful and synchronization is explicit. Use processes when isolation or distributed execution is needed. MPI and torchrun launch processes; each process can create additional numerical-library threads, so total runnable workers can multiply unexpectedly.

For rank r of p workers, the half-open interval [nr/p, n(r+1)/p) with integer division covers uneven n exactly when combined over all ranks. Half-open means the lower index is included and the upper index is excluded. Next, study [process launch](process.md) and [thread safety](thread.md).
