# coding: utf-8

import warnings
from typing import TypedDict, Literal, Optional, NewType
from urllib.parse import quote

from backlog._params import bool_params
from backlog.wiki import _filename_from_response


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
        chartEnabled: Optional[bool] = None,
    ) -> AddProjectResponse:
        """Add project
        https://developer.nulab.com/docs/backlog/api/2/add-project/#form-parameters

        :param name: Project Name
        :type name: str
        :param key: Project Key (Uppercase letters (A-Z), numbers (0-9) and underscore (_) can be used.)
        :type key: str
        :param chatEnabled: Deprecated alias of chartEnabled, kept for backward compatibility
        :type chatEnabled: bool
        :param chartEnabled: Enable chart
        :type chartEnabled: bool
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
        if chartEnabled is not None and chatEnabled is not None and chartEnabled != chatEnabled:
            raise ValueError("chartEnabled and its deprecated alias chatEnabled have conflicting values")
        if chartEnabled is None:
            chartEnabled = chatEnabled
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
        if not request_param:
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
            "excludeGroupMembers": "true" if excludeGroupMembers else "false"
        }

        resp = self.api.invoke_method(_method, _uri, query_param=_query_param)

        return resp.json()

    def add_user(self, projectIdOrKey, userId):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-project-user/

        Requires administrator or project administrator rights.

        :param projectIdOrKey: Project ID or Project Key
        :param userId: (int) numeric user ID ("id", not the login name "userId")
        :return: the added user
        """
        _uri = "projects/{project_id_or_key}/users".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("POST", _uri, request_param={"userId": userId})

        return resp.json()

    def delete_user(self, projectIdOrKey, userId):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-project-user/

        :param projectIdOrKey: Project ID or Project Key
        :param userId: (int) numeric user ID
        :return: the removed user
        """
        _uri = "projects/{project_id_or_key}/users".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("DELETE", _uri, request_param={"userId": userId})

        return resp.json()

    def add_team(self, projectIdOrKey, teamId):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-project-team/

        Requires administrator or project administrator rights.

        :param projectIdOrKey: Project ID or Project Key
        :param teamId: (int) team ID (see Team.list())
        :return: the added team
        """
        _uri = "projects/{project_id_or_key}/teams".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("POST", _uri, request_param={"teamId": teamId})

        return resp.json()

    def delete_team(self, projectIdOrKey, teamId):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-project-team/

        :param projectIdOrKey: Project ID or Project Key
        :param teamId: (int) team ID
        :return: the removed team
        """
        _uri = "projects/{project_id_or_key}/teams".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("DELETE", _uri, request_param={"teamId": teamId})

        return resp.json()

    def list_statuses(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-status-list-of-project/

        :param projectIdOrKey: Project ID or Project Key
        :return: list of statuses in the project (for statusId when adding or updating issues)
        """
        _uri = "projects/{project_id_or_key}/statuses".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def list_versions(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-version-milestone-list/

        :param projectIdOrKey: Project ID or Project Key
        :return: list of versions/milestones in the project (for versionId[] / milestoneId[] of issues)
        """
        _uri = "projects/{project_id_or_key}/versions".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def add_status(self, projectIdOrKey, name, color):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-status/

        A project can have up to 8 custom statuses besides the 4 default ones. Requires administrator.

        :param projectIdOrKey: Project ID or Project Key
        :param name: (str) status name
        :param color: (str) background color, one of "#ea2c00", "#e87758", "#e07b9a", "#868cb7", "#3b9dbd",
            "#4caf93", "#b0be3c", "#eda62a", "#f42858", "#393939"
        :return: the added status
        """
        _uri = "projects/{project_id_or_key}/statuses".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("POST", _uri, request_param={"name": name, "color": color})

        return resp.json()

    def update_status(self, projectIdOrKey, id, name=None, color=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/update-status/

        :param projectIdOrKey: Project ID or Project Key
        :param id: (int) status ID
        :param name: (str) Optional. status name
        :param color: (str) Optional. background color (see add_status())
        :return: the updated status
        """
        _uri = "projects/{project_id_or_key}/statuses/{id}".format(project_id_or_key=projectIdOrKey, id=id)

        resp = self.api.invoke_method("PATCH", _uri, request_param={"name": name, "color": color})

        return resp.json()

    def delete_status(self, projectIdOrKey, id, substituteStatusId):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-status/

        :param projectIdOrKey: Project ID or Project Key
        :param id: (int) status ID
        :param substituteStatusId: (int) status ID that issues with the deleted status get instead
        :return: the deleted status
        """
        _uri = "projects/{project_id_or_key}/statuses/{id}".format(project_id_or_key=projectIdOrKey, id=id)

        resp = self.api.invoke_method("DELETE", _uri, request_param={"substituteStatusId": substituteStatusId})

        return resp.json()

    def update_status_order(self, projectIdOrKey, statusId):
        """
        https://developer.nulab.com/docs/backlog/api/2/update-order-of-status/

        :param projectIdOrKey: Project ID or Project Key
        :param statusId: (list of int) all status IDs of the project in the new order.
            "Open" must be first, "Closed" last, and "In Progress" before "Resolved".
        :return: list of statuses in the new order
        """
        _uri = "projects/{project_id_or_key}/statuses/updateDisplayOrder".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("PATCH", _uri, request_param={"statusId[]": statusId})

        return resp.json()

    def add_version(self, projectIdOrKey, name, description=None, startDate=None, releaseDueDate=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-version-milestone/

        :param projectIdOrKey: Project ID or Project Key
        :param name: (str) version/milestone name
        :param description: (str) Optional.
        :param startDate: (str) Optional. start date (yyyy-MM-dd)
        :param releaseDueDate: (str) Optional. release due date (yyyy-MM-dd)
        :return: the added version/milestone
        """
        _uri = "projects/{project_id_or_key}/versions".format(project_id_or_key=projectIdOrKey)
        _request_param = {"name": name, "description": description, "startDate": startDate, "releaseDueDate": releaseDueDate}

        resp = self.api.invoke_method("POST", _uri, request_param=_request_param)

        return resp.json()

    def update_version(self, projectIdOrKey, id, name, description=None, startDate=None, releaseDueDate=None,
                       archived=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/update-version-milestone/

        :param projectIdOrKey: Project ID or Project Key
        :param id: (int) version/milestone ID
        :param name: (str) version/milestone name (required by the API even if unchanged)
        :param description: (str) Optional.
        :param startDate: (str) Optional. start date (yyyy-MM-dd)
        :param releaseDueDate: (str) Optional. release due date (yyyy-MM-dd)
        :param archived: (bool) Optional.
        :return: the updated version/milestone
        """
        _uri = "projects/{project_id_or_key}/versions/{id}".format(project_id_or_key=projectIdOrKey, id=id)
        _request_param = bool_params({
            "name": name, "description": description, "startDate": startDate, "releaseDueDate": releaseDueDate,
            "archived": archived,
        })

        resp = self.api.invoke_method("PATCH", _uri, request_param=_request_param)

        return resp.json()

    def delete_version(self, projectIdOrKey, id):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-version/

        :param projectIdOrKey: Project ID or Project Key
        :param id: (int) version/milestone ID
        :return: the deleted version/milestone
        """
        _uri = "projects/{project_id_or_key}/versions/{id}".format(project_id_or_key=projectIdOrKey, id=id)

        resp = self.api.invoke_method("DELETE", _uri)

        return resp.json()

    def get_image(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-project-icon/

        :param projectIdOrKey: Project ID or Project Key
        :return: dict with "name" (file name) and "data" (the project icon as bytes)
        """
        _uri = "projects/{project_id_or_key}/image".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return {"name": _filename_from_response(resp), "data": resp.content}

    def list_administrators(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-project-administrators/

        :param projectIdOrKey: Project ID or Project Key
        :return: list of the project administrators (users)
        """
        _uri = "projects/{project_id_or_key}/administrators".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def list_teams(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-project-team-list/

        :param projectIdOrKey: Project ID or Project Key
        :return: list of the teams that belong to the project
        """
        _uri = "projects/{project_id_or_key}/teams".format(project_id_or_key=projectIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def list_shared_files(self, projectIdOrKey, path="", order=None, offset=None, count=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-shared-files/

        :param projectIdOrKey: Project ID or Project Key
        :param path: (str) Optional. directory path, e.g. "docs/specs" (default: the root directory)
        :param order: (str) Optional. "asc" or "desc" (default)
        :param offset: (int) Optional.
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :return: list of the files and directories in the directory ("type" is "file" or "directory")
        """
        _uri = "projects/{project_id_or_key}/files/metadata/{path}".format(
            project_id_or_key=projectIdOrKey, path=quote(path.strip("/"), safe="/"))
        _query_param = {"order": order, "offset": offset, "count": count}

        resp = self.api.invoke_method("GET", _uri, query_param=_query_param)

        return resp.json()

    def get_shared_file(self, projectIdOrKey, sharedFileId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-file/

        :param projectIdOrKey: Project ID or Project Key
        :param sharedFileId: (int) shared file ID
        :return: dict with "id", "name" (file name) and "data" (the file content as bytes)
        """
        _uri = "projects/{project_id_or_key}/files/{shared_file_id}".format(
            project_id_or_key=projectIdOrKey, shared_file_id=sharedFileId)

        resp = self.api.invoke_method("GET", _uri)

        return {"id": sharedFileId, "name": _filename_from_response(resp), "data": resp.content}

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
        warnings.warn(
            "Project.list_categories() is deprecated and will be removed in a future release; use BacklogAPI.category.list() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
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
        warnings.warn(
            "Project.add_category() is deprecated and will be removed in a future release; use BacklogAPI.category.add() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        _uri = "projects/{project_id_or_key}/categories".format(
            project_id_or_key=projectIdOrKey,
        )
        _method = "POST"

        resp = self.api.invoke_method(_method, _uri, request_param={"name": name})

        return resp.json()

    def update_category(self, projectIdOrKey, id, name):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/update-category/

        :param projectIdOrKey:
        :param id:
        :param name: (str) will modified
        :return:
        """
        warnings.warn(
            "Project.update_category() is deprecated and will be removed in a future release; use BacklogAPI.category.update() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        _uri = "projects/{project_id_or_key}/categories/{id}".format(
            project_id_or_key=projectIdOrKey,
            id=id
        )
        _method = "PATCH"

        resp = self.api.invoke_method(_method, _uri, request_param={"name": name})

        return resp.json()

    def delete_category(self, projectIdOrKey, id):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/delete-category/

        :param projectIdOrKey:
        :param id:
        :return:
        """
        warnings.warn(
            "Project.delete_category() is deprecated and will be removed in a future release; use BacklogAPI.category.delete() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        _uri = "projects/{project_id_or_key}/categories/{id}".format(
            project_id_or_key=projectIdOrKey,
            id=id
        )
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()
