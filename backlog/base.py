# coding: utf-8

import re
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

BACKLOG_BASE_URL = "https://{space}.backlog.jp"
BACKLOG_URI_PREFIX = "/api/v2/"
BACKLOG_API_KEY_HEADER = "Backlog-API-Key"
DEFAULT_TIMEOUT = 30

# Space keys consist of alphanumerics and hyphens. Validating it prevents the
# base URL (and therefore the API key) from being pointed at an arbitrary host.
_SPACE_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")


class BacklogError(Exception):
    pass


class BacklogConnectionError(BacklogError):
    """
    Raised when the request could not be sent or no response was received
    (DNS failure, refused connection, TLS error, timeout, ...).
    """
    pass


# Keyword arguments accepted by invoke_method() in addition to its named parameters.
_SUPPORTED_KWARGS = frozenset(["timeout", "files"])


class BaseAPI(object):
    def __init__(self, space, api_key=None, timeout=DEFAULT_TIMEOUT):
        """
        :param space: Backlog space key (the "xxx" of https://xxx.backlog.jp)
        :param api_key: API key. It is sent in the "Backlog-API-Key" request header.
        :param timeout: Default timeout (seconds) passed to the HTTP client.
            Can be overridden per request with the "timeout" keyword argument. None disables it.
        """
        if not isinstance(space, str) or not _SPACE_PATTERN.match(space):
            raise ValueError("Invalid space key: {!r}".format(space))
        self.space = space
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = BACKLOG_BASE_URL.format(space=space) + BACKLOG_URI_PREFIX
        self._build_api()

    def _build_api(self):
        pass

    def _build_headers(self, headers=None):
        """
        Merge authentication headers into the given headers without mutating it.
        """
        _headers = {}
        if self.api_key is not None:
            _headers[BACKLOG_API_KEY_HEADER] = self.api_key
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

    @staticmethod
    def _raise_for_status(resp):
        if resp.status_code // 100 == 2:
            return resp
        raise BacklogError("Http response {status}: {message}".format(status=resp.status_code, message=resp.text))

    def _send(self, method, uri, query_param, request_param, headers, timeout=None, files=None):
        try:
            resp = _http.request(
                method,
                self.base_url + uri,
                params=query_param,
                data=request_param,
                headers=headers,
                files=files,
                timeout=timeout,
            )
        except OSError as e:
            raise BacklogConnectionError(
                "Failed to send {method} request to {url}: {error}".format(method=method.upper(), url=self.base_url + uri, error=e)
            ) from e
        return self._raise_for_status(resp)

    def get(self, method, uri, query_param, request_param, headers, **kwargs):
        return self._send("GET", uri, query_param, None, headers, **kwargs)

    def post(self, method, uri, query_param, request_param, headers, **kwargs):
        return self._send("POST", uri, query_param, request_param, headers, **kwargs)

    def delete(self, method, uri, query_param, request_param, headers, **kwargs):
        return self._send("DELETE", uri, query_param, request_param, headers, **kwargs)

    def patch(self, method, uri, query_param, request_param, headers, **kwargs):
        return self._send("PATCH", uri, query_param, request_param, headers, **kwargs)
