# Runovel Automation

Small, versioned reusable workflows and composite Actions for Runovel
repositories. The stable v1 surface contains repository validation, Python and
Shell CI, and trusted container releases. Other stacks remain experimental
until implemented and documented.

## Workflows

| Workflow | Purpose | Secrets |
| --- | --- | --- |
| `reusable-repository-validation.yml` | Repository syntax, policy, metadata, Action pins, actionlint, and ShellCheck | None |
| `reusable-language-ci.yml` | Python or Shell validation through a small command contract | None |
| `reusable-container-release.yml` | GHCR release, optional Docker Hub mirror, SBOM, scan, provenance, and signing | Docker Hub credentials only when mirroring |

Copy the minimal callers from [`examples/`](examples/). They use the supported
major compatibility reference `@v1`; security-sensitive consumers may replace
it with a full 40-character commit SHA for immutable pinning.

## Shared Actions

- [`metadata-check`](actions/metadata-check/README.md) validates community
  files, namespaces, license metadata, and versioning documentation offline.
- [`version-check`](actions/version-check/README.md) validates and normalizes
  strict semantic release versions offline.

## Versioning and support

This repository follows Semantic Versioning. Exact tags such as `v1.0.0` are
immutable releases; `v1` is the maintained compatibility pointer for the v1
contract. Breaking workflow inputs or behavior require a new major version.
Stable features are supported through issues and the Runovel security process;
future stack proposals are experimental until released.

See [architecture](docs/architecture.md), [security](docs/security.md),
[release](docs/release.md), and [adding a stack](docs/adding-a-stack.md).
