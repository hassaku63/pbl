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

    # Categories
    # https://developer.nulab.com/docs/backlog/api/2/get-category-list/
    print(api.category.list("SampleProject"))

    # IDs to use when adding or updating issues
    print(api.priority.list())                         # priorityId
    print(api.resolution.list())                       # resolutionId
    print(api.project.list_statuses("SampleProject"))  # statusId
    print(api.project.list_versions("SampleProject"))  # versionId[] / milestoneId[]

    # Versions/milestones and statuses of a project
    version = api.project.add_version("SampleProject", "v1.0", releaseDueDate="2026-12-31")
    api.project.update_version("SampleProject", version["id"], "v1.0", archived=True)
    status = api.project.add_status("SampleProject", "In Review", "#3b9dbd")
    api.project.update_status("SampleProject", status["id"], name="Reviewing")

    # Your own user, and the issues you watch
    me = api.user.get_myself()
    print(api.watching.list(me["id"], resourceAlreadyRead=False))  # unread watched issues

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

    """
    Project API
    """
    # list project users
    # https://developer.nulab.com/docs/backlog/api/2/get-project-list/
    print("# list project users")
    users = api.project.list_users("SampleProject")
    print(json.dumps(users, indent=2))


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

- `backlog.base.BacklogError` is raised when the API returns a non-2xx response.
- `backlog.base.BacklogConnectionError` (a subclass of `BacklogError`) is raised when the request could not be sent or no response was received, for example on a timeout.
- `backlog.base.BacklogRateLimitError` (a subclass of `BacklogError`) is raised on 429 Too Many Requests. Its `limit`, `remaining` and `reset` attributes hold the `X-RateLimit-*` headers.

## TLS certificates

HTTPS certificates are verified against the system trust store (it also honors `SSL_CERT_FILE` and `SSL_CERT_DIR`). If `certifi` is installed, or `REQUESTS_CA_BUNDLE` or `CURL_CA_BUNDLE` is set, those CA certificates are trusted as well.

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
