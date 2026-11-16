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
- The list of endpoints, `docs/api_endpoints.json`, is maintained by reading the official API reference: each entry has the page URL and the date it was last accessed. Nothing downloads or parses the documentation site automatically. Endpoints that Backlog removed are listed under `removed`; the CI check fails if a method that is not deprecated still calls one.

## End-to-end tests

`tests/e2e/` contains tests that call a real Backlog space. They are skipped unless `BACKLOG_E2E_SPACE` and `BACKLOG_E2E_API_KEY` are set, so a normal `python -m unittest` run stays offline. See `tests/e2e/__init__.py` for the variables and **[tests/e2e/README.md](tests/e2e/README.md) for the guidelines** (minimal assertions, no response values in messages or logs, cleanup, tiers). The `e2e-test` skill in `.claude/skills/` points AI agents to the same guidelines.

```bash
BACKLOG_E2E_SPACE=... BACKLOG_E2E_API_KEY=... BACKLOG_E2E_PROJECT_KEY=... python -m unittest discover -v -s tests/e2e -t .
```

There are three tiers:

| Tier | What | How to run |
|---|---|---|
| R | read-only | always, when the space is configured |
| W | create, update and delete in the test project, then clean up | `BACKLOG_E2E_WRITE=1` |
| A | space administrator operations, real personal data, external side effects | locally only: `python scripts/e2e_local.py` |

- Requests are throttled (`BACKLOG_E2E_INTERVAL`, default 1 second) to stay well below the rate limits of the free plan.
- Every resource a test creates is named `pbl-e2e-<run id>-...`. `tests/e2e/test_00_cleanup.py` deletes leftovers of earlier runs.
- Tier A never runs in CI: `tests/e2e/support.py` refuses to load with `BACKLOG_E2E_ADMIN=1` in CI, and `scripts/e2e_local.py` refuses to start there. The script asks for confirmation and writes `e2e-report.md` (results and endpoints only, no response data) to share in an issue or pull request.

### Setting up the space and the GitHub environment

`.github/workflows/e2e.yml` runs tiers R and W weekly (R only) and on demand (Actions → E2E → Run workflow, with the `write` input for tier W). A failed scheduled run opens an issue labeled `e2e-failure` that contains only test names. Until the secrets below are configured, scheduled runs are skipped with a notice (no failure, no issue); manual runs fail.

1. **Backlog space.** Use a space where no one else's data can appear in the tests, e.g. your own free-plan space, and create a project dedicated to the tests (Wiki enabled). The tests read the whole space (users, projects, activities) but only write to that project.
2. **API key.** Choose one of these:
   - **Your own API key** (simplest). The workflow then holds a key that can do everything you can, including space administration, so keep the environment restricted as in step 3.
   - **The key of a dedicated user** (least privilege). Add a "Normal user" to the space, for example with a `+e2e` alias of your address. Add it to the test project as a project administrator, and create the key while signed in as that user. A leaked key then reaches only what that user can see.

   In both cases the user needs to be an **administrator of the test project**: tier W creates documents, categories, versions and statuses. Space administrator rights are not needed in CI.
3. **GitHub environment.** In Settings → Environments, create `backlog-e2e`:
   - Deployment branches: **Selected branches → `master`**, so only workflows on master can read the secrets.
   - Do not add required reviewers; they would block the scheduled runs.
   - Secrets: `BACKLOG_E2E_SPACE`, `BACKLOG_E2E_API_KEY` and `BACKLOG_E2E_PROJECT_KEY`. The space is a secret too, so it is masked in the logs.
   - Variable (optional): `BACKLOG_E2E_DOMAIN`, one of `backlog.jp` (default), `backlog.com` and `backlogtool.com`.
4. **Masking.** Before the tests, the workflow runs `python -m tests.e2e.mask`. It registers the name, mail address and other personal values of the API key's user as masked values, so they appear as `***` if they ever reach a log. Tests must still follow the guidelines: masking is a second line of defense, not the first.

To run tier A, use your own administrator key on your machine. `BACKLOG_E2E_USER_EMAIL` must be an address you own: Backlog may send it a registration mail.

```bash
BACKLOG_E2E_SPACE=... BACKLOG_E2E_API_KEY=... BACKLOG_E2E_USER_EMAIL=you+e2e@example.com python scripts/e2e_local.py
```

## Releasing

Releases are automated by `.github/workflows/pypi-release.yml`. Merging into `master` does not release anything by itself; only a change of the `VERSION` file does.

- Pull requests that do not change `VERSION` are merged into `master` and accumulate there until the next release. When a pull request changes something package users notice (new or changed methods, fixes, deprecations, dependencies), add an entry to the `[Unreleased]` section of [CHANGELOG.md](CHANGELOG.md) in [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format, with a link to the pull request. Changes to CI, tests or documentation only are not listed. A breaking change goes into a `### ⚠ Breaking changes` section at the top of the version, with what breaks and how to migrate, and into the table of breaking changes at the top of the file.
- **To release**, bump `VERSION` in a pull request, either on its own or together with the changes. In the same pull request, move the entries under `[Unreleased]` in CHANGELOG.md to a new `## [<VERSION>] - <YYYY-MM-DD>` section (the expected publication date, UTC), and update the compare links at the bottom. The "Changelog" CI job (`python scripts/changelog_check.py`) fails until CHANGELOG.md has a dated section with entries for the new `VERSION` and matching links. When it is merged, the workflow builds the package, publishes it to PyPI and creates the `v<VERSION>` tag and a GitHub Release on that commit.
- The "Release check" workflow comments on every pull request whether merging it releases a new version, and fails if the new `VERSION` cannot be released (not higher than the current version, already tagged, or not in the `X.Y.Z` format).

To release an older commit on `master`, run the "Release" workflow manually (workflow_dispatch) with that commit as `ref`.
