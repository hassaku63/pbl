from enum import Enum
from typing import List, TypedDict, NewType, Optional


class CustomFieldResponse(TypedDict):
    id: int
    projectId: int
    typeId: int
    version: str
    name: str
    description: str
    required: bool
    useIssueType: bool
    applicableIssueTypes: List[int]
    displayOrder: int


class _InitialDate(TypedDict):
    id: int
    shift: Optional[int]
    date: Optional[str]


class NumberCustomFieldResponse(CustomFieldResponse):
    min: int
    max: int
    initialValue: int
    unit: str
    initialDate: _InitialDate


class DateCustomFieldResponse(CustomFieldResponse):
    min: str
    max: str
    initialValueType: int
    initialDate: str
    initialShift: int


class _ListCustomFieldResponseItem(TypedDict):
    id: int
    name: str
    displayOrder: int


class ListCustomFieldResponse(CustomFieldResponse):
    items: List[_ListCustomFieldResponseItem]
    allowInput: bool
    allowAddItem: bool


AddTextCustomFieldResponse = NewType("AddTextCustomFieldResponse", CustomFieldResponse)
AddSentenceCustomFieldResponse = NewType("AddSentenceCustomFieldResponse", CustomFieldResponse)
AddNumberCustomFieldResponse = NewType("AddNumberCustomFieldResponse", NumberCustomFieldResponse)
AddDateCustomFieldResponse = NewType("AddDateCustomFieldResponse", DateCustomFieldResponse)
AddSingleListCustomFieldResponse = NewType("AddSingleListCustomFieldResponse", ListCustomFieldResponse)
AddMultipleListCustomFieldResponse = NewType("AddMultipleListCustomFieldResponse", ListCustomFieldResponse)
AddCheckboxCustomFieldResponse = NewType("AddCheckboxCustomFieldResponse", ListCustomFieldResponse)
AddRadioCustomFieldResponse = NewType("AddRadioCustomFieldResponse", ListCustomFieldResponse)
AddCustomFiledResponse = \
    AddTextCustomFieldResponse | AddSentenceCustomFieldResponse | \
    AddNumberCustomFieldResponse | AddDateCustomFieldResponse | \
    AddSingleListCustomFieldResponse | AddMultipleListCustomFieldResponse | \
    AddCheckboxCustomFieldResponse | AddRadioCustomFieldResponse

DeleteTextCustomFieldResponse = NewType("DeleteTextCustomFieldResponse", CustomFieldResponse)
DeleteSentenceCustomFieldResponse = NewType("DeleteSentenceCustomFieldResponse", CustomFieldResponse)
DeleteNumberCustomFieldResponse = NewType("DeleteNumberCustomFieldResponse", NumberCustomFieldResponse)
DeleteDateCustomFieldResponse = NewType("DeleteDateCustomFieldResponse", DateCustomFieldResponse)
DeleteSingleListCustomFieldResponse = NewType("DeleteSingleListCustomFieldResponse", ListCustomFieldResponse)
DeleteMultipleListCustomFieldResponse = NewType("DeleteMultipleListCustomFieldResponse", ListCustomFieldResponse)
DeleteCheckboxCustomFieldResponse = NewType("DeleteCheckboxCustomFieldResponse", ListCustomFieldResponse)
DeleteRadioCustomFieldResponse = NewType("DeleteRadioCustomFieldResponse", ListCustomFieldResponse)
DeleteCustomFiledResponse = \
    DeleteTextCustomFieldResponse | DeleteSentenceCustomFieldResponse | \
    DeleteNumberCustomFieldResponse | DeleteDateCustomFieldResponse | \
    DeleteSingleListCustomFieldResponse | DeleteMultipleListCustomFieldResponse | \
    DeleteCheckboxCustomFieldResponse | DeleteRadioCustomFieldResponse


