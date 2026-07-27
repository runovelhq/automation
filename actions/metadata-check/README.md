# Repository metadata check

This offline composite Action checks required community files, the documented
versioning model, obvious license metadata, and obsolete personal or image
namespaces. Set `require-changelog` only for release-bearing repositories.

```yaml
- uses: runovelhq/automation/actions/metadata-check@v1
  with:
    require-changelog: "true"
```

The Action requires no secrets or network access and emits GitHub error
annotations. Pin the Action to a full commit SHA when policy requires it.
