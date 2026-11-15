# coding: utf-8

import re
import time
from backlog import _http
from backlog._http import Response  # noqa: F401  (re-exported for type references)
from backlog.wiki import Wiki
from backlog.attachment import Attachment
from backlog.project import Project
from backlog.issue import Issue
from backlog.git import Git
from backlog.user import User
from backlog.category import Category
from backlog.custom_field import CustomField
from backlog.priority import Priority
from backlog.resolution import Resolution

BACKLOG_BASE_URL = "https://{space}.{domain}"
BACKLOG_URI_PREFIX = "/api/v2/"
BACKLOG_API_KEY_HEADER = "Backlog-API-Key"
DEFAULT_TIMEOUT = 30
DEFAULT_DOMAIN = "backlog.jp"
# Domains Backlog spaces are hosted on. Only these are accepted, so the API key or access token
# can never be sent to another host.
BACKLOG_DOMAINS = ("backlog.jp", "backlog.com", "backlogtool.com")
DEFAULT_RATE_LIMIT_MAX_WAIT = 60

# Space keys consist of alphanumerics and hyphens. Validating it prevents the
# base URL (and therefore the API key) from being pointed at an arbitrary host.
_SPACE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")


def build_base_url(space, domain=DEFAULT_DOMAIN):
    """
    Return the base URL of a space (e.g. "https://example.backlog.com"), validating the space key and domain.
    """
    if not isinstance(space, str) or not _SPACE_PATTERN.match(space):
        raise ValueError("Invalid space key: {!r}".format(space))
    if domain not in BACKLOG_DOMAINS:
        raise ValueError("Invalid domain: {!r}. Must be one of: {}".format(domain, ", ".join(BACKLOG_DOMAINS)))
    return BACKLOG_BASE_URL.format(space=space, domain=domain)


class BacklogError(Exception):
    pass


class BacklogConnectionError(BacklogError):
    """
    Raised when the request could not be sent or no response was received
    (DNS failure, refused connection, TLS error, timeout, ...).
    """
    pass


class BacklogRateLimitError(BacklogError):
    """
    Raised when the API returns 429 Too Many Requests (and retries, if enabled, are exhausted).

    :ivar limit: X-RateLimit-Limit (requests per minute), or None
    :ivar remaining: X-RateLimit-Remaining, or None
    :ivar reset: X-RateLimit-Reset (UTC epoch seconds when the window resets), or None
    :ivar response: the :class:`backlog._http.Response`
    """

    def __init__(self, message, response):
        super().__init__(message)
        self.response = response
        self.limit = _int_header(response, "X-RateLimit-Limit")
        self.remaining = _int_header(response, "X-RateLimit-Remaining")
        self.reset = _int_header(response, "X-RateLimit-Reset")


def _int_header(response, name):
    try:
        return int(response.headers.get(name))
    except (TypeError, ValueError):
        return None


# Keyword arguments accepted by invoke_method() in addition to its named parameters.
_SUPPORTED_KWARGS = frozenset(["timeout", "files"])


class BaseAPI(object):
    def __init__(
        self,
        space,
        api_key=None,
        timeout=DEFAULT_TIMEOUT,
        *,
        domain=DEFAULT_DOMAIN,
        access_token=None,
        rate_limit_retries=0,
        rate_limit_max_wait=DEFAULT_RATE_LIMIT_MAX_WAIT,
    ):
        """
        :param space: Backlog space key (the "xxx" of https://xxx.backlog.jp)
        :param api_key: API key. It is sent in the "Backlog-API-Key" request header.
        :param timeout: Default timeout (seconds) passed to the HTTP client.
            Can be overridden per request with the "timeout" keyword argument. None disables it.
        :param domain: Domain of the space: "backlog.jp" (default), "backlog.com" or "backlogtool.com".
        :param access_token: OAuth 2.0 access token, sent as "Authorization: Bearer ...".
            Use either api_key or access_token. See :mod:`backlog.oauth` to obtain and refresh tokens.
        :param rate_limit_retries: How many times to retry a request that was rejected with
            429 Too Many Requests. 0 (default) raises :class:`BacklogRateLimitError` immediately.
        :param rate_limit_max_wait: Maximum number of seconds to wait before a retry. If the rate limit
            resets later than that, :class:`BacklogRateLimitError` is raised instead of waiting.
        """
        if api_key is not None and access_token is not None:
            raise ValueError("Specify either api_key or access_token, not both")
        if not isinstance(rate_limit_retries, int) or rate_limit_retries < 0:
            raise ValueError("rate_limit_retries must be a non-negative integer")
        self.space = space
        self.domain = domain
        self.api_key = api_key
        self.access_token = access_token
        self.timeout = timeout
        self.rate_limit_retries = rate_limit_retries
        self.rate_limit_max_wait = rate_limit_max_wait
        self.base_url = build_base_url(space, domain) + BACKLOG_URI_PREFIX
        self._build_api()

    def set_access_token(self, access_token):
        """
        Replace the OAuth 2.0 access token, e.g. after refreshing it with :func:`backlog.oauth.refresh_access_token`.
        """
        if self.api_key is not None:
            raise ValueError("This client uses an API key; it cannot also use an access token")
        self.access_token = access_token

    def _build_api(self):
        pass

    def _build_headers(self, headers=None):
        """
        Merge authentication headers into the given headers without mutating it.
        """
        _headers = {}
        if self.api_key is not None:
            _headers[BACKLOG_API_KEY_HEADER] = self.api_key
        if self.access_token is not None:
            _headers["Authorization"] = "Bearer {}".format(self.access_token)
        if headers:
            _headers.update(headers)
        return _headers

    def invoke_method(self, method, uri, query_param=None, request_param=None, headers=None, **kwargs):
        """
        Delegate requests to get/post/delete/patch method.

        :param method: HTTP Method. supports GET/POST/DELETE/PATCH
        :param uri: API Endpoint. 'uri' expects a URI excluded '/api/v2/' prefix
        :param query_param: dict of URL parameter. this will be url-encoded string
        :param request_param: dict of body parameter. this will use when invoke post request
        :param headers: HTTP Header dict. Authentication headers are added automatically.
        :param kwargs: ``timeout`` (seconds, overrides the client default) and ``files``
            (dict of field name to ``(filename, fileobj_or_bytes[, content_type])``).
        :return: :class:`backlog._http.Response`
        """
        unsupported = set(kwargs) - _SUPPORTED_KWARGS
        if unsupported:
            raise TypeError(
                "Unsupported keyword argument(s): {}. Since 0.9.0 python-backlog no longer uses requests, "
                "so requests-specific options are not available.".format(", ".join(sorted(unsupported)))
            )

        # Copy the arguments so that neither the caller's dicts nor any shared state are mutated.
        query_param = dict(query_param or {})
        request_param = dict(request_param or {})
        headers = self._build_headers(headers)
        kwargs.setdefault("timeout", self.timeout)

        method = method.lower()

        if method == "get":
            resp = self.get(method, uri, query_param, request_param, headers, **kwargs)

        elif method == "post":
            resp = self.post(method, uri, query_param, request_param, headers, **kwargs)

        elif method == "delete":
            resp = self.delete(method, uri, query_param, request_param, headers, **kwargs)

        elif method == "patch":
            resp = self.patch(method, uri, query_param, request_param, headers, **kwargs)

        else:
            raise BacklogError("Not supported http method: {}".format(method))

        return resp

    def get(self, method, uri, query_param, request_param, headers, **kwargs):
        """Sorry, not implemented yet
        """
        raise NotImplementedError

    def post(self, method, uri, query_param, request_param, headers, **kwargs):
        """Sorry, not implemented yet
        """
        raise NotImplementedError

    def delete(self, method, uri, query_param, request_param, headers, **kwargs):
        """Sorry, not implemented yet
        """
        raise NotImplementedError

    def patch(self, method, uri, query_param, request_param, headers, **kwargs):
        """Sorry, not implemented yet
        """
        raise NotImplementedError


