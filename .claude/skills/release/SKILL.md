---
name: release
description: How to prepare a release of python-backlog. Use it whenever a pull request bumps VERSION (a release pull request on its own, or a feature pull request that also releases), to collect every pull request merged since the previous release and write the CHANGELOG.md section for the new version, so that nothing is left out.
---

# Preparing a release

A release happens when a pull request that changes `VERSION` is merged into `master` (see "Releasing" in CONTRIBUTING.md). Pull requests may be merged without a release and accumulate until one. The pull request that bumps `VERSION` therefore writes the changelog for **all** pull requests merged since the previous release, not only for itself. Collect the material yourself; do not rely on `[Unreleased]` being complete.

## 1. Choose the version

- Look at what was merged since the latest release tag (step 2). New features: bump the minor version. Fixes only: bump the patch version. Before 1.0, breaking changes also bump the minor version and must be called out (step 4).
- Write the new version to `VERSION` (`X.Y.Z`, higher than the current one).

## 2. List the merged pull requests

```bash
git fetch --tags origin master   # in a shallow clone, fetch enough history to reach the latest tag
python scripts/changelog_check.py pulls
```

The command prints every pull request merged into `master` since the latest release tag, newest first, with the files it changed. It reads merge commits ("Merge pull request #N") and squash commits ("... (#N)"). Pull requests that only changed `VERSION` and `CHANGELOG.md` are marked as release only and need no entry.

## 3. Read each pull request

For every listed pull request, read its description (for example `gh pr view <N>`, the GitHub MCP tools, or `https://github.com/hassaku63/pbl/pull/<N>`). If neither is available, read the merge commit and its commits: `git log --format=%B <merge>^1..<merge>`. Decide, from the point of view of someone who uses the package:

- **User-visible**: new or changed methods or parameters, behavior changes, fixes, deprecations, removed features, dependency or Python version changes, security fixes.
- **Internal**: CI, tests, end-to-end tests, tooling, documentation for contributors. Files under `backlog/` usually mean user-visible; `.github/`, `tests/`, `scripts/` and `docs/` usually mean internal. Read the description when unsure.

Also include the changes of the pull request you are writing, if it does more than the release (it is not merged yet, so step 2 cannot list it).

## 4. Write the changelog

In `CHANGELOG.md`:

1. Add `## [<VERSION>] - <YYYY-MM-DD>` directly below `## [Unreleased]`. Use today's date in UTC, the expected PyPI publication date. Move anything that was under `[Unreleased]` into it.
2. Group the user-visible changes under `### Added`, `### Changed`, `### Deprecated`, `### Removed`, `### Fixed` and `### Security`, in this order and only the ones that apply. Write for package users: what they can do now or what changes for them, with method names in backticks. End every entry with a link to its pull request: `([#N](https://github.com/hassaku63/pbl/pull/N))`. Several pull requests may share one entry.
3. **Breaking changes**: put them first, in a `### ⚠ Breaking changes` section that says what breaks, who is affected and how to migrate (a table helps when there are several cases), and add the version to the table of breaking changes at the top of the file. Prefer a deprecation to a breaking change.
4. **Internal pull requests**: add their links to the "## Internal" section at the end of the file (extend its sentence, or add a sentence for the new version).
5. Update the links at the bottom: `[Unreleased]: https://github.com/hassaku63/pbl/compare/v<VERSION>...HEAD`, and add `[<VERSION>]: https://github.com/hassaku63/pbl/compare/v<previous>...v<VERSION>` above the previous version's link.

## 5. Check

```bash
python scripts/changelog_check.py
```

It fails when the new section is missing, empty, out of order or without links, or when a pull request merged since the previous release is linked neither in the new section nor under Internal. The "Changelog" CI job runs the same check on the pull request, so fix every problem it reports before asking for a merge.

## 6. Open the pull request

Title it "Bump VERSION to X.Y.Z" (or mention the release in the title of a feature pull request), and summarize the release in the description with links to the included pull requests. After it is merged, the release workflow publishes to PyPI once a maintainer approves the `pypi` environment, then creates the tag and GitHub Release.
