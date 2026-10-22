# Threads

**Prerequisites:** [Processes and threads](intro.md). **Objective:** Recognize shared-state hazards.

Threads can read a shared immutable array safely. Concurrent writes need exclusive ownership or a synchronization protocol. A read-modify-write such as total += value is not generally one indivisible action.

A mutex allows only one thread into a critical section at a time. A barrier waits until all participating threads arrive. Combining them carelessly can deadlock: never wait at a barrier while holding the lock another participant needs.

Python's interpreter lock does not make a multi-step application protocol atomic. Native numerical libraries may also release it. Run the bounded [race repair](../parallel-programming/parallel-programming-intro.md#race-repair), then prefer reductions for regular numerical loops.
