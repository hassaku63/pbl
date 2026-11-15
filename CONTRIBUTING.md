# Contribution guide

Thanks for your contribute.

Many API features has not supported by python-backlog yet. Any contribution is welcome.

It would be great if you could create an issue or pull request. However, since I may not be aware of your contribution, it may help me to respond to it more reliably if you give me a Mention or let me know via twitter ([@hassaku63](https://twitter.com/hassaku_63)).

## Development

```bash
pip install -e '.[dev]'
ruff check
python -m unittest
```

## Adding or changing API methods

Follow `.claude/skills/api-change/SKILL.md`. In short:

- `docs/API_COVERAGE.md` is generated. After changing `backlog/*.py`, run `python scripts/api_coverage.py generate` and commit the result; the "API coverage doc" CI job checks it.
- Decide whether README.md needs an update, and say so in the pull request.
- `python scripts/api_coverage.py refresh` re-downloads the endpoint list from the official API reference.

## End-to-end tests

`tests/e2e/` contains happy-path tests that call a real Backlog space. They are skipped unless `BACKLOG_E2E_SPACE` and `BACKLOG_E2E_API_KEY` are set, so a normal `python -m unittest` run stays offline. See `tests/e2e/__init__.py` for the variables.

```bash
BACKLOG_E2E_SPACE=... BACKLOG_E2E_API_KEY=... BACKLOG_E2E_PROJECT_KEY=... python -m unittest discover -v -s tests/e2e -t .
```

- Requests are throttled (`BACKLOG_E2E_INTERVAL`, default 1 second) to stay well below the rate limits of the free plan.
- Tests that create data run only with `BACKLOG_E2E_WRITE=1`, use the test project only, and delete what they create.
- On GitHub, `.github/workflows/e2e.yml` runs them weekly and on demand (Actions → E2E → Run workflow) in the `backlog-e2e` environment. A failed scheduled run opens an issue labeled `e2e-failure`.

## Releasing

Releases are automated by `.github/workflows/pypi-release.yml`. Merging into `master` does not release anything by itself; only a change of the `VERSION` file does.

- Pull requests that do not change `VERSION` are merged into `master` and accumulate there until the next release.
- **To release**, bump `VERSION` in a pull request, either on its own or together with the changes. When it is merged, the workflow builds the package, publishes it to PyPI and creates the `v<VERSION>` tag and a GitHub Release on that commit.
- The "Release check" workflow comments on every pull request whether merging it releases a new version, and fails if the new `VERSION` cannot be released (not higher than the current version, already tagged, or not in the `X.Y.Z` format).

To release an older commit on `master`, run the "Release" workflow manually (workflow_dispatch) with that commit as `ref`.
