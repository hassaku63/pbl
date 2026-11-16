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

### Check deprecations and removals

Backlog announces API removals in the changelog (https://developer.nulab.com/docs/backlog/changelog/, as "Deprecated - ..." and later "Removed the following deprecated APIs") and sometimes in a blog post, for example https://nulab.com/blog/product-updates/backlog/discontinued-apis-august-2024/. Some endpoints have also disappeared from the reference without any changelog entry, such as Add/Update/Delete User.

- Read the changelog entries since the last check, in English and Japanese (`/ja/docs/backlog/changelog/`). Look for "Deprecated", "Removed" and permission changes ("Changed ... role").
- When an endpoint is removed, or its reference page is gone (it redirects to the API index):
  - move it from `endpoints` to `removed` in `docs/api_endpoints.json`. Record `removed_in` and `removed_on` (changelog version and date), the `replacement` endpoint, the `announcement` and `changelog` URLs if there are any, and `confirmed_on`. Without a changelog entry, set `removed_in` to null and explain in `note`;
  - deprecate every python-backlog method that calls it: emit a `DeprecationWarning` (with `stacklevel` pointing at the caller) and add `.. deprecated:: <version>` to the docstring. Mention the official announcement in the warning if there is one in English, and the replacement method if python-backlog has one. Keep the method working until a major release removes it;
  - add the replacement endpoint, if python-backlog does not implement it yet.
- `python scripts/api_coverage.py check` fails when a method that is not deprecated calls an endpoint in `removed`.
- When only "Deprecated" is announced and the endpoint still works, deprecate the methods the same way, and move the endpoint to `removed` once the changelog says it was removed.

## 2. Implement

- Call `self.api.invoke_method(<"GET"|"POST"|"PATCH"|"DELETE">, <uri>, ...)` with a literal HTTP method. `scripts/api_coverage.py` finds endpoints by statically reading these calls.
- Build the URI with a string literal, `"...".format(...)` or an f-string. A small helper that returns such a template also works, like `Issue._comment_uri`.
- Keep existing method names and signatures backward compatible. Use deprecation warnings rather than removals (see "Check deprecations and removals" above).
- Add tests that assert the method, path, query string and body that are sent (see `tests/fake_http.py`). Where it is useful, add a happy-path case to `tests/e2e/`, following the `e2e-test` skill and `tests/e2e/README.md`.

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
