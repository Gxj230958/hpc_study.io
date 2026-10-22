# Caches and False Sharing

**Prerequisites:** [Memory](../hardware/memory.md). **Objective:** Explain reuse, misses and coherence traffic.

Temporal locality reuses a recently accessed value. Spatial locality uses nearby values that arrive in the same cache line. A cache miss can require data from another cache or DRAM, and an irregular access can also incur address-translation misses.

False sharing occurs when threads write different values on the same coherent cache line. Their data are logically independent, but ownership of the line moves between cores. Thread-local accumulators followed by a reduction can reduce this traffic.

Blocking processes small tiles so reused data remains near the execution units. A tile must fit the relevant cache with room for other live data; merely fitting an entire input in DRAM says nothing about cache reuse. Next, interpret [stride measurements](../hardware/hardware-intro.md#cache-stride).
