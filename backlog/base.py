# coding: utf-8

from urllib.parse import urlencode
import requests
from backlog.wiki import Wiki
from backlog.attachment import Attachment
from backlog.project import Project
from backlog.issue import Issue
from backlog.git import Git
from backlog.user import User

BACKLOG_BASE_URL = "https://{space}.backlog.jp"
BACKLOG_URI_PREFIX = "/api/v2/"


class BacklogError(Exception):
    pass


class BaseAPI(object):
    def __init__(self, space, api_key=None):
        self.space = space
        self.api_key = api_key
        self.base_url = BACKLOG_BASE_URL.format(space=space) + BACKLOG_URI_PREFIX
        self.api = None
        self._build_api()

    def _build_api(self):
        self.api = None

    def invoke_method(self, method, uri, query_param={}, request_param={}, headers=None, **kwargs):
        """
        Delegate requests to get/post/delete method.
        Each method implements by any http client, default client is requests.

        :param method: HTTP Method. supports GET/POST/DELETE
        :param uri: API Endpoint. 'uri' expects a URI excluded '/api/v2/' prefix
        :param query_param: dict of URL parameter. this will be url-encoded string
        :param request_param: dict of body parameter. this will use when invoke post request
        :param headers: HTTP Header dict. Recommend value is None. if None, then use default implements of http client(requests).
        :return: http response object
        """
        query_param.setdefault("apiKey", self.api_key)

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
        raise NotImplementedError

    def post(self, method, uri, query_param, request_param, headers, **kwargs):
        raise NotImplementedError

    def delete(self, method, uri, query_param, request_param, headers, **kwargs):
        raise NotImplementedError

    def patch(self, method, uri, query_param, request_param, headers, **kwargs):
        raise NotImplementedError


class BacklogAPI(BaseAPI):
    """
    Using 'requests'
    """
    def _build_api(self):
        self.api = None

        self.wiki = Wiki(self)
        self.attachment = Attachment(self)
        self.project = Project(self)
        self.issue = Issue(self)
        self.git = Git(self)
        self.user = User(self)

    def get(self, method, uri, query_param, request_param, headers, **kwargs):
        _url = self.base_url + uri
        if headers is not None:
            resp = requests.get(_url, params=query_param, headers=headers, **kwargs)
        else:
            resp = requests.get(_url, params=query_param, **kwargs)

        if resp.status_code // 100 == 2:
            return resp

        raise BacklogError("Http response {status}: {message}".format(status=resp.status_code, message=resp.text))

    def post(self, method, uri, query_param, request_param, headers, **kwargs):
        _url = self.base_url + uri + "?" + urlencode(query_param)
        if headers is not None:
            resp = requests.post(_url, data=request_param, headers=headers, **kwargs)
        else:
            resp = requests.post(_url, data=request_param, **kwargs)

        if resp.status_code // 100 == 2:
            return resp

        raise BacklogError("Http response {status}: {message}".format(status=resp.status_code, message=resp.text))

    def delete(self, method, uri, query_param, request_param, headers, **kwargs):
        _url = self.base_url + uri + "?" + urlencode(query_param)
        if headers is not None:
            resp = requests.delete(_url, headers=headers, **kwargs)
        else:
            resp = requests.delete(_url, **kwargs)

        if resp.status_code == 200:
            return resp

        raise BacklogError("Http response {status}: {message}".format(status=resp.status_code, message=resp.text))

    def patch(self, method, uri, query_param, request_param, headers, **kwargs):
        """
        TODO: Implementation.

        :param method:
        :param uri:
        :param query_param:
        :param request_param:
        :param headers:
        :param kwargs:
        :return:
        """
        _url = self.base_url + uri + "?" + urlencode(query_param)
        if headers is not None:
            resp = requests.ptach(_url, data=request_param, headers=headers, **kwargs)
        else:
            resp = requests.patch(_url, data=request_param, **kwargs)

        if resp.status_code == 200:
            return resp

        raise BacklogError("Http response {status}: {message}".format(status=resp.status_code, message=resp.text))


class BacklogObject(object):
    def __init__(self, api):
        self.api = api
