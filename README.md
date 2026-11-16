# pbl

A Python package that wraps the [Backlog API v2](https://developer.nulab.com/docs/backlog/).

- Requires Python 3.10 or later.
- No runtime dependencies: only the Python standard library is used.
- [API coverage](https://github.com/hassaku63/pbl/blob/master/docs/API_COVERAGE.md): which Backlog API endpoints have dedicated methods.

## Usage

Install

```bash
pip install python-backlog
```

Code snippet

```python
import base64
import json
from backlog.base import BacklogAPI


def main():
    """
    Initialize API Object
    """
    # The API key is sent in the "Backlog-API-Key" request header.
    # Requests time out after 30 seconds by default (configurable with `timeout=`).
    api = BacklogAPI("your-space", "your-api-key")

    # The space
    print(api.get_space()["name"], api.get_space_licence()["licenceTypeId"])

    # Categories
    # https://developer.nulab.com/docs/backlog/api/2/get-category-list/
    print(api.category.list("SampleProject"))

    # IDs to use when adding or updating issues
    print(api.priority.list())                         # priorityId
    print(api.resolution.list())                       # resolutionId
    print(api.project.list_statuses("SampleProject"))  # statusId
    print(api.project.list_versions("SampleProject"))  # versionId[] / milestoneId[]

    # Members of a project (project administrators)
    api.project.add_user("SampleProject", 12)  # numeric user ID
    api.project.add_team("SampleProject", api.team.list()[0]["id"])

    # Custom fields (project administrators)
    field = api.custom_field.add_single_list_custom_field("SampleProject", "Severity", items=["Low", "High"])
    api.custom_field.add_list_item("SampleProject", field["id"], "Critical")
    api.custom_field.update("SampleProject", field["id"], required=True)

    # Webhooks of a project (project administrators)
    hook = api.webhook.add("SampleProject", "CI", "https://ci.example.com/backlog", activityTypeIds=[1, 2])
    api.webhook.update("SampleProject", hook["id"], allEvent=True)

    # Versions/milestones and statuses of a project
    version = api.project.add_version("SampleProject", "v1.0", releaseDueDate="2026-12-31")
    api.project.update_version("SampleProject", version["id"], "v1.0", archived=True)
    status = api.project.add_status("SampleProject", "In Review", "#3b9dbd")
    api.project.update_status("SampleProject", status["id"], name="Reviewing")

    # Your own user, and the issues you watch
    me = api.user.get_myself()
    print(api.watching.list(me["id"], resourceAlreadyRead=False))  # unread watched issues
    print(api.user.list_recently_viewed_issues(count=5))  # [{"issue": {...}, "updated": ...}, ...]

    # Stars
    api.star.add(issueId=123)
    print(api.star.count_received(me["id"], since="2026-01-01"))

    # Your notifications
    print(api.notification.count(resourceAlreadyRead=False))  # number of unread notifications
    print(api.notification.list(count=10))

    # Recent updates (activities) of the space, a project or a user
    print(api.activity.list(count=10))
    print(api.activity.list_project("SampleProject", activityTypeId=[1, 2]))  # issues added / updated

    # Documents
    project = api.project.get("SampleProject")
    print(api.document.list(projectId=project["id"], keyword="spec"))
    print(api.document.tree("SampleProject"))

    # Shared files
    entries = api.project.list_shared_files("SampleProject", path="docs/specs")
    shared = api.project.get_shared_file("SampleProject", entries[0]["id"])  # {"id", "name", "data": bytes}

    """
    Project API
    """
    # list project users
    # https://developer.nulab.com/docs/backlog/api/2/get-project-list/
    print("# list project users")
    users = api.project.list_users("SampleProject")
    print(json.dumps(users, indent=2))
    print(api.project.list_administrators("SampleProject"), api.project.list_teams("SampleProject"))
    icon = api.user.get_icon(users[0]["id"])  # {"name": "person_168.gif", "data": bytes}


    """
    Wiki API
    """
    # list wikis
    # https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-list/
    print("# list wikis")
    wikis = api.wiki.list("SampleProject")
    print(json.dumps(wikis[0], indent=2))
    print(api.wiki.count("SampleProject"), api.wiki.list_tags("SampleProject"))
    print(api.wiki.list_history(wikis[0]["id"], count=5))  # past versions of the page

    # get attachment
    # https://developer.nulab.com/docs/backlog/api/2/get-issue-attachment/
    print("# get attachment")
    wiki = [w for w in api.wiki.list("SampleProject") if len(w["attachments"]) > 0][0]
    attachment = api.wiki.get_attachment(
        wikiId=wiki["id"],
        attachmentId=wiki["attachments"][0]["id"])
    attachment["data"] = base64.b64encode(attachment["data"]).decode()
    print(json.dumps(attachment, indent=2))


if __name__ == "__main__":
    main()
```

## Pagination

List endpoints return at most 100 items per request. The `iter...()` methods request one page after another and yield every item; they stop after the last page:

```python
for issue in api.issue.iter(**{"projectId[]": [project["id"]], "statusId[]": [1]}):  # offset / count
    print(issue["issueKey"])

for activity in api.activity.iter_project("SampleProject", activityTypeId=[1]):  # newest first (minId / maxId)
    print(activity["id"])
```

| Method | Paging |
|---|---|
| `issue.iter()`, `document.iter()`, `watching.iter()`, `git.iter_pull_requests()` | offset / count |
| `issue.iter_comments()` (oldest first), `activity.iter()`, `iter_project()`, `iter_user()`, `notification.iter()`, `star.iter_received()`, `wiki.iter_history()` (newest first) | minId / maxId; pass `order="asc"` or `"desc"` |

For any other list method, use `backlog.pagination.iterate_by_offset(method, ...)` or `iterate_by_id(method, ...)`. Every page is a separate request, so `rate_limit_retries` (see Options) is useful for long iterations.

## Options

```python
from backlog.base import BacklogAPI

# Spaces on backlog.com (or backlogtool.com); the default is backlog.jp
api = BacklogAPI("your-space", "your-api-key", domain="backlog.com")

# Retry requests rejected with 429 Too Many Requests, waiting until the rate limit resets
# (at most rate_limit_max_wait seconds per retry). Disabled by default.
api = BacklogAPI("your-space", "your-api-key", rate_limit_retries=3, rate_limit_max_wait=60)
print(api.get_rate_limit())
```

## OAuth 2.0

Instead of an API key, you can use an OAuth 2.0 access token, which is sent in the `Authorization: Bearer` header.
`backlog.oauth` helps with the [Authorization Code Grant](https://developer.nulab.com/docs/backlog/auth/):

```python
from backlog import oauth
from backlog.base import BacklogAPI

url = oauth.authorization_url("your-space", client_id, redirect_uri, state=state)  # send the user here
token = oauth.request_access_token("your-space", client_id, client_secret, code, redirect_uri)
api = BacklogAPI("your-space", access_token=token["access_token"])

# Access tokens expire after an hour
token = oauth.refresh_access_token("your-space", client_id, client_secret, token["refresh_token"])
api.set_access_token(token["access_token"])
```

## Errors

All exceptions are subclasses of `backlog.base.BacklogError` (they are defined in `backlog.errors`):

| Exception | Raised when |
|---|---|
| `BacklogConnectionError` | the request could not be sent or no response was received, for example on a timeout |
| `BacklogAPIError` | the API returned a non-2xx status (base class of the following) |
| `BacklogBadRequestError` | 400, e.g. invalid or missing parameters |
| `BacklogUnauthorizedError` | 401, the API key or access token is invalid or expired |
| `BacklogForbiddenError` | 403, the user may not perform the operation |
| `BacklogNotFoundError` | 404, the resource does not exist or is not visible to the user |
| `BacklogRateLimitError` | 429 Too Many Requests; `limit`, `remaining` and `reset` hold the `X-RateLimit-*` headers |
| `BacklogServerError` | 5xx |

`BacklogAPIError` has `status_code`, `response`, `errors` (the `errors` array of the [error response](https://developer.nulab.com/docs/backlog/error-response/)), `code` (the first error code as a `BacklogErrorCode`) and `error_message`:

```python
from backlog.base import BacklogErrorCode, BacklogNotFoundError

try:
    api.issue.get("SAMPLE-1")
except BacklogNotFoundError as e:
    print(e.status_code, e.code is BacklogErrorCode.NO_RESOURCE_ERROR, e.error_message)
```

## TLS certificates

HTTPS certificates are verified against the system trust store (it also honors `SSL_CERT_FILE` and `SSL_CERT_DIR`). If `certifi` is installed, or `REQUESTS_CA_BUNDLE` or `CURL_CA_BUNDLE` is set, those CA certificates are trusted as well.

## Deprecations

- `User.add()`, `User.update()` and `User.delete()` are deprecated since 0.18.0 and emit a `DeprecationWarning`. Their endpoints were removed from the official API reference and are reported not to work in spaces on the new plans, where users are invited and managed in the Backlog web UI. They may still work in spaces on the old plans and will be removed in a future release. To remove a user from a project, use `Project.delete_user()`.
- `Project.list_categories()`, `add_category()`, `update_category()` and `delete_category()` are deprecated since 0.9.0. Use `BacklogAPI.category` instead.

## Upgrading to 0.9

0.9.0 removed the dependency on `requests`:

- `BaseAPI.invoke_method()` returns a `backlog._http.Response` instead of a `requests.Response`. It provides `status_code`, `ok`, `headers`, `content`, `text` and `json()`.
- `invoke_method()` only accepts the `timeout` and `files` keyword arguments. Requests-specific options such as `verify` or `proxies` raise `TypeError`. Proxies are still read from the `HTTP(S)_PROXY` and `NO_PROXY` environment variables.
- Network errors raise `BacklogConnectionError` instead of `requests.exceptions.*`.
- Redirects are not followed, so the API key is never sent to another host.
- `Project.list_categories()`, `add_category()`, `update_category()` and `delete_category()` are deprecated. Use `BacklogAPI.category` instead.

## Contact

Please open an issue on [GitHub](https://github.com/hassaku63/pbl/issues).

Twitter: [hassaku_63](https://twitter.com/hassaku_63)
