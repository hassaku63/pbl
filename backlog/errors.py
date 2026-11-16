# coding: utf-8
"""
Exceptions raised by python-backlog.

    BacklogError
    ├── BacklogConnectionError      the request could not be sent / no response (timeout, DNS, TLS, ...)
    └── BacklogAPIError             the API answered with a non-2xx status
        ├── BacklogBadRequestError      400
        ├── BacklogUnauthorizedError    401
        ├── BacklogForbiddenError       403
        ├── BacklogNotFoundError        404
        ├── BacklogRateLimitError       429
        └── BacklogServerError          5xx

All of them are importable from backlog.base as well. Error responses of the Backlog API look like
{"errors": [{"message": "No project.", "code": 6, "moreInfo": ""}]}:
https://developer.nulab.com/docs/backlog/error-response/
"""

import enum


class BacklogErrorCode(enum.IntEnum):
    """
    The "code" of an error in a Backlog API error response.
    """
    INTERNAL_ERROR = 1
    LICENCE_ERROR = 2
    LICENCE_EXPIRED_ERROR = 3
    ACCESS_DENIED_ERROR = 4
    UNAUTHORIZED_OPERATION_ERROR = 5
    NO_RESOURCE_ERROR = 6
    INVALID_REQUEST_ERROR = 7
    SPACE_OVER_CAPACITY_ERROR = 8
    RESOURCE_OVERFLOW_ERROR = 9
    TOO_LARGE_FILE_ERROR = 10
    AUTHENTICATION_ERROR = 11
    REQUIRED_MFA_ERROR = 12
    TOO_MANY_REQUESTS_ERROR = 13


class BacklogError(Exception):
    """
    Base class of all python-backlog errors.
    """
    pass


class BacklogConnectionError(BacklogError):
    """
    Raised when the request could not be sent or no response was received
    (DNS failure, refused connection, TLS error, timeout, ...).
    """
    pass


def _int_header(response, name):
    try:
        return int(response.headers.get(name))
    except (TypeError, ValueError):
        return None


def _parse_errors(response):
    """
    The "errors" array of a Backlog error response as a list of dicts, or [] if the body has none.
    """
    try:
        errors = response.json().get("errors")
    except (ValueError, AttributeError, TypeError):
        return []
    if not isinstance(errors, list):
        return []
    return [e for e in errors if isinstance(e, dict)]


class BacklogAPIError(BacklogError):
    """
    Raised when the API answers with a non-2xx status.

    :ivar status_code: the HTTP status code
    :ivar errors: the "errors" array of the response body (list of dicts with "message", "code" and "moreInfo"),
        or [] if the body has none
    :ivar response: the :class:`backlog._http.Response`
    """

    def __init__(self, message, response):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code
        self.errors = _parse_errors(response)

    @property
    def code(self):
        """
        The code of the first error: a :class:`BacklogErrorCode` for known codes, the raw value otherwise,
        or None if the response has no errors.
        """
        if not self.errors:
            return None
        code = self.errors[0].get("code")
        try:
            return BacklogErrorCode(code)
        except ValueError:
            return code

    @property
    def error_message(self):
        """
        The message of the first error, or None.
        """
        return self.errors[0].get("message") if self.errors else None


class BacklogBadRequestError(BacklogAPIError):
    """400 Bad Request, e.g. invalid or missing parameters (code 7: InvalidRequestError)."""


class BacklogUnauthorizedError(BacklogAPIError):
    """401 Unauthorized: the API key or access token is missing, invalid or expired."""


class BacklogForbiddenError(BacklogAPIError):
    """403 Forbidden: the user may not perform the operation (e.g. code 5: UnauthorizedOperationError)."""


class BacklogNotFoundError(BacklogAPIError):
    """404 Not Found: the resource does not exist or is not visible to the user (code 6: NoResourceError)."""


class BacklogServerError(BacklogAPIError):
    """5xx: an error on the Backlog side. Retrying later may help."""


class BacklogRateLimitError(BacklogAPIError):
    """
    Raised when the API returns 429 Too Many Requests (and retries, if enabled, are exhausted).

    :ivar limit: X-RateLimit-Limit (requests per minute), or None
    :ivar remaining: X-RateLimit-Remaining, or None
    :ivar reset: X-RateLimit-Reset (UTC epoch seconds when the window resets), or None
    """

    def __init__(self, message, response):
        super().__init__(message, response)
        self.limit = _int_header(response, "X-RateLimit-Limit")
        self.remaining = _int_header(response, "X-RateLimit-Remaining")
        self.reset = _int_header(response, "X-RateLimit-Reset")


_STATUS_ERRORS = {
    400: BacklogBadRequestError,
    401: BacklogUnauthorizedError,
    403: BacklogForbiddenError,
    404: BacklogNotFoundError,
    429: BacklogRateLimitError,
}


def error_for_response(response):
    """
    Build the exception for a non-2xx response. The message keeps the historical
    "Http response <status>: <body>" format.
    """
    message = "Http response {status}: {body}".format(status=response.status_code, body=response.text)
    cls = _STATUS_ERRORS.get(response.status_code)
    if cls is None:
        cls = BacklogServerError if response.status_code >= 500 else BacklogAPIError
    return cls(message, response)
