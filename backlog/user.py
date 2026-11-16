# coding: utf-8


class User(object):
    def __init__(self, api):
        """

        :param api:
        """
        self.api = api

    def list(self):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/get-user-list/

        :return: Compliant with Backlog API specification
        """
        _uri = "users"
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def get_myself(self):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-own-user/

        :return: the user that owns the API key or access token
        """
        resp = self.api.invoke_method("GET", "users/myself")

        return resp.json()

    def list_recently_viewed_issues(self, order=None, offset=None, count=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-recently-viewed-issues/

        :param order: (str) Optional. "asc" or "desc" (default)
        :param offset: (int) Optional.
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :return: list of issues the user that owns the API key or access token viewed recently
        """
        _query_param = {"order": order, "offset": offset, "count": count}

        resp = self.api.invoke_method("GET", "users/myself/recentlyViewedIssues", query_param=_query_param)

        return resp.json()

    def add_recently_viewed_issue(self, issueIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-recently-viewed-issue/

        :param issueIdOrKey: Issue ID or Issue Key
        :return: the issue
        """
        _request_param = {"issueIdOrKey": issueIdOrKey}

        resp = self.api.invoke_method("POST", "users/myself/recentlyViewedIssues", request_param=_request_param)

        return resp.json()

    def list_recently_viewed_projects(self, order=None, offset=None, count=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-recently-viewed-projects/

        :param order: (str) Optional. "asc" or "desc" (default)
        :param offset: (int) Optional.
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :return: list of projects the user viewed recently
        """
        _query_param = {"order": order, "offset": offset, "count": count}

        resp = self.api.invoke_method("GET", "users/myself/recentlyViewedProjects", query_param=_query_param)

        return resp.json()

    def list_recently_viewed_wikis(self, order=None, offset=None, count=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-recently-viewed-wikis/

        :param order: (str) Optional. "asc" or "desc" (default)
        :param offset: (int) Optional.
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :return: list of wiki pages the user viewed recently
        """
        _query_param = {"order": order, "offset": offset, "count": count}

        resp = self.api.invoke_method("GET", "users/myself/recentlyViewedWikis", query_param=_query_param)

        return resp.json()

    def add_recently_viewed_wiki(self, wikiId):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-recently-viewed-wiki/

        :param wikiId: (int) wiki page ID
        :return: the wiki page
        """
        resp = self.api.invoke_method("POST", "users/myself/recentlyViewedWikis", request_param={"wikiId": wikiId})

        return resp.json()

    def get(self, userId):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/get-user/

        :param userId: (str or int) Required.
        :return: Compliant with Backlog API specification
        """
        _uri = "users/{user_id}".format(user_id=userId)
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def add(self, userId, password, name, mailAddress, roleType):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/add-user/

        :param userId: (str) Required.
        :param password: (str) Required.
        :param name: (str) Required.
        :param mailAddress: (str) Required.
        :param roleType: (int) Required. administrator=1, general-user=2, reporter=3, viewer=4, guest-reporter=5, guest-viewer=6
        :return: Compliant with Backlog API specification
        """
        _uri = "users"
        _method = "POST"
        params = dict(
            userId=userId,
            password=password,
            name=name,
            mailAddress=mailAddress,
            roleType=roleType
        )

        resp = self.api.invoke_method(_method, _uri, request_param=params)

        return resp.json()

    def update(self, userId, password=None, name=None, mailAddress=None, roleType=None):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/update-user/

        :param userId: (str) Required.
        :param password: (str) Optional.
        :param name: (str) Optional.
        :param mailAddress: (str) Optional.
        :param roleType: (str) Optional.
        :return: Compliant with Backlog API specification
        """
        _uri = "users/{user_id}".format(user_id=userId)
        _method = "PATCH"
        params = dict(
            password=password,
            name=name,
            mailAddress=mailAddress,
            roleType=roleType
        )
        params = {k: v for k, v in params.items() if v is not None}

        resp = self.api.invoke_method(_method, _uri, request_param=params)

        return resp.json()

    def delete(self, id):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-user/

        :param id: (int) Required.
        :return: Compliant with Backlog API specification
        """
        _uri = "users/{id}".format(id=id)
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()
