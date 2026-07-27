# Adding a stack

Add a stack only for an identified consumer. Define its identifier, runtime
version, working directory, cache inputs, explicit install/lint/test commands,
optional coverage and artifacts, permissions, public-PR behavior, and limits.

Implementation requires contract validation, pinned Actions, deterministic cache
keys, tests for the default and opt-in paths, an example, and security review.
Never execute project scripts by default for a stack where static checking is
possible. Do not introduce secrets into pull-request CI.

If `reusable-language-ci.yml` can no longer be understood in one review, propose
a major-version split into stack-specific workflows. Preserve the common concepts
instead of building a dynamic universal CI engine.
