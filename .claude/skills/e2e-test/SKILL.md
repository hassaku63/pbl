---
name: e2e-test
description: How to add or change end-to-end tests in tests/e2e/ that call a real Backlog space. Use it whenever writing or editing those tests, or when adding an API method that should get an end-to-end check, so that the tests keep personal data out of public CI logs, clean up after themselves and stay within rate limits.
---

# Writing end-to-end tests

The rules are in `tests/e2e/README.md`. Read it before you write or change a test, and follow it. In short:

1. **Choose the tier:**
   - R: read-only → `requires_space` / `requires_project`;
   - W: create, update and delete in the test project → `requires_write`;
   - A: space administrator operations, real personal data or external side effects such as invitation mails → `requires_local_admin`. Tier A never runs in CI.
2. **Assert the minimal structure only, with `tests/e2e/assertions.py`:** values the test chose, always-present keys, and the types of generated values. Never use `self.assert*` or `print` in `tests/e2e/`: `tests/test_e2e_support.py` fails if you do. Never use personal data as an expected value.
3. **Never store or output responses.**
4. **Clean up:** name resources with `resource_name(...)`, delete them in `finally`, and teach `test_00_cleanup.py` about any new kind of resource. Do not trigger notifications.
5. **Use `client()`**, which throttles requests and retries on 429.
6. **Before pushing:** run `python -m unittest` (the end-to-end tests skip without credentials). If you can, also run the end-to-end tests against a simulated API or a real test space.
