# Release process

Automation uses Semantic Versioning. Prepare the changelog, pass all self-tests,
review permissions and Action pins, merge through protected `main`, then create
an immutable exact tag and GitHub Release such as `v1.0.0`. Move the compatible
major pointer such as `v1` to the same reviewed commit.

Major tags promise backward compatibility for documented workflow inputs,
outputs, permissions, and stable behavior. Breaking changes require `v2`.
Rollback consumers to a previous exact tag or commit SHA; do not move an exact
version tag. If a release is unsafe, publish a corrected patch and document the
incident rather than rewriting history.

Container callers release only from matching `vMAJOR.MINOR.PATCH` tags. Stable
versions receive exact, major/minor, major, latest, and short-SHA tags;
pre-releases receive only exact and short-SHA tags.
