# Security model

Validation and language CI have `contents: read` and receive no secrets. Public
pull requests therefore run without write authority. Container release requires
`packages: write`, `id-token: write`, and `attestations: write`; it rejects pull
request events and requires an exact trusted version tag.

Docker Hub credentials are optional and explicitly mapped. Secrets are never
inherited or passed as build arguments. Sensitive builds must use BuildKit secret
mounts in a future reviewed interface rather than adding secret-valued inputs.

External Actions are pinned to full commit SHAs. Release tags are protected,
images are addressed by digest, GitHub OIDC drives provenance and keyless Cosign
signing, and signatures are verified. Cache and artifact content is treated as
untrusted input; release jobs do not consume artifacts from unrelated workflows.

Prohibited patterns include `pull_request_target`, untrusted code with write
permissions, arbitrary-branch releases, hidden secret inheritance, caller values
inserted directly into shell source, mutable Action references, and credentials
in logs. Report findings through Private Vulnerability Reporting.
