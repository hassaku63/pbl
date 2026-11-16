# Changelog

All notable changes to python-backlog are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (before 1.0, a minor version may contain breaking changes).
Dates are the PyPI publication dates (UTC). Only versions published to PyPI are listed: changes of an unpublished version are included in the next published one.

Releases before 0.7.4 are listed on [GitHub Releases](https://github.com/hassaku63/pbl/releases).

Versions with breaking changes start with a **⚠ Breaking changes** section that explains how to migrate:

| Version | Breaking change |
|---|---|
| [0.9.0](#090---2026-11-15) | The `requests` dependency was removed: `invoke_method()` returns a different response type, accepts fewer keyword arguments and raises different network errors |
| [0.8.0](#080---2026-11-15) | Python 3.8 and 3.9 are no longer supported |

## [Unreleased]

## [0.19.0] - 2026-11-16

### Added

- Structured exceptions for API errors. `BacklogAPIError` (a `BacklogError`) has `status_code`, `response`, `errors` (the `errors` array of the error response), `code` (a `BacklogErrorCode`) and `error_message`. Subclasses: `BacklogBadRequestError` (400), `BacklogUnauthorizedError` (401), `BacklogForbiddenError` (403), `BacklogNotFoundError` (404), `BacklogRateLimitError` (429) and `BacklogServerError` (5xx). The classes live in `backlog.errors` and are importable from `backlog.base` as before; the message format is unchanged ([#97](https://github.com/hassaku63/pbl/pull/97)).
- Pagination: `backlog.pagination.iterate_by_offset()` and `iterate_by_id()`, and `iter...()` methods on issues, issue comments, documents, watchings, pull requests, activities, notifications, received stars and wiki history ([#98](https://github.com/hassaku63/pbl/pull/98)).
- Missing parameters: `grandchildIssueEnabled` and `useDocument` for `Project.create()` / `update()`; `templateSummary` and `templateDescription` for `Project.add_issue_type()` / `update_issue_type()`; `attachmentId` for `Git.add_pull_request_comment()`. `Project.list(archived=None)` lists all projects ([#99](https://github.com/hassaku63/pbl/pull/99)).

### Changed

- `Project.create()` and `Project.update()` send booleans as `true` / `false` (the documented form) instead of `True` / `False` ([#99](https://github.com/hassaku63/pbl/pull/99)).
- `Project.update_issue_type()`: `name` and `color` are optional ([#99](https://github.com/hassaku63/pbl/pull/99)).
- Docstrings link to the English API reference and describe every parameter and return value. The type names `AddCustomFieldResponse` and `DeleteCustomFieldResponse` replace the misspelled `...CustomFiledResponse`, which remain as aliases ([#100](https://github.com/hassaku63/pbl/pull/100)).

## [0.18.0] - 2026-11-16

### Deprecated

- **`User.add()`, `User.update()` and `User.delete()` emit a `DeprecationWarning`.** Their endpoints were removed from the official API reference and are reported not to work in spaces on the new plans, where users are managed in the Backlog web UI. They keep working and will be removed in a future release. To remove a user from a project, use `Project.delete_user()` ([#95](https://github.com/hassaku63/pbl/pull/95)).

## [0.17.0] - 2026-11-16

### Added

- Webhooks: `BacklogAPI.webhook` with `list()`, `add()`, `get()`, `update()` and `delete()` ([#91](https://github.com/hassaku63/pbl/pull/91)).
- Custom fields: `CustomField.update()`, `add_list_item()`, `update_list_item()` and `delete_list_item()` ([#92](https://github.com/hassaku63/pbl/pull/92)).
- Project members: `Project.add_user()`, `delete_user()`, `add_team()`, `delete_team()`, and the team list `Team.list()` ([#93](https://github.com/hassaku63/pbl/pull/93)).

## [0.16.0] - 2026-11-16

### Added

- Shared files: `Project.list_shared_files()` and `get_shared_file()` ([#86](https://github.com/hassaku63/pbl/pull/86)).
- Space information: `BacklogAPI.get_space()`, `get_space_licence()`, `get_space_notification()` and `get_space_image()` ([#87](https://github.com/hassaku63/pbl/pull/87)).
- Icons and project members: `Project.get_image()`, `User.get_icon()`, `Team.get_icon()` (new `BacklogAPI.team`), `Project.list_administrators()` and `Project.list_teams()` ([#88](https://github.com/hassaku63/pbl/pull/88)).

## [0.15.0] - 2026-11-16

### Added

- Stars: `BacklogAPI.star` with `add()`, `delete()`, `list_received()` and `count_received()` ([#83](https://github.com/hassaku63/pbl/pull/83)).
- Recently viewed items: `User.list_recently_viewed_issues()`, `add_recently_viewed_issue()`, `list_recently_viewed_projects()`, `list_recently_viewed_wikis()` and `add_recently_viewed_wiki()` ([#84](https://github.com/hassaku63/pbl/pull/84)).

## [0.14.0] - 2026-11-16

### Added

- Recent updates: `BacklogAPI.activity` with `list()`, `list_project()`, `list_user()` and `get()` ([#76](https://github.com/hassaku63/pbl/pull/76)).
- Project statuses and versions/milestones: `Project.add_status()`, `update_status()`, `delete_status()`, `update_status_order()`, `add_version()`, `update_version()` and `delete_version()` ([#77](https://github.com/hassaku63/pbl/pull/77)).
- The remaining wiki endpoints: `Wiki.count()`, `list_tags()`, `list_history()`, `list_stars()`, `list_shared_files()`, `link_shared_files()`, `unlink_shared_file()`, and the `keyword` parameter of `Wiki.list()` ([#78](https://github.com/hassaku63/pbl/pull/78)).

### Changed

- The package metadata uses the GitHub no-reply address as the author email ([#74](https://github.com/hassaku63/pbl/pull/74)).

## [0.13.1] - 2026-11-16

### Fixed

- `Wiki.add_attachment()` sends `attachmentId[]` as the API expects, so files are actually attached. It accepts an int or a list ([#73](https://github.com/hassaku63/pbl/pull/73)).

## [0.13.0] - 2026-11-16

### Added

- Documents: `BacklogAPI.document` with `list()`, `count()`, `tree()`, `get()`, `add()`, `delete()`, `get_attachment()`, `list_comments()`, `add_tags()` and `remove_tags()` ([#71](https://github.com/hassaku63/pbl/pull/71)).

## [0.12.0] - 2026-11-15

### Added

- Git and pull requests: `Git.get_git_repository()`, `get_pull_request()`, `update_pull_request()`, `count_pull_requests()`, pull request comments (`list_...`, `count_...`, `update_pull_request_comment()`) and attachments (`list_...`, `get_...`, `delete_pull_request_attachment()`) ([#66](https://github.com/hassaku63/pbl/pull/66)).
- `User.get_myself()` and watchings: `BacklogAPI.watching` with `list()`, `count()`, `get()`, `add()`, `update()`, `delete()` and `mark_as_read()` ([#67](https://github.com/hassaku63/pbl/pull/67)).
- Issue participants and related issues: `Issue.list_participants()`, `list_related_issues()`, `add_related_issue()` and `remove_related_issue()` ([#68](https://github.com/hassaku63/pbl/pull/68)).
- Notifications: `BacklogAPI.notification` with `list()`, `count()`, `reset_unread_count()` and `mark_as_read()` ([#69](https://github.com/hassaku63/pbl/pull/69)).

## [0.11.0] - 2026-11-15

### Added

- IDs needed to add or update issues: `BacklogAPI.priority.list()`, `BacklogAPI.resolution.list()`, `Project.list_statuses()` and `Project.list_versions()` ([#65](https://github.com/hassaku63/pbl/pull/65)).

## [0.10.0] - 2026-11-15

### Added

- Spaces on backlog.com and backlogtool.com: `BacklogAPI(..., domain="backlog.com")` (default `backlog.jp`). Only these domains are accepted ([#60](https://github.com/hassaku63/pbl/pull/60)).
- OAuth 2.0: `BacklogAPI(..., access_token=...)` sends the token as `Authorization: Bearer`; `backlog.oauth` provides `authorization_url()`, `request_access_token()` and `refresh_access_token()`, and `set_access_token()` swaps the token ([#60](https://github.com/hassaku63/pbl/pull/60)).
- Rate limits: 429 responses raise `BacklogRateLimitError` with the `X-RateLimit-*` values; `rate_limit_retries` and `rate_limit_max_wait` retry after the limit resets; `get_rate_limit()` returns the current limits ([#60](https://github.com/hassaku63/pbl/pull/60)).
- Issue comments, attachments and shared files: the `Issue` methods that raised `NotImplementedError` are implemented (`get_comments()`, `count_comments()`, `get_comment()`, `update_comment()`, comment notifications, `list_issue_attachments()`, `get_issue_attachment()`, `delete_issue_attachment()`, `list_issue_shared_files()`, `link_issue_shared_files()`, `unlink_issue_shared_file()`), and `Issue.delete_comment()` is added ([#61](https://github.com/hassaku63/pbl/pull/61)).

### Fixed

- `Git.add_pull_request_comment()` no longer uses a mutable default argument for `notifiedUserIds` (it was never modified, so behavior is unchanged) ([#59](https://github.com/hassaku63/pbl/pull/59)).

## [0.9.0] - 2026-11-15

### ⚠ Breaking changes

python-backlog no longer depends on `requests`: HTTP requests use a small client built on the standard library (`urllib`), and the package has no runtime dependencies ([#58](https://github.com/hassaku63/pbl/pull/58)). Code that only calls the resource methods (`api.issue.list()`, ...) and catches `BacklogError` needs no change. Check your code if it does any of the following (see also "Upgrading to 0.9" in the README):

| If your code ... | then in 0.9.0 ... | Migration |
|---|---|---|
| uses the return value of `invoke_method()` as a `requests.Response` | it returns `backlog._http.Response` | Use `status_code`, `ok`, `headers`, `content`, `text` and `json()`; other `requests.Response` attributes are not available |
| passes requests options such as `verify`, `proxies` or `allow_redirects` to `invoke_method()` | they raise `TypeError` (only `timeout` and `files` are accepted) | Remove them. Set proxies with `HTTP(S)_PROXY` / `NO_PROXY`, and custom CA certificates with `REQUESTS_CA_BUNDLE` or `CURL_CA_BUNDLE` |
| catches `requests.exceptions.*` (e.g. `ConnectionError`, `Timeout`) | network errors raise `BacklogConnectionError` | Catch `backlog.base.BacklogConnectionError` (or `BacklogError`) |
| relies on HTTP redirects being followed | redirects are not followed | None expected: the Backlog API does not redirect; this keeps the API key from being sent to another host |
| relies on `requests` being installed as a dependency of python-backlog | it is no longer installed with python-backlog | Add `requests` to your own dependencies |
| imports `backlog.base.BacklogObject` or uses `BaseAPI.api` | they were removed (they were unused) | Remove those references |

TLS certificates are verified with the system trust store, plus `REQUESTS_CA_BUNDLE` / `CURL_CA_BUNDLE` and certifi when available.

### Deprecated

- `Project.list_categories()`, `add_category()`, `update_category()` and `delete_category()`. Use `BacklogAPI.category` ([#58](https://github.com/hassaku63/pbl/pull/58)).

## [0.8.1] - 2026-11-15

### Security

- Require `requests >= 2.33.0`. Older releases have known vulnerabilities (CVE-2024-47081, CVE-2026-25645) ([#55](https://github.com/hassaku63/pbl/pull/55)).

## [0.8.0] - 2026-11-15

### ⚠ Breaking changes

- **Python 3.8 and 3.9 are no longer supported.** python-backlog requires Python 3.10 or later and is tested on 3.10 to 3.14 ([#52](https://github.com/hassaku63/pbl/pull/52)). Both versions are end of life.
  - Migration: upgrade to Python 3.10 or later. If you cannot upgrade yet, pin `python-backlog<0.8`: pip then installs 0.7.6, which contains the security and bug fixes of 0.7.5 and 0.7.6. On Python 3.8 and 3.9, pip skips 0.8.0 and later automatically because of `requires-python`.

### Changed

- The package is built from `pyproject.toml` instead of `setup.py` ([#52](https://github.com/hassaku63/pbl/pull/52)).
- The `requests` requirement is relaxed from `~=2.32.2` to `>=2.32.2,<3` ([#52](https://github.com/hassaku63/pbl/pull/52)).

## [0.7.6] - 2026-11-15

A maintenance release of the 0.7 line, for Python 3.8 and 3.9. It was published after 0.8.0. It also contains the changes of 0.7.5, which was tagged but never published to PyPI.

### Security

- Fix a shared mutable default argument in `BaseAPI.invoke_method()` that made every `BacklogAPI` instance reuse the API key of the first one, sending it to other spaces ([#44](https://github.com/hassaku63/pbl/pull/44)).
- Send the API key in the `Backlog-API-Key` header instead of the `apiKey` query parameter, so it no longer appears in URLs, logs or exception messages ([#44](https://github.com/hassaku63/pbl/pull/44)).
- Validate the space key, so the base URL cannot point to another host ([#44](https://github.com/hassaku63/pbl/pull/44)).

### Added

- A default request timeout of 30 seconds, configurable with `timeout` ([#44](https://github.com/hassaku63/pbl/pull/44)).
- `Project.create(chartEnabled=...)`; `chatEnabled` is kept as a deprecated alias ([#46](https://github.com/hassaku63/pbl/pull/46)).

### Fixed

- `BacklogAPI.patch()` (the `requests.ptach` typo) ([#44](https://github.com/hassaku63/pbl/pull/44)).
- Requests now send the parameters the Backlog API expects ([#46](https://github.com/hassaku63/pbl/pull/46)):
  - DELETE requests send their parameters in the body, so `Project.delete_issue_type()` (`substituteIssueTypeId`) and `Wiki.delete()` (`mailNotify`) work;
  - any 2xx response is a success for DELETE and PATCH, as for GET and POST;
  - `Issue.add_comment()` sends the comment in the body instead of the query string;
  - `Project.add_category()` and `update_category()` send the name;
  - `Project.list_users(excludeGroupMembers=True)` sends `true` (was `ture`);
  - `User.add()` and `update()` send `password` (was `passowrd`); `User.update()` sends only the given fields;
  - `Wiki.get_attachment()` returns the file name from `Content-Disposition` instead of `"test"`;
  - `Attachment.upload()` closes the file and sends a proper content type.

## [0.7.4] - 2024-09-07

The last release before this changelog was started. It republishes 0.7.3 without code changes.

## Internal

Changes that do not affect package users are not listed per version. Since 0.7.4 they include: hardened CI and release workflows with automatic releases when `VERSION` changes ([#45](https://github.com/hassaku63/pbl/pull/45), [#53](https://github.com/hassaku63/pbl/pull/53), [#54](https://github.com/hassaku63/pbl/pull/54), [#90](https://github.com/hassaku63/pbl/pull/90)), ruff instead of flake8 ([#59](https://github.com/hassaku63/pbl/pull/59)), test and tooling cleanups ([#56](https://github.com/hassaku63/pbl/pull/56), [#57](https://github.com/hassaku63/pbl/pull/57)), the generated API coverage document and the record of removed endpoints ([#64](https://github.com/hassaku63/pbl/pull/64), [#96](https://github.com/hassaku63/pbl/pull/96)), and opt-in end-to-end tests ([#63](https://github.com/hassaku63/pbl/pull/63), [#72](https://github.com/hassaku63/pbl/pull/72), [#75](https://github.com/hassaku63/pbl/pull/75), [#79](https://github.com/hassaku63/pbl/pull/79), [#80](https://github.com/hassaku63/pbl/pull/80), [#82](https://github.com/hassaku63/pbl/pull/82)).

[Unreleased]: https://github.com/hassaku63/pbl/compare/v0.19.0...HEAD
[0.19.0]: https://github.com/hassaku63/pbl/compare/v0.18.0...v0.19.0
[0.18.0]: https://github.com/hassaku63/pbl/compare/v0.17.0...v0.18.0
[0.17.0]: https://github.com/hassaku63/pbl/compare/v0.16.0...v0.17.0
[0.16.0]: https://github.com/hassaku63/pbl/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/hassaku63/pbl/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/hassaku63/pbl/compare/v0.13.1...v0.14.0
[0.13.1]: https://github.com/hassaku63/pbl/compare/v0.13.0...v0.13.1
[0.13.0]: https://github.com/hassaku63/pbl/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/hassaku63/pbl/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/hassaku63/pbl/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/hassaku63/pbl/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/hassaku63/pbl/compare/v0.8.1...v0.9.0
[0.8.1]: https://github.com/hassaku63/pbl/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/hassaku63/pbl/compare/v0.7.6...v0.8.0
[0.7.6]: https://github.com/hassaku63/pbl/compare/v0.7.4...v0.7.6
[0.7.4]: https://github.com/hassaku63/pbl/compare/v0.7.3...v0.7.4