class BacklogAPI(BaseAPI):
    """
    Backlog API client using the standard library HTTP client.
    """
    def _build_api(self):
        self.wiki = Wiki(self)
        self.attachment = Attachment(self)
        self.project = Project(self)
        self.issue = Issue(self)
        self.git = Git(self)
        self.user = User(self)
        self.category = Category(self)
        self.custom_field = CustomField(self)
        self.priority = Priority(self)
        self.resolution = Resolution(self)

    def get_rate_limit(self):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-rate-limit/

        :return: the rate limits currently applied ("read", "update", "search" and "icon")
        """
        resp = self.invoke_method("GET", "rateLimit")
        return resp.json()

    @staticmethod
    def _raise_for_status(resp):
        if resp.status_code // 100 == 2:
            return resp
        message = "Http response {status}: {message}".format(status=resp.status_code, message=resp.text)
        if resp.status_code == 429:
            raise BacklogRateLimitError(message, resp)
        raise BacklogError(message)

    def _rate_limit_wait(self, resp, attempt):
        """
        Seconds to wait before retrying a 429 response: until X-RateLimit-Reset, or Retry-After,
        or an exponential backoff when neither header is present.
        """
        reset = _int_header(resp, "X-RateLimit-Reset")
        if reset is not None:
            return max(1.0, reset - time.time() + 1)
        retry_after = _int_header(resp, "Retry-After")
        if retry_after is not None:
            return max(1.0, float(retry_after))
        return float(2 ** attempt)

    def _send(self, method, uri, query_param, request_param, headers, timeout=None, files=None):
        url = self.base_url + uri
        attempt = 0
        while True:
            try:
                resp = _http.request(
                    method,
                    url,
                    params=query_param,
                    data=request_param,
                    headers=headers,
                    files=files,
                    timeout=timeout,
                )
            except OSError as e:
                raise BacklogConnectionError(
                    "Failed to send {method} request to {url}: {error}".format(method=method.upper(), url=url, error=e)
                ) from e
            if resp.status_code == 429 and attempt < self.rate_limit_retries:
                wait = self._rate_limit_wait(resp, attempt)
                if wait <= self.rate_limit_max_wait:
                    _rewind_files(files)
                    time.sleep(wait)
                    attempt += 1
                    continue
            return self._raise_for_status(resp)

    def get(self, method, uri, query_param, request_param, headers, **kwargs):
        return self._send("GET", uri, query_param, None, headers, **kwargs)

    def post(self, method, uri, query_param, request_param, headers, **kwargs):
        return self._send("POST", uri, query_param, request_param, headers, **kwargs)

    def delete(self, method, uri, query_param, request_param, headers, **kwargs):
        return self._send("DELETE", uri, query_param, request_param, headers, **kwargs)

    def patch(self, method, uri, query_param, request_param, headers, **kwargs):
        return self._send("PATCH", uri, query_param, request_param, headers, **kwargs)


def _rewind_files(files):
    """
    Rewind file objects before a retry so that the upload is sent again in full.
    """
    for spec in (files or {}).values():
        content = spec[1] if isinstance(spec, (list, tuple)) and len(spec) > 1 else None
        if hasattr(content, "seek"):
            content.seek(0)
