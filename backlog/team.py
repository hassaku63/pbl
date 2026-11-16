# coding: utf-8

from backlog.wiki import _filename_from_response


class Team(object):
    """
    Teams: https://developer.nulab.com/docs/backlog/api/2/get-list-of-teams/

    The teams of a project are listed by Project.list_teams(), and added to or removed from a project
    with Project.add_team() and Project.delete_team().
    """

    def __init__(self, api) -> None:
        self.api = api

    def list(self, order=None, offset=None, count=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-teams/

        Requires administrator or project administrator rights.

        :param order: (str) Optional. "asc" or "desc" (default)
        :param offset: (int) Optional.
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :return: list of the teams in the space
        """
        resp = self.api.invoke_method("GET", "teams", query_param={"order": order, "offset": offset, "count": count})

        return resp.json()

    def get_icon(self, teamId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-team-icon/

        :param teamId: (int) team ID
        :return: dict with "name" (file name) and "data" (the team icon as bytes)
        """
        resp = self.api.invoke_method("GET", "teams/{team_id}/icon".format(team_id=teamId))

        return {"name": _filename_from_response(resp), "data": resp.content}
