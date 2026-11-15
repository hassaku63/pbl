# coding: utf-8

from typing import List, NewType, TypedDict


class ResolutionResponse(TypedDict):
    id: int
    name: str


ListResolutionResponse = NewType("ListResolutionResponse", List[ResolutionResponse])


class Resolution(object):
    def __init__(self, api) -> None:
        self.api = api

    def list(self) -> ListResolutionResponse:
        """List resolutions (e.g. "Fixed", "Won't Fix"), for resolutionId when updating issues

        https://developer.nulab.com/docs/backlog/api/2/get-resolution-list/
        """
        resp = self.api.invoke_method("GET", "resolutions")

        return resp.json()
