# coding: utf-8
"""
Helpers for the Backlog OAuth 2.0 Authorization Code Grant.

https://developer.nulab.com/docs/backlog/auth/

Typical flow::

    from backlog import oauth
    from backlog.base import BacklogAPI

    # 1. Send the user to the authorization page.
    url = oauth.authorization_url("your-space", client_id, redirect_uri, state=state)

    # 2. Backlog redirects back to redirect_uri with ?code=...; exchange it for tokens.
    token = oauth.request_access_token("your-space", client_id, client_secret, code, redirect_uri)

    api = BacklogAPI("your-space", access_token=token["access_token"])

    # 3. Access tokens expire after an hour; refresh them with the refresh token.
    token = oauth.refresh_access_token("your-space", client_id, client_secret, token["refresh_token"])
    api.set_access_token(token["access_token"])
"""

import urllib.parse

from backlog import _http
from backlog.base import DEFAULT_DOMAIN, DEFAULT_TIMEOUT, BacklogConnectionError, BacklogError, build_base_url

AUTHORIZATION_PATH = "/OAuth2AccessRequest.action"
TOKEN_PATH = "/api/v2/oauth2/token"


def authorization_url(space, client_id, redirect_uri, state=None, domain=DEFAULT_DOMAIN):
    """
    Return the URL of the authorization page to send the user to.

    :param state: an opaque value to protect against CSRF; Backlog returns it to redirect_uri unchanged.
    """
    params = {"response_type": "code", "client_id": client_id, "redirect_uri": redirect_uri}
    if state is not None:
        params["state"] = state
    return build_base_url(space, domain) + AUTHORIZATION_PATH + "?" + urllib.parse.urlencode(params)


def request_access_token(space, client_id, client_secret, code, redirect_uri, domain=DEFAULT_DOMAIN, timeout=DEFAULT_TIMEOUT):
    """
    Exchange an authorization code for an access token and a refresh token.

    :return: dict with "access_token", "token_type", "expires_in" and "refresh_token"
    """
    return _token_request(space, domain, timeout, {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    })


def refresh_access_token(space, client_id, client_secret, refresh_token, domain=DEFAULT_DOMAIN, timeout=DEFAULT_TIMEOUT):
    """
    Obtain a new access token with a refresh token.

    :return: dict with "access_token", "token_type", "expires_in" and "refresh_token"
    """
    return _token_request(space, domain, timeout, {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    })


def _token_request(space, domain, timeout, data):
    url = build_base_url(space, domain) + TOKEN_PATH
    try:
        resp = _http.request("POST", url, data=data, timeout=timeout)
    except OSError as e:
        raise BacklogConnectionError("Failed to send POST request to {}: {}".format(url, e)) from e
    if resp.status_code // 100 != 2:
        raise BacklogError("Http response {}: {}".format(resp.status_code, resp.text))
    return resp.json()
