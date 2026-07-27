# Architecture

The repository deliberately has three reusable workflow families and two
offline composite Actions:

1. repository validation checks repository-wide policy and syntax;
2. language CI offers one small contract for Python and Shell;
3. container release owns trusted build, publication, SBOM, scan, provenance,
   signing, and optional mirroring;
4. metadata-check and version-check keep reusable validation logic testable.

Reusable workflows define jobs, permissions, runners, and trust boundaries.
Composite Actions package small step-level logic but cannot define jobs or
permissions. This distinction keeps release authority visible at workflow level.

New stacks extend the documented contract only when there is a real consumer.
If conditional branches make language CI hard to understand, the next major
version may split stacks into separate workflows while retaining shared concepts.
