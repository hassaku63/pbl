# coding: utf-8


class Project(object):
    def __init__(self, api):
        """

        :param api:
        """
        self.api = api

    def list(self, archived=False, all_=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-project-list/

        :param archived: (book) Optional. default = False
        :param all_: (bool) Optional. Admin only. not implemented.
        :return:
        """
        _uri = "projects"
        _method = "GET"
        query_param = {
            "archived": "true" if archived else "false",
            "all": "true" if all_ else "false"
        }

        resp = self.api.invoke_method(_method, _uri, query_param=query_param)

        return resp.json()

    def create(self, name, key, chatEnabled, projectLeaderCanEditProjectLeader, subtaskingEnabled, textFormattingRule):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-project/

        :param name:
        :param key:
        :param chatEnabled:
        :param projectLeaderCanEditProjectLeader:
        :param subtaskingEnabled:
        :param textFormattingRule:
        :return:
        """
        raise NotImplementedError

    def get(self, projectIdOrKey):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-project/

        :param projectIdOrKey: (str or int) Required. project id or project key
        :return: Compliant with Backlog API specification
        """
        _uri = "projects/{project_id_or_key}".format(project_id_or_key=projectIdOrKey)
        _method = "GET"
        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def update(self, projectIdOrKey, name, key, chartEnabled,
               subtaskingEnabled, projectLeaderCanEditProjectLeader,
               textFormattingRule, archived):
        """
        Admin or Project admin only
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/update-project/

        :param projectIdOrKey: str
        :param name: str
        :param key: str
        :param chartEnabled: bool
        :param subtaskingEnabled: bool
        :param projectLeaderCanEditProjectLeader: bool
        :param textFormattingRule: str, "markdown" or "backlog"
        :param archived:
        :return:
        """
        raise NotImplementedError

    def list_users(self, projectIdOrKey, excludeGroupMembers=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-project-user-list/

        :param projectIdOrKey:
        :param excludeGroupMembers:
        :return:
        """
        _uri = "projects/{project_id_or_key}/users".format(project_id_or_key=projectIdOrKey)
        _method = "GET"
        _query_param = {
            "excludeGroupMembers": "ture" if excludeGroupMembers else "false"
        }

        resp = self.api.invoke_method(_method, _uri, query_param=_query_param)

        return resp.json()

    def list_issue_types(self, projectIdOrKey):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-issue-type-list/

        :param projectIdOrKey:
        :return:
        """
        _uri = "projects/{project_id_or_key}/issueTypes".format(
            project_id_or_key=projectIdOrKey
        )
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def add_issue_type(self, projectIdOrKey, name, color):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-issue-type/

        :param projectIdOrKey:
        :param name:
        :param color:
        :return:
        """
        _uri = "projects/{project_id_or_key}/issueTypes".format(
            project_id_or_key=projectIdOrKey
        )
        _method = "POST"
        _request_param = {
            "name": name,
            "color": color
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def update_issue_type(self, projectIdOrKey, id, name, color):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/update-issue-type/

        :param projectIdOrKey:
        :param id: int Issue type ID
        :param name:
        :param color:
        :return:
        """
        _uri = "projects/{project_id_or_key}/issueTypes/{id}".format(
            project_id_or_key=projectIdOrKey,
            id=id
        )
        _method = "PATCH"
        _request_param = {
            "name": name,
            "color": color
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def delete_issue_type(self, projectIdOrKey, id, substituteIssueTypeId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/delete-issue-type/

        :param projectIdOrKey: Project ID or Key
        :param id: Issue Type ID
        :param substituteIssueTypeId: New Issue type ID
        :return:
        """
        _uri = "projects/{project_id_or_key}/issueTypes/{id}".format(
            project_id_or_key=projectIdOrKey,
            id=id
        )
        _method = "DELETE"
        _request_param = {
            "substituteIssueTypeId": substituteIssueTypeId
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def list_categories(self, projectIdOrKey):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-category-list/

        :param projectIdOrKey:
        :return:
        """
        _uri = "projects/{project_id_or_key}/categories".format(
            project_id_or_key=projectIdOrKey,
        )
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def add_category(self, projectIdOrKey, name):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-category/

        :param projectIdOrKey:
        :param name: (str) Category name
        :return:
        """
        _uri = "projects/{project_id_or_key}/categories".format(
            project_id_or_key=projectIdOrKey,
        )
        _method = "POST"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def update_category(self, projectIdOrKey, id, name):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/update-category/

        :param projectIdOrKey:
        :param id:
        :param name: (str) will modified
        :return:
        """
        _uri = "projects/{project_id_or_key}/categories/{id}".format(
            project_id_or_key=projectIdOrKey,
            id=id
        )
        _method = "PATCH"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def delete_category(self, projectIdOrKey, id):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/delete-category/

        :param projectIdOrKey:
        :param id:
        :return:
        """
        _uri = "projects/{project_id_or_key}/categories/{id}".format(
            project_id_or_key=projectIdOrKey,
            id=id
        )
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()
