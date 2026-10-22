# URL Migration

Every original Markdown page has an entry in the [machine-readable mapping](/hpc_study.io/downloads/url-map.json). The build checker compares the full original file set and source hashes against that inventory.

<!-- URL_MAP -->

Retained lesson families keep their published URLs. platform moves to clusters, hpc-intro moves to foundations, alternative GPU programming models move beneath reference/programming-models, and competition, power-management, misc and contribute move beneath reference. Legacy hardware/gpu and performance-analysis/nsys redirect directly to gpu/arch and gpu/nsys.

Original heading IDs are retained as compatibility anchors on the destination lesson. If the English organization changes the surrounding section, the anchor leads to the destination's source/attribution area; consult the linked archived original for the original section context. This is a documented semantic limitation, not an untranslated English lesson.

The static/vendor/README.md inventory was not an instructional page in the original main navigation. Its English destination is the licensing page; the full original is published in the archive. Markdown source-style URLs ending in .md were source paths, not published pretty URLs. Redirects preserve the published directory URLs.

Next, consult [the frozen archive](/hpc_study.io/archive/zh/) or [validation](../learning/validation.md).
