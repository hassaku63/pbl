---
name: api-change
description: Checklist for adding or changing python-backlog methods that call the Backlog API. Use it whenever a change touches backlog/*.py (new endpoints, new or renamed methods or parameters, removed or deprecated methods), to keep docs/API_COVERAGE.md and README.md in sync and to decide whether they need updates.
---

# Adding or changing Backlog API methods

Use this checklist whenever a change touches the API surface in `backlog/*.py`.

## 1. Check the official reference

The endpoint list in `docs/api_endpoints.json` is maintained by reading the documentation, not by scraping it. Each entry records the page `url` and the date it was `last_accessed`.

- Open the endpoint's page (its `url`, or find it from the index at https://developer.nulab.com/docs/backlog/). Check the method, path, parameters (including `xxx[]` array parameters) and the role that may call it.
- The API reference pages are updated even when the changelog is not. Trust the endpoint page over the changelog.
- Update `docs/api_endpoints.json`:
  - set `last_accessed` (YYYY-MM-DD) on every entry whose page you read;
  - add an entry for an endpoint that is not listed yet. Copy the method, path and title from its page.
- When you have reviewed the whole index for added or removed endpoints, also update `index_last_accessed`. Remove entries only when the page is gone from the reference.
- The pages show no last-updated date. The HTTP `Last-Modified` header reflects the deployment of the whole site, so do not record it.

## 2. Implement

- Call `self.api.invoke_method(<"GET"|"POST"|"PATCH"|"DELETE">, <uri>, ...)` with a literal HTTP method. `scripts/api_coverage.py` finds endpoints by statically reading these calls.
- Build the URI with a string literal, `"...".format(...)` or an f-string. A small helper that returns such a template also works, like `Issue._comment_uri`.
- Keep existing method names and signatures backward compatible. Use deprecation warnings rather than removals.
- Add tests that assert the method, path, query string and body that are sent (see `tests/fake_http.py`). Where it is useful, add a happy-path case to `tests/e2e/`.

## 3. Update the coverage document (required; CI enforces it)

```bash
python scripts/api_coverage.py generate
python scripts/api_coverage.py check
```

Commit the regenerated `docs/API_COVERAGE.md`. The "API coverage doc" CI job fails if it does not match the code.

## 4. Decide whether README.md needs an update (judgment)

Update README.md when the change:

- adds a new resource or entry point (e.g. a new `api.<resource>` attribute or a new module such as `backlog.oauth`);
- adds an option, error type or behavior that users must know about (authentication, retries, domains, ...);
- changes or deprecates something existing users rely on. Add it to the upgrade notes as well.

README.md does not need an update for an additional method on an existing resource that follows the existing conventions. `docs/API_COVERAGE.md` already lists it.

State the decision in the pull request description, for example "README: not needed (new methods on an existing resource)". The "Release check" comment reminds you when `backlog/` changed but neither document did.

## 5. Version

Bump `VERSION` only if the change affects package users and should be released. See "Releasing" in CONTRIBUTING.md.
