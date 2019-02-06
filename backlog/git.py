# coding: utf-8


class Git(object):
    def __init__(self, api):
        """

        :param api:
        """
        self.api = api

    def list_git_repositories(self, projectIdOrKey):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-list-of-git-repositories/

        :param projectIdOrKey: (str or int) Required
        :return:
        """
        _uri = "projects/{projectIdOrKey}/git/repositories".format(
            projectIdOrKey=projectIdOrKey
        )
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def add_pull_request(self, projectIdOrKey, repoIdOrName, **kwargs):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-pull-request/

        :param projectIdOrKey: (str or int) Requied.
        :param repoIdOrName: (str or int) Requied.
        :param kwargs: (dict) Optional. Other request parameter, compliant with Backlog API specification
        :return: Compliant with Backlog API specification
        """
        _uri = "projects/{projectIdOrKey}/git/repositories/{repoIdOrName}/pullRequests".format(
            projectIdOrKey=projectIdOrKey,
            repoIdOrName=repoIdOrName
        )
        _method = "POST"

        resp = self.api.invoke_method(_method, _uri, request_param=kwargs)

        return resp.json()
