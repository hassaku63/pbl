# coding: utf-8

from typing import List, NewType, TypedDict


class PriorityResponse(TypedDict):
    id: int
    name: str


ListPriorityResponse = NewType("ListPriorityResponse", List[PriorityResponse])


class Priority(object):
    def __init__(self, api) -> None:
        self.api = api

    def list(self) -> ListPriorityResponse:
        """List priorities (e.g. "High", "Normal", "Low"), for priorityId when adding or updating issues

        https://developer.nulab.com/docs/backlog/api/2/get-priority-list/
        """
        resp = self.api.invoke_method("GET", "priorities")

        return resp.json()
