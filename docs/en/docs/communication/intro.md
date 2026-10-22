# Communication

**Prerequisites:** Processes and ranks. **Objective:** Match a communication pattern to its correctness obligations.

Point-to-point communication transfers data between a specified sender and receiver. Collectives involve a communicator, for example broadcasting a value or summing values across ranks. A collective is not automatically a full application barrier.

Define message type, size, source, destination and tag explicitly. The receiver must provide a compatible buffer. The application must guarantee that no rank exits early while its peers wait for a message or collective.

Start with local correctness, then vary message size and placement. Local shared-memory transport and remote TCP transport are different experiments. Next, examine [message models](model.md).