class CustomField(object):
    class TypeId(Enum):
        TEXT = 1
        SENTENCE = 2
        NUMBER = 3
        DATE = 4
        SINGLE_LIST = 5
        MULTIPLE_LIST = 6
        CHECKBOX = 7
        RADIO = 8

    class DateInitialValueType(Enum):
        TODAY = 1
        TODAY_PLUS_INITIAL_SHIFT = 2
        SPECIFIED_DAY = 3

    def __init__(self, api) -> None:
        self.api = api

    def list(self, projectIdOrKey: str):
        """List custom fields
        https://developer.nulab.com/docs/backlog/api/2/get-custom-field-list/

        :param projectIdOrKey: project id or key
        :type projectIdOrKey: str
        """
        _url = f"projects/{projectIdOrKey}/customFields"
        _method = "GET"

        resp = self.api.invoke_method(_method, _url)

        return resp.json()

    def add(
        self,
        projectIdOrKey: str,
        typeId: TypeId | int,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        **kwargs,
    ) -> AddCustomFiledResponse:
        """Add custom field
        https://developer.nulab.com/docs/backlog/api/2/add-custom-field/#
        """
        _url = f"projects/{projectIdOrKey}/customFields"
        _method = "POST"
        tid = typeId
        if isinstance(typeId, Enum):
            tid = typeId.value
        elif isinstance(typeId, int):
            tid = typeId
        else:
            raise ValueError(f"invalid typeId: {typeId}")
        request_param = {
            "typeId": tid,
            "name": name,
            "applicableIssueTypes": applicableIssueTypes,
            "description": description,
            "required": required,
            **kwargs,
        }
        for k, v in request_param.copy().items():
            if v is None:
                del request_param[k]
            if type(v) is bool:
                request_param[k] = "true" if v else "false"

        # for backlog parameter key spec
        if "applicableIssueTypes" in request_param:
            request_param["applicableIssueTypes[]"] = request_param["applicableIssueTypes"]
            del request_param["applicableIssueTypes"]
        if "items" in request_param:
            request_param["items[]"] = request_param["items"]
            del request_param["items"]

        resp = self.api.invoke_method(_method, _url, request_param=request_param)

        return resp.json()

    def add_text_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
    ) -> AddTextCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            1,
            name,
            applicableIssueTypes,
            description,
            required,
        )

    def add_sentence_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
    ) -> AddSentenceCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            2,
            name,
            applicableIssueTypes,
            description,
            required,
        )

    def add_number_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        min: Optional[int] = None,
        max: Optional[int] = None,
        initialValue: Optional[int] = None,
        unit: Optional[str] = None,
    ) -> AddNumberCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            3,
            name,
            applicableIssueTypes,
            description,
            required,
            min=min,
            max=max,
            initialValue=initialValue,
            unit=unit,
        )

    def add_date_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        min: Optional[str] = None,  # yyyy-MM-dd
        max: Optional[str] = None,  # yyyy-MM-dd
        initialValueType: Optional[DateInitialValueType] = None,
        initialDate: Optional[str] = None,  # yyyy-MM-dd
        initialShift: Optional[int] = None,
    ) -> AddDateCustomFieldResponse:
        if isinstance(initialValueType, Enum):
            initialValueType = initialValueType.value

        if (
            (initialValueType == self.DateInitialValueType.SPECIFIED_DAY.value)
            and (initialDate is None)
        ):
            raise ValueError("initialDate is required when initialValueType is SPECIFIED_DAY")

        return self.add(
            projectIdOrKey,
            4,
            name,
            applicableIssueTypes,
            description,
            required,
            min=min,
            max=max,
            initialValueType=initialValueType,
            initialDate=initialDate,
            initialShift=initialShift,
        )

    def add_single_list_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        items: Optional[List[str]] = None,
        allowInput: Optional[bool] = None,
        allowAddItem: Optional[bool] = None,
    ) -> AddSingleListCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            5,
            name,
            applicableIssueTypes,
            description,
            required,
            items=items,
            allowInput=allowInput,
            allowAddItem=allowAddItem,
        )

    def add_multiple_list_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        items: Optional[List[str]] = None,
        allowInput: Optional[bool] = None,
        allowAddItem: Optional[bool] = None,
    ) -> AddMultipleListCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            6,
            name,
            applicableIssueTypes,
            description,
            required,
            items=items,
            allowInput=allowInput,
            allowAddItem=allowAddItem,
        )

    def add_checkbox_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        items: Optional[List[str]] = None,
        allowInput: Optional[bool] = None,
        allowAddItem: Optional[bool] = None,
    ) -> AddCheckboxCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            7,
            name,
            applicableIssueTypes,
            description,
            required,
            items=items,
            allowInput=allowInput,
            allowAddItem=allowAddItem,
        )

    def add_radio_custom_field(
        self,
        projectIdOrKey: str,
        name: str,
        applicableIssueTypes: Optional[List[int]] = None,
        description: Optional[str] = None,
        required: Optional[bool] = None,
        items: Optional[List[str]] = None,
        allowInput: Optional[bool] = None,
        allowAddItem: Optional[bool] = None,
    ) -> AddRadioCustomFieldResponse:
        return self.add(
            projectIdOrKey,
            8,
            name,
            applicableIssueTypes,
            description,
            required,
            items=items,
            allowInput=allowInput,
            allowAddItem=allowAddItem,
        )

    # def update(self, projectIdOrKey: str, id: int, name: str):
    #     """Update category
    #     https://developer.nulab.com/docs/backlog/api/2/update-category/#

    #     :param projectIdOrKey: project id or key
    #     :type projectIdOrKey: str
    #     :param id: category id
    #     :type id: int
    #     :param name: category name
    #     :type name: str
    #     """
    #     _url = f"projects/{projectIdOrKey}/categories/{id}"
    #     _method = "PATCH"

    #     resp = self.api.invoke_method(_method, _url, request_param={"name": name})

    #     return resp.json()

    def delete(self, projectIdOrKey: str, id: int) -> DeleteCustomFiledResponse:
        """Delete custom field
        https://developer.nulab.com/docs/backlog/api/2/delete-custom-field/#delete-custom-field
        """
        _url = f"projects/{projectIdOrKey}/customFields/{id}"
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _url)

        return resp.json()
