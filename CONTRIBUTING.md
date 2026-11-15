# Contribution guide

Thanks for your contribute.

Many API features has not supported by python-backlog yet. Any contribution is welcome.

It would be great if you could create an issue or pull request. However, since I may not be aware of your contribution, it may help me to respond to it more reliably if you give me a Mention or let me know via twitter ([@hassaku63](https://twitter.com/hassaku_63)).

## Development

```bash
pip install -e '.[dev]'
flake8
python -m unittest
```

## Releasing

Releases are automated by `.github/workflows/pypi-release.yml`:

1. Open a pull request that bumps the number in the `VERSION` file (together with the changes, or on its own).
2. Merge it into `master`. If no `v<VERSION>` tag exists yet, the workflow builds the package, publishes it to PyPI and creates the `v<VERSION>` tag and a GitHub Release on that commit.

Changes that do not affect the package (CI, docs, etc.) do not need a version bump; they are released with the next version.

To release an older commit on `master`, run the "Release" workflow manually (workflow_dispatch) with that commit as `ref`.
