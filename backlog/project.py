# coding: utf-8
from typing import TypedDict, Literal, Optional, NewType


TextFormattingRule = Literal["markdown", "backlog"]


class ProjectResponse(TypedDict):
    id: int
    projectKey: str
    name: str
    chartEnabled: bool
    useResolvedForChart: bool
    subtaskingEnabled: bool
    projectLeaderCanEditProjectLeader: bool
    useWiki: bool
    useFileSharing: bool
    useWikiTreeView: bool
    useOriginalImageSizeAtWiki: bool
    useSubversion: bool
    useGit: bool
    textFormattingRule: TextFormattingRule
    archived: bool
    displayOrder: int
    useDevAttributes: bool


AddProjectResponse = NewType("AddProjectResponse", ProjectResponse)
UpdateProjectResponse = NewType("UpdateProjectResponse", ProjectResponse)


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

    def create(
        self,
        name: str,
        key: str,
        chatEnabled: Optional[bool] = None,
        useResolvedForChart: Optional[bool] = None,
        subtaskingEnabled: Optional[bool] = None,
        projectLeaderCanEditProjectLeader: Optional[bool] = None,
        useWiki: Optional[bool] = None,
        useFileSharing: Optional[bool] = None,
        useWikiTreeView: Optional[bool] = None,
        useSubversion: Optional[bool] = None,
        useGit: Optional[bool] = None,
        useOriginalImageSizeAtWiki: Optional[bool] = None,
        textFormattingRule: Optional[TextFormattingRule] = None,
        useDevAttributes: Optional[bool] = None,
    ) -> AddProjectResponse:
        """Add project
        https://developer.nulab.com/docs/backlog/api/2/add-project/#form-parameters

        :param name: Project Name
        :type name: str
        :param key: Project Key (Uppercase letters (A-Z), numbers (0-9) and underscore (_) can be used.)
        :type key: str
        :param chatEnabled: Enable chart
        :type chatEnabled: bool
        :param useResolvedForChart: Consider Resolved and statuses after as Closed
        :type useResolvedForChart: bool
        :param subtaskingEnabled: Enable subtasking
        :type subtaskingEnabled: bool
        :param projectLeaderCanEditProjectLeader: Allow project administrators to manage each other
        :type projectLeaderCanEditProjectLeader: bool
        :param useWiki: Enable Wiki
        :type useWiki: bool
        :param useFileSharing: Enable shared files
        :type useFileSharing: bool
        :param useWikiTreeView: Enable Wiki tree view
        :type useWikiTreeView: bool
        :param useSubversion: Enable Subversion
        :type useSubversion: bool
        :param useGit: Enable Git
        :type useGit: bool
        :param useOriginalImageSizeAtWiki: Display images in Wikis in their original size
        :type useOriginalImageSizeAtWiki: bool
        :param textFormattingRule: Formatting rules “backlog” or “markdown”
        :type textFormattingRule: TextFormattingRule
        :param useDevAttributes: Enable priorities, versions and milestones
        :type useDevAttributes: bool
        :return: response add project
        :rtype: AddProjectResponse
        """
        _path = "projects"
        _method = "POST"
        request_param = {
            "name": name,
            "key": key,
            "chartEnabled": chatEnabled,
            "useResolvedForChart": useResolvedForChart,
            "subtaskingEnabled": subtaskingEnabled,
            "projectLeaderCanEditProjectLeader": projectLeaderCanEditProjectLeader,
            "useWiki": useWiki,
            "useFileSharing": useFileSharing,
            "useWikiTreeView": useWikiTreeView,
            "useSubversion": useSubversion,
            "useGit": useGit,
            "useOriginalImageSizeAtWiki": useOriginalImageSizeAtWiki,
            "textFormattingRule": textFormattingRule,
            "useDevAttributes": useDevAttributes
        }
        for k, v in request_param.copy().items():
            if v is None:
                del request_param[k]

        resp = self.api.invoke_method(_method, _path, request_param=request_param)

        return resp.json()

    add = create

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

    def update(
        self,
        projectIdOrKey: str,  # path parameter
        name: str = None,
        key: str = None,
        chartEnabled: bool = None,
        useResolvedForChart: bool = None,
        subtaskingEnabled: bool = None,
        projectLeaderCanEditProjectLeader: bool = None,
        useWiki: bool = None,
        useFileSharing: bool = None,
        useWikiTreeView: bool = None,
        useSubversion: bool = None,
        useGit: bool = None,
        useOriginalImageSizeAtWiki: bool = None,
        textFormattingRule: TextFormattingRule = None,
        archived: bool = None,
        useDevAttributes: bool = None,
    ) -> UpdateProjectResponse:
        """Update project
        https://developer.nulab.com/docs/backlog/api/2/update-project/#form-parameters

        :param projectIdOrKey: Project Name
        :type projectIdOrKey: str
        :param key: Project Key, defaults to None
        :type key: str, optional
        :param chartEnabled: Enable chart, defaults to None
        :type chartEnabled: bool, optional
        :param useResolvedForChart: Consider Resolved and statuses after as Closed, defaults to None
        :type useResolvedForChart: bool, optional
        :param subtaskingEnabled: Enable subtasking, defaults to None
        :type subtaskingEnabled: _type_, optional
        :param projectLeaderCanEditProjectLeader: Allow project administrators to manage each other, defaults to None
        :type projectLeaderCanEditProjectLeader: bool, optional
        :param useWiki: Enable Wiki, defaults to None
        :type useWiki: bool, optional
        :param useFileSharing: Enable shared files, defaults to None
        :type useFileSharing: bool, optional
        :param useWikiTreeView: Enable Wiki tree view, defaults to None
        :type useWikiTreeView: bool, optional
        :param useSubversion: Enable Subversion, defaults to None
        :type useSubversion: bool, optional
        :param useGit: Enable Git, defaults to None
        :type useGit: bool, optional
        :param useOriginalImageSizeAtWiki: Display images in Wikis in their original size, defaults to None
        :type useOriginalImageSizeAtWiki: bool, optional
        :param textFormattingRule: Formatting rules “backlog” or “markdown”, defaults to None
        :type textFormattingRule: TextFormattingRule, optional
        :param archived: Archive this project, defaults to None
        :type archived: bool, optional
        :param useDevAttributes: Enable priorities, versions and milestones, defaults to None
        :type useDevAttributes: bool, optional
        """
        _path = f"projects/{projectIdOrKey}"
        _method = "PATCH"
        request_param = {
            "name": name,
            "key": key,
            "chartEnabled": chartEnabled,
            "useResolvedForChart": useResolvedForChart,
            "subtaskingEnabled": subtaskingEnabled,
            "projectLeaderCanEditProjectLeader": projectLeaderCanEditProjectLeader,
            "useWiki": useWiki,
            "useFileSharing": useFileSharing,
            "useWikiTreeView": useWikiTreeView,
            "useSubversion": useSubversion,
            "useGit": useGit,
            "useOriginalImageSizeAtWiki": useOriginalImageSizeAtWiki,
            "textFormattingRule": textFormattingRule,
            "archived": archived,
            "useDevAttributes": useDevAttributes
        }
        for k, v in request_param.copy().items():
            if v is None:
                del request_param[k]
        if len(request_param.keys()) == 0:
            raise ValueError("No parameter to update")

        resp = self.api.invoke_method(_method, _path, request_param=request_param)

        return resp.json()

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
