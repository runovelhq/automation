# Contributing

Open an issue before changing a stable workflow contract. Use a focused branch
and pull request, add tests and documentation, and run:

```console
python -m unittest discover -s tests -v
python scripts/verify-action-pins.py .github examples
```

Every external Action must use a full commit SHA. Keep permissions explicit,
avoid secret inheritance, and document compatibility impact. See
[`docs/adding-a-stack.md`](docs/adding-a-stack.md) for stack changes.
