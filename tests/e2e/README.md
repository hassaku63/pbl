# End-to-end test guidelines

The tests in `tests/e2e/` call a real Backlog space. They are skipped unless `BACKLOG_E2E_SPACE` and `BACKLOG_E2E_API_KEY` are set (see `support.py` for all variables). They run in CI (`.github/workflows/e2e.yml`) for a public repository, so **anything they print is public**. API responses contain personal data, such as names and mail addresses. Follow these rules for every end-to-end test.

## 1. Assert only the minimal structure the test needs

Matching whole payloads is impossible and not useful: the API generates IDs and timestamps, and responses gain fields over time. Check only what the scenario needs:

- **Values the test chose itself:** for example, the summary or status sent when creating an issue, or the content of a comment.
- **Keys that are always present, whatever the usage:** for example, `id`, `issueKey`, `created`.
- **Generated values** (IDs, dates): check that they exist and have the right type, not their value.
- **Lists:** check that a list is returned, optionally with a minimum length, and that each item has the keys the test relies on.

## 2. Never put response values in failure messages

`unittest`'s `self.assert*` methods print the compared values when they fail. For example, `assertIn("id", user)` prints the whole user, including the mail address. **Do not use them in `tests/e2e/`.** Use the helpers in `assertions.py`; their messages contain only field names and types:

| Helper | Checks |
|---|---|
| `has_keys(obj, *keys)` | `obj` is an object with the keys |
| `field_equals(obj, key, expected)` | a field has a value the test chose |
| `field_type(obj, key, type)` | a field has the right type (e.g. a generated ID is an `int`) |
| `is_list(obj, min_length=0, item_keys=())` | a list, and the keys of its items |
| `is_count(obj, expected=None)` | `{"count": <int>}` |
| `contains_id(items, id)` | a list contains the item the test created |
| `is_true(condition, message)` | anything else; write the message yourself, without response values |

Never use personal data, such as names, mail addresses or user IDs, as expected values. `tests/test_e2e_support.py` fails if a module in `tests/e2e/` uses `self.assert*` or `print`.

## 3. Never store or output responses

Do not `print` responses, write them to files, or upload them as CI artifacts. To inspect a payload while debugging, do it in a local run, never in CI.

In CI, `mask.py` registers the API key user's name, mail address and IDs with `::add-mask::` before the tests run. This is a safety net only: masking works on exact strings. Rules 2 and 3 are what keep data out of the log.

## 4. Clean up what you create

- Name every resource with `resource_name(label)`. This gives `pbl-e2e-<run id>-<label>`.
- Delete what the test creates in `try` / `finally`.
- `test_00_cleanup.py` runs first and deletes leftovers of earlier runs: names with the `pbl-e2e-` prefix created more than an hour ago. Extend it when you add a new kind of resource.
- Do not trigger notifications: do not pass `notifiedUserId[]`, and pass `mailNotify=False` where the API has it.

## 5. Tiers

| Tier | What | Where | Decorator |
|---|---|---|---|
| R | Read-only operations a normal user can do | CI and local | `requires_space` / `requires_project` |
| W | Create, update and delete in the test project (normal user, or administrator of the test project only) | CI and local (`BACKLOG_E2E_WRITE=1`) | `requires_write` |
| A | Space administrator operations, operations that need real personal data (e.g. a mail address), or that have external side effects (e.g. invitation mails) | **Local only** (`BACKLOG_E2E_ADMIN=1`) | `requires_local_admin` |

`support.py` refuses to load when `BACKLOG_E2E_ADMIN=1` is set in CI. Tier A results are shared as a report that contains no response data.

Run tier A with `scripts/e2e_local.py`. It refuses to run in CI, lists what will be created and deleted, asks for confirmation, and writes `e2e-report.md` (ignored by git). The report has the result of each test and the endpoints it called, as the HTTP method plus the path with IDs replaced (`PATCH users/:id`). It records failure messages only for assertions from `assertions.py` and error types only for other exceptions. Paste the report into an issue or pull request, not the console output: the console shows the space name.

```bash
BACKLOG_E2E_SPACE=your-space BACKLOG_E2E_API_KEY=admin-key BACKLOG_E2E_USER_EMAIL=you+e2e@example.com \
    python scripts/e2e_local.py            # tier A only; --all adds tier R (and W with BACKLOG_E2E_WRITE=1)
```

When you add a tier A test, describe what it creates and its side effects in the plan that `scripts/e2e_local.py` prints.

## 6. Rate limits

Use `client()` from `support.py`. It waits at least `BACKLOG_E2E_INTERVAL` seconds (default 1) between requests and retries on 429. Keep the number of requests per test small: the free plan has the lowest limits.
