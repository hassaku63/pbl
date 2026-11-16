# coding: utf-8

from backlog.wiki import _filename_from_response


class Team(object):
    """
    Teams: https://developer.nulab.com/docs/backlog/api/2/get-team-icon/

    The teams of a project are listed by Project.list_teams().
    """

    def __init__(self, api) -> None:
        self.api = api

    def get_icon(self, teamId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-team-icon/

        :param teamId: (int) team ID
        :return: dict with "name" (file name) and "data" (the team icon as bytes)
        """
        resp = self.api.invoke_method("GET", "teams/{team_id}/icon".format(team_id=teamId))

        return {"name": _filename_from_response(resp), "data": resp.content}
