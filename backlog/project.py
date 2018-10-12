# coding: utf-8



class Project(object):
    def __init__(self, api):
        """

        :param api:
        """
        self.api = api

    def list(self, archived=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-project-list/

        :param archived:
        :param all:
        :return:
        """
        raise NotImplementedError

    def create(self, name, key, chatEnabled, projectLeaderCanEditProjectLeader,
                       subtaskingEnabled, textFormattingRule):
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

        :param projectIdOrKey:
        :return:
        """
        raise NotImplementedError

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

    def users(self, projectIdOrKey, excludeGroupMembers=False):
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

        return resp
