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

Releases are automated by `.github/workflows/pypi-release.yml`. Merging into `master` does not release anything by itself; only a change of the `VERSION` file does.

- **Do not change `VERSION` in feature or fix pull requests.** Changes are merged into `master` without a version bump and accumulate there until the next release. The "Release check" workflow fails if a pull request changes `VERSION` together with other files.
- **To release**, open a dedicated pull request that changes only `VERSION`. When it is merged, the workflow builds the package, publishes it to PyPI and creates the `v<VERSION>` tag and a GitHub Release on that commit.
- The "Release check" workflow comments on every pull request whether merging it releases a new version.

To release an older commit on `master`, run the "Release" workflow manually (workflow_dispatch) with that commit as `ref`.
