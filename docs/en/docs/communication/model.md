# Message Models

**Prerequisites:** [Communication](intro.md). **Objective:** Distinguish blocking completion from nonblocking initiation.

A blocking send returns when its input buffer may be reused according to that operation's semantics; it does not always mean the receiver has completed processing. A receive returns when its output buffer contains the matched message.

Nonblocking calls return a request. Wait or Test establishes completion; do not modify a send buffer or read an unfinished receive buffer. Overlap only helps when useful independent work exists and the implementation makes progress.

A receive-first exchange or Sendrecv avoids relying on eager buffering. Tags distinguish logical exchanges, but they are not substitutes for matching datatypes and lengths. Next, reason about [deadlock](deadlock.md).
